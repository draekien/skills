# Structural invariants

Drift that is provable from the doc set alone, without opening any code. Each has one correct answer, so each is mechanical — but only where the invariant comes from the contract. Where the repository's convention docs define a different frontmatter form or a different status vocabulary, that form is the invariant.

## What to check

- **Status against reality within the doc set.** A plan or exploration marked `active` whose replacement exists, or whose stated done-condition is visibly met by another document. A record marked `superseded` with an empty `superseded-by`, or naming a file that does not exist. A record marked `accepted` that a later record supersedes without the pair being linked.
- **Link integrity.** Every relative link in every document resolves. A link into `docs/` that points at a moved or renamed file is drift, not a typo — it means the doc set was reorganised and one document was left behind.
- **Frontmatter conformance.** Required fields present, one field per line where the contract asks for that, identifiers zero-padded and unique, status values drawn from the vocabulary the contract defines and no other. An identifier collision is the sharpest form: two records claiming the same number make every reference to that number ambiguous.
- **Import discipline**, where the repository uses pointer files at all. A pointer that holds anything beyond its import line: the extra content will diverge from the file it shadows, and an agent reading both cannot tell which is current. A file that holds guidance and no import is not a failed pointer — it is the document itself, and raising this finding against it would propose deleting the only guidance the repository has.
- **Restated discoverables.** Apply the **discoverable test** line by line: *would an agent learn this in under a minute by reading the package manifest, listing the tree, or opening two source files?* If so, the line earns nothing and rots the moment the repository moves — stack, dependency versions, task-runner commands, directory trees, and file inventories all fail it. A command that genuinely cannot be found — an undocumented flag, a step with no script behind it — passes the test and stays.

## Evidence standard

The finding must cite the two places in the doc set that disagree, or the single line that fails the discoverable test. An invariant finding that needs code to prove it is not an invariant finding — it belongs to claim verification.

## The one that is not mechanical

A restated discoverable that is also *wrong* is two findings in one: the line should not be there at all, and while it is there it misleads. Report it as a structural invariant and delete the line — do not correct the value first. Correcting it preserves the thing that will rot again.
