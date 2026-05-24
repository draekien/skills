---
paths:
  - "**/*.py"
---

# Pathlib Over os.path

Use `pathlib.Path` for all file system operations instead of `os.path` string manipulation. Path objects compose with `/`, carry their own read/write methods, and avoid common string-join errors.

```python
# prefer
from pathlib import Path

output = Path("data") / "results.json"
output.write_text(json.dumps(results))

# avoid
import os

output = os.path.join("data", "results.json")
with open(output, "w") as f:
    f.write(json.dumps(results))
```

`Path.glob()`, `Path.iterdir()`, and `Path.stat()` cover the remaining common `os` use cases.
