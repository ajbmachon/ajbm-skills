# OpenAI

## GPT-5.2

**Status:** Current flagship (replaces GPT-5.1)
**Best for:** Complex reasoning, broad world knowledge, agentic/tool-heavy workflows, and code-heavy tasks
**Knowledge cutoff:** 2025-08-31
**Context (API):** 400K tokens | **Max output:** 128K tokens
**Chat model:** `gpt-5.2-chat-latest` (128K context | 16,384 max output)

### What changed vs GPT-5.1

- Better general intelligence and instruction following
- More accurate and token-efficient answers
- Stronger multimodality (especially vision)
- Better tool calling + context management in the API
- New context management capability via **compaction**
- Adds **`xhigh` reasoning effort** and **concise reasoning summaries**

### The knobs that matter

**1) `reasoning.effort` (quality vs latency/cost)**
- Default is `none` (fast / low-latency).
- Increase gradually (`medium` -> `high` -> `xhigh`) for harder reasoning.
- With `none`, prompting matters more: explicitly ask for a *brief plan / outline* before the final answer.

**2) `text.verbosity` (response length / "how much to say")**
- Values: `low`, `medium`, `high` (default: `medium`).
- Use this instead of trying to fight verbosity purely with prompting.

**3) Reasoning summaries (`reasoning.summary`)**
- GPT-5.2 can return concise summaries of its reasoning (useful for audits / traceability without exposing full hidden reasoning).

**4) Compaction (`POST /v1/responses/compact`)**
- Use for long-running workflows (many turns / tool calls) to extend effective context.
- Output is **opaque/encrypted**: treat as "state to continue with", not data to parse.

### Prompting patterns that reliably improve results

**Output-shape + length clamps (high ROI)**
Give concrete constraints: bullet caps, section names, snippet limits, etc.
(Works especially well for enterprise agents and coding assistants.)

**Scope-drift prevention (especially UI/front-end)**
GPT-5.2 is strong at structured code but may "helpfully" add features/design.
Explicitly forbid extras: "Implement ONLY what I asked. No embellishments."

**Long-context handling**
For big inputs, force re-grounding:
- Summarize key relevant sections first
- Restate constraints (jurisdiction/date range/etc.)
- Anchor claims to sections ("In the Data Retention section...")

**Ambiguity guardrails**
If underspecified: ask 1-3 clarifying questions *or* give 2-3 interpretations with labeled assumptions.
Never invent exact figures/links when uncertain; prefer "based on provided context..."

### Tools & agent workflows

- Prefer **Responses API** for tool-heavy workflows; it supports better conversation state handling.
- GPT-5.2 is post-trained on specific tools (notably `apply_patch` and `shell`) and supports **custom tools** (freeform tool inputs + optional constrained outputs).
- For long task chains, compact after milestones (not every turn), then continue with the compacted state.

### Common gotchas

- Some sampling controls (e.g., temperature/top_p/logprobs) are only supported when `reasoning.effort` is `none`.
- For hard problems, you usually get better reliability by:
  1) raising `reasoning.effort`, and
  2) tightening output shape and scope constraints,
  before adding long personas or many examples.

**Sources:**
- OpenAI "Using GPT-5.2 / latest model" docs: https://platform.openai.com/docs/guides/latest-model
- GPT-5.2 Prompting Guide (Cookbook): https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide
- OpenAI Models pages: https://platform.openai.com/docs/models
- Responses API + compaction reference: https://platform.openai.com/docs/api-reference/responses/compact

---

## GPT-5.1

**Status:** Previous flagship (still useful; cheaper than 5.2 in many setups)
**Best for:** Coding + agentic workflows where you want **configurable reasoning** and strong steerability
**Knowledge cutoff:** 2024-09-30
**Context (API):** 400K tokens | **Max output:** 128K tokens

### Key behaviors

- Default reasoning effort is `none` (fast, "non-reasoning-like" behavior)
- Supported `reasoning.effort` values include `none`, `low`, `medium`, and `high`
- More steerable in **personality, tone, and formatting** than GPT-5
- Better calibrated to prompt difficulty (fewer wasted tokens on easy prompts)

### Prompting: what actually works best

**1) "None" mode = GPT-4o-style prompting**
When `reasoning.effort="none"`, many classic prompt techniques work well again:
- Few-shot examples (when you need strict style/format imitation)
- High-quality tool descriptions
- Concrete output length clamps

**2) Persistence and completeness**
On longer agentic tasks, add an explicit rule:
"Keep going until the user's request is completely resolved; don't stop early."

**3) Persona is helpful -- but don't confuse tone with capability**
GPT-5.1 responds well to a clear persona, but persona alone won't "add knowledge."
Use persona for tone/communication style; use explicit constraints + evals for correctness.

### Tools: `apply_patch` and `shell`

GPT-5.1 is post-trained on:
- `apply_patch` (structured diffs for file edits; reduces patch failure rates vs DIY JSON tools)
- `shell` (plan-execute loop via controlled command execution)

### When to prefer GPT-5.1 vs GPT-5.2

- Choose **GPT-5.1** if you want lower cost and you're already getting high quality with your prompt suite.
- Choose **GPT-5.2** if you need stronger instruction following, better tool reliability, improved vision, compaction, and the best all-around performance.

**Sources:**
- GPT-5.1 model info: https://platform.openai.com/docs/models/gpt-5-1
- GPT-5.1 Prompting Guide (Cookbook): https://cookbook.openai.com/examples/gpt-5/gpt-5-1_prompting_guide
- OpenAI API Changelog (5.1 defaults to `none`): https://platform.openai.com/docs/changelog

---

## GPT-4o

**Context:** 128K tokens
**Best for:** Execution tasks, speed-sensitive applications
**Status:** Retired from ChatGPT as of February 13, 2026. Still available via API but superseded by GPT-5.x.

### Key Behaviors

- More literal instruction following than GPT-4
- Requires explicit specification (implicit rules not inferred)
- Highly steerable with single sentences

### Prompting Patterns

**Use delimiters:**
```python
prompt = """
Summarize the text below as a bullet point list.

Text: \"\"\"
{text_input}
\"\"\"
"""
```

**Be specific about format:**
```
"Use a 3 to 5 sentence paragraph to describe this product."
```

**Say what TO do:**
```
# Don't
"DO NOT ASK USERNAME OR PASSWORD"

# Do
"Refer the user to www.example.com/help instead of asking for PII"
```

### Agentic Prompting

Include these reminders for agentic behavior:
```
# Persistence
Keep going until the user's query is completely resolved.

# Tool Usage
If unsure about content, use tools to gather information. Do NOT guess.

# Planning (optional)
Plan extensively before each function call.
```

---

## o1/o3 Reasoning Models

**What they are:** OpenAI's "o-series" reasoning models are trained to think longer and harder about ambiguous, multi-step problems. They behave differently from GPT "workhorse" models.

### Prompting rules of thumb (from OpenAI guidance)

- **Keep prompts simple and direct.** These models do best with high-level guidance and clear success criteria.
- **Avoid chain-of-thought prompting** ("think step by step", "show your reasoning"). They already reason internally.
- **Try zero-shot first.** Add a *small* number of examples only if you need strict formatting behavior, and ensure examples match instructions precisely.
- **Use delimiters** (headings, XML tags, fenced blocks) to separate task, context, and constraints.
- **Be explicit about constraints** (budget, time, scope, acceptance criteria).

### Developer messages and formatting

- In the API, reasoning models support **developer messages** (instead of "system" messages) to align with the model-spec chain of command.
- Starting with `o1-2024-12-17`, reasoning models avoid Markdown by default. If you *want* Markdown, include **`Formatting re-enabled`** on the first line of your developer message.

### Tool-heavy / agentic workflows

- Prefer the **Responses API** for reasoning models. For complex multi-tool workflows, use `store: true` and carry forward conversation state via `previous_response_id` or by replaying prior output items.
- OpenAI recommends including reasoning items around function calls (at minimum, between the last function call and the previous user message) so the model doesn't "restart" its reasoning when you respond to tool outputs.

### When to use o-series vs GPT-5.x

- Use **o-series** when accuracy/reliability on ambiguous decisions matters more than latency (planning, policy/compliance judgments, dense document reasoning).
- Use **GPT-5.2 / GPT-5.1** when you need fast execution, high-quality writing/coding, or you want to tune reasoning effort per call.

**Note:** GPT-4o, o4-mini, and other models were retired from ChatGPT on Feb 13, 2026. o3 and o4-mini remain available via API. Deep research variants (`o3-deep-research`, `o4-mini-deep-research`) are also available.

**Sources:**
- Reasoning best practices: https://platform.openai.com/docs/guides/reasoning-best-practices
- Reasoning models guide: https://platform.openai.com/docs/guides/reasoning
- Model retirements: https://openai.com/index/introducing-o3-and-o4-mini/

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| GPT-5.2 | Light (ask for brief plan) | Helpful in `none`/`low`; less needed at `medium+` | Yes (system/developer) |
| GPT-5.1 | Light (ask for brief plan) | Helpful in `none`/`low`; less needed at `medium+` | Yes (system/developer) |
| GPT-4o | Manual | Helpful | Yes |
| o1/o3 | **NEVER** | **Hurts** | Developer role |

---

*Last updated: February 2026*
