---
paths:
  - "**/*.py"
---

# Strict Type Checking

Enable mypy `strict = true` in `pyproject.toml`. Strict mode disallows implicit `Any`, requires explicit generics, and enforces return type annotations on all functions.

```python
# prefer — explicit generic, return type annotated
def first(items: list[str]) -> str | None:
    return items[0] if items else None

# avoid — implicit Any, missing return type
def first(items):
    return items[0] if items else None
```

For existing scripts, use `# type: ignore[<code>]` as a temporary escape hatch and track each suppression for removal.
