---
name: writing-for-humans
description: Writes developer-facing documentation in literal style — every sentence states a fact, mechanism, or instruction, with no metaphor, analogy, or restatement. Use when drafting or revising a README, guide, API reference, runbook, or release note for engineers, or when the user says "write the docs", "write this guide", "make this literal", "strip the metaphors", "tighten this documentation".
argument-hint: "[--mode write|audit] [target]"
---

# Writing for humans

The reader is an engineer looking for a specific fact under time pressure. They are not reading for comprehension of a narrative; they are scanning for the parameter, the constraint, or the step, and every sentence that does not carry one is a sentence they had to reject before reaching the one that did.

`--mode write` drafts; `--mode audit` applies the same rules to prose already on the page. Absent, infer from the target: an empty or missing file is `write`, an existing one with content is `audit`.

House convention outranks the wording and formatting rules here — a project style guide, an existing docs set with a settled voice, a vendor template. It does not override the source contract or the verification scan.

## Source contract

Work from source material the user supplies: a specification, a codebase, an existing document, a transcript. Where the source is missing, incomplete, or self-contradictory, name the gap and stop short of it. Do not fill it from general knowledge of how such systems usually work — a plausible invention is indistinguishable from a verified fact once it is on the page, and the reader has no way to tell which they are acting on.

A contradiction between two parts of the source is reported, not silently resolved. Say which parts disagree and what each claims.

## Literal

State what something is, what it does, or how to do it. Never state what it is *like*.

```text
✗ The scheduler wakes up, glances at the queue, and picks the hungriest job.
✓ The scheduler polls the queue every 5 seconds and runs the job with the highest priority value.
```

- **No figurative language** — no metaphor, simile, personification, analogy, or idiom. Each one asks the reader to translate an image back into behaviour before they can act, and the image lands differently in every reader's first language.
- **No rhetorical devices** — no rhetorical questions, no hyperbole, no appeals to how the reader will feel. "Blazingly fast" is not a performance claim; `p99 under 40 ms at 1000 rps` is.
- **A dead metaphor that is the domain's own vocabulary is literal, not figurative.** A stream drains, a handler listens, a node has a parent, a lock is held, a cache is warm. These are the precise technical terms and have no plainer equivalent. The test is whether you reached for the image or the field did.

## Plain language, exact identifiers

Two registers, and the boundary between them is where the words come from the code.

- **Identifiers are copied exactly** — API names, parameter names, file paths, config keys, error codes, environment variables. Never paraphrase, never simplify, never fix the casing. `MAX_RETRY_ATTEMPTS` is not "the max retries setting". Put every one in inline code.
- **Everything else is plain language** — common words, active voice, present tense, one idea per sentence. Name the actor: "the worker retries the request", not "the request is retried".

Where the two conflict, accuracy wins. A concept whose only correct name is a domain term keeps that term, and gets one definition the first time it appears rather than a simpler word that means something slightly different.

## Density

Every sentence carries information the reader cannot get from another sentence.

- **No preamble.** Do not open with what the document is about.

  ```text
  ✗ This guide explains how to configure the connection pool. Configuration is
    important because pooling affects throughput. Let's get started.
  ✓ Set the pool size with `DB_POOL_MAX`. Default: 10.
  ```

- **No doubling back.** State each fact once, in the section it belongs to. No summary section restating what the reader just read, unless the user asked for one.
- **No hedging.** Generally, typically, it is worth noting, please make sure to. A hedge on a real rule tells the reader the rule bends. Where a rule genuinely has an exception, state the exception.
- **Nothing deletable.** A sentence that could be removed without the reader losing information is removed.

## Structure

Headers and lists earn their place by aiding retrieval, not by breaking up the page. Steps, parameters, options, error codes, and limits go in lists or tables, because the reader is looking one of them up. Everything else is short prose.

Code, commands, file paths, and parameter names go in inline code or code blocks. Write no length target — the source material sets the length.

## Verification

Before finalising, scan the draft and remove or flag any sentence that:

1. Contains figurative language the domain did not supply.
2. Restates a point already made.
3. Could be deleted without losing information.
4. Was invented to fill a gap in the source material — flag the gap instead.

In `--mode audit`, report each hit with the original line, the rule it breaks, and the replacement text. An audit that names a problem without supplying the replacement leaves the work undone.

## Out of scope

This skill produces documentation. Marketing copy, opinion pieces, and narrative content need the devices these rules ban, so a request for one of those is named as out of scope rather than attempted in literal style. Say which it is and what you can write instead.

Sibling skills: use `writing-for-agents` where the reader is another agent loading one section in isolation, and `doc-comments` for in-source API documentation. Both ship in the same plugin as this skill — `/plugin install technical-writing-skills@draekien-skills`, or `npx skills add draekien/skills --skill "writing-for-agents"`. The `plain-language` and `simplified-technical-english` output styles set how the assistant talks; this skill sets how the artefact reads.

## Done

Every sentence in the target states a fact, mechanism, or instruction. Every identifier matches the source exactly. Every gap in the source material is named in the output rather than filled. The verification scan runs clean, and in `--mode audit` every finding carries its replacement text.
