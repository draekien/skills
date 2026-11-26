---
name: setup-ship
description: Generates or updates a repository's `ship` skill — one user-triggered workflow that takes a task to a merged PR and cleans up — fitted to the installed skills and the repository's AGENTS.md and CLAUDE.md files.
argument-hint: "[create|update] [repo-path]"
disable-model-invocation: true
---

A `ship` skill is a repository's delivery pipeline: seven fixed phases, each with a contract it must meet, and for each phase a **provider** — the skill, built-in command or instruction-file rule that does the work in this environment. The generated skill composes, never reimplements: a phase with a provider calls it, and only a phase with no provider carries inline guidance. Its value is the phase-to-provider mapping plus the repository facts an agent would otherwise rediscover on every run.

The repository is `repo-path`, or the current working directory when none is given.

## Route

An explicit subcommand wins. Otherwise: **create** when the repository has no `ship` skill, **update** when it has one whose frontmatter carries `metadata.generated-by: setup-ship`. When a `ship` skill exists without that marker, someone wrote it by hand — show the user what it covers and ask whether to replace it, update it in place, or stop.

Both modes end by handing the skill to `writing-skills`, which ships in the same plugin as this skill (`/plugin install meta-skills@draekien-skills`, or `npx skills add draekien/skills --skill "writing-skills"`). If it is not available, ask the user to install it before writing anything.

## Inventory

Explore four surfaces and record every fact with the location it came from. A fact you looked for and did not find is recorded as "not found" with the places searched — never inferred.

- **Skills** — the skills and built-in commands listed as available in your session, the repository's project skill directories, and any skills lock file. For each, note what it does (from its description), which phases it could serve, and whether it is **project-local** (committed to the repository, so every collaborator has it) or **user-installed** (present on this machine only).
- **Instruction files** — every `AGENTS.md` and `CLAUDE.md`: root, nested, user-level, and the files they import. Extract what bears on a phase: skills they mandate before certain edits, commit and branch conventions, check commands, where designs and decision records live, worktree rules, and prohibitions.
- **Repository mechanics** — default branch, hosting service and whether its CLI is authenticated, CI workflows and which checks are required, PR template, issue tracker and its states, the check commands (lint, typecheck, test, build), how to run the app for proof, merge method and whether the host deletes merged branches.
- **Session capabilities** — what your session offers for waiting on a PR: watching a PR, scheduling a wake-up, or monitoring a background command.

An existing pipeline skill — one project skill that covers several phases, such as a raise-PR gate that reviews, proves and opens the PR — is a single provider for every phase it covers. The `ship` skill calls it once at the first phase it covers; never split its work across phases or restate its steps.

Done when every phase in the map below has a provider with a cited location, or is a gap with the places searched.

## Phase contracts

Each phase meets its contract whatever the provider. The contract is the user's policy — write it into the generated skill unchanged, as the phase's completion criterion and rules. Provider precedence, highest first: an instruction-file rule that mandates a skill or process for the phase, a project-local skill, a user-installed skill, inline guidance.

| Phase | Contract |
| --- | --- |
| **Understand** | Goal, scope (in and out), and success criteria each observable in a test or the running app. Every business decision — one that depends on how the user wants the product to work, which no repository source settles — is put to the user; technical decisions are the agent's. Done when the user has confirmed scope and criteria and no business decision is open. |
| **Design** | An implementation design at the scale of the change, recorded where the repository keeps designs, or in chat when it keeps none. Done when the design covers every success criterion and the provider's own gate, if it has one, is passed. |
| **Implement** | **Red-green-refactor** unless an instruction file mandates another discipline; a bug fix starts from a test that fails before the change. Done when every success criterion maps to a passing test or is listed for **Prove**, and the check commands exit 0. |
| **Simplify and review** | Quality passes over the branch diff, applied in order, each reviewing the output of the one before. Done when every finding is applied or recorded with the reason it was not, and the checks still pass on the committed head. |
| **Prove** | Evidence a reviewer can check without re-running the change: quoted counts, exit codes and observed values, screenshots or recordings for visible behaviour, and a **Not covered** list of affected behaviour the proof did not exercise. The PR body carries the evidence, attached, and the title follows the repository's convention. Done when the PR is open and its body shows the proof. |
| **Babysit** | Runs until the user merges; the agent never merges, approves or closes. A failing check caused by the branch is fixed and pushed; one failing on code the branch did not touch is reported. A technical review comment is fixed, pushed, replied to with the commit, and resolved; one the agent disagrees with gets a reply with its reasoning and stays open; one that turns on a business decision pauses the run for the user. Waiting uses the session's PR-watch or wake-up capability; with none, report the PR's state and end the turn — re-invoking `ship` resumes. Done when the host reports the PR merged. |
| **Clean up** | Starts only after the merge is observed. Removes scratch files and proof media, the worktree if `ship` created one, the local branch, the remote branch unless the host already deleted it, and moves the issue to its done state. Done when each item is removed or confirmed absent. |

## Fill the gaps

Search the [draekien/skills](https://github.com/draekien/skills) catalogue — its bucket `README.md` files list every skill with a one-line description — for a skill that covers each gap; another marketplace the user names may be searched instead. Put every gap to the user in one question: the phase, the candidate skill, and its install routes (`/plugin install <bucket>-skills@draekien-skills` and `npx skills add draekien/skills --skill "<skill-name>"`). An installed candidate becomes the provider. A declined one leaves the phase on inline guidance, written from the inventory's repository facts — the actual commands, paths and conventions — never generic advice the agent already follows.

Put any other decision the inventory cannot settle to the user one at a time, with a recommendation — through `get-aligned` when it is available (`/plugin install productivity-skills@draekien-skills`, or `npx skills add draekien/skills --skill "get-aligned"`).

Done when every phase has a provider or confirmed inline guidance, and no decision is open.

## Create

Copy [assets/ship-template.md](assets/ship-template.md) to `ship/SKILL.md` in the directory where the repository keeps its hand-written project skills — not a directory an installer manages through a lock file — defaulting to `.claude/skills/`. Replace every `<...>` placeholder; leave none.

- **Point to instruction files; never copy their rules.** They load in every session already, and a copy drifts from its source. Write "invoke the skills the root `CLAUDE.md` mandatory-skill table requires", not the table.
- **Every user-installed provider gets its install routes** beside its name, so a collaborator without it is told how to get it. Project-local providers need none.
- **Defer what only some runs reach.** A long babysit procedure or proof recipe goes in the generated skill's `references/` behind a pointer that names when to read it. When the repository has no PR template, write `assets/pr-body.md` for the generated skill from the **Prove** contract.

## Update

Re-run **Inventory**, then compare it with the existing skill: providers that are gone, newly available skills that fit a phase better than its current provider, changed check commands, and instruction-file rules that moved or changed. Treat every line the old inventory does not explain as a **hand edit**: keep it, and ask the user only when it conflicts with a proposed change. Show the proposed edits as a list and apply them once the user agrees. Re-run **Fill the gaps** for any phase that lost its provider.

## Quality gate

Run `writing-skills review --gate off --fix` on the generated skill directory, and repeat until it reports nothing to fix.

Done when the gate is clean. Then report the phase map to the user — phase, provider, and whether it is project-local, user-installed or inline — and say that `ship` runs only when the user types `/ship`: its frontmatter closes model invocation, so naming it mid-prompt, from a delegated task or from a scheduled run does nothing.

## Gotchas

- **A skill installed during this session may not be listed until a new session starts.** Confirm it by its files on disk, and tell the user to restart before running `ship`.
- **Built-in commands are providers only if your session lists them.** A review command present in one harness is absent in another; record it as the provider only after seeing it listed, and name the gap it leaves for collaborators who run a different harness.
- **The `metadata.generated-by` marker is how update finds its own output.** Never remove it from the template.
