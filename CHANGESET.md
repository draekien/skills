# writing-skills Dogfood Changeset

Ten self-application loops of `skills/meta/writing-skills` against itself. One entry per loop, one commit per loop. Baseline: commit `2efc8d8`.

## Loop 1

- No violations found; no changes. Audited SKILL.md, `references/spec-rules.md`, and `references/script-design.md` against every tenet, axis, description rule, content-placement rule, craft rule, and anti-pattern. Validator passes (23 pass, 1 expected portability warning for the Claude Code frontmatter extensions).

## Loop 2

- Dropped "Best-in-class" from the start of the description. Rule: the no-op test plus "every description word pays context load / cut identity" — a self-laudatory adjective does no invocation work in a user-triggered (`disable-model-invocation: true`) menu line.
- Removed the duplicated new-vs-existing split from the description's first clause ("craft for authoring or reworking a SKILL.md" → "craft of a SKILL.md"), keeping the split only in the when-to-reach clause. Rule: "keep one trigger per branch — synonym triggers restating a single branch are duplication," and "prune [the description] harder than the body." authoring≈creating-new and reworking≈revising-existing were the same branch stated twice.
- Dismissed (tension 1): near-verbatim overlap between SKILL.md's Validation section and `spec-rules.md`'s intro (both frame "stable subset / fetch the live spec for the rest"). Deferred content is not guaranteed loaded, so the body reader who runs the validator without opening the reference needs the scope boundary, and a reader opening the reference directly needs it too. Neither copy is safely removable; rewording one purely to differ would be cosmetic. Legitimate distinct-tier case, not sediment.
- Validator: 23 pass, 0 fail, 1 expected portability warning.
