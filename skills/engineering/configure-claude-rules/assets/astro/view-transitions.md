---
paths:
  - "**/*.astro"
---

# View Transitions

Include `<ViewTransitions />` in the base layout to enable SPA-like page navigation with animated transitions and preserved client state across navigations.

```astro
---
// prefer — in your base Layout.astro
import { ViewTransitions } from 'astro:transitions';
---

<head>
  <ViewTransitions />
</head>

<!-- without — full page reload on every navigation -->
```

Annotate individual elements with `transition:name` to pair them across pages for element-level morph animations. Disable per-element with `transition:animate="none"` when transitions feel jarring.
