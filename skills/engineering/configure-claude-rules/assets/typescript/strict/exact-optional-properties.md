---
paths:
  - "**/*.{ts,tsx}"
---

# Exact Optional Properties

Never explicitly assign `undefined` to an optional property. Omit the property instead. Assigning `undefined` is semantically different from absence and breaks code that uses `'key' in obj` checks or JSON serialisation.

```typescript
interface Config {
  timeout?: number;
  retries?: number;
}

// prefer — omit absent properties
const config: Config = { timeout: 5000 };

// avoid — explicitly assigns undefined
const config: Config = { timeout: 5000, retries: undefined };
```

When spreading or building objects conditionally, use short-circuit spreading rather than conditional `undefined` assignment:

```typescript
// prefer
const options = {
  method: 'POST',
  ...(body !== null && { body: JSON.stringify(body) }),
};

// avoid
const options = {
  method: 'POST',
  body: body !== null ? JSON.stringify(body) : undefined,
};
```
