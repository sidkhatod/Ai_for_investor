import os
import json
import re
import logging
from typing import Dict, Any, List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    logger.warning("G_API_KEY environment variable not set. LLM calls may fail.")
else:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-2.5-flash")
api_key_str = os.getenv("GOOGLE_API_KEY")
print("Using API KEY:", api_key_str[:10] if api_key_str else "None")


def build_prompt(ticker: str, signals: List[str], metrics: Dict[str, Any]) -> str:
    return f"""
You are simulating a team of 6 independent financial analysts.

CRITICAL RULES:
- Each agent must think independently.
- Agents MUST NOT align by default.
- Bull and Bear MUST produce opposing conclusions using the SAME data.
- Do NOT summarize across agents.
- Each agent must have a distinct perspective.
- Use ONLY provided data.
- Use numeric references (percentages, MA, volume).
- Max 2 sentences per agent.
- No fluff or vague words like 'strong' without numbers.
- If Bull and Bear agree, output is invalid.

---

INPUT:

Ticker: {ticker}

Signals:
{signals}

Metrics:
- Price vs Short MA (%): {metrics.get("price_vs_short_ma_pct", 0)}
- Volume vs Avg (%): {metrics.get("volume_vs_avg_pct", 0)}
- Signal Strength: {metrics.get("signal_strength", 0)}

---

AGENTS (STRICTLY INDEPENDENT):

1. Technical Analyst:
Analyze only price, MA, and volume.

2. Fundamental Analyst:
Ignore technicals. Focus on stability and long-term outlook.

3. Sentiment Analyst:
Focus on perception and participation.

4. Bull Analyst:
Make strongest possible BUY argument using data.

5. Bear Analyst:
Make strongest possible AVOID argument using data.

6. Judge:
- Decide: BUY / WATCH / AVOID
- Confidence (0-1)
- Risk (Low/Medium/High)
- Reason (max 2 sentences)
- why_now (1 sentence)
- verdict_summary (1 sentence)

IMPORTANT DECISION RULES:
- Penalize price below MA
- Penalize weak signal_strength (<0.3)
- Require strong evidence for BUY
- Prefer AVOID if bearish pressure exists

---

RETURN STRICT JSON ONLY (NO EXTRA TEXT):
{{
  "technical": "...",
  "fundamental": "...",
  "sentiment": "...",
  "bull": "...",
  "bear": "...",
  "decision": {{
    "decision": "BUY/WATCH/AVOID",
    "confidence": 0.5,
    "risk": "Low/Medium/High",
    "reason": "...",
    "why_now": "...",
    "verdict_summary": "..."
  }}
}}
"""

def call_llm(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error calling LLM: {e}")
        return None

def fallback_parser(text: str) -> Dict[str, Any]:
    decision = "WATCH"

    if text:
        text_upper = text.upper()
        if "AVOID" in text_upper:
            decision = "AVOID"
        elif "BUY" in text_upper:
            decision = "BUY"

    return {
        "technical": "Fallback: insufficient LLM response",
        "fundamental": "Fallback: insufficient LLM response",
        "sentiment": "Fallback: insufficient LLM response",
        "bull": "Fallback unavailable",
        "bear": "Fallback unavailable",
        "decision": {
            "decision": decision,
            "confidence": 0.5,
            "risk": "Medium",
            "reason": "Fallback decision due to parsing or API issue",
            "why_now": "Fallback triggered",
            "verdict_summary": "Limited confidence decision"
        }
    }


def safe_parse_response(response: str) -> Dict[str, Any]:
    if not response:
        return None

    try:
        return json.loads(response)
    except Exception:
        pass

    # Try extracting JSON block
    try:
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass

    return None

def run_multi_agent_analysis(ticker: str, signals: List[str], metrics: Dict[str, Any]) -> Dict[str, Any]:
    prompt = build_prompt(ticker, signals, metrics)
    response = call_llm(prompt)
    parsed = safe_parse_response(response)

    if parsed is None:
        return fallback_parser(response)

    # Ensure required keys exist
    if "decision" not in parsed or not isinstance(parsed["decision"], dict):
        return fallback_parser(response)

    decision = parsed.get("decision", {})

    # Ensure valid decision
    if decision.get("decision") not in ["BUY", "WATCH", "AVOID"]:
        parsed["decision"]["decision"] = "WATCH"

    # Fill missing fields safely
    parsed["decision"].setdefault("confidence", 0.5)
    parsed["decision"].setdefault("risk", "Medium")
    parsed["decision"].setdefault("reason", "No reason provided")
    parsed["decision"].setdefault("why_now", "No context available")
    parsed["decision"].setdefault("verdict_summary", "No summary available")
    
    parsed.setdefault("technical", "No data")
    parsed.setdefault("fundamental", "No data")
    parsed.setdefault("sentiment", "No data")
    parsed.setdefault("bull", "No data")
    parsed.setdefault("bear", "No data")

    return parsed
