# Model-Specific Prompting Guide

Prompting techniques that work on one model may fail on another. This guide summarizes *model-family-specific* prompting + integration gotchas (model IDs, “thinking” knobs, context limits, and common failure modes).

**Last updated:** 2025-12-23 (Europe/Berlin)

---

## Contents

- [Claude (Anthropic)](#claude-anthropic)
  - [Claude Sonnet 4.5](#claude-sonnet-45)
  - [Claude Opus 4.5](#claude-opus-45)
  - [Claude 4.x family defaults](#claude-4x-family-defaults)
- [OpenAI](#openai)
  - [GPT-5.2](#gpt-52)
  - [GPT-5.2 Chat](#gpt-52-chat)
  - [GPT-5.2 Pro](#gpt-52-pro)
  - [o1/o3 reasoning models](#o1o3-reasoning-models)
  - [GPT-4o](#gpt-4o)
- [Google](#google)
  - [Gemini 3 Pro / Flash](#gemini-3-pro--flash)
  - [Gemini 3 gotcha: thought signatures](#gemini-3-gotcha-thought-signatures)
- [Other families](#other-families)
  - [DeepSeek](#deepseek)
  - [Kimi (Moonshot)](#kimi-moonshot)
  - [Qwen (Alibaba)](#qwen-alibaba)
  - [xAI (Grok)](#xai-grok)
- [Quick reference](#quick-reference)

---

# Claude (Anthropic)

## Claude Sonnet 4.5

**Anthropic API model ID:** `claude-sonnet-4-5-20250929`

**What it’s best at**
- Agentic coding + long-horizon tool workflows
- “Computer use” / tool-heavy automation
- Long-context reasoning *when you manage context deliberately*

**Context**
- **Standard:** 200K tokens
- **Long context (beta):** 1M tokens via beta header `context-1m-2025-08-07` (availability depends on usage tier / custom limits)

**Prompting style that works**
- Be **directive** (ask for implementation, not suggestions).
- Make success criteria **testable**: “Return a diff”, “Return JSON matching schema”, “Include commands and expected outputs”.
- For tool use: set a **budget + stop rule**.

Example:
```text
You may use up to 3 tool calls.
Stop once you have enough evidence to answer confidently.
If you still lack evidence, say exactly what you need next.
Output: a single markdown checklist.
```

**Integration gotcha (Claude 4.5 migration)**
- Do **not** send both `temperature` and `top_p` in the same request when migrating to Claude 4.5 models.

---

## Claude Opus 4.5

**Anthropic API model ID:** `claude-opus-4-5-20251101`

**What it’s best at**
- Highest-precision analysis and coding in the Claude line
- Hard planning / constraint optimization when you want maximal capability

**Context**
- **Standard:** 200K tokens

**Unique knob: `effort` (beta, Opus 4.5 only)**
- Lets you trade response thoroughness vs token efficiency with a single parameter.
- Requires beta header `effort-2025-11-24`.

**Prompting style that works**
- Prefer **goal + constraints + output format** over step-by-step micromanagement.
- If you need depth, say so explicitly:
```text
Optimize for correctness and completeness over brevity.
If there’s ambiguity, list assumptions and proceed minimally.
```

---

## Claude 4.x family defaults

These are common across many Claude 4.x models:

- Claude 4.x tends to be **more concise by default** → request detail explicitly.
- Claude 4.x follows instructions **literally** → specify format, scope, and “done” conditions.
- Claude 4.x can be **eager with tools** in agent setups → give stricter tool criteria if needed.

---

# OpenAI

## GPT-5.2

**OpenAI API model ID:** `gpt-5.2`

**What it’s best at**
- Coding + agentic workflows
- Long-context projects where you can keep a stable plan and compact state

**Context**
- **Context window:** 400,000 tokens
- **Max output:** 128,000 tokens
- **Knowledge cutoff:** 2025-08-31

**Prompting style that works**
- Use **clear sections** (TASK / CONSTRAINTS / INPUT / OUTPUT FORMAT).
- Demand an **output shape** (schema, checklist, table) to reduce drift.
- Repeat critical constraints at the end (mitigates “lost in the middle”).

**Knobs to know**
- `reasoning.effort`: control internal work (`low|medium|high|xhigh` in 5.2 family).
- `text.verbosity`: steer detail (`low|medium|high`).

**Long-running agents: compaction**
- Prefer **compaction** (summarize/condense state) over replaying full histories every turn.

---

## GPT-5.2 Chat

**OpenAI API model ID:** `gpt-5.2-chat-latest`  
Use this when you specifically want the snapshot currently used in ChatGPT.

**Context**
- **Context window:** 128,000 tokens
- **Max output:** 16,384 tokens
- **Knowledge cutoff:** 2025-08-31

---

## GPT-5.2 Pro

**OpenAI API model ID:** `gpt-5.2-pro`

**Important differences**
- Available in the **Responses API only**.
- Designed for tougher problems; some requests can take longer.
- Supports `reasoning.effort` = `medium|high|xhigh`.
- If you hit timeouts, use **background mode**.

**Context**
- **Context window:** 400,000 tokens
- **Max output:** 128,000 tokens

---

## o1/o3 reasoning models

These models are *reasoning-native*; prompting them like GPT-4o often makes them worse.

**Do**
- Give the task once, clearly.
- Specify output format.
- Keep instructions minimal.

**Avoid**
- “Think step by step” / “show your reasoning”
- Large few-shot blocks unless you’ve validated they help
- Over-prescribing how to think

---

## GPT-4o

Best when you want fast, literal instruction following.

**Prompting style that works**
- Be explicit; don’t rely on implied rules.
- Use delimiters for long inputs.
- Specify format/length/structure.

Example:
```text
Summarize the text below into exactly 5 bullets.
Each bullet must be <= 18 words.
Text:
"""
...
"""
```

---

# Google

## Gemini 3 Pro / Flash

**Gemini API model IDs**
- `gemini-3-pro-preview`
- `gemini-3-flash-preview`

**Token limits (Preview)**
- **Input:** 1,048,576 tokens
- **Output:** 65,536 tokens
- **Knowledge cutoff (model card):** 2025-01

**Thinking control**
Gemini 3 uses *thinking levels* (not budgets):
- **Gemini 3 Pro:** `low`, `high`
- **Gemini 3 Flash:** `minimal`, `low`, `medium`, `high`
If not specified, Gemini 3 defaults to `high`.

**Prompting style that works**
- Put **context first**, **task last** (Gemini is sensitive to ordering).
- Use strict schemas for structured output and function calling.

---

## Gemini 3 gotcha: thought signatures

If you use **function calling / tools** with Gemini 3, you must **circulate thought signatures** across turns exactly as received. If you omit them, you can get validation errors (and/or degraded reasoning depending on the endpoint).

Practical rule:
- Treat thought signatures as opaque tokens.
- Echo them back unchanged in conversation history.

---

# Other families

## DeepSeek

General guidance:
- Standard prompting works well.
- Use structured output (JSON) if you need reliable parsing.
- Keep tool schemas tight; validate tool inputs.

## Kimi (Moonshot)

General guidance:
- Works best with **goal-oriented** prompts.
- Avoid “Step 1 / Step 2 / Step 3” micromanagement.
- Specify output format and success criteria.

## Qwen (Alibaba)

General guidance:
- Strong multilingual + structured output compliance.
- Use explicit schemas and examples for tricky formatting.
- For code, include test cases and edge constraints.

## xAI (Grok)

**What it's best at**
- Agentic workflows and tool-calling tasks
- Long-context tasks (Grok 4.1 Fast supports a 2M context window)

**Prompting style that works**
- Use a **detailed system prompt** with explicit task goals and edge cases.
- Provide **structured context** using XML tags or Markdown headings.
- Keep **prompt history stable** across tool loops to maximize cache hits and speed.

**Tool-calling guidance**
- In streaming mode, **function calls are returned in a single chunk**, not interleaved.
- If tool calls are required, instruct the model to **use tools via the tool interface only** (never emit tool-call markup in normal text).

---

# Quick reference

## What to pick (common scenarios)

| Need | Best starting choice |
|------|-----------------------|
| Best agentic coding + long context | GPT-5.2 |
| Highest precision (willing to wait) | GPT-5.2 Pro |
| Match ChatGPT’s current behavior | GPT-5.2 Chat (`-chat-latest`) |
| 1M-token ingestion + tool workflows | Gemini 3 Pro/Flash (Preview) |
| Claude-style agent workflows | Claude Sonnet 4.5 |
| Claude maximum capability | Claude Opus 4.5 |
| Reasoning-native minimal prompting | o1/o3 (if you’re using them) |

## Biggest “gotchas” checklist

- **Gemini 3 + tools:** always round-trip **thought signatures**.
- **Claude 4.5 migration:** don’t send **both** `temperature` and `top_p`.
- **GPT-5.2 Pro:** Responses API only; consider background mode for long tasks.
- **Reasoning-native models:** don’t demand chain-of-thought; keep prompts simple.

---
