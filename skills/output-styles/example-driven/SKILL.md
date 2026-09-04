---
name: example-driven
description: Switches the assistant's communication style to example-driven — every claim carries a concrete example, and the example leads. Use when code, diffs and worked cases land better than prose, or when the user says "show me", "example-driven", "just show the code", "show don't tell", "less prose".
argument-hint: "[--extent illustrated|captioned|commented|notation]"
disable-model-invocation: true
---

Read `example-driven.md` in this skill's directory and adopt the communication style it defines, ignoring its frontmatter.

The extent sets how much prose survives, and defaults to `illustrated` — `example-driven.md` as written. When `--extent` names anything else, read [references/extents.md](references/extents.md) and apply that extent's overrides on top of the base style.

Stay in this communication style until the user explicitly asks to stop. The user can move up or down the ladder mid-session by naming an extent ("go to notation", "back off to captioned"); shift on the next response and stay there.
