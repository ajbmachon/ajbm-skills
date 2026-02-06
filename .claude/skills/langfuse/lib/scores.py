"""Score operations for Langfuse SDK.

This module provides:
- create_score() - Create a score on a trace or observation
- fetch_scores() - Fetch scores with optional filters
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .client import flush, get_langfuse
from .models import SCORE_DATA_TYPES, ScoreCreateResult, ScoreInfo, ScoreListResult

if TYPE_CHECKING:
    pass


def _format_timestamp(ts: Any) -> str:
    """Format timestamp to ISO string."""
    if ts is None:
        return ""
    if hasattr(ts, "isoformat"):
        return ts.isoformat()
    return str(ts)


def create_score(
    trace_id: str,
    name: str,
    value: float | str,
    data_type: str = "numeric",
    comment: str | None = None,
    observation_id: str | None = None,
    *,
    langfuse: Any = None,
) -> ScoreCreateResult:
    """Create a score on a trace or observation.

    Args:
        trace_id: The trace ID to score.
        name: Score name (e.g., 'quality', 'accuracy').
        value: Score value - float for numeric/boolean, string for categorical.
        data_type: Score type ('numeric', 'categorical', 'boolean').
        comment: Optional comment explaining the score.
        observation_id: Optional observation ID to attach score to.
        langfuse: Optional Langfuse client instance (for testing).

    Returns:
        ScoreCreateResult with created score or error.
    """
    data_type_lower = data_type.lower()
    if data_type_lower not in SCORE_DATA_TYPES:
        return ScoreCreateResult(
            ok=False,
            code="INVALID_DATA_TYPE",
            message=f"Invalid data-type. Use: {', '.join(SCORE_DATA_TYPES)}",
        )

    parsed_result = _parse_score_value(value, data_type_lower)
    if isinstance(parsed_result, ScoreCreateResult):
        return parsed_result
    parsed_value = parsed_result

    try:
        if langfuse is None:
            langfuse = get_langfuse()
        langfuse_data_type = _map_data_type(data_type_lower)

        langfuse.create_score(
            trace_id=trace_id,
            name=name,
            value=parsed_value,
            data_type=langfuse_data_type,
            comment=comment,
            observation_id=observation_id,
        )
        flush()

        return ScoreCreateResult(
            ok=True,
            code="OK",
            message=f"Score '{name}' created for trace {trace_id}",
            score=ScoreInfo(
                id=f"{trace_id}-{name}",
                trace_id=trace_id,
                name=name,
                value=parsed_value,
                data_type=langfuse_data_type,
                comment=comment,
                observation_id=observation_id,
            ),
        )
    except Exception as e:
        return ScoreCreateResult(ok=False, code="API_ERROR", message=str(e))


def _parse_score_value(value: float | str, data_type: str) -> float | str | ScoreCreateResult:
    """Parse and validate score value based on data type."""
    if data_type == "numeric":
        return _parse_numeric(value)
    if data_type == "boolean":
        return _parse_boolean(value)
    return str(value)


def _parse_numeric(value: float | str) -> float | ScoreCreateResult:
    """Parse numeric score value."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return ScoreCreateResult(
            ok=False,
            code="INVALID_VALUE",
            message=f"Invalid numeric value: {value}. Must be a number.",
        )


def _parse_boolean(value: float | str) -> float | ScoreCreateResult:
    """Parse boolean score value (0 or 1)."""
    try:
        float_val = float(value)
        if float_val not in (0, 1, 0.0, 1.0):
            return ScoreCreateResult(
                ok=False,
                code="INVALID_VALUE",
                message=f"Invalid boolean value: {value}. Use 0 or 1.",
            )
        return float_val
    except (TypeError, ValueError):
        str_val = str(value).lower()
        if str_val in ("true", "1"):
            return 1.0
        if str_val in ("false", "0"):
            return 0.0
        return ScoreCreateResult(
            ok=False,
            code="INVALID_VALUE",
            message=f"Invalid boolean value: {value}. Use 0, 1, true, or false.",
        )


def _map_data_type(data_type: str) -> str:
    """Map lowercase data type to Langfuse API format."""
    return {"numeric": "NUMERIC", "categorical": "CATEGORICAL", "boolean": "BOOLEAN"}[data_type]


def fetch_scores(
    trace_id: str | None = None,
    name: str | None = None,
    limit: int = 20,
    *,
    langfuse: Any = None,
) -> ScoreListResult:
    """Fetch scores with optional filters.

    Args:
        trace_id: Filter scores by trace ID.
        name: Filter scores by name.
        limit: Maximum number of scores to return.
        langfuse: Optional Langfuse client instance (for testing).

    Returns:
        ScoreListResult with scores or error information.
    """
    try:
        if langfuse is None:
            langfuse = get_langfuse()
        kwargs: dict[str, Any] = {"limit": limit}
        if trace_id:
            kwargs["trace_id"] = trace_id
        if name:
            kwargs["name"] = name

        response = langfuse.api.score_v_2.get(**kwargs)
        scores = _parse_scores(response.data)

        cursor, has_more = _extract_pagination(response)

        return ScoreListResult(
            ok=True,
            code="OK",
            message=f"Found {len(scores)} score(s)",
            scores=scores,
            total_count=len(scores),
            has_more=has_more,
            cursor=cursor,
        )
    except Exception as e:
        return ScoreListResult(ok=False, code="API_ERROR", message=str(e))


def _parse_scores(data: Any) -> list[ScoreInfo]:
    """Parse score list response into ScoreInfo objects."""
    scores = []
    for score in data:
        scores.append(
            ScoreInfo(
                id=score.id,
                trace_id=getattr(score, "trace_id", ""),
                name=getattr(score, "name", ""),
                value=getattr(score, "value", None),
                data_type=getattr(score, "data_type", "NUMERIC"),
                comment=getattr(score, "comment", None),
                observation_id=getattr(score, "observation_id", None),
                timestamp=_format_timestamp(getattr(score, "timestamp", None)),
            )
        )
    return scores


def _extract_pagination(response: Any) -> tuple[str | None, bool]:
    """Extract cursor and has_more from response metadata."""
    cursor = None
    has_more = False
    if hasattr(response, "meta") and response.meta:
        cursor = getattr(response.meta, "cursor", None)
        has_more = cursor is not None
    return cursor, has_more
