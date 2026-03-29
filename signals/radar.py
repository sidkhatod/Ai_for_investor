import pandas as pd
from typing import Dict, Any

def detect_signals(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Detect trading signals based on historical stock data.
    
    Args:
        df (pd.DataFrame): DataFrame containing stock data with 'Close', 'High', 'Volume' columns.
        
    Returns:
        Dict[str, Any]: Dictionary containing 'signals' list and 'metrics' dictionary.
    """
    result = {
        "signals": [],
        "metrics": {}
    }
    
    if df is None or df.empty or len(df) < 20:
        return result

    latest_price = float(df['Close'].iloc[-1])
    latest_volume = float(df['Volume'].iloc[-1])
    
    avg_volume = float(df['Volume'].rolling(window=5).mean().iloc[-1])
    
    # Highs over the previous 10 days (excluding today)
    last_10d_high = float(df['High'].iloc[-11:-1].max())
    
    ma_5 = df['Close'].rolling(window=5).mean()
    ma_20 = df['Close'].rolling(window=20).mean()
    
    short_ma = float(ma_5.iloc[-1])
    long_ma = float(ma_20.iloc[-1])
    prev_ma5 = float(ma_5.iloc[-2])
    prev_ma20 = float(ma_20.iloc[-2])

    strong_signals = []
    signal_strength = 0.0

    # 1. Volume spike: latest volume > 1.3 * avg_volume
    if latest_volume > 1.3 * avg_volume:
        strong_signals.append("Volume Spike")
        signal_strength += 0.3

    # 2. Breakout and Near Breakout
    if latest_price >= last_10d_high:
        strong_signals.append("Breakout")
        signal_strength += 0.4
    elif latest_price >= 0.98 * last_10d_high:
        strong_signals.append("Near Breakout")
        signal_strength += 0.2

    # 3. Moving average crossover
    if prev_ma5 <= prev_ma20 and short_ma > long_ma:
        strong_signals.append("Bullish Crossover")
    elif prev_ma5 >= prev_ma20 and short_ma < long_ma:
        strong_signals.append("Bearish Crossover")

    # 4. Trend definition
    trend = "Uptrend" if short_ma > long_ma else "Downtrend"
    if trend == "Uptrend":
        signal_strength += 0.2

    result["signals"] = strong_signals + [trend]
    
    signal_strength = min(1.0, signal_strength)
    price_vs_short_ma_pct = ((latest_price - short_ma) / short_ma) * 100 if short_ma else 0.0
    volume_vs_avg_pct = ((latest_volume - avg_volume) / avg_volume) * 100 if avg_volume else 0.0

    # Populate metrics with exact percentage numbers and signal strength
    result["metrics"] = {
        "latest_price": latest_price,
        "avg_volume": avg_volume,
        "latest_volume": latest_volume,
        "short_ma": short_ma,
        "long_ma": long_ma,
        "signal_strength": round(signal_strength, 2),
        "price_vs_short_ma_pct": round(price_vs_short_ma_pct, 2),
        "volume_vs_avg_pct": round(volume_vs_avg_pct, 2)
    }
    
    return result
