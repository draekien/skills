# Prefer Interfaces for Object Shapes

Use `interface` to define object shapes. Reserve `type` for unions, intersections, mapped types, conditional types, and aliases for primitives or tuples.

```typescript
// prefer interface for object shapes
interface User {
  id: string;
  name: string;
  email: string;
}

interface Repository<T> {
  findById(id: string): Promise<T | null>;
  save(entity: T): Promise<T>;
}

// type is appropriate for unions and aliases
type UserId = string;
type Status = 'pending' | 'active' | 'closed';
type UserOrAdmin = User | Admin;
```

Interfaces are open and can be augmented via declaration merging, which makes them the right choice for public contracts and extensible shapes. Types cannot be merged and are preferred when composition via intersection is needed.
