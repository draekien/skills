---
paths:
  - "**/*.{ts,tsx}"
---

# Use useMutation for Write Operations

Wrap create, update, and delete operations in `useMutation` rather than calling `fetch` directly in event handlers. `useMutation` tracks pending and error state, exposes lifecycle callbacks for cache updates, and prevents double-submissions.

```typescript
// prefer
const queryClient = useQueryClient();

const mutation = useMutation({
  mutationFn: (id: string) => deletePost(id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: postKeys.lists() });
  },
});

return (
  <button onClick={() => mutation.mutate(postId)} disabled={mutation.isPending}>
    {mutation.isPending ? 'Deleting…' : 'Delete'}
  </button>
);

// avoid — manual state, no lifecycle hooks, no cache sync, double-submit risk
const [isDeleting, setIsDeleting] = useState(false);

async function handleDelete() {
  setIsDeleting(true);
  await fetch(`/api/posts/${postId}`, { method: 'DELETE' });
  setIsDeleting(false); // never resets on error
}

return <button onClick={handleDelete} disabled={isDeleting}>Delete</button>;
```

Use `mutation.isError` and `mutation.error` to surface failure to the user — the avoid pattern silently swallows errors and leaves the button stuck in a loading state if the request fails.
