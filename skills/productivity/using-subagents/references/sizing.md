# Sizing a leaf

Agent success falls as task size grows: near-certain on tasks a person finishes in minutes, rare on tasks that take hours ([METR](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)). Agents also misjudge how much effort a task needs unless the brief states a bound ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)). The bands below give the orchestrator that bound before dispatch.

The bands are calibrated from use, not from a published measurement — no source gives a size limit for the current models. Each band keys on the **Intelligence** score in the `picking-models` model matrix, so a model the matrix scores falls into a band without editing this file.

## Leaves that change files

Build and Write leaves are sized by **reach**: the files the leaf edits, plus the code that must change or be re-checked because of those edits.

| Intelligence | Reach limit | Fits | Over the band |
| --- | --- | --- | --- |
| ≤ 4 | One file, no exported signature changes | Rename a private helper inside `src/utils/date.ts` | Change the signature of an exported `formatDate` — every caller is now in reach |
| 5–8 | One module; exports change only when every caller is inside that module | Migrate every handler in `src/api/orders/` to a new error type | The same error-type change reaching `orders/` and `billing/` |
| ≥ 9 | Crosses modules, only through interfaces the orchestrator fixed in the brief | Wire a new session store into `auth/` and `api/` against a signature given in the brief | Design the session store interface and change its callers in the same leaf |

A module is the smallest directory or package the project itself treats as a unit — a workspace package, a crate, or a top-level directory under the source root. Count reach by reading imports before dispatch, not by estimating. A mechanical fan-out over 40 files is 40 one-file leaves, not one leaf with a reach of 40.

## Leaves that only read

Search and Review leaves are sized by **search space**: the locations the agent must read to answer. A review's search space is the reach of the diff under review.

| Intelligence | Search space limit | Fits | Over the band |
| --- | --- | --- | --- |
| ≤ 4 | A named list of files, or one directory, with an answer checkable against the source | Every file under `src/` importing `lodash` | Where retries are configured, with no location given |
| 5–8 | One module, or a diff whose reach is one module | Where `src/auth/` validates tokens; review the `orders/` migration diff | Review a diff spanning `auth/` and `api/` |
| ≥ 9 | The whole repository, or a diff crossing modules | Why the CI cache misses; review a cross-module session store change | A question spanning several repositories or external sources |

Give each read-only leaf one question. Two questions that both fit the band are still two leaves. Write the band's limit into the brief as the research coverage bound.

## Splitting

Split along the unit the band counts: a leaf over the one-module band splits into one leaf per module; a leaf over the one-file band splits into one leaf per file. A leaf over the cross-module band reaches an interface nobody has fixed: fix the interface yourself, then split into one leaf per module, each briefed with the exact signature. Each leaf gets its own brief and is checked against the band again.

When the only cuts are sequential, dispatch a **gated chain**: one leaf at a time, each leaving a state on disk that a command checks before the next leaf is dispatched.

```text
Leaf: replace cookie sessions with a store-backed session — reach: three modules
  1. add the new store behind the existing SessionStore interface   gate: store tests pass
  2. switch auth/ to the new store                                   gate: auth tests pass
  3. delete the cookie store and its tests                           gate: full suite passes
```

Dispatch each leaf in the chain as a fresh agent whose brief carries the checked state, never by resuming the previous leaf's agent. If no command can check a cut's output, the cut is a phase split and the leaf cannot be cut further.

A gated chain passes a checked state between leaves, not reasoning. Splitting design from implementation is still a phase split: the implementer needs the designer's reasoning, and no command checks it.

A leaf that cannot be cut further and is still over its band runs on the cheapest model whose band it fits. A leaf over every band stays with the orchestrator.
