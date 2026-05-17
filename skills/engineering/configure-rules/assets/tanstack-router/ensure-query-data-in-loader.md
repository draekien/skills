# Ensure Query Data in Loader

Call `queryClient.ensureQueryData(queryOptions)` in the route loader to warm the TanStack Query cache before render, then read with `useSuspenseQuery` in the component. This separates cache warming from rendering and enables SSR streaming.

```typescript
import { queryOptions, useSuspenseQuery } from '@tanstack/react-query'
import { createFileRoute } from '@tanstack/react-router'

const postsQuery = queryOptions({
  queryKey: ['posts'],
  queryFn: () => fetch('/api/posts').then(r => r.json()),
})

// prefer
export const Route = createFileRoute('/posts')({
  loader: ({ context: { queryClient } }) =>
    queryClient.ensureQueryData(postsQuery),
  component: PostsPage,
})

function PostsPage() {
  const { data } = useSuspenseQuery(postsQuery)  // cache already populated
  return <ul>{data.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}

// avoid — fetching only in the component; no SSR, no prefetch
function PostsPage() {
  const { data, isLoading } = useQuery(postsQuery)
  if (isLoading) return <Spinner />
  return <ul>{data.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

Pair with `useSuspenseQuery` (not `useQuery`) so the component never renders without data and participates in SSR streaming.
