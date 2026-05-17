# React Linter Alignment

Expected linter configuration per preset. A repo may use more than one linter (e.g. OxLint for speed plus ESLint for coverage).

## Recommended

Hooks rules, key validation, and component purity.

### ESLint

```js
// eslint.config.js
import reactHooks from 'eslint-plugin-react-hooks';
import react from 'eslint-plugin-react';

export default [
  reactHooks.configs.flat['recommended-latest'],
  {
    plugins: { react },
    rules: { 'react/jsx-key': 'error' },
    settings: { react: { version: 'detect' } },
  },
];
```

`recommended-latest` enables `rules-of-hooks` and `purity` (catches `Math.random()`, `Date.now()`, and other non-deterministic calls during render). Substitute `recommended` if React Compiler diagnostics are unwanted.

Requires: `eslint-plugin-react-hooks`, `eslint-plugin-react`.

### Biome

```json
{
  "linter": {
    "rules": {
      "correctness": {
        "useHookAtTopLevel": "error",
        "useJsxKeyInIterable": "error"
      }
    }
  }
}
```

### OxLint

```json
{
  "plugins": ["react"],
  "rules": {
    "react/rules-of-hooks": "error",
    "react/jsx-key": "error"
  }
}
```

## Strict

Adds exhaustive dependencies and setState-in-effect detection.

### ESLint

```js
{
  rules: {
    'react-hooks/exhaustive-deps': 'error',
    'react-hooks/set-state-in-effect': 'error',
  }
}
```

`set-state-in-effect` requires `recommended-latest` (set above). No equivalent in Biome or OxLint.

### Biome

```json
{
  "linter": {
    "rules": {
      "correctness": { "useExhaustiveDependencies": "error" }
    }
  }
}
```

### OxLint

```json
{
  "rules": { "react/exhaustive-deps": "error" }
}
```

## Optional rules

For the `no-default-props` optional rule.

### ESLint

```js
{ rules: { 'react/no-default-props': 'error' } }
```

### Biome

No native equivalent — `noDefaultProps` does not exist in Biome 2.x. Use ESLint if enforcement is needed.

### OxLint

No native equivalent — use `eslint-plugin-react` if needed.
