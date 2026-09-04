---
name: with-ubiquitous-language
description: DEPRECATED — this skill was renamed to ubiquitous-language and moved to the software-design bucket as software-design/ubiquitous-language. Install the software-design-skills plugin and use that skill instead.
argument-hint: "[--mode migrate] [term-or-context]"
disable-model-invocation: true
---

# Deprecated — renamed and moved to the software-design bucket

This skill dropped its `with-` prefix and now lives at `skills/software-design/ubiquitous-language`, in the `software-design` bucket. Its `references/` and `scripts/` moved with it. The `.skillsrc` key changed from `with-ubiquitous-language` to `ubiquitous-language`; the renamed skill migrates an existing block on its next run, so no manual config edit is needed.

Tell the user:

1. This skill has been renamed to `ubiquitous-language` and moved. The copy here does nothing.
2. Install the new bucket, either route:
   - Claude Code plugin: `/plugin install software-design-skills@draekien-skills`
   - Cross-agent: `npx skills add draekien/skills/skills/software-design/ubiquitous-language`
3. Re-run the request; the renamed skill picks it up.

Then stop. Do not attempt the work from this file.
