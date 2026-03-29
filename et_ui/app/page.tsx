"use client";

import { useEffect, useState } from "react";
import { Bell, ChevronRight, Search, Menu, ArrowLeft, X, TrendingUp, CheckCircle, Users, BarChart3, Zap, AlertCircle, Calendar, Target, MessageSquare, Play, Pause } from "lucide-react";
import { fetchDiscovery, fetchStock, analyzePortfolio, fetchVideoScript } from "@/lib/api";

export default function StockDashboard() {
  return (
    <div className="min-h-screen bg-slate-100 p-4 md:p-8">
      <div className="mx-auto max-w-7xl">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-2">
          {/* Row 1 */}
          <HomeScreen />
          <StockOverviewScreen />
          
          {/* Row 2 */}
          <PortfolioScreen />
          <AlertsScreen />

          {/* Row 3 */}
          <AIMarketVideoScreen />
        </div>
      </div>
    </div>
  )
}

function HomeScreen() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDiscovery()
      .then((res: any) => {
        setData(res);
        setLoading(false);
      })
      .catch((err: any) => {
        console.error("Discovery error:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="rounded-2xl bg-white p-5 shadow-sm h-full flex flex-col justify-center items-center min-h-[400px]">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600 mb-4"></div>
        <div className="text-sm font-medium text-slate-500">Scanning market with AI...</div>
      </div>
    );
  }

  const ops = data?.top_opportunities || [];
  const featured = ops[0];
  const others = ops.slice(1);

  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-900">
            <BarChart3 className="h-4 w-4 text-white" />
          </div>
          <span className="font-semibold text-slate-900">Home</span>
        </div>
        <div className="flex items-center gap-3">
          <Bell className="h-5 w-5 text-slate-500" />
          <div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-600" />
        </div>
      </div>

      {/* Title */}
      <div className="mb-2 flex items-center justify-between">
        <h1 className="text-xl font-bold text-slate-900">What Should I Focus On Today?</h1>
        {data?.summary?.market_health && (
          <span className={`rounded-full px-2 py-1 text-xs font-semibold ${
            data.summary.market_health.includes("Strong") ? "bg-emerald-100 text-emerald-700" :
            data.summary.market_health.includes("Weak") ? "bg-red-100 text-red-700" :
            "bg-amber-100 text-amber-700"
          }`}>
            Market Condition: {data.summary.market_health.split(' ')[0]}
          </span>
        )}
      </div>
      <p className="mb-6 text-sm text-slate-500">
        These are today&apos;s top moves in the market. Stay ahead of the curve.
      </p>

      {/* Top Opportunities */}
      <div className="mb-4 flex items-center justify-between">
        <h2 className="font-semibold text-slate-900">Top Opportunities</h2>
        <button className="flex items-center gap-1 text-sm font-medium text-blue-600">
          SEE WHY <ChevronRight className="h-4 w-4" />
        </button>
      </div>

      {!featured && (
        <div className="mb-8 rounded-xl border border-slate-200 bg-slate-50 p-6 text-center">
          <p className="font-semibold text-slate-900 mb-1">No strong opportunities detected today.</p>
          <p className="text-sm text-slate-500">Market lacks breakout signals.</p>
        </div>
      )}

      {/* Featured Card */}
      {featured && (
        <div className="mb-4 rounded-xl border border-slate-200 bg-slate-50 p-4">
          <div className="mb-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                featured.decision === 'BUY' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'
              }`}>
                ⚡ {featured.decision}
              </span>
              <span className="font-semibold text-slate-900">Score: {featured.score}</span>
            </div>
            <button className="rounded-lg bg-blue-600 px-3 py-1.5 text-xs font-semibold text-white">
              ↗ ACT NOW
            </button>
          </div>
          
          <h3 className="mb-1 text-lg font-bold text-slate-900">{featured.ticker}</h3>
          <p className="mb-3 text-sm text-slate-700">{featured.why_now}</p>
          
          <div className="flex items-center justify-between">
            <button className="flex items-center gap-1 text-sm text-slate-500">
              ▾ SEE WHY
            </button>
            <button className="flex items-center gap-1 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-sm font-medium text-slate-700">
              SEE DETAILS <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* Other Stock Cards */}
      {others.map((stock: any, i: number) => (
        <StockCard
          key={i}
          name={stock.ticker}
          tag={stock.decision}
          tagColor={stock.decision === "BUY" ? "bg-emerald-500" : stock.decision === "WATCH" ? "bg-slate-700" : "bg-red-500"}
          subtitle={`Confidence: ${stock.confidence * 100}%`}
          price={`Score: ${stock.score}`}
          description={stock.why_now}
        />
      ))}

      {/* Market Summary */}
      <div className="mt-4 rounded-xl border border-slate-200 p-4">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="font-semibold text-slate-900">Market Summary</h3>
          <button className="text-sm font-medium text-blue-600">VIEW ALL</button>
        </div>
        <div className="flex items-center gap-6 text-sm">
          <div>
            <span className="text-slate-500">NIFTY</span>
            <div className="font-semibold text-slate-900">18,013 <span className="text-xs text-emerald-500">(+1%)</span></div>
          </div>
          <div className="flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-red-500" />
            <span className="text-slate-500">Banking</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function StockCard({ name, tag, tagColor, subtitle, price, description }: {
  name: string
  tag: string
  tagColor: string
  subtitle: string
  price: string
  description: string
}) {
  return (
    <div className="mb-3 flex items-center justify-between rounded-xl border border-slate-200 bg-white p-4">
      <div className="flex-1">
        <div className="mb-1 flex items-center gap-2">
          <h3 className="font-semibold text-slate-900">{name}</h3>
          <span className={`rounded px-2 py-0.5 text-xs font-semibold text-white ${tagColor}`}>
            {tag}
          </span>
        </div>
        <p className="mb-1 text-xs text-red-500">{subtitle}</p>
        <div className="flex items-center gap-2">
          <span className="font-semibold text-slate-900">{price}</span>
          <span className="text-sm text-slate-500">{description}</span>
        </div>
      </div>
      <ChevronRight className="h-5 w-5 text-slate-400" />
    </div>
  )
}

function StockOverviewScreen() {
  const [ticker, setTicker] = useState("RELIANCE.NS");
  const [searchInput, setSearchInput] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchStock(ticker)
      .then((res: any) => {
        setData(res);
        setLoading(false);
      })
      .catch((err: any) => {
        console.error("Stock error:", err);
        setLoading(false);
      });
  }, [ticker]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchInput.trim()) {
      setTicker(searchInput.trim().toUpperCase());
    }
  };

  const d = data?.decision;

  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <ArrowLeft className="h-5 w-5 text-slate-500" />
          <div className="h-3 w-3 rounded-full border-2 border-blue-600" />
          <span className="font-semibold text-slate-900">Stock Overview</span>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative">
            <MessageSquare className="h-5 w-5 text-slate-500" />
            <span className="absolute -right-1 -top-1 h-2 w-2 rounded-full bg-red-500" />
          </div>
          <Bell className="h-5 w-5 text-slate-500" />
        </div>
      </div>

      {/* Search Input */}
      <form onSubmit={handleSearch} className="mb-6 flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3">
        <Search className="h-5 w-5 text-slate-400" />
        <input 
          type="text" 
          value={searchInput}
          onChange={(e: any) => setSearchInput(e.target.value)}
          placeholder="TYPE TICKER (e.g. RELIANCE.NS)" 
          className="flex-1 bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
        />
        <button type="submit" className="text-sm font-semibold text-blue-600">Search</button>
      </form>

      {loading ? (
        <div className="py-16 flex flex-col items-center justify-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600 mb-4"></div>
          <div className="text-sm font-medium text-slate-500">Running multi-agent analysis...</div>
        </div>
      ) : !data || data.error || !data.signals || data.signals.length === 0 ? (
        <div className="py-16 text-center">
          <p className="font-semibold text-slate-900 mb-1">No clear setup. Consider waiting.</p>
        </div>
      ) : (
        <>
          {/* Stock Info */}
          <div className="mb-4 flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">{ticker}</h1>
              <div className="flex items-center gap-2">
                <span className="text-sm font-semibold text-slate-500">Confidence: {d?.confidence * 100}%</span>
              </div>
            </div>
            <button className={`flex items-center gap-1 rounded-lg px-4 py-2 text-sm font-semibold text-white ${
              d?.decision === 'BUY' ? 'bg-emerald-500' : d?.decision === 'WATCH' ? 'bg-slate-700' : 'bg-red-500'
            }`}>
              {d?.decision} <ChevronRight className="h-4 w-4" />
            </button>
          </div>

          {/* Description */}
          <p className="mb-4 text-sm text-slate-600">
            <span className="font-semibold">{ticker}</span> {d?.reason} {d?.why_now}
          </p>

          {/* Chart Placeholder */}
          <div className="mb-4 rounded-xl bg-slate-50 p-4">
            <div className="relative h-32">
              <div className="absolute left-0 top-4 rounded bg-teal-500 px-2 py-1 text-xs text-white">Breakout</div>
              <div className="absolute bottom-8 right-4 rounded bg-slate-700 px-2 py-1 text-xs text-white">Support ✏</div>
              <svg className="h-full w-full" viewBox="0 0 300 100">
                <path d="M0,80 L30,75 L60,70 L90,65 L120,50 L150,45 L180,40 L210,35 L240,25 L270,20 L300,15" 
                      fill="none" stroke="#14b8a6" strokeWidth="2" />
                <path d="M0,80 L30,75 L60,70 L90,65 L120,50 L150,45 L180,40 L210,35 L240,25 L270,20 L300,15 L300,100 L0,100 Z" 
                      fill="url(#gradient)" opacity="0.2" />
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#14b8a6" />
                    <stop offset="100%" stopColor="transparent" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
          </div>

          {/* Key Signals */}
          <h3 className="mb-3 font-semibold text-slate-900">Key Signals</h3>
          <div className="mb-4 space-y-3">
            {data?.signals?.map((sig: string, i: number) => {
              const [title, desc] = sig.split(': ');
              return (
                <SignalItem 
                  key={i}
                  icon={<TrendingUp className="h-4 w-4 text-emerald-500" />}
                  title={title || "Signal"}
                  description={desc || sig}
                />
              );
            })}
          </div>

          <div className="mb-4 flex items-center gap-2 rounded-lg bg-slate-50 p-3 text-sm">
            <Zap className="h-4 w-4 text-amber-500" />
            <span className="text-slate-600">Risk Assessment: <span className="font-semibold">{d?.risk}</span></span>
            <ChevronRight className="ml-auto h-4 w-4 text-slate-400" />
          </div>
        </>
      )}
    </div>
  )
}

function SignalItem({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
  return (
    <div className="flex items-start gap-3">
      {icon}
      <div>
        <span className="font-medium text-slate-900">{title}: </span>
        <span className="text-sm text-slate-600">{description}</span>
      </div>
    </div>
  )
}

function AlertsScreen() {
  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Search className="h-5 w-5 text-slate-500" />
          <span className="font-semibold text-slate-900">Alerts</span>
        </div>
        <div className="flex items-center gap-3">
          <Menu className="h-5 w-5 text-slate-500" />
          <div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-600" />
        </div>
      </div>

      {/* Title */}
      <h1 className="mb-2 text-xl font-bold text-slate-900">Don&apos;t Miss These Alerts</h1>
      <p className="mb-4 text-sm text-slate-500">
        Stay updated on critical filings, insider trades, and big block deals.
      </p>

      {/* Filter Tabs */}
      <div className="mb-4 flex items-center gap-2 overflow-x-auto">
        <button className="rounded-lg bg-slate-900 px-3 py-1.5 text-sm font-medium text-white">ALL</button>
        <button className="rounded-lg px-3 py-1.5 text-sm font-medium text-slate-600 hover:bg-slate-100">FILINGS</button>
        <button className="rounded-lg px-3 py-1.5 text-sm font-medium text-slate-600 hover:bg-slate-100">INSIDER</button>
        <button className="rounded-lg px-3 py-1.5 text-sm font-medium text-slate-600 hover:bg-slate-100">BLOCK DEALS</button>
        <button className="rounded-lg px-3 py-1.5 text-sm font-medium text-slate-600 hover:bg-slate-100">MORE</button>
        <ChevronRight className="h-4 w-4 text-slate-400" />
      </div>

      {/* Alert Cards */}
      <AlertCard
        company="Surya Pharma"
        time="10 refukets"
        tag="10MIN"
        tagColor="bg-amber-100 text-amber-700"
        icon={<CheckCircle className="h-4 w-4 text-emerald-500" />}
        highlight="Revenue up 25%, Net Profit, 95cr (+10%)"
        description="Biefnan malider s scr + the Profit for ratio st"
      />

      <AlertCard
        company="ABC Ltd."
        time="Today"
        tag="TODAY"
        tagColor="bg-blue-100 text-blue-700"
        icon={<TrendingUp className="h-4 w-4 text-blue-500" />}
        highlight="Promoter bough 6 lakh shares at ₹170"
        description="manay notres jey 85 ocd tali menorces: uf=2280"
      />

      <AlertCard
        company="SBI Fund"
        time="Today"
        tag="TODAY"
        tagColor="bg-blue-100 text-blue-700"
        icon={<AlertCircle className="h-4 w-4 text-red-500" />}
        highlight="SBI releases 4c 1.5% stake in XYZ Ltd."
        description="manay oetense dadr, cautfoura on the ₹2,00 drerc)"
      />

      <AlertCard
        company="Reliance Industries"
        time="Tomorrow"
        tag="TOMORROW"
        tagColor="bg-orange-100 text-orange-700"
        icon={<span className="rounded bg-slate-200 px-1 text-xs font-bold text-slate-700">Q1&8</span>}
        highlight="Sury Staray: historich Bromatory inodlet martel PY25 earnings"
        description="ctashingmals and nate of the Berakoo-staite."
      />
    </div>
  )
}

function AlertCard({ company, time, tag, tagColor, icon, highlight, description }: {
  company: string
  time: string
  tag: string
  tagColor: string
  icon: React.ReactNode
  highlight: string
  description: string
}) {
  return (
    <div className="mb-3 flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50 p-4">
      <div className="flex-1">
        <div className="mb-2 flex items-center gap-2">
          <span className="font-semibold text-slate-900">{company}</span>
          <span className="text-xs text-slate-400">| {time}</span>
          <span className={`ml-auto rounded px-2 py-0.5 text-xs font-semibold ${tagColor}`}>
            ↗ {tag}
          </span>
        </div>
        <div className="mb-1 flex items-start gap-2">
          {icon}
          <span className="text-sm font-medium text-slate-900">{highlight}</span>
        </div>
        <p className="text-xs text-slate-500">{description}</p>
      </div>
      <ChevronRight className="ml-2 h-5 w-5 text-slate-400" />
    </div>
  )
}

function PortfolioScreen() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Hardcoded portfolio for demo
    const testPortfolio = [
      { ticker: "RELIANCE.NS", weight: 0.4 },
      { ticker: "TCS.NS", weight: 0.3 },
      { ticker: "INFY.NS", weight: 0.3 }
    ];

    analyzePortfolio(testPortfolio)
      .then((res: any) => {
        setData(res);
        setLoading(false);
      })
      .catch((err: any) => {
        console.error("Portfolio error:", err);
        setLoading(false);
      });
  }, []);

  const d = data?.summary;

  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Target className="h-5 w-5 text-slate-500" />
          <span className="font-semibold text-slate-900">My Portfolio</span>
        </div>
        <div className="flex items-center gap-3">
          <Menu className="h-5 w-5 text-slate-500" />
          <div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-600" />
        </div>
      </div>

      {/* Title */}
      <h1 className="mb-2 text-xl font-bold text-slate-900">Portfolio Health Overview</h1>
      <p className="mb-4 text-sm text-slate-500">
        AI analysis of your current holdings.
      </p>

      {loading ? (
        <div className="py-16 flex flex-col items-center justify-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600 mb-4"></div>
          <div className="text-sm font-medium text-slate-500">Analyzing portfolio risk...</div>
        </div>
      ) : !d || data?.stocks?.length === 0 ? (
        <div className="py-16 text-center">
          <p className="font-semibold text-slate-900 mb-1">Portfolio is stable with no major risks.</p>
        </div>
      ) : (
        <>
          {/* Main Stats */}
          <div className="mb-6 grid grid-cols-2 gap-4">
            <div className="rounded-xl border border-slate-200 p-4 bg-slate-50">
              <span className="text-xs font-semibold text-slate-500">RISK LEVEL</span>
              <div className="mt-1 flex items-center gap-2">
                <span className="text-2xl font-bold text-slate-900">{d?.portfolio_risk}</span>
                <span className={`h-2 w-2 rounded-full ${d?.portfolio_risk === 'Low' ? 'bg-emerald-500' : d?.portfolio_risk === 'High' ? 'bg-red-500' : 'bg-amber-500'}`} />
              </div>
            </div>
            <div className="rounded-xl border border-slate-200 p-4 bg-slate-50">
              <span className="text-xs font-semibold text-slate-500">STABILITY SCORE</span>
              <div className="mt-1 flex items-center gap-2">
                <span className="text-2xl font-bold text-slate-900">{d?.stability_score}/100</span>
              </div>
            </div>
          </div>

          {/* Top Risk Driver */}
          <div className="mb-4 flex flex-col gap-2 rounded-xl bg-amber-50 p-4 border border-amber-100">
            <div className="flex items-center gap-2 text-amber-800">
              <AlertCircle className="h-5 w-5" />
              <span className="font-bold">Top Risk Driver</span>
            </div>
            <p className="text-sm text-amber-700">{d?.top_risk_driver}</p>
          </div>

          {/* Holdings Demo */}
          <h3 className="mb-3 font-semibold text-slate-900">Current Holdings</h3>
          <div className="mb-6 space-y-3">
            <div className="flex items-center justify-between rounded-lg p-3 border border-slate-100 bg-white">
              <div className="flex items-center gap-2">
                <span className="font-medium text-slate-900">RELIANCE.NS</span>
              </div>
              <span className="text-sm font-semibold text-slate-600">40%</span>
            </div>
            <div className="flex items-center justify-between rounded-lg p-3 border border-slate-100 bg-white">
              <div className="flex items-center gap-2">
                <span className="font-medium text-slate-900">TCS.NS</span>
              </div>
              <span className="text-sm font-semibold text-slate-600">30%</span>
            </div>
            <div className="flex items-center justify-between rounded-lg p-3 border border-slate-100 bg-white">
              <div className="flex items-center gap-2">
                <span className="font-medium text-slate-900">INFY.NS</span>
              </div>
              <span className="text-sm font-semibold text-slate-600">30%</span>
            </div>
          </div>

          <button className="w-full rounded-xl bg-slate-900 py-3 text-sm font-semibold text-white hover:bg-slate-800 flex justify-center items-center gap-2">
            REBALANCE PORTFOLIO <ChevronRight className="h-4 w-4" />
          </button>
        </>
      )}
    </div>
  )
}

function AIMarketVideoScreen() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchVideoScript()
      .then((res: any) => {
        setData(res);
        setLoading(false);
      })
      .catch((err: any) => {
        console.error("Video error:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="flex flex-col items-center rounded-2xl bg-slate-200 p-6 shadow-sm">
      {/* Page Title */}
      <h1 className="mb-6 text-xl font-semibold text-slate-700">AI Market Video Engine</h1>

      {/* Video Card */}
      <div className="w-full rounded-xl bg-white p-5 shadow-sm">
        {/* Header */}
        <div className="mb-5 flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <span>Back</span>
            <span className="text-slate-300">|</span>
            <span className="font-medium text-slate-700">Video Update</span>
          </div>
          <div className="flex items-center gap-3">
            <Bell className="h-5 w-5 text-slate-400" />
            <div className="h-6 w-6 rounded-full border-2 border-slate-300" />
          </div>
        </div>

        {/* Title Section */}
        <div className="mb-4 flex items-start justify-between">
          <div>
            <h2 className="text-xl font-bold text-slate-900">Top Market Moves Today</h2>
            <p className="text-sm text-slate-500">Your quick AI-generated market wrap-up for the day.</p>
          </div>
          <button className="rounded-lg border border-slate-300 px-4 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-50">
            SHARE
          </button>
        </div>

        {/* Video Player */}
        <div className="mb-4 overflow-hidden rounded-xl border border-slate-200 bg-slate-100">
          {/* Video Thumbnail */}
          <div className="relative aspect-video bg-slate-200">
            {/* Illustrated presenter placeholder */}
            <div className="absolute inset-0 flex items-center justify-center bg-slate-800">
              <div className="flex flex-col items-center justify-center p-6 text-center text-white">
                <p className="mb-2 text-sm font-medium opacity-80">AI Presenter Ready</p>
                <div className="h-16 w-16 animate-pulse rounded-full bg-blue-500/20 flex items-center justify-center">
                  <div className="h-8 w-8 rounded-full bg-blue-500"></div>
                </div>
              </div>
            </div>
            {/* Play button overlay */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="flex h-14 w-14 cursor-pointer items-center justify-center rounded-full bg-white/10 shadow-lg backdrop-blur hover:bg-white/20 transition-all">
                <Play className="h-6 w-6 fill-white text-white" />
              </div>
            </div>
          </div>
          
          {/* Video Controls */}
          <div className="flex items-center gap-3 bg-white px-3 py-2">
            <Play className="h-4 w-4 text-slate-600 cursor-pointer" />
            <Pause className="h-4 w-4 text-slate-600 cursor-pointer" />
            <div className="relative flex-1">
              <div className="h-1 rounded-full bg-slate-200">
                <div className="h-1 w-1/4 rounded-full bg-slate-400" />
              </div>
              <div className="absolute left-1/4 top-1/2 h-3 w-3 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-slate-400 bg-white" />
            </div>
            <span className="text-xs text-slate-500">01:45</span>
            <span className="text-slate-300">◇</span>
          </div>
        </div>

        {/* Video Meta */}
        <div className="mb-5 flex items-center justify-between text-sm text-slate-500">
          <span>Just Updated</span>
          <div className="flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>AI Script Ready</span>
          </div>
        </div>

        {/* In This Update */}
        <div className="mb-5">
          <h3 className="mb-3 font-semibold text-slate-900">In This Update:</h3>
          {loading ? (
            <div className="py-8 flex flex-col items-center justify-center">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600 mb-4"></div>
              <div className="text-sm font-medium text-slate-500">Generating AI market briefing...</div>
            </div>
          ) : !data?.script || data.script.length === 0 ? (
            <div className="py-8 text-center">
              <p className="font-semibold text-slate-900 mb-1">No major updates. Market remains neutral.</p>
            </div>
          ) : (
            <ul className="space-y-3">
              {data?.script?.map((line: string, i: number) => (
                <li key={i} className="flex items-start gap-3">
                  <span className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-blue-500" />
                  <span className="text-sm text-slate-700 leading-relaxed">{line}</span>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* See More Section */}
        <div>
          <h3 className="mb-3 font-semibold text-slate-900">Explore AI Topics:</h3>
          <div className="flex flex-wrap gap-2">
            <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
              Daily Wrap
            </button>
            <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
              Sector Highlights
            </button>
            <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
              Top Gainers
            </button>
            <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
              Blocks/Insider Activity
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
