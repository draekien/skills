---
paths:
  - "**/*.{ts,tsx}"
---

# Typed Search Params

Define a `validateSearch` schema on every route that reads search params. Without validation, search params are typed as `unknown` and silently accept malformed URLs.

```typescript
import { z } from 'zod'
import { createFileRoute } from '@tanstack/react-router'

const searchSchema = z.object({
  page: z.number().int().positive().catch(1),
  query: z.string().optional(),
})

// prefer
export const Route = createFileRoute('/posts')({
  validateSearch: searchSchema,
  component: PostsPage,
})

function PostsPage() {
  const { page, query } = Route.useSearch()  // fully typed
  return <PostList page={page} query={query} />
}

// avoid — reading search without validation
function PostsPage() {
  const search = useSearch({ from: '/posts' })  // search is unknown
  const page = Number(search.page) || 1         // manual, unvalidated cast
}
```

Use `.catch()` on individual fields to provide fallback values for malformed input rather than throwing a parse error.
