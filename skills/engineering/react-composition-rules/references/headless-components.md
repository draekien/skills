## Rule: Headless Components — Separate Logic from Presentation

Interactive components with complex behaviour (combobox, date picker, drag-and-drop, multi-select) must separate all behaviour into a hook or headless layer. The visual layer is provided entirely by the consumer. Never couple behaviour to a specific style or markup structure.

**Do:**
- Return prop-getters (`getInputProps`, `getItemProps`) from the headless hook so consumers spread them onto any element
- Include ARIA attributes and keyboard handlers in the prop-getters, not in the consumer
- Allow the hook to be used with any markup structure

**Don't:**
- Render any HTML elements inside the headless hook/component
- Assume a specific class name, tag, or layout in the behaviour layer
- Export a single component that bundles both behaviour and a fixed style

**Example:**
```tsx
// good — headless hook, consumer owns all markup
function useCombobox({ items, onSelect }) {
  const [query, setQuery] = useState('')
  const [open, setOpen] = useState(false)
  const filtered = items.filter(i => i.includes(query))
  return {
    isOpen: open,
    filteredItems: filtered,
    getInputProps: () => ({
      value: query,
      onChange: e => { setQuery(e.target.value); setOpen(true) },
      role: 'combobox',
      'aria-expanded': open,
    }),
    getItemProps: item => ({ onClick: () => { onSelect(item); setOpen(false) } }),
  }
}
```
