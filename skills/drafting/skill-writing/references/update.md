# Update Mode

Revise an existing skill for new or changed requirements. For structural or efficiency cleanup, use refine mode instead.

## Phase 1 — Read

Read the target `SKILL.md` and every file under its `references/`. Ask which skill to update if no path was given.

## Phase 2 — Identify changes

Establish what's changing and what's staying — new behaviours, removed steps, updated trigger phrases, renamed concepts, supporting-file edits. Ask only when context doesn't answer it.

## Phase 3 — Apply

Apply the writing principles and content placement rules.

- Never drop existing process logic without explicit user confirmation.
- If a change touches description trigger keywords, verify the description still reads as an API contract, not a summary.
- Update `references/` files only when content moves into or out of them, or when a reference's content itself is being changed.
- If body grows past 500 lines, propose moving content to `references/`.

## Phase 4 — Confirm

Report what was added, removed, or modified. Include line-count delta if the body changed significantly. Run `scripts/validate.py` per main `SKILL.md`.
