---
paths:
  - "**/*.py"
---

# No Mutable Default Arguments

Never use mutable objects (`[]`, `{}`, `set()`) as default argument values. The default object is created once at function definition time and shared across all calls.

```python
# prefer
def append_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items

# avoid — all callers share the same list instance
def append_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items
```
