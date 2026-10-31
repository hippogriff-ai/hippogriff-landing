"""Cross-asset and cross-signal relationships."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def rolling_beta(y: pd.Series, x: pd.Series, window: int = 60) -> pd.Series:
    """Rolling OLS beta of y on x using log returns."""
    ry = np.log(y.astype(float)).diff()
    rx = np.log(x.astype(float)).diff()
    df = pd.concat([ry.rename("y"), rx.rename("x")], axis=1).dropna()
    cov = df["y"].rolling(window).cov(df["x"])
    var = df["x"].rolling(window).var()
    return (cov / var).dropna()


def lead_lag_corr(a: pd.Series, b: pd.Series, max_lag: int = 10, method: str = "spearman") -> pd.DataFrame:
    """corr(a[t], b[t+lag]) for lag in [-max_lag, max_lag]. Positive lag with high corr means
    `a` leads `b`. Inputs should be stationary (returns, changes, z-scores)."""
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    rows = []
    for lag in range(-max_lag, max_lag + 1):
        shifted = df["b"].shift(-lag)
        pair = pd.concat([df["a"], shifted], axis=1).dropna()
        if len(pair) < 8:
            rows.append((lag, np.nan, np.nan, len(pair)))
            continue
        if method == "spearman":
            r, p = stats.spearmanr(pair.iloc[:, 0], pair.iloc[:, 1])
        else:
            r, p = stats.pearsonr(pair.iloc[:, 0], pair.iloc[:, 1])
        rows.append((lag, float(r), float(p), len(pair)))
    return pd.DataFrame(rows, columns=["lag", "corr", "pvalue", "n"]).set_index("lag")


def granger(a: pd.Series, b: pd.Series, maxlag: int = 5) -> pd.DataFrame:
    """Does `a` Granger-cause `b`? Returns F-test p-values per lag (statsmodels)."""
    from statsmodels.tsa.stattools import grangercausalitytests

    df = pd.concat([b.rename("b"), a.rename("a")], axis=1).dropna()
    res = grangercausalitytests(df[["b", "a"]], maxlag=maxlag)
    rows = [(lag, r[0]["ssr_ftest"][1]) for lag, r in res.items()]
    return pd.DataFrame(rows, columns=["lag", "pvalue"]).set_index("lag")


def zscore(s: pd.Series, window: int = 26) -> pd.Series:
    """Rolling z-score (useful for attention counts)."""
    return (s - s.rolling(window).mean()) / s.rolling(window).std(ddof=1)


def forward_return(close: pd.Series, horizon: int) -> pd.Series:
    """Simple return from t to t+horizon, indexed at t."""
    c = close.astype(float)
    return (c.shift(-horizon) / c - 1.0)
