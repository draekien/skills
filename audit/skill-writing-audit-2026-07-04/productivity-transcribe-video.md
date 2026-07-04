# transcribe-video

## Whisper-model preference persistence mechanism (undefined "memory", no confirm-before-write, no state home)

**Gap:** Step 3 ("Model selection") says to "Check memory for a saved `whisper-model` preference" and, if absent, to "save the choice to memory as a user preference keyed `whisper-model`". "Memory" is never defined — there's no named tool, no fallback for environments without one, no user confirmation before the first write, and it doesn't use this repo's established per-project state home (`.draekien/.skillsrc`, see `specs/skillsrc.md` and `CLAUDE.md`'s Project Configuration Conventions). This trips three separate rules in `skills/drafting/skill-writing/references/stateful-skills.md`: "One state home," "Confirm before first write," and "Script-mediated access" (plus "Document every key").

**Why it's a tradeoff, not a clear-cut fix:** There are two materially different, defensible designs, and picking one is an architectural decision, not a copy edit:

1. **Migrate to `.draekien/.skillsrc`** (the repo convention used by every other stateful skill, e.g. `module-design`, `get-specific`). This requires: bundling a new `scripts/skillsrc.py` implementing the documented `get`/`set` interface, registering `whisper-model` (or a camelCase `whisperModel`) in `specs/skillsrc.md`'s Registered Keys table with type/default, and adding an explicit confirm-before-write step. This treats the preference as durable, version-controlled, per-project config — plausible for a model-size choice that's really a machine/hardware tradeoff (tied to the GPU detected in Step 2), not a personal one.
2. **Name an actual memory tool** (e.g. `mcp__membank__query_memory` / `mcp__membank__save_memory`) with an explicit fallback ("if no memory tool is available, skip/proceed without saving"). This treats the preference as a cross-project user preference, session-portable, and doesn't require adding a new bundled script or repo-config registration. No other skill in this repo currently uses a memory tool this way, so this would be a first precedent rather than following an established pattern.

Which is correct depends on whether "which whisper model to use" is scoped to *this project* (favors `.skillsrc`) or to *this user across all projects* (favors a memory tool) — a product decision I can't make unilaterally, and it also determines whether "Confirm before first write" needs its own step or is inherited from the `.skillsrc` write protocol.

**Recommendation:** Migrate to `.draekien/.skillsrc` (option 1). The preference is really about hardware capability (GPU vs. CPU, download-size tolerance) discovered per machine/project, which fits "per-project configuration" better than a cross-project user trait, and it keeps the skill consistent with every other stateful skill in this repo instead of introducing a second, unprecedented state mechanism.

**Alternative:** Adopt a named memory tool (e.g. `mcp__membank__*`) with an explicit no-tool-available fallback, if the intent is genuinely a cross-project preference that should follow the user rather than the repo.

## Optional: script output format for the transcript path

**Gap:** `scripts/transcribe.py` prints the transcript path as a bare line (`print(str(transcript))`) rather than structured output (e.g. `{"transcript_path": "..."}`), a minor deviation from `script-design.md`'s output-format preference for composability.

**Why it's a tradeoff, not a clear-cut fix:** The payload is a single scalar value, and `SKILL.md` Step 5 already documents "the script prints the exact output path on success" as the contract the calling agent relies on. Switching to JSON adds a parsing step and a behavior change to a script whose only consumer (per this skill's own instructions) reads the line verbatim; it trades a small composability gain for added complexity, which cuts against the "simplicity first: minimum code that solves a problem" principle when there is no current second consumer that needs structured output.

**Recommendation:** Leave as-is (bare path line). Revisit only if a second consumer of this script's output emerges that needs machine parsing beyond a single path.

**Alternative:** Change to a small JSON object (`{"transcript_path": "..."}`) for strict conformance with `script-design.md`, updating `SKILL.md` Step 5's wording to match.
