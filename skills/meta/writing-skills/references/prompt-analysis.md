# Prompt Analysis

A skill is a prompt the future agent must execute, and every execution-level defect in it — a contradiction, a vague quantifier, an unhandled branch — is variance the agent absorbs unpredictably. Beyond auditing a skill against the tenets and craft rules, analyse it as a prompt. This lens catches what a style audit misses.

Analyse the prose the executing agent loads — the body and every linked file — not the frontmatter.

## Findings discipline

This governs every dimension below — apply it before reporting anything:

- Report only issues you are highly confident are real and materially harmful. Skip speculative, stylistic, or low-impact nits.
- Prefer precision over recall — fewer, certain findings beat many uncertain ones. When evidence is weak or ambiguous, omit the finding.
- Returning no issues is valid and expected when a dimension is already sound. Never force a finding to fill a category.
- Quote the exact offending phrase, copied verbatim, so the issue can be located precisely.
- Every finding ends in a concrete rewrite or addition — the specific replacement text, never abstract advice like "be clearer" or "consider being more specific".

## Dimensions

**Contradictions** — two instructions that directly conflict. State both phrases verbatim and explain what wrong behaviour the conflict produces, since the agent cannot satisfy both and will pick unpredictably.

**Ambiguity** — a vague or underspecified instruction the agent could read multiple ways. Name the type and the competing interpretations, then give the disambiguating rewrite:

- *quantifier* — imprecise amounts ("a few", "several") → replace with a number or range
- *reference* — unclear what a word points back to ("it", "this", "the above")
- *term* — a key term used without a fixed meaning, or used loosely after being defined
- *scope* — unclear how far an instruction reaches (one section, the whole task, all outputs)

**Persona & voice consistency** — places where the role, tone, or personality the skill establishes contradicts itself. Name the two clashing traits and the phrase where the mismatch is sharpest, then say which to keep or how to reconcile them.

**Cognitive load** — instruction structures too complex for an agent to follow reliably. Name the type, explain the mistake it invites, and give the restructure (numbered steps, a table, splitting into separate phases):

- *nested-conditions* — deeply stacked if/then branches
- *priority-conflict* — competing priorities with no stated precedence
- *deep-decision-tree* — too many branch points to track at once
- *constraint-overload* — so many simultaneous constraints the agent drops some

**Semantic coverage** — scenarios the skill leaves the agent to guess at. Two forms:

- *coverage gap* — a likely situation or intent the body never addresses; state the gap, rate its impact, and give the exact text to add
- *missing error handling* — an error condition or edge case with no instruction for it; give the exact handling instruction to add

**Composition conflicts** — clashes between the body and the files it links (`references/`, `assets/`), or between two linked files. The agent loads these together, so a conflict across them behaves like a contradiction within one file. Look for:

- *behavioural* — one file forbids what another requires
- *format* — incompatible output instructions across files
- *priority* — two files each claiming to override the other

State the conflicting text from each file and how to resolve it.
