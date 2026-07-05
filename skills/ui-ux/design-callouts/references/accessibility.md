# Callout accessibility reference

Normative requirements (WCAG 2.2, WAI-ARIA and its Authoring Practices Guide) and the practitioner consensus around them. These are compliance requirements, not preferences.

## ARIA semantics

Conflating the live-region roles is the most common accessibility bug in callout components:

- **`role="status"`** — implicit polite live region: announced when the screen reader is idle, without interruption. Use for confirmations, results, progress: success toasts, "saved" messages.
- **`role="alert"`** — implicit assertive + atomic live region: announced immediately, interrupting current speech. Reserve for errors, warnings, time-critical information; frequent alerts are disruptive by construction.
- **`role="log"`** — sequentially appended messages where history matters: notification centers, chat.
- **`role="alertdialog"`** — when the message requires a response: modal, focus moves in and is trapped, needs `aria-modal="true"`, a label, and `aria-describedby` pointing at the message text. If the user must close or answer the message, neither `alert` nor `status` is correct.

Mechanics every implementation must respect:

- **The DOM-priming rule**: a live region announces *changes* to a container the accessibility tree already knows. Render the container empty at page load and inject message text into it; injecting a pre-populated `role="alert"` element generally announces nothing. Content present at initial page render is likewise never announced — server-rendered banners need no live region.
- Announcements are ephemeral and semantic-free: once spoken they cannot be replayed, and any button inside the region is announced as plain text. Hence: no interactive content in live regions, and a persistent reviewable record for anything that matters.
- Keep to roughly one assertive and one polite region per page; compose each message fully and insert it in one operation.
- Support for `aria-relevant`, `aria-atomic`, and `aria-busy` is inconsistent across screen readers — do not build behavior that depends on them.

## The governing WCAG criteria

- **1.4.1 Use of Color (A)** — color never the sole carrier of severity. The spec's own failure examples are "error is shown in red" and "required fields are red." Icon fixes the visual channel only; assistive technology needs the severity in text (a visible "Success" heading, a hidden "Warning:" prefix) or in the role.
- **1.4.13 Content on Hover or Focus (AA)** — hover/focus-revealed content must be **dismissible** (Escape, without moving pointer or focus), **hoverable** (pointer can move onto the revealed content without it vanishing), and **persistent** (stays until trigger leaves, user dismisses, or the information expires). Native `title` tooltips are exempt only because authors cannot control them — they remain unusable for keyboard and touch users and must not be used.
- **2.2.1 Timing Adjustable (A)** — an auto-dismiss timer is a content-set time limit: the user must be able to turn it off, adjust it to 10× the default, or extend it — unless the same information or function is available by other means. A timed toast that is the only channel fails regardless of duration (Roselli's hard line); the standard escape hatch is a persistent notification log.
- **4.1.3 Status Messages (AA)** — status must be programmatically determinable so assistive technology can present it *without the message receiving focus*. This is the normative basis for "toasts never steal focus."
- **2.1.1 Keyboard (A)** — every dismiss button, embedded action, and popover trigger operable by keyboard alone.
- **3.3.1 Error Identification (A) / 3.3.3 Error Suggestion (AA)** — identify the erroring item and describe the problem in text; suggest the correction when known (except where doing so leaks security-relevant information, e.g. whether a username exists).
- **2.3.3 Animation from Interactions (AAA)** — suppress decorative entrance/exit motion (slide-ins, coach-mark pulses) under reduced-motion preferences; motion that itself carries the information (a progress spinner) is exempt.

## Focus management

- **Toasts and ambient status messages never move focus.** An unrequested focus shift is a context change — precisely what live regions exist to avoid.
- **The sanctioned exception**: after a user-initiated submit fails, the error summary on the freshly loaded page *does* receive focus (GOV.UK's pattern — the user caused the context change; focus placement orients rather than interrupts). GOV.UK applies the same logic to its success banner. Both keep an opt-out.
- **Tooltips**: focus stays on the trigger; the tooltip itself is never focusable; Escape dismisses without moving focus; connect via `aria-describedby` and `role="tooltip"`.
- **Interactive popovers/toggletips**: focus moves in on open and returns to the trigger on close (non-modal dialog model). If a toast must carry an action (avoid this), focus is managed deliberately and restored afterward — and a toast requiring focus has arguably stopped being a toast and should be an alert dialog.

## Auto-dismissing toasts: the compound failure and its mitigations

Screen-magnifier users may never see a corner toast; screen-reader announcements cannot be replayed; keyboard users race the timer to reach any control inside. Mitigations are layered, not alternatives:

1. Polite announcement (`role="status"`) for non-critical toasts; assertive only for genuine emergencies.
2. Never the sole channel — duplicate the action/outcome in persistent UI or a notification log.
3. Duration floor of at least 6 seconds, scaled up with message length (≈1s per extra 120 words).
4. Pause the timer on hover and keyboard focus.
5. No auto-dismiss at all when the toast is actionable or the severity is warning/error.
6. Reduced-motion-aware animation.

## Hard requirements per component

- **Banner (persistent)** — live-region role matching severity if injected dynamically (`alert` for error/warning, `status` otherwise); no role needed when server-rendered with the page. Severity = color + icon + text. Dismiss control keyboard-operable when dismissal is permitted; a banner gated on an unresolved system-wide condition (see main skill) has no dismiss control until the condition clears. No focus move on appearance.
- **Toast** — `role="status"` (or `log` with a history); container primed empty in the DOM; never steals focus; no essential interactive content; duration floor + hover/focus pause.
- **Tooltip** — appears on focus as well as hover; `role="tooltip"` + `aria-describedby`; Escape dismisses; hoverable and persistent per 1.4.13; never focusable; non-essential text only.
- **Toggletip / popover / coach mark** — click- or sequence-driven disclosure, not a live region; Escape closes; focus enters if interactive and returns to the trigger on close; programmatically launched teaching surfaces announce their intent on launch.
- **Error summary** — `role="alert"`, receives focus on the post-submit page load; entries link to their fields; wording identical to the inline errors; "Error: " prefixed to the page title.
- **Inline field error** — tied to the field programmatically (`aria-describedby`), problem described in text, input preserved.
- **Docs admonition (static)** — no live region; requirements are 1.4.1 (label text alongside icon and color — e.g. a visually hidden "Warning" prefix when the visible design is icon-only) and sound heading/landmark structure.
