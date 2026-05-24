---
paths:
  - "**/*.py"
---

# PEP 723 Inline Script Metadata

Every uv script must open with a `# /// script` block declaring `requires-python` and any third-party `dependencies`. Without it, `uv run` cannot install dependencies and silently falls back to the ambient environment.

```python
# prefer
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx", "rich"]
# ///

import httpx
from rich import print

# avoid — no metadata block; uv cannot manage dependencies
import httpx
```

Omit the `dependencies` key only when the script has no third-party imports.
