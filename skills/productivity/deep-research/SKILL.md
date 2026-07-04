---
name: deep-research
description: Conducts structured, multi-source research on a topic — interviewing you to pin down scope and constraints, dispatching parallel researchers, and synthesizing a cited report. Use when you need a thorough, well-sourced answer to a complex question.
compatibility: Agent teams mode requires Claude Code with agent teams enabled.
disable-model-invocation: true
---

Runs in two phases: interview to establish scope, then autonomous multi-agent research with a synthesizer report.

## Phase 1 — Interview

Interview the user relentlessly until the topic is fully pinned. Cover:

- The core question or topic
- Scope boundaries (what's in, what's explicitly out)
- Known context or prior work to skip
- Desired depth (quick overview vs. exhaustive)
- Output preference: inline report in the conversation, or written to files in a directory (get a directory path)

Ask one question at a time. If a question can be answered by exploring the project, do that instead of asking.

Stop only when scope is unambiguous and output preference is confirmed.

## Phase 2 — Decompose

Break the topic into research angles (typically 3–6). For each angle, state:

- Name
- One-sentence scope
- Likely sources (web, codebase, memory — see Phase 3 source menu)

Present the full angle list to the user and ask for confirmation — they may add, remove, or reframe angles. Do not spawn any agents until confirmed. If the user rejects the list entirely, re-decompose based on their feedback and present a revised list; repeat until confirmed.

## Phase 3 — Research

### Source menu

Researchers pick sources adaptively based on their angle:

- **Web** — search the web and fetch pages for articles, documentation, papers, announcements
- **Codebase** — search and read local project files for context (relevant when topic is code-adjacent)
- **Memory** — query available memory tools (e.g. mcp__membank__query_memory) for prior relevant context. Skip this source if no memory tools are available in the current environment.

### Researcher mode — select before spawning

If direct agent-to-agent messaging is available: Mode B. Otherwise: Mode A. If unsure, ask the user whether agents in their environment can message each other directly.

### Mode A — Parallel subagents (default)

Spawn one subagent per confirmed angle.

Each subagent receives its angle, scope, and the source menu. All run in parallel. Collect all outputs when complete.

### Mode B — Agent teams (use when available)

Researchers can message each other directly, surfacing cross-cutting findings without waiting for the synthesis phase.

Create a researcher team with one teammate per confirmed angle.

Each researcher receives:

- Their assigned angle and scope
- The names of all other researchers and the lead
- The source menu
- Instructions: research their angle adaptively, send cross-cutting findings to relevant peers via direct message, escalate blockers to the lead via direct message, and send the lead a direct message containing only the word DONE when their angle is exhausted, then stop

Lead resolves blockers as they arrive: if the blocker is a missing source or access issue, instruct the researcher to skip that source and note it as unresolved; if the angle itself is unresolvable, mark it unresolved, notify the researcher to stop, and include it in the synthesizer brief as an Open Question. Wait until all researchers have sent DONE, then collect all outputs.

## Phase 4 — Synthesize

Spawn a separate synthesizer subagent. Pass it: (1) each researcher's output labelled with its angle name, (2) the original topic verbatim, (3) the confirmed angle list, (4) the output preference. Instruct it to produce a report with these sections, in this order: (1) Executive Summary — 2–4 sentences answering the core question; (2) Findings — one section per research angle with key facts, evidence, and notable sources; (3) Cross-cutting Themes — patterns or tensions across multiple angles; (4) Open Questions — gaps the research could not resolve, including any unresolved angles; (5) Sources — all URLs and file paths cited.

If a researcher returns no output or errors, note the angle as "unresolved" and include it in the synthesizer brief. The synthesizer must surface unresolved angles in Open Questions rather than omitting them.

Synthesizer produces a structured report with these sections:

**Executive summary** — 2–4 sentences answering the core question.

**Findings** — one section per research angle: key facts, evidence, and notable sources.

**Cross-cutting themes** — patterns or tensions that surfaced across multiple angles.

**Open questions** — gaps the research could not resolve.

**Sources** — all URLs and file paths cited.

For directory output the synthesizer also partitions findings by angle and collects a unified source list, ready for Phase 5 file writers.

## Phase 5 — Deliver

- Inline: output the synthesizer report directly in the conversation.
- Directory: spawn parallel writer subagents, one per output file, all writing simultaneously to the user's directory:
  - `overview.md` — executive summary, cross-cutting themes, and open questions
  - One `<angle-name>.md` per research angle — that angle's findings and sources
  - `sources.md` — all URLs and file paths cited across all angles
