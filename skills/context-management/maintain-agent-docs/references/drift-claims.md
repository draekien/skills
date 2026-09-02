# Claim verification

A claim is any statement in the doc set that the code can contradict. Verifying one means finding the code it names and checking whether that code still behaves as described.

## Extracting the claim

Restate each claim as something falsifiable before looking for the code. "Errors are handled consistently" cannot be checked; "handlers return a result type rather than throwing" can. A claim that resists falsification is not verifiable — leave it alone rather than inventing a test for it, and note it only if the effort level is `max`.

Prioritise claims by what an agent would act on: a rule about where code goes, a required call, a forbidden pattern, an ownership boundary, a named path or entry point, a constraint on what may be added or upgraded.

## Verification

Open only the code the claim names, plus the minimum needed to tell whether the claim holds there. Three outcomes:

- **Holds** — no finding.
- **Contradicted** — the code does the opposite, consistently. This is the finding that matters most, because an agent following the document will write code the repository rejects.
- **Partially holds** — the rule is followed in most places and broken in a few. The pattern of exceptions is the finding: either the rule has undocumented boundaries, or the exceptions are defects. Report which places diverge; do not average them into a verdict.

## Evidence standard

Cite the document line and the specific code that contradicts it. A single counter-example is enough to raise a finding but not enough to characterise it — check whether the counter-example is the norm or the exception before deciding between contradicted and partially holds.

## Why this class goes to interview

The audit can establish that the document and the code disagree. It cannot establish which one is the mistake, and the two repairs are opposites: rewrite the document, or fix the code. A document that codifies an intended rule the code violates is doing its job — the disagreement is the point. Present both readings with the evidence, and let the user choose.

Where the user says the document is right, the finding becomes a code defect: record it in the report's closing and change nothing. Auditing the code is not this pass.
