---
name: skill-writing
description: Creates a new agent skill following the Agent Skills open standard (agentskills.io). Use when building a new skill, scaffolding a SKILL.md, packaging a workflow into a portable skill, or when the user says "create a skill", "make a skill", "new skill", or "scaffold a skill".
compatibility: Designed for Claude Code (or similar products with Agent Skills support)
---

# New Skill Creator

Guides the creation of a new agent skill conforming to the [Agent Skills open standard](https://agentskills.io/specification). Produces a spec-compliant `SKILL.md` and any supporting files, then validates the result.

See [references/spec-rules.md](references/spec-rules.md) for the full validation checklist.

## Step 1 — Gather requirements (ask these in order, one at a time)

**Question 1 — Purpose**
> "What should this skill do? Describe the workflow or task it will handle."

**Question 2 — Trigger**
> "What would a user say or ask to activate this skill? Give 2–3 example phrases or requests."

**Question 3 — Supporting files**
> "Does this skill need to run scripts, reference external docs, or use templates? Or is it pure instructions?"

Use the answers to decide:
- Whether `scripts/`, `references/`, or `assets/` subdirectories are needed
- The description's trigger keywords (derived from the user's example phrases)
- How much detail belongs in the body vs. reference files

If the user has already described the skill in enough detail, skip questions and proceed.

## Step 2 — Generate the skill name

Rules (from the spec):
- 1–64 characters
- Lowercase letters, numbers, hyphens only (`a-z`, `0-9`, `-`)
- No leading, trailing, or consecutive hyphens
- Must match the directory name exactly

Derive the name from the purpose. Prefer verb-noun form: `pdf-extraction`, `code-review`, `data-sync`.

Present the proposed name and ask for confirmation before proceeding.

## Step 3 — Write the description

The description is the **sole trigger signal** — the agent's entire activation decision depends on it. Write it as an API contract, not a summary.

Rules:
- 1–1024 characters
- Imperative phrasing: "Extracts...", "Creates...", "Validates..." — not "A skill that..."
- State what it does AND when to use it
- Include the specific trigger keywords from the user's example phrases (Step 1, Q2)
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
- Number steps sequentially. Map any decision trees explicitly: "If X, go to step N. Otherwise, continue."
- Third-person imperative: "Extract the text..." not "I will..." or "You should..."
- Pick one term per concept and never vary it
- Omit what the agent already knows (common tool usage, language syntax)
- Add a **Gotchas** section for any environment-specific surprises or non-obvious constraints

### Progressive disclosure — what stays in the body vs. what moves out

Keep in the body (L2):
- The complete workflow steps
- Decision logic
- All information the agent needs on first activation

Move to `references/` (L3):
- API schemas, data formats, lookup tables
- Verbose technical documentation
- Domain-specific reference material unlikely to be needed on every run

Move to `assets/`:
- Output templates the agent copies rather than invents
- Static configuration files
- Example inputs/outputs

Link reference files from the body using relative paths:
```
See [references/schema.md](references/schema.md) for the full schema.
```
Keep reference chains one level deep only — never reference a reference.

### Body length
Target under 500 lines. If the body exceeds this, split the excess into `references/`.

### Useful structural patterns (use as needed)
- **Gotchas section:** common mistakes and environment-specific surprises
- **Output template in `assets/`:** concrete example the agent copies; beats prose descriptions
- **Checklist:** for multi-step workflows where step order matters but steps are independent
- **Validation loop:** "If the output does not satisfy X, retry with Y"
- **Plan-validate-execute:** for destructive or batch operations — always show a plan before running

## Step 5 — Decide on supporting files

### `scripts/` — use when
- A task is deterministic and variation is a bug
- The agent would otherwise re-derive complex logic from scratch on each run
- The operation benefits from idempotency guarantees

**Script design rules (non-negotiable for agent compatibility):**
- No interactive prompts — must run fully unattended
- Structured stdout (data output) vs. stderr (diagnostic logs)
- Actionable error messages — tell the agent how to self-correct
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
3. Full documented dependency list if the above are insufficient

### `references/` — use when
- Documentation is verbose but not needed on every activation
- The content is stable reference material (schemas, cheatsheets, domain specs)
- Loading it every time would waste context unnecessarily

### `assets/` — use when
- The agent needs a concrete template to copy (not invent)
- Static configuration or example files are needed

## Step 6 — Assemble the skill

Create the directory structure:
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
compatibility: <if the skill has specific environment requirements, otherwise omit>
---

# <Human-readable title>

<One-sentence orientation — what this skill does and what it produces>

<Body content from Step 4>
```

Then write any supporting files.

## Step 7 — Validate against the spec

First run the automated validator:

```
uv run scripts/validate.py <skill-dir>
```

Fix any failures before continuing. The script checks all `[AUTO]` rules in [references/spec-rules.md](references/spec-rules.md) — frontmatter structure, file references, body length, script safety, and model-specific term heuristics.

Then manually review the `[LLM]` rules in [references/spec-rules.md](references/spec-rules.md): description quality, instruction style, content placement (body vs. references vs. assets), script robustness, and security.

After all checks pass, confirm to the user:
> "Skill created at `<path>/SKILL.md`. Automated validation passed. Manual checks complete."

If the skill has supporting files, list them too.

## Edge Cases

- **User skips questions:** If enough context is available from the request, proceed without asking. Only ask when the purpose or trigger is genuinely ambiguous.
- **Existing skill being rewritten:** Check if a `SKILL.md` already exists at the target path. If so, read it first and treat this as a revision, not a fresh creation.
- **Skill too complex for one file:** If the workflow has more than ~3 major phases, propose splitting into sibling skills or using a primary skill with reference files — don't create a 1000-line body.
- **LLM-agnostic requirement:** If the user needs the skill to work across multiple LLM providers, avoid any platform-specific extensions in the body. Use `compatibility:` to document platform-specific requirements separately.
