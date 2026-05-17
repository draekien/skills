# Query Select

Use the `select` option to transform or derive data inside the query rather than in the component. The selector runs only when the raw data changes, and TanStack Query memoises the result — preventing unnecessary re-renders when unrelated cache updates occur.

```typescript
// prefer — transformation is co-located with the query
function useActiveUsers() {
  return useQuery({
    queryKey: userKeys.lists(),
    queryFn: fetchUsers,
    select: (users) => users.filter((u) => u.isActive),
  });
}

// two components can select different shapes from the same cache entry
function useUserCount() {
  return useQuery({
    queryKey: userKeys.lists(),
    queryFn: fetchUsers,
    select: (users) => users.length, // re-renders only when count changes
  });
}

// avoid — filtering in the component re-runs on every render
function ActiveUserList() {
  const { data: users } = useQuery({ queryKey: userKeys.lists(), queryFn: fetchUsers });
  const activeUsers = users?.filter((u) => u.isActive); // recomputed every render

  return <>{/* render activeUsers */}</>;
}
```

`select` is optional when the raw API shape is already what the component needs. Reach for it when filtering, mapping, or picking fields — not for every query.
