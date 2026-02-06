---
name: testing-anti-patterns
description: Use when writing, changing, reviewing, or reporting tests. Enforces trustworthy testing behavior: right test level selection, realistic assertions, disciplined mocking, anti-pattern detection, and honest reporting of what was actually run.
---

# Testing Best Practices And Anti-Patterns

## Purpose

This skill turns testing from "check the box" into reliable engineering evidence.

Use it whenever you:
- add or modify code with behavior changes
- write or update tests
- review test quality
- report test results to a human partner

## Outcomes

By the end of a testing task, you should have:
- tests that validate real behavior, not scaffolding
- failure cases and edge cases covered for risky paths
- minimal brittle mocks
- explicit test evidence (what ran, what passed/failed)
- no misleading claims

## The Non-Negotiables

```text
1. Never claim a test passed unless you ran it.
2. Never hide failures behind vague language.
3. Never modify production APIs only for test convenience.
4. Never test mock existence instead of system behavior.
5. Never skip uncertainty: state what you could not verify.
```

## Honesty Contract (Agent Reporting)

When reporting testing, always include:
- exact command(s) run
- scope (which test files/suites)
- result summary (passed/failed/skipped)
- whether full suite was run or only targeted tests
- any environment limitations

### Required phrasing rules

- If you did not run tests, say: `I did not run tests.`
- If only targeted tests ran, say: `I ran targeted tests only.`
- If failures remain, say: `Tests are currently failing:` and list them.
- Do not say "should pass", "looks good", or "likely fixed" without evidence.

## Testing Workflow

### Step 1: Risk map before writing tests

Identify:
- core behavior changed
- critical user journeys affected
- high-risk failure modes (data loss, auth, money, security, concurrency)

Use this to decide test depth.

### Step 2: Choose the right test level

Prefer this mix:
- unit tests for pure logic and branching
- integration tests for component boundaries, contracts, persistence, API calls
- end-to-end tests for top workflows only

Do not force all behavior into unit tests with heavy mocks.

### Step 3: Define observable behavior

Write assertions against externally meaningful outcomes:
- returned values
- persisted state
- emitted events
- user-visible output
- protocol/API responses

Avoid assertions on internal implementation unless that internal behavior is itself the contract.

### Step 4: Write or update tests

Minimum expectation for non-trivial behavior:
- happy path
- at least one failure path
- at least one boundary/edge case

For bug fixes:
- add a regression test that fails before the fix and passes after.

### Step 5: Run tests in layers

Order:
1. targeted tests for changed area
2. broader suite (module/package)
3. full suite when feasible before handoff/merge

### Step 6: Report evidence honestly

Use the Honesty Contract format above.

## Anti-Pattern Catalog

## Anti-pattern 1: Testing mock behavior

Bad:
- asserting mock placeholder nodes (`*-mock`)
- proving stub wiring instead of behavior

Fix:
- assert real output/side effects
- unmock if mock obscures behavior under test

## Anti-pattern 2: Over-mocking dependency chains

Bad:
- mocking multiple layers "to be safe"
- mock setup larger than test intent

Fix:
- mock only true external boundaries (network, filesystem, clock, randomness)
- keep domain logic real

## Anti-pattern 3: Incomplete or unrealistic mocks

Bad:
- partial objects that omit fields used downstream
- impossible states that production never emits

Fix:
- model realistic contract-complete fixtures
- include required metadata and failure variants

## Anti-pattern 4: Test-only methods in production code

Bad:
- adding `resetForTests`, `destroyForTest`, etc. to production objects

Fix:
- use test fixtures/helpers/harnesses in test code
- keep production API clean

## Anti-pattern 5: Implementation-detail assertions

Bad:
- asserting private method calls, internal class names, incidental sequence

Fix:
- assert contract behavior and observable outcomes

## Anti-pattern 6: Snapshot overreach

Bad:
- huge snapshots used as primary correctness signal
- blind snapshot updates

Fix:
- use focused assertions for critical fields
- keep snapshots small and reviewed intentionally

## Anti-pattern 7: Flaky async/time tests

Bad:
- real-time sleeps, race-prone assertions, timezone/locale assumptions

Fix:
- control clock/timeouts
- await deterministic conditions
- isolate nondeterministic dependencies

## Anti-pattern 8: Silent failure handling

Bad:
- catch-and-ignore in tests
- `expect(true).toBe(true)` style placeholder checks

Fix:
- fail loudly with clear diagnostics
- assert specific error messages/codes when relevant

## Anti-pattern 9: Skips as debt hiding

Bad:
- skipping flaky tests without issue tracking
- permanent quarantine with no owner

Fix:
- skip only with explicit reason and tracking reference
- define re-enable conditions

## Anti-pattern 10: Coverage theater

Bad:
- chasing percentage without meaningful assertions
- high line coverage, low behavior coverage

Fix:
- prioritize decision branches, invariants, and negative paths

## Anti-pattern 11: Missing regression test for bugfix

Bad:
- fixing code without pinning failure mode in tests

Fix:
- write regression test first (or same change) so bug cannot silently return

## Anti-pattern 12: No contract tests at boundaries

Bad:
- relying only on unit mocks for external schemas/services

Fix:
- add integration/contract tests for serialization, API shape, DB semantics

## Mocking Decision Gate

Before adding a mock, answer all:
1. Is this dependency external or nondeterministic?
2. Does real behavior make test slow/flaky/non-hermetic?
3. What behavior do I lose if I mock here?
4. Can I mock one layer lower and preserve domain behavior?

If you cannot answer clearly, do not mock yet.

## Completion Gate (Before Declaring Done)

A task is not complete until all are true:
- tests added/updated for changed behavior
- at least one negative or edge case included where risk exists
- targeted tests executed successfully
- broader tests executed or explicitly deferred with reason
- result report is explicit and evidence-based

## Review Checklist (Use In PR/Code Review)

Check each item:
- tests validate behavior, not internals
- mock usage is minimal and justified
- fixtures resemble real contracts
- regression tests exist for bug fixes
- assertions are specific and meaningful
- flaky patterns (sleep/race/time) addressed
- failures are informative
- test report is honest and reproducible

## Strong Output Template For Agents

```text
Testing Summary
- Commands run:
  - <command 1>
  - <command 2>
- Scope:
  - <files/suites>
- Results:
  - <N passed, M failed, K skipped>
- Coverage of change:
  - <what behavior is validated>
- Gaps / limitations:
  - <what was not run or not verified>
```

## Red Flag Phrases (Do Not Use Without Evidence)

- "This should work"
- "Looks good to me"
- "Probably fixed"
- "Tests seem fine"
- "Ready" (without execution evidence)

Replace with precise, verifiable statements.

## Bottom Line

Good tests create trust. Honest reporting preserves it.

If evidence is weak, improve tests.
If evidence is missing, say so directly.
