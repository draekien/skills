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
