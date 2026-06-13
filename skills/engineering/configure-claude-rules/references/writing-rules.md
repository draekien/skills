# Writing `.claude/rules/` Files

Source: <https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/>

## What rules are

Markdown files placed in a project's `.claude/rules/` directory. Each file should cover one topic with a descriptive filename (e.g. `testing.md`, `api-design.md`). All `.md` files are discovered recursively, so subdirectories like `frontend/` or `backend/` are valid.

Rules without `paths` frontmatter are loaded at the start of every session, with the same priority as `.claude/CLAUDE.md`. Rules with `paths` frontmatter only load when Claude reads a file matching the pattern — they never load unconditionally.

## File format

Plain markdown. Optionally include YAML frontmatter with a `paths` field to scope the rule to specific files:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
```

Rules without a `paths` field apply to all files and load at launch.

## Path patterns

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files in any directory |
| `src/**/*` | All files under `src/` |
| `*.md` | Markdown files in the project root |
| `src/components/*.tsx` | React components in a specific directory |

Multiple patterns and brace expansion are supported:

```markdown
---
paths:
  - "src/**/*.{ts,tsx}"
  - "tests/**/*.test.ts"
---
```

## Writing effective rules

- Target under 200 lines per file. Longer files consume more context and reduce adherence.
- Use markdown headers and bullets. Structured sections are easier to follow than dense paragraphs.
- Be specific enough to verify: "Use 2-space indentation" not "format code properly".
- One topic per file. If a rule only applies to certain file types, use `paths` frontmatter so it doesn't load unconditionally.
- Avoid conflicting instructions across files. If two rules give different guidance for the same behaviour, the model may pick one arbitrarily.

## Scoping guidance

- Rules that apply to the whole codebase (e.g. `no-any.md`) → no `paths` frontmatter, load unconditionally.
- Rules that apply only to certain file types (e.g. React-specific rules) → scope with `paths: ["**/*.tsx"]`.
- For instructions that must run at a specific lifecycle point (e.g. before every commit), use hooks instead — rules are context, not enforcement.
