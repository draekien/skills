# Python Tooling Alignment

Expected `pyproject.toml` settings per preset. Scripts using uv manage tooling config inline or via a shared `pyproject.toml` at the workspace root.

## Recommended

No tooling config is required at the recommended preset — ruff's default rule set (`E`, `F`) enforces PEP 8 style and catches common errors.

If `pyproject.toml` is present:

```toml
[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
```

- `E`/`F` — pycodestyle errors and pyflakes (ruff default)
- `I` — import ordering (replaces isort)
- `UP` — pyupgrade (modernises syntax)
- `B` — flake8-bugbear (common pitfalls including mutable defaults)

## Strict

All recommended settings, plus mypy strict mode:

```toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "C4", "TCH"]
```

Additional rule sets:

- `SIM` — flake8-simplify (removes redundant code)
- `C4` — flake8-comprehensions (idiomatic comprehensions)
- `TCH` — type-checking imports (moves type-only imports into `TYPE_CHECKING` block)

## Notes

Scripts run with `uv run` do not require a `pyproject.toml`. Tool config can live in a shared workspace `pyproject.toml` or be omitted entirely for one-off scripts. When reporting discrepancies, note whether config is absent (no file) or misconfigured (file exists but setting differs).
