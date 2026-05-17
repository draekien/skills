# TanStack Query Linter Alignment

Expected ESLint configuration per preset. Confirm `@tanstack/react-query` or `@tanstack/query-core` is in `package.json` before running these checks.

## Recommended

Enable `@tanstack/eslint-plugin-query` `flat/recommended`:

```js
// eslint.config.js
import tanstackQuery from '@tanstack/eslint-plugin-query';

export default [
  ...tanstackQuery.configs['flat/recommended'],
];
```

`flat/recommended` enables:

- `@tanstack/query/exhaustive-deps` — all `queryFn` vars must be in `queryKey`
- `@tanstack/query/stable-query-client` — `QueryClient` must not be created inline
- `@tanstack/query/no-rest-destructuring` — avoid rest-spreading query results
- `@tanstack/query/infinite-query-property-order` — correct prop order for infinite queries

Requires: `@tanstack/eslint-plugin-query`. If absent, report it as recommended and ask whether to add it.

Biome and OxLint have no native TanStack Query rules — use ESLint.

## Strict

Same plugin config as recommended. Strict adds no extra lint rules; its rigour is enforced through coding standards (`exhaustive-query-key.md`, `no-state-sync.md`, `parallel-queries.md`).
