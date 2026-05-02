## Rule: Proper forwardRef Usage

Any reusable component that wraps a native element must forward its ref. Use `useImperativeHandle` to expose a controlled imperative API instead of the raw DOM node when the component has complex behaviour.

**Do:**
- Wrap all components that render a single native element in `forwardRef`
- Name the inner function (not an arrow function) so React DevTools shows the component name
- Use `useImperativeHandle` to define a minimal, intentional imperative API for complex components

**Don't:**
- Drop or ignore the `ref` prop in a component that wraps a native element
- Expose raw DOM nodes from complex components — define an explicit API with `useImperativeHandle`
- Use refs as a workaround to avoid passing props

**Example:**
```tsx
// bad — ref is silently ignored
function Input({ className, ...props }) {
  return <input className={cn('input', className)} {...props} />
}

// good — ref forwarded correctly
const Input = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  function Input({ className, ...props }, ref) {
    return <input ref={ref} className={cn('input', className)} {...props} />
  }
)

// good — controlled API for complex components
const Dialog = forwardRef<{ open(): void; close(): void }, DialogProps>(
  function Dialog({ children }, ref) {
    const [open, setOpen] = useState(false)
    useImperativeHandle(ref, () => ({
      open: () => setOpen(true),
      close: () => setOpen(false),
    }), [])
    return open ? <div role="dialog">{children}</div> : null
  }
)
```
