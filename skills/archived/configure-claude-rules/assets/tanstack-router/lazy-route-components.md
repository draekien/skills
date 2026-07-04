---
paths:
  - "**/*.{ts,tsx}"
---

# Lazy Route Components

Use `lazy()` to code-split non-critical route components into separate JS chunks, reducing the initial bundle size.

```typescript
import { createFileRoute, lazy } from '@tanstack/react-router'

// prefer — component loaded only when the route is visited
export const Route = createFileRoute('/settings/advanced')({
  component: lazy(() => import('./AdvancedSettings')),
})

// avoid for large, rarely visited pages — entire component in main bundle
import AdvancedSettings from './AdvancedSettings'

export const Route = createFileRoute('/settings/advanced')({
  component: AdvancedSettings,
})
```

Apply to routes that are large, rarely visited, or not needed for the initial render. Skip for small or frequently visited routes where the split overhead outweighs the savings.
