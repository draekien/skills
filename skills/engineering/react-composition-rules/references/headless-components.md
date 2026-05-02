## Rule: Headless Components — Separate Logic from Presentation

Interactive components with complex behaviour (combobox, date picker, drag-and-drop, multi-select) must separate behaviour into hook or headless layer. Visual layer owned entirely by consumer. Never couple behaviour to style or markup.

**Do:**

- Return prop-getters (`getInputProps`, `getItemProps`) from headless hook so consumers spread onto any element
- Include ARIA attrs and keyboard handlers in prop-getters, not consumer
- Allow hook with any markup structure

**Don't:**

- Render HTML elements inside headless hook/component
- Assume class name, tag, or layout in behaviour layer
- Export single component bundling behaviour + fixed style

**Example:**

```tsx
// good — headless hook, consumer owns all markup
function useCombobox({ items, onSelect }) {
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const filtered = items.filter((i) => i.includes(query));
  return {
    isOpen: open,
    filteredItems: filtered,
    getInputProps: () => ({
      value: query,
      onChange: (e) => {
        setQuery(e.target.value);
        setOpen(true);
      },
      role: "combobox",
      "aria-expanded": open,
    }),
    getItemProps: (item) => ({
      onClick: () => {
        onSelect(item);
        setOpen(false);
      },
    }),
  };
}
```
