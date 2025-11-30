# Compression

Reduce context size while preserving utility. Enables efficient use of context window.

## Quick Summary

**Impact:** -80% tokens with 95% utility preserved
**When to use:** Long documents, large codebases, multi-document contexts
**Mechanism:** Hierarchical summarization, relevance filtering, structured condensation

## The Pattern

```
Compress this [document/context] for use in answering questions about [topic].

Preserve:
- Key facts and figures
- Main arguments
- Critical details related to [specific focus]

Remove:
- Redundant information
- Tangential content
- Verbose explanations (keep conclusions)
```

## Compression Strategies

### 1. Hierarchical Summarization

```
Level 1: Executive summary (100 words)
Level 2: Section summaries (50 words each)
Level 3: Key details (bullet points)

Include only levels needed for the task.
```

### 2. Relevance Filtering

```
Given the question "[question]", extract only the passages
directly relevant to answering it. Ignore unrelated content.
```

### 3. Structured Extraction

```
Extract from this document:
- Main claim:
- Supporting evidence (3 max):
- Counterarguments:
- Conclusion:
```

## Example

### Before (500 words)
Full article about climate change with history, science, politics, solutions...

### After Compression (100 words)
```
TOPIC: Climate Change Policy
KEY FACTS:
- Global temp +1.1°C since pre-industrial
- 2030 deadline for major reductions
- Current pledges insufficient (2.7°C trajectory)

MAIN ARGUMENT: Carbon pricing most effective mechanism
EVIDENCE: EU ETS reduced emissions 35% in covered sectors
COUNTERPOINT: Regressive impact on low-income populations
SOLUTION PROPOSED: Carbon dividend to offset costs
```

## When to Use

- Long documents that don't fit in context
- Multiple documents to synthesize
- Repeated queries against same content (compress once, reuse)
- Context caching optimization

## When NOT to Use

- When full detail is required for the task
- Legal/medical contexts where precision matters
- Short documents that fit easily

## Tips

- Preserve structure (headers, sections) even when condensing content
- Keep numbers and proper nouns (often critical)
- Test compression quality: Can you answer key questions from compressed version?
- For code: Keep signatures and key logic, remove boilerplate
