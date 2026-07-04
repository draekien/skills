# get-specific

## Free-form text output vs. structured (JSON/CSV/TSV) output in query.py/write.py

`scripts/query.py` and `scripts/write.py` emit hand-formatted prose (`cmd_list_contexts`, `cmd_lookup`, `_print_term`, `cmd_list`, and the success messages in `write.py`) rather than structured output, which nominally violates script-design.md's "prefer structured output over free-form text" rule.

**Why it's a tradeoff, not a clean fix:** the current prose output serves two audiences at once — it is read by the agent to load context (Session Start step 2, Conflict Detection) and it is also meant to be shown to the user in a readable form (e.g. `_print_term`'s `### Name [Context]` formatting, `cmd_list`'s pagination hint). Switching to JSON would make agent parsing more reliable but would require the agent (or the scripts) to re-render that JSON into prose for the user, adding a translation step and touching every call site and success-message string across two scripts. It's a real design choice about who scripts are optimized for, not a mechanical formatting fix.

**Recommendation:** switch `query.py`'s read commands to emit JSON (list-contexts, lookup, list are consumed programmatically far more than they're read raw by the user), but leave `write.py`'s success/failure messages as short human-readable prose, since they're terminal confirmations, not data the agent needs to parse further.

**Alternative(s):** (a) leave all four scripts as-is, accepting the script-design.md deviation, since the agent has tolerated prose output fine so far; (b) add a `--json` flag to `query.py` so both audiences are served without breaking existing invocations documented in references/ubiquitous-language-format.md.

## `scripts/skillsrc.py set` subcommand is unreachable from the documented workflow

`skillsrc.py` implements a `set` subcommand (lines 42-46, 58) for writing a custom `dictionaryPath`, but neither SKILL.md's Session Start nor references/ubiquitous-language-format.md's Script Invocation section ever calls it — Session Start only ever calls `get`. The capability exists in the script but has no invocation path in the skill.

**Why it's a tradeoff, not a clean fix:** there are two legitimate resolutions with different implications. Adding an invocation path means deciding *when* to offer it (every Session Start? only when the user asks to relocate the dictionary?) and what confirmation/UX it needs, which is new process logic, not a bug fix. Removing the `set` subcommand instead is a capability cut that a user relying on manual `.skillsrc` edits plus `set` (e.g. from another tool or script) would lose, and per skill-writing's rule, existing capability should never be silently dropped without flagging.

**Recommendation:** add a small Session Start branch: if the user wants a non-default dictionary location, invoke `skillsrc.py --config .draekien/.skillsrc set <path>` once, before step 1's `get` call in that same session. This keeps the capability reachable without adding it to every session's default path.

**Alternative(s):** (a) remove `cmd_set` and the `set` subparser entirely if no near-term need for a configurable path is anticipated, shrinking the script to only what's used; (b) leave it undocumented as an escape hatch for manual `.skillsrc` maintenance outside the skill's own flow.

## No stated precedence when multiple hard-interrupt conditions fire in the same response

Term Capture (semantic contradiction, step 3) and Conflict Detection (Definition conflict, Cross-context collision, Vague language) all run "concurrently" every response per the Active Behaviors header, and each independently defines its own hard-interrupt trigger, but SKILL.md never states what happens if two or more fire in the same response.

**Why it's a tradeoff, not a clean fix:** any ordering choice is substantive process logic, not a wording correction — it changes what the user sees first and can change downstream state (e.g. resolving a Definition conflict first might retroactively resolve a Vague language match). Picking an order requires domain judgment about which ambiguity is most likely to invalidate the others, which isn't implied by the existing text.

**Recommendation:** resolve Definition conflict first (it's the most authoritative signal — a term already has a canonical definition being contradicted), then Cross-context collision, then Vague language, then Term Capture's semantic contradiction — surfacing only the highest-priority interrupt per response and re-evaluating the rest afterward.

**Alternative(s):** (a) surface all firing interrupts together in one message instead of picking a single priority order, trading a more complex single turn for no re-evaluation step; (b) leave the concurrency model as-is and rely on the low real-world likelihood of simultaneous triggers, treating this as an edge case not worth codifying.
