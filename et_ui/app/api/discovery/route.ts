import { NextResponse } from "next/server";

export async function GET() {
  try {
    const payload = {
      stocks: [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ITC.NS",
        "ADANIENT.NS",
        "TATASTEEL.NS",
        "IRCTC.NS",
        "SBIN.NS"
      ]
    };

    const res = await fetch("http://localhost:8000/discovery", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      throw new Error(`Failed to fetch: ${res.statusText}`);
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: "Backend unavailable" });
  }
}
