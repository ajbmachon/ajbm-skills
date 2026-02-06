---
topic: "Langfuse Evaluation Core Concepts & Methods"
researched: "2026-01-20"
query: "Langfuse evaluation core concepts, score types, LLM-as-a-judge, programmatic scoring, annotation queues"
expires: "2026-02-19"
sources:
  - "https://langfuse.com/docs/evaluation/core-concepts"
  - "https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk"
  - "https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge"
  - "https://langfuse.com/docs/evaluation/evaluation-methods/annotation-queues"
  - "https://langfuse.com/docs/evaluation/evaluation-methods/score-analytics"
  - "https://langfuse.com/changelog/2025-10-16-llm-as-a-judge-execution-tracing"
  - "https://langfuse.com/changelog/2025-03-13-public-api-annotation-queues"
  - "https://langfuse.com/faq/all/manage-score-configs"
---

# Langfuse Evaluation Implementation Guide

**TL;DR:** Langfuse provides four evaluation methods: LLM-as-a-Judge (scalable automated evals), Annotation Queues (human review workflows), Scores via SDK/API (programmatic scoring), and Scores via UI (quick manual scoring). Scores support three data types: Numeric, Categorical, and Boolean. Score Configs enforce schema consistency. Score Analytics provides zero-config comparison and trend analysis.

**Researched:** 2026-01-20 | **Version:** Langfuse latest (v3.119.0+) | **Expires:** 2026-02-19

## Key Findings

- Scores can attach to Traces, Observations, Sessions, or Dataset Runs [[source](https://langfuse.com/docs/evaluation/core-concepts)]
- Three score data types: Numeric (float), Categorical (string), Boolean (0 or 1) [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]
- LLM-as-a-Judge requires models with structured output support [[source](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)]
- Every LLM-as-a-Judge execution creates a trace for debugging (v3.119.0+) [[source](https://langfuse.com/changelog/2025-10-16-llm-as-a-judge-execution-tracing)]
- Score Configs are immutable but can be archived/restored [[source](https://langfuse.com/faq/all/manage-score-configs)]
- Annotation Queues support session-level annotation for multi-turn conversations [[source](https://langfuse.com/changelog/2025-07-28-sessions-in-annotation-queues)]

## The Evaluation Loop

Langfuse supports both **offline evaluation** (testing against fixed datasets before deployment via Experiments) and **online evaluation** (scoring live production traces to catch issues). Edge cases found in production should be added back to datasets for future experiments [[source](https://langfuse.com/docs/evaluation/core-concepts)].

## Score Data Types

### Numeric Scores

Continuous float values for measurable metrics.

```python
from langfuse import get_client

langfuse = get_client()

langfuse.create_score(
    name="correctness",
    value=0.9,  # float value
    trace_id="trace_id_here",
    observation_id="observation_id_here",  # optional
    data_type="NUMERIC",  # optional, inferred if not provided
    comment="Factually correct",  # optional
)
```

**Key Points:**
- Value must be a float [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]
- Data type inferred if not provided [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]
- With Score Config, validated against min/max range [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]

### Categorical Scores

Discrete categories for classification-style evaluations.

```python
langfuse.create_score(
    name="accuracy",
    value="partially correct",  # string value
    trace_id="trace_id_here",
    data_type="CATEGORICAL",
    comment="Some factual errors",
)
```

**Key Points:**
- Value must be a string [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]
- Numeric mapping only produced if Score Config is provided [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]

### Boolean Scores

Binary true/false evaluations.

```python
langfuse.create_score(
    name="helpfulness",
    value=1,  # 0 or 1 as float
    trace_id="trace_id_here",
    data_type="BOOLEAN",  # REQUIRED for boolean
    comment="Helpful response",
)
```

**Key Points:**
- Value must be 0 or 1 (as float) [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]
- `data_type="BOOLEAN"` is REQUIRED (otherwise inferred as NUMERIC) [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]
- String representation (True/False) auto-populated on read [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]

## Score Attachment Targets

| Target | Use Case |
|--------|----------|
| `trace_id` | Evaluation of a single interaction (most common) |
| `observation_id` | Evaluation of a single observation below trace level |
| `session_id` | Comprehensive evaluation across multiple interactions |
| `datasetRunId` | Performance scores of a Dataset Run |

[[source](https://langfuse.com/docs/evaluation/core-concepts)]

## Score Configs (Schema Enforcement)

Score Configs standardize scoring schemas across teams. **Required for Annotation Queues, optional for SDK scoring.**

```python
# Creating a score with config enforcement
langfuse.create_score(
    trace_id="trace_id_here",
    name="accuracy",  # Must match config name
    value=0.9,
    config_id="78545-6565-3453654-43543",  # Validates against config
    data_type="NUMERIC",
)
```

**Validation Rules:**
- Score name must equal config name [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]
- Data type must match config (if provided) [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]
- Numeric: value within min/max range [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]
- Categorical: value must map to defined categories [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]
- Boolean: value must be 0 or 1 [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]

## Idempotent Score Updates

Prevent duplicate scores or update existing ones using an idempotency key:

```python
langfuse.create_score(
    trace_id="trace_id_here",
    name="correctness",
    value=0.9,
    score_id="trace_id_here-correctness",  # Idempotency key
)
```

**Pattern:** `<<trace_id>>-<<score_name>>` [[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]

## LLM-as-a-Judge Setup

### Step 1: Configure LLM Connection

Set up an LLM Connection in project settings. **The model MUST support structured output** for Langfuse to correctly interpret evaluation results [[source](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)].

### Step 2: Create Evaluator

Navigate to Evaluators page and click "+ Set up Evaluator".

**Two evaluator types:**

| Type | Description |
|------|-------------|
| **Managed Evaluator** | Pre-built evaluators (Hallucination, Context-Relevance, Toxicity, Helpfulness) from Langfuse and partners like Ragas |
| **Custom Evaluator** | Write your own evaluation prompt with `{{variables}}` placeholders |

[[source](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)]

### Step 3: Configure Data Scope

**For Live Data:**
- Choose new traces only, existing traces (backfill), or both
- Apply filters (trace name, tags, userId, etc.)
- Set sampling percentage to manage costs

**For Experiments:**
- Select evaluators when running via UI
- Configure in SDK code for programmatic experiments

[[source](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)]

### Step 4: Map Variables

Map trace/dataset properties to prompt variables:

| Prompt Variable | Common Mapping |
|-----------------|----------------|
| `{{input}}` | Trace input |
| `{{output}}` | Trace output / LLM response |
| `{{ground_truth}}` | Dataset item expected_output |

Use JSONPath for nested data: `$.choices[0].message.content` [[source](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)]

### Custom Evaluator Prompt Template

```
Evaluate the correctness of the generation on a continuous scale from 0 to 1.

Input:
Query: {{input}}
Generation: {{output}}
Ground truth: {{ground_truth}}

Think step by step.
```

**Output Schema (structured output):**
```json
{
  "score": "Score between 0 and 1",
  "reasoning": "One sentence reasoning for the score"
}
```

[[source](https://github.com/orgs/langfuse/discussions/9935)]

### Debugging LLM-as-a-Judge

Filter traces by environment `langfuse-llm-as-a-judge` to view execution traces [[source](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)].

**Execution Statuses:**
- **Completed**: Success
- **Error**: Failed (click trace ID for details)
- **Delayed**: Rate limited, retrying with exponential backoff
- **Pending**: Queued

[[source](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)]

## Annotation Queues (Human Review)

### Creating a Queue

1. Navigate to Annotation Queues
2. Create queue with name and description
3. **Select Score Configs** (defines scoring dimensions)
4. Assign users to queue

**Score Configs are REQUIRED** - create them first in Project Settings [[source](https://langfuse.com/docs/evaluation/evaluation-methods/annotation-queues)].

### Adding Items to Queue

**Bulk:** Select traces via checkboxes, use Actions dropdown to add to queue.

**Single:** Click "Annotate" dropdown on individual trace and select queue.

[[source](https://langfuse.com/docs/evaluation/evaluation-methods/annotation-queues)]

### Processing Workflow

Annotators work through items sequentially, scoring along defined dimensions and clicking "Complete + next" [[source](https://langfuse.com/docs/evaluation/evaluation-methods/annotation-queues)].

### Annotation Queue API Endpoints

```
GET  /api/public/annotation-queues              # Get all queues
GET  /api/public/annotation-queues/{queueId}    # Get queue by ID
GET  /api/public/annotation-queues/{queueId}/items           # Get queue items
POST /api/public/annotation-queues/{queueId}/items           # Add item
GET  /api/public/annotation-queues/{queueId}/items/{itemId}  # Get item
PATCH /api/public/annotation-queues/{queueId}/items/{itemId} # Update item
DELETE /api/public/annotation-queues/{queueId}/items/{itemId} # Remove item
```

[[source](https://langfuse.com/changelog/2025-03-13-public-api-annotation-queues)]

## Score Analytics

Zero-configuration analysis of evaluation data. Navigate to Scores > Analytics tab [[source](https://langfuse.com/docs/evaluation/evaluation-methods/score-analytics)].

### Single Score Analysis

- Distribution histogram/bar chart
- Trend over time
- Statistics: count, mean/mode, standard deviation

### Two-Score Comparison

Compare scores of the **same data type** to measure agreement [[source](https://langfuse.com/docs/evaluation/evaluation-methods/score-analytics)].

**Metrics for Numeric Scores:**
| Metric | Interpretation |
|--------|----------------|
| Pearson Correlation | 0.9-1.0: Very Strong, 0.7-0.9: Strong, 0.5-0.7: Moderate |
| Spearman Correlation | Rank-based, robust to outliers |
| MAE | Average absolute difference |
| RMSE | Penalizes larger errors |

**Metrics for Categorical/Boolean Scores:**
| Metric | Interpretation |
|--------|----------------|
| Cohen's Kappa | 0.81-1.0: Almost Perfect, 0.61-0.80: Substantial |
| F1 Score | Harmonic mean of precision/recall |
| Overall Agreement | Simple percentage match |

[[source](https://langfuse.com/docs/evaluation/evaluation-methods/score-analytics)]

### Matched vs All Data

- **Matched**: Only objects with BOTH scores (valid comparison)
- **All**: Complete distribution of each score (coverage analysis)

[[source](https://langfuse.com/docs/evaluation/evaluation-methods/score-analytics)]

## Anti-Patterns to Avoid

### Don't: Create boolean scores without explicit data_type

```python
# BAD - will be inferred as NUMERIC
langfuse.create_score(
    name="is_helpful",
    value=1,
    trace_id="..."
)
```

### Do: Always specify BOOLEAN data_type

```python
# GOOD - explicit boolean
langfuse.create_score(
    name="is_helpful",
    value=1,
    trace_id="...",
    data_type="BOOLEAN"
)
```

[[source](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)]

### Don't: Use LLM-as-a-Judge with models lacking structured output

This will cause parsing failures. Always verify structured output support [[source](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)].

## Quick Reference

| Use Case | Method | Notes |
|----------|--------|-------|
| Automated subjective evals at scale | LLM-as-a-Judge | Requires structured output model |
| Building ground truth datasets | Annotation Queues | Requires Score Configs |
| Quick spot checks | Scores via UI | Ad-hoc manual scoring |
| Custom eval pipelines | Scores via SDK | Full programmatic control |
| User feedback collection | Browser SDK | Capture in-app feedback |
| Guardrails/format checks | Scores via SDK | Deterministic checks |
| Comparing eval methods | Score Analytics | Same data type only |

## Evaluation Method Summary

| Method | Use When | Scoring Types |
|--------|----------|---------------|
| **LLM-as-a-Judge** | Subjective assessments at scale (tone, accuracy, helpfulness) | Numeric (0-1), structured reasoning |
| **Annotation Queues** | Building ground truth, systematic labeling, team collaboration | Per Score Config |
| **Scores via UI** | Quick quality spot checks, reviewing individual traces | Any |
| **Scores via API/SDK** | Custom evaluation pipelines, deterministic checks, automated workflows | Numeric, Categorical, Boolean |

[[source](https://langfuse.com/docs/evaluation/core-concepts)]

## Sources

- [Langfuse Evaluation Core Concepts](https://langfuse.com/docs/evaluation/core-concepts)
- [Scores via API/SDK](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)
- [LLM-as-a-Judge Evaluation](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)
- [Annotation Queues](https://langfuse.com/docs/evaluation/evaluation-methods/annotation-queues)
- [Score Analytics](https://langfuse.com/docs/evaluation/evaluation-methods/score-analytics)
- [LLM-as-a-Judge Execution Tracing Changelog](https://langfuse.com/changelog/2025-10-16-llm-as-a-judge-execution-tracing)
- [Public API for Annotation Queues](https://langfuse.com/changelog/2025-03-13-public-api-annotation-queues)
- [How to Create and Manage Score Configs](https://langfuse.com/faq/all/manage-score-configs)
- [GitHub Discussion: How evaluator prompts are combined](https://github.com/orgs/langfuse/discussions/9935)
