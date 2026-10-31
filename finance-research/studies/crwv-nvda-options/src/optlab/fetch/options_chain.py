"""Current option chains (there is no free historical chain; snapshot and persist daily).

Cboe delayed quotes return the full chain with IV and greeks in one JSON call.
"""
from __future__ import annotations

import re

import pandas as pd

from ._http import get

CBOE = "https://cdn.cboe.com/api/global/delayed_quotes/options/{sym}.json"
_OCC = re.compile(r"^(?P<root>[A-Z]+)(?P<ymd>\d{6})(?P<cp>[CP])(?P<strike>\d{8})$")


def cboe_chain(ticker: str) -> tuple[float, pd.DataFrame]:
    js = get(CBOE.format(sym=ticker)).json()["data"]
    spot = float(js["current_price"])
    rows = []
    for o in js["options"]:
        m = _OCC.match(o["option"])
        if not m:
            continue
        rows.append({"expiry": pd.to_datetime(m["ymd"], format="%y%m%d"), "type": m["cp"],
                     "strike": int(m["strike"]) / 1000.0, "bid": o.get("bid"), "ask": o.get("ask"),
                     "iv": o.get("iv"), "delta": o.get("delta"), "gamma": o.get("gamma"),
                     "open_interest": o.get("open_interest"), "volume": o.get("volume")})
    df = pd.DataFrame(rows)
    df["mid"] = (df["bid"] + df["ask"]) / 2
    return spot, df


def atm_straddle(chain: pd.DataFrame, spot: float, expiry: pd.Timestamp) -> dict:
    e = chain[chain["expiry"] == expiry]
    k = e.iloc[(e["strike"] - spot).abs().argsort()[:1]]["strike"].item()
    c = e[(e["strike"] == k) & (e["type"] == "C")]["mid"].item()
    p = e[(e["strike"] == k) & (e["type"] == "P")]["mid"].item()
    return {"strike": k, "call_mid": c, "put_mid": p, "straddle": c + p, "straddle_pct": (c + p) / spot}


def skew_25d(chain: pd.DataFrame, expiry: pd.Timestamp) -> float:
    """IV(25-delta put) - IV(25-delta call): positive = downside protection bid."""
    e = chain[chain["expiry"] == expiry].dropna(subset=["delta", "iv"])
    put = e[(e["type"] == "P")].iloc[(e[e["type"] == "P"]["delta"] + 0.25).abs().argsort()[:1]]
    call = e[(e["type"] == "C")].iloc[(e[e["type"] == "C"]["delta"] - 0.25).abs().argsort()[:1]]
    return float(put["iv"].item() - call["iv"].item())
