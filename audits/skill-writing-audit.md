# Audit — `skill-writing` skill (dogfooding)

**Target:** `skills/drafting/skill-writing/` (SKILL.md + 6 references + `scripts/validate.py`)
**Method:** the skill's own **Quality Gate** applied to itself — three parallel LLM-judge subagents (Spec & structure, Writing-standards, Prompt-analysis) on Opus 4.8, plus the mechanical gates (`validate.py`, `ruff`, link/anchor resolution).
**Scope:** audit only — no fixes applied. Date: 2026-07-04.

---

## Verdict

The skill is in strong shape and **largely passes its own bar**. Every automated check is green, the body is well under the line limit, voice/durability/freedom-calibration are clean, and no contradictions or persona defects surfaced. The findings below are refinements, not failures — and two of them are notable precisely because this skill *defines* the standard it trips over.

| Gate | Result |
|---|---|
| `validate.py` | 23 passed, 0 failed, 1 non-blocking portability warning (expected) |
| `ruff check scripts/` | All checks passed |
| Body length | 215 / 500 lines |
| Links & anchors | All resolve |
| LLM judges | 2 material, 4 nits |

---

## Material findings

### M1 — Duplication: Workflow step 1 restates the "Context First" section

*Source: Writing-standards judge. Criterion: deletion test → duplication ("give each concept a single source of truth and cross-reference it, never restate it").*

Workflow step 1:
> **Gather context** — understand purpose, scope, trigger phrases, and supporting file needs from session before asking anything.

"Context First, Then Interview" section:
> Exhaust what the session already provides before asking anything. If purpose, scope, trigger phrases, and supporting file needs are clear from context, proceed directly.

Both state the "before asking anything" rule *and* the same enumerated list (purpose, scope, trigger phrases, supporting file needs). The skill's own duplication rule says to give the concept one home and cross-reference it.

**Recommended fix:** collapse step 1's lead clause to a pointer, letting "Context First" own the rule. Keep step 1's unique `vet-skill-idea` sub-bullets (they're not duplicated):
>
> 1. **Gather context** — see `[Context First, Then Interview](#context-first-then-interview)`.
>    - If building from scratch and the concept isn't already validated…

**Tradeoff to weigh:** a numbered Workflow legitimately functions as an at-a-glance overview, and a one-line summary that later sections elaborate is a common, defensible pattern. If you consider the Workflow an intentional table-of-contents, this is a nit rather than material. The judge rated it material on a strict reading of the skill's "never restate" wording; I'd downgrade it to borderline given the overview/detail convention. **Your call on which reading governs.**

### M2 — Coverage gap: the Prompt-analysis judge is told to check composition conflicts but not told to read the files needed to do so

*Source: Prompt-analysis judge. Dimension: semantic coverage (coverage gap). This is the strongest finding — the current audit itself had to work around it.*

In the Quality Gate table, the Prompt-analysis row's **"What to read"** cell lists only:
> [references/prompt-analysis.md](references/prompt-analysis.md)

…but its **"What to check"** cell includes:
> composition conflicts with linked files

Composition-conflict detection is impossible without reading the linked files (`specification.md`, `spec-rules.md`, `quality-criteria.md`, and conditionally `stateful-skills.md` / `script-design.md`). As written, that dimension gets silently skipped or done from memory. The other two judge rows *do* enumerate their source files, so this row's omission is an inconsistency, not a deliberate minimalism. Concrete evidence: to run this very audit I had to hand the Prompt-analysis judge an extra instruction to open the referenced files — the table under-provisioned it.

**Recommended fix:** change the Prompt-analysis "What to read" cell to:
> references/prompt-analysis.md for the method; plus the body's linked files (specification.md, spec-rules.md, quality-criteria.md, and stateful-skills.md / script-design.md when the body links them) so composition conflicts across files can be checked

---

## Nits

### N1 — Two-source-of-truth between the body and `spec-rules.md`

*Source: Spec & structure judge.*

The body's Name / Description / Argument-hint guidance restates rules (and the exact `"[write|audit] [target]"` vs `"[code to write tests for…]"` example) that also live verbatim in `references/spec-rules.md`. This is the drift failure mode the skill warns about — two copies to hand-keep in sync.

**Mitigating context:** the body (author's teaching form, loaded on activation) and `spec-rules.md` (auditor's checklist, loaded by a judge subagent) are never both in one reader's context, so there's no per-read token waste — only a maintenance-sync cost. This is plausibly an intentional write-vs-audit split. **Recommendation:** leave as-is unless you find them drifting; if you want to close it, keep the concrete examples in exactly one file and cross-reference from the other.

### N2 — "One term per concept" drift on the *delta* concept

*Source: Writing-standards judge.*

"Trust the agent's intelligence":
> the *delta from the agent's defaults*

"Knowledge or Procedural":
> the value is the *delta from what the agent already knows*

Same concept, two trailing phrasings. The leading word "delta" holds, so impact is minor — but the skill's own standard is "one term per concept — never vary."

**Recommended fix:** standardize the tail. Reuse "*delta from the agent's defaults*" in both places.

### N3 — Mild restatement of the workflow-scripting principle

*Source: Writing-standards judge.*

Under "Match freedom to fragility":
> If the judgment required is *whether* to follow a process at all — not just how to execute it — encoding the process is wrong regardless of terrain (see the Workflow scripting `[anti-pattern](#anti-patterns)`).

This restates the anti-pattern's own definition ("encoding a fixed sequence of steps when the task requires judgment about whether to follow a process at all") before cross-referencing it. It partly earns its keep by adding the "regardless of terrain" framing.

**Recommended fix (optional):** trim to the terrain-exception nuance plus the pointer, letting the anti-pattern own the definition:
> Terrain doesn't apply when the real question is *whether* to run the process at all, not how — that's the Workflow scripting `[anti-pattern](#anti-patterns)`.

### N4 — Path-relativity ambiguity in Quality Gate step 3

*Source: Prompt-analysis judge. Dimension: ambiguity (scope/reference).*

> Run `uv run scripts/validate.py <skill-dir>` — fix any `[AUTO]` failures before confirming

`scripts/validate.py` is relative to the *skill-writing* directory, while `<skill-dir>` is the *target* skill being audited (a different directory). Nothing states the working directory, and the repo convention (per CLAUDE.md) is to run tooling from repo root — where `scripts/validate.py` does not resolve. The agent will recover, but the ambiguity is real.

**Recommended fix:**
> Run skill-writing's validator against the audited skill: `uv run scripts/validate.py <skill-dir>` — here `scripts/validate.py` is relative to the skill-writing directory and `<skill-dir>` is the skill being audited; fix any `[AUTO]` failures before confirming.

---

## Dimensions checked and found clean

- **Frontmatter / spec:** name matches dir, all charset/length rules pass; description correctly written as a scannable CLI-help line (right choice for `disable-model-invocation: true`), imperative, states what + when; `argument-hint` present, quoted, free-text, single-input form correct (create/revise/audit modes are inferred from context, not typed sub-commands).
- **Content placement:** shared principles correctly in the body; verbose spec/validation material correctly in `references/` behind thin routers; no single-branch material stranded in the body; nothing every-run buried in references.
- **Script design:** `validate.py` satisfies every `script-design.md` rule — no interactive prompts, structured stdout (`--json`) vs stderr, actionable errors, idempotent/read-only, meaningful exit codes (0/1/2), PEP 723 dep constrained; listed under "Available scripts" and invoked via correct relative path.
- **Stateless correctness:** genuinely stateless; correctly omits all stateful machinery (its "Stateful or Stateless" section is teaching content, not skill state).
- **Voice:** third-person imperative throughout; no "I will" / "you should".
- **No tool names:** `git status`, `python scripts/migrate.py` are illustrative freedom-calibration examples; `validate.py` / `uv` / `ruff` / `/vet-skill-idea` are the skill's own bundled scripts and named dependencies — legitimately named.
- **Freedom calibration:** high-freedom prose for judgment sections, low-freedom exact commands for the fragile Quality Gate. The skill's own 4-step Workflow survives its own "remove the headers" workflow-scripting test.
- **Carry the why:** judgment-heavy passages carry reasoning; bare imperatives are confined to deterministic bright-line rules the skill explicitly sanctions.
- **Durability:** no mutable-environment-state references.
- **Contradictions:** none. The one candidate (deletion test "cut it" vs "never drop process logic without confirmation") is explicitly reconciled in-line.
- **Persona/voice consistency, cognitive load, sediment, no-ops:** none found.
- **Reference consistency:** all six references exist, all anchors resolve, "Skill Anatomy" agrees with `specification.md`, and the Quality Gate judge-remit table accurately reflects the actual contents of the three method references (subject to M2).

---

## Suggested priority order

1. **M2** — fix the Prompt-analysis "What to read" cell (clear, self-evident, no tradeoff).
2. **M1** — decide overview-vs-restate reading; collapse step 1 to a pointer if you take the strict view.
3. **N2, N4** — small, unambiguous polish.
4. **N1, N3** — optional; leave unless you want the extra tidiness.
