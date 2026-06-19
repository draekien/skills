# Skill eval results

This folder holds the repeatable eval state for one skill: its frozen test
suites, every run's results, and a report that reads them back.

```
report.html              the readout — open it in a browser (see below)
activation/
  suite/v1.json …        frozen corpus + labels, one file per version
  runs.jsonl             one run record per line
impact/
  suite/v1.json …        frozen tasks + criteria, one file per version
  runs.jsonl             one run record per line
```

## Viewing the report

`report.html` loads the run and suite files with `fetch`, which browsers block
under `file://`. Serve the folder over a local HTTP server instead:

```sh
python -m http.server 8787 --directory .
```

Then open <http://localhost:8787/report.html> and stop the server with Ctrl-C
when you're done. Re-run the skill-evals skill and it can start and stop this
server for you.

## What makes the trend trustworthy

A trend only means something if every run measured the same thing. Each suite
is **frozen** once approved and **versioned** the moment its content changes, so
the report draws each version as its own band — scores from different suites are
never silently joined into one line. If you change a suite (add a hard negative,
fix a mislabel, add a task), the next run mints the next version and the report
segments accordingly.

Commit this folder to version control so the history travels with the skill.
