"""Cost analysis operations for Langfuse SDK.

This module provides:
- fetch_costs() - Get cost breakdown by model, trace, or day
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from .client import get_langfuse
from .models import CostGroup, TraceCostsResult

if TYPE_CHECKING:
    pass


def _safe_get(obj: Any, attr: str, default: Any = None) -> Any:
    """Safely get attribute from object or dict."""
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)


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


def fetch_costs(
    group_by: str = "model", since: str = "7d", limit: int = 20, *, langfuse: Any = None
) -> TraceCostsResult:
    """Get cost breakdown by model, trace, or day.

    Args:
        group_by: Grouping mode ('model', 'trace', 'day').
        since: Time range to analyze (e.g., '24h', '7d').
        limit: Maximum number of items to return per group.
        langfuse: Optional Langfuse client instance (for testing).

    Returns:
        TraceCostsResult with cost breakdown.
    """
    try:
        if langfuse is None:
            langfuse = get_langfuse()
        from_timestamp, human_range = _parse_time_range(since)

        cost_data, total_cost = _aggregate_costs(langfuse, from_timestamp, group_by)
        groups = _build_sorted_groups(cost_data, limit)

        return TraceCostsResult(
            ok=True,
            code="OK",
            message=f"Cost breakdown for {human_range}",
            total_cost=total_cost,
            time_range=human_range,
            group_by=group_by,
            groups=groups,
        )
    except Exception as e:
        return TraceCostsResult(ok=False, code="API_ERROR", message=str(e))


def _aggregate_costs(
    langfuse: Any, from_timestamp: datetime, group_by: str
) -> tuple[dict[str, tuple[float, int, str | None]], float]:
    """Aggregate costs from observations by grouping key."""
    cost_data: dict[str, tuple[float, int, str | None]] = {}
    total_cost = 0.0
    cursor = None

    while True:
        obs_kwargs: dict[str, Any] = {"limit": 100, "from_start_time": from_timestamp}
        if cursor:
            obs_kwargs["cursor"] = cursor

        obs_response = langfuse.api.observations_v_2.get_many(**obs_kwargs)

        for obs in obs_response.data:
            cost = _safe_get(obs, "calculated_total_cost")
            if cost is None or cost == 0:
                continue

            total_cost += cost
            key = _get_grouping_key(obs, group_by)
            existing = cost_data.get(key, (0.0, 0, None))
            cost_data[key] = (existing[0] + cost, existing[1] + 1, None)

        cursor = _get_next_cursor(obs_response)
        if not cursor:
            break

    return cost_data, total_cost


def _get_grouping_key(obs: Any, group_by: str) -> str:
    """Get the grouping key based on group_by mode."""
    if group_by == "model":
        return _safe_get(obs, "model") or "unknown"
    if group_by == "trace":
        return str(_safe_get(obs, "trace_id") or "unknown")
    # day
    start_time = _safe_get(obs, "start_time")
    if hasattr(start_time, "date"):
        return start_time.date().isoformat()
    return str(start_time)[:10]


def _get_next_cursor(response: Any) -> str | None:
    """Get cursor for next page from response metadata."""
    if hasattr(response, "meta") and response.meta:
        return getattr(response.meta, "cursor", None)
    return None


def _build_sorted_groups(
    cost_data: dict[str, tuple[float, int, str | None]], limit: int
) -> list[CostGroup]:
    """Build sorted CostGroup list from aggregated data."""
    groups = [
        CostGroup(key=k, total_cost=v[0], observation_count=v[1], name=v[2])
        for k, v in cost_data.items()
    ]
    return sorted(groups, key=lambda x: x.total_cost, reverse=True)[:limit]
