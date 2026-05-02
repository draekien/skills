# Skills Repository

Repo stores agent skills in buckets under `skills/`. Each bucket groups skills by domain.

## Buckets

- **drafting** — Writing/editing: emails, docs, reports.
- **engineering** — Dev tasks: code review, debugging, architecture, workflows.
- **personal** — Personal productivity: scheduling, decisions, organisation.
- **productivity** — Workplace productivity: summarisation, research, meeting prep, task management.

## Structure

Each skill = directory with `SKILL.md` + optional bundled resources:

```
skills/
  <bucket>/
    <skill-name>/
      SKILL.md           required: YAML frontmatter + instructions
      scripts/           optional: executable scripts
      references/        optional: docs loaded into context as needed
      assets/            optional: templates, icons, other output files
```

- Every skill in `drafting/`, `engineering/`, `productivity/` needs entry in top-level `README.md`. Skills in `personal/` must not appear.
- Each top-level `README.md` entry links skill name to its `SKILL.md`.
- Each bucket has `README.md` listing all skills with one-line descriptions, names linked to `SKILL.md`.

## Plugin manifest

`.claude-plugin/` has two files:

- `marketplace.json` — plugin entries per bucket + `everything` meta-plugin
- Bump version of affected plugin entry when skills change in that bucket. Once per feature branch max.

`marketplace.json` contains:

- One `everything` entry listing every public-facing skill path across all buckets. Keep in sync when adding/removing skills.
- One bucket entry per bucket with at least one skill; empty buckets omitted.

Adding new skill, update `marketplace.json`:

- Add skill path to `everything` plugin's `skills` array
- If bucket has entry, add path to its `skills` array
- If bucket has no entry, add new plugin entry: `name: "<bucket>-skills"`, `source: "./"`, `strict: false`, `version: "0.1.0"`, `skills` array with skill path
- List individual skill paths (e.g. `"./skills/drafting/skill-writing"`), not whole bucket dirs
- `personal/` skills not public-facing — must not appear in any plugin entry

## Workflow

- New skill in this repo: use `skill-creator` skill
- After writing skill: use `compact` caveman skill on yaml `description` and skill contents.
