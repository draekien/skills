# deep-research

## Inconsistent leading term for the per-angle researcher role (subagent / researcher / teammate)

**Gap:** The role of "the agent researching one angle" is named differently depending on mode: Mode A calls it "subagent" (line 50: "Spawn one subagent per confirmed angle. Each subagent receives..."), Mode B calls it "teammate" when introducing it and then "researcher" for the rest of that section (line 58: "Create a researcher team with one teammate per confirmed angle." / line 60: "Each researcher receives:"), and Phase 4 uses "researcher" again (line 71: "each researcher's output labelled with its angle name"). This violates skill-writing's one-term-per-concept guidance.

**Why it's a tradeoff:** This is a rename of an established leading term across a live, working document, not a mechanical fix. There are at least three viable target terms ("researcher," "subagent," "teammate"), each with a different framing:

- "researcher" is mode-agnostic and already dominant in Mode B and Phase 4, but somewhat generic.
- "subagent" is precise about the spawning mechanism in Mode A but doesn't fit Mode B's team-message-passing model, where "subagent" is a less natural description of a teammate.
- "teammate" fits Mode B's framing (agent teams) but is wrong for Mode A, which has no team.

Any single global term either overwrites mode-specific vocabulary that may be intentional (the two modes are structurally different — parallel isolated subagents vs. a communicating team — and the term difference may be signaling that), or requires threading a parenthetical clarification through both Mode A and Mode B, which is itself a judgment call about how much scaffolding to add. Silently picking one and rewriting both modes risks erasing a deliberate distinction the original author drew between the two execution models.

**Recommendation:** Standardize on "researcher" as the leading term for the role in both modes (it already wins 3-to-1 in the current text and is mode-agnostic), and reserve "subagent" / "teammate" only for the sentence that names the spawning mechanism itself, e.g.:

- Mode A: "Spawn one researcher (as a subagent) per confirmed angle. Each researcher receives..."
- Mode B: "Create a researcher team with one researcher (teammate) per confirmed angle."

**Alternatives:**

- Leave the terms mode-specific as-is, on the theory that "subagent" vs. "teammate" usefully signals which execution model is in play at each mention — accept the minor inconsistency as intentional signal rather than sediment.
- Standardize on "subagent" everywhere (including Mode B), treating "teammate" as Mode B's spawning mechanism only — but this reads oddly since Mode B's whole premise is that these are cooperating team members, not isolated subagents.
