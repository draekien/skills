---
paths:
  - "**/*.py"
---

# Main Guard

Protect script entry with `if __name__ == "__main__":` and delegate to a `main()` function. This keeps the module importable and its logic independently testable.

```python
# prefer
def main() -> None:
    run()

if __name__ == "__main__":
    main()

# avoid — top-level execution runs on import, blocking tests and imports
run()
```

`uv run script.py` sets `__name__` to `"__main__"`, so this pattern integrates cleanly with the uv execution model.
