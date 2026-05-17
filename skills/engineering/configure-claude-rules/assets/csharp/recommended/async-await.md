---
paths:
  - "**/*.cs"
---

# Async/Await

Use `async`/`await` for all I/O-bound operations. Never block asynchronous code with `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()` — these cause deadlocks in contexts that have a synchronisation context (ASP.NET, WPF, WinForms).

```csharp
// prefer
public async Task<User> GetUserAsync(int id)
{
    return await _repo.FindAsync(id);
}

public async Task<IReadOnlyList<Order>> GetOrdersAsync(int userId)
{
    var orders = await _db.Orders
        .Where(o => o.UserId == userId)
        .ToListAsync();
    return orders;
}

// avoid — blocks the thread, deadlock risk
public User GetUser(int id)
{
    return _repo.FindAsync(id).Result;
}

public IReadOnlyList<Order> GetOrders(int userId)
{
    return _db.Orders.Where(o => o.UserId == userId).ToListAsync().GetAwaiter().GetResult();
}
```

Pass `CancellationToken` through async call chains whenever the caller may want to cancel. Accept it as the last parameter and forward it to every awaited call.

Avoid `async void` except in event handlers. Return `Task` (or `ValueTask` for hot paths) so callers can observe exceptions.
