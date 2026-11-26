---
name: ship
description: "Takes a <repository name> task from request to merged PR: understand it, design it, implement it, simplify and review it, prove it and raise the PR, babysit the PR until the user merges, then clean up."
argument-hint: "[task-description-or-issue]"
disable-model-invocation: true
metadata:
  generated-by: setup-ship
---

# Ship a task

Run the phases in order. Each ends on a completion criterion; do not start the next phase until it is met.

**Resume** before starting: if this task already has a branch, a design, commits or an open PR, tell the user which phase you infer it is in and why, and wait for their confirmation before skipping **Understand** or **Design** — their completion criteria are user confirmations, which leave no artefact to check. If the task has an open PR, resume at **Babysit**; once the host reports it merged, resume at **Clean up**.

**Missing provider**: if a skill this file calls is not available in your session, stop and give the user its install routes; never do its work from memory.

## Understand

<Provider call, with install routes if user-installed, or inline guidance built from this repository's facts: where tasks come from (issue tracker, task files), which decision records and docs to read for the area the task touches.>

Put every business decision — one that depends on how the user wants the product to work, which no repository source settles — to the user. Technical decisions are yours.

Completion criterion: the user has confirmed the scope (in and out) and the success criteria, each observable in a test or the running app, and no business decision is open.

## Design

Before writing any file, put the work on the task branch. If the task already has one, check it out; otherwise create it: <this repository's branch or worktree convention — the base to branch from, the naming rule, and the check that the working tree is clean before creating>.

<Provider call, or inline guidance: where designs are recorded, at what scale, and the rule for when the code shows the design is wrong.>

Completion criterion: the work is on the task branch, and the design covers every success criterion<, and the provider's gate is passed>.

## Implement

<Provider calls, or inline guidance. Red-green-refactor unless an instruction file names another discipline — cite it here. A bug fix starts from a test that fails before the change. Name the instruction-file rules that apply before edits, by file and section.>

Run `<check commands>`.

Completion criterion: every success criterion maps to a passing test or is listed for **Prove**, and `<check commands>` exit 0.

## Simplify and review

<Provider calls, in order, each reviewing the output of the one before.>

Completion criterion: every finding is applied or recorded with the reason it was not, and `<check commands>` pass on the committed head.

## Prove

<Provider call, or inline guidance: how to run the app or exercise the change, what evidence to capture, how to attach it to the PR.>

Proof is evidence a reviewer can check without re-running the change. Quote counts, exit codes and observed values; show visible behaviour as a screenshot or recording; list every affected behaviour the proof did not exercise under **Not covered**.

Open the PR <with the repository's PR template, or [assets/pr-body.md](assets/pr-body.md)>, titled `<title convention>`.

Completion criterion: the PR is open and its body shows the proof, the check results, the unapplied review findings and the **Not covered** list.

## Babysit

<Provider call or inline guidance for the waiting mechanism. Point to references/ here if the procedure is long.>

When the session offers no way to watch a PR or schedule a wake-up, report the PR's state and end the turn; the user re-invokes `ship` to resume here.

Never merge, approve or close the PR. Respond to each event:

- **A check fails on code the branch changed** → fix it and push.
- **A check fails on code the branch did not touch** → report the check and its failure to the user.
- **A technical review comment** → fix it, push, reply with the commit, and resolve the thread.
- **A review comment you disagree with** → reply with your reasoning and leave the thread open.
- **A review comment that turns on a business decision** → pause and put the decision to the user.

Completion criterion: the host reports the PR merged.

## Clean up

<Repository specifics: scratch and proof-media locations, worktree removal, branch deletion given the host's merged-branch setting, and the tracker's done state.>

Completion criterion: scratch files, proof media, the worktree `ship` created, the local branch and the remote branch are each removed or confirmed absent, and the issue is in its done state.

## Gotchas

<Repository-specific corrections found while generating this skill, one bullet each. Delete this section if there are none.>
