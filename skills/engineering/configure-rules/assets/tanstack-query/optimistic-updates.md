---
paths:
  - "**/*.{ts,tsx}"
---

# Optimistic Updates

Apply the expected mutation result to the cache immediately, then roll back if the server rejects it. This makes write operations feel instant without waiting for the network round-trip.

```typescript
const queryClient = useQueryClient();

const mutation = useMutation({
  mutationFn: (updatedPost: Post) => updatePost(updatedPost),

  onMutate: async (updatedPost) => {
    // cancel any in-flight refetches so they don't overwrite the optimistic update
    await queryClient.cancelQueries({ queryKey: postKeys.detail(updatedPost.id) });

    // snapshot the current value for rollback
    const previousPost = queryClient.getQueryData<Post>(postKeys.detail(updatedPost.id));

    // apply optimistic update
    queryClient.setQueryData(postKeys.detail(updatedPost.id), updatedPost);

    return { previousPost };
  },

  onError: (_error, updatedPost, context) => {
    // roll back to snapshot
    queryClient.setQueryData(postKeys.detail(updatedPost.id), context?.previousPost);
  },

  onSettled: (_, __, updatedPost) => {
    // always sync with server truth after success or error
    queryClient.invalidateQueries({ queryKey: postKeys.detail(updatedPost.id) });
  },
});
```

Use optimistic updates for write-heavy or interactive UIs (drag-and-drop reordering, inline editing, like/unlike). For simple forms or low-frequency writes, the complexity is not worth it — show a loading state instead.
