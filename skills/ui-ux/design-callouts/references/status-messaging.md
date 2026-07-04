# Status messaging reference

Detailed rules for reactive messages — feedback about action outcomes and system state. Synthesized from Material, Carbon, Polaris, Atlassian, GOV.UK, Fluent, Spectrum, and Nielsen Norman Group guidance; where systems disagree, the disagreement is stated so the choice is deliberate.

## Severity taxonomy

Info, success, warning, and error are universal. Systems split on whether "critical" is a fifth severity or a component decision:

- Polaris treats critical as a first-class banner tone beyond warning.
- Atlassian, Fluent, and GOV.UK express criticality by escalating the *component* (to banner or modal), not by adding a color.

Prefer the second model: severity picks the color set; consequence picks the component. Fluent's per-severity usage rules are a good default vocabulary — error = "must be addressed before continuing"; warning = temporary or risky states; success = something went right on this surface; info = helpful, no action required.

NN/g adds an orthogonal axis worth checking against: is the message an *indicator* (passive, tied to an element), a *validation* (input-specific), or a *notification* (system-triggered)? A message that is really a validation must follow the form-validation pattern below regardless of its severity.

## Component selection

The consensus ladder: **alert dialog for blocking decisions; banner for page/system-level persistent conditions; section or inline message for localized issues; toast for low-stakes transient confirmation.**

- Fluent frames the inline message bar as the default, with routing rules away from it: preventing a destructive action → alert dialog; time-sensitive and about somewhere else → toast.
- Atlassian scopes banners hard: "only for critical system-level messaging... about loss of data or functionality."
- GOV.UK prohibits notification banners for validation errors outright, and never shows a notification banner and an error summary on the same page.
- NN/g documents the failure mode that anchors the toast rule: a user waited five minutes on a broken page because the error had faded away in a corner toast.
- Carbon bars interactive content from toasts on WCAG grounds; anything needing an action becomes an "actionable notification" that persists and manages focus.

Known tension: Atlassian and Spectrum put "critical, needs addressing" in persistent non-blocking banners; NN/g reserves that register for a blocking alert dialog. Resolve by asking whether the user may safely continue working while the condition holds — yes → banner; no → alert dialog.

## Placement

- Page-level banner: top of the page, before the main heading, in the document flow (shifting content down, not overlaying).
- Section/element message: immediately adjacent to what it describes. Polaris's proximity ladder — page-level below the page header, section-level below the section heading, element-level immediately above or below the element — with prominence pared back at each step down.
- Field error: directly after the field's label and hint, visually connected to the field (GOV.UK uses a red left border).
- Toast: a screen corner, out of the reading flow. No cross-system consensus on which corner (Material has anchored bottom-center, Atlassian bottom-left, Carbon top-right) — pick one and never vary it within a product.
- Forms: an inline message slot at the bottom of the form, just above the submit button, catches submission-level problems (Carbon).

## Persistence and dismissal

- Toast durations: ~5 seconds is the common default; Spectrum sets a 6-second minimum plus 1 second per extra 120 words (reading-time scaled). Use ≥6s scaled to length, paused on hover and focus.
- **An attached action revokes auto-dismiss** (Carbon, Spectrum) — the toast persists until acted on or dismissed. Polaris instead allows a timed actionable toast with a 10-second floor; prefer the stricter rule, and better still route actionable messages to a persistent component in the first place.
- Errors and warnings never auto-dismiss. Fluent goes further: a warning/error message bar dismissed without resolving the condition reappears next session.
- Critical banners are not dismissible while the condition holds (Polaris); they disappear when the underlying state resolves (Spectrum).

## Content rules

- Structure: what happened → what to do about it. Plain language, one to two sentences, most critical information first, one theme per message.
- Banned phrasing: generic ("an error occurred"), jargon and bare error codes, blame words ("invalid", "illegal", "forbidden"), apologies ("sorry").
- Errors and warnings must carry a path to resolution — Fluent requires a link or button on every error/warning message bar.
- Action labels: one or two words, leading with a verb.
- Two error-message shapes by context: instruction for an empty required field ("Enter your first name"); description for failed validation ("Name must be 35 characters or less"). Echo the field's own label wording.

## Form validation

The GOV.UK error-summary pattern is the canonical implementation:

- On failed submit, always show both an error summary at the top of the page *and* an inline error at each failing field — even for a single error. Wording must match exactly between the two.
- Move keyboard focus to the summary on page load; each summary entry links to its field (first sub-field for composite inputs, first option for radio/checkbox groups).
- Prefix the page title with "Error: " so the failure announces in the tab and to assistive technology.
- Preserve all user input — passing and failing answers alike.

NN/g refinements: validate on field exit rather than only on submit, but never mid-entry; a summary alone is insufficient (it forces searching and memorizing); errors in tooltips are unfindable; the same error hit three or more times in one attempt is a design problem, not a messaging problem. Positive inline confirmation while typing suits high-effort fields (passwords); page-level success banners are for after submission.

## Stacking and queueing

Suppress simultaneity — messages multiplying on screen is a design failure:

- Material: one snackbar at a time. Spectrum: additional toasts queue and wait. Carbon: visible stacking, newest on top. Fluent: multiple message bars in one slot collapse into an accordion headed by the highest severity with a count badge.
- Persistent tiers have no queueing mechanism anywhere — authors are expected to prevent collision. GOV.UK: one notification banner per page; combine related messages.

Default: queue transient messages one at a time; merge persistent ones at the source.
