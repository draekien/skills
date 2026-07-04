---
paths:
  - "**/*.py"
---

# No Bare Except

Never use bare `except:`. It silently catches `KeyboardInterrupt`, `SystemExit`, and `GeneratorExit` — signals that are meant to terminate the process. Catch specific exception types only, and always re-raise or log with context.

```python
# prefer
try:
    response = httpx.get(url)
except httpx.TimeoutException as exc:
    logger.error("Request timed out: %s", exc)
    raise

# avoid — catches Ctrl-C and sys.exit()
try:
    response = httpx.get(url)
except:
    pass
```

`except Exception` is acceptable only at a top-level error boundary where you log and exit; never use it to silently continue.
