# Invalidate After Mutation

Call `queryClient.invalidateQueries` after a successful mutation instead of calling `refetch` directly. Invalidation is lazy — it marks cached queries as stale and only refetches those that are currently mounted. Direct `refetch` is eager and refetches regardless of whether any component is observing the query.

```typescript
// prefer
const queryClient = useQueryClient();

const mutation = useMutation({
  mutationFn: (data: CreatePostData) => createPost(data),
  onSuccess: () => {
    // marks all post list queries stale; refetch runs only for mounted observers
    queryClient.invalidateQueries({ queryKey: postKeys.lists() });
  },
});

// avoid — refetches unconditionally even if no component is showing this data
const { refetch } = useQuery({ queryKey: postKeys.lists(), queryFn: fetchPosts });

const mutation = useMutation({
  mutationFn: createPost,
  onSuccess: () => refetch(), // eager, wasteful
});
```

For mutations where the server response already contains the updated entity, use `queryClient.setQueryData` to update the cache directly and skip the network round-trip entirely.
