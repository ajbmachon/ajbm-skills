---
topic: "Langfuse Datasets & Experiments SDK API"
researched: "2026-01-20"
query: "Langfuse Datasets & Experiments (SDK API)"
expires: "2026-02-19"
sources:
  - "https://langfuse.com/docs/evaluation/experiments/datasets"
  - "https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk"
  - "https://langfuse.com/docs/evaluation/experiments/data-model"
  - "https://langfuse.com/docs/evaluation/experiments/overview"
  - "https://langfuse.com/changelog/2025-09-17-experiment-runner-sdk"
  - "https://langfuse.com/changelog/2024-11-21-all-new-datasets-and-evals-documentation"
  - "https://langfuse.com/changelog/2025-11-06-dataset-schema-enforcement"
  - "https://langfuse.com/guides/cookbook/datasets"
---

# Langfuse Datasets & Experiments SDK Implementation Guide

**TL;DR:** Langfuse provides two approaches for running experiments: (1) the new high-level `run_experiment()` method with automatic tracing and concurrent execution, and (2) the lower-level manual approach using `get_dataset()` with item iteration and `link()`. Datasets store test cases with input, expected_output, and metadata fields. Experiments link traces to dataset items for comparison and evaluation.

**Researched:** 2026-01-20 | **SDK Versions:** Python SDK v2.x+, JS/TS SDK v4.x+ | **Expires:** 2026-02-19

## Key Findings

- Langfuse introduced a new **Experiment Runner SDK** in September 2025 that simplifies running experiments with automatic tracing and concurrent execution [[source](https://langfuse.com/changelog/2025-09-17-experiment-runner-sdk)]
- Datasets support **JSON Schema enforcement** (added November 2025) for validating input and expected_output structure [[source](https://langfuse.com/changelog/2025-11-06-dataset-schema-enforcement)]
- Dataset items have three core fields: `input` (any JSON), `expected_output` (optional, any JSON), and `metadata` (optional, any JSON) [[source](https://langfuse.com/docs/evaluation/experiments/datasets)]
- Experiments are created by linking execution traces to dataset items with a `run_name` [[source](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk)]

## Data Model

### Dataset Structure

```
Dataset
├── name: string (unique identifier)
├── description: string (optional)
├── metadata: object (optional)
└── items: DatasetItem[]
    ├── id: string (auto-generated or custom)
    ├── input: any (JSON - the test input)
    ├── expected_output: any (JSON - ground truth, optional)
    ├── metadata: any (JSON - additional context, optional)
    └── status: "ACTIVE" | "ARCHIVED"
```

[[source](https://langfuse.com/docs/evaluation/experiments/data-model)]

### Experiment Run Structure

```
Dataset Run (Experiment)
├── name: string (identifies the experiment run)
├── description: string (optional)
├── metadata: object (optional, e.g., {model: "gpt-4o"})
└── items: DatasetRunItem[]
    ├── dataset_item_id: string (links to DatasetItem)
    ├── trace_id: string (links to execution trace)
    └── observation_id: string (optional, specific span)
```

[[source](https://langfuse.com/docs/evaluation/experiments/data-model)]

## Current Best Practice: Experiment Runner SDK (Recommended)

The new high-level SDK is the recommended approach for running experiments. It provides automatic tracing, concurrent execution, and built-in evaluation support.

### Python - Using run_experiment()

```python
from langfuse import Langfuse
from functools import partial

langfuse = Langfuse()

# Define your task function (receives dataset item, returns output)
def my_llm_task(item, model="gpt-4o"):
    # Your LLM application logic here
    response = call_my_llm(item.input, model=model)
    return response

# Define evaluators (optional)
def accuracy_evaluator(output, expected_output, item):
    return 1.0 if output == expected_output else 0.0

# Get the dataset
dataset = langfuse.get_dataset("my-test-dataset")

# Run the experiment with the high-level API
result = dataset.run_experiment(
    name="gpt-4o-baseline",
    description="Testing GPT-4o on our benchmark",
    task=partial(my_llm_task, model="gpt-4o"),
    evaluators=[accuracy_evaluator],
    metadata={"model": "gpt-4o", "temperature": 0.7}
)

# Print formatted results
print(result.format())
```

[[source](https://langfuse.com/changelog/2025-09-17-experiment-runner-sdk)]

**Key Points:**
- `run_experiment()` handles tracing automatically [[source](https://langfuse.com/changelog/2025-09-17-experiment-runner-sdk)]
- Supports concurrent execution for faster experiment runs [[source](https://langfuse.com/changelog/2025-09-17-experiment-runner-sdk)]
- Evaluators receive `(output, expected_output, item)` and return a score [[source](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk)]

### TypeScript - Using run_experiment()

```typescript
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

// Get dataset
const dataset = await langfuse.getDataset("my-test-dataset");

// Run experiment
const result = await dataset.runExperiment({
  name: "gpt-4o-baseline",
  description: "Testing GPT-4o on our benchmark",
  task: async (item) => {
    // Your LLM application logic
    const output = await runMyLLMApplication(item.input);
    return output;
  },
  evaluators: [
    async (output, expectedOutput, item) => {
      return output === expectedOutput ? 1.0 : 0.0;
    }
  ],
  metadata: { model: "gpt-4o" }
});

console.log(result.format());
```

[[source](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk)]

## Alternative: Manual Experiment Workflow

For more control, use the lower-level API with manual iteration and linking.

### Python - Manual Approach

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Get the dataset
dataset = langfuse.get_dataset("my-test-dataset")

# Iterate over items manually
for item in dataset.items:
    # Create a trace for this run
    trace = langfuse.trace(
        name="experiment-run",
        input=item.input
    )

    # Run your application
    output = run_my_llm_application(item.input)

    # Update trace with output
    trace.update(output=output)

    # Link the trace to the dataset item (creates the experiment run)
    item.link(
        trace,
        run_name="my-experiment-v1",
        run_description="Testing new prompt template",
        run_metadata={"model": "gpt-4o"}
    )

    # Optionally add scores
    langfuse.score(
        trace_id=trace.id,
        name="accuracy",
        value=compute_accuracy(output, item.expected_output),
        comment="Computed via exact match"
    )

# Flush to ensure all data is sent
langfuse.flush()
```

[[source](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk)]

### TypeScript - Manual Approach

```typescript
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

// Get dataset
const dataset = await langfuse.getDataset("my-test-dataset");

// Iterate over items
for (const item of dataset.items) {
  // Run application and get trace
  const [span, output] = await runMyLLMApplication(item.input, trace.id);

  // Link execution to dataset item
  await item.link(span, "my-experiment-v1", {
    description: "My first run",
    metadata: { model: "gpt-4o" }
  });

  // Add scores
  langfuse.score.trace(span, {
    name: "accuracy",
    value: myEvalFunction(item.input, output, item.expectedOutput),
    comment: "This is a comment"
  });
}

// Flush at the end
await langfuse.flush();
```

[[source](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk)]

## Creating Datasets

### Python SDK

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Create a new dataset
dataset = langfuse.create_dataset(
    name="qa-benchmark-v1",
    description="Question-answering benchmark dataset",
    metadata={"domain": "customer-support", "version": "1.0"}
)

# Add items to the dataset
langfuse.create_dataset_item(
    dataset_name="qa-benchmark-v1",
    input={"question": "What is your return policy?"},
    expected_output={"answer": "You can return items within 30 days..."},
    metadata={"category": "returns", "difficulty": "easy"}
)

# Add multiple items
items = [
    {
        "input": {"question": "How do I track my order?"},
        "expected_output": {"answer": "You can track your order at..."},
        "metadata": {"category": "shipping"}
    },
    {
        "input": {"question": "What payment methods do you accept?"},
        "expected_output": {"answer": "We accept credit cards, PayPal..."},
        "metadata": {"category": "payment"}
    }
]

for item in items:
    langfuse.create_dataset_item(
        dataset_name="qa-benchmark-v1",
        **item
    )
```

[[source](https://langfuse.com/docs/evaluation/experiments/datasets)]

### TypeScript SDK

```typescript
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient();

// Create dataset
await langfuse.api.datasets.create({
  name: "qa-benchmark-v1",
  description: "Question-answering benchmark dataset",
  metadata: { domain: "customer-support" }
});

// Create dataset item
await langfuse.api.datasetItems.create({
  datasetName: "qa-benchmark-v1",
  input: { question: "What is your return policy?" },
  expectedOutput: { answer: "You can return items within 30 days..." },
  metadata: { category: "returns" }
});
```

[[source](https://langfuse.com/docs/evaluation/experiments/datasets)]

## Managing Dataset Items

### Update Item Status (Archive)

```python
# Python - Archive an item
langfuse.api.dataset_items.update(
    dataset_item_id="item-123",
    status="ARCHIVED"
)
```

```typescript
// TypeScript - Archive an item
await langfuse.api.datasetItems.create({
  id: "item-123",
  status: "ARCHIVED"
});
```

[[source](https://langfuse.com/docs/evaluation/experiments/datasets)]

### Retrieve Dataset

```python
# Python
dataset = langfuse.get_dataset("qa-benchmark-v1")

# Access items
for item in dataset.items:
    print(f"Input: {item.input}")
    print(f"Expected: {item.expected_output}")
    print(f"Metadata: {item.metadata}")
```

[[source](https://langfuse.com/docs/evaluation/experiments/datasets)]

## Golden Datasets for Regression Testing

Create golden datasets from production traces for regression testing:

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Create a golden dataset for regression testing
dataset = langfuse.create_dataset(
    name="production-golden-set",
    description="Curated examples from production for regression testing",
    metadata={"purpose": "regression", "created_from": "production_traces"}
)

# Add items from production traces (via UI or API)
# You can also create items programmatically from trace data:
traces = langfuse.api.traces.list(limit=100)  # Get recent traces

for trace in traces.data:
    # Filter for high-quality examples (e.g., positive user feedback)
    if should_include_in_golden_set(trace):
        langfuse.create_dataset_item(
            dataset_name="production-golden-set",
            input=trace.input,
            expected_output=trace.output,
            metadata={
                "source_trace_id": trace.id,
                "collected_at": trace.timestamp
            }
        )
```

**Best Practices for Golden Datasets:**
- Include edge cases and failure modes [[source](https://langfuse.com/docs/evaluation/experiments/overview)]
- Add items with positive user feedback from production [[source](https://langfuse.com/changelog/2024-11-18-dataset-runs-comparison-view)]
- Use JSON Schema enforcement to maintain consistency [[source](https://langfuse.com/changelog/2025-11-06-dataset-schema-enforcement)]

## Anti-Patterns to Avoid

### Don't: Forget to flush at the end of experiments

```python
# BAD - Data may not be sent
for item in dataset.items:
    trace = langfuse.trace(...)
    # ... process item ...
    item.link(trace, "my-run")
# Missing flush!
```

### Do: Always flush after experiments

```python
# GOOD - Ensure all data is sent
for item in dataset.items:
    trace = langfuse.trace(...)
    # ... process item ...
    item.link(trace, "my-run")

langfuse.flush()  # Always flush at the end
```

[[source](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk)]

### Don't: Use inconsistent run names

```python
# BAD - Inconsistent naming creates separate runs
item1.link(trace1, "experiment-1")
item2.link(trace2, "experiment_1")  # Different name!
```

### Do: Use consistent run names across all items

```python
# GOOD - Same run_name groups items together
RUN_NAME = "experiment-v1"
for item in dataset.items:
    item.link(trace, RUN_NAME)
```

[[source](https://langfuse.com/docs/evaluation/experiments/data-model)]

## Quick Reference

| Use Case | Method | Notes |
|----------|--------|-------|
| Create dataset | `langfuse.create_dataset(name, description, metadata)` | Name must be unique |
| Add item | `langfuse.create_dataset_item(dataset_name, input, expected_output, metadata)` | All fields except dataset_name are optional |
| Get dataset | `langfuse.get_dataset(name)` | Returns dataset with items |
| Run experiment (recommended) | `dataset.run_experiment(name, task, evaluators)` | High-level API, auto-tracing |
| Link trace manually | `item.link(trace, run_name, run_description, run_metadata)` | Creates experiment run entry |
| Add score | `langfuse.score(trace_id, name, value, comment)` | Attach evaluation scores |
| Archive item | `langfuse.api.dataset_items.update(id, status="ARCHIVED")` | Soft delete |
| Flush data | `langfuse.flush()` | Always call at end of experiments |

## Sources

- [Datasets Documentation](https://langfuse.com/docs/evaluation/experiments/datasets)
- [Experiments via SDK](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk)
- [Experiments Data Model](https://langfuse.com/docs/evaluation/experiments/data-model)
- [Experiments Overview](https://langfuse.com/docs/evaluation/experiments/overview)
- [Experiment Runner SDK Changelog](https://langfuse.com/changelog/2025-09-17-experiment-runner-sdk)
- [Datasets & Evals Documentation Update](https://langfuse.com/changelog/2024-11-21-all-new-datasets-and-evals-documentation)
- [JSON Schema Enforcement for Datasets](https://langfuse.com/changelog/2025-11-06-dataset-schema-enforcement)
- [Datasets Cookbook](https://langfuse.com/guides/cookbook/datasets)
