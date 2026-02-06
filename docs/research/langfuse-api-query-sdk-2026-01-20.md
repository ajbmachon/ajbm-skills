---
topic: "Langfuse API & Query via SDK"
researched: "2026-01-20"
query: "Langfuse API query traces SDK documentation - fetch_traces, fetch_observations, filtering, pagination, authentication"
expires: "2026-02-19"
sources:
  - "https://langfuse.com/docs/api-and-data-platform/overview"
  - "https://langfuse.com/docs/query-traces"
  - "https://langfuse.com/docs/api-and-data-platform/features/public-api"
  - "https://langfuse.com/docs/api-and-data-platform/features/observations-api"
  - "https://langfuse.com/docs/get-started"
  - "https://langfuse.com/docs/sdk/python/example"
  - "https://langfuse.com/docs/tracing/overview"
  - "https://langfuse.com/docs/scores/custom"
  - "https://langfuse.com/docs/prompts"
  - "https://langfuse.com/docs/datasets/overview"
  - "https://langfuse.com/docs/tracing-features/sessions"
  - "https://langfuse.com/docs/tracing-features/metadata"
  - "https://langfuse.com/docs/tracing-features/tags"
  - "https://langfuse.com/docs/sdk/python/sdk-v3"
---

# Langfuse API & Query via SDK Implementation Guide

**TL;DR:** Langfuse provides Python and JS/TS SDKs with `langfuse.api.*` methods for querying traces, observations, sessions, and scores. Use Basic Auth with public/secret keys. The v2 Observations API offers cursor-based pagination and selective field retrieval for better performance. New data is available within 15-30 seconds of ingestion.

**Researched:** 2026-01-20 | **Version:** SDK v3 / Platform 3.63.0+ | **Expires:** 2026-02-19

## Key Findings

- Langfuse is an "open, extensible and flexible" platform with Public API, SDK queries, UI export, and blob storage export [[source](https://langfuse.com/docs/api-and-data-platform/overview)]
- New data is typically available for querying within 15-30 seconds of ingestion [[source](https://langfuse.com/docs/query-traces)]
- SDK errors are caught and logged - "cannot break your application" [[source](https://langfuse.com/docs/sdk/python/sdk-v3)]
- Fully async requests add almost no latency to your application [[source](https://langfuse.com/docs/sdk/python/sdk-v3)]

## Authentication

Langfuse uses **Basic Authentication** with project-level credentials [[source](https://langfuse.com/docs/api-and-data-platform/features/public-api)]:

- **Username**: Langfuse Public Key (`pk-lf-...`)
- **Password**: Langfuse Secret Key (`sk-lf-...`)

### Environment Variables

```bash
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_BASE_URL="https://cloud.langfuse.com"  # EU region (default)
# or "https://us.cloud.langfuse.com" for US region
# or "https://hipaa.cloud.langfuse.com" for HIPAA region
```
[[source](https://langfuse.com/docs/get-started)]

### SDK Initialization

**Python:**
```python
from langfuse import get_client

# Auto-reads environment variables
langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated!")
```
[[source](https://langfuse.com/docs/sdk/python/example)]

**Direct instantiation (explicit config):**
```python
from langfuse import Langfuse

langfuse = Langfuse(
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    base_url="https://cloud.langfuse.com"
)
```
[[source](https://langfuse.com/docs/sdk/python/sdk-v3)]

## Querying Traces

**Python:**
```python
from langfuse import get_client
langfuse = get_client()

# List traces with filters
traces = langfuse.api.trace.list(
    limit=100,
    user_id="user_123",
    tags=["production"]
)

# Get single trace by ID
trace = langfuse.api.trace.get("traceId")
```
[[source](https://langfuse.com/docs/query-traces)]

**JavaScript/TypeScript:**
```javascript
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();
const traces = await langfuse.api.trace.list();
const trace = await langfuse.api.trace.get("traceId");
```
[[source](https://langfuse.com/docs/query-traces)]

## Querying Observations (v2 API - Recommended)

The v2 Observations API is optimized for performance with cursor-based pagination and selective field retrieval [[source](https://langfuse.com/docs/api-and-data-platform/features/observations-api)].

**Python:**
```python
observations = langfuse.api.observations_v_2.get_many(
    trace_id="abcdef1234",
    type="GENERATION",
    limit=100,
    fields="core,basic,usage"
)
```
[[source](https://langfuse.com/docs/query-traces)]

**JavaScript:**
```javascript
const observations = await langfuse.api.observationsV2.getMany({
    traceId: "abcdef1234",
    type: "GENERATION",
    limit: 100,
    fields: "core,basic,usage"
});
```
[[source](https://langfuse.com/docs/query-traces)]

### Available Field Groups

Use comma-separated `fields` parameter to select data groups [[source](https://langfuse.com/docs/api-and-data-platform/features/observations-api)]:

| Field Group | Description |
|-------------|-------------|
| `core` | Essential observation identifiers |
| `basic` | Basic observation data |
| `time` | Timestamps |
| `io` | Input/output content |
| `metadata` | Custom metadata |
| `model` | Model information |
| `usage` | Token usage details |
| `prompt` | Prompt references |
| `metrics` | Performance metrics |

**Key Point:** The v1 API returns all fields, forcing database scans of every column. Use v2 with selective fields for better performance [[source](https://langfuse.com/docs/api-and-data-platform/features/observations-api)].

## Filtering Parameters

Common filter parameters across query methods [[source](https://langfuse.com/docs/query-traces)] [[source](https://langfuse.com/docs/api-and-data-platform/features/observations-api)]:

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | int | Results per page (default 50, max 1,000) |
| `cursor` | string | Base64 pagination token |
| `user_id` | string | Filter by user identifier |
| `session_id` | string | Filter by session |
| `trace_id` | string | Filter by parent trace |
| `tags` | list | Filter by tags |
| `type` | string | Observation type: GENERATION, SPAN, EVENT |
| `name` | string | Filter by name |
| `level` | string | Filter by log level |
| `fromStartTime` / `toStartTime` | datetime | Time range filters |
| `parseIoAsJson` | bool | Parse input/output as JSON |

## Pagination Patterns

### Cursor-Based Pagination (v2 API)

```python
cursor = None
all_observations = []

while True:
    response = langfuse.api.observations_v_2.get_many(
        trace_id="trace-123",
        limit=100,
        cursor=cursor
    )

    all_observations.extend(response.data)

    # Check for next page
    cursor = response.meta.cursor if hasattr(response.meta, 'cursor') else None
    if not cursor:
        break  # No more pages
```

**Key Point:** When no cursor appears in the response metadata, you've reached the end of results [[source](https://langfuse.com/docs/api-and-data-platform/features/observations-api)].

## Other Queryable Resources

### Sessions
```python
sessions = langfuse.api.sessions.list(limit=50)
```
[[source](https://langfuse.com/docs/query-traces)]

**Session ID constraints** [[source](https://langfuse.com/docs/tracing-features/sessions)]:
- US-ASCII characters only
- Maximum 200 characters
- Exceeded values are dropped

### Scores
```python
scores = langfuse.api.score_v_2.get(score_ids="ScoreId")
```
[[source](https://langfuse.com/docs/query-traces)]

### Datasets
```python
# Create dataset
langfuse.create_dataset(name="my-dataset")

# Access via API
datasets = langfuse.api.datasets.list()
```
[[source](https://langfuse.com/docs/datasets/overview)]

### Metrics (Aggregated Queries)
```python
metrics = langfuse.api.metrics_v_2.get()
```
[[source](https://langfuse.com/docs/query-traces)]

## Creating/Updating Items via API

### Creating Scores

Three score data types are supported [[source](https://langfuse.com/docs/scores/custom)]:
- **Numeric**: Float values for quantitative measurements
- **Categorical**: String values for classifications
- **Boolean**: Binary 0/1 values

**Python:**
```python
langfuse.create_score(
    name="correctness",
    value=0.9,
    trace_id="trace_id_here",
    data_type="NUMERIC"
)
```
[[source](https://langfuse.com/docs/scores/custom)]

**JavaScript:**
```javascript
langfuse.score.create({
    traceId: message.traceId,
    name: "accuracy",
    value: 0.9,
    dataType: "NUMERIC"
});
```
[[source](https://langfuse.com/docs/scores/custom)]

**Preventing duplicates:** Use an `id` parameter as idempotency key [[source](https://langfuse.com/docs/scores/custom)].

### Creating Prompts

```python
langfuse.create_prompt(
    name="movie-critic",
    type="text",  # or "chat"
    prompt="As a {{criticlevel}} movie critic, do you like {{movie}}?",
    labels=["production"]
)
```
[[source](https://langfuse.com/docs/prompts)]

**Variable syntax:** Use `{{variable}}` (double braces) [[source](https://langfuse.com/docs/prompts)].

### Creating Dataset Items

```python
langfuse.create_dataset(name="evaluation-set")
# Items can be added via SDK, CSV import, or from production traces
```
[[source](https://langfuse.com/docs/datasets/overview)]

## Async Support

Python SDK provides async equivalents through `async_api` namespace [[source](https://langfuse.com/docs/query-traces)]:

```python
# Async queries
observations = await langfuse.async_api.observations_v_2.get_many(...)
```

## Best Practices

### Flushing in Short-Lived Applications

```python
# Always flush before shutdown in scripts/serverless
langfuse.flush()
```
[[source](https://langfuse.com/docs/sdk/python/sdk-v3)]

### Metadata Constraints

- Values limited to max 200 characters [[source](https://langfuse.com/docs/tracing-features/metadata)]
- Keys restricted to alphanumeric characters only [[source](https://langfuse.com/docs/tracing-features/metadata)]
- Invalid values are dropped with warnings [[source](https://langfuse.com/docs/tracing-features/metadata)]

### Tags Constraints

- Maximum 200 characters per tag [[source](https://langfuse.com/docs/tracing-features/tags)]
- Tags exceeding limit are dropped [[source](https://langfuse.com/docs/tracing-features/tags)]

### Platform Requirements

Python SDK v3 requires Langfuse platform version >= 3.63.0 for self-hosted deployments [[source](https://langfuse.com/docs/sdk/python/sdk-v3)].

## API Endpoints Reference

| Region | Base URL |
|--------|----------|
| Cloud EU | `https://cloud.langfuse.com/api/public` |
| Cloud US | `https://us.cloud.langfuse.com/api/public` |
| HIPAA US | `https://hipaa.cloud.langfuse.com/api/public` |

[[source](https://langfuse.com/docs/api-and-data-platform/features/public-api)]

### Direct API Example

```bash
curl -u pk-lf-xxx:sk-lf-xxx \
  "https://cloud.langfuse.com/api/public/projects"
```
[[source](https://langfuse.com/docs/api-and-data-platform/features/public-api)]

## Quick Reference

| Use Case | Pattern | Notes |
|----------|---------|-------|
| Initialize SDK | `langfuse = get_client()` | Auto-reads env vars |
| Query traces | `langfuse.api.trace.list(...)` | Supports filters |
| Query observations | `langfuse.api.observations_v_2.get_many(...)` | Use v2 for performance |
| Get single trace | `langfuse.api.trace.get("id")` | Returns full trace |
| Create score | `langfuse.create_score(...)` | NUMERIC/CATEGORICAL/BOOLEAN |
| Paginate results | Check `response.meta.cursor` | None = no more pages |
| Async queries | `langfuse.async_api.*` | Python async support |
| Flush on exit | `langfuse.flush()` | For short-lived apps |

## Sources

- [Langfuse API & Data Platform Overview](https://langfuse.com/docs/api-and-data-platform/overview)
- [Query Traces via SDK](https://langfuse.com/docs/query-traces)
- [Public API](https://langfuse.com/docs/api-and-data-platform/features/public-api)
- [Observations API](https://langfuse.com/docs/api-and-data-platform/features/observations-api)
- [Get Started](https://langfuse.com/docs/get-started)
- [Python SDK Example](https://langfuse.com/docs/sdk/python/example)
- [Tracing Overview](https://langfuse.com/docs/tracing/overview)
- [Scores via API/SDK](https://langfuse.com/docs/scores/custom)
- [Prompt Management](https://langfuse.com/docs/prompts)
- [Datasets Overview](https://langfuse.com/docs/datasets/overview)
- [Sessions](https://langfuse.com/docs/tracing-features/sessions)
- [Metadata](https://langfuse.com/docs/tracing-features/metadata)
- [Tags](https://langfuse.com/docs/tracing-features/tags)
- [Python SDK v3](https://langfuse.com/docs/sdk/python/sdk-v3)
- [API Reference](https://api.reference.langfuse.com)
- [OpenAPI Spec](https://cloud.langfuse.com/generated/api/openapi.yml)
