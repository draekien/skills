---
paths:
  - "**/*.{ts,tsx}"
---

# Use Router Navigation

Navigate with `<Link>` and `useNavigate()` from TanStack Router rather than `<a href>` or `window.location`. Router-aware navigation preserves compile-time path checking, history state, and scroll restoration.

```typescript
import { Link, useNavigate } from '@tanstack/react-router'

// prefer
function PostCard({ id }: { id: string }) {
  return <Link to="/posts/$postId" params={{ postId: id }}>Read post</Link>
}

function SaveButton({ id }: { id: string }) {
  const navigate = useNavigate()
  const handleSave = async () => {
    await save()
    navigate({ to: '/posts/$postId', params: { postId: id } })
  }
  return <button onClick={handleSave}>Save</button>
}

// avoid — bypasses type checking and router state
<a href={`/posts/${id}`}>Read post</a>
window.location.href = `/posts/${id}`
```
