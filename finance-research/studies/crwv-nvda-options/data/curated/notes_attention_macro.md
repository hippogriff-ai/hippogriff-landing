# Attention & Macro Notes: CoreWeave (CRWV) and NVIDIA (NVDA), Nov 2024 - Oct 2026

Compiled 2026-10-31. Companion files: `hn_stories.csv` (124 rows), `social_attention.csv` (15 rows),
`macro_signals.csv` (103 rows). All content below comes from 33 completed WebSearch calls (restricted to
news.ycombinator.com, which also surfaced SEC EDGAR filings). The shared web-search budget was exhausted
before the general-web macro queries ran, so **Task B is partially search-confirmed and partially flagged as
memory-unverified**; see "Gaps" at the end. Nothing in this document was fabricated: every row in the CSVs
carries either a retrieved URL or an explicit `NA` / `MEMORY-UNVERIFIED` / `gap` flag.

## 1. Method and caveats

* Hacker News search results expose titles and item IDs but **not timestamps, points or comment counts**.
  Dates in `hn_stories.csv` are interpolated from HN item IDs using anchors with known dates
  (42839650 = 2025-01-27 DeepSeek rout; 45813734 = 2025-11-03 Burry 13F; 47143110 ~ 2026-02-24 per
  "249 days ago"; 48167659 ~ 2026-05-17 per "167 days ago"; 50245821 ~ 2026-10-26 Reuters China piece).
  Expect +/- 3-5 days error; `date_precision` = `approx-id`. Points/comments are `NA` throughout.
* Article domains are given only when the search result or title made the outlet clear; otherwise `NA`.
* HN item IDs advanced ~10.6k/day in 2025 and ~12.7k/day in 2026, itself a rough proxy for site-wide
  submission growth (not AI-specific).

## 2. How Hacker News tone evolved (with examples)

**Phase 0 - Pre-window context (Oct-Nov 2024): "GPU glut" and GPU-collateralized debt.**
"$2 H100s: How the GPU Rental Bubble Burst" (41805446) set the frame that H100 hours had fallen from ~$8 to
~$2; FT's "$11B debt market for AI groups buying Nvidia chips" (42108336, Nov 2024) introduced CoreWeave to
HN mainly as a *leveraged* borrower (Blackstone, Carlyle, Magnetar). Tone: skeptical of unit economics.

**Phase 1 - DeepSeek efficiency shock (late Jan - Feb 2025): bearish, then rationalized.**
Six-plus threads in 48 hours around the $589B rout (42839650, 42848480, 42822162). Comment consensus
split between "compute is no longer the bottleneck" and Jevons paradox ("more efficient LLMs -> more usage ->
more chips"). The SemiAnalysis-based "DeepSeek has 50k GPUs, spent $1.6B" (42936185) was the bullish rebuttal.
Feb 24 "Microsoft cancels leases" (43157831) was the first *capex pullback* scare.

**Phase 2 - CoreWeave IPO (Mar 2025): skepticism dominates.**
~9 CRWV threads in March. S-1 discussion fixated on 77% revenue from two customers (43394418) and Nvidia's
~$320M MSA payments; "CoreWeave Is a Time Bomb" (Zitron, 43393452) and "founders pocketed $488M" (43270148)
got traction; the downsized $40 pricing with Nvidia's $250M anchor (43494082) and "Debut Dud" (43510363)
reinforced the view. HN was *more* negative than the stock, which went on to rally >300% by June (not
HN-sourced; see gaps).

**Phase 3 - Milestone mania vs. bubble talk (Jul - Oct 2025): bullish headlines, skeptical comments.**
Nvidia $4T (44509988), $4.5T (45429337), $5T (seven duplicate submissions on ~2025-10-29: 45746937,
45747638, 45750331, 45751424, 45754312, 45754481, 45755561). Simultaneously the bubble vocabulary hardened:
Altman "yes, a bubble" (44931264/44938004, Aug 15-16), MIT 95% (four threads, 44941118/44959952/44974104/
44994939), "AI Bubble 2027", "Say farewell to the AI bubble". The 15% China revenue-share (seven threads
Aug 10-11) was read as politicized export policy. Oracle-OpenAI $300B (45201595) immediately spawned
"OpenAI doesn't have the cash to pay Oracle $300B" (45272759).

**Phase 4 - "Circular financing" becomes the master narrative (Sept 2025 - Feb 2026).**
Trigger: Nvidia's $6.3B CoreWeave backstop (front page 2025-09-16; "textbook round tripping" debate at
45337341/45338026) and Nvidia-OpenAI $100B (45353963). Bloomberg's "web of circular deals" (45521629,
Oct 7) and AMD's $0.01 warrant (45490549) cemented it. Peak-skepticism cluster Nov 2025: Burry puts
(45813734), SoftBank exits NVDA (45884937), CoreWeave guidance cut (45888187), Oracle selloff with CRWV CDS
~600bp (45927435), Thiel exits (45948477), FT "Oracle underwater / minus $60B" (45964460, 45971601), "OpenAI
partners amass $100B debt pile" (46105814). Nvidia's Q3 FY26 beat (Nov 19; $57.0B, "cloud GPUs are sold
out") barely registered as a separate HN story. By Dec: "CoreWeave's staggering fall" (46284254), "Neocloud
bubble is a serious danger to the economy" (46418531), Groq $20B framed as an "antitrust loophole" (46403559).
Jan-Feb 2026: the $100B Nvidia-OpenAI deal stalls (46834835/46835479) and is replaced by $30B inside a $110B
round (47086980, 47181211); HN's satirical title "Nvidia invests $100bn in OpenAI, who buy $100bn of Nvidia
chips, who invest the..." (46927711) captures the mood. Huang's "pulling back from OpenAI and Anthropic"
(47256781, Mar 2026) was read as validation.

**Phase 5 - Credit and residual-value focus (Feb - Oct 2026).**
Attention shifted from equity valuation to *who holds the paper*: Blue Owl's CoreWeave DC debt snag
(47091457, 47104922), the Meta-backed $8.5B loan (47143110), "Nobody knows what a used GPU cluster is worth"
(48917135), "Inside the Circular Financing of the GPU Boom" (48873836), "Banks are now trying to offload the
AI data center debt they just underwrote" (50092664), and Reuters' "Market selloff, rising rates test AI data
centre deal boom" (50105900) where CoreWeave's 2032 bonds were reported near 15% yield and the stock fell
~15% in a day. Meanwhile, Nvidia milestone threads continued ($5.7T "Nvidia surpasses Germany", 48167659;
The Economist "Nvidia is the central bank of AI", 49673098) - i.e., HN increasingly treated NVDA as a
*financier of its own demand* rather than a pure chip vendor. Bubble essays persisted at a steady cadence
("How the AI Bubble Bursts", "The AI bubble is popping; we just don't know it yet", "Ask HN: What Makes AI a
Bubble?"), ending with Reuters' "In China, the AI bubble has burst" (STAR50 -40%, ~Oct 26 2026).

**Recurring themes (ranked by thread count in our sample):** circular financing (~14 threads), bubble
(~16), export controls/China (~14), market-cap milestones (~12), debt/credit stress (~14), DeepSeek
efficiency (~6), AI ROI skepticism/MIT (~6), hyperscaler capex (~5), GPU pricing/residual value (~4).

**Tone vs. the stocks (qualitative):** HN was bearish on CRWV at the IPO (stock subsequently tripled),
roughly coincident with the stock on the Nov 2025 guidance cut, and ahead of the market on credit risk
(CDS/bond-yield discussion began Nov 2025; distressed-yield headlines arrived Oct 2026). On NVDA, HN
skepticism peaked at each milestone ($4T, $5T) without a corresponding drawdown until the Nov 2025
Burry/SoftBank/Thiel cluster; HN's "DeepSeek moment" fears (Jan and Jul 2025) did not translate into
sustained NVDA weakness per the subsequent $4T/$5T milestones.

## 3. Which macro signals led price moves (search-confirmed links only)

1. **Export controls -> NVDA, directly and quickly.** Jan 13 2025 AI Diffusion IFR; Apr 15 2025 H20 license
   requirement ($4.5B charge); Aug 2025 15% revenue share (licenses granted but only ~$50M H20 revenue ever
   booked); Aug 22 2025 Beijing effectively freezes H20; by mid-2026 China shipments <1% of DC revenue
   (10-Q for qtr ended 2026-07-26). Net: China went from a swing factor to a rounding error; NVDA's
   milestones ($4T/$5T/$5.7T) occurred *despite* China, i.e., the market stopped pricing China upside.
2. **OpenAI deal flow -> CRWV.** Each OpenAI expansion ($11.9B Mar 2025, +$4B May 2025, +$6.5B Sept 2025)
   coincided with CRWV strength; each OpenAI-funding doubt (FT "doesn't have the cash", Nvidia $100B stall,
   "$100B debt pile") coincided with CRWV/ORCL weakness. CRWV is effectively a levered call on OpenAI's
   ability to finance $1.4T of commitments.
3. **Hyperscaler capex -> NVDA (the leading indicator).** Search-confirmed data points are thin (Meta $65B+
   cited Aug 2025; Nvidia Q2 FY27 release citing >$500B third-party capital platforms). Memory-flagged rows
   show the pattern: every 2025 guidance raise (Meta Jan/Apr/Jul/Oct; Alphabet Feb/Jul/Oct; Amazon Feb/Oct)
   preceded an NVDA leg up; the single downgrade scare (Microsoft lease cancellations, Feb 2025) coincided
   with the post-DeepSeek drawdown.
4. **Credit spreads -> CRWV, with a lag to equity.** CDS ~600bp (Nov 2025) preceded the Dec 2025 "staggering
   fall" headlines; Blue Owl snag (Feb 2026) preceded the Meta-backed refinancing; 15% bond yield (Oct 2026)
   coincided with a -15% day. Hyperscaler-leased DC debt (5.70-7.875%) vs CoreWeave-leased (7.00-9.875%)
   quantifies the counterparty discount.
5. **Rates.** Only indirectly confirmed: Reuters (Oct 2026) attributes the DC-deal stress to "rising rates".
   2025 Fed cuts (Sept/Oct/Dec) are memory-flagged.

## 4. Transmission chain: capex -> NVDA -> CRWV

```
Hyperscaler + OpenAI capex guidance  -->  NVDA bookings / DC revenue (+59% FY26; $57.0B Q3 FY26; $108B Q3 FY27 guide)
        |                                           |
        |  (Nvidia recycles cash: $100B->$30B OpenAI, $5B Intel, $20B Groq, $6.3B CRWV backstop, $1.3B rent-back)
        v                                           v
OpenAI/Meta/Microsoft sign take-or-pay contracts with neoclouds  -->  CRWV backlog (~$22.4B OpenAI, $14.2B Meta)
        |
        v
CRWV borrows against contracts/GPUs (Blackstone/Carlyle/Magnetar; Blue Owl SPVs; $8.5B Meta-backed loan)
        |
        v
Delivery depends on power / third-party DC shells (260 MW OpenAI cluster delayed -> Nov 2025 guide cut)
        |
        v
Credit market prices the chain: CDS ~600bp (Nov 2025) -> 2032 bonds ~15% (Oct 2026); banks offload DC debt
```
Two amplifiers: (a) Nvidia's backstops lower CRWV's cost of capital *and* create the circularity HN objects
to; (b) GPU residual value ("nobody knows what a used cluster is worth") governs the collateral haircut on
every link. The chain's weakest observed link in our data is power/DC readiness (CRWV Nov 2025) and OpenAI's
financing capacity (FT Nov 2025; Nvidia stall Jan 2026).

## 5. Gaps (search budget exhausted before these ran)

* Reddit r/wallstreetbets / r/stocks episodes (incl. CRWV top-ticker June 2025), Google Trends, Vanda /
  JPMorgan retail-flow notes, Polymarket/Kalshi NVDA-earnings markets: **no results; all NA.**
* Hyperscaler 2026 capex guidance (Jan/Apr/Jul/Oct 2026 earnings), Oracle 2026 capex/RPO: **not found.**
* Fed decisions and 10-yr yields in 2026; exact Nasdaq/SOX drawdown magnitudes per episode: **not found.**
* Nebius $17.4B, IREN $9.7B, Applied Digital leases, Oracle RPO $455B, China Sept-2025 ban, Trump-Xi,
  B30A, Microsoft-OpenAI restructuring, Broadcom 10 GW, Meta-Blue Owl Hyperion $27B, 2025 Fed cuts,
  Liberation Day, shutdown, 2025 capex figures: included **only as MEMORY-UNVERIFIED rows (source NA)**.
* 2026 GPU rental price index (H100/H200/B200): not found; one HN comment claims H100s "sold out at the same
  price as two years ago".
* HN points/comment counts: not exposed by search; all NA. Re-running with hn.algolia.com access would fill
  these in minutes.

## 6. Source list (retrieved URLs)

Hacker News items (prefix https://news.ycombinator.com/item?id=): 41805446, 42108336, 42682773, 42785891,
42786573, 42822162, 42839650, 42842056, 42848480, 42848752, 42849565, 42852039, 42936185, 43157831, 43189429,
43247552, 43250000, 43270148, 43393452, 43394418, 43421837, 43431054, 43494082, 43510363, 43699020, 43954890,
43974268, 43997087, 44068028, 44491983, 44505653, 44509988, 44517955, 44654416, 44678802, 44682545, 44742513,
44757247, 44858340, 44859584, 44859996, 44860131, 44866229, 44868442, 44871341, 44920680, 44931264, 44938004,
44941118, 44959952, 44964548, 44974104, 44979855, 44993339, 44994939, 45026833, 45040338, 45041693, 45170164,
45170647, 45201595, 45214257, 45272759, 45288161, 45288476, 45289145, 45293128, 45316088, 45337341, 45338026,
45353963, 45426205, 45429337, 45446560, 45490549, 45490879, 45491087, 45491206, 45510038, 45521629, 45522106,
45522176, 45546069, 45620292, 45732975, 45741836, 45746937, 45747638, 45750331, 45751424, 45754312, 45754481,
45755561, 45813734, 45814080, 45814154, 45814305, 45823738, 45884937, 45888187, 45927435, 45928279, 45930956,
45932125, 45948477, 45961150, 45964460, 45971601, 46105814, 46118072, 46153332, 46178163, 46188451, 46196076,
46197505, 46219853, 46226439, 46246031, 46255446, 46284254, 46379183, 46379609, 46380238, 46403041, 46403263,
46403559, 46408104, 46417067, 46418531, 46422321, 46834835, 46835479, 46927711, 47034849, 47086980, 47091457,
47104922, 47143110, 47181211, 47256781, 47425008, 47573420, 47656126, 47849095, 47928683, 48167659, 48368187,
48417490, 48873836, 48917135, 49154601, 49525497, 49673098, 49676849, 50051583, 50092664, 50105900, 50122112,
50245821; plus https://news.ycombinator.com/front?day=2025-09-16

SEC EDGAR (prefix https://www.sec.gov/Archives/edgar/data/):
1045810/000104581025000007/nvda-20250113.htm (AI Diffusion 8-K);
1045810/000104581025000116/nvda-20250427.htm (10-Q, H20 charge);
1045810/000104581025000115/q1fy26pr.htm; 1045810/000104581025000207/q2fy26pr.htm;
1045810/000104581025000228/q3fy26pr.htm; 1045810/000104581025000230/nvda-20251026.htm (10-Q, 15% share);
1045810/000104581026000021/nvda-20260125.htm (FY26 10-K); 0001045810/000104581026000038/a2026-annualxreportxwebxfi.pdf (ARS, Groq);
0001045810/000104581026000052/nvda-20260426.htm; 0001045810/000104581026000075/nvda-20260726.htm (10-Q, China <1%);
0001045810/000104581026000073/q2fy27pr.htm (Q2 FY27, $108B guide, $500B capital platforms);
1769628/000176962825000047/crwv-20250909.htm (CoreWeave-Nvidia $6.3B 8-K);
1769628/000095010325008492/dp231291_ex9901.htm (Core Scientific 8-K); 1769628/000176962825000041/crwv-20250630.htm (CRWV 10-Q);
2488/000000248826000021/amd-20251227.htm (AMD 10-K/A, OpenAI warrant); 0000002488/000000248826000076/amd-20260328.htm (AMD 10-Q);
50863/000005086325000155/a09152025form8-kex991.htm (Intel 8-K, Nvidia $5B).
