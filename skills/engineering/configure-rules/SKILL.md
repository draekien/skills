---
name: configure-rules
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

## Workflow

1. **Pick topics and presets.** In Explore mode, scan signals; in Preset mode, take user input. For each topic, ask the user to choose `recommended` or `strict`.

2. **Offer optional rules.** List `.md` files directly under `assets/<topic>/` (not in a subdirectory) with a one-line description each. Allow at most one selection per mutually-exclusive group:
   - `typescript`: `prefer-interfaces` ⨯ `prefer-types`

3. **Check existing rules.** Read all files in the target repo's `.claude/rules/`. For each file that would be overwritten with different content, ask: overwrite, keep, or skip. Skip the check if the directory doesn't exist.

4. **Check tooling alignment.** For each selected topic, read its reference file for the expected config per preset, then read the corresponding config in the target repo (resolving any inheritance chain). For each expected setting that is absent or weaker, report it and ask whether to update the config, leave it, or note it for later. Skip the check if no config file exists.

   | Topic | Target config files |
   |-------|---------------------|
   | `typescript` | `tsconfig.json` (resolve `extends` chain) |
   | `csharp` | `.csproj`, `Directory.Build.props` (chain up to repo root) |
   | `react` | `eslint.config.*`, `.eslintrc.*`, `biome.json`, `.oxlintrc.json` |
   | `tanstack-query` | ESLint config; also confirm `@tanstack/eslint-plugin-query` is installed |
   | `tanstack-router` | ESLint config; also confirm `@tanstack/eslint-plugin-router` is installed and `routeTree.gen.ts` is in ignore files |

5. **Offer latest-practices search.** Ask whether to web-search `"<topic> best practices <current year>"` for rules not yet bundled. If yes, present candidates as a numbered list; each approved candidate becomes a new file under `.claude/rules/`.

6. **Write rules.** For each topic:
   - `recommended` writes every file in `assets/<topic>/recommended/`.
   - `strict` writes everything in `recommended/` plus `strict/`.
   - Selected optional rules write the corresponding standalone files.

   Target path is `.claude/rules/<filename>` — flat, no per-topic subdirectory. If an identical file already exists at the target, skip and report "already up to date". Create `.claude/rules/` if missing.

7. **Report.** Summarise files written, skipped (already up to date), and kept (user chose to keep existing).
