# Open Questions Template

**Include when uncertainties remain after the interview.**

---

## Template

```markdown
## Open Questions

- [ ] [Unresolved decision or uncertainty]
- [ ] [Thing that needs more investigation]
- [ ] [Dependency on external factor]

### Details

**[Question 1]**
Context: [Why this is unresolved]
Blocker: [What's needed to resolve it]
Fallback: [What to do if it can't be resolved]

**[Question 2]**
Context: [Why this is unresolved]
Impact: [What depends on this answer]
```

---

## Guidance

### What Qualifies as Open

Include:
- Decisions that couldn't be made during interview
- Technical unknowns requiring investigation
- Dependencies on external people/teams
- Things that need production data to decide

Don't include:
- Resolved questions (those go in Interview Record)
- Implementation details (those get figured out during coding)
- Nice-to-haves being deferred (those are scope decisions)

### Be Specific About What's Needed

```
❌ "Need to figure out authentication"
✅ "Need to confirm with security team: can we use OAuth refresh tokens with 7-day expiry, or is there a policy limit?"
```

### Include Fallback/Default

What should implementation do if the question can't be resolved in time?

```
- [ ] Should error messages be user-facing or generic?
      Fallback: Use generic messages, add feature flag for detailed errors later
```

### Keep It Short

If you have many open questions, the interview wasn't thorough enough.

Ideal: 0-3 open questions
Concerning: 5+ open questions (consider more interview rounds)

### Mark Resolution Path

Who/what can resolve this?

```
- [ ] Rate limit threshold (needs load testing with production-like data)
- [ ] API key rotation policy (needs decision from security team - @alice)
- [ ] Cache invalidation strategy (blocked on understanding write patterns - revisit after v1)
```
