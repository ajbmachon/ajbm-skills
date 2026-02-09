"""Langfuse data models and result dataclasses.

This module contains:
- Result dataclasses for consistent return types
- Error code constants and messages
- Region constants
"""

from __future__ import annotations

from dataclasses import dataclass, field

# -----------------------------------------------------------------------------
# Error Code Constants
# -----------------------------------------------------------------------------

AUTH_MISSING = "AUTH_MISSING"
AUTH_INVALID = "AUTH_INVALID"
AUTH_EXPIRED = "AUTH_EXPIRED"
NETWORK_ERROR = "NETWORK_ERROR"
NETWORK_TIMEOUT = "NETWORK_TIMEOUT"
RATE_LIMITED = "RATE_LIMITED"
REGION_MISMATCH = "REGION_MISMATCH"
NOT_FOUND = "NOT_FOUND"
API_ERROR = "API_ERROR"

# Region constants
LANGFUSE_REGIONS = {
    "EU": "https://cloud.langfuse.com",
    "US": "https://us.cloud.langfuse.com",
}

# Retry configuration
MAX_RETRIES = 3

# Human-readable error messages
ERROR_MESSAGES: dict[str, str] = {
    AUTH_MISSING: (
        "Langfuse credentials not found. "
        "Please set LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, and LANGFUSE_BASE_URL "
        "in your .env file. See: https://langfuse.com/docs/get-started"
    ),
    AUTH_INVALID: (
        "Langfuse authentication failed. Check your API keys are correct. "
        "Keys should start with 'sk-lf-' (secret) and 'pk-lf-' (public)."
    ),
    AUTH_EXPIRED: (
        "Langfuse API keys appear to be expired. "
        "Please generate new keys in the Langfuse dashboard."
    ),
    NETWORK_ERROR: (
        "Could not connect to Langfuse. Check your internet connection and "
        "verify LANGFUSE_BASE_URL is correct. "
        "EU: https://cloud.langfuse.com | US: https://us.cloud.langfuse.com"
    ),
    NETWORK_TIMEOUT: (
        "Connection to Langfuse timed out. Check your internet connection."
    ),
    RATE_LIMITED: (
        "Langfuse API rate limit exceeded. Please wait a moment before retrying."
    ),
    REGION_MISMATCH: (
        "Your API keys appear to be for a different region than your configured "
        "LANGFUSE_BASE_URL."
    ),
    NOT_FOUND: "The requested resource was not found in Langfuse.",
    API_ERROR: (
        "Langfuse API returned an error. Check the error details for more information."
    ),
}

# Score data types
SCORE_DATA_TYPES = ["numeric", "categorical", "boolean"]


# -----------------------------------------------------------------------------
# Base Result Dataclasses
# -----------------------------------------------------------------------------


@dataclass
class Result:
    """Base result with status information."""

    ok: bool
    code: str
    message: str


@dataclass
class AuthResult:
    """Result of an authentication check."""

    code: str
    message: str

    @property
    def ok(self) -> bool:
        """Return True if authentication succeeded."""
        return self.code == "OK"


@dataclass
class DiagnosisIssue:
    """A single issue found during diagnosis."""

    code: str
    severity: str  # "error", "warning", "info"
    message: str
    detail: str


@dataclass
class DiagnosisResult:
    """Result of a comprehensive diagnosis."""

    healthy: bool
    summary: str
    issues: list[DiagnosisIssue]
    next_steps: list[str]


# -----------------------------------------------------------------------------
# Trace Result Dataclasses
# -----------------------------------------------------------------------------


@dataclass
class TraceInfo:
    """Essential trace information for list display."""

    id: str
    name: str | None
    timestamp: str
    status: str  # "success" or "error"
    user_id: str | None = None
    session_id: str | None = None
    latency_ms: float | None = None
    cost: float | None = None


@dataclass
class TraceListResult(Result):
    """Result of fetching traces."""

    traces: list[TraceInfo] = field(default_factory=list)
    has_more: bool = False
    cursor: str | None = None
    page: int | None = None
    total_pages: int | None = None
    total_items: int | None = None


@dataclass
class ObservationInfo:
    """Observation details within a trace."""

    id: str
    type: str  # "GENERATION", "SPAN", "EVENT"
    name: str | None
    start_time: str
    end_time: str | None = None
    duration_ms: float | None = None
    level: str | None = None
    status_message: str | None = None
    model: str | None = None
    input: str | None = None
    output: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    cost: float | None = None
    parent_observation_id: str | None = None


@dataclass
class TraceDetail:
    """Full trace with observations."""

    id: str
    name: str | None
    timestamp: str
    session_id: str | None = None
    user_id: str | None = None
    input: str | None = None
    output: str | None = None
    metadata: dict | None = None
    tags: list[str] | None = None
    observations: list[ObservationInfo] = field(default_factory=list)


@dataclass
class TraceGetResult(Result):
    """Result of fetching a single trace."""

    trace: TraceDetail | None = None


# -----------------------------------------------------------------------------
# Analysis Result Dataclasses
# -----------------------------------------------------------------------------


@dataclass
class BottleneckInfo:
    """Latency bottleneck in a trace."""

    observation_id: str
    observation_name: str | None
    observation_type: str
    duration_ms: float
    percentage_of_total: float
    model: str | None = None


@dataclass
class ErrorInfo:
    """Error in a trace observation."""

    observation_id: str
    observation_name: str | None
    observation_type: str
    level: str
    status_message: str | None
    timestamp: str


@dataclass
class LatencyStats:
    """Latency statistics for trace analysis."""

    total_ms: float
    p50_ms: float | None = None
    p95_ms: float | None = None
    p99_ms: float | None = None
    observation_count: int = 0


@dataclass
class TraceAnalysis:
    """Complete analysis of a trace."""

    trace_id: str
    trace_name: str | None
    has_timing_data: bool
    has_errors: bool
    summary: str
    latency: LatencyStats | None = None
    bottlenecks: list[BottleneckInfo] = field(default_factory=list)
    errors: list[ErrorInfo] = field(default_factory=list)
    total_cost: float | None = None
    cost_by_model: dict[str, float] | None = None


@dataclass
class TraceAnalyzeResult(Result):
    """Result of trace analysis."""

    analysis: TraceAnalysis | None = None


# -----------------------------------------------------------------------------
# Error Result Dataclasses
# -----------------------------------------------------------------------------


@dataclass
class TraceErrorInfo:
    """Error found in a trace."""

    trace_id: str
    trace_name: str | None
    trace_timestamp: str
    observation_id: str
    observation_name: str | None
    observation_type: str
    error_message: str | None
    error_level: str


@dataclass
class TraceErrorsResult(Result):
    """Result of finding traces with errors."""

    errors: list[TraceErrorInfo] = field(default_factory=list)
    total_count: int = 0
    time_range: str = ""


# -----------------------------------------------------------------------------
# Cost Result Dataclasses
# -----------------------------------------------------------------------------


@dataclass
class CostGroup:
    """Cost breakdown for a group (model, trace, or day)."""

    key: str
    total_cost: float
    observation_count: int
    name: str | None = None


@dataclass
class CostByModel:
    """Backward-compatible alias for model cost breakdown."""

    model: str
    total_cost: float
    observation_count: int


@dataclass
class CostByTrace:
    """Backward-compatible alias for trace cost breakdown."""

    trace_id: str
    trace_name: str | None
    total_cost: float
    observation_count: int


@dataclass
class CostByDay:
    """Backward-compatible alias for daily cost breakdown."""

    date: str
    total_cost: float
    observation_count: int


@dataclass
class TraceCostsResult(Result):
    """Result of cost analysis."""

    total_cost: float = 0.0
    time_range: str = ""
    group_by: str = "model"
    groups: list[CostGroup] = field(default_factory=list)
    # Backward compatibility fields
    by_model: list[CostByModel] = field(default_factory=list)
    by_trace: list[CostByTrace] = field(default_factory=list)
    by_day: list[CostByDay] = field(default_factory=list)


# -----------------------------------------------------------------------------
# Score Result Dataclasses
# -----------------------------------------------------------------------------


@dataclass
class ScoreInfo:
    """Score information."""

    id: str
    trace_id: str
    name: str
    value: float | str | None
    data_type: str  # "NUMERIC", "CATEGORICAL", "BOOLEAN"
    comment: str | None = None
    observation_id: str | None = None
    timestamp: str | None = None


@dataclass
class ScoreCreateResult(Result):
    """Result of creating a score."""

    score: ScoreInfo | None = None


@dataclass
class ScoreListResult(Result):
    """Result of listing scores."""

    scores: list[ScoreInfo] = field(default_factory=list)
    total_count: int = 0
    has_more: bool = False
    cursor: str | None = None


# -----------------------------------------------------------------------------
# Exception Class
# -----------------------------------------------------------------------------


@dataclass
class LangfuseError(Exception):
    """Langfuse operation error with machine-readable code and human message."""

    code: str
    message: str

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"
