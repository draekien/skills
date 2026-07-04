---
name: design-callouts
description: Applies callout design principles to design, build, review, or write callouts — classifying whether the need is a status message, a documentation admonition, or an attention/onboarding overlay, selecting the least disruptive component that does the job, and enforcing accessibility requirements. Use when designing or reviewing notifications, toasts, banners, alerts, error messages, tooltips, onboarding tours, or admonitions in docs.
disable-model-invocation: true
---

A callout spends the reader's attention to redirect it. Callouts fail in two opposite ways: too quiet — an error vanishing in a five-second toast nobody saw — or too loud — a page of warning boxes readers have learned to skip. Both come from choosing the component before classifying the message. Every rule below derives from three commitments:

- **Match disruption to consequence.** Interruption is a cost; pay it in proportion to what happens if the message is missed. A missable confirmation earns a transient toast; a data-loss warning the user can keep working alongside earns a persistent banner; a decision the user must resolve before safely continuing earns an alert dialog. Escalating past the consequence trains users to ignore the tier; underspending loses the message.
- **Never the only channel.** Anything the user must see or act on needs a persistent home — the main content flow, an inline message, a notification log. Transient and hover-triggered surfaces may amplify essential content but must never own it. Throughout this skill, content or an action is *essential* when losing it makes the task impossible, unsafe, or unrecoverable; an action is essential when no other route to the same outcome exists.
- **Every callout devalues the next.** Attention habituates: clinical-alert studies show 49–96% of interruptive alerts get overridden once they become routine. Treat callouts as a budget; when two compete, merge or demote one.

These rules apply identically when designing from scratch and when auditing — auditing is holding what exists against the same commitments and reporting each violation with its fix.

## Classify the message first

The three branches follow different rules; misclassifying is the root error behind most callout failures. Pick by trigger:

| Branch | Trigger | Reader's job | Components |
| --- | --- | --- | --- |
| **Status messaging** | An action outcome or system state (reactive) | Absorb; act to resolve if needed | Banner, section/inline message, toast, validation error, error summary, alert dialog |
| **Docs admonitions** | Author decision in static content | Read in context; adjust behavior | Note, tip, important, warning, caution blocks |
| **Attention & onboarding** | Product wants to teach, or user asks for help | Learn; dismiss | Tooltip, toggletip, popover, coach mark, tour, "New" badge |

Keep the branches clean: education surfaces must not carry errors or status (a teaching tip reporting a failure will be dismissed as marketing), and status surfaces must not carry promotion.

Before choosing any component, confirm a callout is warranted at all:

- Content essential to completing the task → main body, field label, or button label — never a callout.
- Content already visible on screen → nothing; delete the redundant callout.
- A second callout adjacent to another, or a third competing in the same view → restructure the content or flow instead of adding one more.

## Status messages

Decide by consequence and scope, in order:

1. **User must decide before anything else continues** (destructive or blocking) → alert dialog: modal, focus-trapped.
2. **Form validation failed** → inline error at each field plus an error summary that receives focus, with identical wording in both, each summary entry linking to its field. Never report validation in a toast or notification banner.
3. **System-wide condition needing attention until resolved** → page-top banner: persistent, never auto-dismissed, non-dismissible while the condition holds.
4. **Scoped to one section or object** → section/inline message placed immediately adjacent to what it describes — proximity tells the reader what the message is about.
5. **Ignorable confirmation with zero consequence if missed** → toast. No actions inside — a toast that needs a button (even Undo) must persist until dismissed and offer the same action in persistent UI, and at that point an inline or actionable message is usually the better component. At least a 6-second floor scaled to message length, paused on hover/focus; a persistent record elsewhere.
6. **A running history of outcomes the user may review later** → notification center / log: a persistent list, newest first. Individual events may also surface as toasts, but the log is their permanent home.

Cross-cutting rules:

- **Severity is color + icon + text, always all three.** Info / success / warning / error is the universal scale; color alone fails 1 in 20 readers and every screen reader (WCAG 1.4.1).
- **An action revokes auto-dismiss.** The moment a message carries a button, it persists until acted on or dismissed — every mature design system converges on this.
- **Say what happened and how to fix it**, in plain language, one to two sentences, leading with the most critical fact. No "an error occurred", no blame ("invalid", "forbidden"), no apology theatrics. Errors and warnings must include a path to resolution — a passive error is a dead end.

Severity taxonomies, placement conventions, persistence rules, validation patterns, and stacking models: [references/status-messaging.md](references/status-messaging.md).

## Docs admonitions

- **The admissibility test:** a callout holds information that is *supplementary* to the task — an aside, a risk flag, an alternate path. If removing it would make the task impossible or unsafe, the content belongs in the main body. Never put steps, prerequisites, or required parameters in an admonition.
- **Placement follows function:** informational notes go after the content they annotate; warnings that gate a hazardous action go before the step, so they are read before the damage is done.
- **Small type vocabulary, used sparingly:** note (contextual), tip (optional improvement), important (required for success), warning/caution (consequences). Fewer types used consistently beat a rich palette. Never stack two admonitions adjacently or nest them — both signal the content needs restructuring.
- Keep each admonition to one to three sentences; longer content belongs in a titled section.

Type-set comparisons, the warning-severity ladder, and writing rules: [references/docs-admonitions.md](references/docs-admonitions.md).

## Attention & onboarding

Prefer pull over push — help that appears when the user asks for it beats help that interrupts:

1. **Labeling or describing a control** → tooltip, on hover *and* keyboard focus. Content must pass the tooltip test: not essential to the task, and not already visible. Nothing interactive inside — a tooltip needing a button is a toggletip/popover.
2. **Richer or interactive help on demand** → toggletip / popover / contextual-help panel, click-triggered, focus-managed.
3. **Teaching proactively** → coach mark or teaching tip, only for genuinely novel interactions the UI cannot make self-evident — the default answer to "should we add a tour?" is to make the UI clearer instead. One visible at a time, at most 3 steps, always skippable, never re-shown after dismissal. Teach at the moment of relevance — an empty state with one clear action outperforms an upfront tour, because instructions given before they are needed are forgotten in seconds.
4. **Flagging new features passively** → badge, reserved for workflow-affecting changes, cleared on first interaction.

Component taxonomy, hover-timing numbers, tour evidence, and badge rules: [references/attention-onboarding.md](references/attention-onboarding.md).

## Accessibility non-negotiables

- Status messages announce without moving focus: `role="status"` (polite) for confirmations, `role="alert"` (assertive) for errors/warnings, `role="alertdialog"` only when a response is required (WCAG 4.1.3).
- Render the live-region container empty at page load and inject message text into it — a region created already-populated announces nothing. Content server-rendered with the page is never announced and needs no live-region role at all.
- Toasts never steal focus. The one sanctioned focus move: an error summary (or success banner) on a fresh page load after the user's own submit.
- Hover/focus-revealed content must be dismissible with Escape, hoverable (pointer can travel onto it), and persistent until the trigger leaves (WCAG 1.4.13). Native `title`-attribute tooltips fail keyboard and touch users — never use them.
- Auto-dismiss is a content-set time limit (WCAG 2.2.1): duration floors, pause on hover/focus, and a redundant persistent channel are the minimum mitigations.
- Every dismiss button and embedded action is keyboard-operable; entrance/exit animation respects reduced-motion preferences.

Full ARIA semantics, per-component hard requirements, and focus-management rules: [references/accessibility.md](references/accessibility.md).

## Anti-patterns

Name these on sight — when auditing, report each finding as the named anti-pattern with its fix:

- **Error in a toast** — the strongest cross-system prohibition in the field. Fix: persistent banner, inline message, or error summary.
- **Color-only severity** — red box with no icon or text label. Fix: color + icon + text, with the ARIA role mirroring severity.
- **Essential or interactive content in a tooltip** — instructions, errors, links, buttons. Fix: main UI for essentials; toggletip/popover for interaction.
- **Redundant tooltip** — restates the visible label. Fix: delete it.
- **Auto-dismiss as the only channel** — an Undo or outcome that exists solely in a timed toast. Fix: duration floor, hover-pause, persistent record.
- **Callout overuse** — warnings on routine content until readers skip them all. Fix: enforce the budget; merge or demote.
- **Task-critical content in an admonition** — required steps in a Note box readers skip. Fix: move to the main flow.
- **Front-loaded tour** — multi-step overlay before the user has tried anything. Fix: contextual teaching at the moment of need.

The full catalog — seventeen anti-patterns with recognition cues and corrections: [references/anti-patterns.md](references/anti-patterns.md).
