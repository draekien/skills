# Tailwind v4 Tooling Alignment

Expected package dependencies and tooling config per preset.

## Recommended

### Dependencies

The following packages must be present in `package.json` (any of `dependencies` or `devDependencies`):

```json
{
  "class-variance-authority": "*",
  "clsx": "*",
  "tailwind-merge": "*"
}
```

If any are absent, report which are missing and offer to install them.

### `cn` utility

Search the codebase for a function that combines `clsx` and `twMerge` — the canonical pattern is:

```ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Common locations: `src/lib/utils.ts`, `src/utils/cn.ts`, `lib/utils.ts`. If no matching function is found, report it and offer to create the file. Default to `src/lib/utils.ts` unless the project has an established utils location.

### Biome

```json
{
  "css": {
    "parser": {
      "cssModules": false,
      "tailwindDirectives": true
    }
  }
}
```

`tailwindDirectives: true` allows `@tailwind`, `@apply`, `@theme`, `@utility`, and `@layer` without parse errors. Without it, Biome will flag Tailwind v4 directives as unknown at-rules.

## Strict

All recommended config, plus:

### Class ordering

Install `prettier-plugin-tailwindcss` to enforce consistent class order automatically:

```json
{
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

Add to `.prettierrc` or `prettier.config.*`. Ensures classes follow Tailwind's recommended order (layout → spacing → typography → colour → effects), which makes diffs easier to read and review.

## Notes

Tailwind v4 requires no `tailwind.config.js` for basic usage — configuration moves to `@theme` in CSS. If a `tailwind.config.js` still exists in the repo, it is likely a v3 migration artefact; flag it and ask whether to remove it.
