---
name: skill-writing
description: Creates a new agent skill following the Agent Skills open standard (agentskills.io). Use when building a new skill, scaffolding a SKILL.md, packaging a workflow into a portable skill, or when the user says "create a skill", "make a skill", "new skill", or "scaffold a skill".
compatibility: Designed for Claude Code (or similar products with Agent Skills support)
---

# New Skill Creator

Guides creation of new agent skill per [Agent Skills open standard](https://agentskills.io/specification). Produces spec-compliant `SKILL.md` + supporting files, then validates.

See [references/spec-rules.md](references/spec-rules.md) for full validation checklist.

## Step 1 — Gather requirements (ask these in order, one at a time)

**Question 1 — Purpose**
> "What should this skill do? Describe the workflow or task it will handle."

**Question 2 — Trigger**
> "What would a user say or ask to activate this skill? Give 2–3 example phrases or requests."

**Question 3 — Supporting files**
> "Does this skill need to run scripts, reference external docs, or use templates? Or is it pure instructions?"

Use answers to decide:
- Whether `scripts/`, `references/`, or `assets/` subdirs needed
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

### Instruction style
- Number steps sequentially. Map decision trees explicitly: "If X, go to step N. Otherwise, continue."
- Third-person imperative: "Extract the text..." not "I will..." or "You should..."
- One term per concept, never vary
- Omit what agent already knows (common tool usage, language syntax)
- Add **Gotchas** section for environment-specific surprises or non-obvious constraints

### Progressive disclosure — body vs. reference files

Keep in body (L2):
- Complete workflow steps
- Decision logic
- All info agent needs on first activation

Move to `references/` (L3):
- API schemas, data formats, lookup tables
- Verbose technical docs
- Domain-specific reference material unlikely needed every run

Move to `assets/`:
- Output templates agent copies rather than invents
- Static config files
- Example inputs/outputs

Link reference files from body using relative paths:
```
See [references/schema.md](references/schema.md) for the full schema.
```
One level deep only — never reference a reference.

### Body length
Target under 500 lines. Excess → split into `references/`.

### Useful structural patterns (use as needed)
- **Gotchas section:** common mistakes + environment surprises
- **Output template in `assets/`:** concrete example agent copies; beats prose descriptions
- **Checklist:** multi-step workflows where order matters but steps are independent
- **Validation loop:** "If output doesn't satisfy X, retry with Y"
- **Plan-validate-execute:** destructive/batch ops — show plan before running

## Step 5 — Decide on supporting files

### `scripts/` — use when
- Task deterministic, variation = bug
- Agent would re-derive complex logic each run
- Op benefits from idempotency

**Script design rules (non-negotiable for agent compatibility):**
- No interactive prompts — must run fully unattended
- Structured stdout (data output) vs. stderr (diagnostic logs)
- Actionable error messages — tell agent how to self-correct
- Idempotent — safe to run twice
- Dry-run flag for destructive operations
- Meaningful exit codes (0 = success, non-zero = specific failure)
- Output size guards to avoid harness truncation

**Dependency approaches (in order of preference):**
1. One-off invocation with pinned version: `uvx some-tool@1.2.3` or `npx tool@version`
2. Self-contained script with PEP 723 inline deps (Python):
   ```python
   # /// script
   # dependencies = ["httpx==0.27.0", "rich==13.7.0"]
   # ///
   ```
3. Full documented dependency list if above insufficient

### `references/` — use when
- Docs verbose but not needed every activation
- Content stable reference material (schemas, cheatsheets, domain specs)
- Loading every time wastes context

### `assets/` — use when
- Agent needs concrete template to copy (not invent)
- Static config or example files needed

## Step 6 — Assemble the skill

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

## Step 7 — Validate against the spec

Run automated validator:

```
uv run scripts/validate.py <skill-dir>
```

Fix failures before continuing. Script checks all `[AUTO]` rules in [references/spec-rules.md](references/spec-rules.md) — frontmatter structure, file references, body length, script safety, model-specific term heuristics.

Then manually review `[LLM]` rules in [references/spec-rules.md](references/spec-rules.md): description quality, instruction style, content placement, script robustness, security.

After all checks pass, confirm to user:
> "Skill created at `<path>/SKILL.md`. Automated validation passed. Manual checks complete."

List supporting files too if present.

## Edge Cases

- **User skips questions:** Enough context in request → proceed without asking. Ask only when purpose or trigger genuinely ambiguous.
- **Existing skill rewrite:** Check if `SKILL.md` exists at target path. If so, read first, treat as revision not fresh creation.
- **Skill too complex for one file:** 3+ major phases → propose sibling skills or primary skill + reference files. Don't create 1000-line body.
- **LLM-agnostic requirement:** Skill must work across multiple LLM providers → avoid platform-specific extensions in body. Use `compatibility:` to document platform requirements separately.