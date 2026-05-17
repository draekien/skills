# Exception Handling

Catch specific exception types. Never use a bare `catch {}` or catch `Exception` without a filter — these swallow unexpected failures and hide bugs.

Rethrow with `throw`, not `throw ex`. `throw ex` resets the stack trace; `throw` preserves it.

```csharp
// prefer — specific catch, preserve stack trace
try
{
    await _httpClient.GetAsync(url, cancellationToken);
}
catch (HttpRequestException ex)
{
    _logger.LogError(ex, "Network error fetching {Url}", url);
    throw;
}
catch (TaskCanceledException)
{
    _logger.LogWarning("Request to {Url} timed out", url);
    throw;
}

// avoid — swallows everything
try
{
    await _httpClient.GetAsync(url);
}
catch { }

// avoid — loses stack trace
try
{
    await _httpClient.GetAsync(url);
}
catch (Exception ex)
{
    throw ex; // stack trace reset
}
```

Throw `ArgumentException`/`ArgumentNullException` for invalid inputs. Throw `InvalidOperationException` for invalid state. Validate at method entry and throw immediately rather than propagating corrupt state.

Custom exception types should extend `Exception` and include a constructor that accepts a `message` and an inner `exception`.
