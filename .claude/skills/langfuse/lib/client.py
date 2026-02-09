"""Langfuse client singleton and authentication utilities.

This module provides:
- get_langfuse() - Client singleton with configurable timeout
- auth_check() - Authentication verification
- flush() - Flush pending events
- LangfuseClient - Backward-compatible wrapper class
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from langfuse import Langfuse

from .models import (
    AUTH_INVALID,
    AUTH_MISSING,
    ERROR_MESSAGES,
    MAX_RETRIES,
    NETWORK_ERROR,
    NETWORK_TIMEOUT,
    RATE_LIMITED,
    AuthResult,
    DiagnosisIssue,
    DiagnosisResult,
    LangfuseError,
    Result,
)

if TYPE_CHECKING:
    from typing import Any

# Default timeout for API calls (seconds)
# The SDK default is 5s which causes intermittent timeouts on Langfuse Cloud
DEFAULT_TIMEOUT = 30

_langfuse_instance: Langfuse | None = None


def get_langfuse() -> Langfuse:
    """Get the Langfuse client singleton with 30s timeout.

    Uses environment variables:
    - LANGFUSE_SECRET_KEY
    - LANGFUSE_PUBLIC_KEY
    - LANGFUSE_BASE_URL (defaults to EU cloud)
    - LANGFUSE_TIMEOUT (override default 30s timeout)

    Returns:
        Initialized Langfuse client.
    """
    global _langfuse_instance
    if _langfuse_instance is None:
        timeout = int(os.getenv("LANGFUSE_TIMEOUT", str(DEFAULT_TIMEOUT)))
        _langfuse_instance = Langfuse(timeout=timeout)
    return _langfuse_instance


def auth_check() -> Result:
    """Verify authentication with Langfuse.

    Returns:
        Result with ok=True if authenticated, ok=False with error details otherwise.
    """
    try:
        langfuse = get_langfuse()
        if langfuse.auth_check():
            return Result(ok=True, code="OK", message="Successfully connected to Langfuse")
        return Result(ok=False, code="AUTH_INVALID", message="Authentication failed")
    except Exception as e:
        return Result(ok=False, code="AUTH_ERROR", message=str(e))


def flush() -> None:
    """Flush pending events to Langfuse.

    Must be called before exit in short-lived applications (scripts, CLI tools,
    serverless functions) to ensure all events are transmitted.
    """
    get_langfuse().flush()


def _classify_error(e: Exception) -> str:
    """Classify an exception into an error code."""
    error_str = str(e).lower()
    if "401" in error_str or "unauthorized" in error_str:
        return AUTH_INVALID
    if "429" in error_str or "rate" in error_str:
        return RATE_LIMITED
    if "404" in error_str or "not found" in error_str:
        return "NOT_FOUND"
    return "API_ERROR"


class LangfuseClient:
    """Backward-compatible wrapper that delegates to module-level functions.

    This class provides the same interface as the previous LangfuseClient
    but internally uses the new SDK v3 patterns via module functions.

    For new code, prefer using the module-level functions directly:
    - get_langfuse() -> Langfuse client singleton
    - auth_check() -> Result
    - fetch_traces(...) -> TraceListResult
    - etc.
    """

    def __init__(self, env_path: str | None = None) -> None:
        """Initialize client, loading auth from .env.

        Args:
            env_path: Optional path to .env file. Defaults to auto-discovery.

        Raises:
            LangfuseError: If required credentials are missing.
        """
        if env_path:
            load_dotenv(env_path)
        else:
            load_dotenv()

        # Validate credentials
        self._secret_key = os.getenv("LANGFUSE_SECRET_KEY", "").strip()
        self._public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "").strip()
        self._base_url = os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")

        if not self._secret_key or not self._public_key:
            missing = []
            if not self._secret_key:
                missing.append("LANGFUSE_SECRET_KEY")
            if not self._public_key:
                missing.append("LANGFUSE_PUBLIC_KEY")
            raise LangfuseError(
                code=AUTH_MISSING,
                message=f"Missing required credentials: {', '.join(missing)}. {ERROR_MESSAGES[AUTH_MISSING]}",
            )

        self._langfuse: Langfuse | None = None

    @property
    def langfuse(self) -> Langfuse:
        """Get the underlying Langfuse SDK client."""
        if self._langfuse is None:
            self._langfuse = get_langfuse()
        return self._langfuse

    @property
    def secret_key(self) -> str:
        """Get the configured secret key."""
        return self._secret_key

    @property
    def public_key(self) -> str:
        """Get the configured public key."""
        return self._public_key

    @property
    def base_url(self) -> str:
        """Get the configured base URL."""
        return self._base_url

    def flush(self) -> None:
        """Flush pending events to Langfuse."""
        if self._langfuse is not None:
            self._langfuse.flush()

    def auth_check(self, retry: bool = True) -> AuthResult:
        """Verify authentication and connection to Langfuse.

        Args:
            retry: If True, retry on network errors (default: True).

        Returns:
            AuthResult with code 'OK' on success, or error code on failure.
        """
        max_attempts = MAX_RETRIES if retry else 1
        last_error: Exception | None = None

        for attempt in range(max_attempts):
            try:
                result = self.langfuse.auth_check()
                if result is True or result is None:
                    return AuthResult(code="OK", message="Successfully connected to Langfuse")
                return AuthResult(code=AUTH_INVALID, message="Authentication failed")
            except Exception as e:
                last_error = e
                error_str = str(e).lower()

                # Don't retry on auth errors
                if "401" in error_str or "unauthorized" in error_str:
                    return AuthResult(code=AUTH_INVALID, message=ERROR_MESSAGES[AUTH_INVALID])
                if "429" in error_str or "rate" in error_str:
                    return AuthResult(code=RATE_LIMITED, message=ERROR_MESSAGES[RATE_LIMITED])

                # Network errors - retry if enabled
                if any(term in error_str for term in ["timeout", "connection", "network"]):
                    if attempt < max_attempts - 1:
                        continue
                    return AuthResult(code=NETWORK_TIMEOUT, message=ERROR_MESSAGES[NETWORK_TIMEOUT])

                # Unknown errors - retry if enabled
                if attempt < max_attempts - 1:
                    continue
                return AuthResult(code=NETWORK_ERROR, message=str(e))

        return AuthResult(
            code=NETWORK_TIMEOUT, message=str(last_error) if last_error else "Connection failed"
        )

    def diagnose(self) -> DiagnosisResult:
        """Diagnose common auth and connection issues."""
        issues: list[DiagnosisIssue] = []
        next_steps: list[str] = []

        # Check key formats
        if self._secret_key and not self._secret_key.startswith("sk-lf-"):
            issues.append(
                DiagnosisIssue(
                    code="INVALID_SECRET_KEY_FORMAT",
                    severity="error",
                    message="Secret key should start with 'sk-lf-'",
                    detail=f"Your key starts with '{self._secret_key[:8]}...' instead",
                )
            )
            next_steps.append("Get a new secret key from Langfuse dashboard: Settings > API Keys")

        if self._public_key and not self._public_key.startswith("pk-lf-"):
            issues.append(
                DiagnosisIssue(
                    code="INVALID_PUBLIC_KEY_FORMAT",
                    severity="error",
                    message="Public key should start with 'pk-lf-'",
                    detail=f"Your key starts with '{self._public_key[:8]}...' instead",
                )
            )
            next_steps.append("Get a new public key from Langfuse dashboard: Settings > API Keys")

        # Test connection
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
            if auth_result.code == AUTH_INVALID:
                next_steps.append("Verify your API keys are correct in .env")

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
            next_steps=list(dict.fromkeys(next_steps)),
        )

    # Method stubs for backward compatibility - delegate to module functions with self.langfuse
    def fetch_traces(
        self,
        limit: int = 10,
        name: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        page: int | None = None,
        cursor: str | None = None,
    ) -> Any:
        """Fetch recent traces with optional filters."""
        from .traces import fetch_traces as _fetch_traces

        return _fetch_traces(
            limit=limit,
            name=name,
            user_id=user_id,
            session_id=session_id,
            page=page,
            cursor=cursor,
            langfuse=self.langfuse,
        )

    def fetch_trace(
        self,
        trace_id: str,
        include_observations: bool = True,
        max_observations: int | None = None,
    ) -> Any:
        """Fetch a single trace with all observations."""
        from .traces import fetch_trace as _fetch_trace

        return _fetch_trace(
            trace_id,
            include_observations=include_observations,
            max_observations=max_observations,
            langfuse=self.langfuse,
        )

    def analyze_trace(self, trace_id: str) -> Any:
        """Analyze a trace for latency bottlenecks and issues."""
        from .traces import analyze_trace as _analyze_trace

        return _analyze_trace(trace_id, langfuse=self.langfuse)

    def fetch_errors(self, since: str = "24h", limit: int = 20) -> Any:
        """Find traces with errors in observations."""
        from .errors import fetch_errors as _fetch_errors

        return _fetch_errors(since=since, limit=limit, langfuse=self.langfuse)

    def fetch_costs(
        self, group_by: str = "model", since: str = "7d", limit: int = 20
    ) -> Any:
        """Get cost breakdown by model, trace, or day."""
        from .costs import fetch_costs as _fetch_costs

        return _fetch_costs(group_by=group_by, since=since, limit=limit, langfuse=self.langfuse)

    def create_score(
        self,
        trace_id: str,
        name: str,
        value: float | str,
        data_type: str = "numeric",
        comment: str | None = None,
        observation_id: str | None = None,
    ) -> Any:
        """Create a score on a trace or observation."""
        from .scores import create_score as _create_score

        return _create_score(
            trace_id=trace_id,
            name=name,
            value=value,
            data_type=data_type,
            comment=comment,
            observation_id=observation_id,
            langfuse=self.langfuse,
        )

    def fetch_scores(
        self,
        trace_id: str | None = None,
        name: str | None = None,
        limit: int = 20,
    ) -> Any:
        """Fetch scores with optional filters."""
        from .scores import fetch_scores as _fetch_scores

        return _fetch_scores(trace_id=trace_id, name=name, limit=limit, langfuse=self.langfuse)
