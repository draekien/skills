# Expression-Bodied Members

Use expression bodies (`=>`) for simple single-expression members: read-only properties, simple methods, and constructors that only assign. Keep expression bodies to one line. Use block bodies for anything that requires multiple statements or branching.

```csharp
// prefer — expression body for simple computed property
public string FullName => $"{FirstName} {LastName}";
public bool IsAdult => Age >= 18;

// prefer — expression body for simple method
public override string ToString() => $"User({Id}, {Email})";

// prefer — block body for multi-step logic
public decimal CalculateTotal()
{
    var subtotal = Lines.Sum(l => l.UnitPrice * l.Quantity);
    var discount = PromoCode is not null ? ApplyPromo(PromoCode, subtotal) : 0;
    return subtotal - discount;
}

// avoid — expression body forced onto complex logic
public decimal CalculateTotal() =>
    Lines.Sum(l => l.UnitPrice * l.Quantity) -
        (PromoCode is not null ? ApplyPromo(PromoCode, Lines.Sum(l => l.UnitPrice * l.Quantity)) : 0);
```
