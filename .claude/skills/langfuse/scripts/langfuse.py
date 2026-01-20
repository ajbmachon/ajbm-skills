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
from pathlib import Path

# Add lib directory to path for imports
_SCRIPT_DIR = Path(__file__).parent.resolve()
_LIB_DIR = _SCRIPT_DIR.parent / "lib"
if str(_LIB_DIR) not in sys.path:
    sys.path.insert(0, str(_LIB_DIR))

from langfuse_utils import LangfuseClient, LangfuseError  # noqa: E402


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
    """List recent traces."""
    client = _require_auth()
    if client is None:
        return 1

    print("trace list: Command implementation pending (US-006)")
    print(f"  --limit: {args.limit}")
    if args.name:
        print(f"  --name: {args.name}")
    if args.user_id:
        print(f"  --user-id: {args.user_id}")
    if args.session_id:
        print(f"  --session-id: {args.session_id}")

    client.flush()
    return 0


def _trace_get(args: argparse.Namespace) -> int:
    """Get trace details."""
    client = _require_auth()
    if client is None:
        return 1

    print("trace get: Command implementation pending (US-007)")
    print(f"  trace_id: {args.trace_id}")

    client.flush()
    return 0


def _trace_analyze(args: argparse.Namespace) -> int:
    """Analyze a trace for issues."""
    client = _require_auth()
    if client is None:
        return 1

    print("trace analyze: Command implementation pending (US-008)")
    print(f"  trace_id: {args.trace_id}")

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
    """Verify auth and connection (ISC row 35)."""
    try:
        client = LangfuseClient()
    except LangfuseError as e:
        print(f"Setup check failed: {e}", file=sys.stderr)
        return 1

    result = client.auth_check()
    if result.ok:
        print(f"Connected to Langfuse at {client.base_url}")
        print("Authentication: OK")
        return 0
    else:
        print(f"Connection failed: {result.message}", file=sys.stderr)
        return 1


def _setup_diagnose(_args: argparse.Namespace) -> int:
    """Diagnose common issues."""
    print("setup diagnose: Command implementation pending (US-005)")
    print("Will detect: wrong region (EU vs US), expired keys, invalid keys")
    return 0


def _setup_guide(_args: argparse.Namespace) -> int:
    """Walk through setup step-by-step."""
    print("setup guide: Command implementation pending (US-005)")
    print("Will walk through: .env setup, API key creation, region selection")
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
