---
paths:
  - "**/*.py"
---

# Typer for CLI Argument Parsing

Use `typer` for command-line interfaces. Typer derives argument definitions from function type annotations — no decorator boilerplate, and it integrates naturally with the `type-hints` rule.

```python
# prefer
import typer

def main(url: str, timeout: float = 10.0) -> None:
    fetch(url, timeout)

if __name__ == "__main__":
    typer.run(main)
```

Declare `typer` in the `# /// script` dependencies block. Mutually exclusive with `click-cli`.
