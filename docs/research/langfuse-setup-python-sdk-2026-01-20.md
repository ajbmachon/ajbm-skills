---
topic: "Langfuse Python SDK Setup & Configuration"
researched: "2026-01-20"
query: "Langfuse setup Python SDK installation environment variables initialization tracing patterns"
expires: "2026-02-19"
sources:
  - "https://langfuse.com/docs/get-started"
  - "https://langfuse.com/docs/sdk/python"
  - "https://langfuse.com/docs/sdk/python/decorators"
  - "https://langfuse.com/docs/sdk/python/low-level-sdk"
  - "https://langfuse.com/docs/sdk/python/example"
  - "https://langfuse.com/docs/integrations/openai/python/get-started"
  - "https://langfuse.com/docs/tracing-features/sessions"
  - "https://langfuse.com/docs/tracing-features/users"
  - "https://langfuse.com/docs/tracing-features/metadata"
  - "https://langfuse.com/docs/tracing-features/tags"
  - "https://langfuse.com/changelog"
---

# Langfuse Python SDK Setup & Configuration

**TL;DR:** Install via `pip install langfuse`, configure three environment variables, use `@observe` decorator for automatic tracing or `get_client()` with context managers for manual control. Call `flush()` before shutdown in short-lived applications.

**Researched:** 2026-01-20 | **SDK Version:** v3+ | **Expires:** 2026-02-19

## Key Findings

- SDK is built on OpenTelemetry, enabling automatic context propagation across nested spans [[source](https://langfuse.com/docs/sdk/python)]
- Fully async requests mean Langfuse adds almost no latency to applications [[source](https://langfuse.com/docs/sdk/python)]
- Non-breaking error handling ensures SDK issues don't affect application behavior [[source](https://langfuse.com/docs/sdk/python)]
- Python SDK v3 requires Langfuse platform >= 3.63.0 for self-hosted deployments [[source](https://langfuse.com/docs/sdk/python)]

## Installation

```bash
pip install langfuse
```

For OpenAI integration:
```bash
pip install langfuse openai
```

OpenAI integration requires SDK version >= 0.27.8; full async/streaming support requires >= 1.0.0 [[source](https://langfuse.com/docs/integrations/openai/python/get-started)]

## Environment Variables

Configure in your `.env` file or system environment:

```bash
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_BASE_URL="https://cloud.langfuse.com"  # EU region (default)
# LANGFUSE_BASE_URL="https://us.cloud.langfuse.com"  # US region
```

| Variable | Description | Required |
|----------|-------------|----------|
| `LANGFUSE_SECRET_KEY` | Server-side secret key (starts with `sk-lf-`) | Yes |
| `LANGFUSE_PUBLIC_KEY` | Public key (starts with `pk-lf-`) | Yes |
| `LANGFUSE_BASE_URL` | API endpoint URL | No (defaults to EU) |
| `LANGFUSE_OBSERVE_DECORATOR_IO_CAPTURE_ENABLED` | Disable I/O capture globally | No |

[[source](https://langfuse.com/docs/get-started)]

## Client Initialization

### Singleton Pattern (Recommended)

```python
from langfuse import get_client

langfuse = get_client()
```

The client automatically reads environment variables. Call `get_client()` anywhere in your app for the same instance [[source](https://langfuse.com/docs/sdk/python)]

### Direct Initialization

```python
from langfuse import Langfuse

langfuse = Langfuse(
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    base_url="https://cloud.langfuse.com"
)
```

[[source](https://langfuse.com/docs/sdk/python/example)]

## Decorator-Based Tracing (@observe)

The `@observe()` decorator automatically captures inputs, outputs, timings, and errors [[source](https://langfuse.com/docs/sdk/python/decorators)]

### Basic Usage

```python
from langfuse import observe

@observe()
def my_data_processing_function(data, parameter):
    return {"processed_data": data, "status": "ok"}

@observe(name="llm-call", as_type="generation")
async def my_async_llm_call(prompt_text):
    return "LLM response"
```

### Decorator Parameters

| Parameter | Purpose | Default |
|-----------|---------|---------|
| `name` | Custom identifier for the observation | Function name |
| `as_type` | Observation type: `"generation"`, `"span"`, `"tool"` | `"span"` |
| `capture_input` | Enable/disable input capture | `True` |
| `capture_output` | Enable/disable output capture | `True` |

[[source](https://langfuse.com/docs/sdk/python/decorators)]

### Nested Traces (Automatic)

```python
@observe()
def inner_function(data):
    return {"processed": data}

@observe()
def outer_function(data):
    # Automatically creates parent-child relationship
    return inner_function(data)
```

Nested `@observe` decorated functions create child observations automatically through the call stack [[source](https://langfuse.com/docs/sdk/python/decorators)]

### Performance Optimization

Disable I/O capture for high-volume scenarios:

```python
@observe(capture_input=False, capture_output=False)
def high_frequency_function(large_payload):
    pass
```

Or globally via environment variable:
```bash
LANGFUSE_OBSERVE_DECORATOR_IO_CAPTURE_ENABLED=false
```

[[source](https://langfuse.com/docs/sdk/python/decorators)]

## Manual Tracing (Context Managers)

For fine-grained control, use context managers with `get_client()` [[source](https://langfuse.com/docs/sdk/python/low-level-sdk)]

### Basic Span

```python
from langfuse import get_client

langfuse = get_client()

with langfuse.start_as_current_observation(
    as_type="span",
    name="process-request"
) as span:
    # Your code here
    span.update(output="Processing complete")
```

### Nested Observations

```python
with langfuse.start_as_current_observation(
    as_type="span",
    name="process-request"
) as span:
    span.update(output="Processing complete")

    with langfuse.start_as_current_observation(
        as_type="generation",
        name="llm-response",
        model="gpt-3.5-turbo"
    ) as generation:
        generation.update(output="Generated response")

langfuse.flush()
```

[[source](https://langfuse.com/docs/sdk/python/example)]

## Attribute Propagation

Propagate user IDs, session IDs, metadata, and tags across nested traces:

```python
from langfuse import observe, propagate_attributes

@observe()
def my_llm_pipeline(user_id: str, session_id: str):
    with propagate_attributes(
        user_id=user_id,
        session_id=session_id,
        tags=["production", "v2"],
        metadata={"pipeline": "main", "region": "us-east-1"}
    ):
        result = call_llm()
        return result
```

**Constraints:**
- Values must be strings <= 200 characters [[source](https://langfuse.com/docs/tracing-features/users)]
- Metadata keys: alphanumeric characters only [[source](https://langfuse.com/docs/tracing-features/metadata)]
- Invalid values are dropped with a warning [[source](https://langfuse.com/docs/tracing-features/metadata)]

Call `propagate_attributes()` early in your trace to ensure all observations are covered [[source](https://langfuse.com/docs/tracing-features/sessions)]

## Sessions and User Tracking

### Setting Session ID

```python
from langfuse import observe, propagate_attributes

@observe()
def process_chat_message(session_id: str, user_id: str):
    with propagate_attributes(
        session_id=session_id,
        user_id=user_id
    ):
        # All child observations inherit these attributes
        return generate_response()
```

Session IDs can be any US-ASCII character string < 200 characters [[source](https://langfuse.com/docs/tracing-features/sessions)]

### Non-Propagated Metadata

Add metadata to specific observations only:

```python
langfuse.update_current_span(metadata={"stage": "parsing"})
```

Or via the span object:

```python
with langfuse.start_as_current_observation(as_type="span", name="process") as span:
    span.update(metadata={"stage": "parsing"})
```

[[source](https://langfuse.com/docs/tracing-features/metadata)]

## OpenAI Integration

Drop-in replacement for automatic tracing [[source](https://langfuse.com/docs/integrations/openai/python/get-started)]

```python
# Replace this:
# import openai

# With this:
from langfuse.openai import openai

# Or import specific clients:
from langfuse.openai import OpenAI, AsyncOpenAI, AzureOpenAI
```

Alternative programmatic configuration:

```python
openai.langfuse_public_key = "pk-lf-..."
openai.langfuse_secret_key = "sk-lf-..."
openai.langfuse_enabled = True
```

Automatically captures all prompts/completions, latencies, errors, model usage, and USD costs [[source](https://langfuse.com/docs/integrations/openai/python/get-started)]

## Flush/Shutdown Patterns

### When to Flush

Call `langfuse.flush()` in short-lived applications (scripts, serverless functions, CLI tools) to ensure all events transmit before shutdown [[source](https://langfuse.com/docs/sdk/python)]

```python
from langfuse import get_client

langfuse = get_client()

# Your tracing code here
with langfuse.start_as_current_observation(as_type="span", name="task"):
    do_work()

# Critical for short-lived apps
langfuse.flush()
```

### Long-Running Applications

For web servers and persistent applications, the SDK handles batching and transmission automatically. No explicit flush required during normal operation [[source](https://langfuse.com/docs/sdk/python)]

## Observation Types

The SDK supports multiple observation types via `as_type` parameter:

| Type | Use Case |
|------|----------|
| `span` | Generic operations (default) |
| `generation` | LLM calls with model info |
| `tool` | Tool/function executions |
| `agent` | Agent orchestration |
| `chain` | Workflow chains |
| `retriever` | RAG retrieval steps |
| `evaluator` | Evaluation operations |
| `embedding` | Embedding generation |
| `guardrail` | Safety checks |

Enhanced observation types added August 2025 for more meaningful span context [[source](https://langfuse.com/changelog)]

## Quick Reference

| Use Case | Pattern | Notes |
|----------|---------|-------|
| Auto-trace functions | `@observe()` | Captures I/O, timing, errors |
| LLM generation | `@observe(as_type="generation")` | Include model info |
| Manual spans | `langfuse.start_as_current_observation()` | Context manager |
| User tracking | `propagate_attributes(user_id=...)` | <= 200 chars |
| Session grouping | `propagate_attributes(session_id=...)` | <= 200 chars |
| Add metadata | `propagate_attributes(metadata={...})` | Alphanumeric keys |
| Add tags | `propagate_attributes(tags=[...])` | List of strings |
| Disable I/O capture | `@observe(capture_input=False)` | Performance optimization |
| Ensure delivery | `langfuse.flush()` | Before app exit |
| OpenAI auto-trace | `from langfuse.openai import openai` | Drop-in replacement |

## Anti-Patterns to Avoid

### Don't: Forget to flush in scripts

```python
# Bad - events may not be sent
langfuse = get_client()
with langfuse.start_as_current_observation(as_type="span", name="task"):
    do_work()
# Script exits, events lost
```

### Do: Always flush before exit

```python
# Good - ensures delivery
langfuse = get_client()
with langfuse.start_as_current_observation(as_type="span", name="task"):
    do_work()
langfuse.flush()
```

### Don't: Call propagate_attributes late

```python
# Bad - early observations miss attributes
@observe()
def process():
    early_step()  # No user_id attached
    with propagate_attributes(user_id="user123"):
        late_step()  # Has user_id
```

### Do: Propagate attributes early

```python
# Good - all observations get attributes
@observe()
def process():
    with propagate_attributes(user_id="user123"):
        early_step()  # Has user_id
        late_step()   # Has user_id
```

## Recent Changes (2025-2026)

- **December 2025**: v2 Metrics and Observations API (Beta) with cursor-based pagination [[source](https://langfuse.com/changelog)]
- **October 2025**: Langchain v1 support with backward compatibility [[source](https://langfuse.com/changelog)]
- **September 2025**: Experiment Runner SDK for dataset-based experiments [[source](https://langfuse.com/changelog)]
- **August 2025**: Enhanced observation types (Agent, Tool, Chain, Retriever, etc.) [[source](https://langfuse.com/changelog)]
- **August 2025**: TypeScript SDK v4 GA with OpenTelemetry architecture [[source](https://langfuse.com/changelog)]

No breaking changes documented for Python SDK in this period [[source](https://langfuse.com/changelog)]

## Sources

- [Langfuse Get Started Guide](https://langfuse.com/docs/get-started)
- [Python SDK Overview](https://langfuse.com/docs/sdk/python)
- [Decorator Documentation](https://langfuse.com/docs/sdk/python/decorators)
- [Low-Level SDK Guide](https://langfuse.com/docs/sdk/python/low-level-sdk)
- [Code Examples](https://langfuse.com/docs/sdk/python/example)
- [OpenAI Integration](https://langfuse.com/docs/integrations/openai/python/get-started)
- [Sessions Feature](https://langfuse.com/docs/tracing-features/sessions)
- [User Tracking](https://langfuse.com/docs/tracing-features/users)
- [Metadata Feature](https://langfuse.com/docs/tracing-features/metadata)
- [Tags Feature](https://langfuse.com/docs/tracing-features/tags)
- [Changelog](https://langfuse.com/changelog)
