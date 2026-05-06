# Create Mode

New skill from scratch. Follow steps in order.

## Step 1 — Gather requirements (ask in order, one at a time)

**Question 1 — Purpose**

> "What should this skill do? Describe the workflow or task it will handle."

**Question 2 — Trigger**

> "What would a user say or ask to activate this skill? Give 2–3 example phrases or requests."

**Question 3 — Supporting files**

> "Does this skill need to run scripts, reference external docs, or use templates? Or is it pure instructions?"

Use answers to decide:

- Whether `scripts/`, `references/`, or `assets/` subdirs needed (see [structure.md](structure.md))
- Description's trigger keywords (from user's example phrases)
- What belongs in body vs. reference files

If user already described skill in enough detail, skip questions and proceed.

## Step 2 — Generate the skill name

Rules (from spec):

- 1–64 characters
- Lowercase letters, numbers, hyphens only (`a-z`, `0-9`, `-`)
- No leading, trailing, or consecutive hyphens
- Must match directory name exactly

Derive name from purpose. Prefer verb-noun form: `pdf-extraction`, `code-review`, `data-sync`.

Present proposed name, ask confirmation before proceeding.

## Step 3 — Write the description

Description = **sole trigger signal** — agent's entire activation decision depends on it. Write as API contract, not summary.

Rules:

- 1–1024 characters
- Imperative phrasing: "Extracts...", "Creates...", "Validates..." — not "A skill that..."
- State what it does AND when to use it
- Include specific trigger keywords from user's example phrases (Step 1, Q2)
- Name edge cases or related tasks that should also trigger it

**Template:**

```
<Imperative verb> <what it does>. Use when <trigger conditions>, or when the user says "<example phrase 1>", "<example phrase 2>".
```

**Good example:**

```
Extracts text, tables, and form fields from PDF files, and merges multiple PDFs. Use when working with PDF documents, or when the user mentions PDFs, forms, or document extraction.
```

**Poor example:**

```
Helps with PDFs.
```

## Step 4 — Write the SKILL.md body

Apply writing standards and progressive disclosure rules from [SKILL.md](../SKILL.md). Useful structural patterns:

- **Gotchas section:** common mistakes + environment surprises
- **Output template in `assets/`:** concrete example agent copies; beats prose descriptions
- **Checklist:** multi-step workflows where order matters but steps are independent
- **Validation loop:** "If output doesn't satisfy X, retry with Y"
- **Plan-validate-execute:** destructive/batch ops — show plan before running

## Step 5 — Assemble the skill

Create directory structure:

```
<skill-name>/
├── SKILL.md
├── scripts/        (if needed)
├── references/     (if needed)
└── assets/         (if needed)
```

Write `SKILL.md` with:

```markdown
---
name: <skill-name>
description: <optimized description from Step 3>
compatibility: <if skill has specific environment requirements, otherwise omit>
---

# <Human-readable title>

<One-sentence orientation — what this skill does and what it produces>

<Body content from Step 4>
```

Then write supporting files.

## Edge Cases

- **User skips questions:** Enough context in request → proceed without asking. Ask only when purpose or trigger genuinely ambiguous.
- **Skill too complex for one file:** 3+ major phases → propose sibling skills or primary skill + reference files. Don't create 1000-line body.
- **LLM-agnostic requirement:** Skill must work across multiple LLM providers → avoid platform-specific extensions in body. Use `compatibility:` to document platform requirements separately.
