---
name: obsolete-skill
description: Retires a skill from this repo — archives it outright, or leaves a stub at the old path when the skill moved to a new one.
argument-hint: "[--mode archive|stub] [skill-name]"
disable-model-invocation: true
---

# Obsolete a skill

Retiring a skill is a registration problem, not a file-deletion problem. Moving the directory is the easy part; what breaks is every index that still names the old path. Work outward from the directory to the indexes, and finish by proving no index still points at nothing.

## Pick the terminal state first

One question decides it: **does this skill's work live on somewhere in this repo?**

- **Archive** — no. The skill is retired, or another skill absorbed its job. The directory moves to `skills/archived/` and every registration is removed. Nobody is sent onward, because there is nowhere to send them.
- **Stub** — yes, at a new path: a bucket move or a rename. A copy goes to the new path, and the old path keeps a **stub** that redirects to it and stays registered. Without the stub, anyone who installed the old bucket's plugin silently loses the skill and never learns where it went.

Infer the terminal state from the request; ask only when the request fits both readings.

## Archive

1. `git mv` the whole directory to `skills/archived/<name>/`, body and bundled resources intact. Archived skills are reference material — strip nothing.
2. Apply the **Archived** column of the registration table below.
3. Leave its frontmatter untouched. An archived skill is never registered, so its description never loads and never competes for activation.
4. If the bucket is now empty, also drop its `marketplace.json` entry, its root README section, and its bucket line in `CLAUDE.md`.

## Stub

1. Copy the directory to the new path with its resources.
2. Prove the copy is intact before editing anything: `bash .claude/skills/obsolete-skill/scripts/verify-copy.sh <old-dir> <new-dir>`. Exit 0 means byte-for-byte. Resolve every reported file — the script names the reason — and re-run until it exits 0.
3. Delete the bundled resource directories from the old path. Resources move with the skill; a stub carries none, because a stub does no work.
4. Rewrite the old `SKILL.md` as the stub: a `description` opening with `DEPRECATED` that names the new path and the plugin to install, and a body that tells the user the skill moved, gives the install command, and stops. Keep any invocation-control field the original set, so activation behaviour does not change.
5. Settle the stub's trigger phrases with the owner — the one genuine trade-off here. **Keeping** them means a user still on the old plugin gets a hit and reads the stub, at the cost of two skills matching the same request once both plugins are installed. **Stripping** them removes that competition, but the stub then only fires when the user invokes it by name, so a user on the old plugin alone gets nothing.
6. Apply the **Stub** and **New path** columns of the registration table below.

## Where each one is registered

This table is the single source of truth for what each terminal state owes each index. Both `outputStyles` and `hooks` appear twice in `marketplace.json` — once on the bucket entry, once on `everything` — so each needs editing in both places.

| Index | Archived | Stub at old path | Copy at new path |
| --- | --- | --- | --- |
| `marketplace.json` bucket entry | removed | stays | added |
| `marketplace.json` `everything` | removed | stays | added |
| `marketplace.json` `outputStyles`, if an output style | removed | stays | added |
| `marketplace.json` `hooks`, if it ships a hook | removed | stays | added |
| Bucket README line | removed | rewritten as `**Deprecated** — moved to [<bucket>/<skill>](...)` | added |
| `skills/archived/README.md` | added, plus `Superseded by [<skill>](...)` where another skill took the job | — | — |
| Root README bucket count | old bucket decremented | not counted | new bucket incremented |

## Sweep the old path out of the repo

Sibling skills, specs, and reference files link to each other by relative path, and those links break silently:

```bash
grep -rn "<skill-name>" --include=*.md --include=*.json --include=*.py . | grep -v "^./<new-dir>/"
```

Every hit either repoints at the new target or goes away. Widen the pattern to the old bucket path when the skill moved buckets.

## Gotchas

- **A stub must stay registered; an archived skill must not.** `tests/check-manifest.py` requires every `SKILL.md` outside `personal/` and `archived/` to appear in both its bucket README and `everything.skills` — deregistering a stub fails that. It separately fails on any manifest path with no `SKILL.md` behind it — archiving without removing the paths fails that. The two mistakes are mirror images, and each one passes the check the other fails.
- **Three indexes have no automated check at all.** `check-manifest.py` reads only `everything.skills` and the bucket READMEs, so a stale root README count, an orphaned `outputStyles` path, and an orphaned `hooks` object all survive a clean test run. Verify those three by eye against the table.
- **A copy made in the working tree carries CRLF, but git stores LF.** The fresh copy then differs on every single line, which reads like a corrupted copy rather than a whitespace artefact. The verification script reports this as `crlf` and gives the normalising command.
- **The root README counts live skills.** A stub still occupies a directory in its bucket, so the bucket's file count and its README count diverge by the number of stubs. Count what a user can actually use.
- **A one-liner lives in exactly one bucket README.** `CLAUDE.md` makes the bucket README the single source of truth for it. After a stub, the old bucket's line describes the deprecation and the new bucket's line describes the skill — never the same sentence in both.
- **Internal skills under `.claude/skills/` are outside all of this.** They are not in `marketplace.json` and not scanned by the manifest test, so retiring one is just deleting the directory.

## Finish

`CLAUDE.md` keys the manifest check to *adding* a skill; it applies just as much to removing or moving one, so run the repo's standard post-change checks here too.

Done means: every index in the table matches the terminal state chosen, no path anywhere in the repo names a directory that no longer holds a skill, and the manifest check and the linter both pass clean.
