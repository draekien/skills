# Scoping and progressive disclosure

The root document is read on every turn. Everything in it is a standing context cost paid by every agent on every task, including the tasks it has nothing to do with. Guidance whose reach is narrower than the repository belongs where its reach ends.

## Blast radius

Establish each block's blast radius before proposing anything: the set of paths where following the guidance changes what an agent writes. Determine it from the code, not from the wording — a rule phrased generally may only ever apply in one package.

- **Repository-wide** — stays in the root document, however long that document becomes. Length is not a defect: a long document of rules that all apply is correct, and splitting it because it is long is the failure mode this class most often produces.
- **One directory subtree** — belongs in a nested document at that subtree's root, where it loads only for agents working there.
- **Nowhere identifiable** — the block may be aspirational rather than operative. That is a claim-verification finding, not a scoping one.

## Coherence

A move is only proposed when the block is coherent on its own: it reads correctly in the destination without the surrounding context, and it does not depend on a definition that stays behind. Scattered lines that each need a different home are reported rather than moved — assembling a nested document out of fragments produces something no one wrote and no one will maintain.

Where a block splits, the durable rule and its directory-specific application can separate: the general rule stays at the root, the specific application moves down. Do not duplicate the rule in both.

## Destination

The nested document sits at the root of the subtree it governs, named the way the contract names agent docs, with a sibling import-only file where the contract uses that pattern.

Do not create a new nested document for a single line. The cost of a file an agent must discover exceeds the saving, until the block is substantial enough that leaving it at the root visibly crowds out what belongs there.

## Evidence standard

Every proposal names the exact lines, the destination path, the blast radius that justifies that destination, and what remains at the root. Where the blast radius rests on a judgement rather than on paths verified in the code, say so — an unverified scope is the most likely way this class goes wrong, because a rule moved too far down goes quiet rather than visibly wrong.

## Reading order within a document

Shape problems also appear inside a single document, where no move is needed: the constraint that governs everything stated last, the gotcha that prevents the common failure buried under prose an agent already knows. Where the fix is ordering rather than relocation, propose the reordering as its own finding and keep it separate from moves.
