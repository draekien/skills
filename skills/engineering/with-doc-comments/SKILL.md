---
name: with-doc-comments
description: DEPRECATED — this skill was renamed to doc-comments and moved to the technical-writing bucket as technical-writing/doc-comments. Install the technical-writing-skills plugin and use that skill instead.
argument-hint: "[--mode write|audit] [target]"
disable-model-invocation: true
---

# Deprecated — renamed and moved to the technical-writing bucket

This skill dropped its `with-` prefix and now lives at `skills/technical-writing/doc-comments`, in the `technical-writing` bucket.

Tell the user:

1. This skill has been renamed to `doc-comments` and moved. The copy here does nothing.
2. Install the new bucket, either route:
   - Claude Code plugin: `/plugin install technical-writing-skills@draekien-skills`
   - Cross-agent: `npx skills add draekien/skills/skills/technical-writing/doc-comments`
3. Re-run the request; the renamed skill picks it up.

Then stop. Do not attempt the work from this file.
