# ReAct Loop

Reason-Act-Observe cycle. The foundational pattern for agentic LLM behavior.

## Quick Summary

**Impact:** Enables autonomous tool use and multi-step problem solving
**When to use:** Tasks requiring external information, tool use, or iterative refinement
**Mechanism:** Model reasons about what to do, takes an action, observes the result, repeats

## The Pattern

```
Loop:
  1. REASON: "I need to [goal]. Based on [observations], I should [plan]."
  2. ACT:    Call tool / execute step
  3. OBSERVE: Read result, update understanding
  -> Repeat until goal is met or max iterations reached
```

## Prompt Templates

### Single-Prompt ReAct (simple tasks)
```
You have access to these tools: [tool list]

For each step:
Thought: Reason about what to do next and why.
Action: tool_name(arguments)
Observation: [tool result will appear here]
... repeat ...
Final Answer: [response]
```

### Multi-Turn ReAct (complex tasks)
Let the framework handle the loop. System prompt sets intent:
```
You are a research assistant. Use the provided tools to answer
the user's question thoroughly. Search multiple sources before
concluding. If a search returns no results, reformulate the query.
```

### Reason-Plan-ReAct (planner + executor separation)
```
PLANNER: Given [goal], create a numbered plan of 3-7 steps.
EXECUTOR: Execute step {N} of {plan}. Previous results: {results}.
```

## When to Use / NOT to Use

| Approach | Best for | Tradeoff |
|----------|----------|----------|
| Single-prompt | Simple 2-3 step tasks | Fast but brittle on long chains |
| Multi-turn | Production agents, complex tasks | Robust but needs orchestration |
| Reason-Plan-ReAct | 5+ step tasks, delegation | Prevents drift, adds latency |

## Common Failures

- **Plan drift:** After 5+ iterations, model forgets original goal. Fix: include goal in every iteration.
- **Hallucinated observations:** Model invents tool results. Fix: use structured tool calling.
- **Infinite loops:** Fix: cap iterations + "if stuck, try a different approach."

## Model-Specific Notes

- **Claude:** Natively handles ReAct through tool use. No explicit formatting needed.
- **GPT-5.x:** Benefits from explicit Thought/Action/Observation template. Use Responses API.
- **o1/o3:** Skip explicit "Thought:" stage -- model reasons in hidden chain.
- **Open-source (Qwen, DeepSeek):** Require explicit ReAct formatting with few-shot examples.
