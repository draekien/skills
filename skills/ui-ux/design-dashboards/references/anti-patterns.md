# Anti-pattern catalog

Eighteen dashboard failures in four groups. Each entry: how to recognize it, why it fails, and the correction. When auditing, report findings as the named anti-pattern — recognition plus mechanism makes the fix unambiguous.

## Chart-level failures

**1. Pie chart overuse.** Pies ranking many categories (>5 slices), pies compared side by side, pies for non-part-to-whole data. The eye compares lengths well and angles poorly; ranking by slice is guesswork. → Sorted bar charts; pie only for a single part-to-whole snapshot with ≤5 slices.

**2. Dual-axis deception.** Two metrics on one chart with independent y-scales. Scale choice can manufacture visual correlation between unrelated series. → Small multiples, or an indexed (percent-change) chart; if a dual axis is truly unavoidable, label both axes on the chart face.

**3. Truncated axes.** Bar chart y-axis starting above zero. Bars encode value as length; truncation breaks the encoding and inflates small differences into dramatic ones. → Bars always start at zero. A zoomed line chart is acceptable for trend detail if the baseline is stated.

**4. 3D charts.** Depth, perspective, and shadow effects on pies and bars. Perspective distorts magnitude (front slices look bigger) and the third dimension encodes nothing. Major BI tools omit 3D charting deliberately. → Flat 2D, clean strokes, legible labels.

**5. Gauges and dials.** Speedometer widgets for KPIs. One snapshot, no trend, enormous footprint per number, and a needle near the red zone provokes reactions to routine variation. → KPI card with sparkline and delta; bullet graph where a compact target-vs-actual is needed.

**6. Rainbow palettes / color without meaning.** Many-hued heatmaps, multiple unrelated color schemes on one screen, red/green used decoratively. Color that carries no consistent meaning is noise the reader must actively ignore. → Single-hue ramps for magnitude, semantic status colors applied only by threshold, grey for everything else.

## Structural failures

**7. Data dump.** 20+ tiles, every available metric, tables so wide users export to spreadsheets. Working memory handles ~7 chunks; beyond that, attention dilutes into analysis paralysis. → Cap primary metrics per view; summarized top-N with drill-down for the rest.

**8. No named audience or question.** Built from available data rather than a decision someone makes. Without an audience, nothing can be prioritized, so nothing is. → Define the audience and their decision first; every metric must map to it or go.

**9. Vanity wall.** Huge hero numbers (total impressions, cumulative signups) with no target, delta, or action, while decision-relevant rates hide in a corner. A museum of big numbers supports no decision. → Frame each KPI as question + target + variance; demote or delete the rest.

**10. Scrolling wall of charts.** Key tiles below the fold, long scroll to reach anything. Below the fold is effectively invisible for a monitoring surface. → Top KPIs above the fold; secondary content behind drill-down, lazy-loaded.

**11. Inconsistent time ranges and grains.** Tiles silently overriding the global range, mixed hourly/daily grains, hidden sticky filters from a prior session. Numbers that appear to disagree destroy trust in the whole surface. → One global range/filter set; visible per-tile scope line for any override.

## Cognitive failures

**12. Numbers without context.** "Total sales: 246" with no target, trend, or comparison. Data without context is noise — the reader cannot tell good from bad. → Every metric paired with target, delta, and/or trend.

**13. Misleading aggregation (Simpson's paradox).** Portfolio-level sums and averages that mask — or reverse — subgroup trends. Averaging smooths out the noise and the truth together. → Show the subgroup breakdown alongside the aggregate; offer segmentation by the likely confounder.

**14. Reacting to noise.** Alerts and status colors triggered by any deviation from target, regardless of normal variation. Produces alert fatigue and knee-jerk interventions while real shifts drown. → Thresholds from statistical baselines (control limits, seasonally adjusted bands); alert only on deviations that are both significant and business-relevant.

**15. Wrong chart for the question / missing labels.** Pies for trends, sparklines for precise analysis, unlabeled axes, vague legends. Mismatch forces the reader to decode instead of read. → Match chart to question (see chart-selection reference); direct-label lines over legends where feasible.

## Process failures

**16. The dashboard graveyard.** Maintained but never opened. Root causes: wrong audience, needs an analyst to interpret, metric overload, missing context, fragmented metric definitions, neglect. → Design around one decision, validate with real users, watch usage analytics, retire what goes unused.

**17. Unclear ownership.** No named owner; teams each maintaining their own version of "the truth" with drifting metric definitions. Data-quality issues bounce between teams and trust erodes. → One named owner per dashboard; a shared metric dictionary as the single definition source.

**18. Stale data.** Outdated timestamps, broken pipelines, no freshness indicator. One detected staleness incident and users revert to spreadsheets permanently — even after the fix. → Automated connections, a visible freshness badge, and pipeline alerts to the owner when data exceeds its freshness SLA.
