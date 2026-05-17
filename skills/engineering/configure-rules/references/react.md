# React Linter Alignment

Expected linter configuration per preset for React-specific rules. Use this during discrepancy detection to compare the target repo's linter config against the chosen preset.

## Detecting the linter

Look for these config files to identify which linter(s) the repo uses:

- `biome.json` or `biome.toml` → Biome
- `.oxlintrc.json`, `oxlint.config.json`, or `"oxlint"` in `package.json` scripts → OxLint
- `eslint.config.js`, `.eslintrc.js`, `.eslintrc.cjs`, `.eslintrc.json`, `.eslintrc.yml` → ESLint

A repo may use more than one (e.g., OxLint for speed + ESLint for rules OxLint does not yet cover natively).

## Recommended

Hooks rules and key validation.

### ESLint

```js
// eslint.config.js
import reactHooks from 'eslint-plugin-react-hooks';
import react from 'eslint-plugin-react';

export default [
  reactHooks.configs.flat.recommended, // enables rules-of-hooks: error
  {
    plugins: { react },
    rules: {
      'react/jsx-key': 'error',
    },
    settings: { react: { version: 'detect' } },
  },
];
```

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

All recommended rules, plus exhaustive dependency checking.

### ESLint

Add to recommended config:

```js
{
  rules: {
    'react-hooks/exhaustive-deps': 'error',
  }
}
```

### Biome

Add to recommended config:

```json
{
  "linter": {
    "rules": {
      "correctness": {
        "useExhaustiveDependencies": "error"
      }
    }
  }
}
```

### OxLint

Add to recommended config:

```json
{
  "rules": {
    "react/exhaustive-deps": "error"
  }
}
```

## Checking config files

For each expected rule that is absent or set to `"warn"` when `"error"` is expected:

- Report the rule name, expected severity, and actual value (or "not configured").
- Ask whether to update the config file, leave it as-is, or note it for later.

If no linter config is found, skip this check.
