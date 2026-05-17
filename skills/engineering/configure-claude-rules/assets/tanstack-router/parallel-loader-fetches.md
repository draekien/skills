---
paths:
  - "**/*.{ts,tsx}"
---

# Parallel Loader Fetches

When a route loader needs multiple queries, fire them with `Promise.allSettled` rather than awaiting them sequentially. Sequential awaits create a waterfall where each fetch blocks the next.

```typescript
import { queryOptions } from '@tanstack/react-query'

const postsQuery = queryOptions({ queryKey: ['posts'], queryFn: fetchPosts })
const tagsQuery = queryOptions({ queryKey: ['tags'], queryFn: fetchTags })

// prefer — both requests in flight simultaneously
export const Route = createFileRoute('/posts')({
  loader: ({ context: { queryClient } }) =>
    Promise.allSettled([
      queryClient.ensureQueryData(postsQuery),
      queryClient.ensureQueryData(tagsQuery),
    ]),
})

// avoid — sequential waterfall doubles the wait time
export const Route = createFileRoute('/posts')({
  loader: async ({ context: { queryClient } }) => {
    await queryClient.ensureQueryData(postsQuery)
    await queryClient.ensureQueryData(tagsQuery)
  },
})
```

`allSettled` (not `all`) is preferred because a single failed query does not abort the others; each query's error can be handled individually in its consuming component.
