---
name: break-down-prd
description: DEPRECATED — this skill moved to the planning bucket as planning/break-down-prd. Install the planning-skills plugin and use that skill instead.
argument-hint: "[prd-file-path]"
disable-model-invocation: true
---

# Deprecated — moved to the planning bucket

This skill now lives at `skills/planning/break-down-prd`, in the `planning` bucket. Its `assets/` templates and `scripts/` moved with it.

Tell the user:

1. This skill has moved and the copy here does nothing.
2. Install the new bucket, either route:
   - Claude Code plugin: `/plugin install planning-skills@draekien-skills`
   - Cross-agent: `npx skills add draekien/skills/skills/planning/break-down-prd`
3. Re-run the request; the moved skill picks it up.

Then stop. Do not attempt the work from this file.
