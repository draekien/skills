# Skills Repository

Repo stores agent skills in buckets under `skills/`. Each bucket groups skills by domain.

## Buckets

- **drafting** — Writing/editing: emails, docs, reports.
- **planning** — Turning an idea into a spec, and a spec into pickup-ready work.
- **software-design** — Designing code and the vocabulary it is built on, from a method to an architectural layer.
- **quality** — Making work hold up: stress-testing a change, and testing it so the tests can fail.
- **technical-writing** — Developer-facing writing: the documentation that ships with the code.
- **version-control** — Git hygiene and repository workflow.
- **engineering** — Retired. Redirect stubs only; do NOT add new skills here. Its README maps each stub to its new bucket.
- **context-management** — Building and managing agent context: the docs and reference indexes an agent reads before touching code.
- **personal** — Personal productivity: scheduling, decisions, organisation.
- **productivity** — Workplace productivity: summarisation, research, meeting prep, task management.
- **problem-solving** — Working through a hard problem or decision: reasoning from fundamentals, debating between options.
- **teaching** — Explanation and comprehension: making an idea land, and repairing it when it does not.
- **roles** — Fixed-persona skills: advocate, listener, critic stances used to sharpen thinking.
- **ui-ux** — User interface and experience design: dashboards, visual design, usability.
- **output-styles** — Tone and voice modes: communication style presets for different audiences and needs. Each one is a native Claude Code output style (`<skill-name>.md`) with a `SKILL.md` wrapper. See [Output styles](#output-styles).
- **meta** — Meta-skills: skills about authoring, vetting, and evaluating skills themselves.
- **archived** — Retired skills kept for reference. Must NOT be indexed or promoted in any README.md, and must NEVER be registered in `marketplace.json` (no bucket entry, no `everything` entry).

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

- The top-level `README.md` has one section per public bucket (`drafting/`, `planning/`, `software-design/`, `quality/`, `technical-writing/`, `version-control/`, `context-management/`, `productivity/`, `problem-solving/`, `teaching/`, `roles/`, `ui-ux/`, `output-styles/`, plus the retired `engineering/`): bucket blurb + a link to that bucket's `README.md`. It does NOT list individual skills.
- Each bucket `README.md` lists all its skills with one-line descriptions, skill names linked to `SKILL.md`. The bucket `README.md` is the single source of truth for a skill's one-liner — it is the only place that one-liner lives.
- Skills in `personal/` must not appear in any public README.

## Output styles

Skills in `output-styles/` work both ways. `<skill-name>.md` holds the instructions as a [native output style](https://code.claude.com/docs/en/output-styles) selectable from `/config`; `SKILL.md` sits beside it as a thin wrapper so the same style is still invokable as a skill:

```
skills/output-styles/
  cte-mode/
    cte-mode.md        native output style — the instructions live here
    SKILL.md           wrapper: reads cte-mode.md, adds session framing
```

- The instructions live in the native file only. `SKILL.md` tells the agent to read its sibling and adopt it, plus the session framing an output style cannot express — that the style holds until the user asks to stop.
- Native frontmatter: `name` matching the directory, the same `description` as the skill, and `keep-coding-instructions: true`. Do not set `force-for-plugin`.
- The files are never placed in a root `output-styles/` directory. Every plugin entry uses `source: "./"`, so that directory would auto-load into all bucket plugins.

## Plugin manifest

`.claude-plugin/marketplace.json` contains:

- One `everything` entry listing every public-facing skill path across all buckets.
- One bucket entry per bucket with at least one skill; empty buckets omitted.
- `personal/` skills live only in the `personal-skills` entry, never in `everything`.

Adding a new skill, update `marketplace.json`:

- Add the skill path to its bucket entry. If the bucket has no entry, add one: `name: "<bucket>-skills"`, `source: "./"`, `strict: false`, `version: "0.1.0"`, `skills` array with the path.
- Also add the path to the `everything` entry — except `personal/` skills, which stay out of `everything`.
- List individual skill paths (e.g. `"./skills/meta/writing-skills"`), not whole bucket dirs.
- When skills change, bump the affected bucket entry and (for public skills) the `everything` entry. Once per feature branch max.
- Output style skills also need their native `.md` path in the `outputStyles` array on both the `output-styles` and `everything` entries. List explicit file paths, never a directory.
- Skills that ship a hook keep only the handler script inside the skill directory (`hooks/<handler>.sh`) and declare the `hooks` object in `marketplace.json` — in both the bucket entry and `everything`. `marketplace.json` is the single source of truth for hook registration. A marketplace entry only accepts the inline object form (event name -> matcher array); a file path or array of paths fails to load. Never add a `hooks/hooks.json` anywhere in the repo: every entry sets `strict: false`, which makes the marketplace entry the plugin's entire definition, so any auto-discovered `hooks.json` is a conflicting manifest and the plugin fails to load.

## Project Configuration Conventions

Skills that require per-project configuration use a shared dotfolder and config file:

- **`.draekien/` directory** — vendor-namespaced folder at the project root. See [specs/draekien.md](specs/draekien.md).
- **`.draekien/.skillsrc`** — JSON config file keyed by skill name. See [specs/skillsrc.md](specs/skillsrc.md). When writing a new skill that needs per-project config, register its keys in the Registered Keys table in that spec.

## Workflow

- New skill in this repo: author it with `writing-skills`.
- After adding a new skill: run `uv run tests/check-manifest.py` from repo root and fix any reported gaps before committing.
- After touching anything in `output-styles/`: also run `uv run tests/check-output-styles.py` from repo root.
- After changing the plain-language linter or its dictionary: also run `uv run tests/check-linter.py` from repo root.
- After editing any markdown: run `npx markdownlint-cli2 --fix "**/*.md"` from repo root (auto-discovers `.markdownlint-cli2.jsonc`), then review the autofixed diff and resolve any remaining reported errors before committing.
- A skill that references another skill by name must say how to install it: the plugin that ships it and the `npx skills add` route. Never reimplement the referenced skill as a fallback. Authoring rule lives in `writing-skills` under Craft.
- Match skill body complexity to task complexity — if the agent already knows how to execute the task, one sentence beats a structured checklist.
