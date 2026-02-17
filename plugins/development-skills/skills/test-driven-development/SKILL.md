---
name: test-driven-development
description: Use when implementing any feature or bugfix before implementation changes. Enforces test-first behavior: write a failing test, verify failure, implement minimal code, and prove green.
---

# Test-Driven Development (TDD)

## Purpose

Use TDD to prove behavior changes, prevent regressions, and keep implementation scope tight.

Core principle:

```text
If you did not observe a meaningful failing test first, you do not yet have proof the test validates the change.
```

## Claude 4.x Execution Rules

Claude 4.x tends to be concise and suggestion-oriented. This skill requires execution-first behavior.

- Perform the TDD cycle, do not stop at advice.
- Run tests and report evidence.
- Avoid speculative language.
- Follow the output contract exactly.

## When To Use

Default for:
- new features
- bug fixes
- behavior changes
- refactors that may change behavior

Allowed exceptions (confirm with human partner):
- throwaway prototypes
- generated code
- pure configuration/docs changes
- urgent incident mitigation where test-first is temporarily impossible

If exception is used, document why and schedule follow-up tests.

## Iron Law

```text
No behavior-changing production code is complete without a failing test that was observed before the final implementation.
```

## If Code Exists Before RED

If you write behavior-changing implementation code before a failing test:
1. Delete that implementation code.
2. Do not keep it as reference while writing tests.
3. Start from RED with a failing test first.
4. Re-implement minimally to GREEN from the test signal.

Exception only with explicit human partner approval.

## Red-Green-Refactor Loop

### RED: Write One Failing Test

- One behavior per test.
- Test name states observable outcome.
- Prefer real domain behavior; mock only boundaries.

### Verify RED (Mandatory)

Run targeted test command and confirm:
- test fails (not setup error)
- failure reason matches missing behavior

If it passes immediately, the test is not proving the new requirement yet.

### GREEN: Minimal Implementation

- Write the smallest change that satisfies failing test.
- Avoid unrelated refactors and feature expansion.

### Verify GREEN (Mandatory)

Run targeted tests, then broader scope when feasible.

Confirm:
- new test passes
- nearby tests still pass
- no new failures introduced

### REFACTOR

After green:
- remove duplication
- improve naming/structure
- keep behavior unchanged

Re-run tests to prove refactor preserved behavior.

## Test Quality Bar

Each non-trivial change should include:
- happy path
- failure path
- at least one boundary/edge case

For bug fixes:
- mandatory regression test that would have caught the bug

## Anti-Patterns

- writing implementation before defining failing test
- accepting a test that passes immediately without validating requirement gap
- broad refactor during GREEN
- mock-heavy tests that only assert call counts
- claiming completion without execution evidence

## Reporting Contract (Required)

```text
TDD Summary
- Requirement under test:
  - <behavior>
- RED evidence:
  - Command: <command>
  - Failure observed: <yes/no + key message>
- GREEN evidence:
  - Command: <command>
  - Result: <passed/failed>
- Broader verification:
  - <suite command + result> OR "Deferred: <reason>"
- Notes:
  - <exceptions, constraints, or follow-up tests>
```

Required phrases:
- If tests were not run: `I did not run tests.`
- If only partial scope ran: `I ran targeted tests only.`

## Completion Gate

Before marking done:
- failing test observed for changed behavior
- minimal implementation landed
- targeted tests green
- broader verification done or explicitly deferred with reason
- summary includes concrete commands and outcomes

## Bottom Line

TDD is an evidence discipline, not a slogan.
