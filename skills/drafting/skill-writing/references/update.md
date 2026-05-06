# Update Mode

Revise an existing skill for new or changed requirements. Functional changes — not structural/efficiency cleanup (that's refine mode).

## Step 1 — Read existing skill

Read the target `SKILL.md` and all files in its `references/` directory (if any).

If no target path provided, ask the user which skill to update before continuing.

## Step 2 — Gather what's changing

Ask the user (one at a time, skip if already clear from context):

**Question 1 — Changes**

> "What needs to change? New behaviors, removed steps, updated trigger phrases, or renamed concepts?"

**Question 2 — Supporting files**

> "Do any supporting files need updating — scripts, reference docs, templates? Or is it SKILL.md only?"

## Step 3 — Apply changes

Apply writing standards from [SKILL.md](../SKILL.md). Follow progressive disclosure rules from [structure.md](structure.md) — keep heavy content in `references/`, not body.

Update `references/` files only if content is being moved into or out of them, or if existing reference content needs updating.

## Step 4 — Confirm

Report changes to user: what was added, removed, or modified. List line count before and after if the body changed significantly.

## Gotchas

- Never drop existing process logic without explicit user confirmation — even if it looks redundant.
- If a change touches trigger keywords in the description, verify the description still reads as an API contract, not a summary.
- If line count grows past 500, propose moving content to `references/`.
