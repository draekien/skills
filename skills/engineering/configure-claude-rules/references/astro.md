# Astro Tooling Alignment

Expected tooling configuration per preset.

## Recommended

### tsconfig.json

Extend Astro's built-in `strict` template:

```json
{
  "extends": "astro/tsconfigs/strict"
}
```

Alternatively use the package form: `@astrojs/tsconfig/strict`.

### eslint.config.js

```js
import eslintPluginAstro from 'eslint-plugin-astro';

export default [
  ...eslintPluginAstro.configs.recommended,
];
```

Requires: `eslint-plugin-astro`, `astro-eslint-parser`.

For TypeScript inside `.astro` files, also add `@typescript-eslint/parser` and set `parserOptions.parser`.

## Strict

### tsconfig.json

Extend Astro's `strictest` template:

```json
{
  "extends": "astro/tsconfigs/strictest"
}
```

`strictest` adds `verbatimModuleSyntax: true` (enforces `import type` for type-only imports) on top of `strict`.

### eslint.config.js

Add TypeScript-aware rules alongside the Astro plugin:

```js
import eslintPluginAstro from 'eslint-plugin-astro';
import tseslint from 'typescript-eslint';

export default [
  ...eslintPluginAstro.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: { project: true },
    },
  },
];
```

### astro.config.mjs

`output` must be explicitly set (see `explicit-output-mode` rule):

```ts
export default defineConfig({
  output: 'static', // or 'server' | 'hybrid'
});
```

## Notes

- Astro ships three tsconfig templates: `base`, `strict`, `strictest`. Always extend one rather than writing compiler options from scratch.
- `eslint-plugin-astro` uses `astro-eslint-parser` internally; set `parser: 'astro-eslint-parser'` in overrides if using legacy `.eslintrc` format.
- For accessibility linting in `.astro` files, add `eslint-plugin-jsx-a11y` alongside `eslint-plugin-astro`.
