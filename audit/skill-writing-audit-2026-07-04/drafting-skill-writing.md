# skill-writing

## Skill name does not follow its own verb-noun naming preference

The skill's own Skill Anatomy section states a naming preference: "verb-noun form preferred when name contains a verb" (examples: `transcribe-video`, `review-code`). The skill's own name, `skill-writing`, is noun+gerund rather than verb-noun (a name like `write-skills` would match the stated preference).

**Why this is a tradeoff, not a clear-cut fix**: Renaming is not a body-text edit — `skill-writing` is an established leading term wired into the directory name, `.claude-plugin/marketplace.json`, the `drafting/` bucket `README.md`, and cross-references from other skills and docs across the repo (e.g. `vet-skill-idea`, `claude-md-management` workflows likely refer to it by name). Renaming it would require a coordinated rename across all of those locations, plus a directory move (the `[AUTO]` rule requires `name` to match the parent directory exactly), and risks breaking any external instructions or muscle-memory invocations (`/skill-writing`) that already reference the current name. The stated rule is also a "preference," not an `[LLM]` or `[AUTO]` hard rule — the skill itself treats it as non-binding.

**Recommendation**: Leave the name as-is. `skill-writing` is unambiguous, is already the de facto term of art in this repo, and the cost of a repo-wide rename outweighs the benefit of strict adherence to a stated stylistic preference for a name that isn't actually confusing.

**Alternative**: If the team wants strict consistency, rename to `write-skills` (or `author-skills`) in a dedicated rename pass that updates: the skill's directory name, `SKILL.md` frontmatter `name` field, `.claude-plugin/marketplace.json` bucket and `everything` entries, the `drafting/README.md` listing and link, and any other in-repo cross-references (e.g. `vet-skill-idea`'s pointers to this skill). This should be done as its own change, not bundled into an unrelated quality-gap fix.
