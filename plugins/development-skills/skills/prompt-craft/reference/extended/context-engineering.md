# Context Engineering

Curating and maintaining the optimal set of tokens during LLM inference. Your context window is a finite resource -- spend it wisely.

## Quick Summary

**Impact:** Determines ceiling of model performance; no prompt trick overcomes bad context
**When to use:** Any non-trivial LLM application, especially agentic systems
**Mechanism:** Strategic loading, compaction, and tiering of information in the context window

## What Is Context?

Context = system prompt + tool descriptions + memory/state + conversation history + RAG docs + user message. Each component competes for the same token budget.

## Token Budget as Resource Management

```
System prompt: 2-5K | Tools: 1-10K | Memory: 1-5K
History: 10-50K (this is what you manage)
RAG docs: 5-20K | User message: 0.1-2K
```

When total context exceeds ~80% of the window, quality degrades. Plan for compaction before hitting that threshold.

## Tiered Context Strategy

### Hot (always present)
- System prompt and identity
- Current tool schemas
- Active task state
- Last 2-3 conversation turns

### Warm (loaded on demand)
- Recent tool call results (summarized)
- Retrieved documents for current query
- Session-level memory

### Cold (stored externally)
- Long-term memory / knowledge base
- Historical conversation logs
- Full tool output history

**Rule of thumb:** Hot context should be under 10K tokens. Warm context loads just-in-time. Cold context lives on disk or in a database.

## Loading Strategies

### Just-in-Time Loading (preferred)
Load information only when the model needs it:
```
"When you need project context, read the README.
When you need test results, run the test suite.
Do NOT preload everything at startup."
```

### Pre-Loading (use sparingly)
Front-load context the model will definitely need (e.g., database schema for a SQL agent).

**When to pre-load:** Information needed in >80% of interactions.
**When to JIT-load:** Information needed in <50% of interactions.

## Compaction Strategies

### 1. Summarize history
Replace old turns with a summary: `[Earlier: implemented JWT auth with 24h expiry. Tests pass.]`

### 2. Clear tool results
Tool outputs are often large and only relevant once. After processing, replace with what was learned.

### 3. Full context reset
Start fresh with a state handoff:
```
You are continuing a task. Current state:
- Goal: [original goal]
- Completed: [what's done]
- Next: [what to do next]
- Key decisions: [important context]
```

### When to compact vs reset
- **Compact** when the conversation is productive and you want continuity
- **Reset** when context is polluted with failed approaches or stale data
- Claude 4.5+ excels at filesystem rediscovery -- fresh context with "read the project files" often outperforms degraded long context

## Progressive Disclosure

Structure information so the model discovers detail as needed:

```
Level 0 (system prompt): Project overview, key rules
Level 1 (file reads):    Architecture docs, schemas
Level 2 (tool calls):    Specific code, test results
Level 3 (search):        External docs, APIs
```

Start with minimal context and drill down. This mirrors how experienced engineers work.

## When to Use

- Building agents that run for many turns
- RAG systems with large document sets
- Multi-tool systems with extensive schemas
- Any application hitting context window limits

## When NOT to Use

- Single-turn Q&A with short prompts
- Applications well within context limits
- Prototyping (optimize later)

## Tips

- Monitor token usage per component; you cannot manage what you do not measure
- Structured data (JSON) compresses better than prose for state tracking
- Put the most important context at the beginning and end of the window (primacy/recency effect)
- Test with artificially small context windows to find fragility early

See also: [multi-session](multi-session.md) for managing context across session boundaries
