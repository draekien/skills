---
paths:
  - "**/*.py"
---

# F-Strings

Use f-strings for all string interpolation. They are more readable than `%`-formatting and `.format()`, and expressions are evaluated at compile time.

```python
# prefer
msg = f"Hello, {name}!"

# avoid — older formatting styles
msg = "Hello, %s!" % name
msg = "Hello, {}!".format(name)
```

Exception: use `%`-style lazy formatting with the `logging` module (`logger.info("Hello, %s", name)`) to avoid constructing the string when the log level is filtered out.
