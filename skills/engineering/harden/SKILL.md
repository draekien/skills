---
name: harden
description: DEPRECATED — this skill moved to the quality bucket as quality/harden. Install the quality-skills plugin and use that skill instead.
argument-hint: "[--mode inline|subagents] [target]"
disable-model-invocation: true
---

# Deprecated — moved to the quality bucket

This skill now lives at `skills/quality/harden`, in the `quality` bucket. Its `references/` moved with it.

Tell the user:

1. This skill has moved and the copy here does nothing.
2. Install the new bucket, either route:
   - Claude Code plugin: `/plugin install quality-skills@draekien-skills`
   - Cross-agent: `npx skills add draekien/skills/skills/quality/harden`
3. Re-run the request; the moved skill picks it up.

Then stop. Do not attempt the work from this file.
