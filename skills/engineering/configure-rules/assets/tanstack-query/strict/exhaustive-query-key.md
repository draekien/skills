# Exhaustive Query Key

Every variable read inside `queryFn` must appear in `queryKey`. Variables absent from the key are invisible to the cache — the query returns stale data when those variables change.

```typescript
// prefer — all queryFn inputs are in queryKey
useQuery({
  queryKey: postKeys.list({ status, page, userId }),
  queryFn: () => fetchPosts({ status, page, userId }),
});

// avoid — page and userId are used in queryFn but missing from queryKey
useQuery({
  queryKey: ['posts', status],           // cache key ignores page and userId
  queryFn: () => fetchPosts({ status, page, userId }), // stale cache hit when page changes
});
```

Enable `@tanstack/eslint-plugin-query`'s `exhaustive-deps` rule to catch this automatically:

```js
// eslint.config.js
import tanstackQuery from '@tanstack/eslint-plugin-query';

export default [
  ...tanstackQuery.configs['flat/recommended'],
];
```

The rule reports any closure variable used in `queryFn` that is not present in the `queryKey` array.
