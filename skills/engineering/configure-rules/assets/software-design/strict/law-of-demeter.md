# Law of Demeter

Only communicate with immediate neighbours. A module should call methods on objects it owns, objects passed to it, or objects it created — not objects retrieved by navigating through another object's internals.

```
// prefer — ask the neighbour to do the work
total = order.calculateTotal()

// avoid — reach through order → customer → address → country to access taxRate
taxRate = order.customer.address.country.taxRate
```

Each dot in a chain that crosses an ownership boundary is a hidden dependency on an intermediate's internal structure. When that structure changes, every chain that reaches through it breaks. Expose behaviour, not data paths.
