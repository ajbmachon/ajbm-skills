# Langfuse Evaluations Reference

> **Deep-dive documentation for the evaluation domain** | For quick start, see [getting-started.md](getting-started.md)

---

## Table of Contents

1. [Overview](#overview)
2. [The Evaluation Loop](#the-evaluation-loop)
3. [Score Types](#score-types)
   - [Numeric Scores](#numeric-scores)
   - [Categorical Scores](#categorical-scores)
   - [Boolean Scores](#boolean-scores)
4. [Score Attachment Targets](#score-attachment-targets)
5. [Score Configs](#score-configs)
6. [Evaluation Methods](#evaluation-methods)
   - [LLM-as-a-Judge](#llm-as-a-judge)
   - [Annotation Queues](#annotation-queues)
   - [Scores via SDK](#scores-via-sdk)
   - [Scores via UI](#scores-via-ui)
7. [Score Analytics](#score-analytics)
8. [Analogies for Non-Experts](#analogies-for-non-experts)

---

## Overview

**Evaluations** in Langfuse let you measure and track the quality of your AI outputs. Think of them as **unit tests for AI responses**—they tell you whether your AI is doing well or needs improvement.

**Key concepts:**
- **Score** = A quality measurement attached to a trace, observation, or session
- **Evaluator** = Something that produces scores (human, LLM, or code)
- **Score Config** = Schema that defines allowed score values
- **Annotation Queue** = Workflow for human reviewers to score traces

**Why evaluate?**
- Catch quality regressions before users do
- Compare different prompts or models objectively
- Build ground truth datasets from human feedback
- Automate quality monitoring at scale

---

## The Evaluation Loop

Langfuse supports both **offline** and **online** evaluation:

```
                    ┌──────────────────────────────────┐
                    │     OFFLINE EVALUATION           │
                    │  (Before deployment)             │
                    │  - Test against datasets         │
                    │  - Compare model versions        │
                    │  - Validate prompt changes       │
                    └──────────────────────────────────┘
                                 ↓
                         Deploy to Production
                                 ↓
                    ┌──────────────────────────────────┐
                    │     ONLINE EVALUATION            │
                    │  (In production)                 │
                    │  - Score live traces             │
                    │  - Monitor quality metrics       │
                    │  - Catch issues early            │
                    └──────────────────────────────────┘
                                 ↓
                    ┌──────────────────────────────────┐
                    │     FEEDBACK LOOP                │
                    │  - Add edge cases to datasets    │
                    │  - Refine evaluation criteria    │
                    │  - Improve prompts/models        │
                    └──────────────────────────────────┘
```

**Best practice:** Edge cases found in production should be added back to datasets for future experiments.

---

## Score Types

Langfuse supports three score data types:

### Numeric Scores

Continuous float values for measurable metrics.

```bash
python scripts/langfuse.py evaluate score <trace-id> \
    --name correctness \
    --value 0.85 \
    --data-type numeric
```

**Use cases:**
- Relevance scores (0.0 to 1.0)
- Confidence levels
- Similarity metrics
- Custom numeric ratings

**With Score Config:** Validated against min/max range.

### Categorical Scores

Discrete categories for classification-style evaluations.

```bash
python scripts/langfuse.py evaluate score <trace-id> \
    --name accuracy \
    --value "partially correct" \
    --data-type categorical
```

**Use cases:**
- Quality tiers (excellent, good, fair, poor)
- Intent classification
- Sentiment labels
- Error categories

**With Score Config:** Value must match one of the defined categories.

### Boolean Scores

Binary true/false evaluations.

```bash
python scripts/langfuse.py evaluate score <trace-id> \
    --name is_helpful \
    --value 1 \
    --data-type boolean
```

**Important:** You MUST specify `--data-type boolean`. Without it, the value is inferred as numeric.

**Use cases:**
- Yes/no judgments
- Pass/fail checks
- Binary quality gates
- Contains/doesn't contain checks

---

## Score Attachment Targets

Scores can attach to different objects:

| Target | Use Case | Example |
|--------|----------|---------|
| `trace_id` | Evaluate a single interaction | "Was this response helpful?" |
| `observation_id` | Evaluate a specific step | "Was this tool call correct?" |
| `session_id` | Evaluate across multiple turns | "How was the overall conversation?" |
| `dataset_run_id` | Evaluate experiment performance | "How did this prompt version perform?" |

**Most common:** Attaching scores to traces (one score per AI interaction).

---

## Score Configs

Score Configs standardize scoring schemas across your team. They define:
- Score name
- Data type (numeric, categorical, boolean)
- Allowed values (min/max for numeric, categories for categorical)

**Required for:** Annotation Queues
**Optional for:** SDK scoring (but recommended for consistency)

**Example config:**

| Name | Type | Values |
|------|------|--------|
| correctness | Numeric | 0.0 - 1.0 |
| quality | Categorical | excellent, good, fair, poor |
| is_on_topic | Boolean | 0 or 1 |

**Why use configs?**
- Enforce consistent scoring across team members
- Prevent typos in score names
- Enable automatic validation
- Power analytics and comparisons

**Note:** Score Configs are immutable but can be archived/restored.

---

## Evaluation Methods

### LLM-as-a-Judge

Use another LLM to automatically evaluate your AI's outputs.

**How it works:**
1. Configure an LLM connection (must support structured output)
2. Create an evaluator with a prompt template
3. Map trace data to prompt variables
4. LLM evaluates and returns structured scores

**Example evaluator prompt:**

```
Evaluate the correctness of this response on a scale of 0 to 1.

User Question: {{input}}
AI Response: {{output}}
Expected Answer: {{ground_truth}}

Provide your score and one sentence of reasoning.
```

**Managed evaluators** (pre-built):
- Hallucination detection
- Context relevance
- Toxicity detection
- Helpfulness scoring
- Ragas evaluators

**When to use:**
- Subjective assessments at scale (tone, accuracy, helpfulness)
- Evaluations that require reasoning
- Cases where human review would be too slow/expensive

**Limitations:**
- Requires models with structured output support
- Has inherent LLM biases
- Costs money per evaluation

**Debugging:** Filter traces by environment `langfuse-llm-as-a-judge` to see execution traces.

### Annotation Queues

Workflow for human reviewers to systematically score traces.

**How it works:**
1. Create a queue with Score Configs
2. Add traces to the queue (bulk or individually)
3. Annotators process items sequentially
4. Scores are attached to traces

**Use cases:**
- Building ground truth datasets
- Quality audits
- Training data labeling
- Calibrating LLM-as-Judge evaluators

**Required:** Score Configs must be created first.

**API endpoints available:**
- List all queues
- Get queue by ID
- Add/remove items
- Update item status

### Scores via SDK

Programmatic scoring for automated pipelines.

```python
langfuse.create_score(
    trace_id="trace_id_here",
    name="correctness",
    value=0.9,
    data_type="NUMERIC",
    comment="Factually correct response"
)
```

**Use cases:**
- Deterministic checks (format validation, length checks)
- Custom evaluation pipelines
- Integration with external evaluation tools
- Automated quality gates

**Idempotent updates:** Use `score_id` pattern `<<trace_id>>-<<score_name>>` to prevent duplicates.

### Scores via UI

Quick manual scoring for spot checks.

**How it works:**
1. Open a trace in Langfuse UI
2. Click "Add Score"
3. Select score type and enter value
4. Submit

**Use cases:**
- Quick quality spot checks
- Reviewing individual traces
- Ad-hoc evaluations
- Training and calibration

---

## Score Analytics

Langfuse provides zero-configuration analysis of your evaluation data.

### Single Score Analysis

View statistics for one score type:
- Distribution histogram/bar chart
- Trend over time
- Statistics: count, mean/mode, standard deviation

### Two-Score Comparison

Compare two scores of the **same data type** to measure agreement.

**For Numeric Scores:**

| Metric | What it measures | Interpretation |
|--------|-----------------|----------------|
| Pearson Correlation | Linear relationship | 0.9-1.0: Very Strong |
| Spearman Correlation | Rank relationship | Robust to outliers |
| MAE | Average error | Lower is better |
| RMSE | Error with penalty for large differences | Lower is better |

**For Categorical/Boolean Scores:**

| Metric | What it measures | Interpretation |
|--------|-----------------|----------------|
| Cohen's Kappa | Agreement beyond chance | 0.81-1.0: Almost Perfect |
| F1 Score | Precision/recall balance | Higher is better |
| Overall Agreement | Simple match percentage | Higher is better |

**Matched vs All:**
- **Matched:** Only traces with BOTH scores (valid comparison)
- **All:** Complete distribution (coverage analysis)

---

## Analogies for Non-Experts

### Scores are like unit tests for AI

In software, unit tests check if code produces the right output. Scores do the same for AI responses. A score of 0.9 on "correctness" means the AI got it mostly right.

### LLM-as-a-Judge is like peer review

When scientists review each other's papers, they evaluate quality using their expertise. LLM-as-a-Judge does the same—one AI evaluates another's work using defined criteria.

### Annotation Queues are like grading homework

Teachers grade papers one by one using a rubric. Annotation queues give human reviewers a consistent rubric (Score Configs) to evaluate AI outputs one by one.

### Score Configs are like grading rubrics

A rubric defines what "excellent" vs "poor" means. Score Configs do the same—they define the scale and categories for scoring, ensuring everyone grades consistently.

### Score Analytics is like test reporting

After running tests, you want dashboards showing pass rates and trends. Score Analytics shows how your AI's quality metrics change over time and how different evaluators agree.

### Boolean scores are like pass/fail tests

Some tests just check "does it work?" Boolean scores are the same—is the response helpful? Yes (1) or No (0).

### Categorical scores are like letter grades

A, B, C, D, F give you categories to understand performance at a glance. Categorical scores like "excellent, good, fair, poor" do the same for AI quality.

### Numeric scores are like percentages

89% on a test tells you exactly where you stand. Numeric scores from 0.0 to 1.0 give you precise quality measurements.

---

## Common Evaluation Patterns

### Pattern 1: Automated Quality Monitoring

```
Production Traces → LLM-as-a-Judge → Scores → Alerts if quality drops
```

Use sampling to control costs.

### Pattern 2: Building Ground Truth

```
Sample Traces → Annotation Queue → Human Scores → Golden Dataset
```

Use for training evaluators or fine-tuning.

### Pattern 3: A/B Testing Prompts

```
Dataset → Run Experiment A → Scores
Dataset → Run Experiment B → Scores
          ↓
    Score Comparison
```

Use Score Analytics to compare.

### Pattern 4: Guardrail Validation

```
Response → Deterministic Checks → Boolean Scores
  ↓
Pass: Serve to user
Fail: Fallback response
```

Use SDK scoring for real-time validation.

---

## Related Commands

| Command | What it does |
|---------|--------------|
| `evaluate design` | Design an evaluation strategy |
| `evaluate score <id>` | Create a score on a trace |
| `evaluate scores` | List scores for the project |

---

## Further Reading

- [Getting Started](getting-started.md) - Quick setup guide
- [Traces Reference](traces.md) - Data model and observation types
- [Datasets Reference](datasets.md) - Experiments and A/B testing
- [Langfuse Docs: Evaluation](https://langfuse.com/docs/evaluation/core-concepts) - Official documentation
