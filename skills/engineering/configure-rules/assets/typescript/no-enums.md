# No Enums

Avoid TypeScript enums. Use `as const` objects with a derived union type instead.

Enums generate runtime JavaScript, have surprising reverse-mapping behaviour for numeric variants, and don't interop cleanly with plain string unions expected by external APIs or other tools.

```typescript
// prefer
const Direction = {
  Up: 'UP',
  Down: 'DOWN',
  Left: 'LEFT',
  Right: 'RIGHT',
} as const;

type Direction = typeof Direction[keyof typeof Direction];
// → 'UP' | 'DOWN' | 'LEFT' | 'RIGHT'

// avoid
enum Direction {
  Up = 'UP',
  Down = 'DOWN',
  Left = 'LEFT',
  Right = 'RIGHT',
}
```

`const` objects are plain values — they tree-shake cleanly, serialise to JSON without ceremony, and the derived union type is compatible anywhere a string literal is expected.

`const enum` is not a safe alternative: it is inlined by the TypeScript compiler but broken by tools that transpile files individually (esbuild, Babel, SWC).
