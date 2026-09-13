# Load-on-demand extraction

The root document is read on every turn, so a block needed by one task in twenty is paid for by the other nineteen. Extraction moves that block into a document of its own and leaves behind the one line that tells an agent when to go and read it.

This is not the scoping move. Scoping asks where guidance applies — a set of paths — and puts it at the root of that subtree, where it loads for every agent working there. This class asks which tasks need it, and leaves it unloaded until one of them starts.

## Name the tasks

Every extraction names the tasks that need the block, and the naming is the test.

```text
✓ Releasing — cutting a release, hotfixing a shipped version. No other task reads it.
✗ This section is long and rarely relevant.
```

A block whose tasks cannot be enumerated is guidance the repository needs on every turn, and it stays where it is. Splitting by size is already an anti-pattern of this skill, and this class is where it returns wearing a new name: length is evidence of nothing, and the enumeration is the whole finding.

## Where the block has a path home

A block often answers both questions, because the tasks that need it are exactly the tasks performed inside one directory. That block belongs to scoping, which resolves it to a nested document loading automatically for agents working there — strictly better than a pointer an agent must choose to follow.

Hand it over rather than taking it. Where scoping has not been activated, report it as an unresolved scoping finding named as out of level and extract nothing. Scoping sits one level above this class, so a default pass meets this case routinely; taking the block anyway is how a run produces a change the user never asked it to consider.

## Destination

The contract names the directory. Read the repository's own convention docs for a load-on-demand convention before proposing any extraction — the path, the filename form, and what a document there is expected to contain.

Where the contract defines none, that absence is the first finding, and it resolves by approval exactly as the missing writing convention does: propose the exact text, and extract only once the user has accepted it. Never install a convention by writing the first document under a path the audit chose.

## The pointer

The pointer is the part that stays loaded, so it is the part that has to work.

```text
✗ See docs/contexts/ for release guidance.
✗ Additional context is available under docs/contexts/.
✓ Read docs/contexts/releasing.md before cutting a release or hotfixing a shipped version.
```

A pointer names the task that triggers the read, never the directory it points at. The enumeration the finding already produced is the wording — nothing further needs inventing.

A pointer naming no trigger produces a directory no agent opens, and the extraction has then made the repository worse than the bloat did: the guidance is gone from the root document and unread in its new home.

## Pointers already written

A weak pointer is a finding of this class whether or not anything is being extracted on this run, because no other class catches it — the link resolves, the line is literal, and it is too short to be padded.

It resolves mechanically, since the tasks are enumerated in the document being pointed at and one correct rewrite follows from them. Where the target names no tasks either, the rewrite has nothing to draw on and the finding becomes a proposal to state them, resolved by approval like any other.

## Evidence standard

Every extraction names the tasks, quotes the lines, gives the destination path and the convention that defines it, and states the pointer verbatim. The token figures come from the measurement the pass already took: what leaves the root document, and what the pointer costs to keep.

Report the difference rather than the size of the block. Forty lines replaced by a pointer of two saves thirty-eight on every turn that does not trigger it, and costs one extra read on every turn that does — and a user deciding whether to accept the move is deciding about that trade, not about a line count.
