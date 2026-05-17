---
paths:
  - "**/*.{ts,tsx}"
---

# Query Client in Router Context

Pass `QueryClient` through TanStack Router's context rather than importing a module-level singleton in loaders. Context-provided clients are required for SSR dehydration/hydration and make loaders testable without module mocking.

```typescript
// prefer — router/main.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createRouter } from '@tanstack/react-router'
import { dehydrate, hydrate } from '@tanstack/react-query'

const queryClient = new QueryClient()

const router = createRouter({
  routeTree,
  context: { queryClient },
  dehydrate: () => ({ queryClientState: dehydrate(queryClient) }),
  hydrate: (d) => hydrate(queryClient, d.queryClientState),
  Wrap: ({ children }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  ),
})

// prefer — route loader uses context
export const Route = createFileRoute('/posts')({
  loader: ({ context: { queryClient } }) =>
    queryClient.ensureQueryData(postsQuery),
})

// avoid — importing singleton bypasses SSR context
import { queryClient } from '../queryClient'
loader: () => queryClient.ensureQueryData(postsQuery)
```
