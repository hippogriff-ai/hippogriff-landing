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
    - Phase 1: Scaffolding (package.json, tsconfig, next.config.ts)
    - Phase 2: Root layout + globals.css (all styles, responsive breakpoints)
    - Phase 3: Static components (Navbar, Header, Footer, ProjectCard, page.tsx)
    - Phase 4: InvaderCanvas client component (MiniInvader class, retina, cleanup)
    - Phase 5: Blog lib (blog.ts) + 4 markdown posts
    - Phase 6: BlogCard, BlogPreview, homepage integration
    - Phase 7: Blog routes (/blog listing + /blog/[slug] with generateStaticParams)
    - Phase 8: Build verified — 9 static pages in out/
  - Now:
    - All phases complete. Build passes. Ready for user review.
  - Next:
    - User visual review / iteration
    - Deploy to Vercel

## Open questions (UNCONFIRMED if needed):
- Footer github link URL (currently placeholder https://github.com/hippogriff-io)

## Working set (files/ids/commands):
- src/app/page.tsx (homepage)
- src/app/layout.tsx (root layout)
- src/app/globals.css (all styles)
- src/app/blog/page.tsx (blog listing)
- src/app/blog/[slug]/page.tsx (blog post)
- src/components/{Navbar,Header,Footer,ProjectCard,InvaderCanvas,BlogCard,BlogPreview}.tsx
- src/lib/blog.ts (markdown processing)
- content/blog/*.md (4 posts)
- next.config.ts (output: 'export')
