# Tradeoffs Template

**Include when decisions were made between alternatives during the interview.**

---

## Template

```markdown
## Tradeoffs & Decisions

| Decision | Alternatives Considered | Why This Choice? |
|----------|------------------------|------------------|
| [Choice made] | [Other options considered] | [Reasoning for selection] |
| Use Redis for caching | Memcached, in-memory Map | Team familiarity, persistence support, existing infrastructure |
| REST over GraphQL | GraphQL, gRPC | Simpler for this use case, matches existing API patterns |
| Optimistic locking | Pessimistic locking, no locking | Better UX for low-conflict scenario, graceful conflict handling |
```

---

## Guidance

### What Qualifies as a Tradeoff

Include when:
- Multiple valid approaches were discussed
- A conscious choice was made between options
- The reasoning should be preserved for future reference

Don't include:
- Obvious choices with no real alternatives
- Decisions already made before the interview
- Implementation details (save for code comments)

### Document the "Why"

The reasoning is the valuable part:

```
❌ "Chose React" (no reasoning)
✅ "Chose React - existing codebase uses it, team expertise, component library available"
```

```
❌ "Went with option A"
✅ "Went with option A - 50% less complexity, acceptable performance tradeoff (100ms vs 50ms)"
```

### Include Rejected Alternatives

Knowing what was NOT chosen and why prevents relitigating the decision:

```
| Sync API calls | Async with queuing | Simpler, latency acceptable (<200ms), avoids queue infrastructure |
```

Future reader understands: "They considered async but chose sync because latency was acceptable."

### Quantify When Possible

```
❌ "Better performance"
✅ "2x faster for 95th percentile queries (measured: 400ms → 200ms)"
```

```
❌ "Simpler"
✅ "200 lines vs 500 lines, no additional dependencies"
```
