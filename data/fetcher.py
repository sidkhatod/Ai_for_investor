import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def get_stock_data(ticker: str, period: str = "3mo", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch historical stock data using yfinance.
    
    Args:
        ticker (str): Stock ticker symbol.
        period (str): Data period to download (e.g., '3mo', '1y').
        interval (str): Data interval (e.g., '1d', '1wk').
        
    Returns:
        pd.DataFrame: DataFrame containing historical stock data.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        
        # Ensure at least 60 rows of data for rolling calculations by defaulting to 3mo.
        # If data length < 30, refetch with period="6mo"
        if not df.empty and len(df) < 30:
            logger.info(f"Data length {len(df)} < 30 for ticker {ticker}. Refetching with period='6mo'.")
            df = stock.history(period="6mo", interval=interval)
            
        if df.empty:
            logger.warning(f"No data fetched for ticker {ticker} with requested period/interval.")
            
        return df
    except Exception as e:
        logger.error(f"Error fetching data for ticker {ticker}: {e}")
        # Return empty dataframe on error for robustness
        return pd.DataFrame()
