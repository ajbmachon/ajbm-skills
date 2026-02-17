# Mocking Guide — Full Reference

When to mock, what to mock, and how to do it right across frameworks.

## Table of Contents

- [The Mocking Hierarchy](#the-mocking-hierarchy)
- [The Five-Question Gate](#the-five-question-gate)
- [Framework-Specific Patterns](#framework-specific-patterns)
  - [JavaScript/TypeScript (Jest/Vitest)](#javascripttypescript-jestvitest)
  - [Python (pytest)](#python-pytest)
  - [Go](#go)
- [Mock Audit Checklist](#mock-audit-checklist)
- [Common Mock Smells](#common-mock-smells)

---

## The Mocking Hierarchy

Always prefer left. Move right only when you have a specific reason.

```
Real → Fake → Spy → Stub → Mock
```

| Level | Definition | Example | Use When |
|-------|-----------|---------|----------|
| **Real** | Actual dependency, no substitution | Real PostgreSQL via test container | Default. Start here. |
| **Fake** | Lightweight in-memory implementation | SQLite for Postgres, in-memory queue | Real is too slow (>100ms) or non-hermetic |
| **Spy** | Real dependency with recording | Real HTTP client that logs requests | Need real behavior AND want to verify interactions |
| **Stub** | Canned responses, no real logic | `fetch` returning `{ status: 200, body: {...} }` | External API with predictable responses |
| **Mock** | Behavior verification object | `jest.fn()` with `.toHaveBeenCalledWith()` | Last resort: truly external, nondeterministic |

## The Five-Question Gate

Before adding any mock:

1. **Is this dependency external or nondeterministic?**
   - External: third-party API, email service, payment processor
   - Nondeterministic: current time, random values, network latency
   - If neither → use the real thing

2. **Will the real dependency make the test flaky, slow, or non-hermetic?**
   - Flaky: network timeouts, rate limits
   - Slow: >500ms per test (consider test containers for 100-500ms range)
   - Non-hermetic: shared database, global state
   - If none of these → use the real thing

3. **What behavior visibility is lost by mocking here?**
   - Name it explicitly: "By mocking the database, I lose validation of SQL correctness"
   - If the lost visibility matters → don't mock, or add a separate integration test

4. **Can mocking happen one layer lower while preserving domain behavior?**
   - Instead of mocking `UserService`, mock only the `HttpClient` it uses
   - Push mocks to the outermost boundary

5. **Am I mocking because I understand the dependency, or because I cannot figure out how to use the real one?**
   - If the latter → invest time in understanding the dependency first
   - AI agents frequently mock because setup is hard, not because mocking is right

## Framework-Specific Patterns

### JavaScript/TypeScript (Jest/Vitest)

**Good — Minimal mock at boundary:**
```typescript
// Only mock the HTTP layer
const mockFetch = vi.fn().mockResolvedValue({
  ok: true,
  json: () => Promise.resolve({ id: 1, name: "Alice" }),
});

test("fetches and transforms user data", async () => {
  const user = await getUser(1, { fetch: mockFetch });
  expect(user.displayName).toBe("Alice");
  expect(mockFetch).toHaveBeenCalledWith("/api/users/1");
});
```

**Bad — Mocking internal modules:**
```typescript
jest.mock("../utils/transform");
jest.mock("../services/cache");
jest.mock("../db/connection");
// Three mocks for one behavior — over-mocking
```

**Patterns:**
- Use `vi.fn()` / `jest.fn()` for function stubs
- Use `vi.spyOn()` for spying on real objects
- Prefer dependency injection over `jest.mock()` for module mocking
- Use `msw` (Mock Service Worker) for HTTP API mocking — it intercepts at the network level

### Python (pytest)

**Good — Fixture with real dependency:**
```python
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.rollback()

def test_user_creation(db_session):
    repo = UserRepository(db_session)
    user = repo.create("alice@example.com")
    assert db_session.query(User).count() == 1
```

**Good — Patching only at external boundary:**
```python
@patch("myapp.services.email.smtp_client.send")
def test_welcome_email(mock_send):
    register_user("alice@example.com")
    mock_send.assert_called_once()
    assert "Welcome" in mock_send.call_args[1]["subject"]
```

**Patterns:**
- Use `pytest` fixtures for setup/teardown
- Use `unittest.mock.patch` with `@patch` decorator at import path
- Use `responses` library for HTTP mocking
- Use `freezegun` for time control

### Go

**Good — Interface-based fake:**
```go
type FakeUserStore struct {
    users map[string]User
}

func (f *FakeUserStore) Save(u User) error {
    f.users[u.ID] = u
    return nil
}

func TestCreateUser(t *testing.T) {
    store := &FakeUserStore{users: make(map[string]User)}
    svc := NewUserService(store)

    err := svc.CreateUser("alice@example.com")
    require.NoError(t, err)
    require.Contains(t, store.users, "alice@example.com")
}
```

**Patterns:**
- Define interfaces at the consumer, not the implementation
- Write fakes (not mocks) that implement the interface
- Use `gomock` only for external services
- Use `testcontainers-go` for database integration tests

## Mock Audit Checklist

Run this checklist during review mode:

- [ ] Every mock has a stated reason for existing
- [ ] No mock replaces a dependency that could reasonably be real
- [ ] Mock setup is shorter than the assertion section
- [ ] Assertions test behavior outcomes, not mock call sequences
- [ ] Mocks are at the outermost boundary, not in the middle of the call chain
- [ ] No mock returns another mock (mock chains)
- [ ] Tests would catch a real bug, not just prove mocks are wired correctly

## Common Mock Smells

| Smell | What It Means | Fix |
|-------|--------------|-----|
| Mock returns a mock | Over-mocking; too deep in the chain | Mock at a higher boundary |
| Mock setup > 10 lines | Setup complexity signal | Use a fake or real dependency |
| `any()` matchers everywhere | Not testing specific behavior | Use specific argument matchers |
| Multiple mocks, 1 assertion | Testing wiring, not behavior | Reduce mocks or add behavior assertions |
| Mock verifies call order | Implementation coupling | Test end state instead |
