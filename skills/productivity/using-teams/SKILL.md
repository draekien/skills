---
name: using-teams
description: Runs an agent team you lead — engineering, review, debugging, research, or a team the project saved — for work that splits into owned slices whose owners must coordinate. `new` defines a team for the project.
argument-hint: "[new] [--team <name>] [request-or-description]"
compatibility: Running a team requires Claude Code with agent teams enabled (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1). Defining one with `new` does not.
disable-model-invocation: true
---

You are the **leader** of a team of members, each running in its own context. You own the plan, the shared decisions, and the final verification; members own the work. A team costs several times what one agent costs, and buys parallel work and members who check each other — so every team carries a **stop condition**, and you keep the team as small as the request allows.

Every team is defined by a **team file** with the same sections: a `Use for` line, then Roster, Task graph, Messaging, Review and Stop. The layout is [assets/team-template.md](assets/team-template.md). The roster's leader row is you; never spawn it. A **task** is always an entry in the task graph; what the user asked for is the **request**.

## Route

The first word `new` selects **Define**. Anything else is **Run**. `--team <name>` names the team; the remaining text is the request, or under `new` the description of the team.

## Run

### Check teams are available

Before anything else, confirm `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is `1` in your environment and that your tools let you spawn named members and message them — check without spawning anyone. If either fails, stop and tell the user which one failed. An unset variable is fixed by setting `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in their shell or in the `env` block of their settings and starting a new session. Missing tools with the variable set mean the session cannot host a team — non-interactive and SDK-hosted sessions never spawn members — so the request has to be run from an interactive terminal session. Do not fall back to subagents — members who cannot message each other are not a team.

Then note whether you can create and update shared tasks, searching your deferred tools too. The answer decides how the task graph runs in Staff the team; it is not a reason to stop.

### Resolve the team

A team name resolves to the first file that exists:

1. `.draekien/using-teams/<name>.md` at the project root — a saved team, which hides the built-in team of the same name.
2. `references/<name>.md` in this skill — a built-in team.

- **`--team` given, no file found** — list every saved and built-in team name and stop.
- **No `--team`** — read only the `Use for` line of each saved team file and of each built-in team file not hidden by a saved one, and pick the team whose `Use for` matches the request and whose `Not for` does not. When nothing fits, say so and stop; a request with no matching team is usually one agent's work.

Read the resolved team file in full. For a saved team, confirm every path and command it names still exists; report any that do not and stop, since a stale path makes a wrong ownership boundary and a stale command makes an unreachable Stop.

### Staff the team

Size each role to the request within the roster's count range — the low end unless the request has more independent slices than that. Three focused members outperform five with overlapping slices, and every member adds a context to brief and a report to read.

Choose each member's model with the `picking-models` skill, classifying by the roster's `Work` column. Write each spawn prompt as a brief with delivery instruction per the `using-subagents` skill. Both ship in `productivity-skills`: `/plugin install productivity-skills@draekien-skills`, or `npx skills add draekien/skills --skill "picking-models"` and `npx skills add draekien/skills --skill "using-subagents"`. If either is missing, ask the user to install it.

Members do not inherit your conversation; the spawn prompt is the only context a member has. Beyond the brief, each spawn prompt carries:

- **The roster** — every member's name and what each owns, so a member knows whom to message about what.
- **Its messaging lines** — every Messaging entry whose sender or recipient is its role, `every member`, or `every <its role>`, copied verbatim.
- **Its owned slice and access** — what it may write, and that everything else is read-only to it.
- **The done signal** — a message to the leader, sent only after it has replied to every message it received that asked for a reply.

Settle every decision that more than one member depends on — interfaces, file ownership, the review target, the hypothesis list — and write it into each affected spawn prompt. Members deciding a shared question in parallel produce work that does not fit together.

Then show the user the team name, the path it was loaded from, and each member you intend to spawn with its owned slice. Spawn only after the user confirms. Run the task graph one of two ways:

- **With shared tasks** — create the graph as shared tasks with their dependencies as members spawn, so members claim unblocked tasks instead of waiting to be told.
- **Without shared tasks** — write each member's tasks and their blockers into its spawn prompt, and tell the member to message you when each task completes. You track the graph; when every blocker of a task is complete, message its member that the task is unblocked.

Staffing is done when every spawn prompt carries the brief, the roster, its messaging lines, its slice and access, and the done signal; every shared decision is written into each affected spawn prompt; and the task graph exists with its dependencies, as shared tasks or in the spawn prompts.

### Lead

- **Do not do members' work.** If you start implementing, members go idle and you edit files they own. Your work is unblocking, deciding, and verifying.
- **Route questions to the owner.** When a member asks you something another member owns, tell it to message that member directly. Answer yourself only what the roster gives to the leader.
- **Stop collisions early.** Two members editing the same path, or two members working the same question, means a slice boundary was wrong: stop one of them and redraw the boundary.
- **Break loops.** A member repeating a task it already completed, or two members trading the same messages without new evidence, will not converge on its own: step in with a decision or a narrower task.
- **Recover stalled members.** A member that stops on an error is idle, not finished: send it the fix or the decision it lacks, or reassign its task.

### Close

The team is done only when the team file's Stop condition holds — not when members go quiet, and not when most tasks are complete. Then run these steps, skipping to step 3 on a Stop without success:

1. Check the combined result against the request, not only against the task graph; a team can complete every task and still miss the request. A gap becomes a new task for the member who owns that slice.
2. Reconcile and re-verify the combined result per the Reconcile section of `using-subagents`.
3. Send every member a shutdown request, and confirm each one has shut down.
4. Report to the user: the outcome, the Stop condition evidence, and anything unfinished.

## Define

`new` writes `.draekien/using-teams/<name>.md`. A name is required; ask for one in kebab-case if `--team` is missing. Defining a team does not need agent teams enabled.

1. **Start from the closest existing file.** An existing saved team of that name, then a built-in team of that name, then [assets/team-template.md](assets/team-template.md).
2. **Draft every section** from the description and from the project: explore its directory layout, test, build and lint commands, and CI config, so roles own real paths and the Review and Stop sections name real commands.
3. **Ask only about the gaps** — what neither the description nor the project answers — one question at a time. Review and Stop must each be checkable: a command that exits 0, or a condition a member can confirm. When either is not, ask until it is; these are the sections a vague team fails on.
4. **Show the full draft** and write it only after the user confirms. If `.draekien/` does not exist at the project root, confirm its creation with the user first.

Done when the file has every section of the template, every non-leader role owns a slice no other role owns, every role with a count above 1 says how its members' slices are split, and the Stop section names a condition for ending without success as well as with it.

## Gotchas

- **Plan approval is not a review gate.** Members spawned while you are in plan mode can have their plans approved without you reading them. If a plan needs review, ask the member to send it to you and wait for your reply.
- **Task status lags.** With shared tasks, a task can show in progress after its member has finished. Ask the member before reassigning its task.
- **No nested teams.** A member cannot run a team of its own, and a session runs one team at a time; split work the team cannot hold into a later team, not a sub-team.
- **Members inherit your permission mode.** A member cannot be granted permissions you do not have; a member blocked on a permission is a decision for the user, not a task to route elsewhere.
