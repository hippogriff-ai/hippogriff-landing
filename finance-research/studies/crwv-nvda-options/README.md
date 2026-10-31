# CoreWeave (CRWV) and NVIDIA (NVDA): options behaviour vs. fundamentals, attention and macro, Nov 2024 – Oct 2026

**Deliverable:** [`report/REPORT.md`](report/REPORT.md) – the written analysis, with figures in `report/figures/`.

## Question

Across eight NVDA earnings reports and six CRWV reports, how did the options market
price each event, how did the stock actually move, and which upstream signals
(fundamentals, hyperscaler capex, OpenAI financing, Hacker News / retail attention,
credit, export policy) led or lagged those moves? What is tradeable over the next
six months (Nov 2026 – Apr 2027)?

## Layout

```
data/curated/        source-cited CSVs compiled by hand from public reporting (every value has a URL)
data/raw/            machine-downloaded time series (git-ignored; regenerate with scripts/run_pipeline.py)
src/optlab/          tested analytics: realized vs implied vol, event study, lead-lag, Granger, rolling beta
scripts/             run_pipeline.py (download), build_figures.py (charts from curated data)
tests/               pytest suite for the analytics (synthetic data, no network)
report/              REPORT.md and figures
```

## Reproduce

```bash
pip install -r ../../requirements.txt
python -m pytest -q tests                      # analytics self-test, offline
python scripts/build_figures.py                # charts from data/curated -> report/figures
python scripts/run_pipeline.py --start 2024-10-01   # needs network: Yahoo/Stooq, SEC, HN Algolia, Cboe
```

## Data provenance and honesty rules

- Daily prices, SEC XBRL facts, Hacker News items and option chains are fetched by
  `scripts/run_pipeline.py`. In the sandbox where this study was written those hosts
  were blocked, so the committed analysis rests on `data/curated/`, which was compiled
  from public articles, filings and data-provider pages found via web search. Each row
  carries its source URL; unknowns are `NA`, never interpolated.
- Options-implied moves are the pre-earnings straddle-implied moves reported by
  Bloomberg, Barchart, Reuters, Market Chameleon or ORATS at the time. They are not
  recomputed.
- Historical option chains are not freely available; `optlab.fetch.options_chain`
  snapshots today's Cboe chain so the dataset grows forward from here.
