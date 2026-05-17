# No Unchecked Indexed Access

Treat array and object index access as potentially `undefined`. Never assume an index exists without checking.

```typescript
// prefer — check before use
const first = items[0];
if (first === undefined) return;
process(first);

// or use explicit destructuring with a default
const [head = defaultValue] = items;

// avoid — assumes index exists
const first = items[0];
process(first); // first could be undefined if items is empty
```

When `noUncheckedIndexedAccess` is enabled in `tsconfig.json`, TypeScript enforces this automatically. The rule here extends that discipline to code review and AI-generated code regardless of tsconfig state.

For `Record<string, T>` lookups, prefer `Map<string, T>` when the key set is dynamic — it makes the optional nature of lookups explicit in the type.
