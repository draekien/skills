# File-Scoped Namespaces

Use file-scoped namespace declarations (C# 10+). Place the namespace at the top of the file followed by a semicolon, with no enclosing braces. One type per file.

```csharp
// prefer
namespace MyApp.Services;

public sealed class UserService
{
    public async Task<User> GetUserAsync(int id) { ... }
}

// avoid — block-scoped, extra indentation level
namespace MyApp.Services
{
    public sealed class UserService
    {
        public async Task<User> GetUserAsync(int id) { ... }
    }
}
```

File-scoped namespaces reduce indentation by one level across the entire file. Combined with one-type-per-file, this keeps file contents at the left margin and eliminates the visual nesting that adds no information.
