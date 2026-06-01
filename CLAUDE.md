# Skills Repository

Repo stores agent skills in buckets under `skills/`. Each bucket groups skills by domain.

## Buckets

- **drafting** — Writing/editing: emails, docs, reports.
- **engineering** — Dev tasks: code review, debugging, architecture, workflows.
- **personal** — Personal productivity: scheduling, decisions, organisation.
- **productivity** — Workplace productivity: summarisation, research, meeting prep, task management.
- **output-styles** — Tone and voice modes: communication style presets for different audiences and needs.

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

- The top-level `README.md` has one section per public bucket (`drafting/`, `engineering/`, `productivity/`, `output-styles/`): bucket blurb + a link to that bucket's `README.md`. It does NOT list individual skills.
- Each bucket `README.md` lists all its skills with one-line descriptions, skill names linked to `SKILL.md`. The bucket `README.md` is the single source of truth for a skill's one-liner — it is the only place that one-liner lives.
- Skills in `personal/` must not appear in any public README.

## Plugin manifest

`.claude-plugin/` has two files:

- `marketplace.json` — plugin entries per bucket + `everything` meta-plugin
- When skills change, bump both the affected bucket plugin entry and the `everything` entry. Once per feature branch max.

`marketplace.json` contains:

- One `everything` entry listing every public-facing skill path across all buckets. Keep in sync when adding/removing skills.
- One bucket entry per bucket with at least one skill; empty buckets omitted.

Adding new skill, update `marketplace.json`:

- Add skill path to `everything` plugin's `skills` array
- If bucket has entry, add path to its `skills` array
- If bucket has no entry, add new plugin entry: `name: "<bucket>-skills"`, `source: "./"`, `strict: false`, `version: "0.1.0"`, `skills` array with skill path
- List individual skill paths (e.g. `"./skills/drafting/skill-writing"`), not whole bucket dirs
- `personal/` skills not public-facing — must not appear in any plugin entry

## Project Configuration Conventions

Skills that require per-project configuration use a shared dotfolder and config file:

- **`.draekien/` directory** — vendor-namespaced folder at the project root. See [specs/draekien.md](specs/draekien.md).
- **`.draekien/.skillsrc`** — JSON config file keyed by skill name. See [specs/skillsrc.md](specs/skillsrc.md). When writing a new skill that needs per-project config, register its keys in the Registered Keys table in that spec.

## Workflow

- New skill in this repo: vet the concept with `vet-skill-idea`, then author it with `skill-writing`.
- After adding a new skill: run `uv run tests/check-manifest.py` from repo root and fix any reported gaps before committing.
- Match skill body complexity to task complexity — if the agent already knows how to execute the task, one sentence beats a structured checklist.
