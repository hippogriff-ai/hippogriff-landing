"""SEC XBRL 'companyconcept' and 'companyfacts' APIs (free, no key, needs a UA header)."""
from __future__ import annotations

import pandas as pd

from ._http import get

CIK = {"NVDA": "0001045810", "CRWV": "0001769628"}
BASE = "https://data.sec.gov/api/xbrl"


def concept(ticker: str, concept: str = "Revenues", taxonomy: str = "us-gaap", unit: str = "USD") -> pd.DataFrame:
    url = f"{BASE}/companyconcept/CIK{CIK[ticker]}/{taxonomy}/{concept}.json"
    js = get(url, headers={"Accept": "application/json"}).json()
    df = pd.DataFrame(js["units"][unit])
    df["end"] = pd.to_datetime(df["end"])
    df["filed"] = pd.to_datetime(df["filed"])
    return df.sort_values(["end", "filed"])


def quarterly_series(ticker: str, concept_name: str) -> pd.Series:
    """Quarterly values, de-duplicated (latest filing wins). Handles 10-K Q4 derivation by
    subtracting the three prior 10-Q quarters when a quarterly 'frame' is missing."""
    df = concept(ticker, concept_name)
    df = df[df["form"].isin(["10-Q", "10-K"])]
    df["start"] = pd.to_datetime(df["start"])
    df["days"] = (df["end"] - df["start"]).dt.days
    q = df[df["days"].between(80, 100)].drop_duplicates("end", keep="last").set_index("end")["val"]
    fy = df[df["days"].between(350, 380)].drop_duplicates("end", keep="last").set_index("end")["val"]
    for end, val in fy.items():
        if end in q.index:
            continue
        prev = q[(q.index < end) & (q.index > end - pd.Timedelta(days=300))]
        if len(prev) == 3:
            q.loc[end] = val - prev.sum()
    return q.sort_index()
