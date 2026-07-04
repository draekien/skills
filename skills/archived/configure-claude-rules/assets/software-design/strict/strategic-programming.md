# Strategic Programming

Every change is an opportunity to improve the design. When new code does not fit the existing structure cleanly, treat that friction as a signal to redesign the interface — not as a reason to patch around it.

```
// prefer — interface designed around the concept
function parseDate(input): Date

// avoid — interface shaped around one caller's immediate needs, not the concept
function parseDateForCheckoutFlow(rawInput, userTimezone, localeOverride, legacyFormat):
  ...
```

Budget roughly 10–20% of implementation time on design quality: naming, module boundaries, eliminating special cases. Tactical shortcuts compound. A system built from a series of "just this once" hacks becomes one where every change carries unknown risk.
