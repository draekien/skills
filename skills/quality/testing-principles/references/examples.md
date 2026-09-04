# Worked Examples

One bad/good pair per pillar, in language-agnostic pseudocode. The bad case is the failure the pillar exists to prevent; the good case is what replaces it. Read the pillar in `SKILL.md` first — these illustrate it, they do not restate it.

## Falsifiability

The bad test runs the code and asserts something that holds no matter what the code does. Mutate `discount` to `return 0` and it stays green.

```
# BAD — cannot fail
test "applies discount":
    result = discount(price=100, percent=10)
    assert result != null          # true for 90, for 100, for -5, for anything
```

The good test pins the exact outcome, so the mutation turns it red. The comment shows the write-time falsifiability check: flip the literal, watch it fail, restore.

```
# GOOD — fails under a real defect
test "applies discount":
    result = discount(price=100, percent=10)
    assert result == 90            # flip to 91, confirm RED, restore to 90
```

## Independent derivation

The bad test was written against existing code: someone ran `tax(100)`, saw `7`, and pasted it. If the rate should be 10%, the function is wrong — and this test now guards the bug.

```
# BAD — expectation copied from the code's output
test "calculates tax":
    assert tax(100) == 7           # 7 is whatever the code returned, not what the spec requires
```

The good test derives the number from the requirement ("tax is 10%") before looking at the code. When it disagrees with the implementation, that disagreement is the bug report.

```
# GOOD — expectation derived from the spec
# Spec: tax is 10% of the amount.
test "calculates tax":
    assert tax(100) == 10          # 10 comes from the spec; if code returns 7, code is wrong
```

## Edge-case enumeration

The bad suite covers only the happy path. Line coverage looks high; the boundaries and error paths that actually break in production are never exercised.

```
# BAD — happy path only
test "parses a positive quantity":
    assert parse_quantity("5") == 5
```

The good suite enumerates the input classes first — empty, zero, boundary, invalid — and writes a case for each.

```
# GOOD — input classes enumerated, one case each
test "parses a positive quantity":     assert parse_quantity("5") == 5
test "rejects empty input":            assert raises(parse_quantity, "")
test "accepts zero":                   assert parse_quantity("0") == 0
test "rejects negatives":              assert raises(parse_quantity, "-1")
test "rejects non-numeric input":      assert raises(parse_quantity, "abc")
test "accepts the documented maximum": assert parse_quantity("9999") == 9999
```

## Behaviour over implementation

The bad test scripts a mock to return `49.99`, then asserts the code returns `49.99`. It verifies the mock, not `checkout` — replace `checkout`'s body with `return priceClient.fetch(...)` and it still passes while the real total logic is gone.

```
# BAD — asserts the mock's scripted output (the mock mirror)
test "checkout returns the total":
    priceClient = mock()
    priceClient.fetch returns 49.99
    result = checkout(cart, priceClient)
    assert result == 49.99         # 49.99 was dictated by the mock, not computed by checkout
```

The good test mocks only the genuine boundary (the price source) and asserts the observable behaviour `checkout` is responsible for — summing line items and applying tax.

```
# GOOD — mock the boundary, assert the behaviour under test
test "checkout sums items and applies tax":
    priceClient = mock()
    priceClient.fetch("apple") returns 30.00
    priceClient.fetch("pear")  returns 20.00
    result = checkout(cart=["apple", "pear"], priceClient, tax_rate=0.10)
    assert result == 55.00         # 50.00 of items + 10% tax — checkout's own logic
```

## One reason to fail

The bad test asserts several unrelated things with bare literals. A failure reports a line number, not a behaviour; the `now()` call makes it flake; `19` is a magic number whose origin is lost.

```
# BAD — assertion roulette, magic number, non-deterministic
test "user":
    u = create_user("Ada", birth_year=2007)
    assert u.name == "Ada"
    assert u.age == 19             # only correct in one calendar year — depends on now()
    assert u.is_adult == true
    assert u.id != null
```

The good version splits behaviours into named tests, injects the clock instead of reading it, and derives each expected value transparently.

```
# GOOD — one behaviour each, deterministic, derived
test "stores the provided name":
    assert create_user("Ada").name == "Ada"

test "computes age from birth year against a fixed clock":
    u = create_user("Ada", birth_year=2007, clock=fixed(2025))
    assert u.age == 2025 - 2007    # derivation shown, not a bare 18

test "treats an 18-year-old as an adult":
    u = create_user("Ada", birth_year=2007, clock=fixed(2025))
    assert u.is_adult == true
```
