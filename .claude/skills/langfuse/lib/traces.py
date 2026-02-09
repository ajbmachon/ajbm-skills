"""Trace operations for Langfuse SDK.

This module provides:
- fetch_traces() - Fetch recent traces with filters
- fetch_trace() - Fetch a single trace with observations
- analyze_trace() - Analyze trace for latency/errors
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .client import get_langfuse
from .models import (
    AUTH_INVALID,
    NETWORK_TIMEOUT,
    NOT_FOUND,
    RATE_LIMITED,
    BottleneckInfo,
    ErrorInfo,
    LatencyStats,
    ObservationInfo,
    TraceAnalysis,
    TraceAnalyzeResult,
    TraceDetail,
    TraceGetResult,
    TraceInfo,
    TraceListResult,
)

if TYPE_CHECKING:
    pass


def _safe_get(obj: Any, attr: str, default: Any = None) -> Any:
    """Safely get attribute from object or dict."""
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)


def _format_timestamp(ts: Any) -> str:
    """Format timestamp to ISO string."""
    if ts is None:
        return ""
    if hasattr(ts, "isoformat"):
        return ts.isoformat()
    return str(ts)


def _truncate(text: str | None, max_len: int = 500) -> str | None:
    """Truncate text with ellipsis if too long."""
    if text is None:
        return None
    s = str(text)
    return s[:max_len] + "..." if len(s) > max_len else s


def _classify_error(e: Exception) -> str:
    """Classify an exception into an error code."""
    error_str = str(e).lower()
    if "401" in error_str or "unauthorized" in error_str:
        return AUTH_INVALID
    if "429" in error_str or "rate" in error_str:
        return RATE_LIMITED
    if "404" in error_str or "not found" in error_str:
        return NOT_FOUND
    if any(
        term in error_str
        for term in (
            "timeout",
            "timed out",
            "status_code: 524",
            "524",
            "taking too long",
            "gateway timeout",
        )
    ):
        return NETWORK_TIMEOUT
    return "API_ERROR"


def fetch_traces(
    limit: int = 10,
    name: str | None = None,
    user_id: str | None = None,
    session_id: str | None = None,
    page: int | None = None,
    cursor: str | None = None,
    *,
    langfuse: Any = None,
) -> TraceListResult:
    """Fetch recent traces with optional filters.

    Args:
        limit: Maximum number of traces to return.
        name: Filter traces by name.
        user_id: Filter traces by user ID.
        session_id: Filter traces by session ID.
        langfuse: Optional Langfuse client instance (for testing).

    Returns:
        TraceListResult with traces and pagination info.
    """
    try:
        if langfuse is None:
            langfuse = get_langfuse()
        kwargs: dict[str, Any] = {"limit": limit}
        if name:
            kwargs["name"] = name
        if user_id:
            kwargs["user_id"] = user_id
        if session_id:
            kwargs["session_id"] = session_id
        if page is not None:
            kwargs["page"] = page
        if cursor:
            # Backward compatibility: some callers may pass a numeric cursor.
            try:
                kwargs["page"] = int(cursor)
            except (TypeError, ValueError):
                kwargs["cursor"] = cursor

        response = langfuse.api.trace.list(**kwargs)
        traces = _parse_trace_list(response.data)

        pagination = _extract_pagination(response)

        return TraceListResult(
            ok=True,
            code="OK",
            message=f"Found {len(traces)} trace(s)",
            traces=traces,
            has_more=pagination["has_more"],
            cursor=pagination["cursor"],
            page=pagination["page"],
            total_pages=pagination["total_pages"],
            total_items=pagination["total_items"],
        )
    except Exception as e:
        return TraceListResult(ok=False, code=_classify_error(e), message=str(e))


def _parse_trace_list(data: Any) -> list[TraceInfo]:
    """Parse trace list response into TraceInfo objects."""
    traces = []
    for trace in data:
        status = "error" if _safe_get(trace, "level") == "ERROR" else "success"
        traces.append(
            TraceInfo(
                id=trace.id,
                name=trace.name,
                timestamp=_format_timestamp(_safe_get(trace, "timestamp")),
                status=status,
                user_id=_safe_get(trace, "user_id"),
                session_id=_safe_get(trace, "session_id"),
            )
        )
    return traces


def _extract_pagination(response: Any) -> dict[str, Any]:
    """Extract pagination details from response metadata.

    Supports both page-based and cursor-based metadata variants.
    """
    page = None
    total_pages = None
    total_items = None
    cursor = None
    has_more = False

    meta = getattr(response, "meta", None)
    if meta:
        page = _safe_get(meta, "page")
        total_pages = _safe_get(meta, "total_pages")
        total_items = _safe_get(meta, "total_items")
        cursor = _safe_get(meta, "cursor")

        if isinstance(page, int) and isinstance(total_pages, int):
            has_more = page < total_pages
        elif cursor is not None:
            has_more = True

    return {
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "cursor": cursor,
        "has_more": has_more,
    }


def fetch_trace(
    trace_id: str,
    include_observations: bool = True,
    max_observations: int | None = None,
    *,
    langfuse: Any = None,
) -> TraceGetResult:
    """Fetch a single trace with all observations.

    Args:
        trace_id: The ID of the trace to fetch.
        langfuse: Optional Langfuse client instance (for testing).

    Returns:
        TraceGetResult with trace details and observations.
    """
    try:
        if langfuse is None:
            langfuse = get_langfuse()
        trace = langfuse.api.trace.get(trace_id)
        observations: list[ObservationInfo] = []
        if include_observations:
            observations = _fetch_all_observations(
                langfuse,
                trace_id,
                max_observations=max_observations,
            )

        trace_detail = _build_trace_detail(trace, trace_id, observations)

        return TraceGetResult(
            ok=True,
            code="OK",
            message=f"Found trace with {len(observations)} observation(s)",
            trace=trace_detail,
        )
    except Exception as e:
        return _handle_trace_error(e, trace_id)


def _fetch_all_observations(
    langfuse: Any,
    trace_id: str,
    *,
    max_observations: int | None = None,
) -> list[ObservationInfo]:
    """Fetch all observations for a trace with pagination."""
    observations = []
    cursor = None

    seen_cursors: set[str] = set()
    while True:
        if max_observations is not None and len(observations) >= max_observations:
            break

        page_limit = 100
        if max_observations is not None:
            page_limit = max(1, min(100, max_observations - len(observations)))

        obs_kwargs: dict[str, Any] = {"trace_id": trace_id, "limit": page_limit}
        if cursor:
            obs_kwargs["cursor"] = cursor

        obs_response = langfuse.api.observations_v_2.get_many(**obs_kwargs)

        for obs in obs_response.data:
            observations.append(_parse_observation(obs))

        pagination = _extract_pagination(obs_response)
        cursor = pagination["cursor"]
        if not cursor:
            break
        if cursor in seen_cursors:
            break
        seen_cursors.add(cursor)
        if not obs_response.data:
            break

    return observations


def _parse_observation(obs: Any) -> ObservationInfo:
    """Parse a single observation into ObservationInfo."""
    start_time = _safe_get(obs, "start_time")
    end_time = _safe_get(obs, "end_time")
    duration_ms = _calculate_duration(start_time, end_time)
    usage = _safe_get(obs, "usage")

    return ObservationInfo(
        id=str(_safe_get(obs, "id", "")),
        type=str(_safe_get(obs, "type", "UNKNOWN")),
        name=_safe_get(obs, "name"),
        start_time=_format_timestamp(start_time),
        end_time=_format_timestamp(end_time),
        duration_ms=duration_ms,
        level=_safe_get(obs, "level"),
        status_message=_safe_get(obs, "status_message"),
        model=_safe_get(obs, "model"),
        input=_truncate(_safe_get(obs, "input"), 300),
        output=_truncate(_safe_get(obs, "output"), 300),
        input_tokens=_safe_get(usage, "input") if usage else None,
        output_tokens=_safe_get(usage, "output") if usage else None,
        total_tokens=_safe_get(usage, "total") if usage else None,
        cost=_safe_get(obs, "calculated_total_cost"),
        parent_observation_id=_safe_get(obs, "parent_observation_id"),
    )


def _calculate_duration(start_time: Any, end_time: Any) -> float | None:
    """Calculate duration in milliseconds from start and end times."""
    if not start_time or not end_time:
        return None
    try:
        return (end_time - start_time).total_seconds() * 1000
    except (TypeError, AttributeError):
        return None


def _build_trace_detail(
    trace: Any, trace_id: str, observations: list[ObservationInfo]
) -> TraceDetail:
    """Build TraceDetail from trace response and observations."""
    return TraceDetail(
        id=_safe_get(trace, "id", trace_id) or trace_id,
        name=_safe_get(trace, "name"),
        timestamp=_format_timestamp(_safe_get(trace, "timestamp")),
        session_id=_safe_get(trace, "session_id"),
        user_id=_safe_get(trace, "user_id"),
        input=_truncate(_safe_get(trace, "input")),
        output=_truncate(_safe_get(trace, "output")),
        metadata=_safe_get(trace, "metadata"),
        tags=_safe_get(trace, "tags"),
        observations=observations,
    )


def _handle_trace_error(e: Exception, trace_id: str) -> TraceGetResult:
    """Handle trace fetch errors with appropriate error codes."""
    code = _classify_error(e)
    if code == NOT_FOUND:
        return TraceGetResult(ok=False, code=NOT_FOUND, message=f"Trace not found: {trace_id}")
    return TraceGetResult(ok=False, code=code, message=str(e))


def analyze_trace(trace_id: str, *, langfuse: Any = None) -> TraceAnalyzeResult:
    """Analyze a trace for latency bottlenecks and issues.

    Args:
        trace_id: The ID of the trace to analyze.
        langfuse: Optional Langfuse client instance (for testing).

    Returns:
        TraceAnalyzeResult with latency stats, bottlenecks, and errors.
    """
    trace_result = fetch_trace(trace_id, langfuse=langfuse)
    if not trace_result.ok or trace_result.trace is None:
        return TraceAnalyzeResult(
            ok=False,
            code=trace_result.code,
            message=trace_result.message,
        )

    trace = trace_result.trace
    analysis_data = _collect_analysis_data(trace.observations)

    if not analysis_data["durations"]:
        return _build_no_timing_result(trace_id, trace.name, analysis_data)

    return _build_analysis_result(trace_id, trace.name, analysis_data)


def _collect_analysis_data(
    observations: list[ObservationInfo],
) -> dict[str, Any]:
    """Collect timing, error, and cost data from observations."""
    durations: list[tuple[ObservationInfo, float]] = []
    errors: list[ErrorInfo] = []
    total_cost = 0.0
    cost_by_model: dict[str, float] = {}

    for obs in observations:
        if obs.duration_ms is not None:
            durations.append((obs, obs.duration_ms))

        if obs.level in ("ERROR", "FATAL", "CRITICAL"):
            errors.append(_build_error_info(obs))

        if obs.cost is not None:
            total_cost += obs.cost
            model = obs.model or "unknown"
            cost_by_model[model] = cost_by_model.get(model, 0.0) + obs.cost

    return {
        "durations": durations,
        "errors": errors,
        "total_cost": total_cost,
        "cost_by_model": cost_by_model,
    }


def _build_error_info(obs: ObservationInfo) -> ErrorInfo:
    """Build ErrorInfo from observation with error level."""
    return ErrorInfo(
        observation_id=obs.id,
        observation_name=obs.name,
        observation_type=obs.type,
        level=obs.level or "ERROR",
        status_message=obs.status_message,
        timestamp=obs.start_time,
    )


def _build_no_timing_result(
    trace_id: str, trace_name: str | None, data: dict[str, Any]
) -> TraceAnalyzeResult:
    """Build result when no timing data is available."""
    return TraceAnalyzeResult(
        ok=False,
        code="NO_TIMING_DATA",
        message="Cannot analyze: no timing data available",
        analysis=TraceAnalysis(
            trace_id=trace_id,
            trace_name=trace_name,
            has_timing_data=False,
            has_errors=bool(data["errors"]),
            summary="Cannot analyze: no timing data available",
            errors=data["errors"],
            total_cost=data["total_cost"] if data["total_cost"] > 0 else None,
            cost_by_model=data["cost_by_model"] if data["cost_by_model"] else None,
        ),
    )


def _build_analysis_result(
    trace_id: str, trace_name: str | None, data: dict[str, Any]
) -> TraceAnalyzeResult:
    """Build complete analysis result with latency stats and bottlenecks."""
    durations = data["durations"]
    sorted_durations = sorted([d for _, d in durations])
    total_latency = sum(sorted_durations)

    latency = _calculate_latency_stats(sorted_durations, total_latency)
    bottlenecks = _calculate_bottlenecks(durations, total_latency)
    summary = _build_summary(data["errors"], bottlenecks, total_latency, latency)

    return TraceAnalyzeResult(
        ok=True,
        code="OK",
        message=summary,
        analysis=TraceAnalysis(
            trace_id=trace_id,
            trace_name=trace_name,
            has_timing_data=True,
            has_errors=bool(data["errors"]),
            summary=summary,
            latency=latency,
            bottlenecks=bottlenecks,
            errors=data["errors"],
            total_cost=data["total_cost"] if data["total_cost"] > 0 else None,
            cost_by_model=data["cost_by_model"] if data["cost_by_model"] else None,
        ),
    )


def _calculate_latency_stats(sorted_durations: list[float], total: float) -> LatencyStats:
    """Calculate latency percentiles from sorted durations."""
    return LatencyStats(
        total_ms=total,
        p50_ms=_percentile(sorted_durations, 50) if len(sorted_durations) >= 3 else None,
        p95_ms=_percentile(sorted_durations, 95) if len(sorted_durations) >= 3 else None,
        p99_ms=_percentile(sorted_durations, 99) if len(sorted_durations) >= 3 else None,
        observation_count=len(sorted_durations),
    )


def _percentile(data: list[float], p: float) -> float:
    """Calculate percentile from sorted data."""
    if not data:
        return 0.0
    k = (len(data) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(data) - 1)
    return data[f] * (c - k) + data[c] * (k - f) if f != c else data[f]


def _calculate_bottlenecks(
    durations: list[tuple[ObservationInfo, float]], total_latency: float
) -> list[BottleneckInfo]:
    """Calculate bottleneck info sorted by duration."""
    bottlenecks = []
    for obs, duration in sorted(durations, key=lambda x: x[1], reverse=True):
        percentage = (duration / total_latency * 100) if total_latency > 0 else 0
        bottlenecks.append(
            BottleneckInfo(
                observation_id=obs.id,
                observation_name=obs.name,
                observation_type=obs.type,
                duration_ms=duration,
                percentage_of_total=percentage,
                model=obs.model,
            )
        )
    return bottlenecks


def _build_summary(
    errors: list[ErrorInfo],
    bottlenecks: list[BottleneckInfo],
    total_latency: float,
    latency: LatencyStats,
) -> str:
    """Build human-readable analysis summary."""
    parts = []
    if errors:
        parts.append(f"Found {len(errors)} error(s) in trace")
    if bottlenecks:
        top = bottlenecks[0]
        top_name = top.observation_name or top.observation_type
        parts.append(
            f"Total latency: {total_latency:.0f}ms, "
            f"slowest: {top_name} ({top.duration_ms:.0f}ms, {top.percentage_of_total:.0f}%)"
        )
        if latency.p95_ms is not None:
            parts.append(f"p50: {latency.p50_ms:.0f}ms, p95: {latency.p95_ms:.0f}ms")
    return ". ".join(parts) or "Trace analyzed successfully"
