# OpenAI Models Research -- February 2026

> Research date: 2026-02-21
> Purpose: Comprehensive model reference for prompt-craft skill update
> Status: RAW RESEARCH -- to be distilled into `openai.md`

---

## Table of Contents

1. [GPT-5.2 (Current Flagship)](#gpt-52-current-flagship)
2. [GPT-5.1 (Previous Flagship)](#gpt-51-previous-flagship)
3. [GPT-5 (Base)](#gpt-5-base)
4. [GPT-5 Mini](#gpt-5-mini)
5. [GPT-5 Nano](#gpt-5-nano)
6. [o3 (Reasoning)](#o3-reasoning-model)
7. [o4-mini (Reasoning)](#o4-mini-reasoning-model)
8. [o3-pro](#o3-pro)
9. [o3-mini (Legacy Reasoning)](#o3-mini-legacy-reasoning)
10. [Model Retirements](#model-retirements)
11. [Pricing Summary Table](#pricing-summary-table)

---

## GPT-5.2 (Current Flagship)

### Specs

| Field | Value |
|-------|-------|
| Model ID (API) | `gpt-5.2` |
| Chat variant | `gpt-5.2-chat-latest` (128K context, 16K max output) |
| Pro variant | `gpt-5.2-pro` |
| Codex variant | `gpt-5.2-codex` |
| Release date | December 11, 2025 |
| Context window | 400K tokens (API); 128K (chat variant) |
| Max output tokens | 128K tokens (API); 16,384 (chat variant) |
| Knowledge cutoff | August 31, 2025 |
| Modality | Text + Image input; Text output |
| Capabilities | Vision, function calling, reasoning, JSON schema, system messages, prompt caching |

### Pricing (Standard tier, per 1M tokens)

| Type | Cost |
|------|------|
| Input | $1.75 |
| Output | $14.00 |
| Cached input | $0.175 |
| Batch input | $0.875 |
| Batch output | $7.00 |
| Priority input | $3.50 |
| Priority output | $28.00 |

GPT-5.2 Pro pricing: $21.00 input / $168.00 output per 1M tokens.

### Variants

| Variant | Use Case | Notes |
|---------|----------|-------|
| `gpt-5.2` | Complex reasoning, agentic tasks, code | Full 400K context, all reasoning levels |
| `gpt-5.2-pro` | Maximum analytical depth | Supports `xhigh` reasoning for top-quality end-to-end execution |
| `gpt-5.2-chat-latest` | ChatGPT "Instant" mode | Reduced context (128K) and output (16K) for faster responses |
| `gpt-5.2-codex` | Interactive coding, full-spectrum coding tasks | Released Jan 2026 |

### Key Improvements vs GPT-5.1

- 38% fewer errors on complex tasks
- 70.9% expert-level performance on GDPval (vs 38.8% for GPT-5 base)
- New August 2025 knowledge cutoff (vs Sep 30, 2024 for GPT-5.1)
- Better token efficiency on medium-to-complex tasks
- Cleaner formatting with less unnecessary verbosity
- Stronger multimodal understanding (especially vision)
- Response compaction for extended context beyond 400K tokens
- `xhigh` reasoning effort level for maximum analytical depth
- 90% cached input discount ($0.175 vs $1.75)
- Improved tool calling reliability (Tau2 Telecom benchmark: 98.7%)

### Benchmark Highlights

| Benchmark | Score |
|-----------|-------|
| GPQA Diamond | ~92-93% |
| HLE | 45% |
| AIME 2025 | 100% |
| MATH | 98% |
| SWE-Bench Verified | 80.0% |
| SWE-Bench Pro | 55.6% |
| HumanEval | 95% |
| LiveCodeBench | 80% |
| IFEval | 95% |
| ARC-AGI-2 | 52.9% |
| ARC-AGI-1 (Pro, xhigh) | 90.5% |
| Terminal-Bench | 60% |
| GDPval (knowledge work) | 70.9% |
| FrontierMath | 40.3% |

### Reasoning Effort Settings

GPT-5.2 supports six `reasoning.effort` levels:

| Level | Behavior | When to Use |
|-------|----------|-------------|
| `none` | **DEFAULT.** Fast, low-latency. No internal reasoning. | Simple tasks, chat, classification. GPT-4o replacement. |
| `minimal` | Very light reasoning | Slightly harder than trivial tasks |
| `low` | Basic reasoning with moderate token usage | Straightforward analysis |
| `medium` | Balanced reasoning depth | Most production workloads |
| `high` | Extensive reasoning analysis | Complex coding, multi-step planning |
| `xhigh` | Maximum reasoning (Pro variant) | Critical decisions, research-grade analysis |

IMPORTANT: Temperature, top_p, and logprobs parameters ONLY work with `reasoning.effort: "none"`. At all other levels, sampling parameters are ignored.

### Text Verbosity Control

Three configurable `text.verbosity` levels:

| Level | Behavior | Example Use |
|-------|----------|-------------|
| `low` | Concise, minimal explanation | SQL queries, yes/no answers, short code snippets |
| `medium` | **DEFAULT.** Balanced explanations | General-purpose responses |
| `high` | Thorough, detailed output | Document analysis, extensive code refactoring |

API usage:
```python
result = client.responses.create(
    model="gpt-5.2",
    input="Write a haiku about code.",
    reasoning={"effort": "low"},
    text={"verbosity": "low"},
)
```

### Compaction API

Endpoint: `POST /v1/responses/compact`

Purpose: Compresses prior conversation state for long-running workflows to extend effective context beyond 400K.

Key rules:
- Use after major milestones, NOT every turn
- Output is opaque/encrypted -- treat as continuation state, not data to parse
- Keep prompts functionally identical when resuming
- Monitor context usage proactively

```python
compacted_response = client.responses.compact(
    model="gpt-5.2",
    input=[user_prompt, assistant_response]
)
```

### Reasoning Summaries

`reasoning.summary` parameter returns concise summaries of internal reasoning. Useful for audits and traceability without exposing full hidden reasoning chain.

### Prompting Best Practices

**Key behavioral difference:** GPT-5.2 exhibits "more deliberate scaffolding" and "generally lower verbosity" than GPT-5.1. It has a "conservative grounding bias" favoring correctness and explicit reasoning.

**CTCO Framework** (Context -> Task -> Constraints -> Output):
1. Define context and role clearly
2. State the task explicitly
3. Set hard constraints (format, length, scope)
4. Specify output shape

**Output-shape + length clamps (high ROI):**
- Give concrete constraints: bullet caps, section names, snippet limits
- Simple yes/no: <=2 sentences
- Typical response: 3-6 sentences or <=5 bullets
- Complex multi-step: 1 overview paragraph + <=5 tagged bullets

**Scope-drift prevention:**
- "Implement EXACTLY and ONLY what the user requests"
- Forbid extra components, uncontrolled styling, invented colors/shadows
- Choose simplest valid interpretation for ambiguous instructions
- GPT-5.2 tends to "helpfully" add features/design -- explicitly forbid extras

**Long-context handling (>10K tokens input):**
- Force model to produce short internal outline of relevant sections
- Re-state user constraints explicitly before answering
- Anchor claims to source sections ("In the Data Retention section...")
- Quote or paraphrase fine details (dates, thresholds, clauses)

**Ambiguity guardrails:**
- Call out ambiguity explicitly
- Ask 1-3 precise clarifying questions OR present 2-3 labeled interpretations
- Use "Based on provided context..." instead of absolute claims
- Never fabricate exact figures, line numbers, or external references

**High-risk self-check pattern:**
- Scan for unstated assumptions
- Verify specific numbers are grounded in context
- Soften overly strong language ("always," "guaranteed")

### Tools & Agent Workflows

- Prefer **Responses API** for tool-heavy workflows; supports better conversation state handling
- Post-trained on `apply_patch` (structured diffs) and `shell` (local command execution)
- Supports **custom tools** with `type: custom` for freeform text inputs
- CFG (Context-Free Grammar) support for domain-specific output formats
- **Preambles**: GPT-5.2 generates explanations before invoking tools, outlining intent
- Parallel tool calls supported; describe tools crisply (1-2 sentences)
- After write operations: restate what changed, where (ID/path), validation performed
- Use `previous_response_id` to avoid re-reasoning across turns
- `allowed_tools` parameter to restrict available tool subset

### Migration Guide

| From | Recommended reasoning.effort |
|------|------|
| GPT-4o / GPT-4.1 | Start with `none` |
| GPT-5 | Preserve existing; convert `minimal` -> `none` |
| GPT-5.1 | Keep same setting; adjust only after evals show regressions |
| o3 | Try `medium` to start |

Steps:
1. Switch models, preserve prompts (test model change in isolation)
2. Pin reasoning_effort to match prior model's latency/depth profile
3. Run baseline evals
4. Tune only if regressions (use Prompt Optimizer)
5. Iterate incrementally -- one change at a time

### Anti-Patterns

- Do NOT use chain-of-thought prompting at `medium+` reasoning levels
- Do NOT use sampling parameters (temperature/top_p) at reasoning levels above `none`
- Do NOT compact every turn (only after milestones)
- Do NOT add long personas when raising reasoning effort would be more effective
- Do NOT use vague instructions -- "ambiguity is now a bug, not a feature"

### Sources

- OpenAI announcement: https://openai.com/index/introducing-gpt-5-2/
- Using GPT-5.2 docs: https://developers.openai.com/api/docs/guides/latest-model/
- GPT-5.2 Prompting Guide (Cookbook): https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide/
- OpenAI Academy resource: https://academy.openai.com/public/resources/latest-model
- eWeek coverage: https://www.eweek.com/news/openai-launches-gpt-5-2/
- Simon Willison analysis: https://simonwillison.net/2025/Dec/11/gpt-52/
- Digital Applied guide: https://www.digitalapplied.com/blog/gpt-5-2-complete-guide
- Atlabs prompting guide: https://www.atlabs.ai/blog/gpt-5.2-prompting-guide-the-2026-playbook-for-developers-agents
- Automatio specs: https://automatio.ai/models/gpt-5-2
- CloudPrice specs: https://cloudprice.net/models/gpt-5.2-2025-12-11
- LLM Stats: https://llm-stats.com/models/gpt-5.2-2025-12-11
- Muon Tools: https://muon.tools/en/models/openai-gpt-5.2

---

## GPT-5.1 (Previous Flagship)

### Specs

| Field | Value |
|-------|-------|
| Model ID (API) | `gpt-5.1` |
| Codex variant | `gpt-5.1-codex` |
| Codex Mini variant | `gpt-5.1-codex-mini` |
| Codex Max variant | `gpt-5.1-codex-max` |
| Release date | November 13, 2025 |
| Context window | 400K tokens |
| Max output tokens | 128K tokens |
| Knowledge cutoff | September 30, 2024 |
| Modality | Text + Image + File input; Text output |

### Pricing (Standard tier, per 1M tokens)

| Type | Cost |
|------|------|
| Input | $1.25 |
| Output | $10.00 |
| Cached input | $0.125 |
| Batch input | $0.625 |
| Batch output | $5.00 |
| Priority input | $2.50 |
| Priority output | $20.00 |

### Key Behaviors

- Default reasoning effort is `none` (fast, "non-reasoning-like" behavior)
- Supported `reasoning.effort` values: `none`, `low`, `medium`, `high` (no `xhigh`)
- More steerable in personality, tone, and formatting than GPT-5 base
- Better calibrated to prompt difficulty (fewer wasted tokens on easy prompts)
- Flagship for coding and agentic tasks with configurable reasoning

### When to Prefer GPT-5.1 over GPT-5.2

- Lower cost ($1.25/$10.00 vs $1.75/$14.00 -- 28% cheaper)
- Already achieving high quality with existing prompt suite
- Latency-sensitive applications where 5.2's extra intelligence is unnecessary
- Budget-constrained high-volume workloads
- Older knowledge cutoff is acceptable (Sep 2024 vs Aug 2025)

### Prompting Patterns

**`none` mode = GPT-4o-style prompting:**
- Few-shot examples work well for strict style/format imitation
- High-quality tool descriptions important
- Concrete output length clamps

**Persistence rule for agentic tasks:**
"Keep going until the user's request is completely resolved; don't stop early."

**Persona handling:**
- GPT-5.1 responds well to clear persona for tone/communication style
- Persona alone will not "add knowledge" -- use explicit constraints + evals for correctness

### Tools

Post-trained on:
- `apply_patch` (structured diffs -- reduces patch failure rates)
- `shell` (plan-execute loop via controlled command execution)

Dedicated coding variants:
- `gpt-5.1-codex` ($1.25/$10.00) -- full coding variant
- `gpt-5.1-codex-mini` ($0.25/$2.00) -- cheaper coding variant
- `gpt-5.1-codex-max` ($1.25/$10.00) -- extended compute coding, released Dec 2025

### Sources

- LLM Stats: https://llm-stats.com/models/gpt-5.1-2025-11-13
- Muon specs: https://muon.tools/en/models/openai-gpt-5.1
- PricePerToken timeline: https://pricepertoken.com/pricing-page/provider/openai
- Finout pricing guide: https://www.finout.io/blog/openai-pricing-in-2026

---

## GPT-5 (Base)

### Specs

| Field | Value |
|-------|-------|
| Model ID (API) | `gpt-5` |
| Release date | August 7, 2025 |
| Context window | 400K tokens |
| Max output tokens | 128K tokens |
| Knowledge cutoff | September 30, 2024 |
| Modality | Text + Image input; Text output |

### Pricing (Standard tier, per 1M tokens)

| Type | Cost |
|------|------|
| Input | $1.25 |
| Output | $10.00 |
| Cached input | $0.125 |
| Batch input | $0.625 |
| Batch output | $5.00 |

### Key Characteristics

- First unified GPT-5 system with built-in thinking
- Automatic routing between instant mode and thinking mode
- Smart router decides which mode based on complexity, tool needs, and explicit user intent (e.g., "think hard about this")
- When usage limits are reached, falls back to mini version
- Introduced four variants: GPT-5 (base), GPT-5 Pro, GPT-5 Mini, GPT-5 Nano
- GDPval score: 38.8%
- SWE-bench: 74.9%
- AIME 2025: 94.6%
- GPT-5 Instant and Thinking variants retired from ChatGPT Feb 13, 2026

### Prompting Patterns (from official GPT-5 Prompting Guide)

**Core principles:**
1. Show one gold example -- few-shot is fastest path to consistent tone
2. Right-size the "thinking" -- light/medium/deep depending on stakes
3. Prefer machine-readable outputs -- JSON beats prose when automating
4. Constrain the canvas -- format, length, style, variables, acceptance checks
5. State the goal first -- one sentence that defines "done"

**Prompt skeleton:**
```
<goal> Summarize the incident ticket for executives.
<style> Plain, neutral. No hype.
<format> JSON object following the schema below.
<constraints> No speculation. Cite sources if present.
<reasoning> medium
<schema> { ... }
```

### Sources

- OpenAI announcement: https://openai.com/index/introducing-gpt-5/
- CNBC coverage: https://www.cnbc.com/2025/08/07/openai-launches-gpt-5-model-for-all-chatgpt-users.html
- VentureBeat: https://venturebeat.com/ai/openai-launches-gpt-5-not-agi-but-capable-of-generating-software-on-demand
- OpenAI API models page: https://developers.openai.com/api/docs/models/gpt-5
- Ondevtra prompting guide: https://ondevtra.com/gpt5-prompt-guide.html
- Usama Codes features guide: https://usama.codes/blog/gpt-5-release-features-impact

---

## GPT-5 Mini

### Specs

| Field | Value |
|-------|-------|
| Model ID (API) | `gpt-5-mini` |
| Release date | August 7, 2025 |
| Context window | 400K tokens |
| Max output tokens | 128K tokens |
| Knowledge cutoff | May 31, 2024 |
| Modality | Text + Image input; Text output |

### Pricing (Standard tier, per 1M tokens)

| Type | Cost |
|------|------|
| Input | $0.25 |
| Output | $2.00 |
| Cached input | $0.025 |
| Batch input | $0.125 |
| Batch output | $1.00 |
| Priority input | $0.45 |
| Priority output | $3.60 |

### Key Characteristics

- Smaller, faster version of GPT-5 optimized for lower latency and resource usage
- Used as ChatGPT fallback when usage limits are reached
- Inherits GPT-5's safety tuning, instruction-following, and multimodal reasoning
- Supports reasoning, vision, and all built-in tools
- 5x cheaper than GPT-5 base on input and output
- Large 400K context window maintained despite being "mini"

### Use Cases

- Cost-optimized reasoning and chat
- Well-defined tasks with predictable complexity
- High-volume applications where GPT-5 base is too expensive
- Fallback tier in routing architectures
- Faster response times for latency-sensitive applications

### Sources

- Roboflow comparison: https://playground.roboflow.com/models/compare/gpt-5-mini-vs-gpt-5-nano
- Rogue Marketing pricing: https://the-rogue-marketing.github.io/openai-api-pricing-comparison-october-2025/
- OpenAI pricing: https://developers.openai.com/api/docs/pricing/

---

## GPT-5 Nano

### Specs

| Field | Value |
|-------|-------|
| Model ID (API) | `gpt-5-nano` |
| Release date | August 7, 2025 |
| Context window | 400K tokens |
| Max output tokens | 128K tokens |
| Knowledge cutoff | Not officially confirmed |
| Modality | Text + Image input; Text output |

### Pricing (Standard tier, per 1M tokens)

| Type | Cost |
|------|------|
| Input | $0.05 |
| Output | $0.40 |
| Cached input | $0.005 |
| Batch input | $0.025 |
| Batch output | $0.20 |

### Key Characteristics

- Most lightweight GPT-5 variant
- Built for speed and efficiency in high-volume or cost-sensitive applications
- Retains reasoning capability at smaller scale
- Ideal for mobile, embedded, or latency-constrained deployments
- Best suited for summarization and classification tasks
- 25x cheaper than GPT-5 base on input, 25x cheaper on output
- 5x cheaper than GPT-5 Mini
- Maintains full 400K context window

### Use Cases

- High-throughput simple instruction-following
- Classification and routing
- Summarization
- Edge/mobile deployments
- Cost-sensitive applications at scale
- Preprocessing and triage in multi-model pipelines

### Sources

- LLM Stats: https://llm-stats.com/models/gpt-5-nano-2025-08-07
- OpenAI API models page: https://developers.openai.com/api/docs/models/gpt-5-nano
- Artificial Analysis: https://artificialanalysis.ai/models/comparisons/gpt-5-1-codex-mini-vs-gpt-5-nano

---

## o3 (Reasoning Model)

### Specs

| Field | Value |
|-------|-------|
| Model ID (API) | `o3` |
| Release date | April 16, 2025 |
| Context window | 200K tokens |
| Max output tokens | 100K tokens |
| Knowledge cutoff | May 2024 |
| Modality | Text + Image input; Text output |
| Capabilities | Vision, function calling, reasoning, structured output, web search, Python, image generation |

### Pricing (Standard tier, per 1M tokens)

| Type | Cost |
|------|------|
| Input | $2.00 |
| Output | $8.00 |
| Cached input | $0.50 |
| Flex input | $1.00 |
| Flex output | $4.00 |
| Priority input | $3.50 |
| Priority output | $14.00 |

Note: Reasoning tokens are NOT visible via API but occupy context window space and are billed as output tokens.

### Key Characteristics

- Most powerful dedicated reasoning model from OpenAI
- Trained to "think for longer before responding"
- First reasoning model that can agentically use and combine ALL tools within ChatGPT
- Natively uses tools within chain of thought (CoT)
- Supports web browsing, Python, image analysis, image generation, file search, and memory
- Supports reasoning effort levels: `low`, `medium`, `high`
- Deliberative alignment: reasons about safety policies in context

### Prompting Best Practices

**Developer messages (not "system" messages):**
- Reasoning models use `developer` role instead of `system`
- System messages are automatically converted to developer messages internally
- Treat developer prompt as analogous to system prompt

**Formatting control:**
- o3 avoids Markdown by default
- To enable Markdown formatting, include `Formatting re-enabled` on the first line of the developer message

**Core prompting rules:**
1. Keep prompts simple and direct -- high-level guidance + clear success criteria
2. **NEVER** use chain-of-thought prompting ("think step by step") -- model already reasons internally
3. Try zero-shot first -- add few-shot examples ONLY for strict formatting behavior
4. Use delimiters (headings, XML tags, fenced blocks) to separate task, context, constraints
5. Be explicit about constraints (budget, time, scope, acceptance criteria)

**Function calling guidance:**

1. **Role prompting**: Establish clear agent identity and scope
2. **Function call ordering**: Explicitly outline task sequences for complex workflows
3. **Boundary definition**: Clarify when to invoke vs avoid tools
4. **Description quality**: Lead with usage rules in function descriptions ("Only call if directory exists")
5. **Few-shot examples**: Include for complex argument formats (especially regex, structured data)
6. **Strict mode**: Always enable `strict: True` in function schemas
7. **Persist reasoning items**: Use `encrypted_content` to maintain CoT between function calls

**Anti-patterns:**
- Do NOT use chain-of-thought prompting
- Do NOT explicitly prompt for planning between tool calls
- Do NOT promise to call functions later -- emit now or respond normally
- Do NOT carry irrelevant past tool calls in conversation history
- Avoid deeply nested parameter hierarchies
- Avoid vague or overlapping function descriptions

**Hallucination prevention:**
- State clearly: "Do NOT promise to call functions later. If needed, emit now."
- Start fresh conversations for unrelated topics
- Discard irrelevant past tool calls; summarize context in user message

**Tool limits:**
- No hard cap, but <100 tools and <20 arguments per tool remain "in-distribution"
- Prefer flat argument structures over deeply nested objects
- Use `allowed_tools` parameter to include only necessary tools

```python
response = client.responses.create(
    model="o3",
    input=context,
    tools=tools,
    include=["reasoning.encrypted_content"]
)
context += response.output  # Preserves reasoning for next turn
```

### When to Use o3 vs GPT-5.x

| Use o3 when... | Use GPT-5.2 when... |
|----------------|---------------------|
| Accuracy/reliability on ambiguous decisions matters more than latency | Fast execution needed |
| Planning and policy/compliance judgments | High-quality writing/coding |
| Dense document reasoning | Want to tune reasoning effort per call |
| Multi-faceted questions requiring deep tool orchestration | Scope-constrained tasks |
| Multi-step scientific/math problems | Cost sensitivity (o3 output is cheaper but reasoning tokens add up) |

### Sources

- OpenAI announcement: https://openai.com/index/introducing-o3-and-o4-mini/
- System card: https://openai.com/index/o3-o4-mini-system-card
- Function calling guide: https://developers.openai.com/cookbook/examples/o-series/o3o4-mini_prompting_guide
- LLM Stats: https://llm-stats.com/models/o3
- DataCamp analysis: https://www.datacamp.com/blog/o4-mini
- Microsoft Tech Community: https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/everything-you-need-to-know-about-reasoning-models-o1-o3-o4-mini-and-beyond/4406846

---

## o4-mini (Reasoning Model)

### Specs

| Field | Value |
|-------|-------|
| Model ID (API) | `o4-mini` |
| Release date | April 16, 2025 |
| Context window | 200K tokens |
| Max output tokens | 100K tokens |
| Knowledge cutoff | May 31, 2024 |
| Modality | Text + Image input; Text output |
| Capabilities | Vision, function calling, reasoning, structured output, web search, Python |

### Pricing (Standard tier, per 1M tokens)

| Type | Cost |
|------|------|
| Input | $1.10 |
| Output | $4.40 |
| Cached input | $0.275 |
| Flex input | $0.55 |
| Flex output | $2.20 |
| Priority input | $2.00 |
| Priority output | $8.00 |

### Key Characteristics

- Latest small o-series model
- Optimized for fast, effective reasoning
- Exceptionally efficient performance in coding and visual tasks
- Faster and more affordable than o3 (45% cheaper on input, 45% cheaper on output)
- Multimodal by default (unlike o3-mini which lacked vision)
- Supports reasoning effort levels: `low`, `medium`, `high`
- Natively uses tools within chain of thought
- Deliberative alignment for safety

### Prompting Best Practices

Same as o3 (see above). Key differences:
- Slightly less powerful reasoning than o3 but significantly faster
- Better cost-performance ratio for most reasoning tasks
- Same developer message and formatting rules as o3
- Same function calling patterns and anti-patterns
- `Formatting re-enabled` trick works the same way

### When to Use o4-mini

- Need reasoning capabilities but at lower cost than o3
- Coding and visual reasoning tasks where speed matters
- Budget-conscious reasoning workloads
- Tasks where o3's extra capability is not needed
- Replaced o3-mini with added vision support

### Status Note

o4-mini was retired from ChatGPT on February 13, 2026 but remains available via API.

### Sources

- OpenAI announcement: https://openai.com/index/introducing-o3-and-o4-mini/
- LLM Stats: https://llm-stats.com/models/o4-mini
- DocsBot specs: https://docsbot.ai/models/o4-mini
- DataCamp analysis: https://www.datacamp.com/blog/o4-mini
- Analytics Vidhya: https://analyticsvidhya.com/blog/2025/04/o3-and-o4-mini

---

## o3-pro

### Specs

| Field | Value |
|-------|-------|
| Model ID (API) | `o3-pro` |
| Release date | June 10, 2025 |
| Context window | 200K tokens (same as o3) |
| Max output tokens | 100K tokens (same as o3) |
| Knowledge cutoff | May 2024 (same as o3) |

### Pricing (Standard tier only, per 1M tokens)

| Type | Cost |
|------|------|
| Input | $20.00 |
| Output | $80.00 |

### Key Characteristics

- Version of o3 designed to think longer for most reliable responses
- Like o1-pro before it -- premium reasoning at premium cost (10x o3 pricing)
- Available to Pro users in ChatGPT and via API
- For tasks where reliability is paramount and cost is secondary
- No Batch or Flex pricing available

### Sources

- OpenAI o3/o4-mini announcement (June 10 update): https://openai.com/index/introducing-o3-and-o4-mini/

---

## o3-mini (Legacy Reasoning)

### Specs

| Field | Value |
|-------|-------|
| Model ID (API) | `o3-mini` |
| Release date | January 31, 2025 |
| Context window | 200K tokens |
| Max output tokens | 100K tokens |
| Knowledge cutoff | October 2023 |
| Modality | Text only (NO vision) |

### Pricing (Standard tier, per 1M tokens)

| Type | Cost |
|------|------|
| Input | $1.10 |
| Output | $4.40 |
| Cached input | $0.55 |

### Key Characteristics

- First small reasoning model with function calling, structured outputs, and developer messages
- Supports reasoning effort: `low`, `medium`, `high`
- Does NOT support vision (use o3 or o4-mini for visual reasoning)
- Replaced o1-mini in the o-series lineup
- Superseded by o4-mini (which adds vision and better performance)
- Same pricing as o4-mini but less capable

### Sources

- OpenAI announcement: https://openai.com/index/openai-o3-mini/
- LLM Stats: https://llm-stats.com/models/o3-mini
- PromptHub model card: https://www.prompthub.us/models/o3-mini

---

## Model Retirements

### Retired from ChatGPT on February 13, 2026

| Model | ChatGPT Status | API Status | Notes |
|-------|----------------|------------|-------|
| GPT-4o | Retired Feb 13 | Shutting down Feb 16, 2026 | Only 0.1% daily usage remained |
| GPT-4.1 | Retired Feb 13 | Available (no announced shutdown) | |
| GPT-4.1 mini | Retired Feb 13 | Available (no announced shutdown) | |
| o4-mini | Retired Feb 13 | Available (no announced shutdown) | |
| GPT-5 (Instant) | Retired Feb 13 | GPT-5 base still available | |
| GPT-5 (Thinking) | Retired Feb 13 | GPT-5 base still available | |
| `chatgpt-4o-latest` | N/A | Shutting down Feb 17, 2026 | Deprecated Nov 18, 2025 |

### Still Available via API (as of Feb 21, 2026)

- GPT-5.2 (all variants) -- current flagship
- GPT-5.1 (all variants)
- GPT-5 (base)
- GPT-5 Mini
- GPT-5 Nano
- o3 and o3-pro
- o4-mini
- o3-mini
- GPT-4o audio variants (Transcribe, mini Transcribe, mini TTS)

### Context: GPT-4o Retirement Story

OpenAI initially deprecated GPT-4o after GPT-5 launch in Aug 2025, then restored it after user backlash about losing its "warmth" and conversational style. Users needed time to transition creative ideation workflows. That feedback directly shaped GPT-5.1 and GPT-5.2 improvements: better personality support, stronger creative ideation, customizable response styles (base styles, tones like "Friendly", warmth/enthusiasm controls). With only 0.1% daily usage remaining, OpenAI finally retired it Feb 13, 2026.

### Sources

- OpenAI retirement announcement: https://openai.com/index/retiring-gpt-4o-and-older-models/
- Deprecations page: https://developers.openai.com/api/docs/deprecations/
- CNBC coverage: https://www.cnbc.com/2026/01/29/openai-will-retire-gpt-4o-from-chatgpt-next-month.html
- Times of India: https://timesofindia.indiatimes.com/technology/tech-news/openai-will-retire-gpt4o-on-february-13-2026-gpt5-2-to-take-over-as-the-new-standard-for-professionals/articleshow/127816579.cms
- NxCode guide: https://www.nxcode.io/resources/news/gpt-4o-retirement-2026
- VentureBeat chatgpt-4o-latest: https://venturebeat.com/ai/openai-is-ending-api-access-to-fan-favorite-gpt-4o-model-in-february-2026

---

## Pricing Summary Table

All prices per 1M tokens, Standard tier.

| Model | Input | Output | Cached Input | Context | Max Output | Knowledge Cutoff | Released |
|-------|-------|--------|--------------|---------|------------|-----------------|----------|
| **GPT-5.2** | $1.75 | $14.00 | $0.175 | 400K | 128K | Aug 31, 2025 | Dec 2025 |
| **GPT-5.2 Pro** | $21.00 | $168.00 | -- | 400K | 128K | Aug 31, 2025 | Dec 2025 |
| **GPT-5.1** | $1.25 | $10.00 | $0.125 | 400K | 128K | Sep 30, 2024 | Nov 2025 |
| **GPT-5** | $1.25 | $10.00 | $0.125 | 400K | 128K | Sep 30, 2024 | Aug 2025 |
| **GPT-5 Mini** | $0.25 | $2.00 | $0.025 | 400K | 128K | May 31, 2024 | Aug 2025 |
| **GPT-5 Nano** | $0.05 | $0.40 | $0.005 | 400K | 128K | Unconfirmed | Aug 2025 |
| **o3** | $2.00 | $8.00 | $0.50 | 200K | 100K | May 2024 | Apr 2025 |
| **o3-pro** | $20.00 | $80.00 | -- | 200K | 100K | May 2024 | Jun 2025 |
| **o4-mini** | $1.10 | $4.40 | $0.275 | 200K | 100K | May 31, 2024 | Apr 2025 |
| **o3-mini** | $1.10 | $4.40 | $0.55 | 200K | 100K | Oct 2023 | Jan 2025 |

---

## Cross-Model Prompting Quick Reference

| Feature | GPT-5.2 | GPT-5.1 | GPT-5 | o3 | o4-mini |
|---------|---------|---------|-------|-----|---------|
| CoT prompting | Light at `none`; avoid at `medium+` | Light at `none`; avoid at `medium+` | Light | **NEVER** | **NEVER** |
| Few-shot | Helpful at `none`/`low`; less needed at `medium+` | Helpful at `none`/`low`; less needed at `medium+` | Helpful | Only for strict formatting | Only for strict formatting |
| System prompt | Yes (system or developer) | Yes (system or developer) | Yes | Developer role ONLY | Developer role ONLY |
| Reasoning effort | `none`/`minimal`/`low`/`medium`/`high`/`xhigh` | `none`/`low`/`medium`/`high` | Auto routing | `low`/`medium`/`high` | `low`/`medium`/`high` |
| Text verbosity | `low`/`medium`/`high` | Not available | Not available | Not available | Not available |
| Markdown default | Yes | Yes | Yes | **No** ("Formatting re-enabled") | **No** ("Formatting re-enabled") |
| Compaction | Yes | No | No | No | No |
| Vision | Yes | Yes | Yes | Yes | Yes (o3-mini: No) |
| Sampling params | Only at `effort: none` | Only at `effort: none` | Yes | Not supported | Not supported |

---

## Additional Model Variants (Specialized)

These are specialized variants noted for completeness:

| Model | Type | Pricing (in/out) | Released | Notes |
|-------|------|------------------|----------|-------|
| `gpt-5.1-codex` | Coding | $1.25 / $10.00 | Nov 2025 | Dedicated coding variant |
| `gpt-5.1-codex-mini` | Coding (small) | $0.25 / $2.00 | Nov 2025 | Cheaper coding variant |
| `gpt-5.1-codex-max` | Coding (max) | $1.25 / $10.00 | Dec 2025 | Extended compute coding |
| `gpt-5.2-codex` | Coding | $1.75 / $14.00 | Jan 2026 | GPT-5.2 coding variant; SWE-Bench Pro 56.4% |
| `gpt-5-image` | Image generation | $10.00 / $10.00 | Oct 2025 | Image generation model |
| `gpt-5-image-mini` | Image gen (small) | $2.50 / $2.00 | Oct 2025 | Cheaper image generation |
| `o3-deep-research` | Deep research | Varies | Oct 2025 | Extended research capability |
| `o4-mini-deep-research` | Deep research (small) | Varies | Oct 2025 | Cheaper deep research |
| `gpt-audio` | Audio | $2.50 / $10.00 | Jan 2026 | Audio processing |
| `gpt-audio-mini` | Audio (small) | $0.60 / $2.40 | Jan 2026 | Cheaper audio processing |
| `gpt-oss-safeguard-20b` | Safety/moderation | $0.07 / $0.30 | Oct 2025 | Open-source safeguard model |

---

*Research compiled: February 21, 2026*
*Primary sources: OpenAI official docs, OpenAI Cookbook, OpenAI Academy, LLM Stats, third-party pricing aggregators*
*Previous version: Abbreviated research from earlier session*
