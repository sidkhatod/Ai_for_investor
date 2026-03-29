from portfolio.analyzer import analyze_portfolio
from discovery.engine import discover_opportunities

def generate_market_briefing(portfolio, stock_list):
    """
    Generate a text briefing combining portfolio risk context and market opportunities.
    """
    # 1. Run core models
    portfolio_data = analyze_portfolio(portfolio)
    discovery_data = discover_opportunities(stock_list)
    
    # 2. Extract Portfolio info
    p_summary = portfolio_data.get("summary", {})
    portfolio_risk = p_summary.get("portfolio_risk", "Unknown")
    portfolio_decision = p_summary.get("portfolio_decision", "Unknown")
    stability_score = p_summary.get("stability_score", 0.0)
    top_risk_driver = p_summary.get("top_risk_driver", {}).get("ticker", "None")
    
    # Extract Discovery info
    top_opportunities = discovery_data.get("top_opportunities", [])
    d_summary = discovery_data.get("summary", {})
    insight = d_summary.get("insight", "Market condition neutral.")
    market_health = d_summary.get("market_health", "")
    
    market_condition_text = market_health if market_health else insight

    # 3. BUILD SCRIPT
    script_parts = []
    
    if portfolio_risk == "High":
        opening = "Markets are showing elevated risk conditions today."
    elif portfolio_risk == "Medium":
        opening = "Markets are showing mixed signals today."
    else:
        opening = "Markets are showing stable conditions today."
        
    script_parts.append(f"{opening}\n")
    script_parts.append("Today's AI Market Briefing:\n")
    script_parts.append("Portfolio Overview:")
    script_parts.append("- Based on your current portfolio allocation:")
    script_parts.append(f"- Your portfolio risk is {portfolio_risk}")
    script_parts.append(f"- Stability score is {round(stability_score, 2)}")
    script_parts.append(f"- Primary risk is driven by {top_risk_driver}\n")
    
    script_parts.append("Market Condition:")
    script_parts.append(f"- {market_condition_text}\n")
    
    script_parts.append("Opportunities:")
    if top_opportunities:
        # Menion top 1-2 stocks with decision
        for stock in top_opportunities[:2]:
            script_parts.append(f"- {stock['ticker']} ({stock['decision']})")
    else:
        script_parts.append("- No strong opportunities detected today")
    script_parts.append("")
    
    script_parts.append("Actionable Insight:")
    script_parts.append(f"- {portfolio_decision} your portfolio")
    if portfolio_risk.lower() in ["high", "critical"]:
        script_parts.append("- Reduce exposure to high-risk positions")
    if top_opportunities:
        script_parts.append("- Consider reallocating capital to stronger setups")
    script_parts.append("")
    
    script_parts.append("Closing:")
    if portfolio_risk == "High":
        script_parts.append("Caution is advised. Prioritize capital protection.")
    elif portfolio_risk == "Medium":
        script_parts.append("Stay selective and wait for confirmation.")
    else:
        script_parts.append("Opportunities exist, but remain disciplined.")

    script = "\n".join(script_parts)

    top_opp = ""
    if top_opportunities:
        top_opp = top_opportunities[0].get("ticker", "")

    # 4. RETURN
    return {
        "script": script,
        "summary": {
            "portfolio_risk": portfolio_risk,
            "market_condition": market_condition_text,
            "top_opportunity": top_opp
        }
    }
