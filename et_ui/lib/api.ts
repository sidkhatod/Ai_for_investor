// API Wrapper Client for Next.js UI integration

export async function fetchDiscovery() {
  const res = await fetch("/api/discovery");
  if (!res.ok) throw new Error("Failed to fetch discovery");
  return res.json();
}

export async function fetchStock(ticker: string) {
  const res = await fetch(`/api/stock?ticker=${encodeURIComponent(ticker)}`);
  if (!res.ok) throw new Error("Failed to fetch stock");
  return res.json();
}

export async function analyzePortfolio(portfolio: any[]) {
  const res = await fetch("/api/portfolio", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(portfolio),
  });
  if (!res.ok) throw new Error("Failed to analyze portfolio");
  return res.json();
}

export async function fetchVideoScript() {
  const res = await fetch("/api/video");
  if (!res.ok) throw new Error("Failed to fetch video script");
  return res.json();
}
