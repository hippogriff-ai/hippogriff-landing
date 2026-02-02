# Continuity Ledger

## Goal (incl. success criteria):
Build hippogriff.io landing page — personal maker brand portfolio with flat card layout and contained animations. Success = Next.js static site builds, all pages render, animation works, blog system functional.

## Constraints/Assumptions:
- 3-color Pluribus-inspired palette (bg #111111, accent #e8a830, text #c8c0b0)
- NO scroll-driven animations — straightforward flat layout
- Projects visible immediately on front page with contained animations per card
- Next.js static export on Vercel
- Inter font, no heavy animation libraries
- Mobile density reduced for invader rain (2000ms spawn on <400px)
- Blog: markdown files in content/blog/ with frontmatter, pinned flag
- Only 1 client component (InvaderCanvas) — rest is zero-JS server HTML

## Key decisions:
- globals.css (not CSS Modules) — ~15 classes total, one file simpler
- remark + remark-html (not MDX) — posts are pure markdown
- Colors as CSS variables — palette is fixed
- InvaderCanvas speed: 15% faster than prototype → (0.15 + Math.random() * 0.25) * 1.15

## State:
  - Done:
    - Phases 1-8: Full site build (scaffold, layout, components, blog, verified)
    - Phase 9: About section on homepage (between blog and footer)
    - Phase 10: SEO metadata (layout OG/Twitter, blog listing metadata, blog post generateMetadata, robots.txt, llms.txt)
    - Phase 11: Amplitude analytics (@amplitude/analytics-browser, AmplitudeProvider, page_view/page_exit/link_click events, time-on-page tracking)
  - Now:
    - All phases complete. Build passes (6 static pages). Ready for user review.
  - Next:
    - User visual review / iteration
    - Set NEXT_PUBLIC_AMPLITUDE_API_KEY in Vercel env
    - Deploy to Vercel

## Open questions (UNCONFIRMED if needed):
- Footer github link URL (currently placeholder https://github.com/hippogriff-io)
- About section text is placeholder — Vicki to finalize

## Working set (files/ids/commands):
- src/app/page.tsx (homepage — now includes About section)
- src/app/layout.tsx (root layout — SEO metadata + AmplitudeProvider)
- src/app/globals.css (all styles — includes .about styles)
- src/app/blog/page.tsx (blog listing — page metadata)
- src/app/blog/[slug]/page.tsx (blog post — generateMetadata)
- src/components/{Navbar,Header,Footer,ProjectCard,InvaderCanvas,BlogCard,BlogPreview,AmplitudeProvider,BackButton}.tsx
- src/lib/blog.ts (markdown processing)
- src/lib/amplitude.ts (analytics helpers)
- content/blog/*.md (posts)
- public/robots.txt, public/llms.txt
- .env.example
- next.config.ts (output: 'export')
