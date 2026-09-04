---
name: with-ubiquitous-language
description: DEPRECATED — this skill was renamed to ubiquitous-language and now ships in the software-design-skills plugin. Install that plugin and use ubiquitous-language instead.
argument-hint: "[--mode migrate] [term-or-context]"
disable-model-invocation: true
---

# Deprecated — renamed to `ubiquitous-language`

This skill dropped its `with-` prefix and now ships in the `software-design-skills` plugin. The copy here does nothing. The `.skillsrc` key changed from `with-ubiquitous-language` to `ubiquitous-language`; the renamed skill migrates an existing block on its next run, so no manual config edit is needed.

Tell the user:

1. This skill has been renamed to `ubiquitous-language` and the copy here does nothing.
2. Install it, either route:
   - `/plugin install software-design-skills@draekien-skills` in a harness with plugin support
   - `npx skills add draekien/skills --skill "ubiquitous-language"` anywhere else
3. Re-run the request; the renamed skill picks it up.

Then stop. Do not attempt the work from this file.
