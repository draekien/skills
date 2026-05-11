---
name: deep-research
description: 'Conducts structured multi-source research on any topic: relentlessly interviews the user to pin scope and constraints, decomposes into research angles for confirmation, dispatches parallel researchers with adaptive source selection, then synthesizes a final report. Use when thorough, well-sourced answers are needed, or when the user says "deep research", "research this thoroughly", "deep dive into", "investigate", "I need a research report on".'
compatibility: Agent teams mode requires Claude Code with agent teams enabled.
---

Runs in two phases: interview to establish scope, then autonomous multi-agent research with a synthesizer report.

## Phase 1 — Interview

Interview the user relentlessly until the topic is fully pinned. Cover:

- The core question or topic
- Scope boundaries (what's in, what's explicitly out)
- Known context or prior work to skip
- Desired depth (quick overview vs. exhaustive)
- Output preference: inline report in the conversation, or written to a file (get a path)

Ask one question at a time. If a question can be answered by exploring the project, do that instead of asking.

Stop only when scope is unambiguous and output preference is confirmed.

## Phase 2 — Decompose

Break the topic into research angles (typically 3–6). For each angle, state:

- Name
- One-sentence scope
- Likely sources (from the source menu below)

Present the full angle list to the user and ask for confirmation — they may add, remove, or reframe angles. Do not spawn any agents until confirmed.

## Source menu

Researchers pick sources adaptively based on their angle:

- **Web** — search the web and fetch pages for articles, documentation, papers, announcements
- **Codebase** — search and read local project files for context (relevant when topic is code-adjacent)
- **Memory** — query available memory tools for prior relevant context from this project

## Phase 3 — Research

Detect which mode is available and use the highest available:

### Mode B — Agent teams (preferred when available)

Create a researcher team with one teammate per confirmed angle.

Each researcher receives:
- Their assigned angle and scope
- The names of all other researchers and the lead
- The source menu
- Instructions: research their angle adaptively, send cross-cutting findings to relevant peers via direct message, escalate blockers to the lead via direct message, and signal "done" to the lead when their angle is exhausted

Lead resolves blockers as they arrive. Wait until all researchers signal "done", then collect all outputs.

### Mode A — Parallel subagents (default)

Spawn one subagent per confirmed angle.

Each subagent receives its angle, scope, and the source menu. All run in parallel. Collect all outputs when complete.

## Phase 4 — Synthesize

Spawn a separate synthesizer subagent with all researcher outputs and the original topic.

Synthesizer produces:

**Executive summary** — 2–4 sentences answering the core question.

**Findings** — one section per research angle: key facts, evidence, and notable sources.

**Cross-cutting themes** — patterns or tensions that surfaced across multiple angles.

**Open questions** — gaps the research could not resolve.

**Sources** — all URLs and file paths cited.

## Phase 5 — Deliver

- Inline: output the synthesizer report directly in the conversation.
- File: write the report to the path the user specified in the interview.
