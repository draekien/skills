---
paths:
  - "**/*.py"
---

# Type Hints

Annotate every function parameter and return type. Type hints serve as inline documentation and enable static type checkers to catch errors before runtime.

```python
# prefer
def fetch(url: str, timeout: float = 10.0) -> bytes:
    ...

# avoid — no annotations; caller has no contract to rely on
def fetch(url, timeout=10.0):
    ...
```

Use `from __future__ import annotations` at the top of the file to enable forward references without runtime cost.
