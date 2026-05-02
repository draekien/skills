# Skills Repository

This repository stores agent skills organised into buckets under `skills/`. Each bucket groups related skills by domain.

## Buckets

- **drafting** — Skills for writing and editing content: emails, documents, reports, and other written output.
- **engineering** — Skills for software development tasks: code review, debugging, architecture, and technical workflows.
- **personal** — Skills for personal productivity and life admin: scheduling, decision-making, and personal organisation.
- **productivity** — Skills for general workplace productivity: summarisation, research, meeting prep, and task management.

## Structure

Each skill is a directory containing a `SKILL.md` and optional bundled resources:

```
skills/
  <bucket>/
    <skill-name>/
      SKILL.md          ← required: YAML frontmatter + instructions
      scripts/          ← optional: executable scripts
      references/       ← optional: docs loaded into context as needed
      assets/           ← optional: templates, icons, other output files
```

## Conventions

- `SKILL.md` frontmatter must include `name` and `description` fields
- `description` controls when the skill triggers — write it to be specific and slightly "pushy" so Claude uses the skill when it should
- Keep `SKILL.md` under 500 lines; use `references/` for overflow content
