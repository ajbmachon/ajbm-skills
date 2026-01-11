# Interview Record Template

**Always include this section. It captures the Q&A that led to the spec.**

---

## Purpose

The Interview Record makes the spec self-contained by documenting:
- Key questions that were asked
- User's answers (condensed, not verbatim)
- Research findings that informed decisions
- The reasoning path that led to conclusions

Without this, future readers (including implementation Claude) won't understand WHY choices were made.

---

## Template

```markdown
## Interview Record

### [Theme 1: e.g., "Scope & Boundaries"]

**Q: [Question Claude asked]**
A: [User's answer, condensed to key points]

**Q: [Follow-up question]**
A: [Answer]

[Research note: Verified X against current docs - confirmed/corrected]

### [Theme 2: e.g., "Technical Approach"]

**Q: [Question]**
A: [Answer]

**Q: [Question]**
A: [Answer]

[Research note: Found that library Y actually does Z, not what was assumed]

### [Theme 3: e.g., "Edge Cases & Failure Modes"]

**Q: [Question about edge case]**
A: [How to handle it]

**Q: [Question about failure scenario]**
A: [Recovery/mitigation approach]

---

*This record captures the key decisions and reasoning that led to this spec.*
```

---

## Guidance

### Organize by Theme

Group related Q&A together. Common themes:
- Scope & Boundaries
- Technical Approach
- Edge Cases & Failure Modes
- Integration Points
- Success Criteria
- Open Questions Resolved

### Condense Answers

Don't transcribe verbatim. Extract the decision/key information.

```
❌ "Well, I think maybe we should probably use Redis because
    we've used it before and it works well for caching..."

✅ "Use Redis for caching (team familiarity, proven in codebase)"
```

### Include Research Notes

When research informed the discussion, note it:

```
[Research note: Verified Redis Cluster supports this pattern - docs confirm]
```

```
[Research note: User assumed API v2, but current docs show v3 has breaking changes]
```

### Don't Include Everything

Only include Q&A that:
- Led to a decision
- Clarified something important
- Resolved an ambiguity
- Corrected an assumption

Skip small talk, confirmations, and tangents.
