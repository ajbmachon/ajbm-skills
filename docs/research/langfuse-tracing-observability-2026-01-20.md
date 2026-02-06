---
topic: "Langfuse Tracing & Observability"
researched: "2026-01-20"
query: "Langfuse tracing observability data model traces spans generations sessions users metadata tags token cost tracking"
expires: "2026-02-19"
sources:
  - "https://langfuse.com/docs/observability/overview"
  - "https://langfuse.com/docs/observability/data-model"
  - "https://langfuse.com/docs/observability/features/observation-types"
  - "https://langfuse.com/docs/observability/features/token-and-cost-tracking"
  - "https://langfuse.com/docs/tracing-features/sessions"
  - "https://langfuse.com/docs/tracing-features/users"
  - "https://langfuse.com/docs/tracing-features/metadata"
  - "https://langfuse.com/docs/tracing-features/tags"
  - "https://langfuse.com/docs/observability/sdk/overview"
  - "https://langfuse.com/integrations/native/opentelemetry"
  - "https://langfuse.com/docs/observability/get-started"
---

# Langfuse Tracing & Observability Implementation Guide

**TL;DR:** Langfuse provides LLM observability through a hierarchical data model: Sessions contain Traces, which contain nested Observations (spans, generations, events, etc.). Built on OpenTelemetry, it offers decorator-based and context-manager instrumentation with automatic cost/token tracking.

**Researched:** 2026-01-20 | **SDK Versions:** Python >=3.3.1, TypeScript >=4.0.0 | **Expires:** 2026-02-19

## Data Model Hierarchy

The Langfuse data model consists of three hierarchical levels [[source](https://langfuse.com/docs/observability/data-model)]:

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

### Sessions

Sessions group multiple traces from the same user interaction [[source](https://langfuse.com/docs/tracing-features/sessions)]:

- **Purpose**: Group traces for chat threads, multi-turn conversations
- **Constraint**: `sessionId` must be US-ASCII string, max 200 characters
- **Features**: Public links, bookmarking, UI-based scoring

### Traces

A trace represents a single request or operation [[source](https://langfuse.com/docs/observability/data-model)]:

- Captures overall input/output plus request metadata
- Example: User question to chatbot response = one trace
- Contains nested observations representing individual steps

### Observations

Observations are individual steps within a trace [[source](https://langfuse.com/docs/observability/data-model)]:

- Can be nested to create hierarchical structures
- Support LLM-specific types (generations, tool calls, RAG steps)
- Built on OpenTelemetry spans internally

## Observation Types

Langfuse supports 10 observation types for contextualizing spans [[source](https://langfuse.com/docs/observability/features/observation-types)]:

| Type | Purpose | Use Case |
|------|---------|----------|
| `span` | Duration of work units | Generic operations |
| `generation` | AI model outputs | LLM calls with prompts, tokens, costs |
| `event` | Point-in-time occurrences | Discrete events in trace |
| `agent` | Application flow decisions | Orchestrating tool usage |
| `tool` | Tool/API calls | Weather API, database queries |
| `chain` | Links between steps | Passing context retriever->LLM |
| `retriever` | Data retrieval operations | Vector store queries |
| `evaluator` | Quality assessment functions | Relevance/correctness scoring |
| `embedding` | Embedding generation | Text embeddings with token tracking |
| `guardrail` | Content protection | Jailbreak/malicious content detection |

## Python SDK Setup

### Installation

```bash
pip install langfuse
```

### Environment Variables

```bash
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_BASE_URL="https://cloud.langfuse.com"  # EU region
# LANGFUSE_BASE_URL="https://us.cloud.langfuse.com"  # US region
```

### Client Initialization

```python
from langfuse import get_client

langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
```

Or with explicit credentials [[source](https://langfuse.com/docs/observability/get-started)]:

```python
from langfuse import Langfuse

langfuse = Langfuse(
    public_key="your-public-key",
    secret_key="your-secret-key",
    base_url="https://cloud.langfuse.com"
)
```

## Creating and Nesting Observations

### Method 1: Decorator Pattern

The `@observe()` decorator automatically captures inputs, outputs, timings, and errors [[source](https://langfuse.com/docs/sdk/python/decorators)]:

```python
from langfuse import observe

@observe()
def my_data_processing_function(data, parameter):
    return {"processed_data": data, "status": "ok"}

@observe(name="llm-call", as_type="generation")
async def my_async_llm_call(prompt_text):
    return "LLM response"
```

**Automatic nesting**: When decorated functions call other decorated functions, the trace structure reflects this hierarchy automatically.

### Method 2: Context Manager Pattern

```python
from langfuse import get_client

langfuse = get_client()

with langfuse.start_as_current_observation(
    as_type="span",
    name="process-request"
) as span:
    span.update(output="Processing complete")

    # Nested generation for LLM calls
    with langfuse.start_as_current_observation(
        as_type="generation",
        name="llm-response",
        model="gpt-3.5-turbo"
    ) as generation:
        generation.update(output="Generated response")

langfuse.flush()
```

### Method 3: Combined Decorator + Propagation

```python
from langfuse import observe, propagate_attributes

@observe()
def my_llm_pipeline(user_id: str, session_id: str):
    with propagate_attributes(
        user_id=user_id,
        session_id=session_id,
        metadata={"pipeline": "main"}
    ):
        result = call_llm()
        return result
```

## Adding Metadata, Tags, and User Info

### Attribute Propagation

Use `propagate_attributes()` to apply attributes to all child observations [[source](https://langfuse.com/docs/tracing-features/metadata)]:

```python
from langfuse import observe, propagate_attributes

@observe()
def process_request():
    with propagate_attributes(
        session_id="chat-session-123",
        user_id="user_12345",
        tags=["production", "v2"],
        metadata={"source": "api", "region": "us-east-1"}
    ):
        result = process_chat_message()
        return result
```

### Constraints

| Attribute | Constraint |
|-----------|------------|
| `session_id` | US-ASCII string, max 200 chars [[source](https://langfuse.com/docs/tracing-features/sessions)] |
| `user_id` | String, max 200 chars [[source](https://langfuse.com/docs/tracing-features/users)] |
| `tags` | Max 200 chars per tag, multiple allowed [[source](https://langfuse.com/docs/tracing-features/tags)] |
| `metadata` values | Strings, max 200 chars [[source](https://langfuse.com/docs/tracing-features/metadata)] |
| `metadata` keys | Alphanumeric only [[source](https://langfuse.com/docs/tracing-features/metadata)] |

**Important**: Call propagation early in your trace to ensure all observations are covered. Invalid values are dropped with warnings.

### Non-Propagated Updates

Add metadata to specific observations only:

```python
langfuse.update_current_span(metadata={"stage": "parsing"})
```

## Token and Cost Tracking

Token/cost tracking applies only to `generation` and `embedding` observation types [[source](https://langfuse.com/docs/observability/features/token-and-cost-tracking)].

### Ingesting Usage Data

```python
@observe(as_type="generation")
def anthropic_completion(**kwargs):
    # ... make API call ...

    langfuse.update_current_generation(
        usage_details={
            "input": response.usage.input_tokens,
            "output": response.usage.output_tokens,
            "cache_read_input_tokens": 2,
            "total": 17
        },
        cost_details={
            "input": 0.01,
            "output": 0.02,
            "cache_read_input_tokens": 0.005
        }
    )
```

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

### OpenAI Schema Compatibility

Langfuse auto-maps OpenAI usage format [[source](https://langfuse.com/docs/observability/features/token-and-cost-tracking)]:

- `prompt_tokens` -> `input`
- `completion_tokens` -> `output`
- `prompt_tokens_details.*` -> `input_*` prefix
- `completion_tokens_details.*` -> `output_*` prefix

### Cost Inference

When usage/cost aren't ingested, Langfuse infers them using:

1. Model definitions with regex matching
2. Built-in tokenizers (tiktoken for GPT, @anthropic-ai/tokenizer for Claude)
3. Pricing configuration

**Priority**: Ingested data always overrides inferred data.

**Limitation**: Reasoning models (o1, o3) cannot have costs inferred; usage must be ingested from API response.

## Session Management

### Creating Sessions

```python
from langfuse import observe, propagate_attributes

@observe()
def handle_chat_turn(session_id: str, user_message: str):
    with propagate_attributes(session_id=session_id):
        # All child observations inherit session_id
        response = process_message(user_message)
        return response

# Multiple calls with same session_id group together
handle_chat_turn("conversation-abc-123", "Hello")
handle_chat_turn("conversation-abc-123", "How are you?")
handle_chat_turn("conversation-abc-123", "Goodbye")
```

### Session Features

- Session replay view in UI
- Public sharing links
- Bookmarking
- UI-based scoring for human evaluation

## Distributed Tracing (OpenTelemetry)

Langfuse is built on OpenTelemetry, enabling distributed tracing [[source](https://langfuse.com/integrations/native/opentelemetry)]:

### Direct OTEL Endpoint

```bash
OTEL_EXPORTER_OTLP_ENDPOINT="https://cloud.langfuse.com/api/public/otel"
OTEL_EXPORTER_OTLP_HEADERS="Authorization=Basic ${AUTH_STRING}"
```

Authentication uses Base64-encoded API key pairs via Basic Auth.

### Attribute Mapping

- `langfuse.*` prefixed attributes -> top-level Langfuse fields
- Standard OTel attributes -> `metadata.attributes`
- Resource attributes -> `metadata.resourceAttributes`

### Context Propagation

Use OpenTelemetry Baggage with BaggageSpanProcessor to propagate trace-level attributes across all spans.

**Security note**: Baggage propagates to downstream services - avoid sensitive data.

## Anti-Patterns to Avoid

### Don't: Forget to flush in short-lived apps

```python
# BAD - data may be lost
def lambda_handler(event, context):
    with langfuse.start_as_current_observation(...) as span:
        process(event)
    # Missing flush!
```

### Do: Always flush before termination

```python
# GOOD - ensures data transmission
def lambda_handler(event, context):
    with langfuse.start_as_current_observation(...) as span:
        process(event)
    langfuse.flush()  # Required for short-lived apps
```

### Don't: Propagate attributes late in the trace

```python
# BAD - early observations miss attributes
@observe()
def process():
    early_step()  # No session_id!
    with propagate_attributes(session_id="..."):
        late_step()  # Has session_id
```

### Do: Propagate early

```python
# GOOD - all observations covered
@observe()
def process():
    with propagate_attributes(session_id="..."):
        early_step()  # Has session_id
        late_step()   # Has session_id
```

## Performance Considerations

- SDK requests are fully async, adding almost no latency [[source](https://langfuse.com/docs/observability/sdk/overview)]
- SDK errors are caught and logged, preventing application disruption
- Disable I/O capture for large payloads: `capture_input=False`, `capture_output=False`
- Environment variable: `LANGFUSE_OBSERVE_DECORATOR_IO_CAPTURE_ENABLED=false`

## Quick Reference

| Use Case | Pattern | Notes |
|----------|---------|-------|
| Basic function tracing | `@observe()` | Auto-captures I/O, timing |
| LLM call | `@observe(as_type="generation")` | Enables token/cost tracking |
| Tool invocation | `@observe(as_type="tool")` | Marks as tool call |
| Add session | `propagate_attributes(session_id="...")` | Groups traces |
| Add user | `propagate_attributes(user_id="...")` | User attribution |
| Add metadata | `propagate_attributes(metadata={...})` | Key-value pairs |
| Add tags | `propagate_attributes(tags=[...])` | Filtering labels |
| Manual span | `langfuse.start_as_current_observation()` | Context manager |
| Update current | `langfuse.update_current_span()` | Mid-execution updates |
| Ensure delivery | `langfuse.flush()` | Required for short-lived apps |

## Sources

- [Langfuse Observability Overview](https://langfuse.com/docs/observability/overview)
- [Tracing Data Model](https://langfuse.com/docs/observability/data-model)
- [Observation Types](https://langfuse.com/docs/observability/features/observation-types)
- [Token and Cost Tracking](https://langfuse.com/docs/observability/features/token-and-cost-tracking)
- [Sessions](https://langfuse.com/docs/tracing-features/sessions)
- [User Tracking](https://langfuse.com/docs/tracing-features/users)
- [Metadata](https://langfuse.com/docs/tracing-features/metadata)
- [Tags](https://langfuse.com/docs/tracing-features/tags)
- [SDK Overview](https://langfuse.com/docs/observability/sdk/overview)
- [OpenTelemetry Integration](https://langfuse.com/integrations/native/opentelemetry)
- [Get Started](https://langfuse.com/docs/observability/get-started)
