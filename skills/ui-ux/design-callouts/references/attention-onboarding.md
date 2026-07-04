# Attention & onboarding reference

Detailed rules for proactive and on-demand guidance surfaces — tooltips through tours. Synthesized from Nielsen Norman Group research, Carbon, Material, Polaris, Fluent/WinUI, Spectrum, Atlassian, and Salesforce Lightning guidance.

## Component taxonomy by trigger

| Trigger | Component | Interactivity | Persistence |
| --- | --- | --- | --- |
| Hover or keyboard focus | Tooltip | None — text only | While hovered/focused |
| Click / tap | Toggletip, popover, contextual-help panel | Yes — links, buttons | Until dismissed |
| Programmatic (first encounter, condition) | Coach mark, teaching tip, spotlight, tour step | Yes — next/skip/dismiss | Until dismissed; never re-shown |
| Passive ambient | "New" badge | None | Until first interaction |

The tooltip/toggletip line is interactivity, and it is hard: tooltips never receive focus, so anything interactive inside one is unreachable for keyboard and assistive-technology users (Carbon's rule; the ARIA authoring guidance routes interactive popups to non-modal dialogs). Material's "rich tooltip" blurs this line by allowing buttons — when in doubt, apply the stricter taxonomy: interactive means click-triggered and focus-managed.

Coach mark anatomy (Fluent): the coach mark is the visual beacon anchored to the target element; the teaching bubble is the explanatory flyout it opens. Teaching surfaces are transient by design and therefore must never carry errors or status changes.

## Tooltip rules

The content test (NN/g): **is the information necessary to complete the task? If yes, it belongs on screen, not in a tooltip.** Corollaries, echoed across Polaris, Material, and Fluent:

- No critical information, no form errors, no interaction feedback.
- No field requirements or instructions — the tooltip disappears and the reader must hold its content in working memory to use it.
- No restating a visible label ("Add new line" tooltip on an "Add new line" button) — every hover costs a small interaction for zero information.
- Needing many tooltips is a symptom: "work on clarifying the design and the language in the experience" (Polaris). Fix the UI, not the tooltip count.

Trigger on hover *and* keyboard focus *and* (where supported) touch — hover-only tooltips exclude keyboard and touchscreen users.

Timing (NN/g's hover-disclosure numbers, the field's de facto reference — no design system publishes its own): visual feedback within 0.1s of cursor entry; reveal after a 0.3–0.5s pause; collapse only after the pointer has been away for more than 0.5s, so it can travel onto the tooltip without dismissing it.

## Interruption etiquette: pull before push

NN/g's framework: *pull* revelations surface when the user signals a need (hover, click on a help icon); *push* revelations interrupt on the product's schedule (launch tutorials, unprompted tours). The research verdict on push: it interrupts, does not measurably improve task performance, and is quickly forgotten — driven by the paradox of the active user (people want to act, not study), memory limits (out-of-context instructions must be memorized), and dismissal friction.

Defaults that follow:

- **Avoid onboarding whenever possible; invest in making the UI more usable instead.** A tour is an admission the UI could not explain itself.
- The one sanctioned push case: a genuinely novel interaction paradigm the user cannot be expected to guess — rare.
- No feature promotion at first launch; users chose the product for those features already.

## Tours and sequencing

When a tour survives the challenge above:

- At most 3 steps (Fluent's cap — the only numeric limit any design system commits to), one surface visible at a time (Atlassian's spotlight rule).
- Always skippable; skippable tours substantially outperform mandatory ones, and practitioner data puts typical tour completion near 5% — design assuming most users will never see step two.
- Let the user act between steps rather than chaining prompts; rapid-fire hints train faster dismissal.
- Show progress (step N of M) when there is more than one step.

Teach at the moment of relevance instead of upfront: short-term memory for an instruction fades in roughly 20 seconds, so an overlay shown when the feature becomes actionable beats the same overlay at launch. Empty states are the strongest teaching surface — they exist exactly when the user needs to act, and a good one states what will appear, why it matters, and one obvious action to create the first item.

## Dismissal and persistence

- Dismissed teaching surfaces stay dismissed — never re-show a dismissed coach mark automatically. Offer opt-in recall through a persistent help affordance instead.
- Two dismissal modes (WinUI): light-dismiss (closes on outside interaction, shows no close button) for glanceable tips; explicit-dismiss (close button) for content the user may want to keep open while acting.
- A "don't show tips again" control is a respectful default for any recurring tip mechanism.

## Badges

The weakest-evidenced area — no major design system publishes badge-lifetime guidance; the following is practitioner consensus, held with proportionate confidence:

- Clear on first interaction with the badged item, not on a timer; a stale badge trains users to ignore the mechanism.
- Reserve "New" for changes that affect the user's workflow; several badges at once are noise.
- Expire badges eventually even if never clicked.
