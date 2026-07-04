# Quality Criteria

The standard every skill must meet.

**Token waste**

- Verbatim LLM response templates (`> "..."` blocks dictating exact phrasing) — describe behaviour, not words
- Prose describing what the agent will say rather than rules it must follow
- Repeated explanations of the same rule across multiple sections (duplication — give the concept one source of truth)
- Examples in the body that belong in `references/` or `assets/`
- Instructions that pass the deletion test (removing them wouldn't change agent output) — no-ops that read as if they matter but don't
- Superseded or stale instructions left in place instead of removed (sediment)

**Mis-calibrated freedom**

- Low-freedom step-by-step instructions where the task is variable and heuristic-driven
- High-freedom heuristics where the task is fragile or sequence-critical

**Reasoning-absent instructions**

- Imperative commands in judgment-heavy phases that carry no reasoning ("do X" with no "so that Y" or "because Z")
- Phase names that are generic sequence numbers when a concept name would encode the mental model
- Missing philosophy section in a skill where the agent needs to understand the goal before executing
- Missing anti-pattern section where a predictable wrong approach exists

**Trust violations**

- Content the agent already knows from training (language syntax, common tool usage)
- Paragraphs that don't justify their token cost
- A role or behaviour skill that describes a role the agent could already approximate instead of the delta from its defaults — the corrections and reflexes-to-suppress that are its real payload

**Body bloat**

- "When to use this skill" sections — activation belongs in the description
- Narrative or session-dated examples that aren't reusable

**Structural mismatch**

- Sequential numbered steps for behaviours that are concurrent or trigger-based
- One-time setup mixed with recurring behaviours
- Sub-flows presented as peers of their parent steps
- An early step whose attention keeps getting pulled toward a later step's goal visible in the same file, that a live run confirms gets rushed or skipped — a candidate for splitting into its own skill

**Content placement**

- Format specs, schemas, lookup tables in the body that belong in `references/`
- Output templates described in prose that belong in `assets/`
- Body over 500 lines when references could absorb the excess
- Single-branch material (a template, edge case, or reference doc only one use-path needs) left in the body instead of behind a context pointer

**Steering**

- A concept re-described in different words each time instead of anchored on one repeated leading word
- Bespoke phrasing invented for an idea that already has a standard domain term with strong training priors

**Outdated content**

- Migration steps for already-completed migrations
- References to deprecated names or patterns
- References to the current state of the codebase/corpus that the skill's own use will invalidate
