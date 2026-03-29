import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const ticker = searchParams.get("ticker") || "RELIANCE.NS";

    const res = await fetch(`http://localhost:8000/stock?ticker=${ticker}`, {
      method: "GET",
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
