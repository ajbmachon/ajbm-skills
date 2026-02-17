# Anti-Pattern Catalog — Full Reference

15 anti-patterns with detailed signals, corrections, and code examples. Patterns 13-15 are AI-specific.

## Table of Contents

- [1. Mock Behavior Testing](#1-mock-behavior-testing)
- [2. Over-Mocking Dependency Chains](#2-over-mocking-dependency-chains)
- [3. Unrealistic Fixtures](#3-unrealistic-fixtures)
- [4. Test-Only Production Methods](#4-test-only-production-methods)
- [5. Implementation-Detail Assertions](#5-implementation-detail-assertions)
- [6. Snapshot Overreach](#6-snapshot-overreach)
- [7. Flaky Async/Time Tests](#7-flaky-asynctime-tests)
- [8. Silent Failures](#8-silent-failures)
- [9. Skip Debt](#9-skip-debt)
- [10. Coverage Theater](#10-coverage-theater)
- [11. Missing Regression Tests](#11-missing-regression-tests)
- [12. Missing Boundary Contract Tests](#12-missing-boundary-contract-tests)
- [13. Assertion Roulette (AI-Specific)](#13-assertion-roulette-ai-specific)
- [14. Circular Oracle (AI-Specific)](#14-circular-oracle-ai-specific)
- [15. Conditional Test Logic (AI-Specific)](#15-conditional-test-logic-ai-specific)

---

## 1. Mock Behavior Testing

**What it looks like:** Tests assert on mock artifacts rather than real system behavior.

**Signals:**
- Assertions on `*-mock` objects or `.called()` / `.calledWith()` exclusively
- No assertions on actual return values, state changes, or side effects
- Test passes even when real behavior is broken

**Good:**
```python
def test_send_welcome_email(smtp_server):
    service = UserService(smtp=smtp_server)
    service.register("alice@example.com")

    messages = smtp_server.get_sent_messages()
    assert len(messages) == 1
    assert messages[0].to == "alice@example.com"
    assert "Welcome" in messages[0].subject
```

**Bad:**
```python
def test_send_welcome_email(mock_smtp):
    service = UserService(smtp=mock_smtp)
    service.register("alice@example.com")

    mock_smtp.send.assert_called_once()  # Proves send was called, not that email was correct
```

---

## 2. Over-Mocking Dependency Chains

**What it looks like:** Multiple stacked mocks for testing one behavior. Setup dwarfs the actual assertion.

**Signals:**
- More than 2 mocks in a single test
- Mock setup takes 10+ lines while assertion is 1-2 lines
- Mocking internal collaborators, not just external boundaries

**Correction:** Mock only at external or nondeterministic boundaries. Keep domain logic real. If the test setup is longer than the assertion, reconsider whether you need those mocks.

---

## 3. Unrealistic Fixtures

**What it looks like:** Partial objects missing required fields, or state combinations that can't occur in production.

**Signals:**
- Objects with only 2-3 fields populated when the real object has 10+
- `null` or `undefined` for fields that are always present in production
- Test-only factory methods that skip validation

**Correction:** Use contract-complete fixtures that resemble real data. Include success and failure variants. Use factory functions (e.g., `createUser()`) that always produce valid objects with overridable fields.

---

## 4. Test-Only Production Methods

**What it looks like:** Production code contains methods that exist only for test convenience.

**Signals:**
- `resetForTests()`, `destroyForTest()`, `_testOnly_getState()`
- `@VisibleForTesting` annotations on private methods
- Public setters that only tests call

**Correction:** Move lifecycle helpers to test harnesses. If you need to observe internal state, test through the public API. If the public API doesn't expose what you need to test, that's a design signal — the API might need enriching for real consumers too.

---

## 5. Implementation-Detail Assertions

**What it looks like:** Tests assert on HOW the system works internally rather than WHAT it produces.

**Signals:**
- Assertions on private method calls or internal field values
- Checking that specific internal methods were called in a specific order
- Tests that break when you refactor internals without changing behavior

**Good:**
```javascript
test("applies 20% discount to premium members", () => {
  const order = createOrder({ member: "premium", subtotal: 100 });
  expect(order.total).toBe(80);
});
```

**Bad:**
```javascript
test("applies 20% discount to premium members", () => {
  const order = createOrder({ member: "premium", subtotal: 100 });
  expect(order._discountStrategy).toBe("percentage");
  expect(order._discountCalculator.calculate).toHaveBeenCalledWith(100, 0.2);
});
```

---

## 6. Snapshot Overreach

**What it looks like:** Huge serialized snapshots used as the primary correctness signal.

**Signals:**
- Snapshots over 50 lines
- Developers running `--updateSnapshot` without reviewing changes
- Snapshot contains volatile data (timestamps, IDs, random values)

**Correction:** Assert critical fields explicitly. Use snapshots only for stable, intentionally reviewed structures (e.g., small API response shapes). Keep snapshots under 20 lines.

---

## 7. Flaky Async/Time Tests

**What it looks like:** Tests that pass or fail nondeterministically.

**Signals:**
- `sleep(2000)` or `setTimeout` waits in tests
- Tests that pass locally but fail in CI (or vice versa)
- Timezone or locale assumptions

**Correction:**
- Control time: `jest.useFakeTimers()`, `freezegun`, `clock.tick()`
- Wait on deterministic conditions: `waitFor(() => expect(...))`, polling with timeout
- Isolate nondeterministic dependencies behind interfaces

---

## 8. Silent Failures

**What it looks like:** Tests that cannot fail, or swallow errors without checking them.

**Signals:**
- `expect(true).toBe(true)` — always passes regardless of behavior
- `try { ... } catch (e) { /* empty */ }` — swallows all errors
- Assertions inside callbacks that never execute (Promise chains without await)
- `toBeDefined()` or `toBeTruthy()` when a specific value is expected

**Correction:** Fail loudly. Assert specific values, error codes, and error messages. Use `rejects.toThrow()` for async errors. Verify callbacks execute with `expect.assertions(N)`.

---

## 9. Skip Debt

**What it looks like:** Skipped tests without clear ownership or re-enable criteria.

**Signals:**
- `test.skip()` or `@pytest.mark.skip` without explanation
- "Temporarily disabled" comments from months ago
- Growing skip count that nobody tracks

**Correction:** Skip only with an explicit reason AND a tracking ticket. Define re-enable criteria. Review skip debt monthly.

---

## 10. Coverage Theater

**What it looks like:** High line coverage but low confidence in correctness.

**Signals:**
- 90%+ line coverage but bugs still ship
- Tests that execute code paths without meaningful assertions
- Coverage-driven development (writing tests to hit lines, not prove behavior)

**Correction:** Prioritize branch coverage, invariant checking, and negative cases. Measure mutation testing score instead of line coverage when possible. One test with a strong assertion beats five tests with weak ones.

---

## 11. Missing Regression Tests

**What it looks like:** Bugs get fixed without a test that would have caught them.

**Signals:**
- Bug fix PRs with no new tests
- Same bug recurring after a refactor
- Fix changes behavior but no test validates the change

**Correction:** Every bug fix includes a regression test that fails before the fix and passes after. The test name should reference the bug (e.g., `test_issue_1234_duplicate_charges_prevented`).

---

## 12. Missing Boundary Contract Tests

**What it looks like:** Only unit tests with mocks around API, database, or schema boundaries.

**Signals:**
- Mock-heavy tests around every external call
- No tests that actually hit the database, API, or filesystem
- Behavior works in tests but breaks in staging

**Correction:** Add integration or contract tests for every external boundary. Use test containers, in-memory databases, or recorded HTTP fixtures to test real interactions.

---

## 13. Assertion Roulette (AI-Specific)

**What it looks like:** Multiple unrelated assertions crammed into one test with no distinguishing failure messages.

**Signals:**
- 5+ assertions in a single test covering different behaviors
- When one assertion fails, you cannot tell which behavior broke without reading the test
- Test named generically: `test_user_service`, `test_api_endpoint`

**Why AI does this:** AI agents try to be thorough by testing everything at once, producing a single "comprehensive" test instead of focused tests.

**Good:**
```python
def test_new_user_has_member_role():
    user = create_user("alice@example.com")
    assert user.role == "member"

def test_new_user_email_is_lowercase():
    user = create_user("Alice@Example.COM")
    assert user.email == "alice@example.com"
```

**Bad:**
```python
def test_create_user():
    user = create_user("Alice@Example.COM")
    assert user is not None
    assert user.role == "member"
    assert user.email == "alice@example.com"
    assert user.created_at is not None
    assert user.id > 0
    assert user.is_active is True
    # 6 unrelated assertions. Which one failed?
```

---

## 14. Circular Oracle (AI-Specific)

**What it looks like:** Test encodes current behavior as expected behavior, validating bugs instead of catching them.

**Signals:**
- Test expected values derived by reading the implementation code
- Test passes on the first run without the developer knowing what the correct output should be
- Expected values are complex computed results that match current output exactly

**Why AI does this:** AI reads the function, mentally executes it, and uses the result as the expected value. If the function has a bug, the expected value encodes the bug.

**Good — Expected from requirements:**
```javascript
// Requirement: 20% discount on orders over $100
test("applies 20% discount on eligible orders", () => {
  const order = createOrder({ subtotal: 150 });
  expect(order.discountedTotal()).toBe(120); // 150 * 0.8 = 120, from spec
});
```

**Bad — Expected from reading code:**
```javascript
// AI read the code: `return subtotal * 0.85` (bug: should be 0.80)
test("applies discount on eligible orders", () => {
  const order = createOrder({ subtotal: 150 });
  expect(order.discountedTotal()).toBe(127.5); // Encodes the bug
});
```

**Prevention:** Follow the Oracle Guard protocol. State expected values from requirements before looking at implementation.

---

## 15. Conditional Test Logic (AI-Specific)

**What it looks like:** Tests contain if/else, loops, try/catch, or computed expected values.

**Signals:**
- `if` statements inside test bodies
- `for` loops generating test cases inline (as opposed to parameterized test frameworks)
- `try/catch` blocks that conditionally pass
- Expected values computed from the same logic as the implementation

**Why AI does this:** AI agents try to be "clever" by generating tests programmatically, mirroring implementation logic. This creates tests that can never catch bugs because they compute expected values the same way the code does.

**Good — Literal expected values:**
```python
def test_fibonacci_sequence():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55
```

**Bad — Computed expected values:**
```python
def test_fibonacci_sequence():
    for n in range(20):
        expected = compute_fibonacci(n)  # Same algorithm as production!
        assert fibonacci(n) == expected  # Tests nothing
```

**The rule:** Expected values in tests should be literals or simple constants, never computed from logic that mirrors the implementation.
