---
name: biome-plugins
description: Authors and debugs Biome linter plugins written in GritQL, verifying each fires only where intended. Use when a project needs a custom Biome lint rule for a convention no built-in rule covers, when writing or debugging a `.grit` file or the `plugins` key in `biome.json`, or when the user says "write a biome plugin", "custom biome rule", "gritql rule", "ban this pattern with biome".
argument-hint: "[rule-to-enforce]"
---

A Biome plugin is a GritQL pattern plus a `register_diagnostic()` call, registered under `plugins` in `biome.json`. The pattern is easy to write and easy to get wrong: GritQL matches structurally, so a pattern that looks precise routinely matches more or less than intended, and Biome reports almost nothing about why. The work is therefore **fixture-first** — the cases decide what the pattern must do, and the pattern is done only when `biome lint` proves it against them.

## Check for a built-in rule first

Before writing a plugin, search Biome's rule list (`https://biomejs.dev/linter/javascript/rules`, and the CSS and JSON equivalents) for the behaviour. Many rules a plugin would reimplement already exist — `noExplicitAny`, `noImportantStyles`, `useConst`, `noRestrictedImports` — and a built-in rule carries tested edge cases, options, and fixes a plugin will not. Write a plugin only for a project convention no rule covers, or where the built-in rule cannot be configured to the convention. When a built-in rule covers it, stop and tell the user the rule name and how to enable it in `biome.json`; write the plugin only if they still want one.

## Fixture first

Write the fixture before the pattern: one file in the target language holding every **must-match** case and every **must-not-match** case, each must-match on its own line so a diagnostic's line number identifies it. Use `.tsx` when any case contains JSX. The must-not-match cases are the half that gets skipped and the half that matters — the near-misses a reviewer would accept (`== null` for a strict-equality rule, `new Date()` with no arguments for a date-parsing ban, a side-effect `import "x"` for an import ban).

Done when every variant of the convention the codebase contains, and every legitimate near-miss, has a line in the fixture.

While the fixture exists its must-match lines fail the project's own `biome lint`. Delete it once verification passes, unless the user wants it kept as a regression fixture — then exclude it through `files.includes`.

## Draft against the fixture

Iterate with `biome search`, which runs a bare pattern without touching config and reports located syntax errors. Run the project's installed Biome, not a globally installed one, because node names and GritQL support vary by version:

```shell
npx @biomejs/biome search '`console.$method($...)` where { $method <: `log` }' fixture.ts
```

Single-quote the query in POSIX shells and PowerShell; inside double quotes, backticks are command substitution in POSIX shells and escape characters in PowerShell. Read the listed lines, not the summary — the "Found N matches" count is per file, not per match.

Choose the pattern form by what the convention describes:

- **Code snippet** (`` `$obj.forEach($...)` ``) — the default, when the convention is a shape of code someone would type. Whitespace and quote style are ignored.
- **Syntax node** (`JsCatchClause(body = JsBlockStatement(statements = []))`) — when the convention is a keyword, modifier, or structural property a snippet cannot express (`TsAnyType()`, `CssDeclarationImportant()`), or when it must find a construct at any depth with `contains`. Find node and field names in the Syntax tab of the Biome playground (`https://biomejs.dev/playground/`) or the `.ungram` files under `xtask/codegen` in the Biome repository. Node names change between Biome versions; a plugin built on them needs rechecking after an upgrade.

The syntax every plugin draws on:

| Construct | Meaning |
| --- | --- |
| `$name` | Binds a node; a repeated name must match identical code (`` `$fn && $fn()` ``) |
| `$_` | Matches any node without binding |
| `$...` | Matches zero or more list elements; `$first, $...` requires at least one |
| `` `pattern` as $call `` | Binds the whole match, usually for `span` |
| `where { a, b }` | Every comma-separated condition must hold |
| `$x <: pattern` | Match operator; `$x <: not pattern` negates |
| `or { p1, p2 }` / `and { … }` | Alternatives / conjunction; a top-level `or` combines several rules in one file, each arm with its own `where` |
| `contains pattern` | Matches anywhere in the subtree |
| `r"regex"` | Matches the node's full source text |
| `$x => \`replacement\`` | Rewrite, offered as a fix |
| `engine biome(1.0)` + `language js(typescript, jsx)` | Header: Biome's syntax tree and target language; `language css` and `language json` select the other targets |

Biome implements only part of GritQL; check `https://github.com/biomejs/biome/issues/2582` before relying on a feature from `docs.grit.io`, and prove any pattern copied from there in `biome search` before trusting it.

## Register the diagnostic

```grit
`$collection.forEach($...)` as $call where {
    register_diagnostic(
        span = $call,
        message = "Use `for...of` instead of `.forEach()`: it supports `break`, `continue`, and `await`.",
        severity = "warn"
    )
}
```

- **`span`** — the narrowest node that shows the reader what to change: the import source, not the whole import statement; the offending attribute, not the JSX element.
- **`message`** — names the convention and the fix. The diagnostic header reads only `plugin`, never the plugin's name, so the message is the reader's only clue to which rule fired and why.
- **`severity`** — `hint`, `info`, `warn`, or `error`; omitted means `error`, which fails CI. Write it explicitly: `warn` by default, `error` only when the user wants the convention to block CI.
- **`fix_kind`** — `safe` only when the rewrite cannot change behaviour in any matched case, since `biome lint --write` applies safe fixes unprompted. Omitted means `unsafe`, applied only with `--write --unsafe`. A rewrite that is wrong for one fixture line is not safe.

## Wire up and verify

Save the plugin in the directory the project's existing plugins use, else `./biome-plugins/`, as `<ruleName>.grit` in camelCase — the file stem becomes the suppression name, `// biome-ignore lint/plugin/<ruleName>: <reason>` — and register it:

```json
{
    "plugins": [
        "./biome-plugins/noForEach.grit",
        { "path": "./biome-plugins/noInlineStyle.grit", "includes": ["**/src/components/**"] }
    ]
}
```

Then run only plugin diagnostics against the fixture:

```shell
npx @biomejs/biome lint --only=plugin fixture.ts
```

Done when every must-match line reports exactly once, no must-not-match line reports, a file outside the `includes` scope reports nothing when `includes` is set, and — if the plugin rewrites — `--write` (plus `--unsafe` for an unsafe fix) on a copy of the fixture produces the intended code on every line. Then run `biome lint --only=plugin` over the real codebase and classify every hit. A true violation is the plugin working: report it to the user and leave the code alone unless asked to fix it. A false positive becomes a must-not-match fixture line, and a variant the fixture lacked becomes a must-match line, before the pattern changes.

## Gotchas

- **A single metavariable in an argument list matches any arity.** `` `console.log($msg)` `` matches `console.log()` and `console.log(a, b)` as well as `console.log(a)`, and a rewrite to `` `console.info($msg)` `` carries all of them across. Use `$first, $...` to require an argument, and keep zero- and multi-argument calls in the fixture.
- **A pattern with no `register_diagnostic()` loads cleanly and reports nothing.** The pattern matches; nothing is told about it. Silence from a new plugin means "check the diagnostic call", not "no violations".
- **`biome lint` hides compile errors.** A broken plugin prints only `Failed to compile the Grit plugin`, with no location, and the run exits 1. Paste the pattern into `biome search` for a located syntax error. Misspelled `register_diagnostic` arguments surface there only as `Error executing the Grit query` — check argument names against `span`, `message`, `severity`, `fix_kind`.
- **A broken registered plugin breaks `biome search` too.** Search loads the configured plugins, so while a plugin is failing, remove it from `biome.json` before debugging the pattern in search.
- **Regexes are anchored to the whole node text, quotes included.** `$source <: r"lodash"` never matches the source `"lodash"`; write `r"\"lodash\""` for an exact match or `r".*lodash.*"` for a substring.
- **Snippet imports miss side-effect imports.** `` `import $_ from $source` `` matches default, named, and namespace imports but not `import "lodash"`; add a `` `import $source` `` arm and a `require($source)` arm if those forms count.
- **Non-JS node names need the `language` header.** `CssDeclarationWithSemicolon()` in a file without `language css` fails to compile; the default target is JavaScript.
- **JSON snippets with metavariables are unsupported.** Match JSON through nodes such as `JsonMemberName()` and `JsonMember(name = …)`.
- **`includes` globs may match against the absolute path.** Biome issue `https://github.com/biomejs/biome/issues/11082` reports `plugins[].includes` resolving differently from `files.includes`, so `src/**` can match nothing. A plugin that goes silent once `includes` is added is this bug until proven otherwise: lint a file inside the scope, and if it reports nothing, prefix the glob with `**/`.
- **`--only` selects plugins as a group.** `--only=plugin` runs every plugin and nothing else; `--only=<ruleName>` silently runs nothing. To isolate one plugin, register only that one while verifying.
- **A suppression with a wrong plugin name warns rather than suppressing.** Biome reports `suppressions/unused` on the comment and the diagnostic still fires — confirm the name is the file stem.
