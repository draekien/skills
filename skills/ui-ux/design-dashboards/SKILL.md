---
name: design-dashboards
description: Applies dashboard design principles to design, build, or review dashboards — classifying the dashboard type, selecting the right chart for each question, structuring KPIs and layout, and catching common anti-patterns. Use when designing or building a dashboard, choosing visualizations for data, or auditing an existing dashboard — or when the user says "design a dashboard", "build a dashboard", "create a dashboard", "review my dashboard", "which chart should I use", "improve this dashboard".
---

A dashboard is a single-screen answer to a specific question for a specific audience. Dashboards fail when they are built for available data instead of a named decision — the result is a wall of metrics nobody uses. Before any visual decision, establish: who reads this, what decision they make from it, and how fast they need the answer. Every rule below derives from three commitments:

- **Serve a decision, not a dataset.** Every tile must map to a question its readers actually ask; anything that maps to nothing gets cut.
- **Answer at a glance.** A reader should grasp "on track or not, and where to look next" within about five seconds, without searching, filtering, or scrolling.
- **Every pixel earns its place.** If an element — color, gridline, icon, decimal place, third dimension — does not help the reader understand faster, remove it (Tufte's data-ink principle). Density is not the enemy; junk is. A dense, junk-free dashboard beats a sparse, decorated one.

These rules apply identically when designing from scratch and when auditing an existing dashboard — auditing is holding what exists against the same commitments and reporting each violation with its fix.

## Classify the dashboard first

The dashboard's type determines refresh rate, density, and interactivity before any tile is drawn. Pick the row that matches the audience and question; resist blending types on one screen — a dashboard serving executives and analysts simultaneously serves neither.

| Type | Question | Audience | Refresh | Density | Interactivity |
| --- | --- | --- | --- | --- | --- |
| **Operational** | What is happening right now? | Frontline staff, supervisors | Real-time | Low–medium | Low — glanceable, no drill-down |
| **Tactical** | Are we on track this week? | Managers, team leads | Daily | Medium | Medium — highlight deviations |
| **Analytical** | Why did performance change? | Analysts | On demand | High | High — filters, drill-down, cross-filtering |
| **Strategic** | Are we progressing toward long-term goals? | Executives | Weekly/monthly | Low — few aggregated KPIs | Low — glance-and-go |

Interactivity follows type, not taste: cross-filtering and deep drill-downs belong on analytical dashboards where exploration is the job; on operational and strategic dashboards they work against the speed goal.

## Choose each display

For every tile, decide in this order:

1. **Is the whole point one number the reader must absorb in seconds?** → KPI card (see below). A big number beats any chart when the question is "am I on track", not "what is the shape of history".
2. **Does the reader need exact values or record lookup?** → Table. Left-align text, right-align numbers on the decimal, same precision per column, tabular figures. Embed sparklines in cells to add trend without losing precision.
3. **Does the reader need a pattern, trend, or comparison?** → Chart. Quick picks by question:
   - Change over time → line chart (≤3 series; small multiples beyond that)
   - Compare category sizes → zero-based bar chart, sorted when rank matters; horizontal when labels are long
   - Variance from target/zero → diverging bar
   - Relationship between two variables → scatterplot
   - Distribution → histogram (one group) or boxplot (several)
   - Part-to-whole → stacked bar; pie only for a single snapshot with ≤5 slices
   - Composition with negative components → waterfall

   The full decision tree — including time-series variants, spatial, flow, and when each chart breaks down — is in [references/chart-selection.md](references/chart-selection.md).

Prefer encodings the eye judges accurately: length and 2D position beat area, angle, and color intensity (Cleveland & McGill). This is why bars and lines outperform pies, gauges, and treemaps for quantitative comparison — and why gauges, 3D effects, and dual axes are banned outright (see anti-patterns).

## KPI cards

A bare number is not a KPI — without context the reader cannot tell good from bad. A complete card has four parts:

1. **Headline value** — large, dominant, rounded to decision-relevant precision ("$1.2M", not "$1,204,532.17"; exact value in the tooltip).
2. **Delta** — versus target or prior period, with direction indicator.
3. **Sparkline** — so the reader can tell a spike from a stable trend. A target says where the metric stands; a trend says where it is heading; a decision needs both.
4. **Semantic color** — green on-track / amber warning / red breach, applied by threshold and never decoratively elsewhere on the screen.

When a metric has no target or prior period yet, omit the delta and label the card as a baseline with no comparison — never invent one.

Cap primary KPIs at 4–6 per view (working memory tops out around 7 competing elements). Set alert thresholds from statistical baselines — control limits, seasonally adjusted bands — not raw distance from target, or the dashboard trains its readers to react to noise.

## Layout

- Most important KPI top-left; eyes scan data-dense screens in an F-pattern, so importance decays rightward and downward. (Simple, action-oriented operational screens may instead use a Z-pattern — status top-left, primary action bottom-right.)
- Structure vertically: status KPIs above the fold ("are we OK?"), trends and comparisons in the middle ("what's changing?"), detail and filters at the bottom ("why?").
- One screen, no scrolling for the primary view. If content demands scrolling, the metric list needs cutting, not the canvas extending.
- Group with whitespace and section headers (Gestalt proximity), not color. Keep tile styling strictly consistent — same type scale, title placement, and filter position everywhere; inconsistency breaks scannability more than any single bad chart.
- Grey/neutral baseline palette with one or two accents reserved for the data that matters; red/amber/green reserved for status semantics only. Never encode meaning with color alone — pair it with an icon, label, or position (roughly 1 in 20 readers has a color-vision deficiency; avoid red/green pairings, prefer blue/orange).
- One global time range and filter set by default; any tile that overrides it must say so visibly. Tiles silently disagreeing on time grain is the fastest way to destroy trust.
- Show data freshness ("as of 10:42") on live dashboards, and skeleton placeholders — not spinners — while tiles load.

Full layout, color, typography, interactivity, accessibility, and loading-state rules: [references/visual-design.md](references/visual-design.md).

## Anti-patterns

Name these on sight — when auditing, report each finding as the specific anti-pattern with its fix:

- **Data dump** — 20+ tiles because the data existed. Fix: cut to the metrics that serve the named decision; move the rest to drill-down.
- **Vanity wall** — big impressive numbers with no target, delta, or action. Fix: complete KPI cards or demotion.
- **Deceptive geometry** — truncated bar axes, dual y-axes, 3D effects. These misstate magnitude by construction. Fix: zero-based bars, small multiples instead of dual axes, flat 2D always.
- **Gauge/dial tiles** — one snapshot, no trend, huge footprint, and they provoke reactions to routine variation. Fix: KPI card with sparkline and statistically grounded thresholds.
- **Rainbow palette** — color without consistent meaning. Fix: single-hue ramps for magnitude, semantic colors for status, grey for everything else.
- **Aggregation hiding the story** — portfolio-level averages that mask or reverse subgroup trends (Simpson's paradox). Fix: show the breakdown alongside the aggregate.
- **No owner, stale data** — an unmaintained dashboard is worse than none; one detected staleness incident and readers never come back. Fix: named owner, freshness badge, pipeline alerting.

The full catalog — eighteen anti-patterns with recognition cues and corrections: [references/anti-patterns.md](references/anti-patterns.md).
