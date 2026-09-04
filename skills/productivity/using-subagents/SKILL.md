---
name: using-subagents
description: Orchestrates subagents so their work actually comes back — cutting the task at real seams, briefing each agent with an explicit delivery instruction, rescuing agents that go idle holding finished work, and isolating concurrent writers in worktrees. Use when fanning work out to parallel subagents, when a dispatched agent never returns its findings, or when the user says "using subagents", "using agent teams", "act as a team lead", "run these in parallel", "my agents aren't reporting back".
argument-hint: "[task to delegate]"
---

Every delegation failure traces to one root cause: **a subagent starts from zero and ends with a single message.** Brief for the zero, specify the message, and most of the rest follows.

The message half is where fan-outs die. Agents do the work, write the findings into their own output, end their turn, and the findings go nowhere. **A report format tells an agent what to write. Only a delivery instruction tells it where to put it.** Every brief needs both.

Choose each agent's model with the `picking-models` skill. Never leave the model unset.

## Seams

One test decides where to cut: **can each piece be verified without the other's output?** If B cannot start until A lands, that is not a seam — it is a phase.

**Good seams:**

- **Disjoint file ownership** — the strongest predictor of a clean merge. Write the ownership into the brief: "You own `src/parser/`. Do not edit anything outside it."
- **Independent questions** — investigations parallelise almost for free. "Where are retries configured" and "why does the CI cache miss" never collide.
- **Mechanical fan-out** — the same transform over many targets, where briefs are identical but for the target list. Integration is trivial.

**Bad seams:**

- **Split by phase** — one agent designs, another implements. The implementer inherits none of the designer's context; you pay the context transfer twice and get drift.
- **Split one feature by layer** — one agent does the endpoint, another the caller. The interface between them churns mid-task and both rework. If two pieces must agree on an interface, fix the interface yourself first, put the exact signature in both briefs, then split.
- **Split for speed alone** — work that runs twenty minutes serially takes longer as two agents plus integration.

Run **two to four agents concurrently** for real work. Your review attention is the bottleneck, not agent capacity: every running agent is a report you must read critically and claims you must spot-check. Past four you start skimming, and a skimmed report is where wrong results get through.

Mechanical fan-out is the one exception, because its review is mechanical too: when the briefs are identical but for the target and one command verifies the union, go as wide as there are targets and verify by re-running that command rather than by reading every report. If each report needs judging on its own merits, you are back to four.

Do not manufacture parallelism. Keep the serial spine yourself — the decisions, the interface, the risky migration step — and fan out the leaves. Depth does not divide, and if waiting on a dispatched agent feels intolerable, the task was too small to delegate.

## The brief

Each agent gets, in this order — the goal anchors everything after it, and delivery sits last so it is the instruction freshest in the agent's context when it finishes:

1. **The goal as an end state**, one sentence. "When you are done, `<command>` exits 0 and every module in `<dir>` is accounted for" — not "work on the modules".
2. **Context it cannot discover**, especially **negative knowledge**: the dead ends you already hit. "Do not try X; it conflicts with Y and fails to load." Rediscovering your dead ends is the most expensive thing you can let an agent do.
3. **Pointers, not payloads.** Give addresses — file paths, symbol names, a starting line: "Start at `src/router.ts:142`, the `resolveRoute` function." An address costs ten tokens; pasted file contents cost thousands and go stale. The agent has tools; let it read. Paste only what it cannot fetch — a diff, an error message, the user's own words.
4. **The scope fence**, as files and as behaviours: "Do not refactor adjacent code, do not fix unrelated lint, do not add tests I did not ask for."
5. **The completion criterion** — see below.
6. **The blocked-path instruction**: "If something is missing or a command is denied, stop. Do not improvise a workaround."
7. **The report format** — what to write, including a mandatory *anything you skipped and why* section. Agents fill in a section that exists far more reliably than they volunteer omissions.
8. **The delivery instruction** — where to put it.

Leave the method open. Constrain the *what* and the *boundaries* tightly; leave the *how* to the agent. A step-by-step recipe gets followed instead of the goal, and when step three does not apply the agent either forces it or stalls. Where you must prescribe, state the reason as well as the rule.

Re-read every brief cold, as a stranger, before sending. An agent confidently answering a slightly different question is the symptom of a brief that assumed shared context — and the fix is yours, not the agent's.

When a task genuinely needs your whole conversation state, dispatch a **fork** (`subagent_type: "fork"`) rather than writing a summary; the fork inherits your context and your summary would be lossy. Fresh agent for self-contained work, fork for context-heavy continuation. There is no workable middle option: half your context is always the wrong half.

### Completion criteria

Make done **binary and checkable by the agent itself**, so it can loop until true and stop when true.

- **Code** — a command, not a vibe: "Done when `<command>` exits 0 and you have pasted its output." "Make it robust" is an invitation to gold-plate.
- **Research** — a coverage bound, not an answer requirement: "Check `<these locations>`. Cite a location for every claim. If it is not there, report 'not found in those locations'. Do not widen the search." Without the bound, an agent that cannot find the answer either searches forever or invents one.
- **Against gold-plating** — "Any file changed outside the list above means the task failed, even if the tests pass" and "Do not add improvements I did not ask for; note them in your report instead." That second clause matters: it gives the agent somewhere to put its initiative other than your diff.
- **Against stopping early** — "Pre-existing test failures: report them and continue; they do not block you." Agents stop on the first anomaly they did not cause.

## Delivery

Two paths carry a subagent's work back to you. Establish which one you are on **before** dispatching, because the brief differs.

- **Relayed return** — you dispatch, and the agent's final message comes back as the dispatch result or a completion notification. The transport is automatic. Its tool outputs and intermediate reasoning still do not reach you.
- **Mailbox** — the agent runs in the background or as a named teammate. Its plain text output is invisible to you. Only an explicit message call addressed to you arrives.

Tell them apart by what your toolset holds: an agent-to-agent messaging tool alongside an agent-listing tool means mailbox delivery is in play. Dispatch that returns only a handle rather than a result confirms it.

**When in doubt, brief for mailbox.** A redundant delivery instruction on a relayed-return harness wastes one sentence. A missing one on a mailbox harness silently voids the entire fan-out.

### The delivery instruction

Five parts. Weakening any one reintroduces the failure.

1. **Name the destination.** On mailbox, the tool and the address: `call SendMessage with to: "main"` — not "report back", not "send me your findings", not "deliver your report". Vague verbs are exactly what fail. On relayed return the equivalent is "your final message is the deliverable".
2. **Name the field the content goes in.** `put the findings in the message field as plain text, in full` — otherwise the agent sends a note saying the work is finished and keeps the work.
3. **Rule out a file.** `Do not write your findings to a file.` You will not go hunting for a report file, and a file the agent writes for you is a report you never read.
4. **Close the exit.** `Do not end your turn without making that call.` Ending the turn is the agent's default; the instruction has to override it explicitly.
5. **Say why.** `Your plain text output is not visible to me.` An agent that understands the reason applies it to cases the brief did not anticipate.

Put all five in the brief you dispatch with. A delivery instruction issued afterwards works, but it costs a round trip per agent and you will not always notice you need one.

## Rescue

An agent that finished and went idle without reporting looks like a broken transport. The trigger is a **received** signal, never elapsed time — an agent still working is not an agent to rescue. Read the signals together:

- A completion or idle notification arrives with no content attached.
- The listing tool reports the agent unreachable, or omits it entirely. **Trust the send, not the listing** — a send can still arrive at an agent the listing left out, so try one by name before believing it.
- Every agent in the batch has signalled idle and none delivered anything.

A whole batch idle and empty at once is diagnostic. Transports do not fail uniformly; a brief missing its delivery instruction does.

**Never re-dispatch a task whose agent you can still reach.** The work is finished and sitting in that agent's context. Re-running pays for it twice and can return a different answer you then have to arbitrate against nothing. Sending to an idle agent by name resumes it from its transcript — which is why rescue is cheap and re-dispatch is not.

Rescue needs that channel. With no agent-to-agent messaging tool you cannot resume an idle agent and the steps below do not apply — an empty relayed return is unrecoverable. Fix the brief, then re-dispatch and accept paying for the work twice. That is the only case where re-dispatch comes before a rescue attempt, and it is the strongest reason to brief for mailbox by default.

Two steps, in order:

1. **Rescue one agent first.** Send it the five-part delivery instruction, plus a line that the work is already done — "do not redo the work; this is a delivery problem only". Without that line the agent may start over.
2. **Confirm it produced a full report, then re-brief the rest with that identical wording.** Spending the round trip on the whole batch before the wording is proven risks paying for every agent for nothing.

Then respond to what comes back:

- **A rescue that returns nothing** — sharpen the wording. Do not resend the same words, and do not change the model; a delivery failure is not a capability failure. Escalate specificity, not politeness or urgency: "Please send your final report now" fails for the same reason the brief did, because it still does not name the mechanism.
- **An agent that no longer holds the text** — ask it to reconstruct from its own transcript, never to redo the investigation.
- **A second sharpened attempt that also returns nothing** — stop. Record the agent as unresolved and name the slice that has no result. Do not keep rewording, and do not hand the slice to a fresh agent until you have fixed the brief that caused the silence.

## Isolation

Worktrees exist to stop concurrent **writes** from colliding. Give an agent its own worktree when:

- **Two or more agents write concurrently** and their file ownership cannot be made provably disjoint — shared config, lockfiles, generated files, or builds writing to shared output directories.
- **An agent runs state-mutating verification** — builds, installs, codegen, migrations: anything that dirties the tree beyond its own edits.
- **An agent needs to switch branches, stash, or commit.**
- **The work is speculative** — "try this approach, I may throw it away". A worktree makes discarding free: you delete it instead of unpicking edits.
- **You want each agent's diff reviewable on its own.**

Worktrees are overkill for read-only investigation (nothing to isolate), for a single writer making ordinary edits (the tree is already its worktree), and for genuinely disjoint text edits. The triggers above win over this list, even for a lone agent. A worktree costs a merge step at the end — do not pay it for nothing.

One worktree per writer, never shared between two. Reconcile the branches yourself; a worktree's value is that its diff arrives intact.

**Signs you needed isolation and did not have it:**

- A diff you cannot attribute to any one agent.
- One agent's tests failing because another's in-progress edit broke the build.
- Dependency or lockfile thrash between agents.
- Git operations failing on index contention.
- An agent reporting that a file already contains the change it was about to make.
- Working-tree noise mid-task that makes your own spot-checks unreliable.

Any one of those, once, means worktrees for that shape of task from then on.

## Reconcile

You merge. Agents never merge each other's work.

1. **Read each report against the tree, not on faith.** Re-run the verification command yourself for anything load-bearing, and spot-check one or two cited locations. A success report with no pasted output is not evidence — send it back asking for the command output. Cheap, and it catches fabrication before it compounds.
2. **Audit the fence.** Compare the files actually changed against the scope fence in the brief. A five-second check that catches scope creep.
3. **Merge in dependency order.** Disjoint-ownership results usually coexist untouched. Worktree results you diff and merge yourself, rebasing the smaller change onto the larger. Conflicts in shared files are yours to resolve, because only you hold both agents' intents.
4. **On contradictions, never average and never vote.** First re-read both briefs: two agents disagreeing usually answered slightly different questions. If the briefs match, check the primary source yourself, or send one targeted follow-up to whichever agent's claim is cheaper to verify — quote the other agent's finding and ask which wins, with the chain of reasoning. Do not dispatch a third agent to arbitrate; it has no better access to the truth than you do.
5. **Re-verify the union.** Each agent verified its own slice; nobody verified the combination. Integration bugs live exactly in the gaps between slices, and no subagent owns the gaps.
6. **Carry the gaps forward.** An agent that returned nothing, or returned partial work, is an open question in what you reconcile — not an omission.

## Gotchas

- **Do not touch files inside a running agent's fence**, and do not launch a second agent onto an area the first has not finished. Both leave an agent working from a tree that has since changed.
- **An agent that cannot find the answer may invent one.** State in the brief that "not found" is an acceptable answer; without that, silence is the only failure mode left to it.
- **Permissions do not travel.** Never route work to another agent because it was denied in your own session.

Delegation is done when every agent's findings are in your context, every dispatched agent has either reported or been explicitly recorded as unresolved, the union has been verified, and no completed work was run twice.
