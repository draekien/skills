# Visual design rules

Layout, color, typography, interactivity, accessibility, and loading-state rules for dashboards. Each rule states the constraint and the mechanism it guards.

## Layout and grid

- **F-pattern priority.** Eye-tracking on data-dense screens shows a top horizontal sweep, a shorter second sweep, and a left-edge vertical scan. Place the most important KPI top-left; attention decays rightward and downward. Simple action-oriented operational screens may use a Z-pattern instead (status top-left, primary action bottom-right).
- **Vertical narrative.** Status/KPIs above the fold, trends and comparisons mid-page, detail and filters at the bottom. Readers abandon screens with more than ~7 competing elements above the fold.
- **Grid discipline.** 3–4 equal-width columns on desktop, identical gutters throughout. Broken grids read as noise and slow scanning.
- **Tile consistency.** Same content type gets identical styling everywhere: title top-left, filters top-right, legend bottom-center, one shared type scale. Inconsistent tiles damage scannability more than any individually bad chart. Keep tiles short — no internal scrolling.
- **Tile sizing by density.** Small tiles for static content up to ~4 data items; medium for moderate data; large only for genuinely complex visualizations. Five workhorse tile archetypes: aggregate status, trend (sparkline), utilization, attribute-value details, event list.
- **Group by proximity, not color.** Whitespace gaps and light bounding regions are the primary relatedness signal; section headers make the grouping's meaning explicit; color only reinforces. A good grouping survives the blur test — recognizable at thumbnail scale.
- **Single screen for status.** Status KPIs render above the fold without scrolling; trends, comparisons, and detail may sit below and require scrolling to reach. Status itself demanding a scroll signals an uncut metric list, not a small canvas.

## Color

- **Grey baseline, scarce accents.** Neutral background and chrome; one or two vivid accents reserved for the most important series and active states. Four or fewer categories rarely need more than a muted qualitative palette.
- **Semantic colors are a protected vocabulary.** Green = good/on-track, amber = warning, red = breach/action-needed, grey = neutral. Apply only by threshold, never decoratively, and never reuse these hues for unrelated categories on the same screen.
- **Palette type follows data structure.** Sequential (single-hue light→dark ramp) for ordered magnitude; diverging (two hues meeting at a neutral midpoint) only when the midpoint is meaningful (target, zero, average); qualitative for unordered categories. Never a rainbow ramp for magnitude.
- **Color-vision deficiency.** Roughly 1 in 20 readers (about 8% of men) cannot reliably distinguish red from green. Prefer blue/orange for good/bad pairings; the Okabe-Ito palette is a tested categorical default. Verify with a deficiency simulator.
- **Never color alone.** Every color-coded status needs a redundant channel — icon, shape, label, or position.
- **Contrast minimums.** 4.5:1 for normal text, 3:1 for large text and non-text elements (chart lines, status icons) against their background.

## Typography and numbers

- **Alignment.** Left-align text columns; right-align numeric columns on the decimal point, headers matching their column. Numbers are compared digit-by-digit from the right; misalignment breaks column scanning.
- **Tabular figures.** Use a typeface with tabular (fixed-width) lining figures for KPI values and tables; monospace as fallback. Proportional digits make columns impossible to scan.
- **Uniform precision.** Every number in a column carries the same decimal places, rounded to the minimum precision that changes a decision — "$1.2M" on the card, the exact figure in the tooltip or export.
- **One type scale.** Primary KPI values distinctly larger and bolder than labels; a small, consistent scale reused across all cards. Per-card font improvisation is visual noise.

## Interactivity

Interactivity budget follows dashboard type (see skill body): analytical dashboards earn filters, drill-downs, and cross-filtering; operational and strategic dashboards should stay glanceable.

- **Progressive disclosure.** Default view shows summary only; definitions, exact values, and granular breakdowns live behind tooltips, expansion, or drill-down.
- **Tooltips are cheap — use liberally** for metric definitions, unrounded values, and contextual mini-detail.
- **Drill-down: preserve context.** Side panel/drawer when the parent view should stay visible; dedicated page when the detail is extensive. Chains deeper than 2–3 levels lose the reader.
- **Cross-filtering carries hidden-state risk.** Only on analytical dashboards, and always with a visible, removable active-filter chip list — invisible filter state is how numbers stop being trusted.
- **Filter placement.** Page-level filters at the top, prominently; tile-level filters in the tile's top-right. Default to the most useful selection, never an empty state.
- **One global time range.** All tiles inherit it; any override is visibly flagged on the tile (a scope line under the title). Tiles silently disagreeing on time range or grain make the dashboard look self-contradictory.

## Accessibility

- Keyboard operability throughout: tab between interactive elements, arrows within composite widgets; semantic markup with appropriate roles/states; live-region announcements for real-time updates.
- Provide a data-table alternative for any non-trivial chart, plus a one-line text takeaway near complex visualizations — alt text alone cannot convey a multi-series chart.
- Honor reduced-motion preferences for count-up and transition animations.

## Loading, freshness, and failure states

- **Skeletons over spinners** for tile content: greyed placeholder shapes matching the final layout. Spinners only for short discrete actions. If loading exceeds a few seconds, switch to an explicit progress/status message.
- **Load in priority order.** Above-the-fold KPIs render first; lower charts lazy-load.
- **Freshness is disclosed, never implied.** "Data as of 10:42" near the content, a manual refresh control, a freshness SLA per source, and an alert to the owner when data exceeds it. Silently presenting stale data as live is the single fastest trust-killer.
- **Fail honestly.** Auto-retry with backoff, then a clear banner ("Offline — reconnecting…") rather than frozen numbers.
- **Signal live updates gently.** 200–400ms fades or count-ups combat change blindness without disorienting; keep the grid stable so spatial memory of tile positions survives updates.

## Mobile

- Collapse to a single column below the breakpoint, re-sorted by importance — not merely reflowed in desktop order.
- Tighter KPI budget: 3–6 on mobile. Touch targets ≥48px. Vertical scroll only; horizontal panning is an anti-pattern.
