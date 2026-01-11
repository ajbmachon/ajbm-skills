# Uncertainty Quantification

Request confidence levels with outputs. Improves calibration and trust.

## Quick Summary

**Impact:** +25-35% calibration improvement
**When to use:** Factual claims, predictions, recommendations
**Mechanism:** Forces model to introspect on certainty; surfaces epistemic limits

## The Pattern

```
[Complete the task]

For your response, include:
- Confidence level: [High/Medium/Low] or [0-100%]
- What would increase your confidence:
- What you're most uncertain about:
```

## Confidence Scales

### Simple Scale
```
Confidence: High / Medium / Low
- High: Very confident, strong evidence
- Medium: Reasonable confidence, some uncertainty
- Low: Uncertain, limited evidence or complex situation
```

### Numeric Scale
```
Confidence: [0-100%]
- 90%+: Very high confidence
- 70-89%: High confidence
- 50-69%: Moderate confidence
- Below 50%: Low confidence (consider flagging)
```

### Calibrated Scale
```
Rate your confidence using this calibration:
- 90% confident = You'd bet 9:1 odds this is correct
- 70% confident = You'd bet 2.3:1 odds
- 50% confident = Coin flip
```

## Example

### Without Uncertainty
```
"The project will likely complete in 6 weeks."
```

### With Uncertainty
```
"The project will likely complete in 6 weeks.

Confidence: Medium (65%)
- Assumes no scope changes
- Based on similar past projects
- Uncertainty: External API dependency timeline unknown

What would increase confidence:
- Confirmation from API vendor on their timeline
- More detailed task breakdown
- Buffer for unknown unknowns"
```

## When to Use

- Predictions and estimates
- Factual claims that might be wrong
- Recommendations with risk
- Diagnostic reasoning
- Any high-stakes output

## When NOT to Use

- Simple factual retrieval ("What's 2+2?")
- Creative tasks (no "correct" answer)
- When precision is false comfort

## Tips

- Ask for confidence per-claim, not just overall
- Include "what would change your mind" for calibration
- Watch for overconfidence (common) and underconfidence
- Use uncertainty to flag items needing verification
- Numeric confidence often more useful than categorical
