# Skills Repository

Repo stores agent skills in buckets under `skills/`. Each bucket groups skills by domain.

## Buckets

- **drafting** — Writing/editing: emails, docs, reports.
- **planning** — Turning an idea into a spec, and a spec into pickup-ready work.
- **software-design** — Designing code and the vocabulary it is built on, from a method to an architectural layer.
- **quality** — Making work hold up: stress-testing a change, and testing it so the tests can fail.
- **technical-writing** — Developer-facing writing: the documentation that ships with the code.
- **version-control** — Git hygiene and repository workflow.
- **context-management** — Building and managing agent context: the docs and reference indexes an agent reads before touching code.
- **personal** — Personal productivity: scheduling, decisions, organisation.
- **productivity** — Workplace productivity: summarisation, research, meeting prep, task management.
- **problem-solving** — Working through a hard problem or decision: reasoning from fundamentals, debating between options.
- **teaching** — Explanation and comprehension: making an idea land, and repairing it when it does not.
- **roles** — Fixed-persona skills: advocate, listener, critic stances used to sharpen thinking.
- **ui-ux** — User interface and experience design: dashboards, visual design, usability.
- **output-styles** — Tone and voice modes: communication style presets for different audiences and needs. Each one is a native Claude Code output style (`<skill-name>.md`) with a `SKILL.md` wrapper. See [Output styles](#output-styles).
- **agent-config** — Configuring the agent itself: standing rules and hooks that apply before any task begins.
- **meta** — Meta-skills: skills about authoring, vetting, and evaluating skills themselves.

## Structure

Each skill = directory with `SKILL.md` + optional bundled resources:

```
skills/
  <bucket>/
    .claude-plugin/
      plugin.json        required: the bucket's plugin manifest
    <skill-name>/
      SKILL.md           required: YAML frontmatter + instructions
      scripts/           optional: executable scripts
      references/        optional: docs loaded into context as needed
      assets/            optional: templates, icons, other output files
```

Each bucket is a plugin, and the bucket directory is its plugin root. See [Plugin manifest](#plugin-manifest).

- The top-level `README.md` has one section per public bucket (`agent-config/`, `drafting/`, `planning/`, `software-design/`, `quality/`, `technical-writing/`, `version-control/`, `context-management/`, `productivity/`, `problem-solving/`, `teaching/`, `roles/`, `ui-ux/`, `output-styles/`): bucket blurb + a link to that bucket's `README.md`. It does NOT list individual skills.
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
- The files are never placed in a root `output-styles/` directory. Plugin roots are the bucket directories, so anything outside `skills/<bucket>/` is unreachable by every plugin.

## Plugin manifest

Every bucket holding at least one skill is a separate plugin, rooted at `skills/<bucket>/`. Two files declare it, and neither repeats the other:

- `.claude-plugin/marketplace.json` — one entry per bucket, two fields: `name` matching the `plugin.json` name, and `source` set to `./skills/<bucket>`. Nothing else. Claude Code reads the rest from `plugin.json` because the source is a relative path inside the marketplace. Empty buckets get no entry.
- `skills/<bucket>/.claude-plugin/plugin.json` — `name`, `version`, `description`, `author`, and `"skills": ["./"]`.

`"skills": ["./"]` is what loads the bucket's `<skill-name>/SKILL.md` children: the plugin root is the bucket, which has no nested `skills/` directory to auto-discover, and without the field the plugin loads zero skills. Write `"./"`, not `"."` — both mean the plugin root to Claude Code, but `npx skills` drops any path that does not start with `./`.

- Adding a skill to an existing bucket needs no manifest edit at all.
- Adding a bucket needs one marketplace entry and one `plugin.json` at `version: "0.1.0"`.
- Bump the bucket's `plugin.json` version when its skills change. Once per feature branch max.
- Output style skills also need their native `.md` path in the bucket `plugin.json` `outputStyles` array, relative to the bucket root (`./<skill-name>/<skill-name>.md`). List explicit file paths, never a directory.
- Skills that ship a hook keep only the handler script inside the skill directory (`hooks/<handler>.sh`) and declare the `hooks` object in the bucket `plugin.json`, where `${CLAUDE_PLUGIN_ROOT}` is the bucket directory. Inline object form only (event name -> matcher array); a file path or array of paths fails to load. Never add a `hooks/hooks.json` anywhere in the repo — an auto-discovered second manifest conflicts with `plugin.json` and the plugin fails to load.
- `personal/` is a plugin like any other. It is kept out of the public READMEs, not out of the manifest.

## Project Configuration Conventions

Skills that require per-project configuration use a shared dotfolder and config file:

- **`.draekien/` directory** — vendor-namespaced folder at the project root. See [specs/draekien.md](specs/draekien.md).
- **`.draekien/.skillsrc`** — JSON config file keyed by skill name. See [specs/skillsrc.md](specs/skillsrc.md). When writing a new skill that needs per-project config, register its keys in the Registered Keys table in that spec.

## Python scripts

Scripts run on every platform, so they normalise their own text I/O rather than trusting the console codepage. Python otherwise decodes with the locale encoding — cp1252 on Windows — which cannot encode characters these scripts print routinely, and `print(f"{src} → {dst}")` dies with `UnicodeEncodeError`.

Every tracked `*.py` file therefore:

- reconfigures `sys.stdout` and `sys.stderr` to UTF-8 at import time, straight after the imports;
- passes `encoding="utf-8"` to every `open()`, `read_text()` and `write_text()`;
- passes `encoding="utf-8"` to every `subprocess` call that sets `text=True`.

`uv run tests/check-encoding.py` enforces all three. Running a script by hand on Windows, `PYTHONUTF8=1` additionally forces UTF-8 for any file opened without an explicit encoding.

## Workflow

- New skill in this repo: author it with `writing-skills`.
- After adding a new skill: run `uv run tests/check-manifest.py` from repo root and fix any reported gaps before committing.
- After touching anything in `output-styles/`: also run `uv run tests/check-output-styles.py` from repo root.
- After changing the plain-language linter or its dictionary: also run `uv run tests/check-linter.py` from repo root.
- After changing a shared script in `specs/` or copying one into a skill: run `uv run tests/check-shared-scripts.py` from repo root, and `--fix` to propagate an edit to every copy. Never symlink a shared script into a skill — symlinks do not survive checkout on Windows without Developer Mode; ship a real copy.
- After adding or editing any Python script: run `uv run tests/check-encoding.py` from repo root. See [Python scripts](#python-scripts).
- After editing any markdown: run `npx markdownlint-cli2 --fix "**/*.md"` from repo root (auto-discovers `.markdownlint-cli2.jsonc`), then review the autofixed diff and resolve any remaining reported errors before committing.
- A skill that references another skill by name must say how to install it: the plugin that ships it and the `npx skills add` route. Never reimplement the referenced skill as a fallback. Authoring rule lives in `writing-skills` under Craft.
- Match skill body complexity to task complexity — if the agent already knows how to execute the task, one sentence beats a structured checklist.
