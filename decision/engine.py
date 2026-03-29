import logging
from typing import Dict, Any
from data.fetcher import get_stock_data
from signals.radar import detect_signals
from agents.multi_agent import run_multi_agent_analysis
from guardrails.interceptor import evaluate_trade

logger = logging.getLogger(__name__)

def generate_full_analysis(ticker: str) -> Dict[str, Any]:
    """
    Generate a full analysis for a given ticker by orchestrating data fetching,
    signal detection, and multi-agent debate/judgment.
    
    Args:
        ticker (str): The stock ticker symbol.
        
    Returns:
        Dict[str, Any]: Structured JSON output of the analysis.
    """
    try:
        # Step 1: Fetch data
        logger.info(f"Fetching data for {ticker}")
        df = get_stock_data(ticker)
        
        if df.empty:
            logger.warning(f"No data fetched for {ticker}. Returning empty analysis.")
            return _empty_analysis(ticker)
            
        # Step 2: Detect signals
        logger.info(f"Detecting signals for {ticker}")
        signal_data = detect_signals(df)
        signals = signal_data.get("signals", [])
        metrics = signal_data.get("metrics", {})
        
        # Step 3, 4, 5: Run all agents, run debate, judge final decision
        logger.info(f"Running multi-agent analysis for {ticker}")
        agent_results = run_multi_agent_analysis(ticker, signals, metrics)
        
        # Map fields to match requested structure
        decision_data = agent_results.get("decision", {})
        
        # Assess Guardrails
        guardrails = evaluate_trade(decision_data, signals, metrics)
        
        if guardrails["override"] is not None:
            logger.warning(f"Guardrail overriding decision from {decision_data.get('decision')} to {guardrails['override']}")
            decision_data["decision"] = guardrails["override"]
            decision_data["reason"] = f"OVERRIDE: {guardrails.get('explanation')}"
        
        return {
            "ticker": ticker,
            "signals": signals,
            "agent_outputs": {
                "technical": agent_results.get("technical", ""),
                "fundamental": agent_results.get("fundamental", ""),
                "sentiment": agent_results.get("sentiment", ""),
                "bull": agent_results.get("bull", ""),
                "bear": agent_results.get("bear", "")
            },
            "decision": {
                "action": decision_data.get("decision", ""),
                "confidence": decision_data.get("confidence", 0.0),
                "risk": decision_data.get("risk", ""),
                "reason": decision_data.get("reason", "")
            },
            "why_now": decision_data.get("why_now", "N/A"),
            "verdict_summary": decision_data.get("verdict_summary", "N/A"),
            "guardrails": guardrails
        }
        
    except Exception as e:
        logger.error(f"Error generating full analysis for {ticker}: {e}")
        return _empty_analysis(ticker)

def _empty_analysis(ticker: str) -> Dict[str, Any]:
    return {
        "ticker": ticker,
        "signals": [],
        "agent_outputs": {
            "technical": "",
            "fundamental": "",
            "sentiment": "",
            "bull": "",
            "bear": ""
        },
        "decision": {
            "action": "ERROR",
            "confidence": 0.0,
            "risk": "Unknown",
            "reason": "Failed to generate analysis due to data fetching or processing error."
        },
        "why_now": "N/A",
        "verdict_summary": "N/A",
        "guardrails": {}
    }
