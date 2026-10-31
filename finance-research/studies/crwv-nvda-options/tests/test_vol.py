import math

import numpy as np
import pandas as pd
import pytest

from optlab.analysis import vol


def _gbm(n=600, sigma=0.40, seed=0):
    rng = np.random.default_rng(seed)
    r = rng.normal(0, sigma / math.sqrt(252), n)
    idx = pd.bdate_range("2024-01-01", periods=n)
    return pd.Series(100 * np.exp(np.cumsum(r)), index=idx)


def test_realized_vol_recovers_sigma():
    s = _gbm(n=5000, sigma=0.40)
    rv = vol.realized_vol(s, window=252).dropna()
    assert abs(rv.mean() - 0.40) < 0.03


def test_parkinson_close_to_cc_for_diffusion():
    rng = np.random.default_rng(1)
    n = 3000
    idx = pd.bdate_range("2020-01-01", periods=n)
    close = pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.02, n))), index=idx)
    # synthetic intraday range consistent with sigma=0.02/day
    high = close * np.exp(abs(rng.normal(0, 0.02, n)))
    low = close * np.exp(-abs(rng.normal(0, 0.02, n)))
    pv = vol.parkinson_vol(high, low, window=252).dropna().mean()
    assert 0.2 < pv < 0.6


def test_iv_to_expected_move():
    assert math.isclose(vol.iv_to_expected_move(0.50, 365), 0.50)
    assert math.isclose(vol.iv_to_expected_move(0.40, 7), 0.40 * math.sqrt(7 / 365))


def test_straddle_implied_move():
    assert math.isclose(vol.straddle_implied_move(5, 5, 100, adj=1.0), 0.10)
    assert math.isclose(vol.straddle_implied_move(5, 5, 100), 0.085)


def test_earnings_move_stats():
    implied = pd.Series([0.08, 0.08, 0.10, 0.07])
    actual = pd.Series([0.04, -0.09, 0.03, -0.02])
    st = vol.earnings_move_stats(implied, actual)
    assert st.n == 4
    assert math.isclose(st.hit_rate_actual_gt_implied, 0.25)
    assert st.mean_ratio_actual_over_implied < 1
    assert st.mean_straddle_pnl_pct_of_premium < 0


def test_iv_crush():
    assert math.isclose(vol.iv_crush_estimate(0.80, 0.56), 0.30)
    with pytest.raises(ValueError):
        vol.iv_crush_estimate(0, 0.5)
