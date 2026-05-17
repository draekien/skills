# Invalidate on Mutation

Call `router.invalidate()` after mutations to re-run the current route's loaders and keep router-loaded data in sync with the server. This is simpler than manually calling `queryClient.invalidateQueries` for every query a loader touches.

```typescript
import { useRouter } from '@tanstack/react-router'
import { useMutation } from '@tanstack/react-query'

// prefer
function DeletePostButton({ id }: { id: string }) {
  const router = useRouter()
  const { mutate } = useMutation({
    mutationFn: () => deletePost(id),
    onSuccess: () => router.invalidate(),
  })
  return <button onClick={() => mutate()}>Delete</button>
}

// avoid — manually tracking which queries to invalidate
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: ['posts'] })
  queryClient.invalidateQueries({ queryKey: ['post-count'] })
  // easy to miss queries that the loader also fetches
}
```

`router.invalidate()` re-runs all active loaders, which in turn call `ensureQueryData` and refresh the cache. Use targeted `queryClient.invalidateQueries` only when you need to invalidate queries that are not covered by any active loader.
