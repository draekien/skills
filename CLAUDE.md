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

- Every skill in `drafting/`, `engineering/`, or `productivity/` must have a reference in the top-level `README.md`. Skills in `personal/` must not appear in either.
- Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.
- Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`.

## Plugin manifest

The `.claude-plugin/` directory contains two files:

- `marketplace.json` — lists one plugin entry per bucket that has at least one skill; empty buckets are omitted
- update the version of the plugin entry when skills are changed in that bucket, at most once per feature branch.

When adding a new skill, update `marketplace.json` as follows:

- If the bucket already has a plugin entry, add the new skill path to its `skills` array
- If the bucket has no entry yet, add a new plugin entry with `name: "<bucket>-skills"`, `source: "./"`, `strict: false`, `version: "0.1.0"`, and a `skills` array listing the skill path
- List individual skill paths (e.g. `"./skills/drafting/skill-writing"`), not whole bucket directories

## Workflow

- When a user wants to create a new skill in this repository, use the `skill-creator` skill from this repository.
