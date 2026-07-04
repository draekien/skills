---
paths:
  - "**/*.{ts,astro}"
---

# No Unchecked Entry Access

`getEntry()` returns `undefined` when the slug does not exist. Always guard against this before accessing entry properties.

```ts
// prefer
const post = await getEntry('blog', slug);
if (!post) return Astro.redirect('/404');
const { title } = post.data;

// avoid — throws at runtime when slug is missing
const post = await getEntry('blog', slug);
const { title } = post!.data;
```

`getCollection()` always returns an array (never `undefined`), so no guard is needed there.
