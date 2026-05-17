# React Linter Alignment

Expected linter configuration per preset for React-specific rules. Use this during discrepancy detection to compare the target repo's linter config against the chosen preset.

## Detecting the linter

Look for these config files to identify which linter(s) the repo uses:

- `biome.json` or `biome.toml` → Biome
- `.oxlintrc.json`, `oxlint.config.json`, or `"oxlint"` in `package.json` scripts → OxLint
- `eslint.config.js`, `.eslintrc.js`, `.eslintrc.cjs`, `.eslintrc.json`, `.eslintrc.yml` → ESLint

A repo may use more than one (e.g., OxLint for speed + ESLint for rules OxLint does not yet cover natively).

## Recommended

Hooks rules, key validation, and component purity.

### ESLint

```js
// eslint.config.js
import reactHooks from 'eslint-plugin-react-hooks';
import react from 'eslint-plugin-react';

export default [
  reactHooks.configs.flat['recommended-latest'], // rules-of-hooks + purity
  {
    plugins: { react },
    rules: {
      'react/jsx-key': 'error',
    },
    settings: { react: { version: 'detect' } },
  },
];
```

`recommended-latest` enables `rules-of-hooks` and `purity` (catches `Math.random()`, `Date.now()`, and other non-deterministic calls during render). Use `recommended` instead if React Compiler diagnostics are unwanted.

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

All recommended rules, plus exhaustive dependency checking and setState-in-effect detection.

### ESLint

Add to recommended config:

```js
{
  rules: {
    'react-hooks/exhaustive-deps': 'error',
    'react-hooks/set-state-in-effect': 'error', // catches useEffect(() => { setState(...) })
  }
}
```

`set-state-in-effect` is only available via `recommended-latest` (enabled in the recommended section above). No equivalent in Biome or OxLint.

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

## Optional rules

For the `no-default-props` optional rule.

### ESLint

```js
{
  rules: {
    'react/no-default-props': 'error',
  }
}
```

### Biome

```json
{
  "linter": {
    "rules": {
      "suspicious": {
        "noDefaultProps": "error"
      }
    }
  }
}
```

### OxLint

No native equivalent. Can be enforced via the `eslint-plugin-react` JS plugin if needed.

## Checking config files

For each expected rule that is absent or set to `"warn"` when `"error"` is expected:

- Report the rule name, expected severity, and actual value (or "not configured").
- Ask whether to update the config file, leave it as-is, or note it for later.

If no linter config is found, skip this check.
