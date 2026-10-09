---
name: retro
description: Reviews a coding session's transcript and recommends changes to the agent's environment — navigation pointers, automated checks, review rules, tool economy, information access — so the next session avoids the same mistakes. Applies them with --fix.
argument-hint: "[--fix safe|unsafe]"
disable-model-invocation: true
---

# Retro

A retro **mistake-proofs the environment** the next agent works in, never the code this session produced. A fix in the code holds once; a fix in the environment holds for every later session.

Every finding is **evidence-led**: it cites the transcript moment that shows the problem — a failed call, a retry, a long search, a user correction. Three **absence findings** need no moment: no **guardrail** (no pre-commit hook or CI job running lint, type check, or tests), no review stage (no `/code-review` use, reviewer agent, or CI review step), and a root steering file missing the `REVIEW.md` pointer.

## Read the session

The session is the current one unless the user names another. Read the current session from context while its turns are still there; otherwise find its transcript where your harness stores it, and condense it:

```bash
uv run scripts/condense-session.py <session-id-or-path> --output <tmp-file>
```

Always pass `--output`; a long timeline overflows a tool result. `--list` prints recent sessions. Read `summary` first, then `timeline` in ranges of at most 200 lines. If the script exits non-zero (`3` means the transcript is not `~/.claude/projects` JSONL) or finds no session, read the raw transcript in the same ranges and say no summary was computed. The script records result sizes, not content; re-run a call only when its size cannot settle whether it was wasted.

Done when every error, repeated call, user correction, and largest result is tied to a finding or judged harmless.

## Inventory existing checks

Before proposing a check, inventory what the repo already runs: manifest scripts, pre-commit config, `REVIEW.md`, and CI — any CI system's pipeline config, not only `.github/workflows/`, plus the scripts and templates each pipeline calls. A pipeline can live only on the CI server, so a missing config file does not prove a missing pipeline: ask the user before reporting a missing guardrail or review stage, and mark the finding unverified if they cannot say.

An existing check that is unwired, or passes on the session's mistake, is the finding — wire it rather than build a second. **Reproduce** before concluding: run the check against the mistake, in a scratch copy if it has since been fixed; if it cannot be reproduced, mark the finding unverified and say why.

## Categories

Skip any category the session gave no evidence for; absence findings are checked on every run.

- **Navigation** — slow or wrong file lookups, a missed dependency → a **navigation pointer**: one line in the root steering file naming the file and when to read it. The root steering file is the `CLAUDE.md` or `AGENTS.md` that holds the guidance; if one imports the other, it is the imported one. Pointers are the only content it gains — every agent loads it every turn.
- **Automated checks** — a mistake a linter, type checker, test, or filesystem check would catch.
- **Coding standards** — a broken convention nothing caught:
  - **Mechanical** (a syntactic pattern, banned API, import shape, file location) → a deterministic check in the cheapest existing guardrail. Never a prose rule.
  - **Judgement call** (cross-file consistency, matching surrounding style) → a rule in `REVIEW.md`.
- **Tool economy** — oversized results, repeated calls, a token-heavy CLI or MCP server → the narrower call or tooling change.
- **Information access** — an unreachable fact (dev server logs, service state, a schema) → read-only access.

Judgement rules go to `REVIEW.md` because the reviewer reads them only at review, while the root steering file costs context on every implementer turn. The root steering file gets the pointer `When reviewing a change, read REVIEW.md and apply its rules.` only when a reviewer the repo uses reads the root steering file but not `REVIEW.md` — check `https://code.claude.com/docs/en/code-review.md`, section "What the review reads and edits".

**Hand off** steering-file problems — an ignored rule, a rule that changes nothing, a bloated file — rather than auditing them or running `maintain-agent-docs` yourself: report the evidence with the command for the user to run, `/maintain-agent-docs --scope prune` for lines to remove or `--scope contexts` for rules in the wrong file. If it is missing, install it with `/plugin install context-management-skills@draekien-skills`, or `npx skills add draekien/skills --skill "maintain-agent-docs"`.

## Rank and report

Rank by cost if it recurs: a mistake that reached a commit or only the user caught, then one the agent caught after rework, then wasted calls or tokens alone. Repeats rank higher within a tier; absence findings rank last.

Load `writing-for-agents` before writing any line an agent will read — pointer, rule, check error message. Install it with `/plugin install technical-writing-skills@draekien-skills`, or `npx skills add draekien/skills --skill "writing-for-agents"`.

```markdown
### 1. <category>: <one-line problem>

- **Evidence:** <timestamp> — <the call, error, or correction>, or "absence"
- **Recommendation:** <the exact line, rule, or check to add>
- **Action:** <this finding's cell in the --fix table for the flag this run used>
```

With no findings, say so and name the categories checked.

## Apply with --fix

| Finding | no flag | `--fix safe` | `--fix unsafe` |
| --- | --- | --- | --- |
| Navigation pointer | report | apply | apply |
| Judgement rule to `REVIEW.md`, plus its pointer | report | apply | apply |
| New check for a mechanical violation | report | proposal | build and prove |
| Existing check unwired or broken | report | proposal | wire and prove |
| Tool economy | report | proposal | proposal |
| Information access | report | proposal | proposal |
| Steering-file problem | hand-off | hand-off | hand-off |

**Prove** each check red-green: it fails on the session's mistake and passes on the corrected code. A check that never goes red is removed, not committed. Never apply information access — it touches credentials and external services. Leave applied fixes uncommitted.

Done when every finding is reported, every applied fix names the file it changed, and every built check shows both proof runs.
