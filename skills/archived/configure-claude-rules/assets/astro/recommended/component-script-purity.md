---
paths:
  - "**/*.astro"
---

# Component Script Purity

Code inside `---` frontmatter fences runs server-side only (at build time for SSG, per request for SSR). Never access browser globals there.

```astro
---
// prefer — server-safe data fetching
const posts = await getCollection('blog');
const title = Astro.props.title;

// avoid — window/document do not exist server-side
const width = window.innerWidth;
document.title = 'hello';
---
```

For client-side logic, use a `<script>` tag or a framework component island with a `client:*` directive.
