#!/usr/bin/env python
"""Download the raw time series behind the study.

Usage:
    python scripts/run_pipeline.py --start 2024-10-01 [--only prices,sec,hn,options]

Outputs land in data/raw/. Requires network access to:
    query1.finance.yahoo.com (or stooq.com), data.sec.gov, hn.algolia.com, cdn.cboe.com
In a sandboxed cloud session these hosts must be allowed in the environment's network settings.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from optlab.fetch import hn, options_chain, prices, sec_xbrl  # noqa: E402
from optlab.fetch._http import NetworkBlocked  # noqa: E402

RAW = ROOT / "data" / "raw"
TICKERS = ["NVDA", "CRWV", "QQQ", "SMH", "^VIX", "^VXN"]
SEC_CONCEPTS = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "NetIncomeLoss",
                "OperatingIncomeLoss", "InterestExpense", "LongTermDebt", "PaymentsToAcquirePropertyPlantAndEquipment"]
HN_QUERIES = ["CoreWeave", "Nvidia", "NVDA", "GPU shortage", "AI bubble", "neocloud"]


def step(name, fn):
    try:
        fn()
        print(f"[ok] {name}")
    except NetworkBlocked as e:
        print(f"[blocked] {name}: {e}")
    except Exception as e:  # keep going; the report must say what failed
        print(f"[error] {name}: {type(e).__name__}: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2024-10-01")
    ap.add_argument("--end", default=None)
    ap.add_argument("--only", default="prices,sec,hn,options")
    a = ap.parse_args()
    only = set(a.only.split(","))
    RAW.mkdir(parents=True, exist_ok=True)

    if "prices" in only:
        for t in TICKERS:
            step(f"prices {t}", lambda t=t: prices.daily(t, a.start, a.end).to_csv(RAW / f"prices_{t.strip('^')}.csv"))
    if "sec" in only:
        for tk in ["NVDA", "CRWV"]:
            for c in SEC_CONCEPTS:
                step(f"sec {tk} {c}", lambda tk=tk, c=c: sec_xbrl.quarterly_series(tk, c).to_csv(RAW / f"sec_{tk}_{c}.csv"))
    if "hn" in only:
        end = a.end or "2026-12-31"
        for q in HN_QUERIES:
            step(f"hn {q}", lambda q=q: hn.stories(q, a.start, end).to_csv(RAW / f"hn_{q.replace(' ', '_')}.csv", index=False))
    if "options" in only:
        for tk in ["NVDA", "CRWV"]:
            def snap(tk=tk):
                spot, chain = options_chain.cboe_chain(tk)
                chain.to_csv(RAW / f"chain_{tk}_{__import__('datetime').date.today()}.csv", index=False)
            step(f"options chain {tk}", snap)


if __name__ == "__main__":
    main()
