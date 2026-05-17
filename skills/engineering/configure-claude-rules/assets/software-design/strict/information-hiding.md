# Information Hiding

Implementation decisions stay private inside the module that makes them. Callers must not depend on *how* a result is achieved — only *what* the module provides. When an internal change forces caller changes, information has leaked.

```
// prefer — interface exposes the concept, not the mechanism
cache.get(key)
cache.set(key, value, ttl)

// avoid — storage technology leaks through the interface
cache.redisClient.hget("cache_ns", key)
cache.redisClient.expire("cache_ns:" + key, ttl)
```

Information leakage is most common with temporal decomposition: splitting a workflow into separate modules by execution order rather than by the knowledge each module owns. Each module should encapsulate a decision, not a step.
