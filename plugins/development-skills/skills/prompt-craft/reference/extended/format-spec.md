# Format-Spec

Provide exact output templates. Ensures consistent, predictable structure.

## Quick Summary

**Impact:** Near-perfect format compliance
**When to use:** Structured reports, consistent outputs, parsed content
**Mechanism:** Template shows exact structure; model fills in content

## The Pattern

```
Output your response in exactly this format:

## [Section Title]
[2-3 sentences about topic]

### Key Points
- [Point 1]
- [Point 2]
- [Point 3]

### Recommendation
[Single paragraph recommendation]
```

## Example Templates

### Report Template
```
# [Report Title]

## Executive Summary
[3-4 sentences summarizing key findings]

## Findings

### Finding 1: [Title]
**Evidence:** [Supporting data]
**Impact:** [High/Medium/Low]

### Finding 2: [Title]
**Evidence:** [Supporting data]
**Impact:** [High/Medium/Low]

## Recommendations
1. [Action item]
2. [Action item]

## Next Steps
- [ ] [Task 1]
- [ ] [Task 2]
```

### Comparison Template
```
| Aspect | Option A | Option B | Winner |
|--------|----------|----------|--------|
| [Criterion 1] | [Value] | [Value] | A/B/Tie |
| [Criterion 2] | [Value] | [Value] | A/B/Tie |

**Recommendation:** [Option] because [reason]
```

### Code Review Template
```
## File: [filename]

### Issues Found
1. **[Severity]** Line [N]: [Description]
   - Problem: [What's wrong]
   - Fix: [How to fix]

### Positive Notes
- [What's done well]

### Summary
- Critical issues: [N]
- Warnings: [N]
- Suggestions: [N]
```

## When to Use

- Reports that need consistent structure
- Outputs that will be parsed programmatically
- Templates for recurring tasks
- When multiple outputs need to be comparable

## When NOT to Use

- Creative writing
- Conversational responses
- When flexibility is more important than structure

## Tips

- Show the exact format with placeholder content
- Use realistic placeholders: `[2-3 sentences]` > `[text here]`
- Include section markers (##, ###) if structure matters
- Combine with structured output (JSON) for programmatic parsing
- Test your template to ensure it's followable
