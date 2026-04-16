# The 15 Testing Principles — Deep Dive

Code examples, exceptions, and language-specific guidance for each principle.

## Table of Contents

- [Tier A — Strategy (Plan Mode)](#tier-a--strategy-plan-mode)
  - [P1: Mostly Integration](#p1-mostly-integration)
  - [P2: The Beyonce Rule](#p2-the-beyonce-rule)
  - [P3: Test Boundaries and Error Paths](#p3-test-boundaries-and-error-paths)
  - [P4: Hermetic Tests](#p4-hermetic-tests)
- [Tier B — Design (Write Mode)](#tier-b--design-write-mode)
  - [P5: Test Behavior, Not Implementation](#p5-test-behavior-not-implementation)
  - [P6: Real Over Mock](#p6-real-over-mock)
  - [P7: One Behavior Per Test](#p7-one-behavior-per-test)
  - [P8: Test State, Not Interactions](#p8-test-state-not-interactions)
  - [P9: DAMP Over DRY](#p9-damp-over-dry)
  - [P10: Straight-Line Tests](#p10-straight-line-tests)
  - [P11: Clear Failure Messages](#p11-clear-failure-messages)
- [Tier C — Verification (Review Mode)](#tier-c--verification-review-mode)
  - [P12: Deterministic Always](#p12-deterministic-always)
  - [P13: Tests Are Documentation](#p13-tests-are-documentation)
  - [P14: Investigate First-Run Passes](#p14-investigate-first-run-passes)
  - [P15: Survive Refactoring](#p15-survive-refactoring)

---

## Tier A — Strategy (Plan Mode)

### P1: Mostly Integration

Integration tests give the highest confidence-per-effort ratio. They test real contracts between components without the brittleness of mocking everything.

**Good — Integration test with real database:**
```python
def test_create_user_persists_to_database(db_session):
    service = UserService(db_session)
    user = service.create_user("alice@example.com", "Alice")

    found = db_session.query(User).filter_by(email="alice@example.com").one()
    assert found.name == "Alice"
```

**Weak — Unit test mocking the database:**
```python
def test_create_user_calls_db(mock_session):
    service = UserService(mock_session)
    service.create_user("alice@example.com", "Alice")

    mock_session.add.assert_called_once()  # Tests mock wiring, not behavior
```

**Exceptions:** Pure algorithmic code (sorting, parsing, math) deserves focused unit tests. The integration label is about the default when uncertain, not a universal mandate.

### P2: The Beyonce Rule

"If you liked it, shoulda put a test on it." (From Google's Software Engineering at Google)

Test everything you value: correctness, performance characteristics, security boundaries, error messages, accessibility behavior. If it would hurt to lose it, it needs a test.

**Commonly missed test targets:**
- Error messages (users depend on them)
- Performance thresholds (response time budgets)
- Security boundaries (auth checks, input validation)
- Logging output (operators depend on it)
- Configuration loading (defaults, env var handling)

### P3: Test Boundaries and Error Paths

Every non-trivial change needs three tests minimum:

| Test | What It Proves |
|------|----------------|
| Happy path | The feature works as intended |
| Failure path | The feature fails gracefully with clear errors |
| Edge/boundary case | The feature handles limits (empty, max, null, concurrent) |

**The boundary checklist:**
- Empty inputs (null, undefined, empty string, empty array)
- Maximum values (overflow, very large strings, many items)
- Off-by-one (first item, last item, boundary of a range)
- Concurrent access (if applicable)
- Malformed input (wrong type, missing fields, extra fields)

### P4: Hermetic Tests

Each test is a self-contained universe. It creates everything it needs and cleans up after itself.

**Good — Self-contained:**
```javascript
test("calculates total for cart with items", () => {
  const cart = createCart([
    { name: "Widget", price: 10.00, quantity: 2 },
    { name: "Gadget", price: 25.50, quantity: 1 },
  ]);

  expect(cart.total()).toBe(45.50);
});
```

**Bad — Depends on shared state:**
```javascript
// Some other test created globalCart with unknown items
test("calculates total", () => {
  expect(globalCart.total()).toBe(45.50);  // Fragile: depends on test order
});
```

**Rules:**
- No shared mutable state between tests
- No dependency on test execution order
- No dependency on external services (use fakes or containers)
- Each test can run independently in any order

---

## Tier B — Design (Write Mode)

### P5: Test Behavior, Not Implementation

Assert on what the system DOES (observable outcomes), not how it does it internally.

**Good — Tests behavior:**
```python
def test_discount_applied_to_order():
    order = Order(items=[Item(price=100)])
    order.apply_discount("SAVE20")

    assert order.total == 80.00
```

**Bad — Tests implementation:**
```python
def test_discount_applied_to_order():
    order = Order(items=[Item(price=100)])
    order.apply_discount("SAVE20")

    # Testing internal implementation, not behavior
    assert order._discount_percentage == 0.20
    assert order._discount_applied is True
    assert order._recalculate_called is True
```

**The litmus test:** If you refactored the internals without changing any behavior, would this test break? If yes, it tests implementation.

**Observable outcomes to assert on:**
- Return values
- Persisted state (database, files)
- Emitted events or messages
- API/protocol output
- Side effects visible to callers
- Error messages and status codes

### P6: Real Over Mock

The mocking hierarchy — always prefer left:

```
Real → Fake → Spy → Stub → Mock
```

| Level | What It Is | When To Use |
|-------|-----------|-------------|
| Real | Actual dependency | Default choice. Always start here. |
| Fake | In-memory implementation (e.g., SQLite for Postgres) | Real dependency is too slow or non-hermetic |
| Spy | Real dependency + recording | Need to verify interactions happened AND test real behavior |
| Stub | Canned responses | External API with predictable responses |
| Mock | Behavior verification object | Last resort: truly external, nondeterministic boundaries |

**Language-specific:**
- **Python:** `pytest` fixtures with real dependencies; `unittest.mock.patch` only at boundaries
- **JavaScript:** Real modules; `jest.mock()` only for network/filesystem
- **Go:** Interface-based fakes; `gomock` only for external services
- **Rust:** Trait-based fakes; mockall for external FFI boundaries

### P7: One Behavior Per Test

Each test describes one scenario. The test name reads as a sentence.

**Good:**
```javascript
test("returns empty array when search finds no results", () => { ... });
test("returns matching items sorted by relevance when search finds results", () => { ... });
test("throws InvalidQueryError when search query is empty", () => { ... });
```

**Bad:**
```javascript
test("search works", () => {
  // Tests empty query, no results, AND sorting in one test
  // Which assertion failed? Who knows.
});
```

### P8: Test State, Not Interactions

Verify WHAT the result is, not HOW the system got there.

**Good — Tests state:**
```python
def test_user_promoted_to_admin():
    user = User(role="member")
    user.promote()

    assert user.role == "admin"
    assert user.can_access_admin_panel() is True
```

**Bad — Tests interactions:**
```python
def test_user_promoted_to_admin(mock_role_service):
    user = User(role="member", role_service=mock_role_service)
    user.promote()

    mock_role_service.update_role.assert_called_once_with(user.id, "admin")
    # Proves the method was called, not that the user is actually an admin
```

### P9: DAMP Over DRY

In tests, readability beats reuse. Duplicate freely if it makes each test self-contained.

**Good — DAMP (Descriptive And Meaningful Phrases):**
```javascript
test("free shipping for orders over $100", () => {
  const order = createOrder({ items: [{ price: 120 }] });
  expect(order.shippingCost()).toBe(0);
});

test("standard shipping for orders under $100", () => {
  const order = createOrder({ items: [{ price: 50 }] });
  expect(order.shippingCost()).toBe(9.99);
});
```

**Bad — Over-abstracted DRY:**
```javascript
const testCases = [
  { price: 120, expected: 0 },
  { price: 50, expected: 9.99 },
];
testCases.forEach(({ price, expected }) => {
  test(`shipping for ${price}`, () => {
    expect(createOrder({ items: [{ price }] }).shippingCost()).toBe(expected);
  });
});
// What behavior is being tested? Have to mentally trace the loop.
```

**Helper functions are fine** when they reduce noise without hiding intent. Good helpers: `createUser()`, `seedDatabase()`. Bad helpers: `assertEverything()`, `runAllChecks()`.

### P10: Straight-Line Tests

Tests should have exactly one path through them. No branching, no loops, no exception handling.

**Good:**
```python
def test_parse_valid_date():
    result = parse_date("2026-01-15")
    assert result.year == 2026
    assert result.month == 1
    assert result.day == 15
```

**Bad:**
```python
def test_parse_dates():
    dates = ["2026-01-15", "invalid", "2026-13-01"]
    for date_str in dates:
        try:
            result = parse_date(date_str)
            assert result is not None  # Which date passed? Which failed?
        except ValueError:
            pass  # Silently swallowing failures
```

### P11: Clear Failure Messages

When a test fails, the failure message alone — without reading the test code — should tell you what went wrong.

**Good:**
```javascript
expect(user.role).toBe("admin");
// Failure: Expected "admin", received "member"
// Immediately clear: user was not promoted
```

**Better — Custom message:**
```javascript
expect(response.status).toBe(200,
  `Expected success response for authenticated user, got ${response.status}: ${response.body}`
);
```

**Bad:**
```javascript
expect(result).toBeTruthy();
// Failure: Expected truthy, received false
// What is "result"? What was expected? No idea.
```

---

## Tier C — Verification (Review Mode)

### P12: Deterministic Always

Same code + same test = same result. Every time. On every machine.

**Sources of nondeterminism and fixes:**

| Source | Fix |
|--------|-----|
| Current time | Inject clock, freeze time (`jest.useFakeTimers()`, `freezegun`) |
| Random values | Seed the generator or inject values |
| Network calls | Use fakes, containers, or recorded responses |
| File system | Use temp directories, clean up in afterEach |
| Database state | Transaction rollback or fresh schema per test |
| Test order | Run tests in random order to catch dependencies |
| Floating point | Use approximate matchers (`toBeCloseTo`) |

### P13: Tests Are Documentation

A well-written test suite is the best documentation of expected behavior. Write tests a stranger would want to read at 3 AM while debugging production.

**Qualities of documentary tests:**
- Test names describe behavior in plain language
- Setup code reveals important preconditions
- Assertions are explicit about expected values
- Edge cases document boundary behavior
- Error tests document failure modes

### P14: Investigate First-Run Passes

**This is the most critical principle for AI agents.** When an LLM generates tests by reading implementation code, the tests can pass on buggy code and fail on correct code — a failure mode known as circular validation.

**The circular oracle problem:** AI reads the current code → infers "expected" behavior from it → writes a test that matches the current output → test passes → but the current output is wrong. See [Tsiokos — "Circular Validation: The Hidden Risk in AI-Generated Tests"](https://george.tsiokos.com/posts/2025/02/circular-validation-ai-testing/) for a worked example.

**The fix:** State expected behavior from requirements BEFORE looking at implementation. Then follow the Oracle Guard protocol (inlined in anti-patterns.md #14).

### P15: Survive Refactoring

The ultimate test of test quality: refactor the implementation without changing behavior. All tests should still pass.

**Tests that survive refactoring assert on:**
- Public API return values
- Database state after operations
- HTTP response bodies and status codes
- Events emitted to message queues
- Files written to disk

**Tests that break during refactoring assert on:**
- Internal method call sequences
- Private field values
- Number of times a function was called
- Specific SQL queries used
- Internal data structure shapes
