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

- Every skill in `drafting/`, `engineering/`, or `productivity/` must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`. Skills in `personal/` must not appear in either.
- Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.
- Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`.

## Workflow

- When a user wants to create a new skill in this repository, use the `skill-creator` skill from this repository.
