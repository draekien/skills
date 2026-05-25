---
paths:
  - "**/*.astro"
---

# Typed Props

Declare `interface Props` or `type Props` in every component script that accepts props. Accessing `Astro.props` without a type declaration produces implicit `any` and removes all prop-site checking.

```astro
---
// prefer
interface Props {
  title: string;
  description?: string;
}
const { title, description } = Astro.props;

// avoid — Astro.props is implicitly any
const { title, description } = Astro.props;
---
```
