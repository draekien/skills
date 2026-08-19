# Backend Rules

Read by whichever delegate is doing the work. Follow the Capture or List rules, then the section for the configured backend.

## Capture

1. **Check reachability** — before drafting, confirm the configured backend can be written to; its section below says how. Stop straight away if it cannot, per step 5. Drafting first wastes the enrichment on a write that was never going to land.
2. **Draft** — a title in the imperative, short enough to scan in a list, plus a short body: what the idea is, why it surfaced, and the files or decisions already in play. Prose or bullets, no fixed headings; the length follows what the conversation actually gives. Never ask a question — there is no user on this side of the hand-off.
3. **Flag instead of guessing** — where the conversation offers nothing to enrich from, write the title alone and flag it `needs-expansion`. An invented body is worse than an honest gap: it reads as recorded intent the author never had.
4. **Write** — per the backend section below.
5. **Stop on failure** — a backend that rejects the write or is not reachable ends the run. Write nothing elsewhere, change no config, and report what failed and what would fix it.
6. **Return one line** — the file path or issue URL, and whether the todo was flagged.

Expanding an existing todo follows the same rules, except it rewrites that todo's body in place and clears the flag.

## List

Return every open todo: title, its identifier (path or issue number), and the literal prefix `[needs-expansion]` before the title of each flagged one — the caller detects flagged todos from that exact string. Sort newest first on the todo's own creation date, not on file modification time. Return the list itself rather than a count or a summary of it — the whole point is that the user reads their todos.

## markdown

Uses `markdownPath` and `markdownLayout`. Reachability: nothing to check — the script creates the path if it is missing.

`scripts/todos.py` owns this file format, in both layouts. Never read or write the markdown by hand: the frontmatter, slugs, checklist boxes, and body indentation all have to agree for List to find what Capture wrote, and the script is the only thing that guarantees they do. Pass `--path` and `--layout` straight from config on every call.

**Capture** — write the body on stdin so its line breaks survive, and add `--needs-expansion` when the todo is flagged:

```bash
uv run scripts/todos.py --path <markdownPath> --layout <markdownLayout> add --title "<title>" --body-file -
```

The script prints the todo's JSON record, including the `location` to report back. Adding the same title and body twice is a no-op, so a retry after an unclear result cannot duplicate the todo.

**List** — returns `{"todos": [...], "total": n, "returned": n, "skipped": [...]}`, newest first, open only, capped at 50:

```bash
uv run scripts/todos.py --path <markdownPath> --layout <markdownLayout> list
```

Each record carries `id`, `title`, `created`, `needsExpansion`, and `location`. Raise `--limit` when `total` exceeds `returned`. A non-empty `skipped` means files that could not be parsed — report them, since they are todos the user cannot see.

**Expand** — address the todo by the `id` from List:

```bash
uv run scripts/todos.py --path <markdownPath> --layout <markdownLayout> update <id> --body-file - --clear-flag
```

## github

Uses `githubLabels`. Reachability: the GitHub CLI is installed and authenticated.

Create the issue with the GitHub CLI, passing the body on stdin rather than as an argument so line breaks survive. Apply every label in `githubLabels`, plus `needs-expansion` when flagged.

**Missing label** — the CLI rejects the whole create when a label does not exist yet. Create the missing label, then retry the create once. Do not drop the label to force the write through: an unlabelled issue is invisible to List.

**List** — list open issues filtered to `githubLabels`, reading each issue's labels so flagged ones can be identified.

## linear

Uses `linearTeamId` and, when set, `linearProjectId`. Both come from config — never guess a team.

Create the issue through the connected Linear integration, with the drafted title as the issue title and the body as its description. Add a `needs-expansion` label when flagged. Reachability: a Linear connection is available in this session — there is no offline equivalent, so stop and say so when it is absent.

**List** — fetch issues for the configured team, narrowed to the project when one is set, in unstarted and started states only.
