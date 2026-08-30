---
name: prune-local-branches
description: Prunes local git branches whose work already reached the base branch, ranking evidence so squash-merged branches are not mistaken for unmerged work. Use when local branches have piled up, after merging a run of pull requests, or when the user says "delete merged branches", "clean up branches", "prune local branches", or asks about stale or orphaned branches.
argument-hint: "[base-branch]"
---

Delete a branch only when its work is provably in the base branch, and record enough to restore anything deleted in error. A branch you cannot prove is merged stays.

## Available scripts

- **`scripts/classify.py`** — classifies every local branch against the base branch and prints the recovery record

## Evidence ladder

The trap is that the obvious signals lie in the same direction — they report merged work as unmerged, so acting on them leaves the pile untouched and teaches you to force-delete instead. Trust in this order:

| Signal | Verdict | Why |
| --- | --- | --- |
| `git merge-base --is-ancestor` | **Decisive** | The commits are reachable from the base branch |
| A merged pull request for the branch | **Decisive** | Proves the work landed even when squashing rewrote it |
| `git branch --merged` | **Partial** | The ancestor test in other clothes; blind to every squash-merge |
| `git cherry base branch` | **Misleading** | A squashed commit matches no individual commit, so multi-commit branches read as unmerged while single-commit ones read as clean |
| An upstream marked `[gone]` | **Misleading** | Says the remote branch is absent, not that the work landed — and `git fetch --prune` can mark every branch gone at once |
| Diffing branch content against the base | **Misleading** | The base moves on, so differences prove nothing about what was merged |

Squash-merging is what breaks the cheap tests: it puts the work in the base branch under a commit that resembles none of the originals. That is why a merged pull request has to carry the proof the commit graph lost.

## Prune

**Classify** — run the script from the repository root:

```bash
uv run scripts/classify.py [--base BRANCH]
```

It needs the GitHub CLI (`gh`), authenticated, for the pull request evidence. Without it every squash-merged branch falls to `unresolved`; say so rather than filling the gap with a guess.

**Record** — show the user the classification, including the `sha` column, before deleting anything. That column is the only way back: `git branch <name> <sha>` restores a deleted branch exactly.

**Delete** — take the `ancestor` and `pr-merged` rows and nothing else:

```bash
git branch -D <branch> [<branch> ...]
```

Use `-D`, not `-d`: `-d` refuses squash-merged branches. That force flag is safe here only because the evidence is already settled — never use it first.

**Report** — name every branch left behind and why: open pull request, closed without merging, or no evidence found.

Done when you have either deleted every local branch other than the base or named it in the report with its reason. Silently skipping a branch fails the task.

## Gotchas

- A closed unmerged pull request means the work never landed. Someone may still want the branch, so it is never a delete candidate.
- Deleting the checked-out branch fails. Switch to the base branch first; the script marks which branch is current.
- `git fetch --prune` before classifying costs nothing, because no verdict depends on upstream tracking. Do not reinstate it as a signal.
- When a permission rule blocks branch deletion, stop and hand over the exact command with the recovery record rather than retrying variations.
