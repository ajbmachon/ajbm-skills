# TDD Block Template

**Include when user wants a test-driven workflow.**

---

## Template

```markdown
## Tests (Write First)

### Unit Tests
- [ ] [Specific behavior to verify]
- [ ] [Edge case to cover]
- [ ] [Error scenario to handle]

### Integration Tests
- [ ] [Component interaction to verify]
- [ ] [External service mock scenario]

### E2E Tests (if applicable)
- [ ] [User flow to verify]

## Tasks (TDD Order)

1. Write failing tests for [core behavior]
2. Implement minimum code to pass
3. Refactor while keeping tests green
4. Write tests for [edge case]
5. Implement edge case handling
6. [Continue pattern...]

## Test Patterns to Follow

[Any specific testing patterns from the codebase or discussion]
```

---

## Guidance

### Tests Should Be Specific

```
❌ "Test the caching"
✅ "Test: cache.get() returns undefined for missing keys"
✅ "Test: cache.set() with TTL expires after specified duration"
✅ "Test: cache.get() after set() returns the set value"
```

### Order Matters

List tests in the order they should be written:
1. Happy path first
2. Edge cases second
3. Error cases third

### Include Test Patterns from Codebase

If the codebase has testing conventions, reference them:

```markdown
## Test Patterns to Follow

- Use `vi.mock()` for external services (see `src/__tests__/setup.ts`)
- Factory functions for test data (see `src/__tests__/factories/`)
- Integration tests use test database (see `docker-compose.test.yml`)
```

### Red-Green-Refactor Reminders

The tasks should reinforce the TDD cycle:

```markdown
## Tasks (TDD Order)

1. Write test: `createUser() returns user with generated ID`
   - **Expected:** Test fails (function doesn't exist)
2. Implement `createUser()` with ID generation
   - **Expected:** Test passes
3. Write test: `createUser() throws on duplicate email`
   - **Expected:** Test fails
4. Add duplicate email check
   - **Expected:** Test passes
5. Refactor: Extract email validation
   - **Expected:** All tests still pass
```
