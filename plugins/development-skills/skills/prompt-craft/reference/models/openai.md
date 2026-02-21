# OpenAI

## GPT-5.2 (Current Flagship)

**Released:** December 11, 2025
**Best for:** Complex reasoning, broad world knowledge, agentic/tool-heavy workflows, code-heavy tasks
**Knowledge cutoff:** 2025-08-31
**Context (API):** 400K tokens | **Max output:** 128K tokens
**Chat model:** `gpt-5.2-chat-latest` (128K context | 16,384 max output)
**Pricing:** $1.75/M input ($0.175 cached), $14/M output
**Three variants:** Instant (speed), Thinking (reasoning), Pro (enterprise)

### What Changed vs GPT-5.1

- Better general intelligence and instruction following
- More accurate and token-efficient answers
- Stronger multimodality (especially vision)
- Better tool calling + context management in the API
- New context management capability via **compaction**
- Adds **`xhigh` reasoning effort** and **concise reasoning summaries**
- 38% reduction in hallucinations vs GPT-5.1
- 98.7% tool-calling reliability (Tau2 benchmark)
- Benchmarks: GPQA Diamond 93.2%, AIME 2025 100%, SWE-Bench Verified 80%

### The Knobs That Matter

**1) `reasoning.effort` (quality vs latency/cost)**
- Six levels: `none` (default) → `minimal` → `low` → `medium` → `high` → `xhigh` (Pro only)
- Default is `none` (fast / low-latency). No internal reasoning.
- Increase gradually for harder reasoning. Temperature/top_p only work at `none`.
- With `none`, prompting matters more: explicitly ask for a *brief plan / outline* before the final answer.

**2) `text.verbosity` (response length / "how much to say")**
- Values: `low`, `medium`, `high` (default: `medium`).
- Use this instead of trying to fight verbosity purely with prompting.

**3) Reasoning summaries (`reasoning.summary`)**
- GPT-5.2 can return concise summaries of its reasoning (useful for audits / traceability without exposing full hidden reasoning).

**4) Compaction (`POST /v1/responses/compact`)**
- Use for long-running workflows (many turns / tool calls) to extend effective context.
- Output is **opaque/encrypted**: treat as "state to continue with", not data to parse.

### Prompting Patterns That Reliably Improve Results

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

### Tools & Agent Workflows

- Prefer **Responses API** for tool-heavy workflows; it supports better conversation state handling.
- GPT-5.2 is post-trained on specific tools (notably `apply_patch` and `shell`) and supports **custom tools** (freeform tool inputs + optional constrained outputs).
- For long task chains, compact after milestones (not every turn), then continue with the compacted state.
- MCP (Model Context Protocol) support available.

### Common Gotchas

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

## GPT-5.3 Codex (Latest Coding Model)

**Released:** February 5, 2026
**Optimized for:** Agentic coding — the most capable coding model to date
**Context (API):** 400K tokens | **Max output:** 128K tokens
**Pricing:** $1.75/M input ($0.175 cached), $14/M output

### What Changed vs GPT-5.2 Codex

- 25% faster inference
- **Mid-task steering:** Interact with and guide the agent in real-time during complex projects
- **Deep diffs:** Reasoning transparency for code changes
- Improved codebase coherence across multi-file edits
- Fixes for lint loops, weak bug explanations, and flaky-test premature completion
- First model classified **High for cybersecurity** under OpenAI's Preparedness Framework

### Key Benchmarks

| Benchmark | GPT-5.3 Codex | GPT-5.2 Codex |
|-----------|---------------|---------------|
| SWE-Bench Pro Public | 56.8% | 56.4% |
| Terminal-Bench 2.0 | 77.3% | 64.0% |
| OSWorld-Verified | 64.7% | — |

### When to Use

- **GPT-5.3 Codex** for sustained, multi-file engineering, terminal tasks, and deployment workflows
- **GPT-5.2** for general-purpose work, mixed workloads, or when you need `none` reasoning effort

**Sources:**
- GPT-5.3 Codex launch: https://www.digitalapplied.com/blog/gpt-5-3-codex-release-features-benchmarks-guide
- Pricing: https://www.eesel.ai/blog/gpt-53-codex-pricing
- Benchmarks: https://automatio.ai/models/gpt-5-3-codex

---

## GPT-5.2 Codex (Previous Coding Model)

**Released:** January 14, 2026
**Status:** Superseded by GPT-5.3 Codex, still available
**Context (API):** 400K tokens | **Max output:** 128K tokens
**Pricing:** $1.75/M input ($0.175 cached), $14/M output

### Key Capabilities

- Post-trained on `apply_patch` (structured diffs) and `shell` (plan-execute loops)
- Context compaction for long coding sessions
- SWE-Bench Pro: 56.4%, Terminal-Bench 2.0: 64.0%
- Reasoning effort: low, medium, high, xhigh (no `none` — always reasons for code)

**Sources:**
- GPT-5.2 Codex guide: https://www.digitalapplied.com/blog/gpt-5-2-codex-openai-model-guide-2026
- https://serenitiesai.com/articles/gpt-52-codex-review-2026

---

## GPT-5.1

**Status:** Previous flagship (still useful; cheaper than 5.2 in many setups)
**Best for:** Coding + agentic workflows where you want **configurable reasoning** and strong steerability
**Knowledge cutoff:** 2024-09-30
**Context (API):** 400K tokens | **Max output:** 128K tokens

### Key Behaviors

- Default reasoning effort is `none` (fast, "non-reasoning-like" behavior)
- Supported `reasoning.effort` values include `none`, `low`, `medium`, and `high`
- More steerable in **personality, tone, and formatting** than GPT-5
- Better calibrated to prompt difficulty (fewer wasted tokens on easy prompts)

### Prompting: What Actually Works Best

**1) "None" mode = classic-style prompting**
When `reasoning.effort="none"`, many classic prompt techniques work well:
- Few-shot examples (when you need strict style/format imitation)
- High-quality tool descriptions
- Concrete output length clamps

**2) Persistence and completeness**
On longer agentic tasks, add an explicit rule:
"Keep going until the user's request is completely resolved; don't stop early."

**3) Persona is helpful — but don't confuse tone with capability**
GPT-5.1 responds well to a clear persona, but persona alone won't "add knowledge."
Use persona for tone/communication style; use explicit constraints + evals for correctness.

### Tools: `apply_patch` and `shell`

GPT-5.1 is post-trained on:
- `apply_patch` (structured diffs for file edits; reduces patch failure rates vs DIY JSON tools)
- `shell` (plan-execute loop via controlled command execution)

### When to Prefer GPT-5.1 vs GPT-5.2

- Choose **GPT-5.1** if you want lower cost and you're already getting high quality with your prompt suite.
- Choose **GPT-5.2** if you need stronger instruction following, better tool reliability, improved vision, compaction, and the best all-around performance.

**Sources:**
- GPT-5.1 model info: https://platform.openai.com/docs/models/gpt-5-1
- GPT-5.1 Prompting Guide (Cookbook): https://cookbook.openai.com/examples/gpt-5/gpt-5-1_prompting_guide
- OpenAI API Changelog (5.1 defaults to `none`): https://platform.openai.com/docs/changelog

---

## GPT-5 (Base)

**Released:** August 7, 2025
**Model ID:** `gpt-5`
**Context:** 400K tokens | **Max output:** 128K tokens
**Pricing:** $1.25/M input ($0.125 cached), $10/M output

First unified GPT-5 system with built-in thinking. Automatic routing between instant and thinking modes.

### Prompting Patterns (Official GPT-5 Prompting Guide)

1. Show one gold example — few-shot is fastest path to consistent tone
2. Right-size the "thinking" — light/medium/deep depending on stakes
3. Prefer machine-readable outputs — JSON beats prose when automating
4. Constrain the canvas — format, length, style, variables, acceptance checks
5. State the goal first — one sentence that defines "done"

---

## GPT-5 Mini & Nano (Cost-Optimized)

| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| GPT-5 Mini (`gpt-5-mini`) | $0.25/M | $2/M | Cost-optimized reasoning, high-volume |
| GPT-5 Nano (`gpt-5-nano`) | $0.05/M | $0.40/M | Classification, routing, edge/mobile |

Both maintain 400K context. Nano is 25x cheaper than GPT-5 base. Use for preprocessing, triage, and latency-sensitive pipelines.

---

## o3 / o4-mini Reasoning Models

| Model | Context | Pricing (in/out) | Reasoning Effort | Released |
|-------|---------|-------------------|-----------------|----------|
| **o3** | 200K | $2/$8 per M | low/medium/high | Apr 2025 |
| **o3-pro** | 200K | $20/$80 per M | Maximum | Jun 2025 |
| **o4-mini** | 200K | $1.10/$4.40 per M | low/medium/high | Apr 2025 |

**What they are:** Reasoning models that think longer about ambiguous, multi-step problems. Behave differently from GPT "workhorse" models.

### Prompting Rules of Thumb

- **Keep prompts simple and direct.** High-level guidance + clear success criteria.
- **NEVER use chain-of-thought prompting** ("think step by step"). They reason internally.
- **Try zero-shot first.** Few-shot only for strict formatting behavior.
- **Use delimiters** (headings, XML tags, fenced blocks) to separate task, context, and constraints.
- **Be explicit about constraints** (budget, time, scope, acceptance criteria).

### Developer Messages and Formatting

- Use **developer messages** (not "system" messages). System messages are converted internally.
- **Markdown off by default.** Include **`Formatting re-enabled`** on the first line of developer message to enable.

### Function Calling Best Practices

1. **Role prompting:** Establish clear agent identity and scope
2. **Function call ordering:** Explicitly outline task sequences for complex workflows
3. **Boundary definition:** Clarify when to invoke vs avoid tools
4. **Description quality:** Lead with usage rules ("Only call if directory exists")
5. **Strict mode:** Always enable `strict: True` in function schemas
6. **Persist reasoning:** Use `encrypted_content` to maintain CoT between function calls

```python
response = client.responses.create(
    model="o3",
    input=context,
    tools=tools,
    include=["reasoning.encrypted_content"]
)
context += response.output  # Preserves reasoning for next turn
```

### Anti-Patterns

- Do NOT use chain-of-thought prompting
- Do NOT explicitly prompt for planning between tool calls
- Do NOT promise to call functions later — emit now or respond normally
- Do NOT carry irrelevant past tool calls in conversation history
- Avoid deeply nested parameter hierarchies (keep tools flat, <100 tools, <20 args)

### When to Use o-series vs GPT-5.x

| Use o-series when... | Use GPT-5.x when... |
|---------------------|---------------------|
| Accuracy on ambiguous decisions > latency | Fast execution needed |
| Planning, compliance, policy judgments | Writing/coding speed |
| Dense document reasoning | Tunable reasoning per call |
| Multi-step scientific/math problems | Cost sensitivity |

**Note:** o3 and o4-mini remain available via API. o4-mini retired from ChatGPT Feb 13, 2026. Deep research variants (`o3-deep-research`, `o4-mini-deep-research`) also available.

**Sources:**
- Reasoning best practices: https://platform.openai.com/docs/guides/reasoning-best-practices
- Function calling guide: https://developers.openai.com/cookbook/examples/o-series/o3o4-mini_prompting_guide
- Model retirements: https://openai.com/index/introducing-o3-and-o4-mini/

---

## Model Retirements (February 13, 2026)

The following models were retired from ChatGPT on February 13, 2026:
- GPT-4o, GPT-4.1, GPT-4.1 mini, o4-mini, GPT-5 Instant, GPT-5 Thinking

API access remains for now. Migrate to GPT-5.2 or GPT-5.1 for production workloads.

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| GPT-5.2 | Light (brief plan at `none`) | Helpful at `none`/`low`; less at `medium+` | Yes (system/developer) |
| GPT-5.3 Codex | Always reasons | Helpful at lower effort | Yes (system/developer) |
| GPT-5.1 | Light (brief plan at `none`) | Helpful at `none`/`low`; less at `medium+` | Yes (system/developer) |
| GPT-5 / Mini / Nano | Light | Helpful | Yes |
| o3 / o4-mini | **NEVER** | Only for strict formatting | Developer role |

---

*Last updated: February 2026*
