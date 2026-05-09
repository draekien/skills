# Writing Principles

Apply these whenever drafting or revising any `SKILL.md` or its references.

## Match freedom to fragility

Calibrate specificity to how variable and how fragile the task is. Three levels:

### High freedom — text-based heuristics

Use when multiple approaches are valid, decisions depend on context, and heuristics are enough to guide.

```
## Code review process

1. Analyse structure and organisation.
2. Check for bugs and edge cases.
3. Suggest improvements for readability and maintainability.
4. Verify adherence to project conventions.
```

### Medium freedom — pseudocode or parameterised templates

Use when a preferred pattern exists, some variation is acceptable, and configuration affects behaviour.

```
## Generate report

def generate_report(data, format="markdown", include_charts=True):
    # process data
    # generate output in specified format
    # optionally include visualisations
```

### Low freedom — exact scripts, few or no parameters

Use when operations are fragile, consistency is critical, or a specific sequence must hold.

```
## Database migration

Run exactly: python scripts/migrate.py --verify --backup
Do not modify or add flags.
```

**Analogy.** Narrow bridge with cliffs → low freedom (exact instructions). Open field → high freedom (general direction). Choose by terrain.

## Trust the agent's intelligence

The agent is capable. Default to omitting context it already has. Challenge every paragraph against:

- Does the agent really need this explanation?
- Can this be assumed as common knowledge?
- Does this content justify its token cost?

If the answer is no, drop it.

## No narrative or session-dated examples

Reject content like "In session 2025-10-03 we found that empty `projectDir` caused...". Too specific, not reusable, decays into noise. Replace with the abstract rule: "Empty `projectDir` is invalid — validate before use."

Generic illustrative examples (a "good vs poor" pair next to a rule) are fine — they teach a pattern. Session anecdotes are not.

## Activation lives in the description

The frontmatter `description` is the sole activation signal. Never duplicate it in the body as a "When to use this skill" section. The body is for *how*, not *whether*.

## Test against your target models

Skills augment models; effectiveness depends on the host model.

- Smaller / faster models: does the skill provide enough scaffolding?
- Mid-tier models: is it clear and efficient?
- Largest models: does it avoid over-explaining?

If a skill is intended to run across model tiers, aim for instructions that work for all of them.
