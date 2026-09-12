# Figurative language

The line is true, correctly placed, and states something the agent could not have found. It states it as an image. The reading agent has to translate the image back into behaviour before it can act, and two agents translate it two ways.

```text
✗ The cache forgets entries nobody has asked for in a while.
✓ The cache evicts an entry after 30 seconds without a read.
```

This class is the one distill class that does not turn on token count. The rewrite above is the same length. What it removes is the interpretation step and the two questions the original leaves open — what "a while" is, and whether "forgets" means evicted or merely deprioritised.

## What qualifies

- **Metaphor, simile, personification, analogy, idiom** — anything describing what a thing is *like* rather than what it is, does, or requires.
- **Rhetorical devices** — rhetorical questions, hyperbole, appeals to how the reader should feel about a rule. "Never, ever commit to main" carries exactly the force of "Never commit to `main`" and spends more tokens saying it.

## What does not

- **The domain's own dead metaphors.** A stream drains, a handler listens, a node has a parent, a lock is held, a cache is warm. These are the precise technical terms and have no plainer equivalent. The test is whether the author reached for the image or the field did.
- **A leading word the repository's glossary defines.** A term of art with a recorded definition is compression, not decoration. Check the glossary before raising the finding; where the repository has no glossary, judge the term on whether the model would already hold the intended meaning — `idempotent` and `blast radius` pass, an invented term does not.
- **Wording the audit would have chosen differently.** A literal line that could be a slightly better literal line is not a finding. This class removes a device, not a style preference.

## Resolution

Mechanical, on the same reversibility licence as the other distill classes: no writing pass runs without a clean tree, so the whole pass is one diff that `git checkout -- .` undoes.

The replacement states the behaviour the image was standing in for. Where the image was standing in for something the document never specified — "a while", "quite large", "as needed" — the literal replacement needs a value the document does not hold. Do not invent it. Report the line as a claim-verification finding instead, carrying the question the metaphor was hiding, and leave the line alone.

## Evidence standard

Quote the line, name the device, and give the replacement. A finding that asserts a line is figurative without naming which device is the audit's own taste, and this class does not resolve that way.

Do not report a token saving for this class. The saving is usually zero and occasionally negative, and quoting it invites the user to reject a correct finding on the wrong measure. State what the reading agent no longer has to interpret.
