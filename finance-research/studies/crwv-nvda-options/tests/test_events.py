import numpy as np
import pandas as pd

from optlab.analysis import events


def _flat_then_jump():
    idx = pd.bdate_range("2025-01-01", periods=60)
    px = pd.Series(100.0, index=idx)
    # event after close on day 30; day 31 gaps +10%, then drifts +0.2%/day
    px.iloc[31:] = 110.0 * (1.002 ** np.arange(len(idx) - 31))
    return px


def test_event_window_anchors_on_event_close():
    px = _flat_then_jump()
    d = px.index[30]
    w = events.event_window_returns(px, [d], pre=2, post=5)
    col = w.columns[0]
    assert w.loc[0, col] == 0
    assert abs(w.loc[1, col] - 0.10) < 1e-9
    assert w.loc[5, col] > w.loc[1, col]


def test_post_event_drift_continuation():
    px = _flat_then_jump()
    w = events.event_window_returns(px, [px.index[30]], pre=2, post=20)
    d = events.post_event_drift(w, horizon=20)
    assert bool(d["continuation"].iloc[0]) is True
    assert d["drift_after_day1"].iloc[0] > 0


def test_market_model_car_removes_beta_component():
    rng = np.random.default_rng(0)
    idx = pd.bdate_range("2024-01-01", periods=400)
    rb = rng.normal(0, 0.01, 400)
    rs = 1.5 * rb + rng.normal(0, 0.002, 400)
    bench = pd.Series(100 * np.exp(np.cumsum(rb)), index=idx)
    stock = pd.Series(100 * np.exp(np.cumsum(rs)), index=idx)
    car = events.market_model_abnormal_returns(stock, bench, [idx[300]], pre=5, post=20)
    # with no idiosyncratic jump, CAR over the window should be small relative to raw moves
    assert car.abs().max().item() < 0.05
