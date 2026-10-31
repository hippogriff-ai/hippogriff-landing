# NVDA / CRWV price path and options-market synthesis (Nov 2024 - Oct 31 2026)

Compiled 2026-10-31 from 34 web searches (WebFetch unavailable; the shared web-search budget was exhausted before every planned query could be run, so several items are marked NA rather than inferred). Every number below carries a URL in the companion CSVs. Nothing is fabricated; where sources disagree, both figures are given.

## 1. Price path in brief

- Oct 2024 -> Oct 2026: NVDA went from ~$133-138 (Nov/Dec 2024 closes 138.03 / 134.29) to $204.64 on 2026-10-30, with an all-time closing high of $238.90 (Macrotrends adjusted 239.24) on 2026-10-06 and an intraday high of $243.37 the same day.
- Market-cap milestones: $4T touched intraday 2025-07-09 (shares 163.93), first close above $4T 2025-07-10; ~$4.5T on the 2025-09-22 OpenAI record close (183.61); first $5T 2025-10-29 (record close 207.04); back above $5T at a record close 2026-04-24; "approaching $6T" per Bloomberg 2026-10-02 (~$5.7T at the Oct 6 record). $3T was first crossed in June 2024, before this window.
- Major drawdowns (close basis unless noted):
  1. Jan 2025 high -> Apr 2025 low: roughly -37/-38% ("almost 38% drawdown from the high on April 4", Webull/Fool; April 2025 monthly low 86.62 per StockScan; Apr 8 close 96.30). Driven by DeepSeek (-16.9% on 2025-01-27), Liberation Day tariffs (Apr 3-4; -7.8% on Apr 4), H20 license requirement (-6% AH Apr 15, ~-7% Apr 16).
  2. Oct 29 2025 record (207.04) -> late Mar 2026 (weekly close 167.52): about -19% ("down 18% in 2026", TIKR), via the Nov 2025 AI-bubble week (Nov 20 close ~-3.2% after +5% intraday; Nov 28 close 176.77 = -14.6% from record), a Feb 5 2026 intraday YTD low near $172, and the Feb 26 2026 post-earnings -5.5%.
  3. May 14 2026 record (235.74) -> Jul 31 2026 (200.53): about -15%.
  4. Oct 6 2026 record (238.90) -> Oct 30 2026 (204.64): -14.3%, culminating in the -4.22% AI-selloff day (Intel -25%, "circular financing" fears, DOJ questions on Nvidia's $12.93B Hugging Face bid).
- Largest single-day gain: +18.7% on 2025-04-09 (tariff pause). Largest loss: -16.9% on 2025-01-27.
- CRWV: IPO at $40 on 2025-03-28. Deal/credit-driven path: Core Scientific all-stock bid 2025-07-07 (stock slumped), lockup expiry (Aug 2025 per Sherwood/Invezz; MarketBeat says Sep 24 - unresolved), Core Scientific vote failure 2025-10-30 (-3.5%), and an October 2026 collapse (-37.75% from Sep 30 close 87.12 to 54.24 on Oct 23; 5y CDS from 452bp on Jun 3 2026 to 1,146bp; close 54.60 on Oct 30 after ~-10%, Quantcha tags -11.8%).

## 2. What the options market got right and wrong on NVDA earnings

Implied vs realized (close-to-close), eight prints:

| Report | Implied (range across sources) | Realized | Verdict |
|---|---|---|---|
| 2024-11-20 | 7.9-8% | ~0.5% | far inside |
| 2025-02-26 | 9.2% | -8.5% | inside, barely |
| 2025-05-28 | 6.5-6.8% | +3.2% (peak +6.4%) | inside |
| 2025-08-27 | 5.4-6.6% | -0.8% | inside |
| 2025-11-19 | 7.0-7.7% | -3.2% (peak +5.1%) | inside |
| 2026-02-25 | 5.5-6.4% | -5.5% | inside, barely |
| 2026-05-20 | 5.5-8.1% | -1.8% | inside |
| 2026-08-26 | 5.4-6.4% (lowest in 2 yrs) | +8.7% | EXCEEDED |

Takeaways:
- Implied moves systematically overshot realized through 2025: ORATS noted at one point that NVDA had moved less than implied for eight consecutive reports; Optionomics' 7-quarter window shows avg implied 6.97% vs avg actual 4.15%. Over longer windows the gap is small (ORATS 12q avg implied 7.7% vs actual 7.6%; EW: exceeded in 5 of 17 = 29%, or 4 of 16 = 25% depending on peak vs close measurement).
- The market "learned": implied moves compressed from 9.2% (Feb 2025) to 5.4% (Aug 2026, "lowest volatility expectation in two years"). The compression was then punished by the +8.7% Aug 2026 move - the only exceedance of the window - a classic case of vol sellers crowding into a trade after it had worked repeatedly. SpotGamma had flagged "the options market may be underpricing this move" before Feb 2026 as well.
- Dollar framing: Bloomberg/Reuters framed each print as the largest-ever dollar swing ($300B Nov 2024, $280B Aug 2025 and Aug 2026, $320B Nov 2025), even as percentage implied moves fell - market cap growth, not vol, drove the headlines.
- Direction: 6 of 8 realized reactions were negative despite beats (e.g., May 2026 revenue $81.62B vs $78.86B est, stock -1.8%), consistent with heavy pre-print call positioning (calls ~2x puts, May 2026) and post-print IV crush/delta unwind.

## 3. Structural features

- Scale: 2025 US listed options volume hit a record 15.21B contracts (+24.4%); single-stock options were 54% (8.27B). An aggregator citing Cboe says NVDA and TSLA each accounted for ~9% of single-stock volume in Q2 2026 (not verified against Cboe). NVDA traded 2.22M contracts on 2026-10-26 (30-day avg 2.80M), put/call 0.58. Single strikes can dominate: one Sep-26-25 182.5 call printed 75,996 contracts = 9.3% of the day's NVDA volume.
- Retail call demand / skew: SpotGamma pre-earnings note showed call skew at the 81st percentile vs put skew at the 16th, with dealers short gamma above $220 (source dates this to "May" - strike level implies May 2026). Market Chameleon's Oct 2026 put/call of ~0.57-0.58 confirms persistent call tilt even in a drawdown.
- Vol premium: Barchart's late-Oct 2026 snapshot shows IV 41.6% vs HV 41.1% - near parity after the -4.2% day; IV30 was 45.1% (81st percentile rank) at the 2026-10-30 close per Market Chameleon. Historical IV30 series around each earnings were NOT found (gap).
- Leveraged ETFs: NVDL AUM peaked at $6.7B (Nov 2024), fell to $4.4B by mid-2025 with $2.2B of outflows, and stood at $3.8B on 2026-10-30. No source quantifying its rebalancing impact on close-of-day flows was found.
- Gamma mechanics: vendor commentary (SpotGamma, Magnelibra, LetsDataScience) frames pre-earnings call-heavy positioning as raising dealer long-delta exposure that "mechanically amplifies" moves and unwinds on IV crush; treated here as heuristic, not validated.
- Macro vol: VIX closed 52.33 on 2025-04-08 (highest outside 2008-09 and 2020; one source labels it intraday), hit 57.96 intraday on 2025-04-09, rose >15 points close-to-close on 2025-04-04, and slipped to 14.95 in late 2025. VIX on the DeepSeek day and VXN at any catalyst were not found.

## 4. CRWV specifics

- Options: listing date and weeklies-add date NOT found. By Oct 2026 ~20 expirations were listed. IV30 100.3% on 2026-10-16 (52-week range 65.9%-122.7%; HV20 79.6%); ATM IV 96.4% with IV rank 53 (Opti-View); 102.3% with 1y IV rank 63 (Unusual Whales, Oct 30); nearest ATM 106.2% on Oct 22. 90-day realized vol 99.8%. This confirms the "90-120%+" regime; no source showed 150%.
- Earnings: unlike NVDA, CRWV repeatedly exceeded implied: 1-day moves -20.8% (Aug 2025), -16.3% (Nov 2025, implied ~12.5%), -18.5% (Feb 2026), -11.4% (May 2026), +19.3% vs ±13.7% implied (Aug 2026; TipRanks preview cited 15.5%). Earnings-Watcher: actual > implied in 83% of the last six reports, avg move ±17.9%. Next report Nov 9/10 2026, implied ±9.84% (avg implied ±12.25%).
- Flow episodes: options volume >7x the 30-day average with heavy put buying during the 2026-10-14 neocloud selloff (CNBC); call volume ~2x puts during a 2026 rally toward ~$107 with IV falling into the rally (Investing.com). June 2025 parabolic-rally options data NOT found.
- Leveraged products: CRWU (REX/Tuttle T-REX 2X Long, launched 2025-07-25 on Cboe), CWVX (Tradr, July 2025, "first-to-market"), CRWG (Leverage Shares), CRWX (Corgi), CORD (2x inverse), CWY (GraniteShares YieldBoost, ~$1.0M AUM). "CRWL" was not found.
- Short interest: 69.8M shares / 1.7 days to cover (AltIndex); 15.2% of shares outstanding; 19.98% of float (Finviz); 11.01% of float (MarketBeat). Borrow fee NA. Beta/correlation to NVDA NA.
- Credit as the vol driver: 5y CDS roughly 2.5x (452 -> 1,146bp) between June and late Oct 2026 while the stock fell 38% in October; equity vol in CRWV is increasingly a financing story (a "$20B funding gap" per TradingKey) rather than an NVDA-beta story.

## 5. Open questions / gaps (search budget exhausted)

1. NVDA IV30 levels immediately before/after each of the eight earnings reports; IV percentile/rank at those dates.
2. VIX closes on 2025-01-27, 2025-04-04, 2025-04-09, each NVDA earnings date; any VXN readings.
3. NVDA put/call ratios at the DeepSeek day, April 2025 lows, Nov 2025 week; record single-day NVDA call-volume figures; 0DTE/weekly share of NVDA volume.
4. Goldman / JPMorgan / Nomura derivatives-strategist notes on NVDA positioning (none surfaced; only ORATS/SpotGamma/LPL/Saxo/Direxion/TipRanks/EW estimates found).
5. Exact NVDA move on 2025-04-03 and the Aug 2025 H20 15% revenue-share day; Oct 31 2024 close.
6. CRWV options listing/weeklies dates, June 2025 rally options volume, lockup date (Aug vs Sep 24 2025), borrow fee, beta to NVDA.
7. The statmuse monthly closes appear dividend-adjusted (~$0.15 below raw); cross-check against Nasdaq/Yahoo raw closes if exactness matters.

## 6. Source list

Price/market cap: statmuse.com (multiple NVDA pages), stockanalysis.com/stocks/nvda/history/, macrotrends.net NVDA stock-price-history, macroaxis.com, digrin.com, stockscan.io, finance.yahoo.com/quote/NVDA/, investing.com NVDA historical data, bitget.com wiki, CNBC (2025-01-27 x3, 2025-11-21, 2026-03-16, 2026-04-24, 2026-10-30), Bloomberg (2025-01-27, 2025-10-29, 2026-10-02), Fortune 2025-10-29, Quartz, Yahoo Finance $4T, Fool.com (2025-04-03, 04-13, 04-16, 2026-10-02, 2026-10-30), Globe and Mail/Motley Fool April 9 2025, HL.co.uk, finviz StockStory, SiliconAngle, TIKR, EBC, MarketBeat 2026-10-30, Invezz, GuruFocus, Yahoo Finance GTC Mar 16 2026, AcadeResearch, Nasdaq.com Jan 13 2026, Investing.com H200 May 2026, Benzinga July 2026, Plus500, Axios/ABC/CNN/Forbes/Fortune Nov 2025.
Options/vol: orats.com (3 posts), earnings-watcher.com (3 pages), convexvalue.com/earnings/NVDA, optionomics.ai, optionslam.com, spotgamma.com, tipranks.com (TheFly/implied-move pages), finance.yahoo.com Reuters reprints ($280B, $320B), investing.com (May 2026, Aug 2026), home.saxo (Nov 2024, May 2026), cnbc.com 2026-05-20, direxion.com, cryptobriefing.com, kiplinger.com, intellectia.ai, bloomberg.com 2024-11-20, marketchameleon.com (NVDA OptionSummary, CRWV IV, CRWV OptionChain, CRWV Earnings), barchart.com (NVDA options-data, put-call-ratios, CRWV expected-move), opti-view.com, unusualwhales.com, volradar.com, interactivebrokers.com Traders' Insight (two pieces), blog.magnelibra.com, letsdatascience.com, strike-watch.com, joincfu.com (OCC/Cboe stats), macroption.com VIX all-time highs, convextrade.com VIX 2025, Audible VIX summaries.
ETFs/short interest: finance.yahoo.com NVDL articles and quote, barchart.com NVDL, rexshares.com CRWU, etfgi.com Tradr launch, leveragedposition.com, stockanalysis.com/etf/crwu and crwg, altindex.com, finviz.com CRWV, marketbeat.com CRWV.
CRWV corporate: coreweave.com IPO pricing release, forgeglobal.com, upmarket.co, sherwood.news (two), invezz.com, datacenterdynamics.com, investors.coreweave.com, tools.optionsai.com/companies/CRWV/earnings, cnbc.com 2026-10-14, 247wallst.com 2026-10-26, finance.yahoo.com CDS article, tradingkey.com, gurufocus.com, tokenpost.com, benzinga.com 2026-10-30, ideas.quantcha.com 2026-10-30.
