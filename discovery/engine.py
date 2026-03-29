from decision.engine import generate_full_analysis

def discover_opportunities(stock_list):
    """
    Discover top trading opportunities from a list of stocks based on decision signals.
    """
    opportunities = []

    # 2. For each stock
    for ticker in stock_list:
        try:
            result = generate_full_analysis(ticker)
        except Exception:
            continue
            
        decision_data = result.get("decision", {})
        
        # Extract fields (handling both "decision" and "action" keys for safety)
        decision = decision_data.get("decision") or decision_data.get("action", "WATCH")
        
        try:
            confidence = float(decision_data.get("confidence", 0.0))
        except (ValueError, TypeError):
            confidence = 0.0
            
        reason = decision_data.get("reason", "")
        why_now = decision_data.get("why_now", "")
        if not why_now:
            why_now = "No strong trigger yet; setup is still developing"
        
        try:
            signal_strength = float(result.get("metrics", {}).get("signal_strength", 0.0))
        except (ValueError, TypeError):
            signal_strength = 0.0

        # 3. FILTER
        if decision in ["BUY", "WATCH"]:
            # 4. SCORE
            score = confidence + signal_strength
            
            if score > 1.2:
                confidence_tag = "High Conviction"
            elif score >= 0.8:
                confidence_tag = "Moderate Setup"
            else:
                confidence_tag = "Early Stage"
            
            # 5. STORE
            opportunities.append({
                "ticker": ticker,
                "decision": decision,
                "confidence": confidence,
                "signal_strength": signal_strength,
                "score": score,
                "confidence_tag": confidence_tag,
                "reason": reason,
                "why_now": why_now
            })
            
    # 10. EDGE CASE
    if not opportunities:
        return {
            "top_opportunities": [],
            "summary": {
                "market_health": "Weak Market",
                "best_stock": None,
                "insight": "No strong opportunities detected in current market conditions",
                "rejection_summary": "Most stocks are currently in downtrend or lack breakout confirmation, indicating weak market conditions."
            }
        }

    # 6. SORT
    opportunities.sort(key=lambda x: x["score"], reverse=True)
    
    # 7. SELECT top 3
    top_ops = opportunities[:3]
    
    # 8. ADD SUMMARY
    best_stock = top_ops[0]["ticker"]
    
    buy_count = sum(1 for op in top_ops if op["decision"] == "BUY")
    watch_count = sum(1 for op in top_ops if op["decision"] == "WATCH")
    
    if buy_count > watch_count:
        insight = "Strong breakout-driven opportunities detected"
        market_health = "Strong Market"
    elif watch_count > buy_count:
        insight = "Market showing early-stage setups without full confirmation"
        market_health = "Developing Market"
    else:
        insight = "Limited high-confidence opportunities in current market"
        market_health = "Mixed Market"
        
    # 9. RETURN
    return {
        "top_opportunities": top_ops,
        "summary": {
            "market_health": market_health,
            "best_stock": best_stock,
            "insight": insight
        }
    }
