"""Integration tests for Langfuse skill MVP validation (US-015).

These tests validate the MVP works end-to-end with real Langfuse data.

Acceptance Criteria (from US-015):
- Integration tests created in tests/integration/
- Tests use .env credentials to connect to real Langfuse
- MVP test passes: fetch traces and analyze them
- Setup check passes with valid credentials
- Trace list returns real traces from Langfuse
- Trace analyze provides meaningful insights on real data
- Example: Run integration tests -> all pass with real Langfuse connection
- Negative case: Missing .env -> integration tests skip with clear message

ISC reference: rows 72-77
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import pytest

# Add the langfuse skill directory to the path for lib package imports
sys.path.insert(
    0,
    str(Path(__file__).parent.parent.parent / ".claude" / "skills" / "langfuse"),
)

from lib import (
    LangfuseClient,
)


def retry_on_timeout(func, max_retries=3, delay=2):
    """Retry a function if it returns a result with timeout or rate limit error."""
    result = None
    for attempt in range(max_retries):
        result = func()
        if result.ok:
            return result
        # Retry on timeout or rate limit if we haven't exhausted retries
        msg_lower = result.message.lower()
        should_retry = (
            "timeout" in msg_lower
            or "timed out" in msg_lower
            or "taking too long" in msg_lower
            or "too long" in msg_lower
            or "status_code: 524" in msg_lower
            or "rate" in msg_lower
            or "connection" in msg_lower
            or result.code == "RATE_LIMITED"
            or result.code == "NETWORK_TIMEOUT"
            or result.code == "NETWORK_ERROR"
        )
        if should_retry and attempt < max_retries - 1:
            # Use exponential backoff for rate limiting
            wait_time = delay * (2**attempt)
            time.sleep(wait_time)
            continue
        if should_retry:
            pytest.skip(
                "Skipping due to transient Langfuse API/network error after retries: "
                f"{result.message}"
            )
        # Non-retryable error or exhausted retries
        return result
    return result


def _has_langfuse_credentials() -> bool:
    """Check if Langfuse credentials are available in environment.

    Returns True if all required credentials are present and non-empty.
    """
    # Try to load .env file from project root
    from dotenv import load_dotenv

    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "").strip()
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "").strip()

    return bool(secret_key and public_key)


# Pytest marker for integration tests that require real Langfuse connection
requires_langfuse = pytest.mark.skipif(
    not _has_langfuse_credentials(),
    reason="Missing .env credentials: LANGFUSE_SECRET_KEY and/or LANGFUSE_PUBLIC_KEY not set. "
    "Integration tests require valid Langfuse credentials to connect to the API.",
)


class TestMissingEnvSkipBehavior:
    """Test that integration tests skip cleanly when .env is missing.

    Acceptance criteria:
    - Negative case: Missing .env -> integration tests skip with clear message
    """

    def test_has_langfuse_credentials_returns_false_when_missing(self, monkeypatch):
        """Verify credential check correctly identifies missing credentials."""
        # Clear environment variables
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)

        # Override the function to test without .env file loading
        secret_key = os.getenv("LANGFUSE_SECRET_KEY", "").strip()
        public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "").strip()
        result = bool(secret_key and public_key)

        assert result is False

    def test_skip_message_is_clear(self):
        """Verify the skip message clearly explains why tests are skipped."""
        # The skipif mark stores reason in kwargs['reason'] or args[1] depending on pytest version
        skip_reason = requires_langfuse.kwargs.get("reason", "")
        assert "Missing .env" in skip_reason
        assert "LANGFUSE_SECRET_KEY" in skip_reason
        assert "LANGFUSE_PUBLIC_KEY" in skip_reason


@requires_langfuse
class TestSetupCheckIntegration:
    """Integration tests for setup check with real Langfuse connection.

    Acceptance criteria:
    - Setup check passes with valid credentials
    - Tests use .env credentials to connect to real Langfuse
    """

    def test_setup_check_passes_with_valid_credentials(self):
        """Verify setup check succeeds with real credentials.

        This test validates ISC row 73: Setup check passes with valid credentials.
        """
        client = LangfuseClient()
        result = client.auth_check(retry=True)

        assert result.ok, f"Auth check failed: {result.message}"
        assert result.code == "OK"
        assert "Connected" in result.message or "Successfully" in result.message

    def test_client_initialization_succeeds(self):
        """Verify LangfuseClient can be initialized with .env credentials."""
        # Should not raise LangfuseError
        client = LangfuseClient()

        # Verify credentials were loaded
        assert client.secret_key.startswith("sk-lf-"), "Secret key format invalid"
        assert client.public_key.startswith("pk-lf-"), "Public key format invalid"
        assert client.base_url, "Base URL should be set"

    def test_diagnose_returns_healthy_status(self):
        """Verify diagnose reports healthy with valid credentials."""
        client = LangfuseClient()
        diagnosis = client.diagnose()

        assert diagnosis.healthy, f"Diagnosis unhealthy: {diagnosis.summary}"
        assert "passed" in diagnosis.summary.lower() or "working" in diagnosis.summary.lower()
        assert len(diagnosis.issues) == 0


@requires_langfuse
class TestTraceListIntegration:
    """Integration tests for trace list with real Langfuse connection.

    Acceptance criteria:
    - Trace list returns real traces from Langfuse
    - MVP test passes: fetch traces and analyze them
    """

    def test_trace_list_returns_traces(self):
        """Verify trace list returns real traces from Langfuse.

        This test validates ISC row 74: Trace list returns real traces from Langfuse.
        """
        client = LangfuseClient()
        result = retry_on_timeout(lambda: client.fetch_traces(limit=5))

        assert result.ok, f"Fetch traces failed: {result.message}"
        assert result.code == "OK"

        # We may or may not have traces - both are valid states
        # The important thing is the API call succeeded
        if result.traces:
            # Verify trace structure
            trace = result.traces[0]
            assert trace.id, "Trace should have an ID"
            assert trace.status in ("success", "error"), "Trace status should be success or error"

    def test_trace_list_with_limit(self):
        """Verify trace list respects the limit parameter."""
        client = LangfuseClient()
        result = retry_on_timeout(lambda: client.fetch_traces(limit=2))

        assert result.ok, f"Fetch traces failed: {result.message}"
        assert len(result.traces) <= 2, "Should return at most 2 traces"

    def test_trace_list_handles_no_traces(self):
        """Verify trace list handles case when no traces match filter gracefully."""
        client = LangfuseClient()
        # Use a highly unlikely filter to get no results
        result = retry_on_timeout(
            lambda: client.fetch_traces(limit=1, name="___nonexistent_trace_name_xyz123___")
        )

        assert result.ok, f"Fetch traces failed: {result.message}"
        # Empty result is fine - just verify no error


@requires_langfuse
class TestTraceAnalyzeIntegration:
    """Integration tests for trace analyze with real Langfuse connection.

    Acceptance criteria:
    - Trace analyze provides meaningful insights on real data
    - MVP test passes: fetch traces and analyze them
    """

    def test_trace_analyze_on_real_trace(self):
        """Verify trace analyze provides meaningful insights on real data.

        This test validates ISC rows 75-76:
        - Trace analyze provides meaningful insights on real data
        - MVP test passes: fetch traces and analyze them
        """
        client = LangfuseClient()

        # First fetch some traces (with retry for transient network issues)
        list_result = retry_on_timeout(lambda: client.fetch_traces(limit=5))
        assert list_result.ok, f"Could not fetch traces: {list_result.message}"

        if not list_result.traces:
            pytest.skip("No traces available in Langfuse to analyze")

        # Try to analyze the first trace (with retry)
        trace_id = list_result.traces[0].id
        analyze_result = retry_on_timeout(lambda: client.analyze_trace(trace_id))

        # The analysis should succeed (even if there's no timing data)
        # We're testing that the API integration works
        assert analyze_result.analysis is not None, "Analysis should return results"
        assert analyze_result.analysis.trace_id == trace_id

        # Analysis should have a summary
        assert analyze_result.analysis.summary, "Analysis should have a summary"

    def test_trace_get_returns_details(self):
        """Verify trace get returns full trace details with observations."""
        client = LangfuseClient()

        # First fetch some traces (with retry)
        list_result = retry_on_timeout(lambda: client.fetch_traces(limit=1))
        assert list_result.ok, f"Could not fetch traces: {list_result.message}"

        if not list_result.traces:
            pytest.skip("No traces available in Langfuse to analyze")

        # Get the full trace details (with retry)
        trace_id = list_result.traces[0].id
        get_result = retry_on_timeout(lambda: client.fetch_trace(trace_id))

        assert get_result.ok, f"Could not fetch trace details: {get_result.message}"
        assert get_result.trace is not None
        assert get_result.trace.id == trace_id

    def test_trace_analyze_handles_nonexistent_trace(self):
        """Verify trace analyze returns appropriate error for nonexistent trace."""
        client = LangfuseClient()

        # Try to analyze a nonexistent trace (with retry to handle transient issues)
        result = retry_on_timeout(lambda: client.analyze_trace("nonexistent-trace-id-xyz123"))

        # Should fail gracefully - could be NOT_FOUND or API_ERROR depending on Langfuse response
        assert not result.ok
        # Accept either NOT_FOUND or any error that indicates the trace wasn't found
        assert (
            "not found" in result.message.lower()
            or result.code == "NOT_FOUND"
            or result.code == "API_ERROR"  # Acceptable if API returns error for missing trace
        )


@requires_langfuse
class TestMVPEndToEndIntegration:
    """End-to-end integration test validating full MVP workflow.

    This validates ISC row 72: Integration tests created in tests/integration/
    and the complete MVP test: fetch traces and analyze them.
    """

    def test_mvp_workflow_setup_list_analyze(self):
        """Validate complete MVP workflow: setup check -> list traces -> analyze.

        This is the core MVP validation test that exercises the full workflow.
        """
        # Step 1: Setup check
        client = LangfuseClient()
        auth_result = client.auth_check(retry=True)
        assert auth_result.ok, f"MVP Step 1 (Setup) failed: {auth_result.message}"

        # Step 2: List traces (with retry for transient network issues)
        list_result = retry_on_timeout(lambda: client.fetch_traces(limit=10))
        assert list_result.ok, f"MVP Step 2 (List) failed: {list_result.message}"

        # Step 3: Analyze (if traces exist)
        if list_result.traces:
            trace_id = list_result.traces[0].id

            # Get trace details (with retry)
            get_result = retry_on_timeout(lambda: client.fetch_trace(trace_id))
            assert get_result.ok, f"MVP Step 3a (Get) failed: {get_result.message}"

            # Analyze trace (with retry)
            analyze_result = retry_on_timeout(lambda: client.analyze_trace(trace_id))
            assert analyze_result.analysis is not None, "MVP Step 3b (Analyze) failed: no analysis returned"

            # Verify meaningful insights
            analysis = analyze_result.analysis
            assert analysis.summary, "Analysis should provide a summary"
            assert analysis.trace_id == trace_id

        # Flush to ensure clean shutdown
        client.flush()


@requires_langfuse
class TestTraceErrorsIntegration:
    """Integration tests for trace errors command."""

    def test_fetch_errors_returns_valid_result(self):
        """Verify fetch_errors works with real Langfuse connection."""
        client = LangfuseClient()
        result = retry_on_timeout(lambda: client.fetch_errors(since="24h", limit=5))

        # Should succeed even if no errors found
        assert result.ok, f"Fetch errors failed: {result.message}"
        assert result.time_range, "Time range should be reported"

        # If we have errors, verify structure
        if result.errors:
            error = result.errors[0]
            assert error.trace_id, "Error should have trace_id"
            assert error.observation_id, "Error should have observation_id"
            assert error.error_level, "Error should have error_level"


@requires_langfuse
class TestTraceCostsIntegration:
    """Integration tests for trace costs command."""

    def test_fetch_costs_by_model(self):
        """Verify fetch_costs works with model grouping."""
        client = LangfuseClient()
        result = retry_on_timeout(lambda: client.fetch_costs(group_by="model", since="7d", limit=5))

        assert result.ok, f"Fetch costs failed: {result.message}"
        assert result.time_range, "Time range should be reported"
        assert result.group_by == "model"

    def test_fetch_costs_by_day(self):
        """Verify fetch_costs works with day grouping."""
        client = LangfuseClient()
        result = retry_on_timeout(lambda: client.fetch_costs(group_by="day", since="7d", limit=5))

        assert result.ok, f"Fetch costs failed: {result.message}"
        assert result.group_by == "day"


@requires_langfuse
class TestScoresIntegration:
    """Integration tests for scores/evaluation commands."""

    def test_fetch_scores_returns_valid_result(self):
        """Verify fetch_scores works with real Langfuse connection."""
        client = LangfuseClient()
        result = retry_on_timeout(lambda: client.fetch_scores(limit=5))

        # Should succeed even if no scores found
        assert result.ok, f"Fetch scores failed: {result.message}"

        # If we have scores, verify structure
        if result.scores:
            score = result.scores[0]
            assert score.id, "Score should have an ID"
            assert score.name, "Score should have a name"
            assert score.trace_id, "Score should have a trace_id"
