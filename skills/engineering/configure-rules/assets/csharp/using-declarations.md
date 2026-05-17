# Using Declarations

Prefer `using var` declarations (C# 8+) over `using (...) { }` statements for `IDisposable` resources. The declaration form disposes at the end of the enclosing scope, eliminating the extra nesting level.

```csharp
// prefer — using declaration, disposed at end of method
public async Task<string> ReadFileAsync(string path)
{
    using var stream = File.OpenRead(path);
    using var reader = new StreamReader(stream);
    return await reader.ReadToEndAsync();
}

// prefer — multiple resources, no nesting
public async Task CopyAsync(string src, string dst)
{
    using var input = File.OpenRead(src);
    using var output = File.OpenWrite(dst);
    await input.CopyToAsync(output);
}

// avoid — nested using statements
public async Task<string> ReadFileAsync(string path)
{
    using (var stream = File.OpenRead(path))
    {
        using (var reader = new StreamReader(stream))
        {
            return await reader.ReadToEndAsync();
        }
    }
}
```

Use the statement form `using (...) { }` only when the disposal scope must end before the surrounding method returns.
