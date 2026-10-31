#!/usr/bin/env python
"""Quantitative summary of the curated earnings datasets -> report/tables.md

Cells in the curated CSVs often hold several provider figures ("5.4 (ORATS) / 6.5 (TipRanks)").
`first_num` takes the FIRST number in a cell, which by construction is the primary source we chose.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from optlab.analysis.vol import earnings_move_stats  # noqa: E402

CUR, OUT = ROOT / "data" / "curated", ROOT / "report" / "tables.md"
NUM = re.compile(r"[-+]?\d+(?:\.\d+)?")


def first_num(x) -> float:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return np.nan
    s = str(x)
    if s.strip().upper().startswith("NA"):
        return np.nan
    m = NUM.search(s.replace(",", ""))
    return float(m.group()) if m else np.nan


def nvda() -> tuple[pd.DataFrame, str]:
    df = pd.read_csv(CUR / "nvda_earnings.csv")
    t = pd.DataFrame({
        "report": df["report_date"], "quarter": df["fiscal_quarter"],
        "rev_bn": df["revenue_bn"].map(first_num), "rev_beat_%": df["revenue_beat_pct"].map(first_num),
        "guide_vs_cons_%": df["guidance_vs_consensus_pct"].map(first_num),
        "implied_%": df["options_implied_move_pct"].map(first_num), "actual_%": df["one_day_move_pct"].map(first_num),
        "drift_5d_%": df["drift_5d_pct"].map(first_num), "drift_20d_%": df["drift_20d_pct"].map(first_num)})
    t["|actual|/implied"] = (t["actual_%"].abs() / t["implied_%"]).round(2)
    st = earnings_move_stats(t["implied_%"] / 100, t["actual_%"] / 100)
    # Spearman correlations: surprise -> reaction
    from scipy.stats import spearmanr
    rows = []
    for col in ["rev_beat_%", "guide_vs_cons_%"]:
        d = t[[col, "actual_%"]].dropna()
        r, p = spearmanr(d[col], d["actual_%"])
        rows.append(f"| {col} vs next-day move | {len(d)} | {r:+.2f} | {p:.2f} |")
    d = t[["actual_%", "drift_20d_%"]].dropna()
    r, p = spearmanr(d["actual_%"], d["drift_20d_%"])
    rows.append(f"| day-1 move vs 21-day drift | {len(d)} | {r:+.2f} | {p:.2f} |")
    md = ["## NVDA: eight earnings reports, Nov 2024 - Aug 2026", "",
          t.to_markdown(index=False, floatfmt=".1f"), "",
          f"- Events with both implied and actual: **{st.n}**",
          f"- Share of events where |actual| > implied (straddle buyer wins): **{st.hit_rate_actual_gt_implied:.0%}**",
          f"- Mean implied move **{st.mean_implied:.1%}** vs mean |actual| **{st.mean_abs_actual:.1%}**; median |actual|/implied **{st.median_ratio:.2f}**",
          f"- Average straddle P&L as % of premium (first-order proxy): **{st.mean_straddle_pnl_pct_of_premium:+.0%}**", "",
          "| Relationship | n | Spearman rho | p |", "|---|---|---|---|", *rows, ""]
    return t, "\n".join(md)


def crwv() -> tuple[pd.DataFrame, str]:
    df = pd.read_csv(CUR / "crwv_earnings.csv")
    df = df[~df["quarter"].astype(str).str.contains("upcoming")]
    t = pd.DataFrame({
        "report": df["report_date"].astype(str).str[:10], "quarter": df["quarter"],
        "rev_m": df["revenue_musd"].map(first_num), "rev_beat_%": df["beat_pct"].map(first_num),
        "backlog_bn": df["revenue_backlog_busd"].map(first_num),
        "ebitda_margin_%": df["adj_ebitda_margin_pct"].map(first_num),
        "interest_m": df["interest_expense_musd"].map(first_num),
        "implied_%": df["options_implied_move_pct"].map(first_num), "actual_%": df["one_day_move_pct"].map(first_num)})
    # supplementary implied moves found for the 2025 reports (see options_vol_observations.csv / notes)
    sup = {"2025-08-12": 18.0, "2025-11-10": 15.0}   # tastylive expected-move previews; TheFly quoted 12.5% for Nov 2025
    for d, v in sup.items():
        m = t["report"] == d
        t.loc[m & t["implied_%"].isna(), "implied_%"] = v
    t["|actual|/implied"] = (t["actual_%"].abs() / t["implied_%"]).round(2)
    both = t.dropna(subset=["implied_%", "actual_%"])
    st = earnings_move_stats(both["implied_%"] / 100, both["actual_%"] / 100)
    md = ["## CRWV: six earnings reports, May 2025 - Aug 2026", "",
          t.to_markdown(index=False, floatfmt=".1f"), "",
          "Implied moves for Aug-2025 and Nov-2025 are tastylive pre-report expected moves (18% and 15%); TheFly quoted 12.5% for Nov-2025. Q1-2025 implied move not found.", "",
          f"- Events with both implied and actual: **{st.n}**",
          f"- Share of events where |actual| > implied: **{st.hit_rate_actual_gt_implied:.0%}**",
          f"- Mean implied **{st.mean_implied:.1%}** vs mean |actual| **{st.mean_abs_actual:.1%}**; median |actual|/implied **{st.median_ratio:.2f}**",
          f"- Average straddle P&L as % of premium: **{st.mean_straddle_pnl_pct_of_premium:+.0%}**", ""]
    return t, "\n".join(md)


def crwv_credit_vs_price() -> str:
    pts = pd.read_csv(CUR / "crwv_price_points.csv")
    cds = pd.DataFrame([("2025-11-14", 600), ("2026-06-03", 452), ("2026-10-15", 1140), ("2026-10-23", 1146)],
                       columns=["date", "cds_bp"])
    pts["date"] = pd.to_datetime(pts["date"]); cds["date"] = pd.to_datetime(cds["date"])
    m = pd.merge_asof(cds.sort_values("date"), pts.sort_values("date"), on="date", direction="nearest")
    return "\n".join(["## CRWV: 5-year CDS vs share price at the same dates", "",
                      m[["date", "cds_bp", "price", "basis"]].to_markdown(index=False), ""])


if __name__ == "__main__":
    nt, nmd = nvda()
    ct, cmd = crwv()
    OUT.write_text("# Tables generated by scripts/analyze_curated.py\n\n" + nmd + "\n" + cmd + "\n" + crwv_credit_vs_price())
    nt.to_csv(ROOT / "report" / "nvda_earnings_table.csv", index=False)
    ct.to_csv(ROOT / "report" / "crwv_earnings_table.csv", index=False)
    print(OUT.read_text())
