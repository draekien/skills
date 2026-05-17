---
paths:
  - "**/*.{ts,tsx}"
---

# Loader for Data Fetching

Fetch async data in the route's `loader` function, not inside component `useEffect` hooks. The loader runs before the component renders, enabling Suspense boundaries and error boundaries to handle loading and error states without component-level boilerplate.

```typescript
// prefer
export const Route = createFileRoute('/posts')({
  loader: async () => {
    const posts = await fetchPosts()
    return { posts }
  },
  component: PostsPage,
})

function PostsPage() {
  const { posts } = Route.useLoaderData()
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}

// avoid — fetching inside the component
function PostsPage() {
  const [posts, setPosts] = useState([])
  useEffect(() => { fetchPosts().then(setPosts) }, [])
  if (!posts.length) return <Spinner />
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```
