from typing import List, Dict, Any
from decision.engine import generate_full_analysis

def analyze_portfolio(portfolio: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluate a portfolio of stocks, calculate aggregate risk, and generate actionable insights.
    
    Args:
        portfolio: List of dictionaries containing 'ticker' and 'weight'.
                   Example: [{"ticker": "RELIANCE.NS", "weight": 0.4}, ...]
                   
    Returns:
        Dict[str, Any]: A structured portfolio risk and recommendation summary.
    """
    stocks_data = []
    
    total_risk = 0.0
    buy_weight = 0.0
    avoid_weight = 0.0
    
    warnings = []
    recommendations = []
    
    for position in portfolio:
        ticker = position.get("ticker", "")
        weight = float(position.get("weight", 0.0))
        
        # 1. Evaluate stock using multi-agent pipeline
        analysis = generate_full_analysis(ticker)
        decision_block = analysis.get("decision", {})
        
        action = decision_block.get("action", "WATCH")
        risk = decision_block.get("risk", "Medium")
        confidence = float(decision_block.get("confidence", 0.0))
        
        # 2. Assign scalar risk_score
        risk_score = 0.6  # Default Medium
        if risk == "High":
            risk_score = 1.0
        elif risk == "Low":
            risk_score = 0.3
            
        # 3. Compute weighted risk_contribution
        risk_contribution = weight * risk_score
        
        # 4. Store individual asset performance
        stock_info = {
            "ticker": ticker,
            "weight": weight,
            "decision": action,
            "risk": risk,
            "confidence": confidence,
            "risk_score": risk_score,
            "risk_contribution": round(risk_contribution, 4)
        }
        stocks_data.append(stock_info)
        
        # 5. Aggregate metrics dynamically
        total_risk += risk_contribution
        if action == "BUY":
            buy_weight += weight
        elif action == "AVOID":
            avoid_weight += weight
            
        # 7. Initial Concentration risk
        if weight > 0.5:
            warnings.append(f"High concentration in single stock ({ticker})")
            
        # 8. Actionable Recommendations
        if action == "AVOID":
            recommendations.append(f"Reduce exposure to {ticker}")
        elif action == "BUY" and weight < 0.3:
            recommendations.append(f"Consider increasing allocation to {ticker}")

    # Normalize total risk
    total_risk = min(total_risk, 1.0)

    # 6. Global Portfolio risk classification
    if total_risk > 0.7:
        portfolio_risk = "High"
        portfolio_decision = "DE-RISK"
    elif total_risk > 0.4:
        portfolio_risk = "Medium"
        portfolio_decision = "REBALANCE"
    else:
        portfolio_risk = "Low"
        portfolio_decision = "HOLD/OPTIMIZE"
        
    # Identify top risk driver
    top_driver = max(stocks_data, key=lambda x: x["risk_contribution"], default=None)
    top_risk_driver = {
        "ticker": top_driver["ticker"] if top_driver else "",
        "contribution": top_driver["risk_contribution"] if top_driver else 0.0
    }
    
    # Calculate stability and relative distribution
    stability_score = 1.0 - total_risk
    
    risk_distribution = []
    for stock in stocks_data:
        contribution_pct = 0.0
        if total_risk > 0:
            contribution_pct = stock["risk_contribution"] / total_risk
        risk_distribution.append({
            "ticker": stock["ticker"],
            "contribution_pct": round(contribution_pct, 4)
        })
        
    # 7. Portfolio-Scale Warnings
    if avoid_weight > 0.5:
        warnings.append("Majority of portfolio in high-risk positions")
        
    # Portfolio-Level Recommendations and Urgency
    buy_stocks = [s for s in stocks_data if s["decision"] == "BUY"]
    if stocks_data and all(s["decision"] == "AVOID" for s in stocks_data):
        recommendations.append("Hold capital or wait for confirmed breakout opportunities before redeployment")
    elif buy_stocks:
        top_buy = max(buy_stocks, key=lambda x: x.get("confidence", 0.0))
        recommendations.append(f"Rotate capital from AVOID into {top_buy['ticker']}")

    if total_risk > 0.8:
        urgency = "Immediate Action Required"
    elif total_risk >= 0.6:
        urgency = "Action Recommended"
    else:
        urgency = "Monitor"

    # 9. Generate Portfolio Insight Summary
    summary_line = f"The portfolio currently exhibits a {portfolio_risk} composite risk profile based on underlying asset signals. " \
                   f"The current allocation sits at {round(buy_weight * 100, 1)}% structural BUY vs {round(avoid_weight * 100, 1)}% structural AVOID."
                   
    if portfolio_risk == "High":
        key_risk = "Critical capital exposure detected; immediate defensive trimming of AVOID-rated assets is recommended."
    elif portfolio_risk == "Medium":
        key_risk = "Balanced but vulnerable structure; carefully monitor concentrated positions and trim underperforming assets."
    else:
        key_risk = "Defensive portfolio positioning is stable; maintain current allocations while monitoring for macro shifts."
        
    action_plan = [
        "Review and systematically trim exposure to all AVOID-rated constituents.",
        "Reallocate freed capital toward BUY-rated assets possessing technical breakout strength, or maintain trailing cash."
    ]

    # 10. Return FINAL STRUCTURE
    return {
        "urgency": urgency,
        "stocks": stocks_data,
        "summary": {
            "portfolio_risk": portfolio_risk,
            "portfolio_decision": portfolio_decision,
            "stability_score": round(stability_score, 4),
            "total_risk": round(total_risk, 4),
            "buy_weight": round(buy_weight, 4),
            "avoid_weight": round(avoid_weight, 4),
            "top_risk_driver": top_risk_driver,
            "risk_distribution": risk_distribution
        },
        "warnings": warnings,
        "recommendations": recommendations,
        "insights": {
            "portfolio_summary": summary_line,
            "key_risk": key_risk,
            "action_plan": action_plan
        }
    }
