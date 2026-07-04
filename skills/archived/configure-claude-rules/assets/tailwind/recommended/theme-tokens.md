---
paths:
  - "**/*.css"
---

# Define Design Tokens in `@theme`

Define project-specific colors, spacing, and typography as CSS variables inside an `@theme` block. Never use arbitrary values like `bg-[#0066ff]` for design tokens — they scatter magic values across the codebase and break theme-wide refactoring.

```css
/* prefer */
@import "tailwindcss";

@theme {
  --color-brand: oklch(55% 0.22 250);
  --color-brand-hover: oklch(48% 0.22 250);
  --spacing-page: 1.5rem;
  --font-heading: "Inter", sans-serif;
}

/* avoid — arbitrary values for project-specific tokens */
<div className="bg-[#1a56db] px-[1.5rem] font-['Inter']" />
```

Once defined in `@theme`, tokens become Tailwind utilities automatically (`bg-brand`, `px-page`, `font-heading`). Use OKLCH for colors to stay consistent with Tailwind v4's default palette.
