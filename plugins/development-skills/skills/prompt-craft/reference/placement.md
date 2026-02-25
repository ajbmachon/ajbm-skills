# Placement (Primacy/Recency)

Position critical information at the beginning or end of prompts, not in the middle. Leverages attention patterns.

## Mechanism

**Why it works:** Primacy effect sets the frame; recency effect keeps information freshest in attention. Research shows LLMs attend less to middle sections in long contexts, mirroring human cognitive patterns.

**The research:** Liu et al. (2023) "Lost in the Middle" found retrieval accuracy drops by up to 50% for information in the middle of long contexts.

## When to Use

- Long prompts (the longer the prompt, the more placement matters)
- Multi-document contexts (put most relevant document first or last)
- Critical constraints that must not be ignored
- RAG applications (order retrieved chunks by relevance)

**Rule of thumb:** If something is critical, put it at the start. If it's the key question, put it at the end.

## When NOT to Use

- Short prompts (under ~500 tokens, placement matters less)
- Sequential instructions with logical ordering
- Narrative contexts where chronological order matters

## The Lost-in-the-Middle Effect

When models process long contexts, they exhibit a U-shaped attention curve:
- **High attention:** Beginning and end of context
- **Low attention:** Middle of context (up to 50% accuracy drop)

| Context Length | Middle Impact |
|----------------|---------------|
| < 1K tokens | Minimal |
| 1K - 4K tokens | Moderate |
| 4K - 32K tokens | Significant |
| 32K+ tokens | Severe |

**Mitigation strategies:**
1. **Sandwich structure:** Key info at start, supporting details in middle, key info repeated at end
2. **Relevance ordering:** Most relevant content first or last
3. **Chunking:** Break long contexts into sections with summaries
4. **Query at end:** For long documents, place the question last

## Deep Example

```
Prompt: "IMPORTANT: Respond in formal business English throughout.

Write a company description for our website using these details:

COMPANY OVERVIEW:
- Founded: 2010
- Headquarters: San Francisco
- Additional offices: London, Tokyo
- Employees: 500
- Annual revenue: $50M
- CEO: Jane Smith

PRODUCT & MARKET:
- Main product: Enterprise CRM system
- Primary customers: Enterprise businesses

Write a professional 2-paragraph company description.
Remember: Maintain formal business English tone throughout."
```

**Why it works:** Critical instruction at start AND repeated at end. Information organized logically. Key constraint bookends the content.

## Model-Specific Notes

| Model | Placement Sensitivity |
|-------|----------------------|
| **Claude** | Moderate; handles long context well but still benefits from good placement |
| **GPT-5.x** | 400K context; lost-in-middle reduced but still benefits from good placement |
| **Gemini 2.0+** | **Place query at END** -- official recommendation for long contexts |
| **DeepSeek** | Standard sensitivity |
| **Kimi K2** | **Put critical constraints EARLY** -- instruction drift after ~900 words |
| **Qwen** | Standard sensitivity |

---

**Impact:** +50% retrieval accuracy in long contexts
**Cost:** None (just reorganization)
**Best for:** Long prompts, RAG, multi-document contexts, critical constraints
