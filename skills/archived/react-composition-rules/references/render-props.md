## Rule: Render Props / Children as Functions for Rendering Flexibility

Use render props (children as function, or named render prop) when component manages state/behaviour but must support multiple consumer-defined UI shapes. Use custom hook when consumer only needs data — not rendering flexibility.

**Do:**

- Type children function signature explicitly in TypeScript
- Use named render prop (`renderEmpty`, `renderItem`) when multiple render slots needed
- Keep component focused on data/state — not opinionated about layout

**Don't:**

- Use render props where hook suffices (adds JSX nesting unnecessarily)
- Accept both `children` as JSX and `children` as function — pick one
- Deeply nest render prop components (prefer hooks + composition instead)

**Example:**

```tsx
// use render props when rendering flexibility is the goal
function DataTable<T>({
  data,
  renderRow,
  renderEmpty,
}: {
  data: T[];
  renderRow: (item: T, index: number) => ReactNode;
  renderEmpty: () => ReactNode;
}) {
  if (data.length === 0) return <>{renderEmpty()}</>;
  return (
    <table>
      <tbody>{data.map(renderRow)}</tbody>
    </table>
  );
}

// use a hook when the consumer only needs the values
const { data, loading } = useTableData(query);
```
