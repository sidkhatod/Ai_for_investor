from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn

# Engines
from discovery.engine import discover_opportunities
from decision.engine import generate_full_analysis
from portfolio.analyzer import analyze_portfolio
from video.engine import generate_market_briefing

app = FastAPI(title="AI Stock Intelligence Backend")

@app.on_event("startup")
async def startup_event():
    print("Pre-warming AI Engine with RELIANCE.NS...")
    try:
        generate_full_analysis("RELIANCE.NS")
    except Exception as e:
        print(f"Pre-warm failed: {e}")
    print("Pre-warming complete. Demo is ready.")


# CORS middleware for allowing localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiscoveryRequest(BaseModel):
    stocks: List[str]

class PortfolioRequest(BaseModel):
    portfolio: List[Dict[str, Any]]

class VideoRequest(BaseModel):
    portfolio: List[Dict[str, Any]]
    stocks: List[str]

@app.post("/discovery")
def discovery_endpoint(req: DiscoveryRequest):
    return discover_opportunities(req.stocks)

@app.get("/stock")
def stock_endpoint(ticker: str):
    return generate_full_analysis(ticker)

@app.post("/portfolio")
def portfolio_endpoint(req: PortfolioRequest):
    return analyze_portfolio(req.portfolio)

@app.post("/video")
def video_endpoint(req: VideoRequest):
    return generate_market_briefing(req.portfolio, req.stocks)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
