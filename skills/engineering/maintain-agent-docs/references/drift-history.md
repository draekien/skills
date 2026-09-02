# History rot and unrecorded decisions

The deepest pass, and the only one that can find a document that was true when written, is still internally consistent, and has quietly stopped matching the repository. Version-control history is the signal the other classes cannot see.

## Rot signals

Work from each document's last substantive change forward, and ask what happened in the repository since.

- **Volume of change under a documented path.** Heavy churn in a subtree whose governing document has not moved in that time means the document is describing an earlier version of that code. Churn is not proof of rot — it is where to look.
- **Paths that no longer exist.** A document naming a directory, module, entry point, or command that has since been renamed or removed. Where the rename is mechanical the repair is mechanical; where the thing was removed outright, the guidance about it may have no subject left.
- **Work that matches an active plan.** Commits or merged branches whose content is the plan's stated steps. A plan whose work has shipped but whose status still reads active is the single most misleading document a repository can hold, because an agent will start work that is already done.
- **Reversals.** A change that undid what a document still recommends. The commit that reversed it is the evidence; whether the reversal was deliberate is the question for the user.
- **The document that never changed.** A conventions document untouched across a period when the repository's structure changed substantially is suspicious in proportion to how confident it sounds.

Where history is absent, shallow, or squashed flat, this class is uncheckable. Report it as such and name why. Raise no rot findings from the working tree alone — without the record of when something changed, a rot finding is a guess wearing evidence.

## Unrecorded decisions

History also holds decisions that were made and never written down: a dependency swapped out, a boundary redrawn, an approach abandoned after being tried. Surface only those clearing the contract's own bar for a decision record — read that bar from the repository's convention docs rather than assuming what it says, since a repository that raised or widened its bar has done so deliberately. Most changes clear it on no count at all.

Offer these as candidates and let the user choose. Never write the rationale: history shows what changed, not why the alternative was rejected, and a decision record with invented reasoning is worse than none. Where the user cannot say why, there is no record to write. Zero is a correct outcome.

## Evidence standard

Cite the change — the commit, branch, or range — and what it did to the document's subject. A rot finding without a specific change behind it is speculation, and belongs only at `max`, marked as probable.

## Why this class goes to interview

History establishes that something moved, not that the document should follow. A document may deliberately outlast a change, and a plan may be dormant rather than done.
