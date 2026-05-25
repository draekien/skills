---
paths:
  - "**/*.astro"
---

# Minimal Client Directives

Use the least-eager `client:*` directive that still meets the UX requirement. Every upgrade toward `client:load` ships more JavaScript on the critical path.

```astro
// prefer — hydrate only when visible
<Counter client:visible />

// prefer — hydrate during idle time
<Newsletter client:idle />

// avoid — hydrates immediately, blocks main thread
<Counter client:load />
```

Directive priority (least to most eager): `client:visible` → `client:idle` → `client:media` → `client:only` → `client:load`. Use `client:only` when the component cannot render server-side at all.
