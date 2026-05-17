# Pattern Matching

Use `is` type patterns and `switch` expressions instead of `as` casts, `typeof` checks, or explicit casts. Prefer exhaustive switch expressions over chains of `if`/`else if`.

```csharp
// prefer — is pattern, no separate null check needed
if (shape is Circle circle)
{
    return Math.PI * circle.Radius * circle.Radius;
}

// prefer — switch expression
double area = shape switch
{
    Circle c    => Math.PI * c.Radius * c.Radius,
    Rectangle r => r.Width * r.Height,
    Triangle t  => 0.5 * t.Base * t.Height,
    _           => throw new ArgumentException($"Unknown shape: {shape.GetType().Name}"),
};

// prefer — property pattern
if (order is { Status: OrderStatus.Pending, Total: > 1000 })
{
    ApplyDiscount(order);
}

// avoid — as + null check
var circle = shape as Circle;
if (circle != null)
{
    return Math.PI * circle.Radius * circle.Radius;
}

// avoid — explicit cast
if (shape is Circle)
{
    var circle = (Circle)shape;
}
```

Use logical pattern combinators (`not`, `and`, `or`) to compose conditions inline rather than nesting `if` blocks.
