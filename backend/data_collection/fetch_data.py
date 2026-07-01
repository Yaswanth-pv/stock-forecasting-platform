"""
fetch_data.py
Fetches historical stock data using yfinance and stores it in a local SQLite database.
"""

import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import os

# Database will live in the data/ folder
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "stock_data.db")
engine = create_engine(f"sqlite:///{DB_PATH}")


def fetch_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a given ticker.

    Args:
        ticker: Stock symbol, e.g. "AAPL"
        period: How far back to fetch, e.g. "1y", "6mo", "5d"

    Returns:
        DataFrame with columns: Date, Open, High, Low, Close, Volume
    """
    data = yf.download(ticker, period=period)

    # yfinance sometimes returns multi-level columns; flatten them
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()
    data["Ticker"] = ticker
    return data


def save_to_db(data: pd.DataFrame, table_name: str = "stock_prices"):
    """Save fetched data into the SQLite database, appending new rows."""
    data.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"Saved {len(data)} rows to table '{table_name}'")


if __name__ == "__main__":
    ticker = input("Enter stock ticker (e.g. AAPL): ").strip().upper()
    df = fetch_stock_data(ticker)
    print(df.head())
    save_to_db(df)
    print(f"Done. Data stored at: {DB_PATH}")