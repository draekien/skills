# TanStack Query Linter Alignment

Expected linter configuration per preset for TanStack Query-specific rules. Use this during discrepancy detection to compare the target repo's linter config against the chosen preset.

## Detecting the plugin

Look for `@tanstack/eslint-plugin-query` in `package.json` `devDependencies` or `dependencies`. If absent, no automated enforcement is configured.

Also check for `@tanstack/query` or `@tanstack/react-query` in dependencies to confirm TanStack Query is in use before running this check.

## Recommended

Stable query client and exhaustive dependency checking.

### ESLint

```js
// eslint.config.js
import tanstackQuery from '@tanstack/eslint-plugin-query';

export default [
  ...tanstackQuery.configs['flat/recommended'],
  // flat/recommended enables:
  //   @tanstack/query/exhaustive-deps        — all queryFn vars must be in queryKey
  //   @tanstack/query/stable-query-client    — QueryClient must not be created inline
  //   @tanstack/query/no-rest-destructuring  — avoid rest-spreading query results
  //   @tanstack/query/infinite-query-property-order — correct prop order for infinite queries
];
```

Requires: `@tanstack/eslint-plugin-query`.

### Biome / OxLint

No native equivalent rules for TanStack Query. Use ESLint with `@tanstack/eslint-plugin-query` for automated enforcement.

## Strict

All recommended rules. No additional plugin rules beyond `flat/recommended` — the strict preset is enforced through coding standards (see `exhaustive-query-key.md`, `no-state-sync.md`, `parallel-queries.md`) rather than additional linter config.

## Checking config files

For each expected rule that is absent or set to `"warn"` when `"error"` is expected:

- Report the rule name, expected severity, and actual value (or "not configured").
- Ask whether to update the config file, leave it as-is, or note it for later.

If `@tanstack/eslint-plugin-query` is not installed, report that it is recommended for the selected preset and ask whether to add it.
