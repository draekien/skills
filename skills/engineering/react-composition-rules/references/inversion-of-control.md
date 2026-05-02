## Rule: Inversion of Control / State Reducer Pattern

Do not add one-off behaviour props (`closeOnSelect`, `resetOnBlur`, `preventToggleWhenDisabled`) to accommodate specific use cases. Instead, expose a `reducer` prop that lets consumers intercept and override state transitions. Always provide a default reducer so the common case requires no configuration.

**Do:**
- Export the default reducer alongside the hook so consumers can call it as a fallback
- Accept a `reducer` prop that defaults to the built-in reducer
- Use this pattern for genuinely complex interactive components — not simple ones

**Don't:**
- Keep adding boolean props to handle edge-case behaviours
- Require consumers to re-implement core logic when they need a small variation
- Apply this pattern to simple components — it adds complexity that must be justified

**Example:**
```tsx
// bad — prop explosion
function useDropdown({ closeOnSelect = true, keepOpenOnOutsideClick = false, ... }) { }

// good — state reducer
export function defaultDropdownReducer(state, action) {
  switch (action.type) {
    case 'select': return { ...state, open: false, selected: action.item }
    default: return state
  }
}

function useDropdown({ reducer = defaultDropdownReducer } = {}) {
  const [state, dispatch] = useReducer(reducer, { open: false, selected: null })
  return { ...state, dispatch }
}

// consumer keeps dropdown open after selection
useDropdown({
  reducer(state, action) {
    if (action.type === 'select') return { ...state, selected: action.item } // no close
    return defaultDropdownReducer(state, action)
  }
})
```
