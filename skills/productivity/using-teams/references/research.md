# research

Use for: questions that must be answered before the leader's request can continue, spread across several independent sources or areas. Not for: a cited report as the end product — that is the `deep-research` skill (`/plugin install productivity-skills@draekien-skills`, or `npx skills add draekien/skills --skill "deep-research"`). Not for: a single lookup, which one agent answers faster.

## Roster

| Role | Count | Owns | Work | Access |
| --- | --- | --- | --- | --- |
| leader | 1 | the questions, the coverage bounds, using the findings in the request | Orchestrate | write |
| searcher | 2–4 | one angle each | Search | read-only |
| checker | 1 | verifying every citation | Review | read-only |

### searcher

Answers the questions on its angle within its coverage bound: the locations, sources or directories it searches, and nothing beyond. Cites a location for every claim — `file:line`, or a URL with its section. Reports "not found in those locations" when the answer is not there; it does not widen the search or infer an answer.

### checker

Opens every cited location and confirms it supports the claim attached to it. Does not research; an unsupported claim goes back to its searcher.

## Task graph

1. Write the questions, the answer each one needs, and a coverage bound per angle — leader — blocked by: none
2. Search one angle — searcher — blocked by: 1
3. Check the citations of one searcher's findings — checker — blocked by: that searcher's task 2
4. Use the findings in the request — leader — blocked by: every task 3

## Messaging

- searcher → searcher: a source that answers a question on the other's angle, sent as its location; or notice that both are covering the same ground, so one drops it.
- searcher → checker: its findings with every citation, as soon as its task 2 completes.
- checker → searcher: a claim its cited location does not support. The searcher corrects the citation or withdraws the claim, and sends the correction or the withdrawal to the checker.
- searcher → leader: its findings in full in the message, sent after the checker reports none of them unsupported.
- every member → leader: the done signal.

## Review

The checker reviews every citation; the leader spot-checks the claims the request will depend on most.

## Stop

Done when every question is answered or marked "not found" within its bound, and the checker reports zero unsupported claims. Stop without success when the questions the request depends on are all "not found"; report the locations searched, so the user can widen the bounds or answer directly.
