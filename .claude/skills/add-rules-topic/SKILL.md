---
name: add-rules-topic
description: Adds a new topic's rule set to the configure-claude-rules skill at skills/engineering/configure-claude-rules. Researches best practices via web search, proposes rules across three tiers, writes asset files, and updates SKILL.md and references. Use when adding new language or framework rules, or when the user says "add [topic] rules", "add react rules", "add python rules", "extend configure-claude-rules with [topic]".
---

Operates on `skills/engineering/configure-claude-rules/`. New topics follow this layout:

```
assets/<topic>/
  recommended/      baseline — written for every project using this preset
  strict/           additive — written alongside recommended when strict is selected
  *.md              optional standalone rules — user selects individually
references/<topic>.md   tooling alignment reference (omit if no tooling config)
```

## Workflow

### 1. Research

Web-search `"<topic> best practices <current year>"` and `"<topic> code quality <current year>"`. Synthesise findings with training knowledge into candidate rules.

### 2. Propose

Exclude any rule routinely enforced by the dominant linter for this topic — ESLint for JS/TS, Ruff for Python, Roslyn analysers for C#, etc. AI rules complement linters; they don't duplicate them. Rules linters can't enforce (architectural decisions, naming semantics, cross-cutting invariants, patterns requiring broader context) are the right candidates.

Present candidates in three tiers, each rule with a one-line description plus tier reasoning. Get approval before writing.

- **Recommended** — baseline quality; every project should follow.
- **Strict** — additive rigour for projects wanting maximum enforcement.
- **Optional** — valid competing alternatives; user picks one per mutually-exclusive group.

### 3. Write asset files

For each approved rule, create the file at the matching path:

- `assets/<topic>/recommended/<rule-name>.md`
- `assets/<topic>/strict/<rule-name>.md`
- `assets/<topic>/<rule-name>.md` (optional)

Rule file canonical layout — include `paths` frontmatter to scope the rule to the relevant file types:

```markdown
---
paths:
  - "<glob matching files where this rule applies>"
---

# Rule Title

One-sentence purpose and the invariant it enforces. Optionally one more sentence on reasoning.

​```<language>
// prefer
<good example>

// avoid — brief inline reason
<bad example>
​```

Optional: one closing sentence on edge cases or when the rule does not apply.
```

Common `paths` mappings by topic:
- TypeScript/TSX → `**/*.{ts,tsx}`
- React (JSX/components) → `**/*.{tsx,jsx}`
- C# → `**/*.cs`
- Python → `**/*.py`
- CSS/Tailwind → `**/*.{css,scss}`
- Config-only topic (no language match) → omit `paths` (loads unconditionally)

Match the conciseness of existing rules in `assets/typescript/` and `assets/csharp/`. Keep files under ~50 lines.

### 4. Write `references/<topic>.md`

Maps preset levels to expected tooling config (linter rules, compiler flags, project settings). Used by configure-claude-rules' tooling alignment check. For any rule category excluded from AI rules because linters cover it, list the equivalent linter rule or plugin here so the user knows where to configure it.

Keep this file **config-only**: the "for each rule absent, report and ask" procedure lives in `configure-claude-rules/SKILL.md` — do not duplicate it.

Sections: `## Recommended`, `## Strict`, and any topic-specific notes (language version requirements, extends-chain semantics, linter alternatives). Follow `references/typescript.md` and `references/react.md` for shape.

Omit this file entirely if the topic has no associated tooling config.

### 5. Update `configure-claude-rules/SKILL.md`

Two table edits, no new prose sections:

- **Topics table** — add one row: `\`<topic>\` | <detection signals> | [references/<topic>.md](references/<topic>.md)`. Omit the reference link if step 4 was skipped.
- **Workflow step 4 table** — if a reference was written, add one row mapping the topic to its target config files.

If the topic has mutually-exclusive optional rules, also add a bullet under workflow step 2.

### 6. Validate

```
uv run skills/drafting/skill-writing/scripts/validate.py skills/engineering/configure-claude-rules
```

Fix any failures before confirming.
