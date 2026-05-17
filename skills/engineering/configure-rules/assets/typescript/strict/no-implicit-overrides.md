# No Implicit Overrides

Always use the `override` keyword when overriding a method or property from a base class. This makes intent explicit and causes a compile error if the base class method is renamed or removed.

```typescript
class Base {
  render(): string {
    return '<base>';
  }
}

// prefer
class Derived extends Base {
  override render(): string {
    return '<derived>';
  }
}

// avoid — silent override, no compile-time safety
class Derived extends Base {
  render(): string {
    return '<derived>';
  }
}
```

When `noImplicitOverride` is enabled in `tsconfig.json`, TypeScript enforces this automatically. The rule here extends that discipline to code review and AI-generated code regardless of tsconfig state.
