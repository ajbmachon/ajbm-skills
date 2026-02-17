# The Testing Trophy — Full Reference

Test strategy, level selection, and advanced testing approaches.

---

## The Testing Trophy (Kent C. Dodds)

Traditional "testing pyramid" (Fowler/Google) says: many unit tests, fewer integration, fewest E2E.

The testing trophy inverts the emphasis: **integration tests give the highest confidence-per-effort.**

```
              ┌─────────┐
              │   E2E   │  Expensive, slow, high confidence
            ┌─┴─────────┴─┐
            │ Integration  │  ← SWEET SPOT: best ROI
          ┌─┴──────────────┴─┐
          │      Unit        │  Fast, cheap, narrow scope
        ┌─┴──────────────────┴─┐
        │   Static Analysis    │  Free: types, linting, formatting
        └──────────────────────┘
```

**Why integration tests win:**
- They test real interactions between components
- They catch bugs that unit tests with mocks miss entirely
- They require fewer mocks, making them more trustworthy
- They survive refactoring better than tightly-coupled unit tests

**The consensus across all sources:** Minimize mocking. Whether you call it "pyramid" or "trophy," the practical advice converges: test real behavior at the highest level that remains fast and deterministic.

## Level Selection Decision Tree

```
Is it pure logic (math, parsing, sorting)?
  → YES: Unit test
  → NO: ↓

Does it cross a boundary (DB, API, filesystem, message queue)?
  → YES: Integration test with real or fake dependency
  → NO: ↓

Is it a critical multi-step user journey?
  → YES: E2E test
  → NO: Integration test (default)
```

**When to override the default:**

| Override To | When |
|-------------|------|
| Unit | Complex algorithm with many edge cases (combinatorial testing) |
| Unit | Pure utility function used everywhere (high leverage) |
| Integration | Uncertain about test level (always the safe default) |
| E2E | User-facing workflow that crosses multiple services |
| Contract | Service-to-service boundaries with independent deployment |

## Property-Based Testing

**The research:** Each property-based test finds approximately 50x as many mutations as the average unit test (OOPSLA 2025).

Property-based testing generates random inputs and checks that properties (invariants) hold across all of them. It finds edge cases humans would never write manually.

**When to use:**
- Serialization/deserialization roundtrips (`decode(encode(x)) == x`)
- Mathematical properties (commutativity, associativity, idempotency)
- Data structure invariants (sorted output, unique elements, size bounds)
- API contracts (valid input always produces valid output, invalid input always produces error)

**Example — Python with Hypothesis:**
```python
from hypothesis import given
from hypothesis.strategies import text

@given(text())
def test_encode_decode_roundtrip(s):
    assert decode(encode(s)) == s
```

**Example — JavaScript with fast-check:**
```javascript
import fc from "fast-check";

test("sort is idempotent", () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      const sorted = mySort(arr);
      expect(mySort(sorted)).toEqual(sorted);
    })
  );
});
```

**Most effective property patterns (from research):**
1. Exception checks (function doesn't crash on any input) — 19x more effective
2. Collection inclusion (output contains expected elements)
3. Type checks (output has correct shape/type)
4. Roundtrip (encode/decode, serialize/deserialize)
5. Idempotency (applying operation twice = applying once)

## Contract Testing

For service-to-service boundaries where services deploy independently.

**The problem:** Service A mocks Service B's API in tests. Service B changes its API. Service A's tests still pass (they test mocks). Production breaks.

**The solution:** Contract tests verify that both sides agree on the API shape.

**Tools:**
- **Pact** — Consumer-driven contracts (JS, Python, Go, Java, Rust)
- **Protovalidate** — Schema validation for protobuf
- **OpenAPI validation** — Schema-first API contracts

**When to use contracts:**
- Microservice-to-microservice communication
- Frontend-to-backend API boundaries
- Any boundary where teams deploy independently

## When E2E Tests Are Worth the Cost

E2E tests are expensive (slow, flaky, hard to maintain). Use them only for:

1. **Critical user journeys** — Login, checkout, onboarding, payment
2. **Multi-service workflows** — Operations that cross 3+ services
3. **Smoke tests** — "The system boots and can serve a basic request"
4. **Regulatory requirements** — Some industries require end-to-end verification

**E2E test rules:**
- Keep the suite small (10-20 tests for most applications)
- Test the happy path; leave edge cases to lower levels
- Use stable selectors (data-testid, accessibility roles)
- Accept some flakiness budget (retry once, then investigate)
- Run on every deploy, not every commit

## Static Analysis (The Foundation)

The base of the trophy. Free confidence that catches errors before tests run.

**Essentials:**
- **Type checking** — TypeScript strict mode, mypy, Go compiler
- **Linting** — ESLint, Ruff, clippy
- **Formatting** — Prettier, Black, gofmt
- **Security scanning** — Dependabot, Snyk, npm audit

Static analysis is the highest-ROI testing investment. It catches entire categories of bugs (typos, type mismatches, unused imports, unreachable code) with zero runtime cost.
