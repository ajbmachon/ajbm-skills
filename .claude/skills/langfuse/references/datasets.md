# Langfuse Datasets & Experiments Reference

> **Deep-dive documentation for datasets and experiments** | For quick start, see [getting-started.md](getting-started.md)

---

## Table of Contents

1. [Overview](#overview)
2. [Data Model](#data-model)
   - [Datasets](#datasets)
   - [Dataset Items](#dataset-items)
   - [Experiment Runs](#experiment-runs)
3. [Creating Datasets](#creating-datasets)
4. [Managing Dataset Items](#managing-dataset-items)
5. [Running Experiments](#running-experiments)
   - [Using run_experiment()](#using-run_experiment)
   - [Manual Experiment Workflow](#manual-experiment-workflow)
6. [Golden Datasets](#golden-datasets)
7. [Comparing Experiment Runs](#comparing-experiment-runs)
8. [Linking Traces to Dataset Items](#linking-traces-to-dataset-items)
9. [JSON Schema Enforcement](#json-schema-enforcement)
10. [Analogies for Non-Experts](#analogies-for-non-experts)

---

## Overview

**Datasets** and **Experiments** in Langfuse enable systematic testing and comparison of AI applications. Think of datasets as **test suites** and experiments as **test runs**.

**Key concepts:**
- **Dataset** = Collection of test cases (inputs + expected outputs)
- **Dataset Item** = One test case with input, expected output, and metadata
- **Experiment** = Running your AI against a dataset and recording results
- **Experiment Run** = Links execution traces to dataset items for comparison

**Why use datasets?**
- A/B test different prompts or models
- Catch regressions before deploying
- Build confidence with systematic testing
- Create reproducible benchmarks

---

## Data Model

### Datasets

A dataset is a named collection of test cases:

| Attribute | Description |
|-----------|-------------|
| `name` | Unique identifier (required) |
| `description` | Human-readable description |
| `metadata` | Key-value pairs for organization |
| `items` | Collection of dataset items |

**Example:**
```
Dataset: "customer-support-qa"
├── description: "Golden test cases for support chatbot"
├── metadata: {domain: "support", version: "2.0"}
└── items: [item1, item2, item3, ...]
```

### Dataset Items

Each item is one test case:

| Attribute | Description | Required |
|-----------|-------------|----------|
| `id` | Unique identifier (auto-generated or custom) | Auto |
| `input` | The test input (any JSON) | Yes |
| `expected_output` | Ground truth answer (any JSON) | No |
| `metadata` | Additional context (any JSON) | No |
| `status` | ACTIVE or ARCHIVED | Auto |

**Example item:**
```json
{
  "id": "item-123",
  "input": {"question": "What is your return policy?"},
  "expected_output": {"answer": "30-day returns with receipt..."},
  "metadata": {"category": "returns", "difficulty": "easy"}
}
```

### Experiment Runs

An experiment run links execution traces to dataset items:

| Attribute | Description |
|-----------|-------------|
| `name` | Identifier for this run (e.g., "gpt-4o-v1") |
| `description` | What this run tests |
| `metadata` | Run configuration (model, temperature, etc.) |
| `items` | Links between dataset items and traces |

**Example run:**
```
Experiment Run: "gpt-4o-baseline"
├── description: "Testing GPT-4o on support benchmark"
├── metadata: {model: "gpt-4o", temperature: 0.7}
└── items:
    ├── item-123 → trace-abc (linked execution)
    ├── item-456 → trace-def (linked execution)
    └── item-789 → trace-ghi (linked execution)
```

---

## Creating Datasets

### Via Skill

```bash
# Create a new dataset
python scripts/lf.py experiment create-dataset \
    --name "golden-cases" \
    --description "Curated test cases for regression testing"
```

### Via Python SDK

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Create dataset
dataset = langfuse.create_dataset(
    name="qa-benchmark-v1",
    description="Question-answering benchmark",
    metadata={"domain": "customer-support", "version": "1.0"}
)
```

**Naming best practices:**
- Use descriptive names: `customer-support-qa-v1`
- Include version numbers for tracking
- Avoid special characters

---

## Managing Dataset Items

### Adding Items via Skill

```bash
# Add a single item (interactive mode prompts for input/expected_output)
python scripts/lf.py experiment add-item --dataset golden-cases

# Add item with inline JSON
python scripts/lf.py experiment add-item \
    --dataset golden-cases \
    --input '{"question": "How do I reset my password?"}' \
    --expected-output '{"answer": "Click forgot password..."}' \
    --metadata '{"category": "account"}'
```

### Adding Items via SDK

```python
# Add single item
langfuse.create_dataset_item(
    dataset_name="qa-benchmark-v1",
    input={"question": "What is your return policy?"},
    expected_output={"answer": "30-day returns with receipt..."},
    metadata={"category": "returns", "difficulty": "easy"}
)

# Add multiple items
items = [
    {
        "input": {"question": "How do I track my order?"},
        "expected_output": {"answer": "You can track at..."},
        "metadata": {"category": "shipping"}
    },
    {
        "input": {"question": "What payment methods?"},
        "expected_output": {"answer": "We accept..."},
        "metadata": {"category": "payment"}
    }
]

for item in items:
    langfuse.create_dataset_item(
        dataset_name="qa-benchmark-v1",
        **item
    )
```

### Archiving Items

Items can be archived (soft deleted) rather than permanently removed:

```python
langfuse.api.dataset_items.update(
    dataset_item_id="item-123",
    status="ARCHIVED"
)
```

Archived items don't appear in normal queries but can be restored.

---

## Running Experiments

### Using run_experiment()

The **recommended approach** using the high-level API:

```bash
# Via skill
python scripts/lf.py experiment run \
    --dataset golden-cases \
    --name "gpt-4o-baseline"
```

```python
# Via Python SDK
from langfuse import Langfuse
from functools import partial

langfuse = Langfuse()

# Define your task function
def my_llm_task(item, model="gpt-4o"):
    # Your LLM application logic here
    response = call_my_llm(item.input, model=model)
    return response

# Define evaluators (optional)
def accuracy_evaluator(output, expected_output, item):
    return 1.0 if output == expected_output else 0.0

# Get dataset and run experiment
dataset = langfuse.get_dataset("golden-cases")
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

**Benefits of run_experiment():**
- Automatic tracing (no manual trace creation)
- Concurrent execution (faster experiments)
- Built-in evaluator support
- Automatic result formatting

### Manual Experiment Workflow

For more control, iterate manually:

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Get dataset
dataset = langfuse.get_dataset("golden-cases")

RUN_NAME = "gpt-4o-manual-v1"

# Iterate over items
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

    # Link trace to dataset item (creates experiment run)
    item.link(
        trace,
        run_name=RUN_NAME,
        run_description="Manual test run",
        run_metadata={"model": "gpt-4o"}
    )

    # Add scores
    langfuse.score(
        trace_id=trace.id,
        name="accuracy",
        value=compute_accuracy(output, item.expected_output),
        comment="Computed via exact match"
    )

# ALWAYS flush at the end
langfuse.flush()
```

**Important:** Always use consistent `run_name` across all items. Different names create separate experiment runs.

---

## Golden Datasets

**Golden datasets** are curated collections of high-quality test cases used for regression testing.

### Creating a Golden Dataset

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Create golden dataset
dataset = langfuse.create_dataset(
    name="production-golden-set",
    description="Curated examples for regression testing",
    metadata={"purpose": "regression", "created_from": "production"}
)
```

### Populating from Production Traces

The best golden datasets come from real production data:

```python
# Get recent production traces
traces = langfuse.api.traces.list(limit=100)

for trace in traces.data:
    # Filter for high-quality examples
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

### Best Practices for Golden Datasets

1. **Include edge cases** - Unusual inputs that might break
2. **Add failure modes** - Examples that have caused issues
3. **Use positive feedback** - Traces where users were satisfied
4. **Version your datasets** - Track changes over time
5. **Keep it manageable** - 50-200 items is often enough
6. **Update regularly** - Add new edge cases as discovered

---

## Comparing Experiment Runs

### Via Skill

```bash
# Compare two experiment runs
python scripts/lf.py experiment compare \
    --runs "gpt-4o-baseline,gpt-4-turbo-v1"
```

### Via Langfuse UI

1. Navigate to Datasets > Your Dataset
2. Select the "Runs" tab
3. Click on two runs to compare
4. View side-by-side comparisons

### Metrics to Compare

| Metric | What it tells you |
|--------|-------------------|
| Average score | Overall quality |
| Score distribution | Consistency |
| Latency | Speed |
| Cost | Expense |
| Error rate | Reliability |

---

## Linking Traces to Dataset Items

The `link()` method connects execution traces to dataset items, creating the experiment run:

```python
# Basic link
item.link(trace, run_name="my-experiment")

# Full link with all options
item.link(
    trace,
    run_name="gpt-4o-v2",
    run_description="Testing new system prompt",
    run_metadata={
        "model": "gpt-4o",
        "temperature": 0.7,
        "system_prompt_version": "v2"
    }
)
```

**What happens when you link:**
1. A dataset run is created (if it doesn't exist)
2. The trace is associated with the dataset item
3. You can now compare this execution against others

**Linking to specific observations:**
```python
# Link to a specific observation within the trace
item.link(
    trace,
    run_name="my-experiment",
    observation_id="specific-span-id"  # Optional
)
```

---

## JSON Schema Enforcement

Langfuse supports JSON Schema validation for dataset inputs and expected outputs.

**Benefits:**
- Ensures consistency across items
- Catches malformed data early
- Documents expected structure

**Setting up schemas:** Configure via Langfuse UI in Dataset settings.

**Example schema:**
```json
{
  "type": "object",
  "properties": {
    "question": {"type": "string"},
    "context": {"type": "string"}
  },
  "required": ["question"]
}
```

Items that don't match the schema will be rejected.

---

## Analogies for Non-Experts

### Datasets are like test suites

In software development, you have a test suite—a collection of tests that verify your code works. Datasets are the same for AI: a collection of inputs and expected outputs that verify your AI works.

### Dataset items are like test cases

Each test case checks one specific scenario. Each dataset item is one scenario: "Given this input, expect this output."

### Experiments are like test runs

When you run your test suite, you get a report. When you run an experiment, you get results showing how your AI performed on each test case.

### Golden datasets are like acceptance tests

Acceptance tests are the critical tests that must pass before shipping. Golden datasets are the critical AI scenarios that must work before deploying.

### run_experiment() is like pytest

pytest runs all your tests automatically and reports results. run_experiment() runs your AI on all dataset items automatically and reports scores.

### Linking traces is like logging test results

When a test runs, it logs what happened. Linking traces records exactly what your AI did for each test case, so you can debug failures.

### Comparing runs is like comparing test reports

"Version A had 95% pass rate, Version B had 87%." Comparing experiment runs shows you which prompt or model version performs better.

### Metadata is like test annotations

You might tag tests as "slow" or "critical". Metadata on dataset items helps you filter and organize: "easy", "edge-case", "customer-reported".

---

## Common Patterns

### Pattern 1: Regression Testing

```
1. Create golden dataset from production
2. Before deploying changes, run experiment
3. Compare against baseline
4. Block deploy if scores drop
```

### Pattern 2: A/B Testing Prompts

```
1. Create dataset with diverse test cases
2. Run experiment A (old prompt)
3. Run experiment B (new prompt)
4. Compare scores to pick winner
```

### Pattern 3: Model Comparison

```
1. Create dataset for your use case
2. Run experiment with Model A
3. Run experiment with Model B
4. Compare cost, latency, and quality
```

### Pattern 4: Continuous Evaluation

```
1. Add edge cases to dataset as discovered
2. Run experiments on every PR
3. Track scores over time
4. Alert on regressions
```

---

## Related Commands

| Command | What it does |
|---------|--------------|
| `experiment create-dataset` | Create a new dataset |
| `experiment add-item` | Add an item to a dataset |
| `experiment run` | Run experiment on dataset |
| `experiment compare` | Compare experiment runs |

---

## Further Reading

- [Getting Started](getting-started.md) - Quick setup guide
- [Traces Reference](traces.md) - Data model and observation types
- [Evals Reference](evals.md) - Score types and LLM-as-Judge
- [Langfuse Docs: Datasets](https://langfuse.com/docs/evaluation/experiments/datasets) - Official documentation
- [Langfuse Docs: Experiments](https://langfuse.com/docs/evaluation/experiments/overview) - Official documentation
