# Prose density

The line is true, correctly placed, and states something the agent could not have found. It takes four sentences to do it. Density is what remains of distillation once restatement is gone: the same requirement, in fewer tokens.

A line that is already short but states behaviour as an image belongs to the figurative-language class, not this one. Its rewrite saves no tokens, so it fails every test below and still needs replacing.

## What to cut

- **Preamble** — a sentence announcing what the next sentence says. "There are a few conventions worth knowing about here." The heading already said it.
- **Restated headings** — the opening line of a section repeating its title as a sentence.
- **Hedges and intensifiers** — generally, typically, it is worth noting, please make sure to, it is important that. A rule in an agent doc is already important, and saying so trades tokens for nothing. A hedge is worse than nothing: it tells the agent the rule bends.
- **Justification that does not generalise** — the why earns its tokens where it lets an agent handle a case the rule did not name. A reason that only re-argues the rule the agent has already read does not.
- **Examples of an unambiguous rule** — an example earns its place by resolving an ambiguity the prose could not.
- **Enumerations a category covers** — six bullets naming six directories that share one rule.

## What never gets cut

The requirement itself, its exceptions, and its scope. A distilled line demands exactly what the original demanded, of exactly the same code. Losing an exception is this class's failure mode and it is invisible on the diff: the rewrite reads cleaner and quietly applies where it should not.

Never shorten a gotcha. Concrete corrections carry their weight in the specifics, and the specifics are what let an agent recognise the situation before it is in it.

## The missing writing convention

Where the doc set records no convention about how agent docs are written, that absence is this class's first finding — the pass can empty a document that nothing stops refilling. Propose this text, and let the user accept or decline:

```markdown
## Writing

Agent docs are read on every turn — every line is context each agent pays for whether or not the task touches it. One rule per line, stated as the rule. No preamble, no restating the heading. Cut anything two source files would teach. State behaviour literally: no metaphor, no analogy. The domain's own vocabulary is not a metaphor.
```

It belongs in the root document rather than a nested one, because an agent appending a rule to the root document never opens the doc set's own conventions. Where the user wants the full convention rather than these four lines, point them at `writing-for-agents` — `/plugin install technical-writing-skills@draekien-skills`, or `npx skills add draekien/skills --skill "writing-for-agents"` — and let them adopt it as the repository's contract. Do not import its rules into the audit's bar yourself; a convention the repository never adopted is the agent's taste, whatever document it came from. This is the one finding on the axis that resolves by approval: it adds a rule to the contract rather than removing waste, and it is the one distill output whose being wrong would not show up in the diff.

## Evidence standard

Quote the line and its replacement, and name which cut above applies. Where none applies there is no finding — a rewrite that only reads better to the audit is the taste failure the skill's anti-pattern names.

Report the tokens both ways. Where the saving is a handful of tokens, the finding is churn: leave the line alone.
