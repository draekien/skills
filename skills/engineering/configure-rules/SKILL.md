---
name: configure-rules
description: Writes AI behaviour rules into a repository's `.claude/rules/` directory from a curated, topic-organised rule library. Detects the repo's technology stack and recommends rule sets, or accepts explicit topic and preset selection. Use when setting up AI coding rules for a repository, enforcing coding standards, or when the user says "configure rules", "set up claude rules", "add typescript rules", "set up AI rules", "add coding rules".
---

Writes `.claude/rules/` files from bundled rule assets. Available topics are discovered by listing subdirectories under `assets/` within this skill directory. See [references/writing-rules.md](references/writing-rules.md) for the official guidance on rule file format, path scoping, and writing effective rules.

## Mode Detection

| Signal | Mode |
|--------|------|
| No arguments, or user says "explore" / "detect" | **Explore** |
| User names a topic and/or preset explicitly | **Preset** |

---

## Explore Mode

1. Scan the target repository for technology signals:
   - `tsconfig.json` or `.ts`/`.tsx` files → `typescript`
   - `.csproj`, `.sln`, `global.json`, or `.cs` files → `csharp`
   - Add mappings here as new topics land in `assets/`

2. For each detected topic, present available presets (`recommended` | `strict`) and ask the user to select one.

3. Present optional standalone rules for the topic (any `.md` files directly under `assets/<topic>/`, not inside a subdirectory). Ask the user to select at most one per mutually-exclusive group.

   **Mutually exclusive groups:**
   - `prefer-interfaces` and `prefer-types` — pick one or neither

4. Run discrepancy checks (see **Discrepancy Detection** below).

5. Write rules (see **Writing Rules** below).

---

## Preset Mode

1. Confirm the topic and preset with the user if not fully specified.
2. Present optional standalone rules for the topic (same as Explore step 3).
3. Run discrepancy checks.
4. Write rules.

---

## Discrepancy Detection

Run before writing any files. Two checks:

### Existing rules conflict

Read all files currently in the target repo's `.claude/rules/`. For each file that would be overwritten with different content:

- Show the rule name, a one-line summary of what exists vs what would be written.
- Ask the user: **overwrite**, **keep existing**, or **skip**.

If no `.claude/rules/` directory exists, skip this check.

### tsconfig alignment

Read `references/typescript.md` for the expected compiler flags per preset. Read the target repo's `tsconfig.json` (including any `extends` chain). For each expected flag that is absent or set to a conflicting value:

- Report the flag, expected value, and actual value (or "not set").
- Ask whether to update `tsconfig.json`, leave it as-is, or note it for later.

If no `tsconfig.json` exists, skip this check.

### .csproj / Directory.Build.props alignment

Read `references/csharp.md` for the expected project settings per preset. Read the target repo's `.csproj` and any `Directory.Build.props` in the directory chain. For each expected setting that is absent or set to a conflicting value:

- Report the setting, expected value, and actual value (or "not set"), including which file in the chain sets it.
- Ask whether to update the file, leave it as-is, or note it for later.

If no `.csproj` exists, skip this check.

---

## Latest Practices Search

Before writing rules, ask the user:

> "Would you like me to search the web for the latest `<topic>` best practices? This may surface rules not yet in the bundled library."

**If yes:**

1. Search for `"<topic> best practices <current year>"` and any closely related queries (e.g. `"<topic> code quality <current year>"`).
2. Compare findings against the bundled rules for the selected preset and optional rules.
3. Identify practices from the search that are not already covered by the bundled assets.
4. Present the additional candidates as a numbered list with a one-line description each. Ask the user which to include.
5. For each approved candidate, write a new `.md` file to `.claude/rules/<rule-name>.md` alongside the preset rules (same idempotency check applies).

**If no:** proceed directly to Writing Rules.

---

## Writing Rules

For a given topic and preset:

- **`recommended`**: write all files from `assets/<topic>/recommended/`
- **`strict`**: write all files from `assets/<topic>/recommended/` **and** `assets/<topic>/strict/`
- **Optional rules**: write selected standalone `.md` files from `assets/<topic>/`

Target path: `.claude/rules/<filename>` (flat — no subdirectory per topic).

**Idempotency:** Before writing each file, check whether an identical file already exists at the target path. If content matches exactly, skip it and report it as "already up to date". Only write files whose content differs or that don't yet exist.

Create `.claude/rules/` if it does not exist.

After writing, report a summary: files written, files skipped (already up to date), files kept (user chose to keep existing).
