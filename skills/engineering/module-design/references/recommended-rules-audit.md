# Recommended Rules Audit

After writing the spec, spawn an independent subagent to audit it. Brief it to:

- Read the spec at the resolved path.
- Check each recommended rule listed in design-principles.md under the Recommended Rules heading, where full rule definitions live.
- For each violation: quote the offending spec text, name the rule, and suggest a concrete fix.
- Report clean if no violations found. Do not rewrite the spec — findings only.
