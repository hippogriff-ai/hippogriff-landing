"""Volatility utilities.

All volatilities are annualized decimals (0.45 == 45%). Moves are decimals too.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

TRADING_DAYS = 252


def log_returns(close: pd.Series) -> pd.Series:
    """Daily log returns, index preserved, first value dropped."""
    close = close.astype(float)
    return np.log(close / close.shift(1)).dropna()


def realized_vol(close: pd.Series, window: int = 21, annualize: int = TRADING_DAYS) -> pd.Series:
    """Close-to-close realized volatility over a rolling window (annualized)."""
    r = log_returns(close)
    return r.rolling(window).std(ddof=1) * math.sqrt(annualize)


def parkinson_vol(high: pd.Series, low: pd.Series, window: int = 21, annualize: int = TRADING_DAYS) -> pd.Series:
    """Parkinson high-low range estimator. Roughly 5x more efficient than close-to-close
    when there are no jumps; it under-estimates when overnight gaps dominate (true of
    earnings nights), which is exactly why we report both."""
    hl = np.log(high.astype(float) / low.astype(float)) ** 2
    factor = 1.0 / (4.0 * math.log(2.0))
    return np.sqrt(factor * hl.rolling(window).mean() * annualize)


def iv_to_expected_move(iv: float, days: int, basis: int = 365) -> float:
    """One-standard-deviation expected move (decimal) implied by an annualized IV over `days` calendar days."""
    return iv * math.sqrt(days / basis)


def straddle_implied_move(call_mid: float, put_mid: float, spot: float, adj: float = 0.85) -> float:
    """Market convention: expected absolute move ~= 0.85 * ATM straddle price / spot.

    The 0.85 factor converts the straddle (which pays |S_T - K|) into the expected
    absolute move under a normal approximation (E|X| = sigma*sqrt(2/pi) ~= 0.8*sigma,
    then practitioners round up for skew). Bloomberg/desks quote the raw straddle
    without the factor; set adj=1.0 to match them.
    """
    return adj * (call_mid + put_mid) / spot


def variance_risk_premium(iv: pd.Series, rv_forward: pd.Series) -> pd.Series:
    """IV minus subsequently realized vol, aligned on the IV observation date.

    Positive values mean options were 'expensive' ex post. `rv_forward` must already be
    shifted so that rv_forward[t] is the realized vol over (t, t+window]."""
    return (iv - rv_forward).dropna()


@dataclass
class EarningsMoveStats:
    n: int
    hit_rate_actual_gt_implied: float   # share of events where |actual| > implied (straddle buyers win)
    mean_abs_actual: float
    mean_implied: float
    mean_ratio_actual_over_implied: float
    median_ratio: float
    mean_straddle_pnl_pct_of_premium: float  # (|actual| - implied) / implied, averaged


def earnings_move_stats(implied: pd.Series, actual: pd.Series) -> EarningsMoveStats:
    """Compare options-implied moves to actual next-day moves (both decimals, aligned index).

    The straddle P&L proxy treats the implied move as the straddle cost (in % of spot) and
    |actual| as its payoff. It ignores the 0.85 adjustment and gamma scalping, so it is a
    conservative first-order view of whether vol was over- or under-priced."""
    df = pd.DataFrame({"implied": implied.abs(), "actual": actual.abs()}).dropna()
    if df.empty:
        raise ValueError("no overlapping observations")
    ratio = df["actual"] / df["implied"]
    return EarningsMoveStats(
        n=len(df),
        hit_rate_actual_gt_implied=float((df["actual"] > df["implied"]).mean()),
        mean_abs_actual=float(df["actual"].mean()),
        mean_implied=float(df["implied"].mean()),
        mean_ratio_actual_over_implied=float(ratio.mean()),
        median_ratio=float(ratio.median()),
        mean_straddle_pnl_pct_of_premium=float(((df["actual"] - df["implied"]) / df["implied"]).mean()),
    )


def iv_crush_estimate(iv_before: float, iv_after: float) -> float:
    """Fractional fall in IV across the event (0.3 == IV fell 30%)."""
    if iv_before <= 0:
        raise ValueError("iv_before must be positive")
    return 1.0 - iv_after / iv_before
