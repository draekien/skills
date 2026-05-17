# Explicit Access Modifiers

Always write access modifiers explicitly. Never rely on implicit defaults (`internal` for top-level types, `private` for members).

```csharp
// prefer
public class OrderService
{
    private readonly IOrderRepository _repo;
    private readonly ILogger<OrderService> _logger;

    public OrderService(IOrderRepository repo, ILogger<OrderService> logger)
    {
        _repo = repo;
        _logger = logger;
    }

    public async Task<Order> GetOrderAsync(int id) => await _repo.FindAsync(id);

    private void LogError(string message) => _logger.LogError(message);
}

// avoid — implicit private/internal, intent unclear
class OrderService
{
    readonly IOrderRepository _repo;

    OrderService(IOrderRepository repo) { _repo = repo; }

    async Task<Order> GetOrderAsync(int id) => await _repo.FindAsync(id);
}
```

Apply to classes, structs, interfaces, enums, records, methods, properties, fields, and constructors.
