---
name: visualise
description: Takes user-supplied input and produces a self-contained HTML file that visualises it. Use when the user wants to see data, text, or structured content rendered visually, or when the user says "visualise this", "show me a chart", "make a diagram", "render this as HTML".
---

Pick the most informative visual form for the input, generate a self-contained HTML file (no non-CDN external requests — approved CDN libraries are permitted), validate it, then report the full path.

If the input has no clear visual form, default to a formatted document layout (readable typography, structured sections) rather than forcing a chart. Never ask the user to clarify — pick the most informative form and proceed.

Write the output file to the user's current working directory, named `visualisation.html` (or a descriptive slug, e.g. `sales-2025.html`).

Apply the aesthetic and design thinking guidance in [references/design-thinking.md](references/design-thinking.md).

## Available scripts

- **`scripts/validate.py`** — Validates the generated HTML for structure, self-containment, and typography issues.

## Validation loop

After writing the HTML file, run:

```bash
uv run scripts/validate.py <output-path>
```

If failures are reported, fix each `[FAIL]` item and re-run until the output is clean. Only present the file path to the user once validation passes with zero failures.

Note: the font-size check only covers explicit values in `<style>` blocks — Tailwind utility classes (e.g. `text-sm`) are not statically analysable and must be reviewed manually if used.
