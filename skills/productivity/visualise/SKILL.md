---
name: visualise
description: Turns data, text, or structured content into a self-contained HTML visualisation, such as a chart or diagram. Use when you want something rendered visually rather than described in text.
argument-hint: "[data, file, or text to visualise] [optional output name]"
disable-model-invocation: true
---

Pick the most informative visual form for the input, generate a self-contained output file (no non-CDN external requests — approved CDN libraries are permitted), validate it, then report the output path.

If the input has no clear visual form, default to a formatted document layout (readable typography, structured sections) rather than forcing a chart. Never ask the user to clarify — a visualisation only has value if it appears quickly, and a clarifying question stalls that; pick the most informative form and proceed.

Write the output file to the directory containing the input data (or the project root if there is no input file), named `visualisation.html` by default. Use a descriptive slug (e.g. `sales-2025.html`) only when the user's input has an obvious subject or time period that would make the filename meaningfully more identifiable.

Apply the aesthetic and design thinking guidance in [references/design-thinking.md](references/design-thinking.md).

## Available scripts

- **`scripts/validate.py`** — Validates the output file for structure, self-containment, and typography issues.

## Validation loop

After writing the output file, run:

```bash
uv run scripts/validate.py <output-path>
```

If failures are reported, fix each `[FAIL]` item and re-run until the output is clean. Only present the output path to the user once validation passes with zero failures, with one exception: if three fix-and-rerun cycles have been completed and one or more failures still remain that cannot be resolved (e.g. styles injected by a CDN library), present the output path anyway, with a note listing the outstanding failures and why they could not be fixed.

Note: if Tailwind was used, a clean validator run does not cover its utility classes — re-check the Tailwind caveat in [references/design-thinking.md](references/design-thinking.md) before reporting.
