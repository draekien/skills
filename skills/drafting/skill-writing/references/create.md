# Create Mode

Produces a new skill from scratch. Phases run in order; sub-decisions inside each phase are heuristics.

## Phase 1 — Gather

Establish three things, by asking the user or inferring from context:

- **Purpose** — the workflow or task the skill handles.
- **Triggers** — 2–3 phrases a user would say to invoke it.
- **Supporting files** — scripts, references, assets, or none.

Skip questions when context already answers them. Don't read scripted prompts at the user.

## Phase 2 — Name (low freedom)

Spec rules:

- 1–64 characters, `[a-z0-9-]` only.
- No leading, trailing, or consecutive hyphens.
- Matches parent directory name exactly.
- Verb-noun form preferred when name contains a verb (`transcribe-video`, `review-code`).

Propose, confirm, then proceed.

## Phase 3 — Description

The description is the sole activation signal. Write as API contract.

- 1–1024 characters, imperative ("Extracts...", "Creates..."), states what + when.
- Embed the user's trigger phrases verbatim so the agent recognises them.

Template:

```
<verb> <what it does>. Use when <conditions>, or when the user says "<phrase 1>", "<phrase 2>".
```

## Phase 4 — Body

Apply the writing principles and content placement rules. Pick patterns that fit the task — don't force a template. Common shapes:

- Gotchas section for known pitfalls.
- Output template in `assets/` for outputs the agent should copy rather than invent.
- Checklist when order matters but steps are independent.
- Validation loop ("if output doesn't satisfy X, retry with Y") for fragile generations.
- **Philosophy section** — opens with the core principle and explains *why* it matters before any workflow. Use when task judgment matters more than step adherence; place before procedure. The agent internalises the model and applies it — rather than following steps that break when the situation doesn't match.
- **Anti-pattern section** — names the common wrong approach, explains the mechanism by which it fails, and contrasts it with correct behaviour. "Don't do X" gives the agent no way to recognise X in the wild; naming and explaining it does.
- **Concept-named phases** — name phases by what the agent is doing conceptually (*Build a Feedback Loop*, *Tracer Bullet*) rather than by sequence (*Step 1*, *Step 2*). Names that encode the mental model survive when steps are skipped or reordered; sequence numbers don't.

## Phase 5 — Assemble

Create the directory, write `SKILL.md` with frontmatter (`name`, `description`, optional `compatibility`) plus a one-sentence orientation and the body. Add chosen subdirs and supporting files. Run `scripts/validate.py` per main `SKILL.md`.
