---
name: with-testing-principles
description: DEPRECATED — this skill was renamed to testing-principles and moved to the quality bucket as quality/testing-principles. Install the quality-skills plugin and use that skill instead.
argument-hint: "[--mode write|audit] [target]"
disable-model-invocation: true
---

# Deprecated — renamed and moved to the quality bucket

This skill dropped its `with-` prefix and now lives at `skills/quality/testing-principles`, in the `quality` bucket. Its `references/` moved with it.

Tell the user:

1. This skill has been renamed to `testing-principles` and moved. The copy here does nothing.
2. Install the new bucket, either route:
   - Claude Code plugin: `/plugin install quality-skills@draekien-skills`
   - Cross-agent: `npx skills add draekien/skills/skills/quality/testing-principles`
3. Re-run the request; the renamed skill picks it up.

Then stop. Do not attempt the work from this file.
