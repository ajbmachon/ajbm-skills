---
name: langfuse
description: Analyze Langfuse traces, design evaluations, and iterate on AI applications. Use when user mentions langfuse, traces, spans, generations, evals, scores, datasets, or experiments. Codex uses a local Python Langfuse CLI to query real telemetry and return actionable findings.
---

# Langfuse

Query and analyze Langfuse data directly from Codex without MCP.

## Prereqs

- `uv` installed (`uv --version`)
- Network access for `uv` to resolve the Langfuse SDK on first run
- Langfuse credentials in the active environment (or project `.env`):
  - `LANGFUSE_SECRET_KEY`
  - `LANGFUSE_PUBLIC_KEY`
  - `LANGFUSE_BASE_URL` (optional; defaults to EU cloud)
- Canonical CLI entrypoint:
  - `"$CODEX_HOME/skills/langfuse/scripts/lf.sh"`

## Deterministic Workflow

1. Validate runtime and auth
- Run `"$CODEX_HOME/skills/langfuse/scripts/lf.sh" setup check`
- If failed, run `"$CODEX_HOME/skills/langfuse/scripts/lf.sh" setup diagnose`

2. Route by user intent
- Debug latency/errors: `trace list`, `trace analyze <id>`, `trace errors`, `trace costs`
- Evaluation design/scoring: `evaluate design`, `evaluate score <id>`, `evaluate scores`
- Experiment/dataset work: `experiment create-dataset`, `experiment add-item`, `experiment run`, `experiment compare`

3. Execute with smallest useful query first
- Start with limited windows (examples: `--limit 10`, `--since 24h`)
- Expand scope only if signal is insufficient

4. Interpret and synthesize
- Extract concrete evidence (trace IDs, spans, timestamps, costs, error patterns)
- Map evidence to likely root causes and prioritized next actions

5. Exit criteria
- Findings are evidence-backed
- Recommendation list is specific, testable, and ordered by impact

## Core Commands

```bash
# Setup
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" setup check
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" setup check --json
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" setup diagnose

# Traces
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" trace list --limit 10
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" trace list --limit 50 --page 1 --all --max-pages 20 --json
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" trace analyze <trace-id>
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" trace get <trace-id> --no-observations --json
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" trace get <trace-id> --max-observations 50 --json
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" trace errors --since 24h
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" trace costs --group-by model --since 7d
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" trace export --limit 20 --page 1 --all --max-pages 10 --mode metadata --no-auth-check --json
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" trace export --limit 20 --page 1 --all --max-pages 10 --mode full --no-observations --exclude-user ilias@gmail.com --json

# Evals
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" evaluate design
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" evaluate score <trace-id> --name quality --value 0.8
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" evaluate scores --name quality --limit 20

# Experiments
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" experiment create-dataset --name golden-cases
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" experiment add-item --dataset golden-cases
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" experiment run --dataset golden-cases
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" experiment compare --dataset golden-cases
```

## Command Overview (No Extra --help Needed)

- `setup check [--json]`: Validate auth + connectivity.
- `setup diagnose [--json]`: Diagnose key/region/config issues.
- `setup guide [--json]`: Return setup instructions.
- `trace list [--limit N] [--page N] [--name X] [--user-id U] [--session-id S] [--all] [--max-pages N] [--no-auth-check] [--json]`: List traces with optional page-based pagination and filters.
- `trace get <trace_id> [--no-observations] [--max-observations N] [--no-auth-check] [--json]`: Fetch trace details; skip/limit observations for speed.
- `trace analyze <trace_id> [--no-auth-check] [--json]`: Latency/error bottleneck analysis.
- `trace errors [--since 24h|7d|... ] [--limit N] [--no-auth-check] [--json]`: Error traces.
- `trace costs [--group-by model|trace|day] [--since 7d|... ] [--no-auth-check] [--json]`: Cost breakdown.
- `trace export [--output-dir DIR] [--limit N] [--page N] [--all] [--max-pages N] [--mode metadata|full] [--no-observations] [--max-observations N] [--exclude-user U] [--include-excluded] [--no-auth-check] [--json]`: Local JSON export with manifest.
- `evaluate design|score|scores ... [--no-auth-check] [--json]`: Eval strategy and score operations.
- `experiment create-dataset|add-item|run|compare ... [--no-auth-check] [--json]`: Experiment scaffolding.

## Performance Playbook (Avoid Stalls)

- Use fast path first: add `--no-auth-check` to skip one network round-trip.
- Use machine mode: add `--json` to avoid parsing tables and to enable reliable scripting.
- Keep queries bounded: start with `trace list --limit 10`; only increase if needed.
- For `trace get`, start with `--no-observations`; only fetch observations when required.
- For large traces, use `--max-observations N` before full retrieval.
- For broad scans, use `trace list --page 1 --all --max-pages <small number>` and increase gradually.
- For golden datasets, use `trace export --mode metadata` first, then selectively re-run with `--mode full`.
- If latency is unstable, lower SDK timeout per run via env: `LANGFUSE_TIMEOUT=15 "$CODEX_HOME/skills/langfuse/scripts/lf.sh" <command>`.
- If a process appears stuck, terminate lingering Python jobs before retrying.

## Failure Recovery

- `AUTH_MISSING`: set keys in env or `.env`, then rerun `setup check`
- `AUTH_INVALID` / `AUTH_EXPIRED`: rotate keys in Langfuse and rerun `setup diagnose`
- `NETWORK_TIMEOUT` / `NETWORK_ERROR`: verify `LANGFUSE_BASE_URL` and connectivity, retry with narrower query
- `RATE_LIMITED`: wait/backoff and rerun with smaller scope
- `NOT_FOUND`: verify trace/dataset/score IDs before retrying
- Missing runtime/deps: run the wrapper directly (`"$CODEX_HOME/skills/langfuse/scripts/lf.sh" --help`) so `uv` provisions a compatible Python + packages

## Output Contract

When this skill is used in a task, return:

1. Setup status
- Auth/connectivity result and region/base URL assumptions

2. Evidence summary
- Trace IDs analyzed
- Time window and filters used
- Top anomalies (latency, failure points, cost hotspots)

3. Recommendations
- Prioritized next actions with expected impact
- Suggested follow-up commands to validate each recommendation

## Validation

Run these before relying on skill changes:

```bash
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" --help
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" setup --help
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" trace --help
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" evaluate --help
"$CODEX_HOME/skills/langfuse/scripts/lf.sh" experiment --help
```

## References

- [Getting Started](references/getting-started.md)
- [Traces](references/traces.md)
- [Evals](references/evals.md)
- [Datasets and Experiments](references/datasets.md)
