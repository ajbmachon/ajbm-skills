"""Error discovery operations for Langfuse SDK.

This module provides:
- fetch_errors() - Find traces with errors in observations
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from .client import get_langfuse
from .models import TraceErrorInfo, TraceErrorsResult

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


def _parse_time_range(time_range: str) -> tuple[datetime, str]:
    """Parse time range string like '24h', '7d' into datetime."""
    now = datetime.now(UTC)

    if time_range.endswith("h"):
        hours = int(time_range[:-1])
        return now - timedelta(hours=hours), f"last {hours} hour(s)"
    if time_range.endswith("d"):
        days = int(time_range[:-1])
        return now - timedelta(days=days), f"last {days} day(s)"
    if time_range.endswith("w"):
        weeks = int(time_range[:-1])
        return now - timedelta(weeks=weeks), f"last {weeks} week(s)"

    return now - timedelta(hours=24), "last 24 hours"


def fetch_errors(
    since: str = "24h", limit: int = 20, *, langfuse: Any = None
) -> TraceErrorsResult:
    """Find traces with errors in observations.

    Args:
        since: Time range to search (e.g., '24h', '7d').
        limit: Maximum number of error traces to return.
        langfuse: Optional Langfuse client instance (for testing).

    Returns:
        TraceErrorsResult with errors or appropriate message.
    """
    try:
        if langfuse is None:
            langfuse = get_langfuse()
        from_timestamp, human_range = _parse_time_range(since)

        errors = _collect_errors(langfuse, from_timestamp, limit)

        if not errors:
            return TraceErrorsResult(
                ok=True,
                code="OK",
                message=f"No errors in the specified time range ({human_range})",
                time_range=human_range,
            )

        return TraceErrorsResult(
            ok=True,
            code="OK",
            message=f"Found {len(errors)} error(s) in {human_range}",
            errors=errors,
            total_count=len(errors),
            time_range=human_range,
        )
    except Exception as e:
        return TraceErrorsResult(ok=False, code="API_ERROR", message=str(e))


def _collect_errors(
    langfuse: Any, from_timestamp: datetime, limit: int
) -> list[TraceErrorInfo]:
    """Collect errors from observations within time range."""
    errors: list[TraceErrorInfo] = []
    seen: set[tuple[str, str]] = set()
    cursor = None

    while len(errors) < limit:
        obs_kwargs: dict[str, Any] = {
            "limit": min(100, limit * 2),
            "from_start_time": from_timestamp,
        }
        if cursor:
            obs_kwargs["cursor"] = cursor

        obs_response = langfuse.api.observations_v_2.get_many(**obs_kwargs)

        for obs in obs_response.data:
            error_info = _extract_error_if_present(obs, seen)
            if error_info:
                errors.append(error_info)
                if len(errors) >= limit:
                    break

        cursor = _get_next_cursor(obs_response)
        if not cursor:
            break

    return errors


def _extract_error_if_present(
    obs: Any, seen: set[tuple[str, str]]
) -> TraceErrorInfo | None:
    """Extract error info from observation if it has an error level."""
    level = _safe_get(obs, "level")
    if level not in ("ERROR", "FATAL", "CRITICAL"):
        return None

    trace_id = _safe_get(obs, "trace_id")
    if not trace_id:
        return None

    obs_id = str(_safe_get(obs, "id", ""))
    key = (str(trace_id), obs_id)
    if key in seen:
        return None
    seen.add(key)

    return TraceErrorInfo(
        trace_id=str(trace_id),
        trace_name=None,
        trace_timestamp=_format_timestamp(_safe_get(obs, "start_time")),
        observation_id=obs_id,
        observation_name=_safe_get(obs, "name"),
        observation_type=str(_safe_get(obs, "type", "UNKNOWN")),
        error_message=_safe_get(obs, "status_message"),
        error_level=str(level),
    )


def _get_next_cursor(response: Any) -> str | None:
    """Get cursor for next page from response metadata."""
    if hasattr(response, "meta") and response.meta:
        return getattr(response.meta, "cursor", None)
    return None
