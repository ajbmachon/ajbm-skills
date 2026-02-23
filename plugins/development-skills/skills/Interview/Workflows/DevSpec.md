# Development Specification Workflow

Interview type for crystallizing software development ideas into implementation-ready specs.

---

## Domain-Specific Research (Phase 1)

### BLOCKING Research Targets
- **Codebase:** Structure, patterns, existing implementations, conventions
- **Technologies mentioned:** ALWAYS verify against CURRENT docs — training data may be stale
- **Existing libraries/solutions:** Search for what already solves this
- **API surfaces:** Verify capabilities, deprecations, breaking changes

### Research Agent Usage

| Topic | Agent Type | Phase |
|-------|------------|-------|
| Codebase structure | Explore | Phase 1 (BLOCKING) |
| Existing implementations | Explore | Phase 1 (BLOCKING) |
| Technology docs | docs-research-specialist | Phase 1 (BLOCKING) |
| API verification | docs-research-specialist | Phase 3+ (BACKGROUND) |
| Library alternatives | docs-research-specialist | Phase 3+ (BACKGROUND) |

---

## Domain-Specific Challenge Angles (Phase 2)

- "Does this need to exist as code? Could configuration solve it?"
- "Is there already a library that does this?" (cite specific findings)
- "Your codebase already has a pattern for this in [location]. Should we follow it?"
- "This seems like it could be solved with [simpler approach]. Why the complexity?"
- "What happens at scale? This pattern tends to break at [threshold]."

---

## Domain-Specific Questions (Phase 3)

### Architecture & Design
- How does this integrate with the existing architecture?
- What data model changes are needed?
- What are the performance requirements?
- How will this be deployed?

### Implementation Details
- What testing strategy? (unit, integration, E2E)
- What error handling approach?
- How does this interact with existing APIs?
- What migration path from current state?

### Technical Edge Cases
- What happens under concurrent access?
- How does this behave with large datasets?
- What if dependencies are unavailable?
- What's the rollback strategy?

---

## Dev-Specific Verification Gate Tiers

The core VerificationGate.md defines the general protocol. These are the dev-specific decision tiers.

### Dev Tier 1: Major Structural Decisions (FULL CHECK)

Full constraint verification before:
- **Architecture patterns**: Monorepo vs polyrepo, microservices vs monolith, serverless vs containers
- **Database choices**: SQL vs NoSQL, managed vs self-hosted, single vs sharded
- **Deployment strategy**: Single tenant vs multi-tenant, per-customer vs shared
- **Framework selection**: React vs Vue, Express vs Fastify, any major tech choice
- **Service architecture**: How components communicate, API design
- **Data flow**: Where data lives, how it moves between systems

### Dev Tier 2: Minor Refinements (LIGHTWEIGHT CHECK)

Quick constraint scan before: file naming, code style, variable naming, comment style.

### Dev "Standard Pattern" Trap Examples

Claude knows standard dev patterns and applies them without checking fit:
- "Turborepo monorepos have apps/ and packages/" — but user needs separate repos
- "Microservices communicate via message queues" — but user has a team of 2
- "React apps use Redux for state management" — but user's app is simple enough for context

**Before applying any standard dev pattern**, run the Verification Gate's 4-question check against the Constraint Registry.

---

## Domain-Specific Output Additions

### TDD Block (include when test-driven workflow requested)

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

## Test Patterns to Follow

[Any specific testing patterns from the codebase or discussion]
```

**Guidance:**
- Tests should be specific: "Test: cache.get() returns undefined for missing keys" not "Test the caching"
- Order: Happy path, then edge cases, then error cases
- Reference codebase testing conventions when present
- Reinforce red-green-refactor cycle

### Code Examples (include ONLY when needed)

Include code examples when:
- Pattern is specific to this codebase/framework
- Implementation is easy to get wrong
- Current documentation differs from training data
- Codebase has conventions that override defaults

Skip when Claude would write it correctly from standard knowledge.

```markdown
## Code Examples

> These patterns are specific to this codebase/framework. Follow them exactly.

### [Pattern Name]

**Why this matters:** [Brief explanation]

```[language]
// Example code
```

**Key points:**
- [Important detail 1]
- [Important detail 2]

**From codebase:** `[file path where this pattern exists]`
```
