from typing import Dict, Any, List

def evaluate_trade(decision: Dict[str, Any], signals: List[str], metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate trade decision using heavily quantitative and qualitative guardrails, focusing on systemic market risk.
    """
    warnings = []
    severity = "Low"
    force_high_severity = False
    
    dec_action = decision.get("decision", "WATCH")
    confidence = decision.get("confidence", 0.0)
    
    price_vs_short_ma_pct = metrics.get("price_vs_short_ma_pct", 0.0)
    volume_vs_avg_pct = metrics.get("volume_vs_avg_pct", 0.0)
    signal_strength = metrics.get("signal_strength", 0.0)
    
    # === 1. GLOBAL RISK DETECTION (Always Evaluated) ===
    # Rule 2: Strong bearish crash
    if price_vs_short_ma_pct < -2 and volume_vs_avg_pct > 10:
        warnings.append("Price breakdown with elevated volume indicates strong bearish pressure")
        force_high_severity = True
        
    # Rule 3: Weak Setup Structure
    if signal_strength < 0.3:
        warnings.append("Very low signal strength indicates unreliable trade setup")
        
    # Rule 4: Trend Conflict Mismatch
    if "Uptrend" in signals and price_vs_short_ma_pct < 0:
        warnings.append("Signal inconsistency: trend vs price action mismatch")
        
    # === 2. Technical Risk Checks (Decision Bound) ===
    if dec_action == "BUY" and "Downtrend" in signals:
        warnings.append("Buying in downtrend is statistically unfavorable")
        force_high_severity = True
        
    if dec_action == "BUY" and price_vs_short_ma_pct < 0:
        warnings.append("Price below moving average indicates weak momentum")
        
    if dec_action == "BUY" and "Breakout" not in signals:
        warnings.append("No breakout confirmation increases false entry risk")
        
    # === 3. Behavioral Risk Simulation ===
    if dec_action == "BUY" and "Near Breakout" in signals:
        warnings.append("Chasing near breakout often leads to false breakouts")
        
    if dec_action == "BUY" and price_vs_short_ma_pct < 0:
        warnings.append("Buying during price decline may indicate catching a falling knife")
        
    # === 4. Decision Quality Checks ===
    if dec_action == "BUY" and confidence < 0.5:
        warnings.append("Low confidence contradicts aggressive buy decision")
        
    # === 5. Severity Logic Update ===
    # Rule 7: Any strong bearish pattern -> High, Multiple moderate issues -> High
    num_warnings = len(warnings)
    if force_high_severity or num_warnings >= 2:
        severity = "High"
    elif num_warnings == 1:
        severity = "Medium"
        
    # === 6. Decision Alignment Override ===
    # Rule 5 & 6: risk_flag = True if ANY High severity condition exists or if market is dangerous.
    risk_flag = severity == "High" or num_warnings > 0

    override = None
    if severity == "High" and dec_action != "AVOID":
        override = "AVOID"
    elif severity == "Medium" and dec_action == "BUY":
        override = "WATCH"
        
    # === 8. Explanation MUST reflect MARKET RISK ===
    if not warnings:
        explanation = "Market environment shows stable risk factors; metrics align well with technical thresholds."
    else:
        explanation_lines = [f"Market Risk is {severity.upper()} with {num_warnings} structural warning(s)."]
        if warnings:
            explanation_lines.append(f"Primary risk matrix: {warnings[0]}.")
        if len(warnings) > 1:
            explanation_lines.append(f"Secondary issues: {warnings[1]}.")
        explanation = " ".join(explanation_lines)
        
    return {
        "risk_flag": risk_flag,
        "severity": severity,
        "warnings": warnings,
        "explanation": explanation,
        "override": override
    }
