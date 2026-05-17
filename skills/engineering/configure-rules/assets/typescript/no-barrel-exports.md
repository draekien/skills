---
paths:
  - "**/*.{ts,tsx}"
---

# No Barrel Exports

Avoid `index.ts` barrel files that re-export from multiple modules. Import directly from the source file instead.

```typescript
// prefer
import { UserService } from './services/user-service';
import { formatDate } from './utils/date';

// avoid — barrel re-export
import { UserService, formatDate } from './';
```

Barrel files cause several problems at scale:

- **Circular dependencies**: re-exporting across module boundaries makes cycles easy to create and hard to detect.
- **Slower builds**: TypeScript's module resolver and bundlers must process every file a barrel touches, even when only one export is needed.
- **Worse tree-shaking**: some bundlers cannot statically analyse re-export chains and include more code than necessary.

If a module has a true public API that should be stable and separate from its internal structure, a single `index.ts` that explicitly documents that boundary is acceptable. The rule is against reflexive barrel files that exist only for import convenience.
