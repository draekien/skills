---
paths:
  - "**/*.cs"
---

# No Null-Forgiving Operator

Never use the null-forgiving operator `!` to suppress nullable warnings. If it is needed, the design has a nullability problem — fix the root cause.

```csharp
// avoid
public void Process(string? input)
{
    var upper = input!.ToUpper(); // hides potential NullReferenceException
}

// prefer — guard and return or throw
public void Process(string? input)
{
    if (input is null) throw new ArgumentNullException(nameof(input));
    var upper = input.ToUpper();
}

// prefer — propagate nullability
public string? Process(string? input) => input?.ToUpper();

// avoid — suppressed warning during deserialization
public class Config
{
    public string ConnectionString { get; set; } = null!;
}

// prefer — required forces initialisation at construction
public class Config
{
    public required string ConnectionString { get; init; }
}
```

The only acceptable use of `!` is when an external API or framework guarantees non-null at a point the compiler cannot verify, and a comment explains why. Treat every `!` as a code smell requiring justification.
