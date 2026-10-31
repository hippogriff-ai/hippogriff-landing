# finance-research

Fundamental + quantitative research on public equities and their options markets.
Each study is self-contained under `studies/<name>/` with its own curated data,
reproducible pipeline, figures, and written report.

| Study | Question | Status |
|---|---|---|
| [`crwv-nvda-options`](studies/crwv-nvda-options/) | How did CoreWeave (CRWV) and NVIDIA (NVDA) options behave around earnings, catalysts, and attention shocks over Nov 2024 – Oct 2026, and which signals lead price? | Report v1 |

## Why this lives in a subdirectory

This folder was created in a Claude Code cloud session whose GitHub integration
is scoped to a single repository and cannot create new ones. It is laid out as a
standalone repository so you can split it out in one step:

```bash
# from the hippogriff-landing checkout
git subtree split --prefix=finance-research -b finance-research-main
# create an empty repo on GitHub (e.g. <you>/finance-research), then:
git push git@github.com:<you>/finance-research.git finance-research-main:main
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Each study documents its own commands in its README.

## Conventions

- `data/curated/` – hand-compiled, source-cited CSVs (committed). Every number has a URL.
- `data/raw/` – machine-downloaded time series (git-ignored, regenerate with the pipeline).
- `src/` – importable Python package with tested analytics; `scripts/` – thin CLIs.
- `report/` – the written findings and generated figures.
- Nothing in a report is invented. Values that could not be sourced are marked `NA`.
