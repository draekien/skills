---
paths:
  - "**/*.cs"
---

# Sealed Classes

Mark classes `sealed` by default. Only remove `sealed` when the type is explicitly designed for inheritance — not just because inheritance is theoretically possible.

```csharp
// prefer — sealed by default
public sealed class EmailService : IEmailService
{
    public async Task SendAsync(string to, string subject, string body) { ... }
}

// prefer — abstract base when inheritance IS the design
public abstract class NotificationService
{
    public abstract Task SendAsync(Notification notification);

    protected void LogSent(Notification notification) { ... }
}

public sealed class EmailNotificationService : NotificationService
{
    public override async Task SendAsync(Notification notification) { ... }
}

// avoid — unsealed with no inheritance intent
public class EmailService : IEmailService
{
    public virtual async Task SendAsync(string to, string subject, string body) { ... }
}
```

Sealing a class signals to the compiler and to callers that the type is complete. It enables devirtualisation optimisations and prevents unexpected subclass behaviour. Use interfaces for contracts; sealed classes for implementations.
