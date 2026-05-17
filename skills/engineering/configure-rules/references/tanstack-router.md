# TanStack Router Linter Alignment

Expected ESLint configuration per preset. Confirm `@tanstack/react-router` or `@tanstack/router` is in `package.json` before running these checks.

## Recommended

Enable `@tanstack/eslint-plugin-router` `flat/recommended`:

```js
// eslint.config.js
import pluginRouter from '@tanstack/eslint-plugin-router'

export default [
  ...pluginRouter.configs['flat/recommended'],
]
```

`flat/recommended` enables:

- `@tanstack/router/create-route-property-order` — enforces consistent property order in `createRoute` / `createRootRoute`

Requires: `@tanstack/eslint-plugin-router`. If absent, report it as recommended and ask whether to add it.

Also check that generated files are excluded from linters and formatters:

- ESLint: `routeTree.gen.ts` in `.eslintignore` or `ignores` array in `eslint.config.js`
- Prettier: `routeTree.gen.ts` in `.prettierignore`

Biome and OxLint have no native TanStack Router rules — use ESLint for this plugin.

## Strict

Same plugin config as recommended. Strict adds no extra lint rules; its rigour is enforced through coding standards (`no-throw-non-router-errors.md`, `no-inline-route-components.md`).

If the project uses `@typescript-eslint/only-throw-error`, confirm it is configured to allow `Redirect` and `NotFoundError` from `@tanstack/router-core`:

```js
{
  '@typescript-eslint/only-throw-error': ['error', {
    allow: [
      { from: 'package', package: '@tanstack/router-core', name: 'Redirect' },
      { from: 'package', package: '@tanstack/router-core', name: 'NotFoundError' },
    ],
  }],
}
```
