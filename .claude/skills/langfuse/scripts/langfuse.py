#!/usr/bin/env python3
"""Langfuse CLI - Single entry point for Langfuse operations.

This script provides a command-line interface for interacting with Langfuse,
enabling trace analysis, evaluation management, experimentation, and setup validation.

Usage:
    python scripts/langfuse.py <subcommand> <action> [options]

Subcommands:
    trace       Query and analyze traces
    evaluate    Create and manage evaluations
    experiment  Create datasets and run experiments
    setup       Verify connection and diagnose issues

ISC Reference: rows 7-13
"""

from __future__ import annotations

import argparse
import sys
import threading
import time
from pathlib import Path

# Add lib directory to path for imports
_SCRIPT_DIR = Path(__file__).parent.resolve()
_LIB_DIR = _SCRIPT_DIR.parent / "lib"
if str(_LIB_DIR) not in sys.path:
    sys.path.insert(0, str(_LIB_DIR))

from langfuse_utils import (  # noqa: E402
    LANGFUSE_REGIONS,
    LangfuseClient,
    LangfuseError,
    TraceAnalyzeResult,
    TraceGetResult,
    TraceListResult,
)


def _show_progress_indicator(message: str, stop_event: threading.Event) -> None:
    """Show a progress indicator for long-running operations (ISC row 68).

    Args:
        message: Message to display with the spinner
        stop_event: Event to signal when to stop the indicator
    """
    spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    idx = 0
    while not stop_event.is_set():
        print(f"\r{spinner_chars[idx % len(spinner_chars)]} {message}", end="", flush=True)
        idx += 1
        time.sleep(0.1)
    # Clear the progress line
    print("\r" + " " * (len(message) + 3) + "\r", end="", flush=True)


def _require_auth() -> LangfuseClient | None:
    """Validate auth before any operation (ISC row 11).

    Returns:
        LangfuseClient if auth is valid, None otherwise.
        Prints error message and returns None on failure.
    """
    try:
        client = LangfuseClient()
        result = client.auth_check()
        if not result.ok:
            print(f"Error: {result.message}", file=sys.stderr)
            return None
        return client
    except LangfuseError as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


# =============================================================================
# TRACE SUBCOMMAND
# =============================================================================


def _setup_trace_parser(subparsers: argparse._SubParsersAction) -> None:
    """Set up the 'trace' subcommand with its actions."""
    trace_parser = subparsers.add_parser(
        "trace",
        help="Query and analyze traces",
        description="Commands for listing, fetching, and analyzing Langfuse traces.",
    )
    trace_subparsers = trace_parser.add_subparsers(
        dest="action",
        title="actions",
        description="Available trace actions",
        metavar="<action>",
    )

    # trace list
    list_parser = trace_subparsers.add_parser(
        "list",
        help="List recent traces",
        description="Fetch recent traces with optional filters.",
    )
    list_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of traces to return (default: 10)",
    )
    list_parser.add_argument("--name", help="Filter by trace name")
    list_parser.add_argument("--user-id", help="Filter by user ID")
    list_parser.add_argument("--session-id", help="Filter by session ID")
    list_parser.set_defaults(func=_trace_list)

    # trace get
    get_parser = trace_subparsers.add_parser(
        "get",
        help="Get trace details",
        description="Fetch a single trace with all observations.",
    )
    get_parser.add_argument("trace_id", help="The trace ID to fetch")
    get_parser.set_defaults(func=_trace_get)

    # trace analyze
    analyze_parser = trace_subparsers.add_parser(
        "analyze",
        help="Analyze a trace",
        description="Analyze trace for latency bottlenecks and issues.",
    )
    analyze_parser.add_argument("trace_id", help="The trace ID to analyze")
    analyze_parser.set_defaults(func=_trace_analyze)

    # trace errors
    errors_parser = trace_subparsers.add_parser(
        "errors",
        help="Find traces with errors",
        description="Find traces that have errors in their observations.",
    )
    errors_parser.add_argument(
        "--since",
        default="24h",
        help="Time range to search (e.g., '24h', '7d') (default: 24h)",
    )
    errors_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of error traces to return (default: 20)",
    )
    errors_parser.set_defaults(func=_trace_errors)

    # trace costs
    costs_parser = trace_subparsers.add_parser(
        "costs",
        help="Show cost breakdown",
        description="Show cost breakdown by model, trace, or time period.",
    )
    costs_parser.add_argument(
        "--group-by",
        choices=["model", "trace", "day"],
        default="model",
        help="Group costs by model, trace, or day (default: model)",
    )
    costs_parser.add_argument(
        "--since",
        default="7d",
        help="Time range to analyze (e.g., '24h', '7d') (default: 7d)",
    )
    costs_parser.set_defaults(func=_trace_costs)

    trace_parser.set_defaults(func=_trace_help, parser=trace_parser)


def _trace_help(args: argparse.Namespace) -> int:
    """Show help for trace subcommand."""
    args.parser.print_help()
    return 0


def _trace_list(args: argparse.Namespace) -> int:
    """List recent traces (ISC row 14).

    Fetches recent traces with optional filters and displays them
    with trace ID, name, timestamp, and status.

    Acceptance criteria:
    - 'trace list' fetches recent traces with optional filters
    - Supports filters: --limit, --name, --user-id, --session-id
    - Output shows: trace ID, name, timestamp, status (success/error)
    - Progress indicator for fetches >5 seconds
    - Example: 'trace list --limit 10' -> shows 10 most recent traces
    - Negative case: No traces found -> 'No traces found matching your criteria'
    """
    client = _require_auth()
    if client is None:
        return 1

    # Set up progress indicator for long operations (ISC row 68)
    # The progress indicator is started before the fetch and shows a spinner
    # if the operation takes longer than 5 seconds.
    stop_event = threading.Event()
    progress_started = threading.Event()

    def delayed_progress_start() -> None:
        """Start progress indicator after 5 second delay."""
        if not stop_event.wait(5.0):  # Returns True if stopped early
            progress_started.set()
            _show_progress_indicator("Fetching traces...", stop_event)

    # Start background thread that will show progress after 5 seconds
    progress_thread = threading.Thread(target=delayed_progress_start, daemon=True)
    progress_thread.start()

    try:
        result: TraceListResult = client.fetch_traces(
            limit=args.limit,
            name=args.name,
            user_id=args.user_id,
            session_id=args.session_id,
        )
    finally:
        # Stop progress indicator
        stop_event.set()
        progress_thread.join(timeout=1.0)

    # Handle errors
    if not result.ok:
        print(f"Error: {result.message}", file=sys.stderr)
        client.flush()
        return 1

    # Handle no traces found (negative case)
    if not result.traces:
        print("No traces found matching your criteria.")
        client.flush()
        return 0

    # Display traces (ISC row 14: ID, name, timestamp, status)
    print(f"Found {len(result.traces)} trace(s):\n")

    # Table header
    print(f"{'ID':<36} {'Name':<25} {'Timestamp':<25} {'Status':<8}")
    print("-" * 96)

    for trace in result.traces:
        # Truncate long names
        name = trace.name or "(unnamed)"
        if len(name) > 24:
            name = name[:21] + "..."

        # Format timestamp for display (take first 25 chars)
        timestamp = trace.timestamp[:25] if trace.timestamp else "(no timestamp)"

        # Status indicator
        status_icon = "✓" if trace.status == "success" else "✗"
        status_display = f"{status_icon} {trace.status}"

        print(f"{trace.id:<36} {name:<25} {timestamp:<25} {status_display:<8}")

    # Pagination info
    if result.has_more:
        print("\n(More traces available. Use --limit to fetch more.)")

    client.flush()
    return 0


def _trace_get(args: argparse.Namespace) -> int:
    """Get trace details with all observations (ISC rows 15, 20).

    Fetches a single trace and displays the hierarchy:
    Session -> Trace -> Observations

    Acceptance criteria:
    - 'trace get <id>' fetches single trace with all observations
    - Output shows hierarchy: Session -> Trace -> Observations
    - Displays observation types (generation, span, event, etc.)
    - Shows timing, input/output, model, cost for each observation
    - Example: Valid trace ID -> full trace tree with observations
    - Negative case: Invalid trace ID -> 'Trace not found: [id]'
    """
    client = _require_auth()
    if client is None:
        return 1

    # Set up progress indicator for long operations
    stop_event = threading.Event()
    progress_started = threading.Event()

    def delayed_progress_start() -> None:
        """Start progress indicator after 5 second delay."""
        if not stop_event.wait(5.0):
            progress_started.set()
            _show_progress_indicator("Fetching trace details...", stop_event)

    progress_thread = threading.Thread(target=delayed_progress_start, daemon=True)
    progress_thread.start()

    try:
        result: TraceGetResult = client.fetch_trace(args.trace_id)
    finally:
        stop_event.set()
        progress_thread.join(timeout=1.0)

    # Handle errors
    if not result.ok:
        print(f"Error: {result.message}", file=sys.stderr)
        client.flush()
        return 1

    trace = result.trace
    if trace is None:
        print(f"Error: Trace not found: {args.trace_id}", file=sys.stderr)
        client.flush()
        return 1

    # Display trace hierarchy (ISC row 20)
    print("=" * 80)
    print("TRACE DETAILS")
    print("=" * 80)
    print()

    # Session level (if available)
    if trace.session_id:
        print(f"Session: {trace.session_id}")
        print("-" * 40)
        print()

    # Trace level
    print(f"Trace: {trace.id}")
    print(f"  Name: {trace.name or '(unnamed)'}")
    print(f"  Timestamp: {trace.timestamp}")

    if trace.user_id:
        print(f"  User ID: {trace.user_id}")

    if trace.tags:
        print(f"  Tags: {', '.join(trace.tags)}")

    if trace.input:
        print(f"  Input: {trace.input}")

    if trace.output:
        print(f"  Output: {trace.output}")

    print()
    print("-" * 40)
    print(f"Observations ({len(trace.observations)}):")
    print("-" * 40)

    if not trace.observations:
        print("  (no observations)")
    else:
        # Group observations by parent to show hierarchy
        # Root observations have no parent_observation_id
        root_observations = [
            obs for obs in trace.observations if obs.parent_observation_id is None
        ]
        child_map: dict[str, list] = {}

        for obs in trace.observations:
            if obs.parent_observation_id:
                if obs.parent_observation_id not in child_map:
                    child_map[obs.parent_observation_id] = []
                child_map[obs.parent_observation_id].append(obs)

        def print_observation(obs, indent: int = 0) -> None:
            """Recursively print observation with children."""
            prefix = "  " * indent
            type_icon = {
                "GENERATION": "[GEN]",
                "SPAN": "[SPAN]",
                "EVENT": "[EVENT]",
            }.get(obs.type, f"[{obs.type}]")

            # Main observation line
            name_display = obs.name or "(unnamed)"
            print(f"{prefix}{type_icon} {name_display} (id: {obs.id[:12]}...)")

            # Timing
            if obs.duration_ms is not None:
                print(f"{prefix}  Duration: {obs.duration_ms:.2f}ms")
            elif obs.start_time:
                print(f"{prefix}  Started: {obs.start_time}")
                if obs.end_time:
                    print(f"{prefix}  Ended: {obs.end_time}")

            # Model (for generations)
            if obs.model:
                print(f"{prefix}  Model: {obs.model}")

            # Token usage
            if obs.input_tokens or obs.output_tokens or obs.total_tokens:
                tokens_parts = []
                if obs.input_tokens:
                    tokens_parts.append(f"in: {obs.input_tokens}")
                if obs.output_tokens:
                    tokens_parts.append(f"out: {obs.output_tokens}")
                if obs.total_tokens:
                    tokens_parts.append(f"total: {obs.total_tokens}")
                print(f"{prefix}  Tokens: {', '.join(tokens_parts)}")

            # Cost
            if obs.cost is not None:
                print(f"{prefix}  Cost: ${obs.cost:.6f}")

            # Status/level
            if obs.level and obs.level != "DEFAULT":
                print(f"{prefix}  Level: {obs.level}")
            if obs.status_message:
                print(f"{prefix}  Status: {obs.status_message}")

            # Input/output (truncated)
            if obs.input:
                print(f"{prefix}  Input: {obs.input}")
            if obs.output:
                print(f"{prefix}  Output: {obs.output}")

            print()

            # Print children
            if obs.id in child_map:
                for child in child_map[obs.id]:
                    print_observation(child, indent + 1)

        # Print root observations first, then their children recursively
        for obs in root_observations:
            print_observation(obs, indent=1)

        # Print any orphaned observations (parent not in this trace)
        printed_ids = set()
        for obs in trace.observations:
            printed_ids.add(obs.id)

        for obs in trace.observations:
            if (
                obs.parent_observation_id
                and obs.parent_observation_id not in printed_ids
                and obs not in root_observations
            ):
                # Parent is not in trace, print at root level
                print_observation(obs, indent=1)

    print("=" * 80)

    client.flush()
    return 0


def _trace_analyze(args: argparse.Namespace) -> int:
    """Analyze a trace for latency bottlenecks and issues (ISC rows 16, 21, 69).

    Acceptance criteria:
    - 'trace analyze <id>' analyzes latency and finds bottlenecks
    - Output is insight-first: key findings before supporting data
    - Identifies slowest observations and their contribution to total time
    - Calculates p50, p95, p99 if analyzing multiple traces
    - Example: 'Your p95 latency is 3.2s, caused by the embedding-lookup span (2.8s average)'
    - Trace with errors -> highlights error observations first
    - Negative case: Trace has no timing data -> 'Cannot analyze: no timing data available'
    """
    client = _require_auth()
    if client is None:
        return 1

    # Set up progress indicator for long operations
    stop_event = threading.Event()
    progress_started = threading.Event()

    def delayed_progress_start() -> None:
        """Start progress indicator after 5 second delay."""
        if not stop_event.wait(5.0):
            progress_started.set()
            _show_progress_indicator("Analyzing trace...", stop_event)

    progress_thread = threading.Thread(target=delayed_progress_start, daemon=True)
    progress_thread.start()

    try:
        result: TraceAnalyzeResult = client.analyze_trace(args.trace_id)
    finally:
        stop_event.set()
        progress_thread.join(timeout=1.0)

    # Handle errors
    if not result.ok:
        print(f"Error: {result.message}", file=sys.stderr)
        client.flush()
        return 1

    analysis = result.analysis
    if analysis is None:
        print(f"Error: No analysis returned for trace {args.trace_id}", file=sys.stderr)
        client.flush()
        return 1

    # Display analysis results (insight-first per ISC row 21, 69)
    print("=" * 80)
    print("TRACE ANALYSIS")
    print("=" * 80)
    print()

    # Trace info
    print(f"Trace: {analysis.trace_id}")
    if analysis.trace_name:
        print(f"Name: {analysis.trace_name}")
    print()

    # KEY FINDINGS FIRST (insight-first per ISC row 21, 69)
    print("-" * 40)
    print("KEY FINDINGS")
    print("-" * 40)
    print()
    print(f"  {analysis.summary}")
    print()

    # ERRORS FIRST (if any) - per ISC row 16: highlights error observations first
    if analysis.has_errors and analysis.errors:
        print("-" * 40)
        print(f"ERRORS ({len(analysis.errors)})")
        print("-" * 40)
        print()
        for error in analysis.errors:
            error_name = error.observation_name or error.observation_type
            print(f"  ✗ [{error.level}] {error_name}")
            print(f"    ID: {error.observation_id[:12]}...")
            if error.status_message:
                print(f"    Message: {error.status_message}")
            print(f"    Time: {error.timestamp}")
            print()

    # LATENCY ANALYSIS
    if analysis.latency:
        print("-" * 40)
        print("LATENCY ANALYSIS")
        print("-" * 40)
        print()
        print(f"  Total latency: {analysis.latency.total_ms:.2f}ms")
        print(f"  Observations analyzed: {analysis.latency.observation_count}")

        # Percentiles (if available)
        if analysis.latency.p50_ms is not None:
            print()
            print("  Percentiles:")
            print(f"    p50: {analysis.latency.p50_ms:.2f}ms")
            if analysis.latency.p95_ms is not None:
                print(f"    p95: {analysis.latency.p95_ms:.2f}ms")
            if analysis.latency.p99_ms is not None:
                print(f"    p99: {analysis.latency.p99_ms:.2f}ms")
        print()

    # BOTTLENECKS
    if analysis.bottlenecks:
        print("-" * 40)
        print("BOTTLENECKS (sorted by duration)")
        print("-" * 40)
        print()

        # Show top 5 bottlenecks by default
        for i, bottleneck in enumerate(analysis.bottlenecks[:5], 1):
            name = bottleneck.observation_name or bottleneck.observation_type
            type_icon = {
                "GENERATION": "[GEN]",
                "SPAN": "[SPAN]",
                "EVENT": "[EVENT]",
            }.get(bottleneck.observation_type, f"[{bottleneck.observation_type}]")

            print(f"  {i}. {type_icon} {name}")
            print(f"     Duration: {bottleneck.duration_ms:.2f}ms ({bottleneck.percentage_of_total:.1f}% of total)")
            if bottleneck.model:
                print(f"     Model: {bottleneck.model}")
            print()

        if len(analysis.bottlenecks) > 5:
            print(f"  ... and {len(analysis.bottlenecks) - 5} more observation(s)")
            print()

    # COST SUMMARY (if available)
    if analysis.total_cost is not None and analysis.total_cost > 0:
        print("-" * 40)
        print("COST SUMMARY")
        print("-" * 40)
        print()
        print(f"  Total cost: ${analysis.total_cost:.6f}")
        if analysis.cost_by_model:
            print()
            print("  By model:")
            for model, cost in sorted(
                analysis.cost_by_model.items(), key=lambda x: x[1], reverse=True
            ):
                print(f"    {model}: ${cost:.6f}")
        print()

    print("=" * 80)

    client.flush()
    return 0


def _trace_errors(args: argparse.Namespace) -> int:
    """Find traces with errors."""
    client = _require_auth()
    if client is None:
        return 1

    print("trace errors: Command implementation pending (US-009)")
    print(f"  --since: {args.since}")
    print(f"  --limit: {args.limit}")

    client.flush()
    return 0


def _trace_costs(args: argparse.Namespace) -> int:
    """Show cost breakdown."""
    client = _require_auth()
    if client is None:
        return 1

    print("trace costs: Command implementation pending (US-009)")
    print(f"  --group-by: {args.group_by}")
    print(f"  --since: {args.since}")

    client.flush()
    return 0


# =============================================================================
# EVALUATE SUBCOMMAND
# =============================================================================


def _setup_evaluate_parser(subparsers: argparse._SubParsersAction) -> None:
    """Set up the 'evaluate' subcommand with its actions."""
    eval_parser = subparsers.add_parser(
        "evaluate",
        help="Create and manage evaluations",
        description="Commands for designing, creating, and managing evaluations.",
    )
    eval_subparsers = eval_parser.add_subparsers(
        dest="action",
        title="actions",
        description="Available evaluate actions",
        metavar="<action>",
    )

    # evaluate design
    design_parser = eval_subparsers.add_parser(
        "design",
        help="Design evaluation strategy",
        description="Interactive guide to design an evaluation strategy.",
    )
    design_parser.set_defaults(func=_evaluate_design)

    # evaluate score
    score_parser = eval_subparsers.add_parser(
        "score",
        help="Create a score on a trace",
        description="Create a score (evaluation result) on a specific trace.",
    )
    score_parser.add_argument("trace_id", help="The trace ID to score")
    score_parser.add_argument("--name", required=True, help="Score name (e.g., 'quality', 'relevance')")
    score_parser.add_argument("--value", required=True, help="Score value")
    score_parser.add_argument(
        "--data-type",
        choices=["numeric", "categorical", "boolean"],
        default="numeric",
        help="Score data type (default: numeric)",
    )
    score_parser.add_argument("--comment", help="Optional comment explaining the score")
    score_parser.set_defaults(func=_evaluate_score)

    # evaluate scores
    scores_parser = eval_subparsers.add_parser(
        "scores",
        help="List scores",
        description="List scores for the project or a specific trace.",
    )
    scores_parser.add_argument("--trace", help="Filter by trace ID")
    scores_parser.add_argument("--name", help="Filter by score name")
    scores_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of scores to return (default: 20)",
    )
    scores_parser.set_defaults(func=_evaluate_scores)

    eval_parser.set_defaults(func=_evaluate_help, parser=eval_parser)


def _evaluate_help(args: argparse.Namespace) -> int:
    """Show help for evaluate subcommand."""
    args.parser.print_help()
    return 0


def _evaluate_design(_args: argparse.Namespace) -> int:
    """Design evaluation strategy."""
    client = _require_auth()
    if client is None:
        return 1

    print("evaluate design: Command implementation pending (US-010)")

    client.flush()
    return 0


def _evaluate_score(args: argparse.Namespace) -> int:
    """Create a score on a trace."""
    client = _require_auth()
    if client is None:
        return 1

    print("evaluate score: Command implementation pending (US-010)")
    print(f"  trace_id: {args.trace_id}")
    print(f"  --name: {args.name}")
    print(f"  --value: {args.value}")
    print(f"  --data-type: {args.data_type}")
    if args.comment:
        print(f"  --comment: {args.comment}")

    client.flush()
    return 0


def _evaluate_scores(args: argparse.Namespace) -> int:
    """List scores."""
    client = _require_auth()
    if client is None:
        return 1

    print("evaluate scores: Command implementation pending (US-010)")
    if args.trace:
        print(f"  --trace: {args.trace}")
    if args.name:
        print(f"  --name: {args.name}")
    print(f"  --limit: {args.limit}")

    client.flush()
    return 0


# =============================================================================
# EXPERIMENT SUBCOMMAND
# =============================================================================


def _setup_experiment_parser(subparsers: argparse._SubParsersAction) -> None:
    """Set up the 'experiment' subcommand with its actions."""
    exp_parser = subparsers.add_parser(
        "experiment",
        help="Create datasets and run experiments",
        description="Commands for creating datasets, running experiments, and comparing results.",
    )
    exp_subparsers = exp_parser.add_subparsers(
        dest="action",
        title="actions",
        description="Available experiment actions",
        metavar="<action>",
    )

    # experiment create-dataset
    create_dataset_parser = exp_subparsers.add_parser(
        "create-dataset",
        help="Create a new dataset",
        description="Create a new dataset for experimentation.",
    )
    create_dataset_parser.add_argument("--name", required=True, help="Dataset name")
    create_dataset_parser.add_argument("--description", help="Dataset description")
    create_dataset_parser.set_defaults(func=_experiment_create_dataset)

    # experiment add-item
    add_item_parser = exp_subparsers.add_parser(
        "add-item",
        help="Add item to dataset",
        description="Add a test item to an existing dataset.",
    )
    add_item_parser.add_argument("--dataset", required=True, help="Dataset name")
    add_item_parser.add_argument("--input", required=True, help="Input value (JSON string)")
    add_item_parser.add_argument("--expected-output", help="Expected output (JSON string)")
    add_item_parser.set_defaults(func=_experiment_add_item)

    # experiment run
    run_parser = exp_subparsers.add_parser(
        "run",
        help="Run experiment",
        description="Run an experiment using a dataset and evaluation function.",
    )
    run_parser.add_argument("--dataset", required=True, help="Dataset name to use")
    run_parser.add_argument("--name", help="Experiment run name")
    run_parser.set_defaults(func=_experiment_run)

    # experiment compare
    compare_parser = exp_subparsers.add_parser(
        "compare",
        help="Compare experiment runs",
        description="Compare results from multiple experiment runs.",
    )
    compare_parser.add_argument("--dataset", required=True, help="Dataset name")
    compare_parser.add_argument(
        "--runs",
        nargs="+",
        help="Run names to compare (if not specified, compares all runs)",
    )
    compare_parser.set_defaults(func=_experiment_compare)

    exp_parser.set_defaults(func=_experiment_help, parser=exp_parser)


def _experiment_help(args: argparse.Namespace) -> int:
    """Show help for experiment subcommand."""
    args.parser.print_help()
    return 0


def _experiment_create_dataset(args: argparse.Namespace) -> int:
    """Create a new dataset."""
    client = _require_auth()
    if client is None:
        return 1

    print("experiment create-dataset: Command implementation pending (US-011)")
    print(f"  --name: {args.name}")
    if args.description:
        print(f"  --description: {args.description}")

    client.flush()
    return 0


def _experiment_add_item(args: argparse.Namespace) -> int:
    """Add item to dataset."""
    client = _require_auth()
    if client is None:
        return 1

    print("experiment add-item: Command implementation pending (US-011)")
    print(f"  --dataset: {args.dataset}")
    print(f"  --input: {args.input}")
    if args.expected_output:
        print(f"  --expected-output: {args.expected_output}")

    client.flush()
    return 0


def _experiment_run(args: argparse.Namespace) -> int:
    """Run experiment."""
    client = _require_auth()
    if client is None:
        return 1

    print("experiment run: Command implementation pending (US-011)")
    print(f"  --dataset: {args.dataset}")
    if args.name:
        print(f"  --name: {args.name}")

    client.flush()
    return 0


def _experiment_compare(args: argparse.Namespace) -> int:
    """Compare experiment runs."""
    client = _require_auth()
    if client is None:
        return 1

    print("experiment compare: Command implementation pending (US-011)")
    print(f"  --dataset: {args.dataset}")
    if args.runs:
        print(f"  --runs: {args.runs}")

    client.flush()
    return 0


# =============================================================================
# SETUP SUBCOMMAND
# =============================================================================


def _setup_setup_parser(subparsers: argparse._SubParsersAction) -> None:
    """Set up the 'setup' subcommand with its actions."""
    setup_parser = subparsers.add_parser(
        "setup",
        help="Verify connection and diagnose issues",
        description="Commands for verifying Langfuse setup and diagnosing connection issues.",
    )
    setup_subparsers = setup_parser.add_subparsers(
        dest="action",
        title="actions",
        description="Available setup actions",
        metavar="<action>",
    )

    # setup check
    check_parser = setup_subparsers.add_parser(
        "check",
        help="Verify auth and connection",
        description="Verify authentication and connection to Langfuse.",
    )
    check_parser.set_defaults(func=_setup_check)

    # setup diagnose
    diagnose_parser = setup_subparsers.add_parser(
        "diagnose",
        help="Diagnose common issues",
        description="Diagnose common auth and connection issues.",
    )
    diagnose_parser.set_defaults(func=_setup_diagnose)

    # setup guide
    guide_parser = setup_subparsers.add_parser(
        "guide",
        help="Step-by-step setup guide",
        description="Walk through Langfuse setup step-by-step.",
    )
    guide_parser.set_defaults(func=_setup_guide)

    setup_parser.set_defaults(func=_setup_help, parser=setup_parser)


def _setup_help(args: argparse.Namespace) -> int:
    """Show help for setup subcommand."""
    args.parser.print_help()
    return 0


def _setup_check(_args: argparse.Namespace) -> int:
    """Verify auth and connection (ISC row 35).

    Acceptance criteria:
    - 'setup check' verifies auth and connection to Langfuse
    - Example: Valid setup -> 'Connected to Langfuse at [url]. Project: [name]'
    """
    try:
        client = LangfuseClient()
    except LangfuseError as e:
        print(f"Setup check failed: {e}", file=sys.stderr)
        print("\nNext step: Run 'setup guide' for step-by-step setup instructions.", file=sys.stderr)
        return 1

    print(f"Checking connection to {client.base_url}...")
    result = client.auth_check(retry=True)

    if result.ok:
        print(f"\n✓ Connected to Langfuse at {client.base_url}")
        print("✓ Authentication: OK")
        # Note: Project name would require additional API call which isn't in basic auth_check
        # The SDK doesn't expose project info in auth_check response
        return 0
    else:
        print(f"\n✗ Connection failed: {result.message}", file=sys.stderr)
        print("\nNext step: Run 'setup diagnose' to identify the issue.", file=sys.stderr)
        return 1


def _setup_diagnose(_args: argparse.Namespace) -> int:
    """Diagnose common issues (ISC rows 36-40).

    Acceptance criteria:
    - 'setup diagnose' detects common issues: wrong region (EU vs US), expired keys, invalid keys
    - Example: Wrong region -> 'Your keys appear to be for EU cloud, but LANGFUSE_BASE_URL points to US'
    """
    print("Running diagnostics...\n")

    try:
        client = LangfuseClient()
    except LangfuseError as e:
        # Even if client creation fails, we can still diagnose
        print(f"⚠ Cannot create client: {e.code}")
        print(f"  {e.message}\n")

        if e.code == "AUTH_MISSING":
            print("Diagnosis: Missing credentials")
            print("\nNext steps:")
            print("  1. Create a .env file in your project root")
            print("  2. Add your Langfuse credentials:")
            print("     LANGFUSE_SECRET_KEY=sk-lf-...")
            print("     LANGFUSE_PUBLIC_KEY=pk-lf-...")
            print("     LANGFUSE_BASE_URL=https://cloud.langfuse.com")
            print("\n  Run 'setup guide' for detailed instructions.")
        return 1

    diagnosis = client.diagnose()

    if diagnosis.healthy:
        print("✓ " + diagnosis.summary)
        return 0

    print("✗ " + diagnosis.summary + "\n")

    for issue in diagnosis.issues:
        severity_icon = {"error": "✗", "warning": "⚠", "info": "ℹ"}.get(
            issue.severity, "•"
        )
        print(f"{severity_icon} [{issue.code}] {issue.message}")
        if issue.detail:
            print(f"  {issue.detail}")
        print()

    if diagnosis.next_steps:
        print("Next steps:")
        for i, step in enumerate(diagnosis.next_steps, 1):
            print(f"  {i}. {step}")

    return 1


def _setup_guide(_args: argparse.Namespace) -> int:
    """Walk through setup step-by-step (ISC row 37).

    Acceptance criteria:
    - 'setup guide' walks through setup step-by-step
    - Clear next steps provided on any failure
    """
    print("=" * 60)
    print("Langfuse Setup Guide")
    print("=" * 60)
    print()
    print("Step 1: Create a Langfuse Account")
    print("-" * 40)
    print("If you don't have an account yet:")
    print("  • EU Cloud: https://cloud.langfuse.com")
    print("  • US Cloud: https://us.cloud.langfuse.com")
    print()
    print("Step 2: Create a Project")
    print("-" * 40)
    print("  1. Log in to Langfuse")
    print("  2. Click 'New Project' or select an existing project")
    print("  3. Note which region you're using (EU or US)")
    print()
    print("Step 3: Generate API Keys")
    print("-" * 40)
    print("  1. Go to Settings > API Keys")
    print("  2. Click 'Create API Key'")
    print("  3. Copy both keys:")
    print("     • Secret Key (starts with 'sk-lf-')")
    print("     • Public Key (starts with 'pk-lf-')")
    print()
    print("Step 4: Configure Environment")
    print("-" * 40)
    print("Create a .env file in your project root with:")
    print()
    print("  LANGFUSE_SECRET_KEY=sk-lf-your-secret-key")
    print("  LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key")
    print()
    print("For region, add the appropriate base URL:")
    print()
    for region, url in LANGFUSE_REGIONS.items():
        print(f"  # {region} Cloud:")
        print(f"  LANGFUSE_BASE_URL={url}")
        print()
    print("Step 5: Verify Setup")
    print("-" * 40)
    print("Run the following command to verify your setup:")
    print()
    print("  python scripts/langfuse.py setup check")
    print()
    print("If you encounter issues, run:")
    print()
    print("  python scripts/langfuse.py setup diagnose")
    print()
    print("=" * 60)
    print("For more information: https://langfuse.com/docs/get-started")
    print("=" * 60)
    return 0


# =============================================================================
# MAIN
# =============================================================================


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the Langfuse CLI.

    Args:
        argv: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = argparse.ArgumentParser(
        prog="langfuse",
        description="Langfuse CLI - Query traces, manage evaluations, and run experiments.",
        epilog="Use '%(prog)s <command> --help' for more information on a command.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Available commands",
        metavar="<command>",
    )

    # Set up all subcommand parsers
    _setup_trace_parser(subparsers)
    _setup_evaluate_parser(subparsers)
    _setup_experiment_parser(subparsers)
    _setup_setup_parser(subparsers)

    args = parser.parse_args(argv)

    # No command specified
    if args.command is None:
        parser.print_help()
        return 0

    # Command specified but no action (for subcommands with nested actions)
    if hasattr(args, "action") and args.action is None and hasattr(args, "func"):
        return args.func(args)

    # Execute the command
    if hasattr(args, "func"):
        return args.func(args)

    # Fallback: show help for the subcommand
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
