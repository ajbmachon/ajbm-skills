---
name: testing-anti-patterns
description: Use when writing, changing, reviewing, or reporting tests. Enforces trustworthy testing behavior: right test level selection, realistic assertions, disciplined mocking, anti-pattern detection, and honest reporting of what was actually run.
---

# Testing Best Practices And Anti-Patterns

## Purpose

Use this skill to produce test evidence that is trustworthy, reproducible, and useful for decisions.

Apply it whenever you:
- add or modify behavior
- write or revise tests
- review test quality
- report test status to a human partner

## Claude 4.x Execution Rules

Claude 4.x is concise and literal. Use explicit actions and deterministic output.

- Execute testing work, do not just suggest it.
- State unknowns explicitly instead of implying confidence.
- Follow the output contract exactly when reporting.
- Prefer positive directives: what to do next, not just what to avoid.

## Operating Modes

Pick one mode immediately, then run the matching workflow:
- `plan` - build risk map and test strategy before writing tests
- `write` - implement or update tests for changed behavior
- `review` - audit existing tests for anti-patterns and coverage gaps
- `report` - summarize exactly what was executed and what remains

If the user intent is mixed, run `plan` then continue with `write`.

## Non-Negotiables

```text
1. Never claim a test passed unless you ran it.
2. Never hide failures behind vague language.
3. Never modify production APIs only for test convenience.
4. Never test mock existence instead of system behavior.
5. Never skip uncertainty: state what you could not verify.
```

## Honesty Contract (Required In Every Report)

Always include:
- exact command(s) run
- scope (files/suites/packages)
- result summary (passed/failed/skipped)
- whether execution was targeted or full-suite
- environment limits that affected confidence

Required phrases:
- If tests were not run: `I did not run tests.`
- If only partial scope ran: `I ran targeted tests only.`
- If failures remain: `Tests are currently failing:` followed by the list.

Never use: "should pass", "looks good", "probably fixed", "ready" without evidence.

## Workflow

### Step 1: Build Risk Map (`plan`)

Identify:
- behavior changed
- affected user paths
- high-risk failure modes (data loss, auth, money, security, concurrency)

Define minimum test depth before writing tests.

### Step 2: Select Test Level

Use the lowest level that still proves behavior:
- unit: pure logic and branching
- integration: contracts, persistence, boundaries, API/DB semantics
- e2e: critical user journeys only

Do not force everything into unit tests with deep mocks.

### Step 3: Define Observable Outcomes

Assert externally meaningful outcomes:
- returned values
- persisted state
- emitted events
- API/protocol output
- user-visible behavior

Avoid implementation-detail assertions unless internals are part of contract.

### Step 4: Implement Tests (`write`)

For non-trivial changes include:
- one happy path
- one failure path
- one boundary/edge case

For bug fixes include a regression test that fails before the fix.

### Step 5: Run In Layers

Run in this order:
1. targeted tests for changed area
2. broader package/module suite
3. full suite when feasible before handoff

### Step 6: Audit Against Anti-Patterns (`review`)

Check mock scope, fixture realism, assertion quality, flaky behavior, and regression coverage.

### Step 7: Report Evidence (`report`)

Use the required template exactly.

## Anti-Pattern Catalog

### 1) Testing mock behavior instead of system behavior

Signals:
- assertions on `*-mock` artifacts
- proving stub wiring only

Correction:
- assert outputs or side effects from real system behavior
- reduce mocks until assertions target true contract

### 2) Over-mocking dependency chains

Signals:
- multiple stacked mocks for one behavior
- setup larger than assertion intent

Correction:
- mock only external or nondeterministic boundaries
- keep domain logic real

### 3) Incomplete or unrealistic fixtures

Signals:
- partial objects missing required fields
- impossible state combinations

Correction:
- use contract-complete fixtures
- include realistic success and failure variants

### 4) Test-only methods in production code

Signals:
- `resetForTests`, `destroyForTest`, etc.

Correction:
- move lifecycle helpers to test harness/fixtures
- keep production APIs clean

### 5) Implementation-detail assertions

Signals:
- private method call checks
- incidental sequencing checks that are not contractual

Correction:
- assert behavior and outcomes users depend on

### 6) Snapshot overreach

Signals:
- huge snapshots as primary correctness signal
- blind snapshot refreshes

Correction:
- assert critical fields explicitly
- keep snapshots small and intentionally reviewed

### 7) Flaky async/time tests

Signals:
- sleep-based waits
- race-prone assertions
- timezone/locale assumptions

Correction:
- control time/clock
- wait on deterministic conditions
- isolate nondeterministic dependencies

### 8) Silent failures

Signals:
- catch-and-ignore in tests
- placeholder assertions (`expect(true).toBe(true)`)

Correction:
- fail loudly with actionable diagnostics
- assert specific error codes/messages when relevant

### 9) Skip debt hiding

Signals:
- skipped tests without issue reference or owner

Correction:
- skip only with explicit reason + tracking ticket
- define re-enable criteria

### 10) Coverage theater

Signals:
- high line coverage but weak behavior coverage

Correction:
- prioritize branch decisions, invariants, and negative cases

### 11) Missing regression tests for bug fixes

Signals:
- bug fixed without pinning original failure in tests

Correction:
- add regression test before or with fix

### 12) Missing boundary contract tests

Signals:
- only unit mocks around APIs/schemas/storage

Correction:
- add integration/contract tests for boundary semantics

## Mocking Decision Gate

Before adding a mock, answer all:
1. Is this dependency external or nondeterministic?
2. Will real dependency make test flaky, slow, or non-hermetic?
3. What behavior visibility is lost by mocking here?
4. Can mocking happen one layer lower while preserving domain behavior?

If answers are unclear, do not mock yet.

## Completion Gate

Do not mark complete until all are true:
- tests updated for changed behavior
- failure/edge coverage added for risky paths
- targeted tests executed successfully
- broader/full execution done or explicitly deferred
- report includes concrete evidence and limitations

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
- Risks covered:
  - <behaviors validated>
- Gaps / limitations:
  - <what was not verified>
```

## Bottom Line

Evidence is the product.

If evidence is weak, improve tests.
If evidence is missing, say so directly.
