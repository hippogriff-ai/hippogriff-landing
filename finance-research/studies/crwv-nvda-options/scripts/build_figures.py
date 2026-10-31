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


def fig_price_paths():
    n, c = load("nvda_monthly_close.csv"), load("crwv_monthly_close.csv")
    if n is None or c is None:
        return
    n["month_end"] = pd.to_datetime(n["month_end"]); c["month_end"] = pd.to_datetime(c["month_end"])
    n["close"], c["close"] = num(n["close"]), num(c["close"])
    n, c = n.dropna(subset=["close"]).sort_values("month_end"), c.dropna(subset=["close"]).sort_values("month_end")
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.plot(n["month_end"], n["close"], color=C_NVDA, lw=2, label="NVDA (left axis)")
    ax.set_ylabel("NVDA close ($)")
    ax2 = ax.twinx(); ax2.grid(False)
    ax2.plot(c["month_end"], c["close"], color=C_CRWV, lw=2, label="CRWV (right axis)")
    ax2.set_ylabel("CRWV close ($)")
    ev = load("catalysts.csv")
    if ev is not None:
        ev["date"] = pd.to_datetime(ev["date"], errors="coerce")
        for _, r in ev.dropna(subset=["date"]).iterrows():
            ax.axvline(r["date"], color=C_GREY, lw=0.6, alpha=0.5)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left", frameon=False)
    ax.set_title("Month-end closes; grey lines = catalysts in catalysts.csv")
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
    ax.set_ylabel("% move"); ax.set_title(title); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(FIG / fname); plt.close(fig)
    print(f"[ok] {fname}")


def fig_implied_vs_actual():
    n = load("nvda_earnings.csv")
    if n is not None:
        _implied_vs_actual(n, "fiscal_quarter", C_NVDA, "NVDA: options-implied vs actual earnings move", "02_nvda_implied_vs_actual.png")
    c = load("crwv_earnings.csv")
    if c is not None:
        _implied_vs_actual(c, "quarter", C_CRWV, "CRWV: options-implied vs actual earnings move", "03_crwv_implied_vs_actual.png")


def fig_beat_vs_reaction():
    rows = []
    for name, lab, col in [("nvda_earnings.csv", "NVDA", C_NVDA), ("crwv_earnings.csv", "CRWV", C_CRWV)]:
        df = load(name)
        if df is None:
            continue
        beat = num(df["revenue_beat_pct"]) if "revenue_beat_pct" in df else num(df.get("beat_pct", pd.Series(dtype=float)))
        guide = num(df["guidance_vs_consensus_pct"]) if "guidance_vs_consensus_pct" in df else pd.Series(np.nan, index=df.index)
        react = num(df["one_day_move_pct"])
        for b, g, r, q in zip(beat, guide, react, df.iloc[:, 1]):
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
    c = load("crwv_monthly_close.csv")
    if c is not None:
        c["month_end"] = pd.to_datetime(c["month_end"]); c["close"] = num(c["close"])
        ax2 = ax.twinx(); ax2.grid(False)
        ax2.plot(c["month_end"], c["close"], color=C_CRWV, lw=1.5, ls="--", label="CRWV close")
        ax2.set_ylabel("CRWV close ($)")
    fig.tight_layout(); fig.savefig(FIG / "05_hn_attention.png"); plt.close(fig)
    print("[ok] 05_hn_attention.png")


def fig_capex():
    m = load("macro_signals.csv")
    if m is None:
        return
    cap = m[m["category"].astype(str).str.lower() == "capex"].copy()
    cap["date"] = pd.to_datetime(cap["date"], errors="coerce")
    cap["val"] = num(cap["value"])
    cap = cap.dropna(subset=["date", "val"])
    if cap.empty:
        print("[skip] 06_capex: no numeric capex rows"); return
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.scatter(cap["date"], cap["val"], color=C_ACCENT, s=30)
    for _, r in cap.iterrows():
        ax.annotate(str(r["event"])[:40], (r["date"], r["val"]), fontsize=6, xytext=(3, 3), textcoords="offset points")
    ax.set_title("Hyperscaler capex guidance announcements ($B) — the demand signal upstream of NVDA and CRWV")
    ax.set_ylabel("$B")
    fig.tight_layout(); fig.savefig(FIG / "06_capex_signals.png"); plt.close(fig)
    print("[ok] 06_capex_signals.png")


def fig_crwv_events():
    ev = load("crwv_events.csv")
    c = load("crwv_monthly_close.csv")
    if ev is None or c is None:
        return
    ev["date"] = pd.to_datetime(ev["date"], errors="coerce"); ev["mv"] = num(ev["stock_move_pct"])
    ev = ev.dropna(subset=["date"])
    c["month_end"] = pd.to_datetime(c["month_end"]); c["close"] = num(c["close"])
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(c["month_end"], c["close"], color=C_CRWV, lw=2)
    cats = ev["category"].astype(str).str.lower()
    palette = {"ipo": C_ACCENT, "contract": C_NVDA, "debt": "#B8860B", "lockup": C_NEG, "mna": "#7B2CBF",
               "analyst": C_GREY, "guidance": C_NEG, "insider": "#555555", "other": C_GREY}
    ymax = c["close"].max()
    for (_, r), cat in zip(ev.iterrows(), cats):
        y = np.interp(r["date"].value, c["month_end"].astype("int64"), c["close"]) if len(c) else ymax
        ax.scatter(r["date"], y, color=palette.get(cat, C_GREY), s=28, zorder=3)
    for cat, col in palette.items():
        if (cats == cat).any():
            ax.scatter([], [], color=col, label=cat)
    ax.legend(frameon=False, ncol=4, fontsize=8); ax.set_ylabel("CRWV close ($)")
    ax.set_title("CRWV corporate events on the (monthly) price path")
    fig.tight_layout(); fig.savefig(FIG / "07_crwv_events.png"); plt.close(fig)
    print("[ok] 07_crwv_events.png")


if __name__ == "__main__":
    for f in (fig_price_paths, fig_implied_vs_actual, fig_beat_vs_reaction, fig_hn_attention, fig_capex, fig_crwv_events):
        try:
            f()
        except Exception as e:
            print(f"[error] {f.__name__}: {type(e).__name__}: {e}")
