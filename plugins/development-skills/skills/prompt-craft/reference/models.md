# Model-Specific Prompting Guide

Prompting techniques that work on one model may fail on another. This guide covers model-specific best practices.

## Table of Contents

### Claude (Anthropic)
- [Claude 4.x Family](#claude-4x-family)
- [Claude Opus 4.5](#claude-opus-45)

### OpenAI
- [GPT-5.2](#gpt-52)
- [GPT-5.1](#gpt-51)
- [GPT-4o](#gpt-4o)
- [o1/o3 Reasoning Models](#o1o3-reasoning-models)

### DeepSeek
- [DeepSeek V3](#deepseek-v3)
- [DeepSeek R1](#deepseek-r1)

### Google
- [Gemini 2.0](#gemini-20)

### Moonshot
- [Kimi K2](#kimi-k2)

### Alibaba
- [Qwen 2.5](#qwen-25)

### Quick Reference
- [Critical Differences Table](#critical-differences-table)
- [Reasoning Models Warning](#reasoning-models-warning)

---

# Claude (Anthropic)

## Claude 4.x Family

### Key Changes from Claude 3.x

| Aspect | Claude 3.x | Claude 4.x |
|--------|------------|------------|
| Verbosity | Naturally verbose | Concise by default |
| Tool calling | Conservative | Aggressive parallel execution |
| Instructions | Flexible interpretation | Precise, literal following |
| Action vs suggestion | Mixed | Tends toward suggestion |

### Prompting Adjustments

**Be directive:** Claude 4.x tends toward suggestion over action.
```
# Don't
"Can you suggest some changes to improve this function?"

# Do
"Change this function to handle edge cases. Implement the changes."
```

**Request detail explicitly:** Concise by default.
```
"Include as many relevant features as possible. Go beyond basics."
```

**Explain why:** Context helps Claude follow constraints better.
```
# Don't
"NEVER use ellipses in responses."

# Do
"Never use ellipses—they don't render in our text-to-speech system."
```

**Use positive framing:** Tell what TO do.
```
# Don't
"Do not use markdown formatting."

# Do
"Format your response as smoothly flowing prose paragraphs."
```

### Tool Use Notes

- Sonnet 4.5 aggressively executes parallel tool calls
- Overtriggering is more common than undertriggering
- Use balanced prompting (not "MUST use tool")

## Claude Opus 4.5

**Released:** November 24, 2025
**Context:** 200K tokens
**Strengths:** Coding, agentic workflows, computer use

### Specific Guidance

**Extended thinking:** Enable for complex STEM, coding, constraint optimization.
```
# Use high-level direction, not prescriptive steps
"Analyze this problem thoroughly before providing your solution."

# Avoid prescriptive steps that limit model creativity
```

**Agentic workflows:** For long-running agents, use two-agent pattern:
1. Initializer agent (runs once, establishes structure)
2. Coding agent (operates across sessions)

**State persistence:** Maintain across sessions:
- `features.json` for feature tracking (JSON > Markdown for stability)
- `progress.txt` for session logging
- Git commits for checkpoints

**API note:** Use `temperature` OR `top_p`, not both (causes errors in 4.5).

---

# OpenAI


## GPT-5.2

**Status:** Current flagship (replaces GPT-5.1)  
**Best for:** Complex reasoning, broad world knowledge, agentic/tool-heavy workflows, and code-heavy tasks  
**Knowledge cutoff:** 2025-08-31  
**Context (API):** 400K tokens • **Max output:** 128K tokens  
**Chat model:** `gpt-5.2-chat-latest` (128K context • 16,384 max output)

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
- Increase gradually (`medium` → `high` → `xhigh`) for harder reasoning.  
- With `none`, prompting matters more: explicitly ask for a *brief plan / outline* before the final answer.

**2) `text.verbosity` (response length / “how much to say”)**  
- Values: `low`, `medium`, `high` (default: `medium`).  
- Use this instead of trying to fight verbosity purely with prompting.

**3) Reasoning summaries (`reasoning.summary`)**  
- GPT‑5.2 can return concise summaries of its reasoning (useful for audits / traceability without exposing full hidden reasoning).

**4) Compaction (`POST /v1/responses/compact`)**  
- Use for long-running workflows (many turns / tool calls) to extend effective context.  
- Output is **opaque/encrypted**: treat as “state to continue with”, not data to parse.

### Prompting patterns that reliably improve results

**Output-shape + length clamps (high ROI)**  
Give concrete constraints: bullet caps, section names, snippet limits, etc.  
(Works especially well for enterprise agents and coding assistants.)

**Scope-drift prevention (especially UI/front-end)**  
GPT-5.2 is strong at structured code but may “helpfully” add features/design.  
Explicitly forbid extras: “Implement ONLY what I asked. No embellishments.”

**Long-context handling**  
For big inputs, force re-grounding:
- Summarize key relevant sections first
- Restate constraints (jurisdiction/date range/etc.)
- Anchor claims to sections (“In the Data Retention section…”)

**Ambiguity guardrails**  
If underspecified: ask 1–3 clarifying questions *or* give 2–3 interpretations with labeled assumptions.  
Never invent exact figures/links when uncertain; prefer “based on provided context…”

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

**Sources (primary):**
- OpenAI “Using GPT-5.2 / latest model” docs: https://platform.openai.com/docs/guides/latest-model  
- GPT-5.2 Prompting Guide (Cookbook): https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide  
- OpenAI Models pages: https://platform.openai.com/docs/models  
- Responses API + compaction reference: https://platform.openai.com/docs/api-reference/responses/compact  

---

## GPT-5.1

**Status:** Previous flagship (still useful; cheaper than 5.2 in many setups)  
**Best for:** Coding + agentic workflows where you want **configurable reasoning** and strong steerability  
**Knowledge cutoff:** 2024-09-30  
**Context (API):** 400K tokens • **Max output:** 128K tokens

### Key behaviors

- Default reasoning effort is `none` (fast, “non-reasoning-like” behavior)
- Supported `reasoning.effort` values include `none`, `low`, `medium`, and `high`
- More steerable in **personality, tone, and formatting** than GPT-5
- Better calibrated to prompt difficulty (fewer wasted tokens on easy prompts)

### Prompting: what actually works best

**1) “None” mode ≈ GPT-4o-style prompting**  
When `reasoning.effort="none"`, many classic prompt techniques work well again:
- Few-shot examples (when you need strict style/format imitation)
- High-quality tool descriptions
- Concrete output length clamps

**2) Persistence and completeness**  
On longer agentic tasks, add an explicit rule:  
“Keep going until the user’s request is completely resolved; don’t stop early.”

**3) Persona is helpful — but don’t confuse tone with capability**  
GPT-5.1 responds well to a clear persona, but persona alone won’t “add knowledge.”  
Use persona for tone/communication style; use explicit constraints + evals for correctness.

### Tools: `apply_patch` and `shell`

GPT‑5.1 is post‑trained on:
- `apply_patch` (structured diffs for file edits; reduces patch failure rates vs DIY JSON tools)
- `shell` (plan-execute loop via controlled command execution)

### When to prefer GPT-5.1 vs GPT-5.2

- Choose **GPT‑5.1** if you want lower cost and you’re already getting high quality with your prompt suite.
- Choose **GPT‑5.2** if you need stronger instruction following, better tool reliability, improved vision, compaction, and the best all-around performance.

**Sources (primary):**
- GPT-5.1 model info: https://platform.openai.com/docs/models/gpt-5-1  
- GPT-5.1 Prompting Guide (Cookbook): https://cookbook.openai.com/examples/gpt-5/gpt-5-1_prompting_guide  
- OpenAI API Changelog (5.1 defaults to `none`): https://platform.openai.com/docs/changelog  

---

## GPT-4o

**Context:** 128K tokens
**Best for:** Execution tasks, speed-sensitive applications

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

## o1/o3 Reasoning Models

**What they are:** OpenAI’s “o‑series” reasoning models are trained to think longer and harder about ambiguous, multi-step problems. They behave differently from GPT “workhorse” models.  

### Prompting rules of thumb (from OpenAI guidance)

- **Keep prompts simple and direct.** These models do best with high-level guidance and clear success criteria.
- **Avoid chain-of-thought prompting** (“think step by step”, “show your reasoning”). They already reason internally.
- **Try zero-shot first.** Add a *small* number of examples only if you need strict formatting behavior, and ensure examples match instructions precisely.
- **Use delimiters** (headings, XML tags, fenced blocks) to separate task, context, and constraints.
- **Be explicit about constraints** (budget, time, scope, acceptance criteria).

### Developer messages and formatting

- In the API, reasoning models support **developer messages** (instead of “system” messages) to align with the model-spec chain of command.
- Starting with `o1-2024-12-17`, reasoning models avoid Markdown by default. If you *want* Markdown, include **`Formatting re-enabled`** on the first line of your developer message.

### Tool-heavy / agentic workflows

- Prefer the **Responses API** for reasoning models. For complex multi-tool workflows, use `store: true` and carry forward conversation state via `previous_response_id` or by replaying prior output items.
- OpenAI recommends including reasoning items around function calls (at minimum, between the last function call and the previous user message) so the model doesn’t “restart” its reasoning when you respond to tool outputs.

### When to use o-series vs GPT-5.x

- Use **o-series** when accuracy/reliability on ambiguous decisions matters more than latency (planning, policy/compliance judgments, dense document reasoning).
- Use **GPT‑5.2 / GPT‑5.1** when you need fast execution, high-quality writing/coding, or you want to tune reasoning effort per call.

**Sources (primary):**
- Reasoning best practices: https://platform.openai.com/docs/guides/reasoning-best-practices  
- Reasoning models guide: https://platform.openai.com/docs/guides/reasoning  


# DeepSeek

## DeepSeek V3

**Architecture:** 671B MoE (37B active)
**Context:** 128K tokens
**Best for:** General chat, code generation

### Temperature Settings

| Use Case | Temperature |
|----------|-------------|
| Coding / Math | 0.0 |
| Data Analysis | 1.0 |
| General Chat | 1.3 |
| Creative Writing | 1.5 |

### Prompting

Standard prompting works. System prompts supported.

```python
messages = [
    {"role": "system", "content": "You are an expert Python developer."},
    {"role": "user", "content": "Write a function to..."}
]
```

## DeepSeek R1

**Critical:** Requires FUNDAMENTALLY different prompting.

### What NOT to Do

```
DON'T: Use system prompts
DON'T: Provide few-shot examples (degrades performance)
DON'T: Trigger chain-of-thought manually (automatic)
DON'T: Set temperature/top_p (not supported for R1)
```

### What TO Do

**All instructions in user message:**
```python
messages = [
    {
        "role": "user",
        "content": """
You are an expert Python developer.

## Task
Write a function to validate email addresses.

## Requirements
- Handle edge cases
- Return boolean
- Include docstring

## Output Format
Provide only the Python code.
"""
    }
]
```

**Multi-turn handling:**
```python
# IMPORTANT: Strip reasoning_content between turns
for message in conversation_history:
    if 'reasoning_content' in message:
        del message['reasoning_content']  # Required to avoid 400 errors
```

### R1-Specific Tips

- For math: Include "Put your final answer within `\boxed{}`"
- Use `temperature=0.6` (official recommendation)
- If reasoning bypassed: "Start with the `<think>` tag"

---

# Google

## Gemini 2.0

**Context:** 1M tokens
**Strengths:** Multimodal, long context, native tool use

### Key Principle: Query at END

For long contexts, place the question LAST:
```
[All context / documents]
...
Based on the information above, answer: [question]
```

### Temperature

| Model | Temperature |
|-------|-------------|
| Gemini 2.0 | 0 works for deterministic |
| Gemini 2.5 | 0 works for deterministic |
| Gemini 3.0 | 1.0 (required default) |

### Multimodal Prompting

**Images:** Place text prompt AFTER image.
```python
contents = [
    image_part,  # Image first
    "Describe what you see"  # Text after
]
```

### Grounding

Enable Google Search for factual accuracy:
```python
response = model.generate_content(
    "What happened in tech news today?",
    tools=[{"google_search": {}}]
)
```

### Key Behaviors

- **No negative examples:** Don't show "what NOT to do"
- **Thinking mode:** Use `thinkingBudget` for complex tasks
- **Lost-in-middle:** Still applies even with 1M context
- **Object detection:** Returns 0-1000 normalized coordinates

---

# Moonshot

## Kimi K2

**Architecture:** 1T MoE (32B active)
**Context:** 128K-256K tokens
**Design:** Agentic-first

### Critical Settings

```python
temperature = 0.6  # Official recommendation
system_prompt = "You are Kimi, an AI assistant created by Moonshot AI."
```

### Prompting Style

**Use goal-oriented prompts (not step-by-step):**
```
# Don't
"Step 1: Read the file. Step 2: Parse JSON. Step 3: Extract users..."

# Do
"Count the number of users in this JSON file and return the total."
```

### Known Issues

| Issue | Mitigation |
|-------|------------|
| Instruction drift after ~900 words | Put critical constraints EARLY |
| Formatting inconsistencies in long outputs | Use explicit section markers |
| Overthinking simple tasks | Request brevity explicitly |
| Over-confident paraphrasing | Ask for direct quotes |

### Long Context

- Normal speed < 100K tokens
- Speed drops 100K-256K tokens
- For very long: add executive summary in final user message

### K2-Thinking Variant

```python
temperature = 1.0  # Different from Instruct!
max_tokens = 16000  # Minimum for reasoning + output
min_p = 0.01
```

---

# Alibaba

## Qwen 2.5

**Sizes:** 0.5B - 72B (open weights)
**Context:** 128K tokens
**Variants:** Qwen2.5, Qwen2.5-Coder, Qwen2.5-Math, Qwen-Max (API)

### Chat Template (Critical)

Qwen uses ChatML format. Always use the tokenizer:
```python
# CORRECT
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

# NEVER manually construct ChatML tokens
```

### Sampling Parameters

**General:**
```python
{
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 20,
    "repetition_penalty": 1.05
}
```

**Code (Qwen-Coder):**
```python
{
    "temperature": 0.2,  # Lower for determinism
    "top_p": 0.9,
    "repetition_penalty": 1.05
}
```

### Key Differentiators

- **Bilingual strength:** Native Chinese + English (no quality penalty for Chinese)
- **29+ languages:** Strong multilingual without English bias
- **Open weights:** Apache 2.0 license (except 3B Coder)

### Default System Prompt

```
"You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
```

### Notes

- `repetition_penalty: 1.05` recommended to prevent repetition
- Qwen-Coder specialized for code; use base for non-code
- Qwen2.5-Math: English and Chinese math only (not general use)

---

# Quick Reference

## Critical Differences Table

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| Claude 4.x | Manual | Helpful | Yes |
| GPT-4o | Manual | Helpful | Yes |
| GPT-5.2 | Light (ask for brief plan) | Helpful in `none`/`low`; less needed at `medium+` | Yes (system/developer) |
| GPT-5.1 | Light (ask for brief plan) | Helpful in `none`/`low`; less needed at `medium+` | Yes (system/developer) |
| o1/o3 | **NEVER** | **Hurts** | Developer role |
| DeepSeek V3 | Manual | Helpful | Yes |
| DeepSeek R1 | **NEVER** | **Hurts** | **NO** |
| Gemini 2.0 | Manual/Thinking | Helpful (no negatives) | Yes |
| Kimi K2 | Automatic (Thinking) | Varies | Goal-oriented |
| Qwen 2.5 | Manual | Helpful | Yes |
## Reasoning Models Warning

There are (at least) two “reasoning styles” you’ll run into:

### 1) Always-thinking reasoning models (o-series, DeepSeek R1, Kimi Thinking)
Examples: **o1/o3**, DeepSeek R1, Kimi K2-Thinking

For these models:
1. **Avoid chain-of-thought prompts** (“think step by step”, “explain your reasoning”) — often unnecessary and can hurt performance
2. **Try zero-shot first**; add few-shot only if needed and tightly aligned
3. **Keep prompts simple and direct**
4. Prefer the **Responses API** for tool-heavy flows; carry forward conversation state

### 2) Tunable reasoning (GPT-5.1 / GPT-5.2)
These models can run with **`reasoning.effort="none"`** (fast, “workhorse-like”), or spend more compute at `medium`/`high`/`xhigh`.

- In `none`: classic prompt engineering (few-shot, detailed schemas) works well.
- In `medium+`: reduce prompt micromanagement; tighten *success criteria + output shape* instead.

## Model Selection Guide

| Need | Best Choice |
|------|-------------|
| Complex reasoning | GPT‑5.2, o1/o3, DeepSeek R1 |
| Code generation | Claude Opus 4.5, DeepSeek, Qwen-Coder |
| Speed + cost | Gemini Flash, DeepSeek V3, Kimi K2 |
| Long context | GPT‑5.2/5.1 (400K), Gemini (1M), Kimi (256K), Claude (200K) |
| Multilingual | Qwen, Kimi |
| Agentic workflows | Claude 4.x, Kimi K2 |
| Multimodal | Gemini, GPT-4o |

---

*Last updated: January 2026*
*Add new models by appending sections and updating TOC*
