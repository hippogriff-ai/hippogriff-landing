#!/usr/bin/env python
"""Build the report figures from data/curated/*.csv.

Every figure degrades gracefully: if a dataset or column is missing the figure is skipped
with a message, never faked.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
CUR = ROOT / "data" / "curated"
FIG = ROOT / "report" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# brand-neutral palette (see dataviz skill); NVDA = teal, CRWV = orange, context = greys
C_NVDA, C_CRWV, C_GREY, C_ACCENT, C_NEG = "#1B998B", "#E4572E", "#8A8F98", "#4C6EF5", "#C0392B"
plt.rcParams.update({"figure.dpi": 130, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.25, "font.size": 9, "axes.titleweight": "bold"})


def load(name: str) -> pd.DataFrame | None:
    p = CUR / name
    if not p.exists():
        print(f"[skip] {name} not found")
        return None
    df = pd.read_csv(p)
    df.columns = [c.strip() for c in df.columns]
    return df


def num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.replace("%", "").str.replace("$", "").str.replace(",", ""), errors="coerce")


def crwv_points() -> pd.DataFrame | None:
    c = load("crwv_price_points.csv")
    if c is None:
        return None
    c = c[~c["basis"].astype(str).str.contains("intraday")].copy()
    c["month_end"] = pd.to_datetime(c["date"]); c["close"] = num(c["price"])
    c["derived"] = c["basis"].astype(str).str.contains("derived|unverified|approx")
    return c.dropna(subset=["close"]).sort_values("month_end")


def fig_price_paths():
    n, c = load("nvda_monthly_close.csv"), crwv_points()
    if n is None or c is None:
        return
    n["month_end"] = pd.to_datetime(n["month_end"])
    n["close"] = num(n["close"])
    n = n.dropna(subset=["close"]).sort_values("month_end")
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.plot(n["month_end"], n["close"], color=C_NVDA, lw=2, label="NVDA (left axis)")
    ax.set_ylabel("NVDA close ($)")
    ax2 = ax.twinx(); ax2.grid(False)
    ax2.plot(c["month_end"], c["close"], color=C_CRWV, lw=2, label="CRWV (right axis; dated points, see crwv_price_points.csv)")
    der = c[c["derived"]]
    ax2.scatter(der["month_end"], der["close"], color="white", edgecolor=C_CRWV, s=18, zorder=4, label="CRWV derived point")
    ax2.set_ylabel("CRWV price ($)")
    ev = load("catalysts.csv")
    if ev is not None:
        ev["date"] = pd.to_datetime(ev["date"], errors="coerce")
        for _, r in ev.dropna(subset=["date"]).iterrows():
            ax.axvline(r["date"], color=C_GREY, lw=0.6, alpha=0.5)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left", frameon=False)
    ax.set_title("NVDA month-end closes and CRWV dated price points; grey lines = catalysts in catalysts.csv")
    fig.tight_layout(); fig.savefig(FIG / "01_price_paths.png"); plt.close(fig)
    print("[ok] 01_price_paths.png")


def _implied_vs_actual(df: pd.DataFrame, label_col: str, color: str, title: str, fname: str):
    if df is None:
        return
    imp, act = num(df["options_implied_move_pct"]), num(df["one_day_move_pct"])
    m = imp.notna() & act.notna()
    if m.sum() == 0:
        print(f"[skip] {fname}: no implied/actual pairs"); return
    d = df[m].copy(); d["imp"], d["act"] = imp[m].abs(), act[m]
    x = np.arange(len(d))
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.bar(x - 0.2, d["imp"], 0.4, color=C_GREY, label="options-implied move (|%|)")
    ax.bar(x + 0.2, d["act"].abs(), 0.4, color=[color if a > 0 else C_NEG for a in d["act"]],
           label="actual next-day move (|%|; red = down)")
    for i, (a, b) in enumerate(zip(d["imp"], d["act"])):
        ax.text(i + 0.2, abs(b) + 0.2, f"{b:+.1f}%", ha="center", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(d[label_col], rotation=0, fontsize=8)
    ax.set_ylabel("% move"); ax.set_title(title); ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2)
    fig.tight_layout(); fig.savefig(FIG / fname); plt.close(fig)
    print(f"[ok] {fname}")


def load_table(name: str) -> pd.DataFrame | None:
    """Clean numeric tables written by scripts/analyze_curated.py (first-number parsing of the curated cells)."""
    p = ROOT / "report" / name
    if not p.exists():
        print(f"[skip] {name} not found (run scripts/analyze_curated.py first)"); return None
    df = pd.read_csv(p)
    return df.rename(columns={"implied_%": "options_implied_move_pct", "actual_%": "one_day_move_pct",
                              "rev_beat_%": "revenue_beat_pct", "guide_vs_cons_%": "guidance_vs_consensus_pct"})


def fig_implied_vs_actual():
    n = load_table("nvda_earnings_table.csv")
    if n is not None:
        n["label"] = n["quarter"].str.replace("FY20", "FY") + "\n" + n["report"].str[:7]
        _implied_vs_actual(n, "label", C_NVDA, "NVDA: options-implied vs actual next-day earnings move (8 reports)", "02_nvda_implied_vs_actual.png")
    c = load_table("crwv_earnings_table.csv")
    if c is not None:
        c["label"] = c["quarter"] + "\n" + c["report"].str[:7]
        _implied_vs_actual(c, "label", C_CRWV, "CRWV: options-implied vs actual next-day earnings move (6 reports)", "03_crwv_implied_vs_actual.png")


def fig_beat_vs_reaction():
    rows = []
    for name, lab, col in [("nvda_earnings_table.csv", "NVDA", C_NVDA), ("crwv_earnings_table.csv", "CRWV", C_CRWV)]:
        df = load_table(name)
        if df is None:
            continue
        beat = df["revenue_beat_pct"]
        guide = df["guidance_vs_consensus_pct"] if "guidance_vs_consensus_pct" in df else pd.Series(np.nan, index=df.index)
        react = df["one_day_move_pct"]
        for b, g, r, q in zip(beat, guide, react, df["report"].str[:7]):
            rows.append((lab, col, b, g, r, q))
    d = pd.DataFrame(rows, columns=["tk", "color", "beat", "guide", "react", "q"]).dropna(subset=["beat", "react"])
    if d.empty:
        print("[skip] 04_beat_vs_reaction"); return
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    for ax, xcol, xl in [(axes[0], "beat", "revenue beat vs consensus (%)"), (axes[1], "guide", "next-quarter guidance vs consensus (%)")]:
        dd = d.dropna(subset=[xcol])
        for tk, g in dd.groupby("tk"):
            ax.scatter(g[xcol], g["react"], color=g["color"].iloc[0], s=45, label=tk)
            for _, r in g.iterrows():
                ax.annotate(str(r["q"]), (r[xcol], r["react"]), fontsize=7, xytext=(3, 3), textcoords="offset points")
        ax.axhline(0, color=C_GREY, lw=0.8); ax.axvline(0, color=C_GREY, lw=0.8)
        ax.set_xlabel(xl); ax.set_ylabel("next-day stock move (%)"); ax.legend(frameon=False)
    fig.suptitle("Beating the number is not the same as beating the market: reaction vs. surprise")
    fig.tight_layout(); fig.savefig(FIG / "04_beat_vs_reaction.png"); plt.close(fig)
    print("[ok] 04_beat_vs_reaction.png")


def fig_hn_attention():
    hn = load("hn_stories.csv")
    if hn is None:
        return
    hn["date"] = pd.to_datetime(hn["date"], errors="coerce")
    hn = hn.dropna(subset=["date"])
    hn["month"] = hn["date"].dt.to_period("M").dt.to_timestamp()
    counts = hn.groupby(["month", "company"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(9, 4.2))
    bottom = np.zeros(len(counts))
    colors = {"CRWV": C_CRWV, "NVDA": C_NVDA, "AI-infra": C_GREY}
    for col in counts.columns:
        ax.bar(counts.index, counts[col], width=25, bottom=bottom, color=colors.get(col, C_ACCENT), label=col)
        bottom += counts[col].values
    ax.set_title("Hacker News front-page stories found per month (curated sample, not a census)")
    ax.set_ylabel("stories"); ax.legend(frameon=False)
    c = crwv_points()
    if c is not None:
        ax2 = ax.twinx(); ax2.grid(False)
        ax2.plot(c["month_end"], c["close"], color=C_CRWV, lw=1.5, ls="--", label="CRWV close")
        ax2.set_ylabel("CRWV close ($)")
    fig.tight_layout(); fig.savefig(FIG / "05_hn_attention.png"); plt.close(fig)
    print("[ok] 05_hn_attention.png")


def fig_capex():
    cap = load("hyperscaler_capex_guidance.csv")
    if cap is None:
        return
    cap["date"] = pd.to_datetime(cap["date"], errors="coerce"); cap["val"] = num(cap["midpoint_busd"])
    cap = cap.dropna(subset=["date", "val"]).sort_values("date")
    fig, ax = plt.subplots(figsize=(9, 4.2))
    cols = {"MSFT": C_ACCENT, "GOOGL": C_NVDA, "AMZN": "#B8860B", "META": "#7B2CBF"}
    for co, g in cap.groupby("company"):
        ax.step(g["date"], g["val"], where="post", color=cols.get(co, C_GREY), lw=1.8, label=co)
        ax.scatter(g["date"], g["val"], color=cols.get(co, C_GREY), s=22, zorder=3)
    for d, lab in [("2025-01-27", "DeepSeek"), ("2025-04-15", "H20 ban"), ("2025-11-10", "CRWV guide cut"), ("2026-10-28", "MSFT trims")]:
        ax.axvline(pd.Timestamp(d), color=C_GREY, lw=0.7, ls="--"); ax.text(pd.Timestamp(d), ax.get_ylim()[1] * 0.98 if ax.get_ylim()[1] > 0 else 200, lab, fontsize=7, rotation=90, va="top", color=C_GREY)
    ax.set_title("Hyperscaler full-year capex guidance (midpoint, $B) as announced; 2025 guides left, 2026 guides right")
    ax.set_ylabel("$B"); ax.legend(frameon=False, ncol=4)
    fig.tight_layout(); fig.savefig(FIG / "06_capex_signals.png"); plt.close(fig)
    print("[ok] 06_capex_signals.png")


def fig_crwv_events():
    ev = load("crwv_events.csv")
    c = crwv_points()
    if ev is None or c is None:
        return
    ev["date"] = pd.to_datetime(ev["date"].astype(str).str[:10], errors="coerce"); ev["mv"] = num(ev["stock_move_pct"])
    ev = ev.dropna(subset=["date"])
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(c["month_end"], c["close"], color=C_CRWV, lw=2)
    cats = ev["category"].astype(str).str.lower()
    palette = {"ipo": C_ACCENT, "contract": C_NVDA, "debt": "#B8860B", "lockup": C_NEG, "mna": "#7B2CBF",
               "analyst": C_GREY, "guidance": C_NEG, "insider": "#555555", "other": C_GREY}
    import matplotlib.dates as mdates
    xs = mdates.date2num(c["month_end"].dt.to_pydatetime())
    for (_, r), cat in zip(ev.iterrows(), cats):
        y = float(np.interp(mdates.date2num(r["date"].to_pydatetime()), xs, c["close"].to_numpy(dtype=float)))
        ax.scatter(r["date"], y, color=palette.get(cat, C_GREY), s=34, zorder=3, edgecolor="white", linewidth=0.6)
    for cat, col in palette.items():
        if (cats == cat).any():
            ax.scatter([], [], color=col, label=cat)
    ax.legend(frameon=False, ncol=4, fontsize=8); ax.set_ylabel("CRWV close ($)")
    ax.set_title("CRWV corporate events on the price path (dated points; derived points interpolated)")
    fig.tight_layout(); fig.savefig(FIG / "07_crwv_events.png"); plt.close(fig)
    print("[ok] 07_crwv_events.png")


if __name__ == "__main__":
    for f in (fig_price_paths, fig_implied_vs_actual, fig_beat_vs_reaction, fig_hn_attention, fig_capex, fig_crwv_events):
        try:
            f()
        except Exception as e:
            print(f"[error] {f.__name__}: {type(e).__name__}: {e}")
