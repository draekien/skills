---
paths:
  - "**/*.{ts,tsx}"
---

# Parallel Queries

Fetch independent data with co-located `useQuery` calls or `useQueries` — never chain them sequentially. Sequential fetching creates artificial waterfalls where the total load time is the sum of all request durations instead of the maximum.

```typescript
// prefer — two useQuery calls at the same component level fire in parallel
function Dashboard({ userId }: { userId: string }) {
  const { data: user } = useQuery({ queryKey: userKeys.detail(userId), queryFn: () => fetchUser(userId) });
  const { data: posts } = useQuery({ queryKey: postKeys.byUser(userId), queryFn: () => fetchPostsByUser(userId) });

  return <>{/* render both */}</>;
}

// prefer — useQueries for a dynamic number of parallel queries
function usePostsForUsers(userIds: string[]) {
  return useQueries({
    queries: userIds.map((id) => ({
      queryKey: postKeys.byUser(id),
      queryFn: () => fetchPostsByUser(id),
    })),
  });
}

// avoid — waiting for user before fetching posts when neither depends on the other
function Dashboard({ userId }: { userId: string }) {
  const { data: user } = useQuery({ queryKey: userKeys.detail(userId), queryFn: () => fetchUser(userId) });

  const { data: posts } = useQuery({
    queryKey: postKeys.byUser(userId),
    queryFn: () => fetchPostsByUser(userId),
    enabled: !!user, // unnecessary gate — posts don't need user data
  });
}
```

Use `enabled` to chain queries only when the second query genuinely depends on data returned by the first.
