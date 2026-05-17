# Error Handling

Type `catch` clause bindings as `unknown`. Narrow with `instanceof` or a type guard before accessing properties.

```typescript
// prefer
try {
  await fetchData();
} catch (err: unknown) {
  if (err instanceof Error) {
    logger.error(err.message);
  } else {
    logger.error('Unknown error', { err });
  }
}

// avoid — catch bindings are unknown at runtime
try {
  await fetchData();
} catch (err: any) {
  logger.error(err.message); // unsound
}
```

When defining custom error types, extend `Error` rather than throwing plain objects or strings. This preserves stack traces and makes `instanceof` checks reliable.

```typescript
class ApiError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}
```
