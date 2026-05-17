# Deep Modules

A module's value is its power-to-interface ratio. Prefer a few rich abstractions that hide substantial complexity behind a narrow surface over many thin wrappers that expose every internal step to callers.

```
// prefer — one call, all complexity hidden
store.save(record)

// avoid — caller orchestrates internal steps; every step is a new dependency
store.beginTransaction()
store.validate(record)
store.writeRow(record)
store.commitTransaction()
```

A module whose interface is nearly as complex as its implementation (a shallow module) adds cognitive overhead without returning value. When in doubt, pull complexity inward.
