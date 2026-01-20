"""Shared Langfuse utilities for consistent auth, client init, and error handling.

This module provides:
- LangfuseClient wrapper class for consistent client initialization
- Auth loading from .env (LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_BASE_URL)
- Error code constants with human-readable messages
- flush() helper for short-lived operations
- Retry with exponential backoff for network operations
- Region detection and diagnosis utilities

ISC Reference: rows 53-59, 35-40
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from dotenv import load_dotenv

if TYPE_CHECKING:
    from langfuse import Langfuse

# -----------------------------------------------------------------------------
# Error Code Constants (ISC row 58)
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

# -----------------------------------------------------------------------------
# Region Constants (ISC row 38)
# -----------------------------------------------------------------------------

LANGFUSE_REGIONS = {
    "EU": "https://cloud.langfuse.com",
    "US": "https://us.cloud.langfuse.com",
}

DEFAULT_REGION = "EU"
DEFAULT_BASE_URL = LANGFUSE_REGIONS[DEFAULT_REGION]

# Retry configuration (ISC row 63)
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 1.0  # seconds
RETRY_BACKOFF_MULTIPLIER = 2.0

# -----------------------------------------------------------------------------
# Human-Readable Error Messages (ISC row 59)
# -----------------------------------------------------------------------------

ERROR_MESSAGES: dict[str, str] = {
    AUTH_MISSING: (
        "Langfuse credentials not found. "
        "Please set LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, and LANGFUSE_BASE_URL "
        "in your .env file. See: https://langfuse.com/docs/get-started"
    ),
    AUTH_INVALID: (
        "Langfuse authentication failed. Check your API keys are correct. "
        "Keys should start with 'sk-lf-' (secret) and 'pk-lf-' (public). "
        "Also verify LANGFUSE_BASE_URL matches your region (EU vs US)."
    ),
    AUTH_EXPIRED: (
        "Langfuse API keys appear to be expired. "
        "Please generate new keys in the Langfuse dashboard: Settings > API Keys. "
        "See: https://langfuse.com/docs/get-started"
    ),
    NETWORK_ERROR: (
        "Could not connect to Langfuse. Check your internet connection and "
        "verify LANGFUSE_BASE_URL is correct. "
        "EU: https://cloud.langfuse.com | US: https://us.cloud.langfuse.com"
    ),
    NETWORK_TIMEOUT: (
        "Connection to Langfuse timed out after retrying. "
        "Check your internet connection and try again. "
        "If the issue persists, check Langfuse status at https://status.langfuse.com"
    ),
    RATE_LIMITED: (
        "Langfuse API rate limit exceeded. Please wait a moment before retrying. "
        "For high-volume usage, consider implementing request batching."
    ),
    REGION_MISMATCH: (
        "Your API keys appear to be for a different region than your configured "
        "LANGFUSE_BASE_URL. EU keys work with https://cloud.langfuse.com, "
        "US keys work with https://us.cloud.langfuse.com."
    ),
    NOT_FOUND: ("The requested resource was not found in Langfuse."),
    API_ERROR: (
        "Langfuse API returned an error. Check the error details for more information."
    ),
}


# -----------------------------------------------------------------------------
# Custom Exception
# -----------------------------------------------------------------------------


@dataclass
class LangfuseError(Exception):
    """Langfuse operation error with machine-readable code and human message."""

    code: str
    message: str

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


# -----------------------------------------------------------------------------
# LangfuseClient Wrapper (ISC rows 53-57)
# -----------------------------------------------------------------------------


class LangfuseClient:
    """Wrapper for Langfuse client with consistent auth and error handling.

    Provides:
    - Auth loading from .env (ISC row 55)
    - Client initialization (ISC row 54)
    - flush() helper for short-lived operations (ISC row 57)
    - Consistent error handling with codes (ISC rows 58-59)

    Usage:
        client = LangfuseClient()
        result = client.auth_check()
        if result.code != "OK":
            print(result.message)
        else:
            # Use client.langfuse for operations
            client.flush()  # Before exit in short-lived scripts
    """

    def __init__(self, env_path: Path | str | None = None) -> None:
        """Initialize client, loading auth from .env.

        Args:
            env_path: Optional path to .env file. Defaults to project root.

        Raises:
            LangfuseError: If required credentials are missing or empty.
        """
        self._langfuse: Langfuse | None = None
        self._env_path = Path(env_path) if env_path else None
        self._load_env()
        self._validate_auth()

    def _load_env(self) -> None:
        """Load environment variables from .env file."""
        if self._env_path and self._env_path.exists():
            load_dotenv(self._env_path)
        else:
            # Try common locations: cwd, then parent directories
            load_dotenv()  # Loads from cwd or finds .env up the tree

    def _validate_auth(self) -> None:
        """Validate that required auth credentials are present and non-empty.

        Raises:
            LangfuseError: If credentials are missing or empty.
        """
        secret_key = os.getenv("LANGFUSE_SECRET_KEY", "").strip()
        public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "").strip()

        # ISC acceptance criteria: Empty LANGFUSE_SECRET_KEY -> AUTH_MISSING
        if not secret_key or not public_key:
            missing = []
            if not secret_key:
                missing.append("LANGFUSE_SECRET_KEY")
            if not public_key:
                missing.append("LANGFUSE_PUBLIC_KEY")

            raise LangfuseError(
                code=AUTH_MISSING,
                message=(
                    f"Missing required credentials: {', '.join(missing)}. "
                    f"{ERROR_MESSAGES[AUTH_MISSING]}"
                ),
            )

    @property
    def langfuse(self) -> Langfuse:
        """Get or create the Langfuse client instance.

        Returns:
            Initialized Langfuse client.

        Note:
            Client is lazily initialized on first access.
        """
        if self._langfuse is None:
            from langfuse import Langfuse

            self._langfuse = Langfuse()
        return self._langfuse

    @property
    def secret_key(self) -> str:
        """Get the configured secret key."""
        return os.getenv("LANGFUSE_SECRET_KEY", "")

    @property
    def public_key(self) -> str:
        """Get the configured public key."""
        return os.getenv("LANGFUSE_PUBLIC_KEY", "")

    @property
    def base_url(self) -> str:
        """Get the configured base URL (defaults to EU cloud)."""
        return os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")

    def flush(self) -> None:
        """Flush pending events to Langfuse (ISC row 57).

        Must be called before exit in short-lived applications (scripts, CLI tools,
        serverless functions) to ensure all events are transmitted.

        Note:
            For long-running applications (web servers), the SDK handles
            batching automatically and explicit flush is not required during
            normal operation.
        """
        if self._langfuse is not None:
            self._langfuse.flush()

    def auth_check(self, retry: bool = True) -> AuthResult:
        """Verify authentication and connection to Langfuse.

        Args:
            retry: If True, retry on network errors with exponential backoff (ISC row 63).

        Returns:
            AuthResult with code and message indicating status.

        Note:
            Does not raise exceptions - returns error codes for handling.
        """
        last_error: Exception | None = None
        attempts = MAX_RETRIES if retry else 1

        for attempt in range(attempts):
            try:
                # Attempt to make a simple API call to verify auth
                self.langfuse.auth_check()
                return AuthResult(code="OK", message="Successfully connected to Langfuse")
            except Exception as e:
                last_error = e
                error_str = str(e).lower()

                # Don't retry auth errors - they won't change
                if "401" in error_str or "unauthorized" in error_str:
                    return AuthResult(
                        code=AUTH_INVALID,
                        message=ERROR_MESSAGES[AUTH_INVALID],
                    )

                # Don't retry rate limiting - wait is needed
                if "429" in error_str or "rate" in error_str:
                    return AuthResult(
                        code=RATE_LIMITED,
                        message=ERROR_MESSAGES[RATE_LIMITED],
                    )

                # Network errors - retry with backoff
                is_network_error = any(
                    term in error_str
                    for term in ["connection", "timeout", "network", "dns", "refused"]
                )

                if is_network_error and attempt < attempts - 1:
                    # Exponential backoff
                    wait_time = RETRY_BACKOFF_BASE * (RETRY_BACKOFF_MULTIPLIER**attempt)
                    time.sleep(wait_time)
                    continue

                # Final attempt or non-retryable error
                if is_network_error:
                    return AuthResult(
                        code=NETWORK_TIMEOUT,
                        message=ERROR_MESSAGES[NETWORK_TIMEOUT],
                    )

                # Unknown error - include original message
                return AuthResult(
                    code=NETWORK_ERROR,
                    message=f"Langfuse connection failed: {e}",
                )

        # Should not reach here, but handle gracefully
        return AuthResult(
            code=NETWORK_ERROR,
            message=f"Langfuse connection failed after {attempts} attempts: {last_error}",
        )

    def diagnose(self) -> DiagnosisResult:
        """Diagnose common auth and connection issues (ISC rows 36-40).

        Performs comprehensive checks to identify setup problems:
        - Validates key format (sk-lf-, pk-lf- prefixes)
        - Checks for region mismatch (EU vs US)
        - Tests network connectivity
        - Provides specific remediation steps

        Returns:
            DiagnosisResult with detailed findings and next steps.
        """
        issues: list[DiagnosisIssue] = []
        next_steps: list[str] = []

        # Check 1: Key format validation
        secret_key = self.secret_key
        public_key = self.public_key

        if secret_key and not secret_key.startswith("sk-lf-"):
            issues.append(
                DiagnosisIssue(
                    code="INVALID_SECRET_KEY_FORMAT",
                    severity="error",
                    message="Secret key should start with 'sk-lf-'",
                    detail=f"Your key starts with '{secret_key[:8]}...' instead",
                )
            )
            next_steps.append(
                "Get a new secret key from Langfuse dashboard: Settings > API Keys"
            )

        if public_key and not public_key.startswith("pk-lf-"):
            issues.append(
                DiagnosisIssue(
                    code="INVALID_PUBLIC_KEY_FORMAT",
                    severity="error",
                    message="Public key should start with 'pk-lf-'",
                    detail=f"Your key starts with '{public_key[:8]}...' instead",
                )
            )
            next_steps.append(
                "Get a new public key from Langfuse dashboard: Settings > API Keys"
            )

        # Check 2: Region detection and mismatch
        configured_url = self.base_url.rstrip("/")
        configured_region = self._detect_region_from_url(configured_url)
        key_region = self._detect_region_from_key(secret_key)

        if key_region and configured_region and key_region != configured_region:
            issues.append(
                DiagnosisIssue(
                    code=REGION_MISMATCH,
                    severity="error",
                    message=f"Your keys appear to be for {key_region} cloud, "
                    f"but LANGFUSE_BASE_URL points to {configured_region}",
                    detail=f"Keys: {key_region} | URL: {configured_url}",
                )
            )
            correct_url = LANGFUSE_REGIONS.get(key_region, configured_url)
            next_steps.append(
                f"Set LANGFUSE_BASE_URL={correct_url} in your .env file"
            )

        # Check 3: Test actual connection
        auth_result = self.auth_check(retry=True)

        if not auth_result.ok:
            issues.append(
                DiagnosisIssue(
                    code=auth_result.code,
                    severity="error",
                    message="Connection test failed",
                    detail=auth_result.message,
                )
            )

            # Add specific next steps based on error type
            if auth_result.code == AUTH_INVALID:
                next_steps.append("Verify your API keys are correct in .env")
                next_steps.append("Check if keys have been rotated in Langfuse dashboard")
            elif auth_result.code in (NETWORK_ERROR, NETWORK_TIMEOUT):
                next_steps.append("Check your internet connection")
                next_steps.append("Verify LANGFUSE_BASE_URL is accessible")
            elif auth_result.code == RATE_LIMITED:
                next_steps.append("Wait a few minutes before retrying")

        # Build summary
        if not issues:
            return DiagnosisResult(
                healthy=True,
                summary="All checks passed. Your Langfuse setup is working correctly.",
                issues=[],
                next_steps=[],
            )

        return DiagnosisResult(
            healthy=False,
            summary=f"Found {len(issues)} issue(s) with your Langfuse setup.",
            issues=issues,
            next_steps=list(dict.fromkeys(next_steps)),  # Dedupe while preserving order
        )

    def _detect_region_from_url(self, url: str) -> str | None:
        """Detect region from base URL."""
        url_lower = url.lower()
        if "us.cloud.langfuse.com" in url_lower:
            return "US"
        if "cloud.langfuse.com" in url_lower:
            return "EU"
        # Custom/self-hosted - can't determine
        return None

    def _detect_region_from_key(self, key: str) -> str | None:
        """Attempt to detect region from key format.

        Note: This is a heuristic. Langfuse may encode region in keys,
        but there's no official documentation on this. We check common patterns.
        """
        if not key:
            return None
        # Currently, there's no reliable way to detect region from key format
        # This is a placeholder for future enhancement if Langfuse adds region encoding
        return None

    def fetch_traces(
        self,
        limit: int = 10,
        name: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
    ) -> TraceListResult:
        """Fetch recent traces with optional filters (ISC row 14).

        Uses the Langfuse API to fetch traces with cursor-based pagination.
        Supports filtering by name, user_id, and session_id.

        Args:
            limit: Maximum number of traces to return (default: 10)
            name: Filter traces by name
            user_id: Filter traces by user ID
            session_id: Filter traces by session ID

        Returns:
            TraceListResult with traces and status information.
        """
        try:
            # Build kwargs for trace list API call
            kwargs: dict = {"limit": limit}
            if name:
                kwargs["name"] = name
            if user_id:
                kwargs["user_id"] = user_id
            if session_id:
                kwargs["session_id"] = session_id

            # Fetch traces using the SDK API
            response = self.langfuse.api.trace.list(**kwargs)

            # Process traces into TraceInfo objects
            traces: list[TraceInfo] = []
            for trace in response.data:
                # Determine status based on observation errors or level
                # Traces don't have direct status, so we check for errors in metadata
                status = "success"
                if hasattr(trace, "level") and trace.level == "ERROR":
                    status = "error"

                # Format timestamp for display
                timestamp = ""
                if hasattr(trace, "timestamp") and trace.timestamp:
                    timestamp = trace.timestamp.isoformat() if hasattr(trace.timestamp, "isoformat") else str(trace.timestamp)

                trace_info = TraceInfo(
                    id=trace.id,
                    name=trace.name,
                    timestamp=timestamp,
                    status=status,
                    user_id=getattr(trace, "user_id", None),
                    session_id=getattr(trace, "session_id", None),
                )
                traces.append(trace_info)

            # Check for pagination cursor
            has_more = False
            cursor = None
            if hasattr(response, "meta") and response.meta:
                cursor = getattr(response.meta, "cursor", None)
                has_more = cursor is not None

            return TraceListResult(
                ok=True,
                code="OK",
                message=f"Found {len(traces)} trace(s)",
                traces=traces,
                has_more=has_more,
                cursor=cursor,
            )

        except Exception as e:
            error_str = str(e).lower()

            # Determine error type
            if "401" in error_str or "unauthorized" in error_str:
                return TraceListResult(
                    ok=False,
                    code=AUTH_INVALID,
                    message=ERROR_MESSAGES[AUTH_INVALID],
                    traces=[],
                )
            if "404" in error_str or "not found" in error_str:
                return TraceListResult(
                    ok=False,
                    code=NOT_FOUND,
                    message=ERROR_MESSAGES[NOT_FOUND],
                    traces=[],
                )
            if "429" in error_str or "rate" in error_str:
                return TraceListResult(
                    ok=False,
                    code=RATE_LIMITED,
                    message=ERROR_MESSAGES[RATE_LIMITED],
                    traces=[],
                )

            # Generic API error
            return TraceListResult(
                ok=False,
                code=API_ERROR,
                message=f"Failed to fetch traces: {e}",
                traces=[],
            )

    def fetch_trace(self, trace_id: str) -> TraceGetResult:
        """Fetch a single trace with all observations (ISC rows 15, 20).

        Retrieves the trace and all associated observations, building a hierarchy
        suitable for display: Session -> Trace -> Observations.

        Args:
            trace_id: The ID of the trace to fetch.

        Returns:
            TraceGetResult with trace details and observations.
        """
        try:
            # Fetch the trace first
            trace = self.langfuse.api.trace.get(trace_id)

            # Format timestamp
            timestamp = ""
            if hasattr(trace, "timestamp") and trace.timestamp:
                timestamp = (
                    trace.timestamp.isoformat()
                    if hasattr(trace.timestamp, "isoformat")
                    else str(trace.timestamp)
                )

            # Format input/output for display (truncate if too long)
            trace_input = None
            if hasattr(trace, "input") and trace.input:
                trace_input = (
                    str(trace.input)[:500] + "..."
                    if len(str(trace.input)) > 500
                    else str(trace.input)
                )

            trace_output = None
            if hasattr(trace, "output") and trace.output:
                trace_output = (
                    str(trace.output)[:500] + "..."
                    if len(str(trace.output)) > 500
                    else str(trace.output)
                )

            # Fetch observations for this trace using v2 API
            observations: list[ObservationInfo] = []
            cursor = None

            while True:
                obs_kwargs: dict = {
                    "trace_id": trace_id,
                    "limit": 100,
                }
                if cursor:
                    obs_kwargs["cursor"] = cursor

                obs_response = self.langfuse.api.observations_v_2.get_many(**obs_kwargs)

                for obs in obs_response.data:
                    # Calculate duration if start/end times available
                    duration_ms = None
                    start_time_str = ""
                    end_time_str = None

                    if hasattr(obs, "start_time") and obs.start_time:
                        start_time_str = (
                            obs.start_time.isoformat()
                            if hasattr(obs.start_time, "isoformat")
                            else str(obs.start_time)
                        )

                    if hasattr(obs, "end_time") and obs.end_time:
                        end_time_str = (
                            obs.end_time.isoformat()
                            if hasattr(obs.end_time, "isoformat")
                            else str(obs.end_time)
                        )

                        # Calculate duration in ms
                        if hasattr(obs, "start_time") and obs.start_time:
                            try:
                                duration_s = (
                                    obs.end_time - obs.start_time
                                ).total_seconds()
                                duration_ms = duration_s * 1000
                            except (TypeError, AttributeError):
                                pass

                    # Format input/output
                    obs_input = None
                    if hasattr(obs, "input") and obs.input:
                        obs_input = (
                            str(obs.input)[:300] + "..."
                            if len(str(obs.input)) > 300
                            else str(obs.input)
                        )

                    obs_output = None
                    if hasattr(obs, "output") and obs.output:
                        obs_output = (
                            str(obs.output)[:300] + "..."
                            if len(str(obs.output)) > 300
                            else str(obs.output)
                        )

                    # Extract usage/cost data
                    input_tokens = None
                    output_tokens = None
                    total_tokens = None
                    cost = None

                    if hasattr(obs, "usage") and obs.usage:
                        input_tokens = getattr(obs.usage, "input", None)
                        output_tokens = getattr(obs.usage, "output", None)
                        total_tokens = getattr(obs.usage, "total", None)

                    if hasattr(obs, "calculated_total_cost") and obs.calculated_total_cost:
                        cost = obs.calculated_total_cost

                    obs_info = ObservationInfo(
                        id=obs.id,
                        type=getattr(obs, "type", "UNKNOWN"),
                        name=getattr(obs, "name", None),
                        start_time=start_time_str,
                        end_time=end_time_str,
                        duration_ms=duration_ms,
                        level=getattr(obs, "level", None),
                        status_message=getattr(obs, "status_message", None),
                        model=getattr(obs, "model", None),
                        input=obs_input,
                        output=obs_output,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        total_tokens=total_tokens,
                        cost=cost,
                        parent_observation_id=getattr(obs, "parent_observation_id", None),
                    )
                    observations.append(obs_info)

                # Check for more pages
                cursor = None
                if hasattr(obs_response, "meta") and obs_response.meta:
                    cursor = getattr(obs_response.meta, "cursor", None)

                if not cursor:
                    break

            # Build trace detail
            trace_detail = TraceDetail(
                id=trace.id,
                name=getattr(trace, "name", None),
                timestamp=timestamp,
                session_id=getattr(trace, "session_id", None),
                user_id=getattr(trace, "user_id", None),
                input=trace_input,
                output=trace_output,
                metadata=getattr(trace, "metadata", None),
                tags=getattr(trace, "tags", None),
                observations=observations,
            )

            return TraceGetResult(
                ok=True,
                code="OK",
                message=f"Found trace with {len(observations)} observation(s)",
                trace=trace_detail,
            )

        except Exception as e:
            error_str = str(e).lower()

            # Check for not found error
            if "404" in error_str or "not found" in error_str:
                return TraceGetResult(
                    ok=False,
                    code=NOT_FOUND,
                    message=f"Trace not found: {trace_id}",
                    trace=None,
                )

            # Auth errors
            if "401" in error_str or "unauthorized" in error_str:
                return TraceGetResult(
                    ok=False,
                    code=AUTH_INVALID,
                    message=ERROR_MESSAGES[AUTH_INVALID],
                    trace=None,
                )

            # Rate limiting
            if "429" in error_str or "rate" in error_str:
                return TraceGetResult(
                    ok=False,
                    code=RATE_LIMITED,
                    message=ERROR_MESSAGES[RATE_LIMITED],
                    trace=None,
                )

            # Generic API error
            return TraceGetResult(
                ok=False,
                code=API_ERROR,
                message=f"Failed to fetch trace: {e}",
                trace=None,
            )

    def analyze_trace(self, trace_id: str) -> TraceAnalyzeResult:
        """Analyze a trace for latency bottlenecks and issues (ISC rows 16, 21, 69).

        Performs comprehensive analysis of a trace:
        - Identifies slowest observations and their contribution to total time
        - Highlights error observations first
        - Calculates latency statistics (p50, p95, p99 if enough data)
        - Provides insight-first output with key findings before supporting data

        Args:
            trace_id: The ID of the trace to analyze.

        Returns:
            TraceAnalyzeResult with analysis or error information.

        Examples:
            - 'Your p95 latency is 3.2s, caused by the embedding-lookup span (2.8s average)'
            - Trace with errors -> highlights error observations first
            - No timing data -> 'Cannot analyze: no timing data available'
        """
        # First, fetch the trace with observations
        trace_result = self.fetch_trace(trace_id)

        if not trace_result.ok:
            return TraceAnalyzeResult(
                ok=False,
                code=trace_result.code,
                message=trace_result.message,
                analysis=None,
            )

        trace = trace_result.trace
        if trace is None:
            return TraceAnalyzeResult(
                ok=False,
                code=NOT_FOUND,
                message=f"Trace not found: {trace_id}",
                analysis=None,
            )

        # Collect timing data from observations
        durations: list[tuple[ObservationInfo, float]] = []
        errors: list[ErrorInfo] = []
        total_cost = 0.0
        cost_by_model: dict[str, float] = {}

        for obs in trace.observations:
            # Collect duration data
            if obs.duration_ms is not None:
                durations.append((obs, obs.duration_ms))

            # Collect errors
            if obs.level in ("ERROR", "FATAL", "CRITICAL"):
                errors.append(
                    ErrorInfo(
                        observation_id=obs.id,
                        observation_name=obs.name,
                        observation_type=obs.type,
                        level=obs.level,
                        status_message=obs.status_message,
                        timestamp=obs.start_time,
                    )
                )

            # Collect costs
            if obs.cost is not None:
                total_cost += obs.cost
                model = obs.model or "unknown"
                cost_by_model[model] = cost_by_model.get(model, 0.0) + obs.cost

        # Check for timing data (negative case)
        has_timing_data = len(durations) > 0
        has_errors = len(errors) > 0

        if not has_timing_data:
            return TraceAnalyzeResult(
                ok=False,
                code=NO_TIMING_DATA,
                message="Cannot analyze: no timing data available",
                analysis=TraceAnalysis(
                    trace_id=trace_id,
                    trace_name=trace.name,
                    has_timing_data=False,
                    has_errors=has_errors,
                    summary="Cannot analyze: no timing data available",
                    latency=None,
                    bottlenecks=[],
                    errors=errors,
                    total_cost=total_cost if total_cost > 0 else None,
                    cost_by_model=cost_by_model if cost_by_model else None,
                ),
            )

        # Calculate latency statistics
        sorted_durations = sorted([d for _, d in durations])
        total_latency = sum(sorted_durations)

        def percentile(data: list[float], p: float) -> float:
            """Calculate percentile value."""
            if not data:
                return 0.0
            k = (len(data) - 1) * (p / 100.0)
            f = int(k)
            c = f + 1 if f + 1 < len(data) else f
            if f == c:
                return data[f]
            return data[f] * (c - k) + data[c] * (k - f)

        # Only calculate percentiles if we have enough data points
        latency = LatencyStats(
            total_ms=total_latency,
            p50_ms=percentile(sorted_durations, 50) if len(sorted_durations) >= 3 else None,
            p95_ms=percentile(sorted_durations, 95) if len(sorted_durations) >= 3 else None,
            p99_ms=percentile(sorted_durations, 99) if len(sorted_durations) >= 3 else None,
            observation_count=len(sorted_durations),
        )

        # Identify bottlenecks (sorted by duration descending)
        bottlenecks: list[BottleneckInfo] = []
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

        # Generate insight-first summary
        summary_parts = []

        # Errors first (ISC row 16: highlights error observations first)
        if has_errors:
            summary_parts.append(f"Found {len(errors)} error(s) in trace")

        # Key latency insight
        if bottlenecks:
            top = bottlenecks[0]
            top_name = top.observation_name or top.observation_type
            summary_parts.append(
                f"Total latency: {total_latency:.0f}ms, "
                f"slowest: {top_name} ({top.duration_ms:.0f}ms, {top.percentage_of_total:.0f}%)"
            )

            # Add percentile insight if available
            if latency.p95_ms is not None:
                summary_parts.append(f"p50: {latency.p50_ms:.0f}ms, p95: {latency.p95_ms:.0f}ms")

        summary = ". ".join(summary_parts) if summary_parts else "Trace analyzed successfully"

        return TraceAnalyzeResult(
            ok=True,
            code="OK",
            message=summary,
            analysis=TraceAnalysis(
                trace_id=trace_id,
                trace_name=trace.name,
                has_timing_data=True,
                has_errors=has_errors,
                summary=summary,
                latency=latency,
                bottlenecks=bottlenecks,
                errors=errors,
                total_cost=total_cost if total_cost > 0 else None,
                cost_by_model=cost_by_model if cost_by_model else None,
            ),
        )


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
    """Result of a comprehensive diagnosis (ISC rows 36-40)."""

    healthy: bool
    summary: str
    issues: list[DiagnosisIssue]
    next_steps: list[str]


@dataclass
class TraceInfo:
    """Information about a single trace (ISC row 14).

    Represents the essential information displayed in trace list output.
    """

    id: str
    name: str | None
    timestamp: str
    status: str  # "success" or "error"
    user_id: str | None = None
    session_id: str | None = None


@dataclass
class TraceListResult:
    """Result of fetching traces (ISC row 14).

    Contains traces and metadata about the fetch operation.
    """

    ok: bool
    code: str
    message: str
    traces: list[TraceInfo]
    has_more: bool = False
    cursor: str | None = None


@dataclass
class ObservationInfo:
    """Information about a single observation (ISC rows 15, 20).

    Represents detailed observation data for trace hierarchy display.
    """

    id: str
    type: str  # "GENERATION", "SPAN", "EVENT"
    name: str | None
    start_time: str
    end_time: str | None
    duration_ms: float | None  # Calculated from start/end
    level: str | None  # Log level
    status_message: str | None
    model: str | None
    input: str | None
    output: str | None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    cost: float | None = None
    parent_observation_id: str | None = None


@dataclass
class TraceDetail:
    """Detailed trace information with observations (ISC rows 15, 20).

    Contains full trace data including all child observations for hierarchy display.
    """

    id: str
    name: str | None
    timestamp: str
    session_id: str | None
    user_id: str | None
    input: str | None
    output: str | None
    metadata: dict | None
    tags: list[str] | None
    observations: list[ObservationInfo]


@dataclass
class TraceGetResult:
    """Result of fetching a single trace (ISC row 15).

    Contains the trace details or error information.
    """

    ok: bool
    code: str
    message: str
    trace: TraceDetail | None = None


# -----------------------------------------------------------------------------
# Trace Analysis Data Classes (ISC row 16, 21, 69)
# -----------------------------------------------------------------------------


@dataclass
class BottleneckInfo:
    """Information about a latency bottleneck in a trace.

    Identifies observations that contribute significantly to total latency.
    """

    observation_id: str
    observation_name: str | None
    observation_type: str
    duration_ms: float
    percentage_of_total: float  # How much this contributes to total latency
    model: str | None = None


@dataclass
class ErrorInfo:
    """Information about an error in a trace observation."""

    observation_id: str
    observation_name: str | None
    observation_type: str
    level: str
    status_message: str | None
    timestamp: str


@dataclass
class LatencyStats:
    """Latency statistics for trace analysis.

    Contains p50, p95, p99 percentiles when analyzing multiple observations.
    """

    total_ms: float
    p50_ms: float | None = None
    p95_ms: float | None = None
    p99_ms: float | None = None
    observation_count: int = 0


@dataclass
class TraceAnalysis:
    """Complete analysis of a trace (ISC rows 16, 21, 69).

    Provides insight-first output with key findings before supporting data.
    """

    trace_id: str
    trace_name: str | None
    has_timing_data: bool
    has_errors: bool

    # Key findings (insight-first)
    summary: str  # Human-readable summary of key findings

    # Latency analysis
    latency: LatencyStats | None

    # Bottlenecks (sorted by percentage_of_total descending)
    bottlenecks: list[BottleneckInfo]

    # Errors (if any)
    errors: list[ErrorInfo]

    # Cost summary
    total_cost: float | None
    cost_by_model: dict[str, float] | None


@dataclass
class TraceAnalyzeResult:
    """Result of trace analysis (ISC row 16).

    Contains the analysis or error information.
    """

    ok: bool
    code: str
    message: str
    analysis: TraceAnalysis | None = None


# Error code for no timing data
NO_TIMING_DATA = "NO_TIMING_DATA"
