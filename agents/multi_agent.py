import os
import json
import logging
from typing import Dict, Any, List
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# api_key = os.getenv("GOOGLE_API_KEY")
logger = logging.getLogger(__name__)

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    logger.warning("G_API_KEY environment variable not set. LLM calls may fail.")
else:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-2.5-flash")
print("Using API KEY:", os.getenv("GOOGLE_API_KEY")[:10])
def call_llm(prompt: str, json_format: bool = False, fallback_text: str = None) -> str:
    """Helper function to call the Gemini LLM."""
    try:
        system_instruction = (
            "System Instruction: You are a sharp, decisive financial analyst. "
            "Keep outputs to a MAX of 2 sentences. No paragraphs. No formatting (no asterisks, bold, etc.). "
            "Maintain a sharp, analytical tone only. Avoid fluff like 'this depends'. Be decisive. "
            "IMPORTANT: Always reference specific numbers and metrics (e.g. price_vs_short_ma_pct, volume_vs_avg_pct) to support your claims. "
            "Avoid vague words like 'strong' or 'robust' without accompanying numerical justification.\n\n"
        )
        full_prompt = system_instruction + prompt
        
        response = model.generate_content(full_prompt)
        result = response.text.strip()
        
        # Clean up markdown block format if json is expected
        if json_format and result.startswith("```json"):
            result = result.replace("```json", "").replace("```", "").strip()
            
        return result
    except Exception as e:
        logger.error(f"Error calling LLM: {e}")
        if json_format:
            return "{}"
        if fallback_text:
            return fallback_text
        return "Analysis constrained by system limits. Neutral outlook assumed."

def run_multi_agent_analysis(ticker: str, signals: List[str], metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run multi-agent reasoning for stock analysis using Google Gemini.
    """
    context = f"Ticker: {ticker}\nSignals: {signals}\nMetrics: {metrics}"

    # A. Technical Agent
    tech_prompt = f"""
Analyze the following technical signals and metrics for a stock.
Focus strictly on trend, momentum, signal_strength, and breakout strength. Make a sharp, definitive assessment.
Quote specific percentage differences (e.g., price vs MA, volume vs avg) in your assessment.
{context}
"""
    technical_analysis = call_llm(tech_prompt, fallback_text="Insufficient LLM response. Using rule-based analysis: price below MA indicates bearish momentum.")

    # B. Fundamental Agent
    fund_prompt = f"""
Assume generic fundamental characteristics for the following stock based on typical market behavior for its sector.
Evaluate stability, growth assumptions, and valuation risk. Make a sharp, concise assessment.
Quote specific percentage differences provided in metrics to justify any valuation risk assumptions.
{context}
"""
    fundamental_analysis = call_llm(fund_prompt, fallback_text="Fundamental analysis unavailable due to system limits. Assuming neutral sector performance.")

    # C. Sentiment Agent
    sent_prompt = f"""
Assume neutral-to-positive sentiment unless the technical signals specifically suggest panic or high momentum.
Reason about the current market perception of this stock. Keep it sharp and analytical.
Quote specific volume vs avg % metrics to justify the sentiment assessment.
{context}
"""
    sentiment_analysis = call_llm(sent_prompt, fallback_text="Sentiment analysis unavailable. Assuming risk-off baseline.")

    # D. Bull Agent
    bull_prompt = f"""
Provide a strong, compelling argument for why to BUY this stock right now.
Use the provided signals, signal_strength, and exact percentage data to build your case.
{context}

Technical view: {technical_analysis}
Fundamental view: {fundamental_analysis}
"""
    bull_case = call_llm(bull_prompt, fallback_text="Bull case unavailable due to system limits. No strong bullish evidence present.")

    # E. Bear Agent
    bear_prompt = f"""
Provide a strong, compelling argument detailing the risks and why NOT to buy this stock.
You must strongly challenge bullish assumptions and make your case as convincing as the Bull.
Highlight specific weaknesses such as lack of confirmed breakout, overextension from moving averages, or risk of pullback after a volume spike.
Avoid weak phrases; be definitive and aggressive in your bearish outlook. Use exact quantitative metrics.
{context}

Technical view: {technical_analysis}
Fundamental view: {fundamental_analysis}
"""
    bear_case = call_llm(bear_prompt, fallback_text="Bear case: price below MA with elevated volume indicates downside risk.")

    # F. Judge Agent
    judge_prompt = f"""
You are the lead portfolio manager. Review all analyst inputs and make a final decision.

Crucial scoring rules:
1. Decision MUST be exactly one of: BUY, WATCH, AVOID. NEVER return None or null.
2. If strong bearish signals -> AVOID, mixed -> WATCH, strong bullish -> BUY.
3. Strict Confidence Calibration Rules:
   - If the trend is "Downtrend" -> maximum confidence = 0.70.
   - If the signals include "Near Breakout" -> maximum confidence = 0.70.
   - You may ONLY assign a confidence > 0.80 if the signals contain BOTH "Breakout" AND "Volume Spike".
   - Ensure realistic confidence values based on these caps and the overall `signal_strength`.
4. Ensure output is STRICTLY valid JSON so parsing always succeeds. Always fill all fields.

Context & Data:
{context}

Technical Analysis: {technical_analysis}
Fundamental Analysis: {fundamental_analysis}
Sentiment Analysis: {sentiment_analysis}
Bull Case: {bull_case}
Bear Case: {bear_case}

Produce a structured JSON output EXACTLY wrapped in a strict JSON block matching this schema:
```json
{{
  "decision": "BUY/WATCH/AVOID",
  "confidence": <float>,
  "risk": "Low/Medium/High",
  "reason": "...",
  "why_now": "...",
  "verdict_summary": "..."
}}
```
"""
    judge_output = call_llm(judge_prompt, json_format=True)
    
    decision_data = {}
    try:
        decision_data = json.loads(judge_output)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Judge output: {e}\nOutput was: {judge_output}")
        
        # Fallback keyword matching
        fallback_decision = "WATCH"
        text_upper = judge_output.upper()
        if "AVOID" in text_upper:
            fallback_decision = "AVOID"
        elif "BUY" in text_upper:
            fallback_decision = "BUY"
            
        decision_data = {
            "decision": fallback_decision,
            "confidence": 0.5,
            "risk": "Medium",
            "reason": f"Fallback extraction due to JSON parse error.",
            "why_now": "N/A",
            "verdict_summary": "N/A"
        }

    return {
        "technical": technical_analysis,
        "fundamental": fundamental_analysis,
        "sentiment": sentiment_analysis,
        "bull": bull_case,
        "bear": bear_case,
        "decision": decision_data
    }
