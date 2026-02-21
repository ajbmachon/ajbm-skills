# ReAct Loop

Reason-Act-Observe cycle. The foundational pattern for agentic LLM behavior.

## Quick Summary

**Impact:** Enables autonomous tool use and multi-step problem solving
**When to use:** Tasks requiring external information, tool use, or iterative refinement
**Mechanism:** Model reasons about what to do, takes an action, observes the result, then repeats

## The Pattern

```
Loop:
  1. REASON: "I need to [goal]. Based on [observations], I should [plan]."
  2. ACT:    Call tool / execute step
  3. OBSERVE: Read result, update understanding
  → Repeat until goal is met or max iterations reached
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
Thought: I now have enough information.
Final Answer: [response]
```

### Multi-Turn ReAct (complex tasks)
Let the framework handle the loop. Your system prompt sets intent:
```
You are a research assistant. Use the provided tools to answer
the user's question thoroughly. Search multiple sources before
concluding. If a search returns no results, reformulate the query.
```

### Reason-Plan-ReAct Variant (planner + executor separation)
```
PLANNER PROMPT:
Given this goal: [user request]
Create a numbered plan of 3-7 steps. Each step should be one
concrete action. Output ONLY the plan as a numbered list.

EXECUTOR PROMPT:
You are executing step {N} of this plan:
{full_plan}

Previous results:
{accumulated_results}

Execute ONLY step {N}. Use tools as needed. Output your result.
```

## When to Use Single-Prompt vs Multi-Turn

| Approach | Best for | Tradeoff |
|----------|----------|----------|
| Single-prompt ReAct | Simple 2-3 step tasks, demos | Fast but brittle on long chains |
| Multi-turn (framework) | Production agents, complex tasks | Robust but needs orchestration |
| Reason-Plan-ReAct | Tasks with 5+ steps, delegation | Prevents plan drift, adds latency |

## Common Failures

**Plan drift:** After 5+ iterations, the model forgets its original goal. Fix: include the original goal in every iteration's context.

**Action-observation mismatch:** Model hallucinates a tool result instead of waiting for the real one. Fix: use structured tool calling (not free-text "Action:").

**Infinite loops:** Model repeats the same action expecting different results. Fix: cap iterations and include a "if stuck, try a different approach" instruction.

**Over-reasoning:** Model writes paragraphs of thought before a simple action. Fix: "Keep reasoning to 1-2 sentences. Act quickly."

## Model-Specific Notes

- **Claude:** Natively handles ReAct through tool use. No need for explicit Thought/Action/Observation formatting -- just provide tools and a clear system prompt. Claude auto-delegates reasoning internally.
- **GPT-4o / GPT-5:** Benefits from explicit ReAct structure in the prompt. Use the Thought/Action/Observation template for best results.
- **o1 / o3:** Extended thinking handles reasoning internally. Provide tools but skip the explicit "Thought:" stage -- the model reasons in its hidden chain.
- **Open-source (Qwen, DeepSeek):** Require explicit ReAct formatting. Include few-shot examples of the loop.

## When to Use

- Any task requiring external data retrieval
- Multi-step problem solving with tools
- Research tasks needing iterative search refinement
- Debugging workflows (hypothesize, test, observe)

## When NOT to Use

- Pure text generation (no tools needed)
- Tasks where the answer is in the prompt context already
- Latency-critical single-shot responses
- When chaining (see: chaining.md) with fixed stages is sufficient

## Tips

- Start with multi-turn framework-managed ReAct; only drop to single-prompt for simple cases
- Always set a max iteration limit (5-10 for most tasks)
- Include the original goal in every loop iteration to prevent drift
- For 5+ step tasks, use Reason-Plan-ReAct to separate planning from execution
- Log intermediate observations for debugging failed chains

See also: [chaining](chaining.md) for fixed-stage pipelines
