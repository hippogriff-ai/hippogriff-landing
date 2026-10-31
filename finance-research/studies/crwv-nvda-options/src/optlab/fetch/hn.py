"""Hacker News via the Algolia search API (free)."""
from __future__ import annotations

import time

import pandas as pd

from ._http import get

API = "https://hn.algolia.com/api/v1/search_by_date"


def stories(query: str, start: str, end: str, pause: float = 0.3) -> pd.DataFrame:
    t0 = int(pd.Timestamp(start).timestamp())
    t1 = int(pd.Timestamp(end).timestamp())
    rows, page = [], 0
    while True:
        js = get(API, params={"query": query, "tags": "story", "hitsPerPage": 1000, "page": page,
                              "numericFilters": f"created_at_i>{t0},created_at_i<{t1}"}).json()
        for h in js.get("hits", []):
            rows.append({"created_at": h["created_at"], "title": h.get("title"), "url": h.get("url"),
                         "points": h.get("points"), "num_comments": h.get("num_comments"),
                         "objectID": h["objectID"], "query": query})
        page += 1
        if page >= js.get("nbPages", 0):
            break
        time.sleep(pause)
    df = pd.DataFrame(rows)
    if not df.empty:
        df["created_at"] = pd.to_datetime(df["created_at"])
    return df


def weekly_attention(df: pd.DataFrame) -> pd.DataFrame:
    """Stories, total points and comments per ISO week."""
    g = df.set_index("created_at").resample("W")
    return pd.DataFrame({"stories": g["objectID"].count(), "points": g["points"].sum(),
                         "comments": g["num_comments"].sum()})
