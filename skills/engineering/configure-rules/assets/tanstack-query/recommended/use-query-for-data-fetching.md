---
paths:
  - "**/*.{ts,tsx}"
---

# Use TanStack Query for Data Fetching

Fetch server data with `useQuery` rather than `fetch` inside `useEffect`. Manual fetching requires boilerplate loading/error state, is prone to race conditions when dependencies change quickly, and provides no caching or background refresh.

```typescript
// prefer
function UserProfile({ id }: { id: string }) {
  const { data: user, isPending, isError } = useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => fetchUser(id),
  });

  if (isPending) return <Spinner />;
  if (isError) return <ErrorMessage />;
  return <div>{user.name}</div>;
}

// avoid — manual state, no caching, susceptible to race conditions
function UserProfile({ id }: { id: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [isPending, setIsPending] = useState(false);

  useEffect(() => {
    setIsPending(true);
    fetch(`/api/users/${id}`)
      .then(res => res.json())
      .then(data => {
        setUser(data);
        setIsPending(false);
      });
  }, [id]);

  if (isPending) return <Spinner />;
  return <div>{user?.name}</div>;
}
```

The avoid example has a stale-closure bug: if `id` changes while the request is in flight, both responses race to update state. `useQuery` handles deduplication and cancellation automatically.
