# {Project name}

## Purpose

{What this repository is for, who uses it, and what it deliberately does not do. Intent, not description — an agent can read the code, it cannot read why the code exists.}

## Conventions

{Only rules an agent would otherwise break: naming, error handling, commit format, generated files that must not be hand-edited, directories that are off limits, a pattern the codebase follows for reasons that are not evident from following it. Cut anything a competent agent already does by default, and anything it would infer from reading two files.}

## Constraints

{Limits invisible in the code: compliance boundaries, performance contracts, deployment targets, dependencies that cannot be added or upgraded, decisions imposed from outside the team. Omit the section if there are none.}

## Gotchas

{Concrete corrections to mistakes agents actually make here — the failing test that needs a running service, the endpoint that lies about health, the script that must run from the repo root, the command that looks right but is not the one this repo uses. Omit the section if there are none.}

## Documentation

Agent-facing documentation lives in `docs/`. Read [docs/AGENTS.md](docs/AGENTS.md) before reading or writing anything there.
