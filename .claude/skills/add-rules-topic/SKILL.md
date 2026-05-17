---
name: add-rules-topic
description: Adds a new topic's rule set to the configure-rules skill at skills/engineering/configure-rules. Researches best practices via web search, proposes rules across three tiers, writes asset files, and updates SKILL.md and references. Use when adding new language or framework rules, or when the user says "add [topic] rules", "add react rules", "add python rules", "extend configure-rules with [topic]".
---

Operates on the `skills/engineering/configure-rules/` skill in this repository. New topics follow this layout:

```
assets/<topic>/
  recommended/      # baseline — written for every project using this preset
  strict/           # additive — written alongside recommended when strict is selected
  *.md              # optional standalone rules — user selects individually
references/<topic>.md  # tooling alignment reference for discrepancy detection
```

## Workflow

### 1. Research

Search the web for `"<topic> best practices <current year>"` and `"<topic> code quality <current year>"`. Synthesise findings alongside training knowledge. Identify candidate rules, then classify each by tier.

### 2. Propose

Present the proposed rules categorised as:

- **Recommended** — rules every project should follow; baseline quality
- **Strict** — additive rules for projects wanting maximum rigour
- **Optional** — rules with valid competing alternatives; user picks one per mutually-exclusive group

For each rule: one-line description + reasoning for its tier placement. Get user approval before writing any files.

### 3. Write asset files

For each approved rule, create the corresponding `.md` file:

- `assets/<topic>/recommended/<rule-name>.md`
- `assets/<topic>/strict/<rule-name>.md`
- `assets/<topic>/<rule-name>.md` (optional)

Rule file format — plain markdown, no frontmatter:

```markdown
# Rule Title

One-sentence purpose and the invariant it enforces.

​```<language>
// prefer
<good example>

// avoid
<bad example — explain why briefly as inline comment>
​```

Optional: one sentence on edge cases or exceptions.
```

See existing rules in `assets/csharp/` and `assets/typescript/` for examples.

### 4. Write references/<topic>.md

Maps preset levels to expected tooling config (linter rules, compiler flags, config file settings). Used by the discrepancy detection step when configure-rules runs in a target repo. Follows the format of `references/typescript.md` and `references/csharp.md`.

Omit this file if the topic has no associated tooling config (e.g., a pattern-only rule set).

### 5. Update SKILL.md

Two additions to `skills/engineering/configure-rules/SKILL.md`:

**Explore Mode detection** — add a signal under the scan list:
```
- <file signals that indicate this topic> → `<topic>`
```

**Discrepancy Detection** — if a `references/<topic>.md` was written, add an alignment check section after the existing checks:

```markdown
### <config file> alignment

Read `references/<topic>.md` for the expected settings per preset. Read the target repo's <config file> and any parent config files in the directory chain. For each expected setting absent or set to a conflicting value:

- Report the setting, expected value, and actual value (or "not set").
- Ask whether to update the file, leave it as-is, or note it for later.

If no <config file> exists, skip this check.
```

### 6. Validate

```
uv run skills/drafting/skill-writing/scripts/validate.py skills/engineering/configure-rules
```

Fix any failures before confirming.
