"""Event-study helpers: windows around earnings or catalysts."""
from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


def _nearest_index_on_or_after(idx: pd.DatetimeIndex, when: pd.Timestamp) -> int:
    pos = idx.searchsorted(when)
    if pos >= len(idx):
        raise KeyError(f"{when.date()} is after the last price date")
    return int(pos)


def event_window_returns(
    close: pd.Series,
    event_dates: Iterable[str | pd.Timestamp],
    pre: int = 5,
    post: int = 20,
    after_close: bool = True,
) -> pd.DataFrame:
    """Cumulative simple returns relative to the event-day close, for t in [-pre, +post].

    `after_close=True` (earnings released after the bell) anchors t=0 at the close of the
    report day, so t=+1 is the first full reaction day. Returns a DataFrame indexed by
    relative day, one column per event date."""
    close = close.astype(float).sort_index()
    idx = close.index
    out = {}
    for d in event_dates:
        d = pd.Timestamp(d)
        i0 = _nearest_index_on_or_after(idx, d)
        if not after_close:
            i0 -= 1  # anchor on the prior close when the event lands during the session
        lo, hi = max(0, i0 - pre), min(len(idx) - 1, i0 + post)
        seg = close.iloc[lo : hi + 1]
        rel = np.arange(lo - i0, hi - i0 + 1)
        out[d.strftime("%Y-%m-%d")] = pd.Series((seg / close.iloc[i0] - 1.0).values, index=rel)
    return pd.DataFrame(out)


def market_model_abnormal_returns(
    stock_close: pd.Series,
    bench_close: pd.Series,
    event_dates: Iterable[str | pd.Timestamp],
    est_window: int = 120,
    pre: int = 5,
    post: int = 20,
) -> pd.DataFrame:
    """Cumulative abnormal returns (CAR) using a market-model beta estimated on the
    `est_window` trading days ending 10 days before each event."""
    s = np.log(stock_close.astype(float)).diff().dropna()
    b = np.log(bench_close.astype(float)).diff().dropna()
    df = pd.concat([s.rename("s"), b.rename("b")], axis=1).dropna()
    idx = df.index
    out = {}
    for d in event_dates:
        d = pd.Timestamp(d)
        i0 = _nearest_index_on_or_after(idx, d)
        est = df.iloc[max(0, i0 - 10 - est_window) : i0 - 10]
        if len(est) < 30:
            continue
        beta, alpha = np.polyfit(est["b"], est["s"], 1)
        win = df.iloc[max(0, i0 - pre) : min(len(df), i0 + post + 1)]
        ar = win["s"] - (alpha + beta * win["b"])
        rel = np.arange(-min(pre, i0), len(win) - min(pre, i0))
        car = ar.cumsum()
        out[d.strftime("%Y-%m-%d")] = pd.Series(car.values, index=rel)
    return pd.DataFrame(out)


def post_event_drift(windows: pd.DataFrame, horizon: int = 20) -> pd.DataFrame:
    """From an event_window_returns frame, extract the day-1 reaction and the drift
    from day 1 to `horizon` (does the initial move continue or mean-revert?)."""
    day1 = windows.loc[1]
    dayh = windows.loc[horizon]
    drift = (1 + dayh) / (1 + day1) - 1
    return pd.DataFrame({"day1": day1, f"day{horizon}": dayh, "drift_after_day1": drift,
                         "continuation": np.sign(day1) == np.sign(drift)})
