# Scope

Set explicit boundaries on what to include and exclude. Prevents drift and irrelevant content.

## Quick Summary

**Impact:** Reduces drift, improves relevance
**When to use:** Open-ended tasks, analysis, research, content generation
**Mechanism:** Explicit boundaries prevent the model from expanding beyond what's needed

## The Pattern

```
In scope:
- [Include this]
- [Include this]

Out of scope:
- [Exclude this]
- [Exclude this]

Focus specifically on [primary focus]. Do not expand into [related but excluded areas].
```

## Example

### Without Scope
```
"Analyze our marketing strategy."
```
Result: 2000-word analysis covering everything from brand to pricing to social media...

### With Scope
```
"Analyze our marketing strategy.

IN SCOPE:
- Social media effectiveness (Instagram, TikTok only)
- Q4 2024 campaigns
- Engagement metrics

OUT OF SCOPE:
- Email marketing
- Paid advertising
- Historical comparison before 2024

Focus: What's working on social and what should change for Q1 2025."
```

## Scope Dimensions

| Dimension | In Scope Example | Out of Scope Example |
|-----------|------------------|----------------------|
| **Time** | "Last 6 months only" | "Don't analyze historical data" |
| **Topic** | "Security vulnerabilities" | "Not performance issues" |
| **Depth** | "High-level overview" | "No implementation details" |
| **Audience** | "Technical readers" | "Skip beginner explanations" |
| **Format** | "Bullet points only" | "No prose paragraphs" |

## When to Use

- Open-ended analysis requests
- Research tasks that could expand infinitely
- Content that needs to fit specific requirements
- When you know exactly what you don't want

## When NOT to Use

- Exploratory tasks where expansion is valuable
- When you want comprehensive coverage
- Simple, naturally bounded tasks

## Tips

- Be specific: "Don't discuss competitors" > "Stay focused"
- Include both positive and negative scope when helpful
- Use scope to manage output length indirectly
- Update scope if initial output reveals missed boundaries
