# Placement (Primacy/Recency)

Position critical information at the beginning or end of prompts, not in the middle. Leverages attention patterns.

## Table of Contents
1. [Mechanism](#mechanism)
2. [When to Use](#when-to-use)
3. [When NOT to Use](#when-not-to-use)
4. [Shallow vs Deep Examples](#shallow-vs-deep-examples)
5. [The Lost-in-the-Middle Effect](#the-lost-in-the-middle-effect)
6. [Common Mistakes](#common-mistakes)
7. [Self-Check](#self-check)

---

## Mechanism

**Why it works:**
1. **Primacy effect:** Information at the start sets the frame for everything that follows
2. **Recency effect:** Information at the end is freshest in the model's "attention"
3. **Middle neglect:** Research shows LLMs attend less to middle sections in long contexts
4. Mirrors human cognitive patterns (we remember beginnings and endings)

**The research:** Liu et al. (2023) "Lost in the Middle" found retrieval accuracy drops by up to 50% for information in the middle of long contexts. Placing key info at start/end improves accuracy significantly.

**The mechanism in one sentence:** LLMs pay more attention to the beginning and end of context, so place critical information there.

---

## When to Use

- **Long prompts** - The longer the prompt, the more placement matters
- **Multi-document contexts** - Put the most relevant document first or last
- **Critical constraints** - Instructions that must not be ignored
- **RAG applications** - Order retrieved chunks by relevance to query
- **System prompts** - Put key behaviors at start and end

**Rule of thumb:** If something is critical, put it at the start. If it's the key question, put it at the end.

---

## When NOT to Use

- **Short prompts** - Under ~500 tokens, placement matters less
- **Sequential instructions** - When order has logical meaning
- **Narrative contexts** - When chronological order matters for understanding

---

## Shallow vs Deep Examples

### Shallow (What to Avoid)

```
Prompt: "Here's some background information about our company. We were
founded in 2010. We have 500 employees. Our main product is a CRM
system. Our headquarters is in San Francisco.

IMPORTANT: Always respond in formal business English.

We also have offices in London and Tokyo. Our CEO is Jane Smith.
Our annual revenue is $50M. We primarily serve enterprise customers.

Please write a company description for our website."
```

**Why it's shallow:**
- Critical instruction ("formal business English") buried in the middle
- Important context scattered randomly
- No thought to what should be emphasized

### Deep (What to Aim For)

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

**Why it's deep:**
- Critical instruction at start AND repeated at end
- Information organized logically
- Key constraint bookends the content
- Clear structure aids comprehension

---

## The Lost-in-the-Middle Effect

### What It Is

When models process long contexts, they exhibit a U-shaped attention curve:
- **High attention:** Beginning of context
- **Low attention:** Middle of context (up to 50% accuracy drop)
- **High attention:** End of context

### Implications

| Context Length | Middle Impact |
|----------------|---------------|
| < 1K tokens | Minimal |
| 1K - 4K tokens | Moderate |
| 4K - 32K tokens | Significant |
| 32K+ tokens | Severe |

### Mitigation Strategies

1. **Sandwich structure:** Key info at start, supporting details in middle, key info repeated at end
2. **Relevance ordering:** Most relevant content first or last
3. **Chunking:** Break long contexts into sections with summaries
4. **Query at end:** For long documents, place the question last

---

## Common Mistakes

### 1. Burying Instructions in the Middle
**Mistake:** Important constraint mentioned once, mid-prompt
**Problem:** Model may ignore or forget it
**Fix:** Place at start; optionally repeat at end

### 2. Irrelevant Content First
**Mistake:** Starting with background before getting to the task
**Problem:** Sets wrong frame; key task lost in middle
**Fix:** Lead with task, then provide supporting context

### 3. Question Before Context
**Mistake:**
```
"What caused the system failure?

[5000 words of logs and documentation]"
```
**Problem:** Model reads question, then context, question is now "old"
**Fix:** Context first, question last (for long contexts)

### 4. Random Document Ordering in RAG
**Mistake:** Retrieved chunks in arbitrary order
**Problem:** Most relevant info might land in the middle
**Fix:** Order by relevance score, put most relevant first

### 5. Forgetting to Repeat Critical Constraints
**Mistake:** Mentioning a constraint once at the start of a long prompt
**Problem:** May be "forgotten" by the time generation starts
**Fix:** Repeat critical constraints at end: "Remember: [constraint]"

---

## Self-Check

Before sending a long prompt:

- [ ] Are the most important instructions at the start?
- [ ] Is the key question/task at the end (after context)?
- [ ] Have I repeated critical constraints at both start and end?
- [ ] Are retrieved documents ordered by relevance?
- [ ] Is critical information in the middle? (If yes, move it)
- [ ] For very long context: Have I added section summaries?

---

## Patterns

### Pattern 1: Sandwich Structure

```
[CRITICAL INSTRUCTION - START]

[Supporting context]
[Background information]
[Additional details]

[CRITICAL INSTRUCTION - REPEATED AT END]
[Specific question/task]
```

### Pattern 2: Context → Query (for RAG)

```
Here are relevant documents:

[Most relevant document]
[Second most relevant]
[Third most relevant]

Based on the documents above, answer: [question]
```

### Pattern 3: Task-First for Short Prompts

```
Write a haiku about autumn.

Style: melancholic
Theme: falling leaves
Avoid: clichés about seasons changing
```

### Pattern 4: Long-Form with Bookends

```
=== IMPORTANT ===
You are a legal assistant. You must only cite sources provided.
You must never make up case law.
=================

[Document 1: Smith v. Jones (2019)]
[Document 2: Contract terms...]
[Document 3: State regulations...]
...

Based on the documents above, analyze whether the defendant
breached the contract.

=== REMINDER ===
Only cite the documents provided. Do not invent case law.
================
```

---

## Model-Specific Notes

| Model | Placement Sensitivity |
|-------|----------------------|
| **Claude** | Moderate; handles long context well but still benefits from good placement |
| **GPT-4o** | Moderate; 128K context but lost-in-middle still applies |
| **Gemini 2.0** | **Place query at END** - official recommendation for long contexts |
| **DeepSeek** | Standard sensitivity |
| **Kimi K2** | **Put critical constraints EARLY** - instruction drift after ~900 words |
| **Qwen** | Standard sensitivity |

### Special Case: Gemini

Google's official guidance for Gemini 2.0 is explicit:
```
[All context / documents]
...
Based on the information above, [specific question]
```

The query should come LAST after all context for best retrieval.

---

**Impact:** +50% retrieval accuracy in long contexts
**Cost:** None (just reorganization)
**Best for:** Long prompts, RAG, multi-document contexts, critical constraints
