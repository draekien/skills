---
paths:
  - "**/*.{ts,tsx}"
---

# Prefer `const`

Use `const` by default. Only use `let` when the variable must be reassigned after declaration. Never use `var`.

```typescript
// prefer
const count = items.length;
const user = await fetchUser(id);

// only when reassignment is required
let cursor: string | undefined;
cursor = response.nextCursor;
```

Reassigning object properties does not require `let` — the binding itself is not changing.

```typescript
const config = { retries: 3 };
config.retries = 5; // fine — const binding, mutable object
```
