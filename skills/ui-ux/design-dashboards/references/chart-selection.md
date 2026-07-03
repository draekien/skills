# Chart selection decision tree

Synthesized from Andrew Abela's chart chooser and the Financial Times Visual Vocabulary. Route by the question the reader asks, not by the data's shape. Overriding meta-rule: the right chart is whatever the reader grasps fastest — when two candidates tie, pick the more familiar one.

## Root: what is the reader's question?

| Question | Category | Go to |
| --- | --- | --- |
| How has X changed over time? | Change over time | §1 |
| How big is X compared to Y? | Magnitude / ranking | §2 |
| How far is X from a target, zero, or average? | Deviation | §3 |
| How do two or more variables relate? | Correlation | §4 |
| How are values spread? | Distribution | §5 |
| What parts make up the whole? | Part-to-whole | §6 |
| Where does it happen? | Spatial | §7 |
| What moves between states? | Flow | §8 |

## 1. Change over time

- Default → **line chart**; add point markers when intervals are irregular. Practical ceiling ~3 series; beyond that, use small multiples rather than a spaghetti chart.
- One series, emphasis on discrete period values → **column chart** (zero-based).
- Amount and rate together → **line + column combo** (label both axes explicitly; see dual-axis caution in anti-patterns).
- Simplify to a before/after story with 2–3 time points → **slope chart**.
- Cyclical/calendar pattern matters more than precise values → **calendar heatmap**.
- Future projection with uncertainty → **fan chart**.
- Two variables changing together over time → **connected scatterplot**.
- Both date and duration matter → **timeline/Gantt-style (Priestley) chart**.
- Area charts: use with care — fine for total change, weak for reading individual components of a stacked total.

## 2. Magnitude and ranking

- Compare sizes, short labels → **column chart**, axis starting at zero, always.
- Long category labels → **horizontal bar chart**.
- Rank order matters more than exact magnitude → **sorted bar** or **lollipop** (lollipop when drawing attention to the value ends).
- Two series → **paired bars**. More than two series → paired bars break down; use **small multiples** or a **table**.
- Rank change over time or between two states → **slope chart**.
- Many multi-variable comparisons in small space → **radar** or **parallel coordinates** — both are last resorts; axis order changes the story, so arrange axes deliberately.
- Whole-number counts for non-expert readers → **pictogram/isotype** (whole icons only, never partial).

## 3. Deviation

- Values above/below a reference → **diverging bar**.
- Sentiment or agree/neutral/disagree scales → **diverging stacked bar**.
- One value split into two contrasting components → **spine chart**.
- Balance versus a baseline over time → **surplus/deficit filled line**.

## 4. Correlation

- Two continuous variables → **scatterplot**. Caution: readers infer causation from correlation charts; annotate or caveat when the link is not causal.
- Third variable needed → **bubble chart** (size encodes it; size is read imprecisely — fine for "big vs small", not fine differences).
- Relationship between two categorical dimensions → **XY heatmap** (patterns, not precise amounts).

## 5. Distribution

- One group → **histogram** (keep bin gaps minimal).
- Compare several groups' distributions → **boxplot**; when distributions are complex or multimodal → **violin plot**.
- Show individual values → **dot strip plot** (weak when many values coincide) or **barcode plot**.
- Age/sex structure → **population pyramid**.
- Inequality → **cumulative curve**.

## 6. Part-to-whole

- Single snapshot, ≤5 slices, precision unimportant → **pie or donut** (donut's center can hold the total). Beyond 5 slices or comparing across snapshots, pies fail — angles are read poorly.
- Composition across categories or over time → **stacked bar/column**; proportions only (each bar to 100%) → **proportional stacked bar**.
- Hierarchical composition → **treemap** (weak with many small segments; area is read imprecisely — exploratory use, not KPI display).
- Components include negatives (budget bridges, P&L walk) → **waterfall**.
- Percentages with whole numbers for non-expert readers → **gridplot** (10×10 waffle).

## 7. Spatial

- Rates or ratios by region → **choropleth**. Never map totals on a choropleth — large regions dominate regardless of the story.
- Totals or counts by location → **proportional symbol map**.
- Movement between places → **flow map**.
- Individual event locations → **dot density map**.
- De-emphasize land area, emphasize per-region values → **cartogram** (equal-area or scaled).

## 8. Flow

- Volumes through a multi-step process → **Sankey**.
- Sequential additive/subtractive steps → **waterfall**.
- Two-way flows in a matrix → **chord diagram**.
- Strength of interconnection → **network diagram**.

## Table vs chart vs KPI card

- Reader asks "what is the exact value" or looks up specific records → **table**. Precision-first readers (finance, ops, account management) usually want tables they can scan and export.
- Reader asks "what is the pattern/trend/shape" → **chart**. Headline-first readers (executives) usually want charts.
- Reader asks "am I on track" about a single metric → **KPI card** (value + delta + sparkline + status color; see skill body).
- Reader needs both headline and detail → summary chart with a detail table beneath it, or sparklines embedded in table cells.
- More than two series to compare precisely, or mixed text-and-number attributes → table beats any chart.
