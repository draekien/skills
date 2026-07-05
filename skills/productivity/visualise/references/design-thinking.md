# Design Thinking

Aesthetic direction and frontend design principles for generating visually striking, readable HTML visualisations.

Before coding, commit to a bold aesthetic direction:

- **Purpose** — What problem does this interface solve? Who uses it?
- **Tone** — Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian. Use these for inspiration but design one that is true to the aesthetic direction.
- **Differentiation** — What makes this unforgettable? What's the one thing someone will remember?

Choose a clear conceptual direction and execute it with precision. The key is intentionality, not intensity. Visual clarity and readability are non-negotiable — every aesthetic choice must serve comprehension, not fight it.

## Dependencies

Load libraries via CDN — do not bundle or download anything. `scripts/validate.py` only accepts resources from its `ALLOWED_CDN_HOSTS` list (currently `cdn.tailwindcss.com`, `cdnjs.cloudflare.com`, `cdn.jsdelivr.net`, `cdn.plot.ly`) — check that list before reaching for an unlisted host. Approved CDN libraries:

- **Tailwind CSS** — `<script src="https://cdn.tailwindcss.com"></script>` for utility-first styling. Prefer inline `<style>` rules or a non-Tailwind library when font-size compliance must be verified by the validator. If Tailwind is used, manually audit all `text-*` utility classes to confirm body text meets the 1rem minimum before reporting the file to the user.
- **Chart.js** — for charts and graphs
- **D3.js** — for complex data visualisations
- **Alpine.js** — for lightweight interactivity without a framework

Only include what the visualisation actually needs.

## Frontend Aesthetics

- **Typography** — Pair a distinctive display font with a purpose-built body font. Load via Google Fonts or similar CDN. These are separate concerns with different constraints:
  - *Display / headings*: Choose something beautiful, unique, and interesting. Avoid generic fonts (Arial, Inter, Roboto, system fonts, Space Grotesk).
  - *Body / prose*: Must be designed for extended reading — a humanist sans-serif or a reading-optimised serif with high x-height and moderate stroke contrast. Never use decorative, display, geometric, or ultra-thin fonts for body text. Hard limits: minimum `1rem` (16px), line-height `1.5–1.7`, prose containers `max-width: 65ch`. On dark backgrounds, bump line-height by `0.05–0.1` and add `letter-spacing: 0.01–0.02em` to compensate for perceived weight loss.
- **Color & Theme** — Commit to a cohesive aesthetic. Use CSS variables for consistency. Ensure sufficient contrast for readability. Vary between light and dark themes across generations — never converge on common choices.
- **Motion** — CSS-only animations. Focus on high-impact moments: staggered page load reveals, hover states that surprise. Never animate content the user needs to read mid-animation.
- **Spatial Composition** — Unexpected layouts. Asymmetry. Overlap. Generous negative space OR controlled density — but always guided by what makes the content easiest to parse.
- **Backgrounds & Visual Details** — Create atmosphere and depth: gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, grain overlays. Effects must enhance rather than obscure the content.

Never produce generic AI-generated aesthetics: overused font families, clichéd purple gradients on white backgrounds, predictable layouts, or cookie-cutter design that lacks context-specific character.

Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate effects. Minimalist designs need restraint and precision. Elegance comes from executing the vision well, not from volume of code.
