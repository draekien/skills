---
name: playwright-testing
description: Writes, fixes and audits Playwright Test end-to-end tests — locators read from the rendered page, web-first assertions, isolated tests, setup-project auth, mocked third-party calls. Use when writing or editing a spec that imports `@playwright/test`, when a Playwright test is flaky, times out or fails only in CI, or when the user says "write a playwright test", "fix this flaky e2e test", "review these playwright tests". Not for browser automation outside a test suite.
argument-hint: "[audit] [--fix] [path]"
---

# Playwright testing

If the first argument is `audit`, or the request is to review or audit existing specs, run audit mode. Otherwise run writing mode, which includes fixing a failing or flaky test. `--fix` given without `audit` means `audit --fix`. Any other argument is `path`; with no `path`, use the config's `testDir`.

- `audit [--fix] [path]` — apply every rule below to the specs, fixtures and `playwright.config.*` under `path`. Report each violation as `file:line`, the rule, and the replacement code. Without `--fix`, change nothing; the audit is done when every file under `path` has been read and every violation reported. With `--fix`, apply the replacements, then run [Verify](#verify).
- Writing — apply the rules below to the tests being written or changed, within `path` if given, and end on [Verify](#verify).

## Look it up

The rules in this skill are principles. The API names, options, defaults, config keys and CLI flags that carry them out change between Playwright releases, so this skill does not state them: read them from the page in the [Docs index](#docs-index) for the topic, at the time you write the code.

- Run `npx playwright --version` before the first lookup. playwright.dev documents the latest release. Each API entry shows the version it was added in; when that is newer than the installed version, find what the installed version offers in the release notes.
- Where a page in the index has moved, search playwright.dev for the topic named in the index row.

Done when every API call, option, config key and CLI flag you write was read on a docs page during this task, not recalled.

## Read the page before writing locators

A locator written from the component source guesses the accessible name, and the rendered page decides it: a label joined from two elements, an icon button named by `aria-label`, text changed by translation. Read the rendered accessibility tree first.

Default tool: `playwright-cli`, Playwright's command-line browser for agents. It opens a page, prints its accessibility tree as a snapshot, loads saved signed-in state, and prints the Playwright code for each action it performs. Playwright publishes a skill that teaches its commands; if that skill is installed, follow it, otherwise read the `playwright-cli` pages in the [Docs index](#docs-index). Where `playwright-cli` cannot be installed, log an aria snapshot of the page from a throwaway test instead.

```ts
✗ page.locator('[ref=e9]')
✓ page.getByRole('button', { name: 'Place order' })
```

Snapshot refs such as `e9` exist only inside `playwright-cli` and change on every page change. Never put a ref in a spec; take the role and name from the snapshot line.

This step is done when every locator in the spec matches a role and name, label or text in a snapshot taken in the state the test acts on: after the clicks and navigation that precede it, not only on page load.

## Locators

Locate an element by what the user perceives, in this order: role with accessible name; label; placeholder; visible text for non-interactive elements; alt text or title; test id when the element has no stable accessible name. The locators page lists the method for each.

```ts
✗ page.locator('button.buttonIcon.episode-actions-later')
✓ page.getByRole('button', { name: 'Watch later' })
```

CSS and XPath selectors break when markup changes. Use them only when nothing in the list applies, and say why in the final summary or audit report.

**Strictness.** An action on a locator that matches more than one element fails. Narrow the locator by chaining and filtering; do not pick by position (first, last, nth), which acts on whichever element happens to be in that position.

```ts
✗ await page.getByRole('button', { name: 'Add to cart' }).first().click()
✓ await page
    .getByRole('listitem')
    .filter({ hasText: 'Product 2' })
    .getByRole('button', { name: 'Add to cart' })
    .click()
```

## Assertions and waiting

Actions wait for the element to be actionable, and **web-first assertions** — `expect(locator)` matchers such as `toBeVisible` — retry until they pass or time out. A test never waits explicitly for the page to be ready.

```ts
✗ expect(await page.getByText('Order placed').isVisible()).toBe(true)
✓ await expect(page.getByText('Order placed')).toBeVisible()
```

A call that returns a value from the page reads it once, and a generic matcher on that value does not retry, so it fails whenever the page has not updated yet. Use the web-first assertion for the same check; the assertions page lists which matchers retry.

Never add these to get a test passing. Each hides the condition the test is really waiting for:

| Do not use | Use instead |
| --- | --- |
| a fixed sleep | a web-first assertion on the state being waited for |
| waiting for the network to go idle | a web-first assertion on content that appears once loading is done |
| a forced action that skips actionability checks | find what blocks the element (an overlay, a disabled state, an animation) and assert it has cleared |
| a raised timeout | find the condition the test is waiting for and assert on it |
| a selector-string method on `page`, or an element handle | the same operation on a locator |

The API reference marks the methods it discourages; check the entry before using any method on `page`.

For a value that is not a locator (an API response, a database row, a file), use the polling form of `expect`; to retry a block of several statements, use the retrying-block form. Use soft assertions when one test checks several independent things and every failure should be reported.

## Isolation

Every test gets a fresh browser context, so no cookies or storage carry over from another test; the only starting state is what the config's saved storage state loads. Files run in parallel and a failed test restarts its worker, so no test may depend on another having run first.

- Create the data a test needs inside that test or its fixtures. Do not read data another test created.
- Do not switch a file to serial mode to make dependent tests pass; make each test set up its own state.
- Put shared setup in a fixture rather than a `beforeEach` repeated across files. A fixture runs only for tests that request it and keeps its teardown next to its setup.

## Authentication

Log in once in a setup project, save the browser's storage state to a file, and have the test projects load it. Do not log in through the UI in every test.

- Add the saved state directory to `.gitignore`. The file holds cookies that can sign in as the test account.
- One shared account works only when no test changes server-side state another test reads. When tests change settings, carts or other per-account state in parallel, give each worker its own account.
- A file that tests the signed-out experience resets the storage state to empty.
- Check on the auth page which storage the saved state includes. An app that keeps its token somewhere it excludes needs the manual restore that page shows.

## Network

Test only what the project controls. Mock third-party services (payment providers, analytics, maps, external APIs) by routing their requests; do not let a test depend on a server, banner or rate limit outside the project.

- To change one field of a real response, fetch the real response inside the route handler and fulfil with the edited body.
- To replay many recorded calls, record them to a HAR file once and replay it. Read the mock page's rules for which requests match a recording and what happens to one that does not.
- Do not mock the project's own backend in a test meant to cover it end to end. Control its data instead: seed it in a fixture, or run against an environment whose data does not change.

## Configuration

When writing the first tests in a project, check that the config has each of these, and add what is missing:

- a base URL, so specs navigate by path and run against any environment;
- a web server entry that starts the app, reusing a running server locally;
- retries on CI only. Retries let a CI run finish and classify a test that passes on retry as flaky; they are not a fix for a flaky test, so never add or raise them to make one test pass;
- traces recorded on the first retry, not on every test, which slows every run;
- one project per browser the product supports;
- the lint rule that reports unawaited promises (`@typescript-eslint/no-floating-promises`), and a type check in CI. A missing `await` on an action or assertion is the bug review most often misses, and the rule finds every one.

## Fixing a failing or flaky test

Find the cause before changing the test. The changes that make a flaky test pass without a cause (a sleep, a longer timeout, a forced action, retries, serial mode) hide the race instead of removing it.

1. **Reproduce.** Run the one test many times with retries disabled; the CLI page lists the flags. If it never fails, run the whole file the same way: a test that fails only alongside others points to shared state, not timing. If it still never fails, report it as unreproduced with the commands tried, and do not change the test.
2. **Inspect.** Run the test in debug mode, attach `playwright-cli` to it, and step to the failing line, reading the snapshot, console errors and network requests there. The `playwright-cli` test-debugging page gives the commands. For a failure that happens only in CI, open the trace recorded on the retry.
3. **Fix the cause.** The usual causes, in order: a value assertion that should be a web-first assertion; a locator that matches a different element while the page is still rendering; an action on an element covered by a loading overlay; data left by another test.
4. **Confirm.** Rerun the step 1 command. The test is fixed when it passes every repetition.

## Verify

Writing, fixing and `audit --fix` end here. Run the changed specs several times each with retries disabled, so a pass on retry cannot count as a pass.

The work is done when:

- every changed test passes every repetition;
- the project's type-check script, or `npx tsc --noEmit` where `package.json` defines none, exits 0;
- a reread of each changed file finds no locator, assertion or wait that a rule above replaces.

If the specs cannot run (no app server, missing credentials), the work is not done: report why and list the files left unverified. Report any test that could not be made to pass with its failing assertion and trace path.

## Traps to check

Each of these has caught tests written from memory. Before relying on the behaviour, read the current answer on the page named:

- What timeout the retrying-block form of `expect` uses by default, and whether it follows the assertion timeout — assertions page.
- Whether getting every match of a locator as a list waits for the list to finish loading — Locator API.
- Whether a `has` filter's inner locator is matched from the page or from the outer match, and whether `hasText` is case-sensitive — locators page.
- What `or` does when both sides match — locators page.
- Whether UI mode runs setup projects by default — auth page.
- Which browsers CI installs — install only those the config uses; best-practices page.

## Docs index

| Topic | Page |
| --- | --- |
| Principles behind every rule here | <https://playwright.dev/docs/best-practices> |
| Locator methods, filtering, chaining, strictness | <https://playwright.dev/docs/locators> |
| Which matchers retry; polling, retrying blocks, soft assertions | <https://playwright.dev/docs/test-assertions> |
| Every web-first matcher and its options | <https://playwright.dev/docs/api/class-locatorassertions> |
| Locator methods, added-in versions, discouraged notes | <https://playwright.dev/docs/api/class-locator> |
| Page methods, discouraged notes | <https://playwright.dev/docs/api/class-page> |
| Which checks each action waits for | <https://playwright.dev/docs/actionability> |
| Timeouts and their defaults | <https://playwright.dev/docs/test-timeouts> |
| Test isolation | <https://playwright.dev/docs/browser-contexts> |
| Fixtures | <https://playwright.dev/docs/test-fixtures> |
| Page object models | <https://playwright.dev/docs/pom> |
| Setup project, saved state, per-worker accounts | <https://playwright.dev/docs/auth> |
| Routing and mocking requests, HAR replay | <https://playwright.dev/docs/mock> |
| Network events and request handling | <https://playwright.dev/docs/network> |
| Config file options | <https://playwright.dev/docs/test-configuration> |
| `use` options: base URL, test id attribute, storage state | <https://playwright.dev/docs/test-use-options> |
| CLI flags | <https://playwright.dev/docs/test-cli> |
| Retries and flaky classification | <https://playwright.dev/docs/test-retries> |
| Parallelism, workers, serial mode | <https://playwright.dev/docs/test-parallel> |
| Sharding | <https://playwright.dev/docs/test-sharding> |
| Debug mode | <https://playwright.dev/docs/debug> |
| Traces | <https://playwright.dev/docs/trace-viewer> |
| UI mode | <https://playwright.dev/docs/test-ui-mode> |
| Aria snapshots | <https://playwright.dev/docs/aria-snapshots> |
| Visual comparisons | <https://playwright.dev/docs/test-snapshots> |
| Recording locators | <https://playwright.dev/docs/codegen> |
| CI setup and browser installs | <https://playwright.dev/docs/ci-intro> |
| Changes between versions | <https://playwright.dev/docs/release-notes> |
| `playwright-cli` install | <https://playwright.dev/agent-cli/installation> |
| `playwright-cli` skill | <https://playwright.dev/agent-cli/skills> |
| `playwright-cli` snapshots and refs | <https://playwright.dev/agent-cli/snapshots> |
| `playwright-cli` saved storage state | <https://playwright.dev/agent-cli/commands/storage> |
| `playwright-cli` attached to a paused test | <https://playwright.dev/agent-cli/commands/test-debugging> |
| Unawaited promise lint rule | <https://typescript-eslint.io/rules/no-floating-promises/> |
