---
name: with-doc-comments
description: Writes and audits in-source API doc comments — JSDoc, TSDoc, XML docs, docstrings, rustdoc, godoc, KDoc — so each one carries the contract the signature cannot. Use when documenting a public member, backfilling doc comments across a codebase, or reviewing existing ones, or when the user says "document this API", "add JSDoc", "add XML docs", "write docstrings", "review these doc comments".
argument-hint: "[--mode write|audit] [target]"
---

A doc comment earns its place only if it says something the signature does not. The reflex to fill every slot produces the dominant failure: `@param userId The user ID.` — a line that costs a read, satisfies the linter, blocks the "undocumented" warning that would have flagged the gap, and tells the caller nothing. The signature already carries names, types, arity, and nullability. The comment's job is the contract around them.

This holds identically when writing new comments and when auditing existing ones. Auditing is the same rules applied to text already on the page.

Before writing, read neighbouring files in the same module and match their dialect — tag vocabulary, tag ordering, whether the codebase links members by reference or inherits docs from a base type. House convention outranks the wording and formatting rules below; it does not override the coverage rules, which decide what gets documented at all.

## Coverage

Decide what gets a comment before deciding how to word one.

- **Document the whole public surface** — every exported or public type, method, property, constant, event, and enum member, along with its parameters, return value, and thrown errors. A public member is a promise to someone who cannot read the implementation.
- **Leave internals alone.** Private and internal members get no doc comment, and do not fall back to an ordinary implementation comment either. Code that needs prose to be understood should be renamed, split, or restructured until it does not, and an invariant worth stating is worth enforcing — in the type system, a guard clause, or a test.
- **No comment beats a restated one.** When you cannot say more than the member's name already says, the member is either self-evident — leave it bare — or badly named. Renaming is the better fix.
- **Never bulk-generate doc comments to clear a linter.** The result is uniform noise that hides the members which genuinely needed explaining.

## The summary sentence

Documentation generators index the first sentence alone. It has to stand by itself.

Open with a verb in present tense, third person, and do not repeat the member's own name or lead with "This method". The verb form follows the member's kind:

| Member kind | Opening |
| --- | --- |
| Performs an action or returns data | `Adds…`, `Sends…`, `Parses…` |
| Getter returning a boolean | `Checks whether…` |
| Getter returning anything else | `Gets the…` |
| Returns nothing | `Sets…`, `Updates…`, `Deletes…`, `Registers…` |
| Constructor | `Creates a…` |
| Callback or handler | `Called by…` |

Keep the sentence free of anything that renders as a mid-sentence period — write "for example", not "e.g." — because generators truncate the summary at the first period. Put API names, members, and constants in code font; put string literals in code font with double quotation marks. Pluralise the noun, not the type name: "`Intent` objects", not "`Intents`".

Deprecations name the replacement in the first sentence. Reasons and migration steps follow in later sentences.

## Slots

Each tagged slot has a fixed shape. Capitalise the first word and end with a period.

- **Non-boolean parameter** — begin with "The" or "A": `The maximum number of retries before the call fails.`
- **Boolean parameter driving an action** — `If true, retries the request. If false, fails immediately.`
- **Boolean parameter describing a state** — `True if the account is locked; false otherwise.`
- **Return value** — begin with "The" for non-booleans; use `True if…; false otherwise.` for booleans. Keep it short and push the detail up to the type's own comment.
- **Defaults** — state them explicitly as `Default: 30 seconds.` A default that lives only in the code is invisible to the caller reading generated docs.
- **Thrown errors** — begin with "If" where the generator inserts the word "Throws" itself; begin with "Thrown when" where it does not. Check which by looking at how the codebase's existing comments render.

Never put `true` or `false` in code font or quotation marks in these slots.

## What the signature cannot say

This is the payload. A comment that covers the slots and stops has documented the shape and skipped the contract. Work through what the type system leaves unsaid and state whatever applies:

- **Why a caller picks this member** over the similarly-named one beside it.
- **Preconditions and call order** — what must already be true, what must be called first.
- **Side effects** — mutated arguments, written files, emitted events, cleared caches.
- **Ownership and lifetime** — who disposes the result; whether a returned collection is a live view or a copy.
- **Failure behaviour** — which errors surface, and whether a failed operation leaves partial work behind.
- **Concurrency** — thread safety, reentrancy, whether the call blocks.
- **Cost** — complexity or network round trips, where a caller would be surprised.
- **Units, ranges, and formats the type does not encode** — milliseconds against seconds, inclusive against exclusive bounds, the accepted shape of a string.

Add a short usage example on a type or on a member whose correct use is not obvious from its signature.

## Register

Write the prose in plain language. The reader is a developer under time pressure, often reading in a second language, inside a tooltip.

- Everyday words, active voice, present tense. Name the actor.
- Short sentences, one idea each.
- Address the caller directly — "Call this after the connection opens", not "the user should call this".
- Cut throat-clearing. "This function is a helper that validates…" becomes "Validates…".
- Define a domain term once, on the type that owns it, and use it unchanged everywhere else. Keep the precise technical term; do not trade accuracy for a simpler word.

## Audit failure modes

Name these on sight and replace each with a corrected comment rather than deleting it, unless the member is internal.

- **Stale** — describes behaviour the code no longer has, documents a parameter that is gone, or promises an error the code stopped raising. The most damaging mode, because it is trusted. Verify every claim against the implementation, not against the comment's plausibility.
- **Restated signature** — the comment paraphrases names and types and adds nothing.
- **Buried summary** — the first sentence carries background, so the generated index shows nothing useful.
- **Undocumented failure** — the member throws, returns null, or partially succeeds, and the comment is silent.
- **Copy-paste drift** — cloned from a sibling member and still naming the sibling's arguments or behaviour.
- **Throat-clearing** — "This method is used to…" ahead of the actual verb.
- **Documented internals** — doc comments on private members, diluting the real surface.

## Done

Every public member in the target is accounted for: documented against the rules above, or explicitly judged outside the public surface. Every documented member's contract claims — errors, side effects, defaults, units — are checked against the implementation. In an audit, every finding is named with its failure mode and carries the replacement text.
