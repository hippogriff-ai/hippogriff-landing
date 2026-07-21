# AEO for hippogriff.io: verified research + playbook (July 2026)

Deep-research run 2026-07-20: 106 agents, 24 sources fetched, 115 claims extracted, top 25 adversarially verified with 3-vote panels (22 confirmed, 3 refuted). This doc records what survived verification and what it means for this site.

## TL;DR

1. Crawler policy is the only hard gate: allow OAI-SearchBot, Claude-User, and Claude-SearchBot or you cannot be cited by ChatGPT search or Claude. GPTBot and ClaudeBot are independent training-only levers.
2. Pre-rendered HTML is non-negotiable: OpenAI, Anthropic, and Perplexity crawlers do not execute JavaScript. Our `output: 'export'` already satisfies this.
3. The only empirically validated content lever is evidence density: citations, quotations, and quantitative statistics in visible prose (30-40% relative visibility gains in the KDD 2024 GEO paper; +22-37% validated live on Perplexity).
4. Two hyped tactics are refuted as AEO levers: llms.txt (97% of ~38K valid files got zero requests in Ahrefs' 137K-domain log study; no major provider supports it) and JSON-LD schema (no citation uplift in a matched diff-in-diff experiment; retrieval reads only visible HTML).

## Verified findings

### Crawler / robots.txt policy (primary vendor docs, fetched live 2026-07-20)

- OpenAI splits search from training. OAI-SearchBot indexes for ChatGPT search; GPTBot collects training data; controls are explicitly independent. Sites disallowing OAI-SearchBot are excluded from ChatGPT search answers. (3-0; developers.openai.com/api/docs/bots)
- ChatGPT-User performs user-triggered fetches and "robots.txt rules may not apply" per OpenAI's own docs. Only server/firewall rules can block it. (3-0)
- Anthropic runs three separately controllable crawlers: ClaudeBot (training only), Claude-User (user-triggered retrieval; blocking prevents Claude citing you), Claude-SearchBot (Claude search index). Claude search is also powered by Brave Search, so Brave-index visibility is a parallel path. (3-0; support.claude.com article 8896518)
- Current policy for this site: `User-agent: * / Allow: /`. Everything is allowed, including training bots. This is the max-presence posture. Blocking GPTBot/ClaudeBot would preserve citations while opting out of training, but being in training data is itself presence for a personal brand. Decision owner: Vicki.

### llms.txt (null result)

- Ahrefs 137,210-domain server-log study (May 2026): 97% of ~38K valid llms.txt files received zero requests from anything. AI retrieval bots were 1.1% of the few requests. AI bots never probe for the file (0% of 404s). (3-0)
- Independent 48-day CDN log study (wislr.com): 12,099 AI-bot requests, zero llms.txt fetches. (3-0)
- No provider adoption: Google's May 2026 ai-optimization guide explicitly mythbusts it; Mueller called it "a temporary crutch"; OpenAI/Anthropic/Google/Meta all unadopted. (3-0)
- The only measurable audience is coding agents (Claude-Code was the #2 fetcher after GPTBot in Ahrefs' data). For a developer-audience site this makes llms.txt a low-cost nicety, not an AEO lever. Keep it cheap and current; expect nothing from it. (3-0)

### JavaScript rendering (2-1, scope-corrected)

- OpenAI, Anthropic, and Perplexity crawlers do not render JS (Vercel/MERJ study, ~1.3B crawler fetches). Google AI Overviews/Gemini and Applebot DO render; Bingbot partially. Static export covers all cases.
- AI bot hits never fire client-side analytics. Amplitude/GA cannot see crawler traffic; only server/CDN logs can. Human click-throughs from chatgpt.com / perplexity.ai referrers ARE visible client-side.

### Content tactics (GEO paper, KDD 2024, peer-reviewed)

- Top validated optimizations: quotation addition (+22% on live Perplexity), statistics addition (up to +37%), citing sources. Fluency/keyword-stuffing style edits did nothing. (3-0)
- Gains skew to lower-authority sites (rank-5 sources gained +97-115% from these edits) but only conditional on being retrieved at all. The retrieval gate still favors classic ranking: ~75% of AI Overview links come from top-12 organic results; Claude citations largely mirror Brave's top listings. (2-1: conditionality matters)
- Refuted: "classic SEO doesn't transfer to AEO" was killed 0-3. Traditional SEO remains the prerequisite for clearing the retrieval gate.

### Structured data (null result for citations, keep for classic SEO)

- Ahrefs matched diff-in-diff (1,885 treated pages vs 4,000 controls): adding JSON-LD produced no significant citation change on Google AI Mode (+2.4%) or ChatGPT (+2.2%), small significant decline (-4.6%) on AI Overviews. The 3x schema-citation correlation is confounding. (3-0)
- searchVIU mechanism test: ChatGPT, Claude, Perplexity, Gemini, AI Mode all extract only visible HTML at retrieval time; schema-only content was read by 0 of 5 systems. (3-0)
- Implication: keep minimal BlogPosting/Person/WebSite schema for Google rich results and classic ranking (which gates AI Overviews). Never put a load-bearing fact only in schema.

## Implemented 2026-07-20

- `src/app/sitemap.ts`: generates /sitemap.xml at build (was a live 404 referenced by robots.txt).
- `src/app/feed.xml/route.ts`: RSS 2.0 with full post content (content:encoded).
- Canonical host aligned to https://www.hippogriff.io (apex 307s to www) via `src/lib/site.ts`; canonicals on all page types; RSS alternate link on all pages (Next replaces, not merges, page-level `alternates`).
- JSON-LD: BlogPosting per post, WebSite + Person on home.
- `public/llms.txt`: all 5 post URLs with descriptions plus feed URL.
- Post metadata: authors, OG url, publishedTime.

## Editorial playbook (per post, the highest-leverage work)

1. Answer-first opening: the first paragraph should be quotable standalone (posts mostly do this already).
2. Add quantitative statistics in visible prose. Concrete numbers from your own builds are unique data nobody else has ("~320 lines of Python", "500 of 13K applicants" are the pattern; more of this).
3. Quote primary sources directly, with attribution, in the text.
4. Cite sources inline as links with descriptive anchors.
5. Question-shaped H2s where natural (chunk-level retrieval favors self-contained sections).
6. Distribution clears the retrieval gate: share posts to HN/Reddit/X, link them from GitHub repo READMEs (concept-demos, remo). Backlinks and Brave/Google ranking remain the entry ticket.

## Measurement

- Client-side (Amplitude): human referrals from chatgpt.com, claude.ai, perplexity.ai, copilot.microsoft.com, gemini.google.com are visible via referrer. Worth adding a referrer-based segment.
- Crawler activity: invisible client-side. On Vercel: Observability > Bot traffic, or a log drain. Spot-check with `site:` and direct questions in ChatGPT/Claude/Perplexity monthly.

## Open questions from the research (unverified areas)

- PerplexityBot/Google-Extended/Bingbot robots.txt specifics were not confirmed by the verification panel.
- Whether sitemap/RSS actively drive AI-crawler discovery is unproven (the one log-based claim was refuted 1-2). They remain cheap and standard.
- Off-site authority weighting (Reddit/HN/GitHub vs on-page tactics) lacks verified quantification.

## Key sources

- https://developers.openai.com/api/docs/bots (primary)
- https://support.claude.com/en/articles/8896518 (primary)
- https://ahrefs.com/blog/llmstxt-study/ (primary log data)
- https://arxiv.org/abs/2311.09735 (GEO paper, KDD 2024)
- https://ahrefs.com/blog/schema-ai-citations/ (diff-in-diff)
- https://www.searchviu.com/en/schema-markup-and-ai-in-2025-what-chatgpt-claude-perplexity-gemini-really-see/
- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- https://vercel.com/blog/the-rise-of-the-ai-crawler
- Full verified report: deep-research run wf_1ec0a2cb-ff3 (session 95ce9597, 2026-07-20)
