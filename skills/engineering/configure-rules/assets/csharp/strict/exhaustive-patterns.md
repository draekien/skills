# Exhaustive Pattern Matching

Switch expressions over discriminated types (unions, enums, sealed hierarchies) must handle all known cases explicitly. Include a `_ => throw new UnreachableException(...)` fallback so that any future variant addition causes a runtime failure at the unhandled branch rather than silently returning a default.

```csharp
// prefer — every known case explicit, unhandled case throws
double area = shape switch
{
    Circle c    => Math.PI * c.Radius * c.Radius,
    Rectangle r => r.Width * r.Height,
    Triangle t  => 0.5 * t.Base * t.Height,
    _ => throw new UnreachableException($"Unhandled shape type: {shape.GetType().Name}"),
};

// prefer — enum switch
string label = status switch
{
    OrderStatus.Pending   => "Awaiting payment",
    OrderStatus.Confirmed => "Processing",
    OrderStatus.Shipped   => "On the way",
    OrderStatus.Cancelled => "Cancelled",
    _ => throw new UnreachableException($"Unhandled status: {status}"),
};

// avoid — default returns a magic value, new variants silently fall through
double area = shape switch
{
    Circle c    => Math.PI * c.Radius * c.Radius,
    Rectangle r => r.Width * r.Height,
    _           => 0, // hides unhandled types
};
```

`UnreachableException` is in `System.Diagnostics` (.NET 7+). For earlier targets, throw `InvalidOperationException` with a descriptive message.
