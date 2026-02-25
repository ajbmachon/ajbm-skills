# Context Engineering

Curating and maintaining the optimal set of tokens during LLM inference. Your context window is a finite resource.

## Quick Summary

**Impact:** Determines ceiling of model performance; no prompt trick overcomes bad context
**When to use:** Any non-trivial LLM application, especially agentic systems
**Mechanism:** Strategic loading, compaction, and tiering of information

## Token Budget as Resource Management

```
System prompt: 2-5K | Tools: 1-10K | Memory: 1-5K
History: 10-50K (this is what you manage)
RAG docs: 5-20K | User message: 0.1-2K
```

When total context exceeds ~80% of the window, quality degrades.

## Tiered Context Strategy

- **Hot (always present):** System prompt, tool schemas, active task state, last 2-3 turns
- **Warm (loaded on demand):** Recent tool results (summarized), retrieved docs, session memory
- **Cold (stored externally):** Long-term memory, historical logs, full tool output history

**Rule of thumb:** Hot context under 10K tokens. Warm loads just-in-time. Cold lives on disk.

## Loading Strategies

**Just-in-time (preferred):** Load information only when the model needs it.
**Pre-loading (sparingly):** Front-load context needed in >80% of interactions.

## Compaction Strategies

1. **Summarize history:** Replace old turns with a summary
2. **Clear tool results:** After processing, replace with what was learned
3. **Full context reset:** Start fresh with a state handoff:
```
You are continuing a task. Current state:
- Goal: [original goal]
- Completed: [what's done]
- Next: [what to do next]
```

**When to compact vs reset:** Compact when productive; reset when context is polluted with failed approaches.

## Tips

- Monitor token usage per component
- JSON compresses better than prose for state tracking
- Important context at beginning and end of window (primacy/recency)

See also: [multi-session](multi-session.md) for cross-session persistence
