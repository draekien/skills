## Rule: Inversion of Control / State Reducer Pattern

No one-off behaviour props (`closeOnSelect`, `resetOnBlur`, `preventToggleWhenDisabled`). Expose `reducer` prop — lets consumers intercept and override state transitions. Always provide default reducer so common case needs no config.

**Do:**

- Export default reducer alongside hook so consumers call it as fallback
- Accept `reducer` prop defaulting to built-in reducer
- Use for genuinely complex interactive components — not simple ones

**Don't:**

- Keep adding boolean props for edge-case behaviours
- Force consumers to re-implement core logic for small variations
- Apply to simple components — complexity must be justified

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
