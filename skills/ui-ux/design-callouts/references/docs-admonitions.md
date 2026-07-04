# Docs admonitions reference

Detailed rules for callout boxes in static documentation — notes, tips, warnings and their kin. Synthesized from the Google, GitLab, Red Hat, Splunk, and Microsoft documentation style guides, the GFM/Asciidoctor/MkDocs/Docusaurus/MyST admonition vocabularies, and the ANSI Z535 hazard-communication standard the whole genre descends from.

## Type vocabulary

The working core is five types; what each means where the guides agree:

| Type | Meaning | Test |
| --- | --- | --- |
| **Note** | Contextual aside — useful, not required | Reader who skips it still succeeds |
| **Tip** | Optional better way | Reader who skips it succeeds, just less elegantly |
| **Important** | Required for success, but not dangerous | Reader who skips it fails the task |
| **Warning** | Danger exists — irreversible action, data loss | "Don't do this" or "this cannot be undone" |
| **Caution** | Proceed carefully | Care needed, consequences less severe than warning |

Known blur points, and how to resolve them:

- **Note vs important**: both say "don't skim past this"; the differentiator is stakes — note is optional context, important is success-critical. If in doubt whether content is important-tier, first ask whether it belongs in the main body instead (see below).
- **Warning vs caution**: Asciidoctor has the only crisp rule — caution advises the reader to *act carefully*; warning states that *danger exists*. Several guides (GitLab, Red Hat) resolve the ambiguity by eliminating caution entirely.
- **Type-set size**: guides that curate for consistency prune toward two to four types (GitLab reduced to note + warning); tooling ecosystems offer ten or more as a decorative palette. For any given docs corpus, a small set used consistently beats a rich one — every extra type is another distinction readers must learn and authors will misapply.
- **Success/positive callouts**: contested — Google restricts them to interactive content; some tooling offers them for static pages. Default to prose for positive outcomes in static docs.

## The admissibility test

Consensus across every style guide: **a callout holds supplementary signal — asides, risk flags, alternate paths — never load-bearing task content.** Google's phrasing is the cleanest: create a note only when the information is "relevant but not necessary" and "not part of the flow."

Never in an admonition:

- Procedural steps ("do not convert full procedural steps into notes" — Google; "do not include procedures in an admonition" — Red Hat)
- Prerequisites, or anything that must be read before starting
- Cross-references that are the primary path forward
- Anything whose removal would make the task impossible or unsafe

The default move when a note is tempting: rewrite it as ordinary prose in the flow, its own paragraph, or a titled section (GitLab's explicit escalation ladder). The one sanctioned duplication: safety-critical content lives in the main body *and* is echoed as a warning before the hazardous step.

## Placement

- Informational notes and tips: **after** the content they annotate; never immediately after a topic title, and never in place of prerequisites.
- Warnings gating a hazardous action: **before** the step — the reader must see the warning before performing the action it guards. Inherited directly from hazard-communication practice, which also recommends the two-tier pattern for long procedures: a general precautions section up front *plus* the specific warning repeated at the specific step, because readers jump straight to the task.

## Frequency budget

The most consistent theme in every guide consulted: overuse kills the mechanism.

- Google: "overuse diminishes their effectiveness... they begin to lose their visual distinctiveness."
- GitLab: "use notes sparingly"; Red Hat: "keep admonitions to a minimum."
- Hazard-communication literature names it "warning pollution" and gives the calibration rule: warn only where the reader isn't already expecting the danger — a qualified electrician doesn't need a shock warning on every step.
- The mechanism is habituation, and it is measured: clinical decision-support studies record 49–96% override rates for interruptive alerts. Readers learn to filter recurring boxed elements exactly as they filter banner ads.

No guide sets a hard numeric cap; the practical heuristic is one or two per screen of content, with any adjacent pair treated as a restructuring signal.

## Writing rules

- One to three sentences. Multi-paragraph content belongs in the main body under its own heading.
- The type label is the heading; a custom title is optional, never required.
- No procedures, numbered lists of steps, or link dumps inside the box — links only when essential to the point being flagged.
- House voice applies inside callouts; there is no special "callout voice."
- Severity must not be color-only: keep the type label text visible alongside icon and color.

## Stacking and nesting

Prohibited everywhere it is addressed:

- GitLab: "never have an alert box immediately follow another alert box" (absolute).
- Google: avoid grouping notices; if it seems necessary, reorganize the content.
- Red Hat: no multiple admonitions close together, no combining several under one label, no nesting.

Adjacent or nested callouts are always a restructuring signal — merge them, demote one to prose, or break the section up.

## Severity heritage (ANSI Z535)

The signal words come from industrial safety signage, where they form a strict consequence ladder: DANGER (will cause death/serious injury — used sparingly), WARNING (could cause death/injury), CAUTION (minor injury), NOTICE (property/process only). Software docs borrowed the words but flattened the ladder into parallel categories, which is why warning/caution/danger read inconsistently across tools. When a docs corpus needs a genuine severity ladder (destructive operations, irreversible data loss), restore the ANSI logic: reserve the top tier for the worst consequence class and use it rarely — a ladder where every rung is popular is not a ladder.
