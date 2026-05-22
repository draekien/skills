---
name: configure-claude-rules
description: Writes AI behaviour rules into a repository's `.claude/rules/` directory from a curated, topic-organised rule library. Detects the repo's technology stack and recommends rule sets, or accepts explicit topic and preset selection. Use when setting up AI coding rules for a repository, enforcing coding standards, or when the user says "configure rules", "set up claude rules", "add typescript rules", "set up AI rules", "add coding rules".
---

Writes `.claude/rules/` files from bundled assets in `assets/<topic>/`. See [references/writing-rules.md](references/writing-rules.md) for rule file format and path scoping.

## Modes

- **Explore** — no arguments, or user says "explore" / "detect". Scan the repo for signals and recommend topics.
- **Preset** — user names a topic and/or preset. Confirm any missing piece, then proceed.

## Topics

| Topic | Detection signals | Reference |
|-------|-------------------|-----------|
| `typescript` | `tsconfig.json` or `.ts` / `.tsx` files | [references/typescript.md](references/typescript.md) |
| `csharp` | `.csproj`, `.sln`, `global.json`, or `.cs` files | [references/csharp.md](references/csharp.md) |
| `react` | `react` in `package.json` dependencies | [references/react.md](references/react.md) |
| `tanstack-query` | `@tanstack/react-query` or `@tanstack/query-core` in `package.json` dependencies | [references/tanstack-query.md](references/tanstack-query.md) |
| `tanstack-router` | `@tanstack/react-router` or `@tanstack/router` in `package.json` dependencies | [references/tanstack-router.md](references/tanstack-router.md) |
| `software-design` | any codebase | — |
| `tailwind` | `tailwindcss` in `package.json` dependencies, or `@import "tailwindcss"` in any CSS file | [references/tailwind.md](references/tailwind.md) |

> **Permission mode:** This skill writes to `.claude/rules/`, a protected path. In `auto` mode the classifier may block these writes, causing the skill to fail. Run in `default` or `acceptEdits` mode so writes can be approved as they are requested.

## Available scripts

- **`scripts/detect-topics.py`** — Scans repo signals and outputs detected topics as JSON.
- **`scripts/check-rules.py`** — Compares source rule files against target directory; reports `new`, `modified`, or `identical` per file.
- **`scripts/write-rules.py`** — Copies selected rule files into the target rules directory.

## Workflow

1. **Pick topics and presets.** In Explore mode, run `uv run scripts/detect-topics.py <target-dir>` to detect topics from the repo's signals and present the results to the user. In Preset mode, take user input directly. For each topic, ask the user to choose `recommended` or `strict`.

2. **Offer optional rules.** List `.md` files directly under `assets/<topic>/` (not in a subdirectory) with a one-line description each. Allow at most one selection per mutually-exclusive group:
   - `typescript`: `prefer-interfaces` ⨯ `prefer-types`

3. **Check existing rules.** Resolve the full list of source files for the selected topics and presets. If `.claude/rules/` exists, run the check script (path relative to skill root):

   ```
   uv run scripts/check-rules.py --target <target-rules-dir> <source-file> [...]
   ```

   Files with status `identical` are automatically skipped. For each file with status `modified`, present the filename and ask: overwrite or keep? Build the final write list from all `new` files plus any `modified` files the user approved.

4. **Check tooling alignment.** For each selected topic, read its reference file for the expected config per preset, then read the corresponding config in the target repo (resolving any inheritance chain). For each expected setting that is absent or weaker, report it and ask whether to update the config, leave it, or note it for later. Skip the check if no config file exists.

   | Topic | Target config files |
   |-------|---------------------|
   | `typescript` | `tsconfig.json` (resolve `extends` chain) |
   | `csharp` | `.csproj`, `Directory.Build.props` (chain up to repo root) |
   | `react` | `eslint.config.*`, `.eslintrc.*`, `biome.json`, `.oxlintrc.json` |
   | `tanstack-query` | ESLint config; also confirm `@tanstack/eslint-plugin-query` is installed |
   | `tanstack-router` | ESLint config; also confirm `@tanstack/eslint-plugin-router` is installed and `routeTree.gen.ts` is in ignore files |
   | `tailwind` | `package.json` (check `class-variance-authority`, `clsx`, `tailwind-merge`); `biome.json` (`css.parser.tailwindDirectives`); codebase (`cn` utility) |

5. **Offer latest-practices search.** Ask whether to web-search `"<topic> best practices <current year>"` for rules not yet bundled. If yes, present candidates as a numbered list; each approved candidate becomes a new file under `.claude/rules/`.

6. **Write rules.** Pass the final write list from step 3 to the write script:

   ```
   uv run scripts/write-rules.py --target <target-rules-dir> <source-file> [...]
   ```

   The script creates `.claude/rules/` if missing and copies each file flat (no per-topic subdirectory). Source tiers:
   - `recommended` → `assets/<topic>/recommended/`
   - `strict` → `assets/<topic>/recommended/` and `assets/<topic>/strict/`
   - Optional rules → `assets/<topic>/` (root, not a subdirectory)

7. **Report.** Summarise files written, skipped (already up to date), and kept (user chose to keep existing).
