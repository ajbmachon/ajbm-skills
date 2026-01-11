# Assumption Corrections Template

**Include when assumptions were corrected during the interview (either user's or Claude's).**

---

## Purpose

This section documents mutual assumption discovery:
- User assumptions that research contradicted
- Claude assumptions that investigation corrected
- Decisions made after discovering the corrections

This prevents the same wrong assumptions from recurring during implementation.

---

## Template

```markdown
## Assumption Corrections

| Original Assumption | Who Held It | Source of Correction | Corrected Understanding |
|---------------------|-------------|----------------------|-------------------------|
| [What was assumed] | User/Claude | [How we learned otherwise] | [What's actually true] |
| API X supports feature Y | User | Claude researched docs | API X requires Z workaround for Y |
| Common pattern is A | Claude | Codebase investigation | This project uses pattern B instead |
| Library handles edge case | User | Testing during interview | Library throws, need custom handling |
| Deprecated in v3 | Claude | Checked current docs | Still supported, deprecation reverted |

---

*Documenting corrected assumptions prevents repeating mistakes during implementation.*
```

---

## Guidance

### What Qualifies as a Correction

Include when:
- Research contradicted a stated belief
- Codebase investigation showed different patterns
- Documentation revealed outdated understanding
- Testing showed unexpected behavior

Don't include:
- Clarifications (user added detail, not corrected)
- Preferences (not right/wrong, just choices)
- Scope changes (decisions, not corrections)

### Be Specific About Sources

```
❌ "Found out it doesn't work"
✅ "Redis docs v7.2 section 4.3 - SCAN doesn't guarantee ordering"
```

```
❌ "Codebase does it differently"
✅ "src/services/cache.ts:45 - uses LRU, not TTL"
```

### Include Both Parties' Corrections

This isn't just about catching user mistakes. Document when Claude was wrong too:

```
| JWT tokens expire in 1 hour | Claude | User showed auth config | Configured for 24 hours in this app |
```

### Document the Decision

After noting the correction, be clear about what was decided:

```
| API is synchronous | User | Docs show async | Will use async/await pattern, add error handling |
```

---

## When to Omit This Section

If no assumptions were corrected during the interview, omit this section entirely. Don't create an empty table or write "None."

A spec without corrections means either:
- Both parties were well-informed (good!)
- Research wasn't thorough enough (check this)
