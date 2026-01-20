# Langfuse Traces Reference

> **Deep-dive documentation for the trace domain** | For quick start, see [getting-started.md](getting-started.md)

---

## Table of Contents

1. [Overview](#overview)
2. [Data Model](#data-model)
   - [Hierarchy](#hierarchy)
   - [Sessions](#sessions)
   - [Traces](#traces)
   - [Observations](#observations)
3. [Observation Types](#observation-types)
4. [Token & Cost Tracking](#token--cost-tracking)
   - [Ingesting Usage Data](#ingesting-usage-data)
   - [Cost Inference](#cost-inference)
   - [Usage Detail Fields](#usage-detail-fields)
5. [Metadata, Tags & User Tracking](#metadata-tags--user-tracking)
6. [Querying Traces](#querying-traces)
   - [Listing Traces](#listing-traces)
   - [Filtering](#filtering)
   - [Pagination](#pagination)
7. [Analyzing Traces](#analyzing-traces)
   - [Latency Analysis](#latency-analysis)
   - [Error Detection](#error-detection)
   - [Cost Breakdown](#cost-breakdown)
8. [Analogies for Non-Experts](#analogies-for-non-experts)

---

## Overview

**Traces** are the foundation of Langfuse observability. Think of them as **detailed receipts** for every AI interaction your application processes.

When your AI app handles a user message, a trace captures:
- What went in (the input)
- What came out (the output)
- Every step in between (observations)
- How long each step took (timing)
- How much it cost (token/cost tracking)

**Example use cases:**
- Debug why a response was slow
- Find which API calls are failing
- Track costs across different models
- Identify patterns in user interactions

---

## Data Model

### Hierarchy

Langfuse uses a three-level hierarchy:

```
Session (optional)
  |
  +-- Trace (single request/operation)
        |
        +-- Observation (nested steps)
              |
              +-- Child Observation
                    |
                    +-- ...
```

**Analogy:** Think of it like a folder structure:
- **Session** = A folder for a conversation thread
- **Trace** = A single document (one complete interaction)
- **Observations** = Sections and subsections within that document

### Sessions

Sessions group multiple traces from the same user interaction:

| Attribute | Description | Constraint |
|-----------|-------------|------------|
| `session_id` | Unique identifier | US-ASCII string, max 200 chars |

**When to use sessions:**
- Chat threads (multiple messages in one conversation)
- Multi-turn interactions
- Workflow steps that span multiple API calls

**Features:**
- Session replay view in UI
- Public sharing links
- Bookmarking
- UI-based scoring for human evaluation

### Traces

A trace represents **one complete AI interaction**:

| Attribute | Description |
|-----------|-------------|
| `id` | Unique identifier (auto-generated) |
| `name` | Descriptive name (e.g., "chatbot-response") |
| `input` | What was sent to the AI |
| `output` | What the AI returned |
| `metadata` | Key-value pairs for custom data |
| `timestamp` | When the trace started |
| `session_id` | Optional link to a session |
| `user_id` | Optional user attribution |
| `tags` | Labels for filtering |

**Example:** User asks "What's the weather?" → AI responds "It's sunny" = one trace.

### Observations

Observations are **individual steps within a trace**:

| Attribute | Description |
|-----------|-------------|
| `id` | Unique identifier |
| `trace_id` | Parent trace reference |
| `type` | Observation type (see below) |
| `name` | Descriptive name |
| `start_time` | When the step started |
| `end_time` | When the step finished |
| `input` | Step input |
| `output` | Step output |
| `model` | Model used (for generations) |
| `usage` | Token counts |
| `cost` | Computed cost |

Observations can be **nested** to create hierarchical structures.

---

## Observation Types

Langfuse supports **10 observation types** to contextualize what each step does:

| Type | Purpose | Use Case |
|------|---------|----------|
| `span` | Duration of work units | Generic operations |
| `generation` | AI model outputs | LLM calls with prompts, tokens, costs |
| `event` | Point-in-time occurrences | Discrete events (no duration) |
| `agent` | Application flow decisions | Orchestrating tool usage |
| `tool` | Tool/API calls | Weather API, database queries |
| `chain` | Links between steps | Passing context retriever→LLM |
| `retriever` | Data retrieval operations | Vector store queries |
| `evaluator` | Quality assessment functions | Relevance/correctness scoring |
| `embedding` | Embedding generation | Text embeddings with token tracking |
| `guardrail` | Content protection | Jailbreak/malicious content detection |

**Most common types:**
- `generation` - Use for any LLM API call (enables cost tracking)
- `span` - Use for custom operations you want to time
- `tool` - Use for external API calls (weather, search, etc.)

**Analogy:** Observation types are like **categories in a detailed receipt**. A restaurant receipt separates food, drinks, and service—observation types separate LLM calls, tool uses, and other operations.

---

## Token & Cost Tracking

Token and cost tracking applies only to `generation` and `embedding` observation types.

### Ingesting Usage Data

You can explicitly provide usage data:

```python
langfuse.update_current_generation(
    usage_details={
        "input": response.usage.input_tokens,
        "output": response.usage.output_tokens,
        "total": 17
    },
    cost_details={
        "input": 0.01,
        "output": 0.02
    }
)
```

### Cost Inference

When you don't provide usage/cost data, Langfuse can **infer** it using:

1. **Model definitions** with regex matching
2. **Built-in tokenizers** (tiktoken for GPT, @anthropic-ai/tokenizer for Claude)
3. **Pricing configuration**

**Priority:** Ingested data always overrides inferred data.

**Limitation:** Reasoning models (o1, o3) cannot have costs inferred—you must ingest usage from the API response.

### Usage Detail Fields

| Field | Description |
|-------|-------------|
| `input` | Input/prompt tokens |
| `output` | Output/completion tokens |
| `total` | Total tokens (auto-derived if not provided) |
| `cached_tokens` | Cached token count |
| `cache_read_input_tokens` | Cache read tokens |
| `audio_tokens` | Audio processing tokens |
| `image_tokens` | Image processing tokens |
| `reasoning_tokens` | Reasoning model tokens |

**OpenAI compatibility:** Langfuse auto-maps OpenAI's usage format:
- `prompt_tokens` → `input`
- `completion_tokens` → `output`

---

## Metadata, Tags & User Tracking

### Adding Metadata

Metadata is key-value pairs attached to traces or observations:

```python
with propagate_attributes(
    metadata={"source": "api", "region": "us-east-1"}
):
    # All child observations inherit this metadata
    process_request()
```

**Constraints:**
| Attribute | Constraint |
|-----------|------------|
| `metadata` keys | Alphanumeric only |
| `metadata` values | Strings, max 200 chars |

### Adding Tags

Tags are labels for filtering:

```python
with propagate_attributes(
    tags=["production", "v2", "high-priority"]
):
    process_request()
```

**Constraint:** Max 200 chars per tag.

### User Tracking

Associate traces with users:

```python
with propagate_attributes(
    user_id="user_12345"
):
    process_request()
```

**Constraint:** Max 200 chars.

---

## Querying Traces

### Listing Traces

Basic listing with the skill:

```bash
# List 10 most recent traces
python scripts/langfuse.py trace list --limit 10

# List traces by name
python scripts/langfuse.py trace list --name "chatbot-response"
```

### Filtering

Available filters:

| Filter | Description | Example |
|--------|-------------|---------|
| `--limit` | Number of traces to return | `--limit 20` |
| `--name` | Filter by trace name | `--name chatbot` |
| `--user-id` | Filter by user | `--user-id user_123` |
| `--session-id` | Filter by session | `--session-id session_abc` |
| `--since` | Time window | `--since 24h` |

### Pagination

The skill uses cursor-based pagination internally (Langfuse v2 Observations API).

For large result sets:
- Results are returned in batches
- Progress indicator shown for fetches >5 seconds
- Use `--limit` to control batch size

---

## Analyzing Traces

### Latency Analysis

Find bottlenecks in your AI application:

```bash
python scripts/langfuse.py trace analyze <trace-id>
```

**What it shows:**
- Total trace duration
- Slowest observations (ranked)
- Percentage contribution to total time
- P50/P95/P99 percentiles (when analyzing multiple traces)

**Example output:**
```
Latency Analysis for trace abc123
================================
Total duration: 3.2s

Top bottlenecks:
1. embedding-lookup (span)    - 2.1s (65.6%)
2. gpt-4-completion (generation) - 0.8s (25.0%)
3. retrieval-step (retriever) - 0.3s (9.4%)

Insight: Your p95 latency is dominated by the embedding-lookup span.
Consider caching frequently accessed embeddings.
```

### Error Detection

Find traces with errors:

```bash
# Errors in last 24 hours
python scripts/langfuse.py trace errors --since 24h

# All recent errors
python scripts/langfuse.py trace errors --limit 20
```

**What it shows:**
- Trace ID with error
- Error message
- Timestamp
- Which observation failed

### Cost Breakdown

Understand your spending:

```bash
# Total costs
python scripts/langfuse.py trace costs

# By model
python scripts/langfuse.py trace costs --group-by model

# By time period
python scripts/langfuse.py trace costs --since 7d
```

**What it shows:**
- Total cost for the period
- Cost per model
- Top N most expensive traces

---

## Analogies for Non-Experts

### Traces are like detailed receipts

When you buy groceries, the receipt shows every item, its price, and the total. A trace does the same for AI requests—showing every step, its duration, and the total cost.

### Sessions are like conversation threads

Just like email threads group related messages, sessions group related traces. A user chatting with your AI over multiple messages creates one session with multiple traces.

### Observations are like line items

Each line on a receipt is one item. Each observation is one step in processing the AI request. Some steps are quick (like fetching from cache), others are slow (like calling GPT-4).

### Metadata is like notes on the receipt

When you write "business expense" on a receipt, that's metadata. In Langfuse, metadata helps you filter and understand your traces later.

### Cost tracking is like itemized billing

Some receipts show "food: $20, drinks: $10, tax: $3". Langfuse shows "input tokens: $0.01, output tokens: $0.02". You can see exactly where your money goes.

---

## Related Commands

| Command | What it does |
|---------|--------------|
| `trace list` | List recent traces |
| `trace get <id>` | Get full trace details |
| `trace analyze <id>` | Find bottlenecks |
| `trace errors` | Find errors |
| `trace costs` | View cost breakdown |

---

## Further Reading

- [Getting Started](getting-started.md) - Quick setup guide
- [Evals Reference](evals.md) - Score types and LLM-as-Judge
- [Datasets Reference](datasets.md) - Experiments and A/B testing
- [Langfuse Docs: Tracing](https://langfuse.com/docs/observability/overview) - Official documentation
