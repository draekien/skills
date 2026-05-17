# Stale Time Defaults

Set a meaningful global `staleTime` on `QueryClient`. The built-in default of `0` marks every query stale immediately, causing a background refetch on every component mount.

```typescript
// prefer — configure once at the app boundary
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute: data is fresh for 60 s after fetch
      gcTime: 5 * 60 * 1000, // 5 minutes: unused cache entries are kept for 5 min
    },
  },
});

// override per-query when freshness requirements differ
useQuery({
  queryKey: stockKeys.price(ticker),
  queryFn: () => fetchPrice(ticker),
  staleTime: 10 * 1000, // prices need to be near-real-time
});

// avoid — omitting staleTime entirely hits the API on every mount
const queryClient = new QueryClient();
```

`staleTime` controls when a cached result is considered fresh; `gcTime` controls how long an unused entry stays in memory. Set `staleTime` higher than `gcTime` only when you want to prevent background refetches entirely.
