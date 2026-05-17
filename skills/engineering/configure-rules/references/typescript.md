# TypeScript tsconfig Alignment

Expected `tsconfig.json` compiler flags per preset. Use this during discrepancy detection to compare the target repo's configuration against the chosen preset.

## Recommended

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

`strict: true` is a shorthand that enables: `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitAny`, `noImplicitThis`, `useUnknownInCatchVariables`, `alwaysStrict`.

Check for `strict: true` **or** all of the above flags set individually. Either form satisfies the recommended preset.

## Strict

All recommended flags, plus:

```json
{
  "compilerOptions": {
    "strict": true,
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

## Checking an `extends` chain

If `tsconfig.json` uses `extends`, resolve the chain and check the merged result. A flag set in a base config counts as set. Report which file in the chain sets each flag when surfacing discrepancies.
