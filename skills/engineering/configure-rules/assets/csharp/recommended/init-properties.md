# Init-Only Properties

Prefer `init` over `set` for properties on types that should not change after construction. This enforces immutability at compile time without requiring a custom constructor for each combination of fields.

```csharp
// prefer — init-only, settable via object initialiser, immutable after
public class CreateOrderRequest
{
    public required string CustomerId { get; init; }
    public required IReadOnlyList<OrderLine> Lines { get; init; }
    public string? PromoCode { get; init; }
}

var request = new CreateOrderRequest
{
    CustomerId = "CUST-42",
    Lines = [new OrderLine("SKU-1", 2)],
};

// avoid — fully mutable, any code can reassign after construction
public class CreateOrderRequest
{
    public string CustomerId { get; set; }
    public List<OrderLine> Lines { get; set; }
    public string? PromoCode { get; set; }
}
```

Combine `init` with `required` (C# 11+) to eliminate the need for a custom constructor while still ensuring essential properties are provided at construction time.
