---
name: module-design
description: DEPRECATED — this skill moved to the software-design bucket as software-design/module-design. Install the software-design-skills plugin and use that skill instead.
argument-hint: "[--mode design|audit] [module-or-file]"
disable-model-invocation: true
---

# Deprecated — moved to the software-design bucket

This skill now lives at `skills/software-design/module-design`, in the `software-design` bucket. Its `references/` and `scripts/` moved with it.

Tell the user:

1. This skill has moved and the copy here does nothing.
2. Install the new bucket, either route:
   - Claude Code plugin: `/plugin install software-design-skills@draekien-skills`
   - Cross-agent: `npx skills add draekien/skills/skills/software-design/module-design`
3. Re-run the request; the moved skill picks it up.

Then stop. Do not attempt the work from this file.
