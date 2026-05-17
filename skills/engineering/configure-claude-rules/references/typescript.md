# TypeScript tsconfig Alignment

Expected `tsconfig.json` compiler flags per preset.

## Recommended

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

`strict: true` enables `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitAny`, `noImplicitThis`, `useUnknownInCatchVariables`, `alwaysStrict`. Either `strict: true` or all flags set individually satisfies this preset.

## Strict

All recommended flags, plus:

```json
{
  "compilerOptions": {
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

## Notes

A flag set in a base config (via `extends`) counts as set. When reporting discrepancies, name which file in the chain sets each flag.
