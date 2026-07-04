## Rule: Proper forwardRef Usage

Reusable component wrapping native element must forward ref. Use `useImperativeHandle` for controlled imperative API instead of raw DOM node when component has complex behaviour.

**Do:**

- Wrap all components rendering single native element in `forwardRef`
- Name inner function (not arrow) so React DevTools shows component name
- Use `useImperativeHandle` for minimal, intentional imperative API on complex components

**Don't:**

- Drop/ignore `ref` prop in component wrapping native element
- Expose raw DOM nodes from complex components — define explicit API with `useImperativeHandle`
- Use refs to avoid passing props

**Example:**

```tsx
// bad — ref is silently ignored
function Input({ className, ...props }) {
  return <input className={cn("input", className)} {...props} />;
}

// good — ref forwarded correctly
const Input = forwardRef<
  HTMLInputElement,
  InputHTMLAttributes<HTMLInputElement>
>(function Input({ className, ...props }, ref) {
  return <input ref={ref} className={cn("input", className)} {...props} />;
});

// good — controlled API for complex components
const Dialog = forwardRef<{ open(): void; close(): void }, DialogProps>(
  function Dialog({ children }, ref) {
    const [open, setOpen] = useState(false);
    useImperativeHandle(
      ref,
      () => ({
        open: () => setOpen(true),
        close: () => setOpen(false),
      }),
      [],
    );
    return open ? <div role="dialog">{children}</div> : null;
  },
);
```
