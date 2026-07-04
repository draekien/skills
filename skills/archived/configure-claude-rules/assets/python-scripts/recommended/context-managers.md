---
paths:
  - "**/*.py"
---

# Context Managers

Use `with` statements for any resource that has a lifecycle: files, network connections, locks, and temporary state. The context manager guarantees cleanup even when an exception is raised.

```python
# prefer
with open("data.txt") as f:
    contents = f.read()

# avoid — file may not be closed if an exception occurs
f = open("data.txt")
contents = f.read()
f.close()
```

For resources without a built-in context manager, use `contextlib.contextmanager` or implement `__enter__` / `__exit__`.
