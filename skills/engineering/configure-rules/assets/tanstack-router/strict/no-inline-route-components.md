# No Inline Route Components

Define route components as named functions outside the `createFileRoute()` call, not as inline arrow functions inside it. Inline definitions create a new component reference on every module evaluation, which can cause React to unmount and remount the tree.

```typescript
// prefer
function PostsPage() {
  const { posts } = Route.useLoaderData()
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}

export const Route = createFileRoute('/posts')({
  loader: fetchPosts,
  component: PostsPage,
})

// avoid — component defined inline
export const Route = createFileRoute('/posts')({
  loader: fetchPosts,
  component: () => {
    const { posts } = Route.useLoaderData()
    return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
  },
})
```
