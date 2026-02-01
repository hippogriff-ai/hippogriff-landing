# Hippogriff Landing

Source for [hippogriff.io](https://hippogriff.io) — a personal maker portfolio showcasing projects and writing.

## Stack

- **Next.js 15** with App Router, static export (`output: 'export'`)
- **TypeScript**
- **Markdown blog** via gray-matter + remark

## Structure

```
src/
├── app/
│   ├── layout.tsx          # Root layout (Inter font, metadata)
│   ├── page.tsx            # Homepage
│   ├── globals.css         # All styles
│   └── blog/
│       ├── page.tsx        # /blog listing
│       └── [slug]/page.tsx # /blog/[slug] post
├── components/
│   ├── Navbar.tsx
│   ├── Header.tsx          # Title, subtitle, social icons
│   ├── ProjectCard.tsx
│   ├── InvaderCanvas.tsx   # Client component — canvas animation
│   ├── BlogCard.tsx
│   ├── BlogPreview.tsx
│   └── Footer.tsx
└── lib/
    └── blog.ts             # Markdown file reading + rendering
content/blog/               # Markdown posts (frontmatter: title, date, excerpt, pinned)
prototypes/                  # Design playground HTML
```

## Development

```bash
npm install
npm run dev       # http://localhost:3000
```

## Build & Deploy

```bash
npm run build     # Generates static site in out/
npx serve out     # Preview locally
```

Deployed on Vercel via static export.

## Design

- 3-color palette: `#111111` (bg), `#e8a830` (accent), `#c8c0b0` (text)
- Single client component (InvaderCanvas) — everything else is zero-JS server HTML
- Responsive at 768px and 480px breakpoints
