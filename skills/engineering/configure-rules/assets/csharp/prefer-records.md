# Prefer Records for Data Types

Use `record` (C# 9+) for immutable data types — DTOs, request/response objects, value objects, and domain events. Use `class` for stateful, mutable services.

Records automatically generate structural equality, `ToString()`, deconstruction, and `with` expressions, eliminating boilerplate.

```csharp
// prefer — record for immutable data
public record UserDto(string Id, string Email, string DisplayName);

public record CreateOrderRequest(
    string CustomerId,
    IReadOnlyList<OrderLine> Lines,
    string? PromoCode = null);

// with-expression for non-destructive updates
var updated = original with { DisplayName = "New Name" };

// prefer — sealed record for leaf types
public sealed record OrderLine(string Sku, int Quantity, decimal UnitPrice);

// use class for services
public sealed class OrderService
{
    private readonly IOrderRepository _repo;

    public OrderService(IOrderRepository repo) { _repo = repo; }

    public async Task<Order> PlaceOrderAsync(CreateOrderRequest request) { ... }
}
```

Prefer `record` over `class` with `init`-only properties when the type carries no behaviour — records are the idiomatic choice for data holders in modern C#.
