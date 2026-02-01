# Hippogriff Landing Page — Design Decisions

## Brand

**Hippogriff** — a magical creature symbolizing love and loyalty (Harry Potter). The domain `hippogriff.io` is a personal maker brand showcasing projects built with care.

## Design Philosophy

- **The page is the portfolio.** The craft of the landing page itself proves the quality of the work. No pitch needed — the work speaks.
- **Pluribus-inspired color restraint.** Inspired by Vince Gilligan's Apple TV+ series *Pluribus*, which uses deliberate, minimal color to guide attention. Scenes are driven by mood, not palette complexity.
- **Apple-level interactivity.** Scroll-driven animations give visual impact. Things zoom, reveal, and come alive as you scroll. Motion replaces color as the attention driver.
- **Simplicity.** No more than 3 colors. People focus on the message, not getting distracted by varying colors.

## Color Palette

Chosen: **Option 4 — Yellow + Near-Black + Warm White** (Pluribus Minimal)

| Role       | Hex       | Usage                          |
|------------|-----------|--------------------------------|
| Background | `#1a1a1a` | Page background, card fills    |
| Accent     | `#f5c542` | Logo, tagline, CTAs, highlights|
| Text       | `#f0ece2` | Body text, titles, descriptions|

Yellow and near-black on warm white. The yellow pops hard against dark backgrounds. Content breathes.

## Page Structure

A vertical scroll film. Each project is a full-viewport scene with scroll-driven animation.

### Scene Sequence

1. **Hero** — "Hippogriff" title scales in, tagline reveals word-by-word, subtitle fades up. Scroll hint pulses at bottom.
2. **Project Scenes** — Each project is a sticky full-viewport section. Scroll progress drives a unique animation per project. Currently one (TypeCraft), designed to scale to ~8.
3. **Coming Soon** — Placeholder cards for unreleased projects, dimmed.
4. **Footer** — Minimal. GitHub link. "built with love."

### TypeCraft Scene

- As user scrolls into the section, pixel-art invaders begin falling from the top
- Letters appear on the invaders (matching the game mechanic)
- Scroll deeper → more invaders, faster spawn rate, higher intensity
- An intensity bar on the right edge shows scroll depth
- At ~60% scroll, the project name + description + "Play" CTA fades in over the invader rain
- Links to `typecraft.hippogriff.io`

### Future Project Scenes

Each project will get its own scroll-driven animation tailored to what it does:
- Resume optimization project → TBD animation
- Interior design agent → TBD animation
- ~5 more projects over time

## Interaction Model

- **Scroll-only.** No keyboard capture on the landing page. This avoids conflicts when multiple projects are showcased (e.g., TypeCraft uses keypresses, but the landing page should not).
- **No click-to-enter modes.** Each scene animates on scroll, with a CTA button at the end linking to the live app.

## Technical Approach

- **Framework:** Next.js (static export) on Vercel
- **Animations:** CSS scroll-timeline / Intersection Observer + requestAnimationFrame (no heavy animation libraries)
- **Projects as data:** Defined in an array — name, description, URL, animation component. Adding a project = adding an array entry + an animation component.
- **Fonts:** Inter (from Google Fonts or self-hosted)

## Prototypes

- `prototypes/01-palette-explorer.html` — Interactive color palette playground with presets
- `prototypes/02-scroll-experience.html` — Full scroll experience with invader animation
