---
paths:
  - "**/*.py"
---

# Click for CLI Argument Parsing

Use `click` for command-line interfaces. Decorator-based definitions keep argument declarations co-located with their handlers, and `click` handles help text, type coercion, and error messages automatically.

```python
# prefer
import click

@click.command()
@click.argument("url")
@click.option("--timeout", default=10.0, help="Request timeout in seconds.")
def main(url: str, timeout: float) -> None:
    fetch(url, timeout)

if __name__ == "__main__":
    main()
```

Declare `click` in the `# /// script` dependencies block. Mutually exclusive with `typer-cli`.
