# Required Members

Use the `required` modifier (C# 11+) on properties that must be set at object initialisation. This makes the compiler enforce that no caller can create a partially-initialised object.

```csharp
// prefer — compiler enforces all required properties are set
public class CreateUserRequest
{
    public required string Email { get; init; }
    public required string DisplayName { get; init; }
    public string? PhoneNumber { get; init; }
}

var request = new CreateUserRequest
{
    Email = "alice@example.com",
    DisplayName = "Alice",
}; // valid

var bad = new CreateUserRequest(); // CS9035 — required members not set

// avoid — settable but not required; partially constructed objects silently compile
public class CreateUserRequest
{
    public string Email { get; set; }
    public string DisplayName { get; set; }
    public string? PhoneNumber { get; set; }
}

var bad = new CreateUserRequest(); // compiles; Email and DisplayName are null
```

Combine `required` with `init` for data types: `required` guarantees presence at construction, `init` prevents mutation afterwards.
