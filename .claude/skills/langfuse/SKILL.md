---
name: langfuse
description: Analyze Langfuse traces, design evaluations, and iterate on AI applications. Use when user mentions langfuse, traces, spans, generations, evals, scores, datasets, or experiments. Claude acts as expert guide with real data access via Python SDK. Supports three workflows - Debug (find latency/errors), Evaluate (design scoring), Experiment (A/B test prompts).
---

# Langfuse Skill

AI developer's expert guide for trace analysis, evaluation design, and experimentation.

## Quick Reference

| Task | Command | Reference |
|------|---------|-----------|
| **Check setup** | `python scripts/langfuse.py setup check` | - |
| **Diagnose auth issues** | `python scripts/langfuse.py setup diagnose` | - |
| **List recent traces** | `python scripts/langfuse.py trace list` | [traces.md](references/traces.md) |
| **Analyze a trace** | `python scripts/langfuse.py trace analyze <id>` | [traces.md](references/traces.md) |
| **Find errors** | `python scripts/langfuse.py trace errors` | [traces.md](references/traces.md) |
| **View costs** | `python scripts/langfuse.py trace costs` | [traces.md](references/traces.md) |
| **Design evaluation** | `python scripts/langfuse.py evaluate design` | [evals.md](references/evals.md) |
| **Score a trace** | `python scripts/langfuse.py evaluate score <id>` | [evals.md](references/evals.md) |
| **Create dataset** | `python scripts/langfuse.py experiment create-dataset` | [datasets.md](references/datasets.md) |
| **Run experiment** | `python scripts/langfuse.py experiment run` | [datasets.md](references/datasets.md) |
| **New to Langfuse?** | - | [getting-started.md](references/getting-started.md) |

---

## Workflows

### Debug: Find Issues in Traces

When user asks about slow responses, errors, or unexpected behavior:

1. `python scripts/langfuse.py trace list --limit 10` - See recent traces
2. `python scripts/langfuse.py trace analyze <id>` - Find bottlenecks
3. `python scripts/langfuse.py trace errors` - Surface failures

**Output format:** Key findings first, then supporting data.

### Evaluate: Design Quality Scoring

When user asks about response quality, scoring, or evals:

1. `python scripts/langfuse.py evaluate design` - Interactive eval strategy
2. `python scripts/langfuse.py evaluate score <id> --name quality --value 0.8` - Score traces
3. `python scripts/langfuse.py evaluate scores` - Review scores

**Concept:** Scores are like unit tests for AI responses.

### Experiment: A/B Test Prompts

When user asks about testing prompts, comparing models, or experiments:

1. `python scripts/langfuse.py experiment create-dataset --name test-cases` - Create golden dataset
2. `python scripts/langfuse.py experiment add-item` - Add test cases
3. `python scripts/langfuse.py experiment run --dataset test-cases` - Run experiment
4. `python scripts/langfuse.py experiment compare` - Compare results

**Concept:** Golden datasets capture known-good input/output pairs for regression testing.

---

## Setup

### Prerequisites

```bash
# Required in .env (project root)
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com  # EU, or us.cloud.langfuse.com for US
```

### Verify Connection

```bash
python scripts/langfuse.py setup check
```

If auth fails, run `python scripts/langfuse.py setup diagnose` for guided troubleshooting.

---

## Reference Files

Load these for deep-dive explanations:

| File | Content |
|------|---------|
| [getting-started.md](references/getting-started.md) | New user onboarding (<2 min read) |
| [traces.md](references/traces.md) | Trace data model, observation types, cost tracking |
| [evals.md](references/evals.md) | Score types, LLM-as-Judge, annotation queues |
| [datasets.md](references/datasets.md) | Experiments, golden datasets, run_experiment() API |

---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| `AUTH_MISSING` | Credentials not in .env | Set LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY |
| `AUTH_INVALID` | Keys incorrect or expired | Verify keys in Langfuse dashboard |
| `NETWORK_ERROR` | Connection failed | Check LANGFUSE_BASE_URL matches region |
| `RATE_LIMITED` | Too many requests | Wait and retry |

---

## Architecture

```
langfuse/
├── SKILL.md           # This routing table
├── scripts/
│   └── langfuse.py    # Single entry point with subcommands
├── lib/
│   └── langfuse_utils.py  # Shared auth, client, error handling
└── references/
    ├── getting-started.md
    ├── traces.md
    ├── evals.md
    └── datasets.md
```

**Design:** Progressive loading - SKILL.md is the router, reference files loaded on demand.

---

## Activation Rules

**Triggers on:** langfuse, traces, spans, generations, evals, scores, datasets, experiments

**Does NOT trigger on:** Generic "analyze my logs" without Langfuse context

**Role:** Expert guide and sparring partner with real data access
