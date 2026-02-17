---
name: testing-best-practices
description: Use when writing, reviewing, or reporting tests. Enforces trustworthy testing through the Testing Trophy strategy, 15 evidence-based principles, disciplined mocking, AI oracle prevention, anti-pattern detection, and honest execution reporting. Applies to unit, integration, and e2e test work.
---

# Testing Best Practices

## Purpose

Use this skill to produce test evidence that is trustworthy, reproducible, and useful for decisions.

Apply it whenever you:
- add or modify behavior
- write or revise tests
- review test quality
- report test status to a human partner

**Scope boundary:** This skill covers test *quality* — what makes a good test, how to choose test levels, and how to verify tests are trustworthy. For the test-*first* process (RED-GREEN-REFACTOR), use `test-driven-development`.

## Claude Execution Rules

- Execute testing work, do not just suggest it.
- State unknowns explicitly instead of implying confidence.
- Follow the output contract exactly when reporting.
- Prefer positive directives: what to do next, not just what to avoid.
- Run the Oracle Check after every test you write (see write workflow).

## Operating Modes

Pick one mode immediately, then run the matching workflow:
- `plan` — build risk map and test strategy (apply **Tier A** principles)
- `write` — implement or update tests for changed behavior (apply **Tier B** principles)
- `review` — audit existing tests for quality and trustworthiness (apply **Tier C** principles)
- `report` — summarize exactly what was executed and what remains

If user intent is mixed, run `plan` then continue with `write`.

## The Five Iron Laws

```text
1. ALWAYS investigate when a test passes on first run — verify it tests the right thing.
2. ALWAYS assert on real system behavior, not mock wiring.
3. ALWAYS keep tests as straight-line code — no conditionals, loops, or try/catch.
4. ALWAYS execute tests and report concrete evidence before claiming they pass.
5. ALWAYS keep production APIs clean — move test lifecycle helpers to test harnesses.
```

## The Testing Trophy

Confidence-per-effort, highest to lowest:

```
          ┌───────┐
          │  E2E  │  Few: critical user journeys only
        ┌─┴───────┴─┐
        │Integration │  Most: contracts, persistence, boundaries
      ┌─┴────────────┴─┐
      │     Unit       │  Many: pure logic and branching
    ┌─┴────────────────┴─┐
    │  Static Analysis   │  All: types, linting, formatting
    └────────────────────┘
```

**Decision heuristic:** Use the lowest test level that still proves the behavior.
- Pure logic, calculations, branching → **unit test**
- Contracts, persistence, API boundaries, DB semantics → **integration test**
- Critical multi-step user journeys → **e2e test**

Prefer integration tests when uncertain. They catch real bugs with fewer mocks.

For property-based testing, contract testing, and when E2E is worth the cost, see [references/testing-trophy.md](references/testing-trophy.md).

## The 15 Principles

Organized into three tiers that map to operating modes.

### Tier A — Strategy (plan mode: decide WHAT to test)

| # | Principle | Rule |
|---|-----------|------|
| 1 | Mostly Integration | Integration tests give highest confidence-per-effort. Default to them when uncertain. |
| 2 | The Beyonce Rule | "If you liked it, shoulda put a test on it." Test everything you value: performance, security, error paths. |
| 3 | Test Boundaries and Errors | Every non-trivial change needs: happy path + failure path + edge case. |
| 4 | Hermetic Tests | Self-contained, order-independent, no shared mutable state. Each test sets up and tears down its own world. |

### Tier B — Design (write mode: decide HOW to write each test)

| # | Principle | Rule |
|---|-----------|------|
| 5 | Test Behavior, Not Implementation | Assert on observable outcomes (return values, persisted state, API output). If refactoring breaks the test, the test was wrong. |
| 6 | Real Over Mock | Prefer: Real > Fake > Spy > Mock. Mock only at external or nondeterministic boundaries. |
| 7 | One Behavior Per Test | Each test is a single given/when/then. Test name reads as a sentence describing the behavior. |
| 8 | Test State, Not Interactions | Verify WHAT the result is, not HOW the system got there. `verify(mock).called()` is almost always wrong. |
| 9 | DAMP Over DRY | Descriptive And Meaningful Phrases. Duplicate freely if it makes each test self-contained and readable. |
| 10 | Straight-Line Tests | No conditionals, loops, try/catch, or computed expected values in tests. Every path through a test is the same path. |
| 11 | Clear Failure Messages | The failure message alone should tell you what went wrong, at 3 AM, without reading the test code. |

### Tier C — Verification (review mode: decide IF tests are trustworthy)

| # | Principle | Rule |
|---|-----------|------|
| 12 | Deterministic Always | Same code + same test = same result. Control time, randomness, network, ordering. |
| 13 | Tests Are Documentation | Write tests a stranger would want to read while debugging. They document expected behavior. |
| 14 | Investigate First-Run Passes | A test that passes immediately proves nothing. Verify it tests the right thing — not the current (possibly buggy) behavior. |
| 15 | Survive Refactoring | If refactoring internals breaks a test without changing behavior, that test is testing implementation details. |

For code examples, exceptions, and language-specific notes on each principle, see [references/principles.md](references/principles.md).

## Mocking Decision Gate

Before adding a mock, answer all five:

1. **Is this dependency external or nondeterministic?** If no, use the real thing.
2. **Will real dependency make the test flaky, slow, or non-hermetic?** If no, use the real thing.
3. **What behavior visibility is lost by mocking here?** Name it explicitly.
4. **Can mocking happen one layer lower while preserving domain behavior?** Push mocks to the edge.
5. **Am I mocking because I understand the dependency, or because I cannot figure out how to use the real one?** Honest self-check.

If answers are unclear, do not mock yet.

**The hierarchy — prefer left:**

```
Real dependency → Fake (in-memory impl) → Spy (real + recording) → Stub (canned response) → Mock (behavior verification)
```

For framework-specific mocking patterns (Jest, pytest, gomock) and the mock audit checklist, see [references/mocking-guide.md](references/mocking-guide.md).

## AI Oracle Guard

**The problem:** AI reads code, infers "expected" behavior from it, writes a test matching the current (possibly buggy) output. 68% of AI-generated test suites validate bugs this way.

**The protocol (mandatory during `write` mode):**

1. **Before writing the test:** State the expected behavior from requirements or spec — not from reading the implementation code.
2. **Write the test** encoding what the code SHOULD do, not what it currently DOES.
3. **Run it against current code.**
4. **If it passes on first run — STOP and investigate:**
   - Behavior already exists correctly → mark as "verified existing behavior" and continue
   - Behavior might be wrong → flag for human review with specific concern
   - Test is too weak (e.g., `toBeDefined()` instead of `toEqual(specificValue)`) → strengthen assertion
5. **If it fails** → proceed with implementation (this is the expected TDD path)

The test must encode what the code SHOULD do, not what it DOES do.

## Anti-Pattern Quick Reference

| # | Pattern | Signal | Fix |
|---|---------|--------|-----|
| 1 | Mock behavior testing | Assertions on `*-mock` artifacts only | Assert real system outputs |
| 2 | Over-mocking | Setup larger than assertion intent | Mock only external boundaries |
| 3 | Unrealistic fixtures | Partial objects, impossible state | Contract-complete fixtures |
| 4 | Test-only production methods | `resetForTests`, `destroyForTest` | Move to test harness |
| 5 | Implementation-detail assertions | Private method call checks | Assert observable outcomes |
| 6 | Snapshot overreach | Huge snapshots as primary signal | Assert critical fields explicitly |
| 7 | Flaky async/time tests | sleep-based waits, race conditions | Control clock, wait on conditions |
| 8 | Silent failures | `expect(true).toBe(true)`, catch-ignore | Fail loudly with diagnostics |
| 9 | Skip debt | Skipped tests without tracking | Skip only with reason + ticket |
| 10 | Coverage theater | High line coverage, weak behavior coverage | Prioritize branch decisions and invariants |
| 11 | Missing regression tests | Bug fixed without pinning failure | Add regression test with fix |
| 12 | Missing boundary contracts | Only unit mocks around APIs | Add integration/contract tests |
| 13 | Assertion roulette | Multiple unrelated assertions, no clear failure message | One behavior per test, clear messages |
| 14 | Circular oracle | Test validates current behavior, not correct behavior | State expected behavior first (Oracle Guard) |
| 15 | Conditional test logic | if/else, loops, try/catch in test body | Straight-line code only |

For full details with code examples, signals, and corrections, see [references/anti-patterns.md](references/anti-patterns.md).

## Workflow

### Plan Mode

1. **Build risk map:** Identify behaviors changed, affected user paths, high-risk failure modes (data loss, auth, money, security, concurrency).
2. **Apply Testing Trophy:** Select test levels using the decision heuristic.
3. **Define minimum test depth** before writing any tests.
4. Apply Tier A principles (P1-P4: Mostly Integration, Beyonce Rule, Boundaries, Hermetic).

### Write Mode

1. **Define observable outcomes:** Return values, persisted state, emitted events, API output, user-visible behavior.
2. **For each non-trivial change:** Write one happy path + one failure path + one boundary/edge case.
3. **For bug fixes:** Include a regression test that fails before the fix.
4. **Oracle Check (mandatory):** Run each test against current code. If it passes on first run, follow the Oracle Guard protocol above.
5. **DAMP structure:** Keep tests descriptive, self-contained, straight-line. Each test tells a complete story.
6. **Clear failure messages:** Every assertion failure should identify what went wrong without reading the test source.
7. Apply Tier B principles (P5-P11).

### Review Mode

1. **Anti-pattern scan:** Check each test against the anti-pattern catalog.
2. **Mutation smell check:** For each assertion, ask: "Would this test still pass if the value were wrong by 1, null, or empty string?" If yes, the assertion is too weak.
3. **Refactoring resilience check:** "Would refactoring internals break this test without changing behavior?" If yes, it tests implementation details.
4. **Determinism check:** Identify time, randomness, network, or ordering dependencies.
5. Apply Tier C principles (P12-P15).

### Report Mode

Use the Required Output Template exactly. Include all fields, no omissions.

### Run Order

When executing tests, run in layers:
1. Targeted tests for changed area
2. Broader package/module suite
3. Full suite when feasible before handoff

## Completion Gate

Do not mark complete until all are true:
- [ ] Tests updated for all changed behavior
- [ ] Failure/edge coverage added for risky paths
- [ ] Oracle Check passed (no unexplained first-run passes)
- [ ] Targeted tests executed successfully
- [ ] Broader/full execution done or explicitly deferred with reason
- [ ] Report includes concrete evidence and limitations

## Honesty Contract

Always include in reports:
- Exact command(s) run
- Scope (files/suites/packages)
- Result summary (passed/failed/skipped)
- Whether execution was targeted or full-suite
- Environment limits that affected confidence

**Required phrases:**
- If tests were not run: `I did not run tests.`
- If only partial scope ran: `I ran targeted tests only.`
- If failures remain: `Tests are currently failing:` followed by the list.
- If first-run passes were investigated: `I accepted N first-run passing tests after investigation.`

**Forbidden phrases:** "should pass", "looks good", "probably fixed", "ready" — without evidence.

## Required Output Template

```text
Testing Summary
- Mode: <plan|write|review|report>
- Commands run:
  - <command>
- Scope:
  - <files/suites>
- Results:
  - <N passed, M failed, K skipped>
- Oracle Check:
  - <N tests investigated for first-run pass, M verified, K flagged>
- Risks covered:
  - <behaviors validated>
- Gaps / limitations:
  - <what was not verified>
```

## Integration with Other Skills

- **Required:** `test-driven-development` for the RED-GREEN-REFACTOR cycle
- **Complementary:** `systematic-debugging` for investigating test failures
- **Referenced by:** `authoring-skills` for testing skills

## Bottom Line

Evidence is the product.

If evidence is weak, improve tests. If evidence is missing, say so directly. If a test passed on first run, prove it should have.
