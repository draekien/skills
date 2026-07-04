# break-down-prd

## `scripts/skillsrc.py` does not handle malformed JSON in `.draekien/.skillsrc`

**Gap:** `load()` in `skills/engineering/break-down-prd/scripts/skillsrc.py` (lines 30-33) calls `json.loads(...)` with no error handling. A corrupted `.skillsrc` file raises an unhandled `JSONDecodeError` traceback instead of an actionable stderr message and a distinct non-zero exit code, which `references/script-design.md` requires ("Actionable error messages", "Meaningful exit codes").

**Why it's a tradeoff, not a clear-cut fix:** The identical `load()` implementation — same missing try/except — exists verbatim in `skills/engineering/module-design/scripts/skillsrc.py` and (per `specs/skillsrc.md`) in `skills/engineering/get-specific/scripts/skillsrc.py`, both of which `specs/skillsrc.md` names as the *reference implementations* for this exact script pattern. Patching only `break-down-prd`'s copy would:

- make the three "identical by design" `skillsrc.py` scripts diverge, contradicting the spec's own template convention (`specs/skillsrc.md` "Script Convention" section presents them as interchangeable boilerplate copied per skill), and
- fix the symptom in one skill while leaving the same defect live in the two skills the spec calls the reference implementations for anyone copying the pattern next.

This is a cross-cutting defect in the shared script template, not something scoped to `break-down-prd` alone — fixing it correctly means updating the template/spec and all three copies together, which is outside this audit's scope (auditing only `skills/engineering/break-down-prd`).

**Recommendation:** Raise a follow-up task against `specs/skillsrc.md`'s "Script Convention" section to add a required try/except around `json.loads` with an actionable stderr message and a distinct exit code (e.g. exit 1 for "corrupt config"), then propagate that change to all three existing `skillsrc.py` copies (`break-down-prd`, `module-design`, `get-specific`) in one pass so they stay identical.

**Alternative:** Patch only `break-down-prd`'s copy now, accepting that it will briefly diverge from the two files the spec calls its reference implementations, until a follow-up brings the others in line.
