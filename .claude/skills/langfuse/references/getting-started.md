# Getting Started with Langfuse

> **Reading time: ~2 minutes** | For detailed guides, see the linked reference files.

---

## What is Langfuse?

Think of **traces** like detailed logs for each AI request. When your AI app processes a user message, Langfuse captures everything: what went in, what came out, how long each step took, and how much it cost.

**Key concepts:**
- **Trace** = One complete AI interaction (like a detailed log entry)
- **Observation** = Individual steps within a trace (API calls, tool uses, etc.)
- **Score** = Quality measurement you attach to a trace (like a unit test result)
- **Dataset** = Collection of test cases for experiments

---

## Quick Setup (~1 minute)

### 1. Get Your API Keys

1. Log in to [Langfuse](https://cloud.langfuse.com) (EU) or [US Cloud](https://us.cloud.langfuse.com)
2. Go to **Settings > API Keys**
3. Copy your **Secret Key** (`sk-lf-...`) and **Public Key** (`pk-lf-...`)

### 2. Create `.env` File

In your project root:

```bash
LANGFUSE_SECRET_KEY=sk-lf-your-secret-key
LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key
LANGFUSE_BASE_URL=https://cloud.langfuse.com  # Use us.cloud.langfuse.com for US
```

### 3. Verify Connection

```bash
python scripts/lf.py setup check
```

Expected output: `✓ Connected to Langfuse at https://cloud.langfuse.com`

**Trouble?** Run `python scripts/lf.py setup diagnose` for guided troubleshooting.

---

## Your First Trace Query

Once connected, see what's happening in your AI app:

```bash
# List your 10 most recent traces
python scripts/lf.py trace list --limit 10
```

You'll see something like:

```
ID                                   Name                      Timestamp                 Status
----------------------------------------------------------------------------------------------------
abc123...                            chatbot-response          2024-01-15T10:30:00Z      ✓ success
def456...                            document-qa               2024-01-15T10:28:00Z      ✗ error
```

**No traces?** Your AI app needs to be instrumented with Langfuse SDK. See [Langfuse docs](https://langfuse.com/docs/get-started).

---

## Three Main Workflows

### 1. Debug: Find Issues

*"Why is my chatbot slow?"*

```bash
# Find bottlenecks in a specific trace
python scripts/lf.py trace analyze <trace-id>

# Find recent errors
python scripts/lf.py trace errors --since 24h
```

→ Deep dive: [traces.md](traces.md)

### 2. Evaluate: Measure Quality

*"Are my responses good?"*

```bash
# Design an evaluation strategy
python scripts/lf.py evaluate design

# Score a trace manually
python scripts/lf.py evaluate score <trace-id> --name quality --value 0.8
```

Think of scores like **unit tests for AI responses**. They help you measure if your AI is doing well.

→ Deep dive: [evals.md](evals.md)

### 3. Experiment: A/B Test Prompts

*"Is GPT-4o better than GPT-4 for this task?"*

```bash
# Create a test dataset
python scripts/lf.py experiment create-dataset --name "golden-cases"

# Run the experiment
python scripts/lf.py experiment run --dataset golden-cases
```

Golden datasets are **curated test cases** that represent important scenarios. Use them to catch regressions.

→ Deep dive: [datasets.md](datasets.md)

---

## Quick Command Reference

| What you want | Command |
|--------------|---------|
| Check setup | `setup check` |
| List traces | `trace list` |
| Analyze a trace | `trace analyze <id>` |
| Find errors | `trace errors` |
| View costs | `trace costs` |
| Score a trace | `evaluate score <id> --name X --value Y` |
| Design evals | `evaluate design` |

All commands use: `python scripts/lf.py <command>`

---

## Next Steps

1. **Explore your traces**: `trace list --limit 20`
2. **Analyze a slow one**: `trace analyze <id>`
3. **Start scoring**: `evaluate score <id> --name relevance --value 0.9`

For detailed documentation:
- [Traces Reference](traces.md) - Data model, observation types, cost tracking
- [Evals Reference](evals.md) - Score types, LLM-as-Judge, annotation queues
- [Datasets Reference](datasets.md) - Experiments, golden datasets, A/B testing

---

**Need help?** Run `python scripts/lf.py <command> --help` for any command.
