# engineering

Use for: building or changing a feature that spans several modules whose files can be owned by one member each. Not for: a change one agent finishes in one sitting, or work where two members would edit the same file.

## Roster

| Role | Count | Owns | Work | Access |
| --- | --- | --- | --- | --- |
| leader | 1 | the task graph, every shared interface, the final verification | Orchestrate | write |
| implementer | 2–3 | a disjoint set of source paths each | Build | write |
| tester | 1 | test files only | Build | write |
| reviewer | 1 | the review findings | Review | read-only |

Before spawning anyone, the leader fixes every interface two slices share — exact signatures, payload shapes, error cases — and writes the ownership map: which paths each implementer owns.

### implementer

Builds one slice inside its owned paths, against the fixed interfaces. Does not edit any path it does not own; a needed change elsewhere goes to the owner as a message. Does not change a shared interface — it requests the change from the leader.

### tester

Writes tests against the fixed interfaces while the implementers build, so the tests check the contract rather than echo the implementation. Runs the suite once the slices land and sends each failure to the implementer who owns the failing code.

### reviewer

Reviews each slice as it lands, against the interfaces and the project's conventions. Marks each finding blocking (correctness, contract break, security) or non-blocking. Never reviews code it wrote; it writes none.

## Task graph

1. Fix interfaces and the ownership map — leader — blocked by: none
2. Implement slice N, one task per implementer — implementer — blocked by: 1
3. Write tests against the interfaces — tester — blocked by: 1
4. Review slice N — reviewer — blocked by: 2 for that slice
5. Fix blocking findings for slice N, and re-request review until none is open — implementer — blocked by: 4 for that slice
6. Run the full suite, create a fix task for the owning implementer per failure, and re-run until it passes — tester — blocked by: 2, 3
7. Verify the combined tree — leader — blocked by: 5, 6

## Messaging

- implementer → implementer: a question about how the other's slice behaves at the shared interface, or a change needed inside the other's paths.
- tester → implementer: a failing test, with the command and its output, sent to the owner of the failing code.
- reviewer → implementer: a finding, with `file:line`, severity, and the failure it causes.
- implementer → reviewer: "fixed, re-check" naming the finding or the failing test, so code changed by a test fix is reviewed too.
- every member → leader: an interface change request, a blocker, the done signal.

## Review

The reviewer reads every slice; the tester's suite plus the project's build and lint commands check the combined tree. The leader re-runs those commands on the combined tree, because each member verified only its own slice.

## Stop

Done when every task is completed, the reviewer reports zero open blocking findings, and the project's test, build and lint commands exit 0 on the combined tree when the leader runs them. Stop without success when an implementer is blocked on a decision only the user can make; report the decision and what is finished.
