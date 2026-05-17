---
paths:
  - "**/*.{ts,tsx}"
---

# No Modify Generated Files

Never manually edit `routeTree.gen.ts` or any other file with a `.gen.ts` suffix produced by the TanStack Router CLI or Vite plugin. These files are fully regenerated on every dev start and build, overwriting any manual changes.

```typescript
// prefer — add a new route by creating a file in the routes directory
// src/routes/posts.tsx  →  router regenerates routeTree.gen.ts automatically

// avoid — editing routeTree.gen.ts directly
// /* TANSTACK_ROUTER_MANIFEST ... */
// export const routeTree = rootRoute.addChildren({ ... })  ← will be overwritten
```

Exclude the file from linters and formatters (`.eslintignore`, `.prettierignore`) and mark it read-only in VS Code via `"files.readonlyInclude": { "**/routeTree.gen.ts": true }`. Commit the file to git — it is required for type checking and builds.
