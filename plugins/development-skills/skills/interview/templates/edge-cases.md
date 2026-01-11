# Edge Cases Template

**Include when edge cases or failure modes were surfaced during the interview.**

---

## Template - Table Format

```markdown
## Edge Cases & Failure Modes

| Scenario | How to Handle |
|----------|---------------|
| [Edge case description] | [Approach to handle it] |
| [Failure mode] | [Recovery/prevention strategy] |
| Empty input | Return empty result, don't error |
| Network timeout | Retry 3x with exponential backoff, then surface error to user |
| Concurrent modifications | Use optimistic locking, show conflict resolution UI |
```

---

## Template - List Format

Use when more detail is needed:

```markdown
## Edge Cases & Failure Modes

- **[Scenario]**: [How to handle]
  - Detail if needed
  - Additional consideration

- **[Failure mode]**: [Recovery/prevention]
  - Specific steps
  - Fallback behavior
```

---

## Guidance

### Categories to Consider

**Input Edge Cases:**
- Empty/null values
- Extremely large inputs
- Malformed data
- Unicode/special characters

**State Edge Cases:**
- First-time use (no data)
- Migration scenarios (old data format)
- Partial completion (interrupted operations)

**Timing Edge Cases:**
- Race conditions
- Concurrent access
- Stale data

**Failure Modes:**
- Network failures
- Dependency unavailable
- Rate limiting
- Disk full / memory exhaustion
- Permission denied

### Be Specific About Handling

```
❌ "Handle gracefully"
✅ "Show inline error message, preserve user input, enable retry button"
```

```
❌ "Log and continue"
✅ "Log to error channel with context, skip item, increment failure counter, alert if >10 failures/minute"
```

### Prioritize

If many edge cases were identified, indicate priority:

```markdown
### Critical (Must Handle)
- [Edge case that would cause data loss or security issue]

### Important (Should Handle)
- [Edge case that affects user experience]

### Nice to Have (Can Defer)
- [Edge case that's unlikely or has acceptable fallback]
```
