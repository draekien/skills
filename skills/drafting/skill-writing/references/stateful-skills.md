# State Design Rules

Design rules for skills that persist per-project state. A stateful skill must satisfy every rule — each guards a distinct failure mode.

- **One namespaced home** — all persistent state lives in a single, vendor- or skill-namespaced location at the project root, so it cannot collide with other tooling and the user always knows where to look.
- **Absence never errors** — every config key has a documented default; a missing file or key means defaults apply, not failure. The skill must work on first contact with a project that has never seen it.
- **Confirm before first write** — creating the state home or persisting a setting requires user confirmation; files appearing in a repository unannounced erode trust. Once confirmed in a session, later writes do not re-ask.
- **Load once at session start** — read state on first invocation, before any work that depends on it; work done before loading runs on the wrong settings, and re-reading mid-session invites drift.
- **Script-mediated access** — when the state format is shared or fragile (a file holding multiple skills' sections, a structured dictionary), wrap reads and writes in bundled scripts that touch only this skill's portion; free-hand edits corrupt neighbours.
- **Document every key** — every key or file the skill reads or writes is documented with its type and default; undocumented state is unmaintainable.
- **Version-controlled by default** — project state is shared team configuration, not a cache; it belongs in the repository unless the user opts out.
