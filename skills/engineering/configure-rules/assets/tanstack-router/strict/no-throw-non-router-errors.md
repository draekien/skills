# No Throw Non-Router Errors

In route loaders and actions, only throw `redirect()` or `notFound()` from TanStack Router. All other exceptional conditions must throw `Error` instances. Throwing plain objects or strings conflicts with `@typescript-eslint/only-throw-error` and produces untyped error boundaries.

```typescript
import { createFileRoute, redirect, notFound } from '@tanstack/react-router'

// prefer
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    if (!isAuthenticated()) throw redirect({ to: '/login' })
    const post = await fetchPost(params.postId)
    if (!post) throw notFound()
    if (post.error) throw new Error(post.error.message)  // Error instance
    return post
  },
})

// avoid — throwing non-Error values
loader: async ({ params }) => {
  if (someFailure) throw { code: 500, message: 'failed' }  // plain object
  if (otherCase) throw 'something went wrong'              // string
}
```

Configure `@typescript-eslint/only-throw-error` to allow `Redirect` and `NotFoundError` from `@tanstack/router-core` as throwable exceptions.
