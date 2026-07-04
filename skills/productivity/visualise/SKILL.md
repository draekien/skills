---
name: visualise
description: Turns data, text, or structured content into a self-contained HTML visualisation, such as a chart or diagram. Use when you want something rendered visually rather than described in text.
disable-model-invocation: true
---

Pick the most informative visual form for the input, generate a self-contained HTML file (no non-CDN external requests — approved CDN libraries are permitted), validate it, then report the full path.

If the input has no clear visual form, default to a formatted document layout (readable typography, structured sections) rather than forcing a chart. Never ask the user to clarify — pick the most informative form and proceed.

Write the output file to the directory containing the input data (or the project root if there is no input file), named `visualisation.html` by default. Use a descriptive slug (e.g. `sales-2025.html`) only when the user's input has an obvious subject or time period that would make the filename meaningfully more identifiable.

Apply the aesthetic and design thinking guidance in [references/design-thinking.md](references/design-thinking.md).

## Available scripts

- **`scripts/validate.py`** — Validates the generated HTML for structure, self-containment, and typography issues.

## Validation loop

After writing the HTML file, run:

```bash
uv run scripts/validate.py <output-path>
```

If failures are reported, fix each `[FAIL]` item and re-run until the output is clean. Only present the file path to the user once validation passes with zero failures. If after three fix-and-rerun cycles one or more failures remain that cannot be resolved (e.g. styles injected by a CDN library), present the file path with a note listing the outstanding failures and why they could not be fixed.

Note: the font-size check only covers explicit values in `<style>` blocks — Tailwind utility classes (e.g. `text-sm`) are not statically analysable and must be reviewed manually if used.
