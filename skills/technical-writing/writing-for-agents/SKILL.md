---
name: writing-for-agents
description: Writes documentation whose reader is another agent — AGENTS.md, llms.txt indexes, ADRs, reference docs, runbooks an agent executes — literal, self-contained per section, and marked wherever a claim could not be verified. Use when drafting or revising agent-facing docs, when a doc must survive being loaded one section at a time, or when the user says "write the agent docs", "make this self-contained", "document this for agents".
argument-hint: "[--mode write|audit] [target]"
---

# Writing for agents

The reader has no memory of the conversation that produced the document, no shared context with its author, and may load any single section in isolation while every other section stays unread. A document that reads correctly top to bottom can still fail that reader, because the sentence that made section four safe was in section two.

`--mode write` drafts; `--mode audit` applies the same rules to a document already in the repository. Absent, infer from the target: an empty or missing file is `write`, an existing one with content is `audit`.

The repository's own convention outranks the structural rules here — its frontmatter fields, its heading sets, its file naming. Where the repository has settled a question, follow it and do not propose a migration. The literal, self-containment, verification, and redaction rules are not structural preferences and hold regardless.

## Establish the verification mechanism first

Name what you can actually check the system with before asserting anything about its current state: code search, running the build, reading a provided file, introspecting an API. State that mechanism in the report.

Where a claim needs a mechanism you do not have, mark the claim rather than dropping it or asserting it:

```markdown
✗ The worker retries three times.
✓ The worker retries three times. <!-- unverified: no access to `worker/` at time of writing -->
```

An omitted caveat and an omitted claim fail the same way — the next agent acts on the sentence in front of it. Never present unverified information as current fact, and never delete a claim to avoid marking it.

## Literal

State what something is, what it does, or how to do it. Never state what it is *like*.

```text
✗ Migrations are a minefield here — tread carefully around the tenant tables.
✓ A migration touching `tenants` or `tenant_settings` requires a backfill script
  in the same change. `pnpm migrate` fails without one.
```

- **No figurative language** — no metaphor, simile, personification, analogy, or idiom, except a leading word the glossary defines.
- **No rhetorical devices** — no rhetorical questions, no hyperbole, no appeals to emotion.
- **A dead metaphor that is the domain's own vocabulary is literal, not figurative.** A stream drains, a handler listens, a node has a parent, a lock is held. These are the precise technical terms and have no plainer equivalent. The test is whether you reached for the image or the field did.

## Leading words

A **leading word** is a term of art carrying a fixed, glossary-defined meaning that the model already holds priors about — `red-green-refactor`, `SOLID`, `idempotent`, `blast radius`. It sets the reading agent onto the right trajectory without spending tokens on explanation, which is the one reason to accept a figurative term at all.

Two rules govern the body of any document:

- **Use a leading word only where the glossary defines it.** An undefined figurative term is not a leading word, however obvious its meaning seems while writing it.
- **Never coin one inline.** A concept that would benefit from a leading word gets the term proposed and defined in the glossary first, then used.

Read [references/leading-words.md](references/leading-words.md) before adding a term to the glossary, before removing one, or when an existing term's use looks inconsistent with its definition.

The glossary holds terms of art for *instruction*. A project's domain vocabulary — the nouns of the business — is a different artefact with a different owner; keep the two separate and cross-link rather than merging them. Where the project maintains one, `ubiquitous-language` builds and enforces it: install with `/plugin install software-design-skills@draekien-skills`, or `npx skills add draekien/skills --skill "ubiquitous-language"`.

## Self-containment

Write each section so it is correct when it is the only section loaded.

- **Name the target, never the position.** "As mentioned above", "see the next section", and "the table below" all resolve to nothing in isolation.

  ```text
  ✗ See the authentication flow described earlier.
  ✓ See `docs/AUTH_FLOW.md`.
  ✓ See the "Token expiry" section of this document.
  ```

- **Repeat the noun.** No pronoun or demonstrative whose antecedent is more than one sentence away, and none where two candidate antecedents sit in the same paragraph. "It expires after an hour" is unusable when the paragraph mentions both a token and a session.
- **State scope at the top of each section** — which service, which environment, which version the section governs. Scope inherited from an earlier heading is scope the isolated reader never sees.

**Repeating a scope statement is not duplication.** The rule against stating a fact twice governs *rules and facts*, which drift apart once copied; a scope line exists precisely so the section stands alone, and it costs three tokens to prevent an agent applying a staging rule in production. Repeating a *rule* across two documents remains waste, because the copies drift and an agent acts on whichever one it read.

## Structure

Where the repository defines its own frontmatter and heading conventions, use those. Where it defines none, open every document with a metadata block:

```yaml
---
version: 1.2
last-verified-against: commit a1b2c3d, YYYY-MM-DD
owner: auth-service
---
```

`last-verified-against` is the field that keeps the document honest — it records the state the claims were checked against, so a later reader can tell how much has moved since. A document with no such marker reads as current forever.

Use a fixed set of section headers per document type, so a document of that type is predictable to an agent that has read another one. Steps, parameters, config keys, options, and error conditions go in lists or tables; short prose covers only what does not decompose. Identifiers — API names, parameter names, file paths, config keys, error codes — are copied exactly, in inline code, with their original casing.

## Density

Every line is context the reading agent pays for, on every turn, including the turns the line has nothing to do with.

- **No preamble.** Do not open with what the document is about.
- **No doubling back.** State each fact once, in the section it belongs to — subject to the scope carve-out in the self-containment rules of this document.
- **No hedging.** A hedge on a real rule tells the agent the rule bends.
- **Nothing deletable.** A line the agent would learn faster by reading the code earns nothing and rots when the code moves.

## Redaction

Never write a credential, secret, API key, token, or internal-only hostname into a document, even when the source material contains one. Replace it with a placeholder and say the value is redacted:

```text
✓ Set `DATABASE_URL` to the connection string from the secrets manager. <!-- value redacted -->
```

An agent-facing document is read by every agent on every task, and a secret in one is a secret in every context window that loads it.

## Verification

Before finalising, scan the draft and remove or flag any content that:

1. Contains figurative language no glossary entry defines.
2. Restates a fact or rule already stated elsewhere in the document.
3. Depends on a positional reference or an ambiguous pronoun to be understood.
4. Asserts a claim about current state without verification, or omits the metadata block where the repository has no convention of its own.
5. Includes a credential, secret, or sensitive identifier that is not redacted.
6. Uses a leading word that is shorter than its plain-language equivalent but no clearer to the reading agent.
7. Could be deleted without losing information.

In `--mode audit`, report each hit with the original line, the numbered check it fails, and the replacement text.

## Edge cases

- **Source material contradicts the existing document** — flag the conflict, state which is more current and on what evidence, and let the user decide. Silently picking one deletes a rule the code may be violating.
- **No verification mechanism is available** — say verification could not be performed. Do not quietly omit the caveat because every claim would carry it.
- **A leading word's use has drifted from its glossary definition** — flag the drift. Do not pick either meaning and write on; a term used two ways is worse than an undefined one, because both readings look authorised.
- **The request is not documentation maintenance** — writing code, making the design decision the document would record, choosing between the options an exploration lists. Name it as out of scope and say what you can write instead.

Sibling skills: use `writing-for-humans` where the reader is an engineer reading a README or guide, and `doc-comments` for in-source API documentation. Both ship in the same plugin as this skill — `/plugin install technical-writing-skills@draekien-skills`, or `npx skills add draekien/skills --skill "writing-for-humans"`.

## Done

Every section in the target is correct when read alone: its scope is stated, its references name their targets, and no pronoun reaches outside it. Every claim about current state is either verified against a named mechanism or marked unverified. Every figurative term is a glossary entry. No secret survives in the text. The verification scan runs clean, and in `--mode audit` every finding carries its replacement text.
