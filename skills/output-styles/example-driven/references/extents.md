# Extents

The extent sets how much prose survives. Each one adds constraints to `example-driven.md`; the rules there still hold except where an extent overrides them.

`illustrated` is the default and needs no override — it is `example-driven.md` as written.

The ladder, by prose remaining:

| Extent | Prose allowed |
| --- | --- |
| `illustrated` | Full prose, carrying the argument |
| `captioned` | One line per example |
| `commented` | Comments inside blocks only, plus a one-line verdict |
| `notation` | None |

## captioned

The example is the whole answer. Prose collapses to a caption of one line or less per example, plus a one-line verdict at the top naming the cause or the recommendation.

Cut the trade-off and the why unless the answer is wrong without them. Where a caption would restate the example, drop it and let the example stand alone.

```jsx
// ✗ identity changes every render
function Form() {
  const Field = (p) => <input {...p} />;
  return <Field value={v} onChange={setV} />;
}

// ✓ identity stable
const Field = (p) => <input {...p} />;

function Form() {
  return <Field value={v} onChange={setV} />;
}
```

## commented

No prose outside a block. All explanation moves into comments inside the example, where it sits against the exact line it explains. A one-line verdict above the first block is the only exception.

This extent forces reasoning to be concrete — an explanation that cannot survive as a comment on a specific line was too vague to keep. Split one example into two blocks rather than compressing a comment past the point of usefulness.

```jsx
function Form() {
  // Each render evaluates this arrow expression afresh.
  // React compares by reference, sees a different type,
  // unmounts the old tree and mounts a new one.
  // A remounted <input> is a new DOM node: focus,
  // selection and uncontrolled state all reset.
  const Field = (p) => <input {...p} />;

  return <Field value={v} onChange={setV} />;
}
```

Non-code subjects use commented configs, annotated directory trees, or a table whose cells carry the reasoning.

## notation

No sentences anywhere, including in comments. Everything becomes a diff, a table, a decision tree, a state transition, a derivation, or pseudocode. Comments reduce to labels and fragments.

```text
render(n):   Field_n   = (p) => <input {...p} />
render(n+1): Field_n+1 = (p) => <input {...p} />

Field_n !== Field_n+1        // reference inequality
  ⇒ type changed
  ⇒ unmount(Field_n) ; mount(Field_n+1)
  ⇒ new DOM node
  ⇒ focus = null
```

| scope | evaluated | identity | reconciler | focus |
| --- | --- | --- | --- | --- |
| render | per render | new | remount | lost |
| module | once | stable | update | kept |

Two limits, because this extent has the narrowest range:

- **A judgment call becomes a decision table, never pseudocode.** Options as rows, criteria as columns, the recommendation marked. Pseudocode over a question with no algorithm is theatre.
- **A subject that cannot be reduced to notation without losing the answer drops to `commented` for that response only.** Say which extent is in use when this happens, in as few words as the extent allows, and return to `notation` on the next response.
