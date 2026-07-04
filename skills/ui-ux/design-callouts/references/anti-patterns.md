# Anti-pattern catalog

Seventeen callout failures in five groups. Each entry: how to recognize it, why it fails, and the correction. When auditing, report findings as the named anti-pattern — recognition plus mechanism makes the fix unambiguous.

## Wrong component

**1. Error in a toast.** A save failure, validation error, or permission problem announced in a corner toast that fades in seconds. The user needs to act, but the message self-destructs; magnifier users never see it, screen-reader users can't reach it in time. The strongest cross-system prohibition in the field. → Persistent banner (system-wide), section/inline message (scoped), or error summary (forms). Toasts only for outcomes ignorable with zero consequence.

**2. Validation in a notification banner.** Form errors reported in a page-top notification banner — or a notification banner and an error summary shown together, splitting attention. → Error summary (focused, linking to fields) plus matching inline errors; notification banners only for things unrelated to the page's task. One banner per page; merge related messages.

**3. Task-critical content in an admonition.** A required step, prerequisite, or parameter inside a Note box. Experienced readers skip callouts; anything needed to complete the task must live in the main flow. → Move it into the procedure body; callouts carry only supplementary signal.

**4. Education surface carrying status.** A teaching tip reporting an error, or a status banner promoting a feature. Teaching surfaces are transient and get dismissed as marketing; mixing feedback and promotion breaks users' learned expectations of both. → Feedback components for outcomes, education components for teaching, each within its own frequency budget.

## Too much

**5. Callout overuse.** Multiple admonitions per section, warnings on routine content, "important" on everything. Each callout devalues the next; habituation is measured — interruptive clinical alerts get overridden 49–96% of the time once routine. → Budget roughly one per screen of content; merge or demote when two compete; reserve warning severity for real consequences.

**6. Front-loaded tour.** A multi-step overlay at first launch, before the user has tried anything. Instructions given before they're needed are forgotten in about 20 seconds; typical tour completion is near 5%; tutorials don't measurably improve task performance. → Contextual teaching at the moment of need — empty states with one clear action, single coach marks when the feature becomes relevant, at most 3 steps, always skippable.

**7. Badge spam.** "New" badges scattered across a menu, or badges persisting after the user has seen the feature. Badges work by scarcity; stale ones train users to ignore the mechanism. → Reserve for workflow-affecting changes; clear on first interaction; expire regardless.

## Wrong content

**8. Redundant tooltip.** A "Search" tooltip on a button labeled "Search." Adds hover cost and double-announces for screen readers while conveying nothing. → Delete it. If an icon needs a name, that name is its accessible label, not a decoration.

**9. Essential or interactive content in a tooltip.** Instructions, field requirements, errors, links, or buttons inside a hover surface. Tooltips are unreachable on touch, disappear on pointer-move, and never receive focus — interactive content inside is unusable by keyboard. → Essentials into the main UI; interaction into a click-triggered toggletip or popover.

**10. Generic, blaming, or apologetic errors.** "An error occurred", "Invalid input", "Oops! Sorry!!". Fails to identify the problem or suggest the fix (WCAG 3.3.1/3.3.3) and erodes trust. → Say what happened and exactly how to fix it, in the user's vocabulary; no blame words, no apology theatrics; identical wording in summary and field.

**11. Dead-end error.** An error or warning with no path forward — no link, no action, no instruction. The user is told something is wrong and left stranded. → Every error/warning carries its resolution: a fix instruction, a retry, or a link to the place the fix happens.

## Accessibility failures

**12. Color-only severity.** Red, amber, and green boxes distinguished by background alone. Fails 1-in-20 readers with color-vision deficiency and every screen reader (WCAG 1.4.1). → Severity = color + icon + text label, with the ARIA role mirroring severity.

**13. Focus-stealing status message.** A toast or banner grabbing keyboard focus mid-task, losing the user's place. Status must announce without focus (WCAG 4.1.3); the only sanctioned move is the error summary/success banner on a fresh page load after the user's own submit. → Live regions for mid-task messages; deliberate focus only on user-initiated context changes.

**14. Live region created on demand.** Injecting a fully populated `role="alert"` element at announcement time. Screen readers announce *changes* to known regions; a region arriving pre-filled usually announces nothing — the message silently vanishes for assistive-technology users. → Render the empty container at page load; inject the text into it.

**15. Auto-dismiss as the only channel.** A timed toast holding the sole record of an outcome or the only path to an action (Undo living nowhere else). A content-set time limit without an alternative route fails WCAG 2.2.1 regardless of duration. → Duration floor scaled to length, pause on hover/focus, no auto-dismiss when actionable, persistent log or redundant UI path.

**16. Hover-only or `title`-attribute tooltip.** Appears on mouse hover but not keyboard focus, vanishes when the pointer moves toward it, can't be Escape-dismissed — or the native `title` attribute doing tooltip duty (invisible to keyboard and touch, inconsistently exposed to assistive technology). → Hover *and* focus triggers, hoverable, Escape to dismiss, `role="tooltip"` + `aria-describedby`.

## Documentation placement

**17. Stacked, nested, or misplaced admonitions.** Two callouts back-to-back, a callout inside a callout, or a "this deletes all data" warning *after* the destructive step it guards. Adjacent boxes compete and read as decoration; readers execute steps as they read, so late warnings arrive after the damage. → Merge or demote adjacent callouts; never nest; hazard warnings before the step, informational notes after their referent.
