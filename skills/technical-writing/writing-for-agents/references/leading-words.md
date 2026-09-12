# Leading words

A leading word compresses an instruction into a term the model already holds strong priors about, so the reading agent starts on the right trajectory without the document spending tokens on explanation. The compression is the entire justification: a term that is merely shorter to type, or merely more precise-sounding, is not a leading word.

## Where the glossary lives

A central glossary file, where the repository provides one, is the source of truth for every document in that repository. Find it before writing — a repository with a glossary and a document that ignores it produces two definitions of the same term.

Where the repository has none, maintain a glossary section inside the document being written, and say in that section that it is document-scoped. Do not create a repository-wide glossary file as a side effect of writing one document; propose it and let the user decide, because a glossary nobody agreed to is a contract nobody signed.

## Entry format

Three parts: the term, a one-sentence definition, and a one-sentence condition for when to use it instead of plain language.

| Term | Definition | Use when |
| --- | --- | --- |
| `red-green-refactor` | Write a failing test, make it pass with minimal code, then improve structure without changing behaviour. | Instructing a change to tested code where test-first sequencing matters. |
| `blast radius` | The set of paths where following a rule changes what an agent writes. | Deciding where a rule belongs, rather than how strong it is. |

The third column is what stops the glossary filling with terms that are defined but never worth using.

## Admitting a term

All four must hold.

1. **Pretrained** — the model already associates the term with the meaning being assigned. A coined term pays in definition tokens exactly what a pretrained term gives free, so coining one is a net loss unless no pretrained term fits.
2. **Fixed** — the term has one meaning in this repository, and the definition pins it.
3. **Compressing** — the term is shorter *and* clearer than the plain-language sentence it replaces. Equal length means plain language wins; shorter but less clear means plain language wins.
4. **Unambiguous in this domain** — the term's established meaning does not collide with another meaning the surrounding subject matter uses. `floor` as a pricing term and `floor` as a physical layer cannot both live in a facilities-billing document without disambiguation in the same sentence.

A term failing any of these is not admitted, and the concept is written in plain language instead. There is no partial admission.

## Coining a new term

Only when no pretrained term fits the concept and the concept recurs often enough to repay its definition. Propose the term to the user with its three-part entry, get agreement, add it to the glossary, and only then use it in a document body. Never introduce a coined term and its definition in the same sentence of a body document — that is the definition cost the leading word existed to avoid, paid anyway.

## Retiring a term

Remove an entry when the concept stops appearing, or when the term is used inconsistently often enough that the definition is no longer what readers take it to mean. Retiring is a change to every document that used the term: find those uses and replace them with plain language in the same change, or the retired term becomes an undefined figurative term everywhere it survives.

## Drift

A term used in a way its definition does not cover is drift, and it is flagged rather than resolved. Both readings look authorised to the next agent, which makes drift more damaging than an undefined term — an undefined term at least announces that it needs checking.

Report the definition, each divergent use with its file and line, and the two candidate meanings. The user decides whether the definition widens, the uses change, or the term splits into two. Do not pick one and rewrite the other, and do not widen a definition to cover a use that was simply wrong: a definition stretched to fit every observed use stops constraining anything.
