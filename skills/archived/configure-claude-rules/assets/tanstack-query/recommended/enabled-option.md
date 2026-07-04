---
paths:
  - "**/*.{ts,tsx}"
---

# Enabled Option for Dependent Queries

Gate any query that depends on a runtime value with `enabled: !!value`. Without it the query fires immediately with `undefined`, producing 404s or malformed requests before the dependency is available.

```typescript
// prefer
function useUserPosts(userId: string | undefined) {
  return useQuery({
    queryKey: postKeys.byUser(userId!),
    queryFn: () => fetchPostsByUser(userId!),
    enabled: !!userId, // query is skipped until userId is defined
  });
}

// chaining: second query waits for first to resolve
function usePostWithAuthor(postId: string) {
  const { data: post } = useQuery({
    queryKey: postKeys.detail(postId),
    queryFn: () => fetchPost(postId),
  });

  return useQuery({
    queryKey: userKeys.detail(post?.authorId!),
    queryFn: () => fetchUser(post!.authorId),
    enabled: !!post?.authorId,
  });
}

// avoid — fires immediately with undefined userId
useQuery({
  queryKey: postKeys.byUser(userId),
  queryFn: () => fetchPostsByUser(userId), // userId is undefined on first render
});
```

`enabled: false` pauses the query indefinitely; `enabled: !!value` resumes automatically once the value is defined.
