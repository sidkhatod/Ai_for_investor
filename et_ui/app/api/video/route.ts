import { NextResponse } from "next/server";

export async function GET() {
  try {
    const payload = {
      portfolio: [
        { ticker: "RELIANCE.NS", weight: 0.4 },
        { ticker: "TCS.NS", weight: 0.3 },
        { ticker: "INFY.NS", weight: 0.3 }
      ],
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

    const res = await fetch("http://localhost:8000/video", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      throw new Error(`Failed to fetch: ${res.statusText}`);
    }

    const data = await res.json();
    
    // Ensure script is returned as an array of strings for the UI
    let scriptArray = data.script;
    if (typeof data.script === 'string') {
      scriptArray = data.script.split('\n').filter((l: string) => l.trim().length > 0);
    }
    
    return NextResponse.json({
      script: scriptArray,
      summary: data.summary || {}
    });
  } catch (error) {
    return NextResponse.json({ error: "Backend unavailable" });
  }
}

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const payload = {
            portfolio: body.portfolio || [
                { ticker: "RELIANCE.NS", weight: 0.4 },
                { ticker: "TCS.NS", weight: 0.3 },
                { ticker: "INFY.NS", weight: 0.3 }
            ],
            stocks: body.stocks || [
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

        const res = await fetch("http://localhost:8000/video", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (!res.ok) {
            throw new Error(`Failed to fetch: ${res.statusText}`);
        }

        const data = await res.json();
        
        // Ensure script is returned as an array of strings for the UI
        let scriptArray = data.script;
        if (typeof data.script === 'string') {
        scriptArray = data.script.split('\n').filter((l: string) => l.trim().length > 0);
        }
        
        return NextResponse.json({
            script: scriptArray,
            summary: data.summary || {}
        });
    } catch (error) {
        return NextResponse.json({ error: "Backend unavailable" });
    }
}
