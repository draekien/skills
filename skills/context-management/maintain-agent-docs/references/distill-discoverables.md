# Restated discoverables

A line the agent would learn faster by looking. It is true — that is what separates this class from drift — and it still costs context on every turn, and it rots the moment the repository moves.

## The discoverable test

Apply it line by line: **would an agent learn this in under a minute by reading the package manifest, listing the tree, or opening two source files?** If so, the line earns nothing.

Fails the test: stack and framework names, dependency versions, task-runner commands, directory trees, file inventories, exported symbol lists, and anything restating a config file the repository already holds.

Passes the test: an undocumented flag, a step with no script behind it, a command that looks right but is not the one this repository uses, the reason a discoverable thing is the way it is. A gotcha is never a restated discoverable, however mechanical it sounds.

## Duplication within the doc set

The same rule stated in two documents is the same waste in a different shape, and worse: the copies drift, and an agent reading the one that was not updated acts on a rule the other has already retired. The root document holds the rule; a nested document restating it loses the copy, never the original.

Where the two copies already disagree, this is not the class. A nested document reversing a root rule is a cross-document contradiction, and it goes to interview whatever the effort level.

## The one that carries a rule

A line can restate a discoverable and add a requirement on top of it — "run `pnpm test`; it needs the compose stack up" restates one thing and teaches another. Cut to what the artifact does not say. Deleting the whole line to remove the restatement takes the rule with it, and the rule is why someone wrote the line.

A restated discoverable that is also *wrong* is deleted, not corrected. Correcting the value preserves the thing that will rot again.

## Evidence standard

Name the artifact the line restates and quote the part of it that says the same thing: the manifest key, the config field, the directory listing, the other document and its line. A finding asserting that a line is discoverable without naming where it is discoverable from is the audit's own taste, and this class does not resolve that way.
