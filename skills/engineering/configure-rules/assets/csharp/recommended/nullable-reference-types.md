---
paths:
  - "**/*.cs"
---

# Nullable Reference Types

Enable and enforce nullable reference types. All reference types are non-nullable by default. Use `?` to annotate types that can be null, and use `??`, null-conditional (`?.`), or explicit null-checks to handle nullable values safely. Never use the null-forgiving operator `!` without a comment explaining why it is safe.

```csharp
// prefer
public string? GetMiddleName(User user) => user.MiddleName;

public string GetDisplayName(User? user)
{
    if (user is null) return "Guest";
    return user.Name;
}

public string FormatName(User user) =>
    user.MiddleName is not null
        ? $"{user.FirstName} {user.MiddleName} {user.LastName}"
        : $"{user.FirstName} {user.LastName}";

// avoid — ignores nullability, hides potential NullReferenceException
public string GetDisplayName(User user)
{
    return user.Name.ToUpper(); // user or Name may be null
}
```

When the project `.csproj` does not yet have `<Nullable>enable</Nullable>`, add it rather than scattering `#nullable enable` directives.
