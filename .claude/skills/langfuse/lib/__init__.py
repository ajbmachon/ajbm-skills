"""Langfuse skill shared utilities.

New SDK v3 API (preferred):
    from lib import get_langfuse, auth_check, fetch_traces, ...

Backward-compatible API:
    from lib import LangfuseClient
    client = LangfuseClient()

Module structure:
    - models.py - Result dataclasses and error constants
    - client.py - Langfuse client singleton and auth
    - traces.py - Trace fetch and analysis operations
    - scores.py - Score create and fetch operations
    - errors.py - Error discovery operations
    - costs.py - Cost analysis operations
"""

# Models and constants
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

# Client functions
from .client import (
    LangfuseClient,
    auth_check,
    flush,
    get_langfuse,
)

# Trace operations
from .traces import (
    analyze_trace,
    fetch_trace,
    fetch_traces,
)

# Score operations
from .scores import (
    create_score,
    fetch_scores,
)

# Error operations
from .errors import (
    fetch_errors,
)

# Cost operations
from .costs import (
    fetch_costs,
)

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
    # Client functions (new API)
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
]
