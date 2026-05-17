# Single Abstraction Level

Each function or module should operate at one conceptual level. Business intent and implementation mechanics must not share a function body — the reader must constantly shift mental gears when they do.

```
// prefer — each function stays at its own level
function processOrder(order):
  validateOrder(order)
  chargePayment(order)
  fulfilOrder(order)

// avoid — business intent mixed with raw mechanics
function processOrder(order):
  if order.items.length == 0: raise Error("order is empty")
  db.execute("INSERT INTO charges VALUES (?)", order.total)
  smtp.send(order.customer.email, "Your order is confirmed")
```

When a function reads as a mix of high-level policy and low-level detail, extract the details into named helpers. The top-level function should read like an outline.
