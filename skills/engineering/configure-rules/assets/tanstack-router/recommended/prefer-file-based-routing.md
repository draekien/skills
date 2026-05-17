# Prefer File-Based Routing

Define routes as files under the configured `routesDirectory` rather than constructing the route tree in code. The file structure directly mirrors the URL hierarchy, making routes easy to locate and co-locate with their components.

```
// prefer — file tree maps to URL tree
src/routes/
  __root.tsx          →  layout for all routes
  index.tsx           →  /
  posts.tsx           →  /posts
  posts.$postId.tsx   →  /posts/:postId
  _auth/
    profile.tsx       →  /profile  (pathless _auth layout)

// avoid — code-based tree assembled manually
const postRoute = createRoute({ getParentRoute: () => rootRoute, path: '/posts' })
const rootRoute = createRootRoute()
const routeTree = rootRoute.addChildren([postRoute])
```

Code-based routing is available for edge cases (dynamic plugin systems, programmatic generation) but should not be the default.
