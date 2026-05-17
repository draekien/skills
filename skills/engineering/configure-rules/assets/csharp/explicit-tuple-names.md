# Explicit Tuple Names

Always name tuple elements. Never return or accept positional tuples without names — callers cannot tell what `.Item1` and `.Item2` mean.

```csharp
// prefer — named elements, clear intent
public (int Id, string Email) GetUserSummary(int userId)
{
    var user = _repo.Find(userId);
    return (user.Id, user.Email);
}

var (id, email) = GetUserSummary(42);

// prefer — deconstruct with meaningful names
var (orderId, total, placedAt) = GetOrderSummary(orderId);

// avoid — positional, opaque to callers
public (int, string) GetUserSummary(int userId) { ... }

var summary = GetUserSummary(42);
var id = summary.Item1;    // What is Item1?
var email = summary.Item2; // What is Item2?
```

For complex return values, prefer a dedicated `record` or class over a tuple — tuples are for lightweight, local use only.
