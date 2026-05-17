# No State Sync

Never copy query data into `useState`. Doing so creates a second source of truth that diverges from the cache on background refetches, leaving stale data on screen.

```typescript
// prefer — consume query data directly
function UserProfile({ id }: { id: string }) {
  const { data: user, isLoading } = useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => fetchUser(id),
  });

  if (isLoading) return <Spinner />;
  return <div>{user?.name}</div>;
}

// avoid — local copy becomes stale when the cache updates
function UserProfile({ id }: { id: string }) {
  const { data } = useQuery({ queryKey: userKeys.detail(id), queryFn: () => fetchUser(id) });
  const [user, setUser] = useState(data); // diverges after background refetch

  useEffect(() => {
    if (data) setUser(data); // playing catch-up with the cache
  }, [data]);

  return <div>{user?.name}</div>;
}
```

The exception is editable form state: copy query data into `useState` (or a form library) only when the user needs to edit it locally before submitting. Use the query result to populate initial values, not as the live data source.
