# Model-Specific Prompting Guide

Prompting techniques that work on one model may fail on another. This guide covers model-specific best practices.

## Table of Contents

### Claude (Anthropic)
- [Claude 4.x Family](#claude-4x-family)
- [Claude Opus 4.5](#claude-opus-45)

### OpenAI
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

**Critical:** These models require DIFFERENT prompting than GPT-4o.

### What NOT to Do

| Standard Models | Reasoning Models |
|-----------------|------------------|
| "Think step by step" | **NEVER** - hurts performance |
| Few-shot examples help | **Often degrades** performance |
| System messages | Use **developer** messages |
| Detailed guidance | Keep prompts **simple** |

### Correct Approach

**Keep prompts simple:**
```python
# Don't
"Let's think step by step and explain your reasoning..."

# Do
"Solve this problem: [problem]"
```

**Use developer role:**
```python
response = client.chat.completions.create(
    model="o3",
    messages=[
        {"role": "developer", "content": "You are a legal analyst."},
        {"role": "user", "content": "Review this contract..."}
    ]
)
```

**Enable markdown explicitly:**
```
Formatting re-enabled

[Rest of developer message...]
```

**Reasoning effort (o3-mini, o4-mini):**
```python
response = client.chat.completions.create(
    model="o3-mini",
    reasoning_effort="medium"  # "low", "medium", or "high"
)
```

### Function Calling

- Use `strict: True` for schema enforcement
- Keep function count under 20
- Don't make model fill values you already have

---

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
| o1/o3 | **NEVER** | **Hurts** | Developer role |
| DeepSeek V3 | Manual | Helpful | Yes |
| DeepSeek R1 | **NEVER** | **Hurts** | **NO** |
| Gemini 2.0 | Manual/Thinking | Helpful (no negatives) | Yes |
| Kimi K2 | Automatic (Thinking) | Varies | Goal-oriented |
| Qwen 2.5 | Manual | Helpful | Yes |

## Reasoning Models Warning

**o1/o3, DeepSeek R1, Kimi K2-Thinking** have built-in reasoning.

For these models:
1. **Do NOT use chain-of-thought prompts** - they hurt performance
2. **Skip few-shot examples** - often degrades quality
3. **Keep prompts simple and direct**
4. **Let the model reason internally**

The prompting that makes standard models better makes reasoning models worse.

## Model Selection Guide

| Need | Best Choice |
|------|-------------|
| Complex reasoning | o1/o3, DeepSeek R1 |
| Code generation | Claude Opus 4.5, DeepSeek, Qwen-Coder |
| Speed + cost | Gemini Flash, DeepSeek V3, Kimi K2 |
| Long context | Gemini (1M), Kimi (256K), Claude (200K) |
| Multilingual | Qwen, Kimi |
| Agentic workflows | Claude 4.x, Kimi K2 |
| Multimodal | Gemini, GPT-4o |

---

*Last updated: November 2025*
*Add new models by appending sections and updating TOC*
