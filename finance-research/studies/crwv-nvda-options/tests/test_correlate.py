import numpy as np
import pandas as pd

from optlab.analysis import correlate


def test_rolling_beta_recovers_beta():
    rng = np.random.default_rng(2)
    n = 1000
    idx = pd.bdate_range("2022-01-01", periods=n)
    rx = rng.normal(0, 0.01, n)
    ry = 2.0 * rx + rng.normal(0, 0.003, n)
    x = pd.Series(100 * np.exp(np.cumsum(rx)), index=idx)
    y = pd.Series(100 * np.exp(np.cumsum(ry)), index=idx)
    b = correlate.rolling_beta(y, x, window=120)
    assert abs(b.mean() - 2.0) < 0.1


def test_lead_lag_detects_leader():
    rng = np.random.default_rng(3)
    n = 500
    a = pd.Series(rng.normal(0, 1, n))
    b = a.shift(3).fillna(0) + rng.normal(0, 0.3, n)  # a leads b by 3
    ll = correlate.lead_lag_corr(a, b, max_lag=6)
    assert ll["corr"].idxmax() == 3


def test_granger_runs():
    rng = np.random.default_rng(4)
    n = 300
    a = pd.Series(rng.normal(0, 1, n))
    b = 0.8 * a.shift(1).fillna(0) + rng.normal(0, 0.5, n)
    g = correlate.granger(a, b, maxlag=3)
    assert g.loc[1, "pvalue"] < 0.01


def test_forward_return_and_zscore():
    s = pd.Series([100, 110, 121, 133.1])
    fr = correlate.forward_return(s, 1)
    assert abs(fr.iloc[0] - 0.10) < 1e-9
    z = correlate.zscore(pd.Series(range(40), dtype=float), window=10)
    assert z.dropna().shape[0] == 31
