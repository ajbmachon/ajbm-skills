#!/usr/bin/env python3
"""Langfuse CLI - Single entry point for Langfuse operations.

This script provides a command-line interface for interacting with Langfuse,
enabling trace analysis, evaluation management, experimentation, and setup validation.

Usage:
    python3 "$CODEX_HOME/skills/langfuse/scripts/lf.py" <subcommand> <action> [options]

Subcommands:
    trace       Query and analyze traces
    evaluate    Create and manage evaluations
    experiment  Create datasets and run experiments
    setup       Verify connection and diagnose issues

ISC Reference: rows 7-13
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path

# Add skill directory to path for lib package imports
_SCRIPT_DIR = Path(__file__).parent.resolve()
_SKILL_DIR = _SCRIPT_DIR.parent
if str(_SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILL_DIR))

# Import from lib package (modular structure)
try:
    from lib import (  # noqa: E402
        LANGFUSE_REGIONS,
        LangfuseClient,
        LangfuseError,
        ScoreCreateResult,
        ScoreListResult,
        TraceAnalyzeResult,
        TraceCostsResult,
        TraceErrorsResult,
        TraceGetResult,
        TraceListResult,
    )
except ModuleNotFoundError as exc:  # pragma: no cover - startup guard
    if exc.name in {"langfuse", "dotenv"}:
        print(
            "Missing Python dependency.\n"
            "Run the uv wrapper instead:\n"
            "  \"$CODEX_HOME/skills/langfuse/scripts/lf.sh\" --help",
            file=sys.stderr,
        )
        sys.exit(2)
    raise


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


def _require_auth(*, retry: bool = False, skip: bool = False) -> LangfuseClient | None:
    """Validate auth before any operation (ISC row 11).

    Returns:
        LangfuseClient if auth is valid, None otherwise.
        Prints error message and returns None on failure.
    """
    try:
        client = LangfuseClient()
        skip_env = os.getenv("LANGFUSE_SKIP_AUTH_CHECK", "").lower() in {"1", "true", "yes", "on"}
        if skip or skip_env:
            return client
        result = client.auth_check(retry=retry)
        if not result.ok:
            print(f"Error: {result.message}", file=sys.stderr)
            return None
        return client
    except LangfuseError as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def _json_requested(args: argparse.Namespace) -> bool:
    """Return whether the caller requested JSON output."""
    return bool(getattr(args, "json", False))


def _to_jsonable(value):
    """Convert SDK/dataclass objects to JSON-serializable structures."""
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return {k: _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(v) for v in value]
    return value


def _emit_json(payload) -> None:
    """Print pretty JSON payload."""
    print(json.dumps(_to_jsonable(payload), indent=2, default=str))


def _add_json_flag(parser: argparse.ArgumentParser) -> None:
    """Add --json output mode to an action parser."""
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON output",
    )


def _add_no_auth_flag(parser: argparse.ArgumentParser) -> None:
    """Add --no-auth-check flag for low-latency calls."""
    parser.add_argument(
        "--no-auth-check",
        action="store_true",
        help="Skip preflight auth_check call for faster execution",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        help="Override Langfuse SDK timeout for this command",
    )


def _apply_runtime_tuning(args: argparse.Namespace) -> None:
    """Apply per-command runtime tuning before client initialization."""
    timeout_seconds = getattr(args, "timeout_seconds", None)
    if timeout_seconds is not None:
        os.environ["LANGFUSE_TIMEOUT"] = str(max(1, timeout_seconds))


def _canonical_user_id(value: str | None) -> str:
    """Normalize user IDs/emails for robust exclusion matching."""
    if not value:
        return ""
    return re.sub(r"[^a-z0-9]", "", value.strip().lower())


def _write_json_file(path: Path, payload) -> None:
    """Write payload as UTF-8 JSON with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(_to_jsonable(payload), indent=2, default=str),
        encoding="utf-8",
    )


def _fetch_traces_page_with_retries(
    client: LangfuseClient,
    *,
    limit: int,
    page: int,
    name: str | None = None,
    user_id: str | None = None,
    session_id: str | None = None,
    page_retries: int = 2,
) -> TraceListResult:
    """Fetch a trace page with bounded retries on transient API failures."""
    attempts = max(1, page_retries + 1)
    last_result: TraceListResult | None = None
    for attempt in range(1, attempts + 1):
        result: TraceListResult = client.fetch_traces(
            limit=limit,
            page=page,
            name=name,
            user_id=user_id,
            session_id=session_id,
        )
        if result.ok:
            return result
        last_result = result
        if attempt < attempts:
            time.sleep(min(2.0 * attempt, 5.0))
    return last_result or TraceListResult(ok=False, code="API_ERROR", message="Unknown fetch error")


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
        help="Maximum number of traces per page (default: 10)",
    )
    list_parser.add_argument("--name", help="Filter by trace name")
    list_parser.add_argument("--user-id", help="Filter by user ID")
    list_parser.add_argument("--session-id", help="Filter by session ID")
    list_parser.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    list_parser.add_argument(
        "--cursor",
        help="Deprecated alias for page number; use --page",
    )
    list_parser.add_argument(
        "--all",
        action="store_true",
        help="Fetch all pages until exhausted (respects filters)",
    )
    list_parser.add_argument(
        "--max-pages",
        type=int,
        default=100,
        help="Safety cap for --all pagination (default: 100)",
    )
    list_parser.add_argument(
        "--page-retries",
        type=int,
        default=2,
        help="Retries per page on transient failures (default: 2)",
    )
    _add_no_auth_flag(list_parser)
    _add_json_flag(list_parser)
    list_parser.set_defaults(func=_trace_list)

    # trace get
    get_parser = trace_subparsers.add_parser(
        "get",
        help="Get trace details",
        description="Fetch a single trace with all observations.",
    )
    get_parser.add_argument("trace_id", help="The trace ID to fetch")
    get_parser.add_argument(
        "--no-observations",
        action="store_true",
        help="Skip observation pagination for faster metadata fetch",
    )
    get_parser.add_argument(
        "--max-observations",
        type=int,
        help="Limit number of observations returned",
    )
    _add_no_auth_flag(get_parser)
    _add_json_flag(get_parser)
    get_parser.set_defaults(func=_trace_get)

    # trace analyze
    analyze_parser = trace_subparsers.add_parser(
        "analyze",
        help="Analyze a trace",
        description="Analyze trace for latency bottlenecks and issues.",
    )
    analyze_parser.add_argument("trace_id", help="The trace ID to analyze")
    _add_no_auth_flag(analyze_parser)
    _add_json_flag(analyze_parser)
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
    _add_no_auth_flag(errors_parser)
    _add_json_flag(errors_parser)
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
    _add_no_auth_flag(costs_parser)
    _add_json_flag(costs_parser)
    costs_parser.set_defaults(func=_trace_costs)

    # trace export
    export_parser = trace_subparsers.add_parser(
        "export",
        help="Export traces to local JSON files",
        description="Export traces with optional pagination, filtering, and full trace hydration.",
    )
    export_parser.add_argument(
        "--output-dir",
        default="./langfuse-export",
        help="Directory where export files are written (default: ./langfuse-export)",
    )
    export_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of traces per page (default: 20)",
    )
    export_parser.add_argument(
        "--page",
        type=int,
        default=1,
        help="Start page for export (default: 1)",
    )
    export_parser.add_argument(
        "--all",
        action="store_true",
        help="Export all pages from --page onward (bounded by --max-pages)",
    )
    export_parser.add_argument(
        "--max-pages",
        type=int,
        default=100,
        help="Safety cap for all-page export (default: 100)",
    )
    export_parser.add_argument(
        "--page-retries",
        type=int,
        default=2,
        help="Retries per page on transient failures (default: 2)",
    )
    export_parser.add_argument("--name", help="Filter traces by name")
    export_parser.add_argument("--user-id", help="Filter traces by user ID")
    export_parser.add_argument("--session-id", help="Filter traces by session ID")
    export_parser.add_argument(
        "--mode",
        choices=["metadata", "full"],
        default="full",
        help="Export mode: metadata only or full trace payloads (default: full)",
    )
    export_parser.add_argument(
        "--no-observations",
        action="store_true",
        help="When mode=full, skip observation hydration for faster exports",
    )
    export_parser.add_argument(
        "--max-observations",
        type=int,
        help="When mode=full, cap observations per trace",
    )
    export_parser.add_argument(
        "--exclude-user",
        action="append",
        default=[],
        help="User ID/email to exclude (repeatable)",
    )
    export_parser.add_argument(
        "--include-excluded",
        action="store_true",
        help="Disable default exclusion of ilias@gmail.com / ilias-gmail-com",
    )
    _add_no_auth_flag(export_parser)
    _add_json_flag(export_parser)
    export_parser.set_defaults(func=_trace_export)

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
    client = _require_auth(skip=args.no_auth_check)
    if client is None:
        return 1

    # Disable spinners in JSON mode to keep output machine-parseable.
    show_progress = not _json_requested(args)
    stop_event = threading.Event()
    progress_thread: threading.Thread | None = None

    if show_progress:
        # Set up progress indicator for long operations (ISC row 68)
        def delayed_progress_start() -> None:
            """Start progress indicator after 5 second delay."""
            if not stop_event.wait(5.0):  # Returns True if stopped early
                _show_progress_indicator("Fetching traces...", stop_event)

        # Start background thread that will show progress after 5 seconds
        progress_thread = threading.Thread(target=delayed_progress_start, daemon=True)
        progress_thread.start()

    try:
        if args.all:
            result: TraceListResult | None = None
            pages: list[TraceListResult] = []
            current_page = args.page
            if args.cursor:
                try:
                    current_page = int(args.cursor)
                except ValueError:
                    pass
            seen_pages: set[int] = set()
            for _ in range(max(1, args.max_pages)):
                page = _fetch_traces_page_with_retries(
                    client,
                    limit=args.limit,
                    page=current_page,
                    name=args.name,
                    user_id=args.user_id,
                    session_id=args.session_id,
                    page_retries=args.page_retries,
                )
                if not page.ok:
                    result = page
                    break
                pages.append(page)
                if not page.has_more:
                    break
                next_page = (page.page or current_page) + 1
                if next_page in seen_pages:
                    break
                seen_pages.add(next_page)
                current_page = next_page
                if not page.traces:
                    break

            if pages:
                all_traces = []
                for page in pages:
                    all_traces.extend(page.traces)
                last_page = pages[-1]
                result = TraceListResult(
                    ok=True,
                    code="OK",
                    message=f"Found {len(all_traces)} trace(s)",
                    traces=all_traces,
                    has_more=last_page.has_more,
                    cursor=last_page.cursor,
                    page=last_page.page,
                    total_pages=last_page.total_pages,
                    total_items=last_page.total_items,
                )
            else:
                if result is None:
                    result = TraceListResult(ok=False, code="API_ERROR", message="No pages returned")
        else:
            result = _fetch_traces_page_with_retries(
                client,
                limit=args.limit,
                page=args.page,
                name=args.name,
                user_id=args.user_id,
                session_id=args.session_id,
                page_retries=args.page_retries,
            )
    finally:
        # Stop progress indicator
        stop_event.set()
        if progress_thread is not None:
            progress_thread.join(timeout=1.0)

    # Handle errors
    if not result.ok:
        if _json_requested(args):
            _emit_json(result)
            client.flush()
            return 1
        print(f"Error: {result.message}", file=sys.stderr)
        client.flush()
        return 1

    # Handle no traces found (negative case)
    if not result.traces:
        if _json_requested(args):
            _emit_json(result)
            client.flush()
            return 0
        print("No traces found matching your criteria.")
        client.flush()
        return 0

    if _json_requested(args):
        payload = _to_jsonable(result)
        payload["pagination"] = {
            "requested_all": bool(args.all),
            "max_pages": args.max_pages,
            "next_cursor": result.cursor,
            "has_more": result.has_more,
            "page": result.page,
            "total_pages": result.total_pages,
            "total_items": result.total_items,
        }
        _emit_json(payload)
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
    client = _require_auth(skip=_args.no_auth_check)
    if client is None:
        return 1

    show_progress = not _json_requested(args)
    stop_event = threading.Event()
    progress_thread: threading.Thread | None = None

    if show_progress:
        def delayed_progress_start() -> None:
            """Start progress indicator after 5 second delay."""
            if not stop_event.wait(5.0):
                _show_progress_indicator("Fetching trace details...", stop_event)

        progress_thread = threading.Thread(target=delayed_progress_start, daemon=True)
        progress_thread.start()

    try:
        result: TraceGetResult = client.fetch_trace(
            args.trace_id,
            include_observations=not args.no_observations,
            max_observations=args.max_observations,
        )
    finally:
        stop_event.set()
        if progress_thread is not None:
            progress_thread.join(timeout=1.0)

    # Handle errors
    if not result.ok:
        if _json_requested(args):
            _emit_json(result)
            client.flush()
            return 1
        print(f"Error: {result.message}", file=sys.stderr)
        client.flush()
        return 1

    trace = result.trace
    if trace is None:
        if _json_requested(args):
            _emit_json(
                {
                    "ok": False,
                    "code": "NOT_FOUND",
                    "message": f"Trace not found: {args.trace_id}",
                    "trace_id": args.trace_id,
                }
            )
            client.flush()
            return 1
        print(f"Error: Trace not found: {args.trace_id}", file=sys.stderr)
        client.flush()
        return 1

    if _json_requested(args):
        payload = _to_jsonable(result)
        payload["fetch_options"] = {
            "include_observations": not args.no_observations,
            "max_observations": args.max_observations,
        }
        _emit_json(payload)
        client.flush()
        return 0

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
    client = _require_auth(skip=args.no_auth_check)
    if client is None:
        return 1

    show_progress = not _json_requested(args)
    stop_event = threading.Event()
    progress_thread: threading.Thread | None = None

    if show_progress:
        def delayed_progress_start() -> None:
            """Start progress indicator after 5 second delay."""
            if not stop_event.wait(5.0):
                _show_progress_indicator("Analyzing trace...", stop_event)

        progress_thread = threading.Thread(target=delayed_progress_start, daemon=True)
        progress_thread.start()

    try:
        result: TraceAnalyzeResult = client.analyze_trace(args.trace_id)
    finally:
        stop_event.set()
        if progress_thread is not None:
            progress_thread.join(timeout=1.0)

    # Handle errors
    if not result.ok:
        if _json_requested(args):
            _emit_json(result)
            client.flush()
            return 1
        print(f"Error: {result.message}", file=sys.stderr)
        client.flush()
        return 1

    analysis = result.analysis
    if analysis is None:
        if _json_requested(args):
            _emit_json(
                {
                    "ok": False,
                    "code": "NO_ANALYSIS",
                    "message": f"No analysis returned for trace {args.trace_id}",
                    "trace_id": args.trace_id,
                }
            )
            client.flush()
            return 1
        print(f"Error: No analysis returned for trace {args.trace_id}", file=sys.stderr)
        client.flush()
        return 1

    if _json_requested(args):
        _emit_json(result)
        client.flush()
        return 0

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
    """Find traces with errors in observations (ISC row 17).

    Acceptance criteria:
    - 'trace errors' finds traces with errors in observations
    - Shows: trace ID, error message, timestamp, observation that failed
    - Example: 'trace errors --since 24h' -> errors in last 24 hours
    - Negative case: No errors found -> 'No errors in the specified time range'
    """
    client = _require_auth(skip=args.no_auth_check)
    if client is None:
        return 1

    show_progress = not _json_requested(args)
    stop_event = threading.Event()
    progress_thread: threading.Thread | None = None

    if show_progress:
        def delayed_progress_start() -> None:
            """Start progress indicator after 5 second delay."""
            if not stop_event.wait(5.0):
                _show_progress_indicator("Searching for errors...", stop_event)

        progress_thread = threading.Thread(target=delayed_progress_start, daemon=True)
        progress_thread.start()

    try:
        result: TraceErrorsResult = client.fetch_errors(
            since=args.since,
            limit=args.limit,
        )
    finally:
        stop_event.set()
        if progress_thread is not None:
            progress_thread.join(timeout=1.0)

    # Handle errors
    if not result.ok:
        if _json_requested(args):
            _emit_json(result)
            client.flush()
            return 1
        print(f"Error: {result.message}", file=sys.stderr)
        client.flush()
        return 1

    # Negative case: No errors found
    if not result.errors:
        if _json_requested(args):
            _emit_json(result)
            client.flush()
            return 0
        print(f"No errors in the specified time range ({result.time_range})")
        client.flush()
        return 0

    if _json_requested(args):
        _emit_json(result)
        client.flush()
        return 0

    # Display errors (ISC row 17)
    print("=" * 80)
    print("TRACE ERRORS")
    print("=" * 80)
    print()
    print(f"Found {result.total_count} error(s) in {result.time_range}")
    print()

    # Table header
    print("-" * 80)

    for i, error in enumerate(result.errors, 1):
        # Error level indicator
        level_icon = "✗"
        if error.error_level == "FATAL" or error.error_level == "CRITICAL":
            level_icon = "⚠"

        obs_name = error.observation_name or "(unnamed)"
        print(f"{i}. {level_icon} [{error.error_level}] {obs_name}")
        print(f"   Trace ID: {error.trace_id}")
        print(f"   Observation: [{error.observation_type}] {error.observation_id[:16]}...")
        print(f"   Timestamp: {error.trace_timestamp}")

        if error.error_message:
            # Truncate long error messages
            msg = error.error_message
            if len(msg) > 100:
                msg = msg[:97] + "..."
            print(f"   Message: {msg}")
        print()

    print("-" * 80)
    print("\nUse 'trace get <trace_id>' to see full trace details.")

    client.flush()
    return 0


def _trace_costs(args: argparse.Namespace) -> int:
    """Show cost breakdown by model, trace, or time period (ISC row 18).

    Acceptance criteria:
    - 'trace costs' shows cost breakdown by model, trace, or time period
    - Shows: total cost, cost per model, cost per trace (top N)
    - Example: 'trace costs --group-by model' -> cost breakdown by model
    """
    client = _require_auth(skip=args.no_auth_check)
    if client is None:
        return 1

    show_progress = not _json_requested(args)
    stop_event = threading.Event()
    progress_thread: threading.Thread | None = None

    if show_progress:
        def delayed_progress_start() -> None:
            """Start progress indicator after 5 second delay."""
            if not stop_event.wait(5.0):
                _show_progress_indicator("Analyzing costs...", stop_event)

        progress_thread = threading.Thread(target=delayed_progress_start, daemon=True)
        progress_thread.start()

    try:
        result: TraceCostsResult = client.fetch_costs(
            group_by=args.group_by,
            since=args.since,
        )
    finally:
        stop_event.set()
        if progress_thread is not None:
            progress_thread.join(timeout=1.0)

    # Handle errors
    if not result.ok:
        if _json_requested(args):
            _emit_json(result)
            client.flush()
            return 1
        print(f"Error: {result.message}", file=sys.stderr)
        client.flush()
        return 1

    if _json_requested(args):
        _emit_json(result)
        client.flush()
        return 0

    # Display costs (ISC row 18)
    print("=" * 80)
    print("COST BREAKDOWN")
    print("=" * 80)
    print()
    print(f"Time range: {result.time_range}")
    print(f"Total cost: ${result.total_cost:.6f}")
    print()

    # Display based on grouping mode
    if result.group_by == "model" and result.by_model:
        print("-" * 40)
        print("COST BY MODEL")
        print("-" * 40)
        print()

        # Table header
        print(f"{'Model':<30} {'Cost':>15} {'Observations':>15}")
        print("-" * 62)

        for item in result.by_model:
            print(f"{item.model:<30} ${item.total_cost:>14.6f} {item.observation_count:>15}")

        print()

    elif result.group_by == "trace" and result.by_trace:
        print("-" * 40)
        print(f"TOP {len(result.by_trace)} MOST EXPENSIVE TRACES")
        print("-" * 40)
        print()

        for i, item in enumerate(result.by_trace, 1):
            trace_name = item.trace_name or "(unnamed)"
            if len(trace_name) > 40:
                trace_name = trace_name[:37] + "..."

            print(f"{i}. {trace_name}")
            print(f"   ID: {item.trace_id}")
            print(f"   Cost: ${item.total_cost:.6f}")
            print(f"   Observations: {item.observation_count}")
            print()

    elif result.group_by == "day" and result.by_day:
        print("-" * 40)
        print("COST BY DAY")
        print("-" * 40)
        print()

        # Table header
        print(f"{'Date':<15} {'Cost':>15} {'Observations':>15}")
        print("-" * 47)

        for item in result.by_day:
            print(f"{item.date:<15} ${item.total_cost:>14.6f} {item.observation_count:>15}")

        print()

    else:
        # No data for the grouping
        if result.total_cost == 0:
            print("No cost data found in the specified time range.")
            print()

    print("=" * 80)

    client.flush()
    return 0


def _trace_export(args: argparse.Namespace) -> int:
    """Export traces to local JSON files."""
    client = _require_auth(skip=args.no_auth_check)
    if client is None:
        return 1

    start_page = max(1, args.page)
    default_excludes = [] if args.include_excluded else ["ilias@gmail.com", "ilias-gmail-com"]
    all_excludes = default_excludes + list(args.exclude_user)
    canonical_excludes = {_canonical_user_id(v) for v in all_excludes}

    run_dir = Path(args.output_dir) / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    traces_dir = run_dir / "traces"
    traces_dir.mkdir(parents=True, exist_ok=True)

    pages_requested = args.max_pages if args.all else 1
    pages_attempted = 0
    pages_succeeded = 0
    page_errors: list[dict] = []
    traces_seen: set[str] = set()

    exported: list[dict] = []
    skipped: list[dict] = []
    failures: list[dict] = []

    for offset in range(max(1, pages_requested)):
        current_page = start_page + offset
        pages_attempted += 1

        page_result = _fetch_traces_page_with_retries(
            client,
            limit=args.limit,
            page=current_page,
            name=args.name,
            user_id=args.user_id,
            session_id=args.session_id,
            page_retries=args.page_retries,
        )
        if not page_result.ok:
            page_errors.append(
                {
                    "page": current_page,
                    "code": page_result.code,
                    "message": page_result.message,
                }
            )
            continue

        pages_succeeded += 1

        if not page_result.traces:
            break

        for trace in page_result.traces:
            if trace.id in traces_seen:
                continue
            traces_seen.add(trace.id)

            if _canonical_user_id(trace.user_id) in canonical_excludes:
                skipped.append(
                    {
                        "trace_id": trace.id,
                        "reason": "excluded_user",
                        "user_id": trace.user_id,
                        "timestamp": trace.timestamp,
                    }
                )
                continue

            try:
                if args.mode == "metadata":
                    payload = {
                        "trace": _to_jsonable(trace),
                        "export_metadata": {
                            "exported_at": datetime.now(timezone.utc).isoformat(),
                            "mode": args.mode,
                        },
                    }
                else:
                    full_result: TraceGetResult = client.fetch_trace(
                        trace.id,
                        include_observations=not args.no_observations,
                        max_observations=args.max_observations,
                    )
                    if not full_result.ok or full_result.trace is None:
                        failures.append(
                            {
                                "trace_id": trace.id,
                                "code": full_result.code,
                                "message": full_result.message,
                            }
                        )
                        continue
                    payload = {
                        "trace": _to_jsonable(full_result.trace),
                        "export_metadata": {
                            "exported_at": datetime.now(timezone.utc).isoformat(),
                            "mode": args.mode,
                            "include_observations": not args.no_observations,
                            "max_observations": args.max_observations,
                        },
                    }

                trace_path = traces_dir / f"{trace.id}.json"
                _write_json_file(trace_path, payload)
                exported.append(
                    {
                        "trace_id": trace.id,
                        "file": str(trace_path),
                        "user_id": trace.user_id,
                        "timestamp": trace.timestamp,
                    }
                )
            except Exception as exc:  # pragma: no cover - defensive
                failures.append({"trace_id": trace.id, "message": str(exc)})

        if args.all and not page_result.has_more:
            break

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "output_root": str(run_dir),
        "mode": args.mode,
        "filters": {
            "limit": args.limit,
            "start_page": start_page,
            "all_pages": bool(args.all),
            "max_pages": args.max_pages,
            "page_retries": args.page_retries,
            "timeout_seconds": args.timeout_seconds,
            "name": args.name,
            "user_id": args.user_id,
            "session_id": args.session_id,
        },
        "exclusion": {
            "raw": all_excludes,
            "canonical": sorted(canonical_excludes),
            "include_excluded": bool(args.include_excluded),
        },
        "pages_attempted": pages_attempted,
        "pages_succeeded": pages_succeeded,
        "page_errors": page_errors,
        "trace_candidates": len(traces_seen),
        "exported_count": len(exported),
        "skipped_count": len(skipped),
        "failed_count": len(failures),
        "exported": exported,
        "skipped": skipped,
        "failures": failures,
    }

    manifest_path = run_dir / "manifest.json"
    _write_json_file(manifest_path, manifest)

    if _json_requested(args):
        _emit_json(
            {
                "ok": True,
                "code": "OK",
                "message": "Trace export completed",
                "manifest": str(manifest_path),
                "summary": {
                    "trace_candidates": len(traces_seen),
                    "exported_count": len(exported),
                    "skipped_count": len(skipped),
                    "failed_count": len(failures),
                    "pages_attempted": pages_attempted,
                    "pages_succeeded": pages_succeeded,
                },
            }
        )
    else:
        print("=" * 80)
        print("TRACE EXPORT")
        print("=" * 80)
        print(f"Output:   {run_dir}")
        print(f"Manifest: {manifest_path}")
        print(f"Mode:     {args.mode}")
        print(f"Pages:    {pages_succeeded}/{pages_attempted} succeeded")
        print(f"Traces:   candidates={len(traces_seen)} exported={len(exported)} skipped={len(skipped)} failed={len(failures)}")
        print("=" * 80)

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
    _add_no_auth_flag(design_parser)
    _add_json_flag(design_parser)
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
    _add_no_auth_flag(score_parser)
    _add_json_flag(score_parser)
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
    _add_no_auth_flag(scores_parser)
    _add_json_flag(scores_parser)
    scores_parser.set_defaults(func=_evaluate_scores)

    eval_parser.set_defaults(func=_evaluate_help, parser=eval_parser)


def _evaluate_help(args: argparse.Namespace) -> int:
    """Show help for evaluate subcommand."""
    args.parser.print_help()
    return 0


def _evaluate_design(_args: argparse.Namespace) -> int:
    """Design evaluation strategy interactively (ISC row 22).

    Acceptance criteria:
    - 'evaluate design' helps design evaluation strategy interactively
    - Provides guidance on score types, methods, and best practices
    """
    client = _require_auth(skip=_args.no_auth_check)
    if client is None:
        return 1

    if _json_requested(_args):
        _emit_json(
            {
                "ok": True,
                "code": "OK",
                "message": "Evaluation strategy guidance",
                "recommended_workflow": [
                    "Start with manual scoring for pattern discovery",
                    "Define score configs for consistency",
                    "Add LLM-as-a-judge for scale",
                    "Use annotation queues for ground truth",
                    "Compare human vs automated scores in analytics",
                ],
            }
        )
        client.flush()
        return 0

    print("=" * 80)
    print("EVALUATION STRATEGY DESIGN GUIDE")
    print("=" * 80)
    print()
    print("Langfuse supports multiple evaluation methods. Choose based on your needs:")
    print()

    print("-" * 40)
    print("1. SCORES VIA SDK/API (Programmatic)")
    print("-" * 40)
    print("   Use when: You need automated scoring pipelines, deterministic checks,")
    print("             or custom evaluation logic")
    print()
    print("   Score Types:")
    print("   • NUMERIC    - Continuous float values (e.g., 0.0 to 1.0)")
    print("   • CATEGORICAL- Discrete categories (e.g., 'good', 'bad', 'neutral')")
    print("   • BOOLEAN    - Binary true/false (0 or 1)")
    print()
    print("   Example:")
    print("     evaluate score <trace_id> --name quality --value 0.8 --data-type numeric")
    print()

    print("-" * 40)
    print("2. LLM-AS-A-JUDGE (Automated)")
    print("-" * 40)
    print("   Use when: You need scalable subjective assessments")
    print("             (e.g., tone, helpfulness, accuracy)")
    print()
    print("   Requirements:")
    print("   • LLM Connection configured in project settings")
    print("   • Model MUST support structured output")
    print()
    print("   Setup:")
    print("   1. Configure LLM Connection in Langfuse dashboard")
    print("   2. Create evaluator (managed or custom)")
    print("   3. Map variables (input, output, ground_truth)")
    print()

    print("-" * 40)
    print("3. ANNOTATION QUEUES (Human Review)")
    print("-" * 40)
    print("   Use when: You need human reviewers to build ground truth datasets")
    print("             or do systematic quality labeling")
    print()
    print("   Requirements:")
    print("   • Score Configs defined first")
    print("   • Users assigned to queues")
    print()
    print("   Setup:")
    print("   1. Create Score Configs in Settings")
    print("   2. Create Annotation Queue")
    print("   3. Add traces to queue")
    print("   4. Annotators review and score")
    print()

    print("-" * 40)
    print("4. SCORES VIA UI (Quick Manual)")
    print("-" * 40)
    print("   Use when: You need quick spot checks or ad-hoc reviews")
    print()
    print("   Simply view a trace in Langfuse UI and click 'Add Score'")
    print()

    print("=" * 80)
    print("RECOMMENDED WORKFLOW")
    print("=" * 80)
    print()
    print("1. Start with manual scoring (UI) to understand quality patterns")
    print("2. Define Score Configs for consistency")
    print("3. Set up LLM-as-a-Judge for scalable automated evals")
    print("4. Use Annotation Queues to build ground truth for validation")
    print("5. Compare automated vs human scores with Score Analytics")
    print()
    print("For more details: https://langfuse.com/docs/evaluation/core-concepts")
    print("=" * 80)

    client.flush()
    return 0


def _evaluate_score(args: argparse.Namespace) -> int:
    """Create a score on a trace (ISC row 23).

    Acceptance criteria:
    - 'evaluate score <trace_id>' creates a score on a trace
    - Supports all score types: NUMERIC, CATEGORICAL, BOOLEAN
    - Score command accepts: --name, --value, --comment, --data-type
    - Example: 'evaluate score abc123 --name quality --value 0.8 --data-type numeric'
    - Negative case: Invalid score type -> 'Invalid data-type. Use: numeric, categorical, boolean'
    """
    client = _require_auth(skip=args.no_auth_check)
    if client is None:
        return 1

    # Create the score
    result: ScoreCreateResult = client.create_score(
        trace_id=args.trace_id,
        name=args.name,
        value=args.value,
        data_type=args.data_type,
        comment=args.comment,
    )

    # Handle errors
    if not result.ok:
        if _json_requested(args):
            _emit_json(result)
            client.flush()
            return 1
        print(f"Error: {result.message}", file=sys.stderr)
        client.flush()
        return 1

    if _json_requested(args):
        _emit_json(result)
        client.flush()
        return 0

    # Success output
    print("=" * 60)
    print("SCORE CREATED")
    print("=" * 60)
    print()
    print(f"✓ Score '{args.name}' created successfully")
    print()
    print(f"  Trace ID:   {args.trace_id}")
    print(f"  Name:       {args.name}")
    print(f"  Value:      {args.value}")
    print(f"  Data Type:  {args.data_type.upper()}")

    if args.comment:
        print(f"  Comment:    {args.comment}")

    print()
    print("=" * 60)

    client.flush()
    return 0


def _evaluate_scores(args: argparse.Namespace) -> int:
    """List scores for the project (ISC row 24).

    Acceptance criteria:
    - 'evaluate scores' lists scores for the project
    - Supports filtering by trace ID and score name
    - Example: 'evaluate scores --trace abc123' -> all scores for that trace
    """
    client = _require_auth(skip=args.no_auth_check)
    if client is None:
        return 1

    show_progress = not _json_requested(args)
    stop_event = threading.Event()
    progress_thread: threading.Thread | None = None

    if show_progress:
        def delayed_progress_start() -> None:
            """Start progress indicator after 5 second delay."""
            if not stop_event.wait(5.0):
                _show_progress_indicator("Fetching scores...", stop_event)

        progress_thread = threading.Thread(target=delayed_progress_start, daemon=True)
        progress_thread.start()

    try:
        result: ScoreListResult = client.fetch_scores(
            trace_id=args.trace,
            name=args.name,
            limit=args.limit,
        )
    finally:
        stop_event.set()
        if progress_thread is not None:
            progress_thread.join(timeout=1.0)

    # Handle errors
    if not result.ok:
        if _json_requested(args):
            _emit_json(result)
            client.flush()
            return 1
        print(f"Error: {result.message}", file=sys.stderr)
        client.flush()
        return 1

    # Handle no scores found
    if not result.scores:
        if _json_requested(args):
            _emit_json(result)
            client.flush()
            return 0
        filter_desc = ""
        if args.trace:
            filter_desc = f" for trace {args.trace}"
        elif args.name:
            filter_desc = f" with name '{args.name}'"
        print(f"No scores found{filter_desc}.")
        client.flush()
        return 0

    if _json_requested(args):
        _emit_json(result)
        client.flush()
        return 0

    # Display scores
    print("=" * 80)
    print("SCORES")
    print("=" * 80)
    print()

    filter_desc = ""
    if args.trace:
        filter_desc = f" (trace: {args.trace})"
    elif args.name:
        filter_desc = f" (name: {args.name})"

    print(f"Found {len(result.scores)} score(s){filter_desc}:")
    print()

    # Table header
    print(f"{'Name':<20} {'Value':<15} {'Type':<12} {'Trace ID':<36} {'Comment':<25}")
    print("-" * 110)

    for score in result.scores:
        # Format value based on type
        if score.data_type == "NUMERIC":
            value_display = f"{score.value:.4f}" if isinstance(score.value, float) else str(score.value)
        elif score.data_type == "BOOLEAN":
            value_display = "True" if score.value == 1 else "False"
        else:
            value_display = str(score.value) if score.value is not None else "(none)"

        # Truncate long values
        if len(value_display) > 14:
            value_display = value_display[:11] + "..."

        # Format comment
        comment_display = score.comment or ""
        if len(comment_display) > 24:
            comment_display = comment_display[:21] + "..."

        # Truncate trace ID for display
        trace_display = score.trace_id[:36] if score.trace_id else "(none)"

        print(f"{score.name:<20} {value_display:<15} {score.data_type:<12} {trace_display:<36} {comment_display:<25}")

    # Pagination info
    if result.has_more:
        print()
        print("(More scores available. Use --limit to fetch more.)")

    print()
    print("=" * 80)

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
    _add_no_auth_flag(create_dataset_parser)
    _add_json_flag(create_dataset_parser)
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
    _add_no_auth_flag(add_item_parser)
    _add_json_flag(add_item_parser)
    add_item_parser.set_defaults(func=_experiment_add_item)

    # experiment run
    run_parser = exp_subparsers.add_parser(
        "run",
        help="Run experiment",
        description="Run an experiment using a dataset and evaluation function.",
    )
    run_parser.add_argument("--dataset", required=True, help="Dataset name to use")
    run_parser.add_argument("--name", help="Experiment run name")
    _add_no_auth_flag(run_parser)
    _add_json_flag(run_parser)
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
    _add_no_auth_flag(compare_parser)
    _add_json_flag(compare_parser)
    compare_parser.set_defaults(func=_experiment_compare)

    exp_parser.set_defaults(func=_experiment_help, parser=exp_parser)


def _experiment_help(args: argparse.Namespace) -> int:
    """Show help for experiment subcommand."""
    args.parser.print_help()
    return 0


def _experiment_create_dataset(args: argparse.Namespace) -> int:
    """Create a new dataset."""
    client = _require_auth(skip=args.no_auth_check)
    if client is None:
        return 1

    if _json_requested(args):
        _emit_json(
            {
                "ok": True,
                "code": "NOT_IMPLEMENTED",
                "message": "experiment create-dataset pending (US-011)",
                "name": args.name,
                "description": args.description,
            }
        )
        client.flush()
        return 0

    print("experiment create-dataset: Command implementation pending (US-011)")
    print(f"  --name: {args.name}")
    if args.description:
        print(f"  --description: {args.description}")

    client.flush()
    return 0


def _experiment_add_item(args: argparse.Namespace) -> int:
    """Add item to dataset."""
    client = _require_auth(skip=args.no_auth_check)
    if client is None:
        return 1

    if _json_requested(args):
        _emit_json(
            {
                "ok": True,
                "code": "NOT_IMPLEMENTED",
                "message": "experiment add-item pending (US-011)",
                "dataset": args.dataset,
                "input": args.input,
                "expected_output": args.expected_output,
            }
        )
        client.flush()
        return 0

    print("experiment add-item: Command implementation pending (US-011)")
    print(f"  --dataset: {args.dataset}")
    print(f"  --input: {args.input}")
    if args.expected_output:
        print(f"  --expected-output: {args.expected_output}")

    client.flush()
    return 0


def _experiment_run(args: argparse.Namespace) -> int:
    """Run experiment."""
    client = _require_auth(skip=args.no_auth_check)
    if client is None:
        return 1

    if _json_requested(args):
        _emit_json(
            {
                "ok": True,
                "code": "NOT_IMPLEMENTED",
                "message": "experiment run pending (US-011)",
                "dataset": args.dataset,
                "name": args.name,
            }
        )
        client.flush()
        return 0

    print("experiment run: Command implementation pending (US-011)")
    print(f"  --dataset: {args.dataset}")
    if args.name:
        print(f"  --name: {args.name}")

    client.flush()
    return 0


def _experiment_compare(args: argparse.Namespace) -> int:
    """Compare experiment runs."""
    client = _require_auth(skip=args.no_auth_check)
    if client is None:
        return 1

    if _json_requested(args):
        _emit_json(
            {
                "ok": True,
                "code": "NOT_IMPLEMENTED",
                "message": "experiment compare pending (US-011)",
                "dataset": args.dataset,
                "runs": args.runs or [],
            }
        )
        client.flush()
        return 0

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
    _add_json_flag(check_parser)
    check_parser.set_defaults(func=_setup_check)

    # setup diagnose
    diagnose_parser = setup_subparsers.add_parser(
        "diagnose",
        help="Diagnose common issues",
        description="Diagnose common auth and connection issues.",
    )
    _add_json_flag(diagnose_parser)
    diagnose_parser.set_defaults(func=_setup_diagnose)

    # setup guide
    guide_parser = setup_subparsers.add_parser(
        "guide",
        help="Step-by-step setup guide",
        description="Walk through Langfuse setup step-by-step.",
    )
    _add_json_flag(guide_parser)
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
        if _json_requested(_args):
            _emit_json({"ok": False, "code": e.code, "message": e.message})
            return 1
        print(f"Setup check failed: {e}", file=sys.stderr)
        print("\nNext step: Run 'setup guide' for step-by-step setup instructions.", file=sys.stderr)
        return 1

    if not _json_requested(_args):
        print(f"Checking connection to {client.base_url}...")
    result = client.auth_check(retry=True)

    if result.ok:
        if _json_requested(_args):
            _emit_json(
                {
                    "ok": True,
                    "code": "OK",
                    "base_url": client.base_url,
                    "message": "Connected to Langfuse",
                }
            )
            return 0
        print(f"\n✓ Connected to Langfuse at {client.base_url}")
        print("✓ Authentication: OK")
        # Note: Project name would require additional API call which isn't in basic auth_check
        # The SDK doesn't expose project info in auth_check response
        return 0
    else:
        if _json_requested(_args):
            _emit_json(
                {
                    "ok": False,
                    "code": result.code,
                    "base_url": client.base_url,
                    "message": result.message,
                }
            )
            return 1
        print(f"\n✗ Connection failed: {result.message}", file=sys.stderr)
        print("\nNext step: Run 'setup diagnose' to identify the issue.", file=sys.stderr)
        return 1


def _setup_diagnose(_args: argparse.Namespace) -> int:
    """Diagnose common issues (ISC rows 36-40).

    Acceptance criteria:
    - 'setup diagnose' detects common issues: wrong region (EU vs US), expired keys, invalid keys
    - Example: Wrong region -> 'Your keys appear to be for EU cloud, but LANGFUSE_BASE_URL points to US'
    """
    if not _json_requested(_args):
        print("Running diagnostics...\n")

    try:
        client = LangfuseClient()
    except LangfuseError as e:
        # Even if client creation fails, we can still diagnose
        if _json_requested(_args):
            _emit_json({"healthy": False, "code": e.code, "message": e.message, "issues": []})
            return 1
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
        if _json_requested(_args):
            _emit_json(diagnosis)
            return 0
        print("✓ " + diagnosis.summary)
        return 0

    if _json_requested(_args):
        _emit_json(diagnosis)
        return 1

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
    if _json_requested(_args):
        _emit_json(
            {
                "ok": True,
                "code": "OK",
                "message": "Langfuse setup guide",
                "regions": LANGFUSE_REGIONS,
                "required_env": [
                    "LANGFUSE_SECRET_KEY",
                    "LANGFUSE_PUBLIC_KEY",
                    "LANGFUSE_BASE_URL",
                ],
            }
        )
        return 0

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
    lf_cmd = '"$CODEX_HOME/skills/langfuse/scripts/lf.sh"'
    print("Run the following command to verify your setup:")
    print()
    print(f"  {lf_cmd} setup check")
    print()
    print("If you encounter issues, run:")
    print()
    print(f"  {lf_cmd} setup diagnose")
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
        _apply_runtime_tuning(args)
        return args.func(args)

    # Execute the command
    if hasattr(args, "func"):
        _apply_runtime_tuning(args)
        return args.func(args)

    # Fallback: show help for the subcommand
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
