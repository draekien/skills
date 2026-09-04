---
name: prune-local-branches
description: DEPRECATED — this skill moved to the version-control bucket as version-control/prune-local-branches. Install the version-control-skills plugin and use that skill instead.
argument-hint: "[--base branch]"
disable-model-invocation: true
---

# Deprecated — moved to the version-control bucket

This skill now lives at `skills/version-control/prune-local-branches`, in the `version-control` bucket. Its `scripts/` moved with it.

Tell the user:

1. This skill has moved and the copy here does nothing.
2. Install the new bucket, either route:
   - Claude Code plugin: `/plugin install version-control-skills@draekien-skills`
   - Cross-agent: `npx skills add draekien/skills/skills/version-control/prune-local-branches`
3. Re-run the request; the moved skill picks it up.

Then stop. Do not attempt the work from this file.
