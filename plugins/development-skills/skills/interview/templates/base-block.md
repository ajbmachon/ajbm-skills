# Base Block Template

**Always include these sections in every spec.**

---

## Template

```markdown
## Problem Statement

[What pain does this solve? Why does it matter? Who has this problem?]

Be specific:
- Who experiences this problem?
- When/how does it manifest?
- What's the cost of not solving it?

## Objective

[What are we building? Clear, concrete goal.]

One sentence that captures the essence. Should be quotable.

Example: "A caching layer that reduces API latency by 80% for repeat queries."

## Success Criteria

[How do you know it worked? What does "done" look like?]

List specific, testable criteria:
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

Each criterion should be verifiable - someone should be able to check "yes, this is met" or "no, it's not."
```

---

## Guidance

### Problem Statement

Don't be vague:
- ❌ "Users have trouble with performance"
- ✅ "Dashboard load times exceed 5 seconds for users with >1000 items, causing page abandonment"

### Objective

Keep it concrete:
- ❌ "Improve the user experience"
- ✅ "Add real-time search filtering to the project list, updating results as user types"

### Success Criteria

Make them testable:
- ❌ "Works well"
- ✅ "Response time < 200ms for 95th percentile queries"
- ✅ "All existing tests pass"
- ✅ "User can filter 10,000 items in under 1 second"
