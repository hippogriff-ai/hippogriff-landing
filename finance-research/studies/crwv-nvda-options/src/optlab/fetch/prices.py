"""Daily OHLCV. Primary: Yahoo via yfinance. Fallback: Stooq CSV."""
from __future__ import annotations

import io

import pandas as pd

from ._http import NetworkBlocked, get


def yahoo(ticker: str, start: str, end: str | None = None) -> pd.DataFrame:
    import yfinance as yf

    df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)
    if df is None or df.empty:
        raise NetworkBlocked(f"yfinance returned nothing for {ticker} (network policy or bad ticker)")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.rename(columns=str.lower)[["open", "high", "low", "close", "adj close", "volume"]]
    df.index.name = "date"
    return df


def stooq(ticker: str, start: str, end: str) -> pd.DataFrame:
    sym = f"{ticker.lower()}.us"
    url = f"https://stooq.com/q/d/l/?s={sym}&i=d&d1={start.replace('-', '')}&d2={end.replace('-', '')}"
    r = get(url)
    df = pd.read_csv(io.StringIO(r.text), parse_dates=["Date"]).rename(columns=str.lower).set_index("date")
    df["adj close"] = df["close"]
    return df


def daily(ticker: str, start: str, end: str | None = None) -> pd.DataFrame:
    try:
        return yahoo(ticker, start, end)
    except Exception:
        return stooq(ticker, start, end or pd.Timestamp.today().strftime("%Y-%m-%d"))
