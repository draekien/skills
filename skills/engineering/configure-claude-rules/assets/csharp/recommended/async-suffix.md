---
paths:
  - "**/*.cs"
---

# Async Suffix

All methods and properties that return `Task`, `Task<T>`, `ValueTask`, or `ValueTask<T>` must have an `Async` suffix. Synchronous methods must never have an `Async` suffix.

```csharp
// prefer
public async Task<User> GetUserAsync(int id) { ... }
public async Task SaveAsync(Order order) { ... }
public async Task<bool> ExistsAsync(string email) { ... }

// synchronous — no suffix
public User GetUser(int id) { ... }
public IReadOnlyList<Order> GetOrders() { ... }

// avoid — async method without suffix
public async Task<User> GetUser(int id) { ... }

// avoid — sync method with suffix
public User GetUserAsync(int id) { ... }
```

This convention is the .NET standard (Task-based Asynchronous Pattern). It makes async entry points immediately visible to callers and prevents accidental blocking calls where the caller does not notice it is receiving a `Task`.
