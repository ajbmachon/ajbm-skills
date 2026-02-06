"""Langfuse SDK v3 utilities for trace querying and evaluation.

DEPRECATED: This module exists for backward compatibility only.
New code should import directly from the lib package:

    from lib import get_langfuse, auth_check, fetch_traces, ...

Or from specific modules:

    from lib.client import get_langfuse, auth_check
    from lib.traces import fetch_traces, fetch_trace
    from lib.scores import create_score, fetch_scores

This file re-exports all public symbols from the new modular structure.
"""

# Re-export everything from the new modular structure
from .models import (
    # Error codes
    API_ERROR,
    AUTH_EXPIRED,
    AUTH_INVALID,
    AUTH_MISSING,
    NETWORK_ERROR,
    NETWORK_TIMEOUT,
    NOT_FOUND,
    RATE_LIMITED,
    REGION_MISMATCH,
    # Constants
    ERROR_MESSAGES,
    LANGFUSE_REGIONS,
    MAX_RETRIES,
    SCORE_DATA_TYPES,
    # Base results
    AuthResult,
    DiagnosisIssue,
    DiagnosisResult,
    LangfuseError,
    Result,
    # Trace results
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
    # Error results
    TraceErrorInfo,
    TraceErrorsResult,
    # Cost results
    CostByDay,
    CostByModel,
    CostByTrace,
    CostGroup,
    TraceCostsResult,
    # Score results
    ScoreCreateResult,
    ScoreInfo,
    ScoreListResult,
)

from .client import (
    DEFAULT_TIMEOUT,
    LangfuseClient,
    auth_check,
    flush,
    get_langfuse,
)

from .traces import (
    analyze_trace,
    fetch_trace,
    fetch_traces,
)

from .scores import (
    create_score,
    fetch_scores,
)

from .errors import (
    fetch_errors,
)

from .costs import (
    fetch_costs,
)

# For backward compatibility, also export load_dotenv since it was used in monkeypatching tests
from dotenv import load_dotenv

__all__ = [
    # Error codes
    "AUTH_EXPIRED",
    "AUTH_INVALID",
    "AUTH_MISSING",
    "API_ERROR",
    "NETWORK_ERROR",
    "NETWORK_TIMEOUT",
    "NOT_FOUND",
    "RATE_LIMITED",
    "REGION_MISMATCH",
    # Constants
    "ERROR_MESSAGES",
    "LANGFUSE_REGIONS",
    "MAX_RETRIES",
    "SCORE_DATA_TYPES",
    "DEFAULT_TIMEOUT",
    # Client functions
    "get_langfuse",
    "auth_check",
    "flush",
    # Trace functions
    "fetch_traces",
    "fetch_trace",
    "analyze_trace",
    "fetch_errors",
    "fetch_costs",
    # Score functions
    "create_score",
    "fetch_scores",
    # Result dataclasses
    "Result",
    "AuthResult",
    "DiagnosisIssue",
    "DiagnosisResult",
    "TraceInfo",
    "TraceListResult",
    "ObservationInfo",
    "TraceDetail",
    "TraceGetResult",
    "BottleneckInfo",
    "ErrorInfo",
    "LatencyStats",
    "TraceAnalysis",
    "TraceAnalyzeResult",
    "TraceErrorInfo",
    "TraceErrorsResult",
    "CostGroup",
    "CostByModel",
    "CostByTrace",
    "CostByDay",
    "TraceCostsResult",
    "ScoreInfo",
    "ScoreCreateResult",
    "ScoreListResult",
    # Backward compatibility
    "LangfuseClient",
    "LangfuseError",
    "load_dotenv",
]
