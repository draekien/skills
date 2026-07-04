---
paths:
  - "**/*.{ts,tsx}"
---

# Query Key Factory

Centralise all query keys in a factory object so every call site references the same key shape, enabling reliable cache invalidation and eliminating typos.

```typescript
// prefer
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  detail: (id: string) => [...userKeys.all, 'detail', id] as const,
};

function useUsers(filters: UserFilters) {
  return useQuery({ queryKey: userKeys.list(filters), queryFn: () => fetchUsers(filters) });
}

// invalidate all user queries after a mutation
queryClient.invalidateQueries({ queryKey: userKeys.all });

// avoid — inline strings scatter keys across files and break invalidation
useQuery({ queryKey: ['users', filters], queryFn: () => fetchUsers(filters) });
```

Key arrays are serialised for comparison, so `['users', 5]` and `['users', '5']` are different cache entries. The factory enforces consistent types at the definition site.
