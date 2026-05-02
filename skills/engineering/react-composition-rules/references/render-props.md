## Rule: Render Props / Children as Functions for Rendering Flexibility

Use render props (children as a function, or a named render prop) when a component manages state or behaviour but must support multiple, consumer-defined UI shapes. Use a custom hook when the consumer only needs the data — not rendering flexibility.

**Do:**
- Type the children function signature explicitly in TypeScript
- Use a named render prop (`renderEmpty`, `renderItem`) when multiple render slots are needed
- Keep the component focused on providing data/state — not opinionated about layout

**Don't:**
- Use render props where a hook would suffice (unnecessarily adds JSX nesting)
- Accept both `children` as JSX and `children` as a function — pick one
- Deeply nest render prop components (prefer hooks + composition at that point)

**Example:**
```tsx
// use render props when rendering flexibility is the goal
function DataTable<T>({
  data,
  renderRow,
  renderEmpty,
}: {
  data: T[]
  renderRow: (item: T, index: number) => ReactNode
  renderEmpty: () => ReactNode
}) {
  if (data.length === 0) return <>{renderEmpty()}</>
  return <table><tbody>{data.map(renderRow)}</tbody></table>
}

// use a hook when the consumer only needs the values
const { data, loading } = useTableData(query)
```
