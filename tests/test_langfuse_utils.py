"""Tests for langfuse_utils module.

Tests verify acceptance criteria from US-002:
- lib/langfuse_utils.py created with LangfuseClient wrapper class
- Auth loading from .env (LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_BASE_URL)
- Error code constants defined (AUTH_MISSING, AUTH_INVALID, NETWORK_ERROR, RATE_LIMITED)
- Human-readable error messages for each code
- flush() helper for short-lived operations
- Example: Missing .env -> returns AUTH_MISSING code with guidance message
- Example: Invalid keys -> returns AUTH_INVALID with 'Check your API keys' message
- Negative case: Empty LANGFUSE_SECRET_KEY -> AUTH_MISSING, not silent failure

ISC Reference: rows 53-59
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add the lib directory to the path for imports
sys.path.insert(
    0,
    str(Path(__file__).parent.parent / ".claude" / "skills" / "langfuse" / "lib"),
)

from langfuse_utils import (
    API_ERROR,
    AUTH_EXPIRED,
    AUTH_INVALID,
    AUTH_MISSING,
    ERROR_MESSAGES,
    LANGFUSE_REGIONS,
    MAX_RETRIES,
    NETWORK_ERROR,
    NETWORK_TIMEOUT,
    NOT_FOUND,
    RATE_LIMITED,
    REGION_MISMATCH,
    AuthResult,
    DiagnosisIssue,
    DiagnosisResult,
    LangfuseClient,
    LangfuseError,
    ObservationInfo,
    TraceDetail,
    TraceGetResult,
    TraceInfo,
    TraceListResult,
)


class TestErrorCodeConstants:
    """Tests for error code constants (ISC row 58)."""

    def test_auth_missing_constant_exists(self):
        """AUTH_MISSING constant should be defined."""
        assert AUTH_MISSING == "AUTH_MISSING"

    def test_auth_invalid_constant_exists(self):
        """AUTH_INVALID constant should be defined."""
        assert AUTH_INVALID == "AUTH_INVALID"

    def test_auth_expired_constant_exists(self):
        """AUTH_EXPIRED constant should be defined."""
        assert AUTH_EXPIRED == "AUTH_EXPIRED"

    def test_network_error_constant_exists(self):
        """NETWORK_ERROR constant should be defined."""
        assert NETWORK_ERROR == "NETWORK_ERROR"

    def test_network_timeout_constant_exists(self):
        """NETWORK_TIMEOUT constant should be defined."""
        assert NETWORK_TIMEOUT == "NETWORK_TIMEOUT"

    def test_rate_limited_constant_exists(self):
        """RATE_LIMITED constant should be defined."""
        assert RATE_LIMITED == "RATE_LIMITED"

    def test_region_mismatch_constant_exists(self):
        """REGION_MISMATCH constant should be defined."""
        assert REGION_MISMATCH == "REGION_MISMATCH"

    def test_not_found_constant_exists(self):
        """NOT_FOUND constant should be defined."""
        assert NOT_FOUND == "NOT_FOUND"

    def test_api_error_constant_exists(self):
        """API_ERROR constant should be defined."""
        assert API_ERROR == "API_ERROR"


class TestRegionConstants:
    """Tests for region constants (ISC row 38)."""

    def test_eu_region_exists(self):
        """EU region should be defined."""
        assert "EU" in LANGFUSE_REGIONS
        assert "cloud.langfuse.com" in LANGFUSE_REGIONS["EU"]

    def test_us_region_exists(self):
        """US region should be defined."""
        assert "US" in LANGFUSE_REGIONS
        assert "us.cloud.langfuse.com" in LANGFUSE_REGIONS["US"]

    def test_max_retries_defined(self):
        """MAX_RETRIES constant should be defined."""
        assert MAX_RETRIES == 3


class TestErrorMessages:
    """Tests for human-readable error messages (ISC row 59)."""

    def test_all_error_codes_have_messages(self):
        """Every error code should have a human-readable message."""
        error_codes = [
            AUTH_MISSING,
            AUTH_INVALID,
            AUTH_EXPIRED,
            NETWORK_ERROR,
            NETWORK_TIMEOUT,
            RATE_LIMITED,
            REGION_MISMATCH,
            NOT_FOUND,
            API_ERROR,
        ]
        for code in error_codes:
            assert code in ERROR_MESSAGES
            assert len(ERROR_MESSAGES[code]) > 0

    def test_auth_missing_message_has_guidance(self):
        """AUTH_MISSING message should provide setup guidance."""
        msg = ERROR_MESSAGES[AUTH_MISSING]
        assert "LANGFUSE_SECRET_KEY" in msg
        assert "LANGFUSE_PUBLIC_KEY" in msg
        assert ".env" in msg

    def test_auth_invalid_message_mentions_api_keys(self):
        """AUTH_INVALID message should mention checking API keys."""
        msg = ERROR_MESSAGES[AUTH_INVALID]
        # Acceptance criteria: 'Check your API keys' message
        assert "api keys" in msg.lower() or "keys" in msg.lower()

    def test_network_error_message_has_url_info(self):
        """NETWORK_ERROR message should provide URL guidance."""
        msg = ERROR_MESSAGES[NETWORK_ERROR]
        assert "cloud.langfuse.com" in msg

    def test_rate_limited_message_mentions_retry(self):
        """RATE_LIMITED message should mention retry behavior."""
        msg = ERROR_MESSAGES[RATE_LIMITED]
        assert "retry" in msg.lower() or "wait" in msg.lower()


class TestLangfuseError:
    """Tests for LangfuseError exception class."""

    def test_langfuse_error_has_code_and_message(self):
        """LangfuseError should have code and message attributes."""
        error = LangfuseError(code=AUTH_MISSING, message="Test message")
        assert error.code == AUTH_MISSING
        assert error.message == "Test message"

    def test_langfuse_error_str_includes_code(self):
        """LangfuseError string representation should include code."""
        error = LangfuseError(code=AUTH_MISSING, message="Test message")
        assert AUTH_MISSING in str(error)
        assert "Test message" in str(error)


class TestAuthResult:
    """Tests for AuthResult dataclass."""

    def test_auth_result_ok_when_code_is_ok(self):
        """AuthResult.ok should be True when code is 'OK'."""
        result = AuthResult(code="OK", message="Success")
        assert result.ok is True

    def test_auth_result_not_ok_when_code_is_error(self):
        """AuthResult.ok should be False when code is an error."""
        result = AuthResult(code=AUTH_MISSING, message="Error")
        assert result.ok is False


class TestLangfuseClientValidation:
    """Tests for LangfuseClient auth validation."""

    @pytest.fixture(autouse=True)
    def clean_env(self, monkeypatch):
        """Clean environment and prevent dotenv from loading the project .env file."""
        # Patch load_dotenv to do nothing (prevents reading from project .env)
        monkeypatch.setattr("langfuse_utils.load_dotenv", lambda *args, **kwargs: None)
        # Remove all Langfuse-related env vars completely
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_BASE_URL", raising=False)

    def test_missing_secret_key_raises_auth_missing(self, monkeypatch):
        """Missing LANGFUSE_SECRET_KEY should raise AUTH_MISSING error."""
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
        # Secret key is missing (deleted by clean_env)

        with pytest.raises(LangfuseError) as exc_info:
            LangfuseClient()

        assert exc_info.value.code == AUTH_MISSING
        assert "LANGFUSE_SECRET_KEY" in exc_info.value.message

    def test_missing_public_key_raises_auth_missing(self, monkeypatch):
        """Missing LANGFUSE_PUBLIC_KEY should raise AUTH_MISSING error."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        # Public key is missing (deleted by clean_env)

        with pytest.raises(LangfuseError) as exc_info:
            LangfuseClient()

        assert exc_info.value.code == AUTH_MISSING
        assert "LANGFUSE_PUBLIC_KEY" in exc_info.value.message

    def test_empty_secret_key_raises_auth_missing(self, monkeypatch):
        """Empty LANGFUSE_SECRET_KEY should raise AUTH_MISSING, not silent failure.

        This is a critical acceptance criterion from US-002:
        Negative case: Empty LANGFUSE_SECRET_KEY -> AUTH_MISSING, not silent failure
        """
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "")  # Empty
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

        with pytest.raises(LangfuseError) as exc_info:
            LangfuseClient()

        assert exc_info.value.code == AUTH_MISSING

    def test_whitespace_only_secret_key_raises_auth_missing(self, monkeypatch):
        """Whitespace-only LANGFUSE_SECRET_KEY should raise AUTH_MISSING."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "   ")  # Whitespace only
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

        with pytest.raises(LangfuseError) as exc_info:
            LangfuseClient()

        assert exc_info.value.code == AUTH_MISSING

    def test_valid_credentials_no_exception(self, monkeypatch):
        """Valid credentials should not raise an exception."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

        # Should not raise
        client = LangfuseClient()
        assert client.secret_key == "sk-lf-test"
        assert client.public_key == "pk-lf-test"


class TestLangfuseClientProperties:
    """Tests for LangfuseClient properties."""

    @pytest.fixture(autouse=True)
    def setup_env(self, monkeypatch):
        """Set up valid environment using monkeypatch."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test-secret")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test-public")
        monkeypatch.setenv("LANGFUSE_BASE_URL", "https://custom.langfuse.com")

    def test_secret_key_property(self):
        """secret_key property should return the configured secret key."""
        client = LangfuseClient()
        assert client.secret_key == "sk-lf-test-secret"

    def test_public_key_property(self):
        """public_key property should return the configured public key."""
        client = LangfuseClient()
        assert client.public_key == "pk-lf-test-public"

    def test_base_url_property_custom(self):
        """base_url property should return custom URL when set."""
        client = LangfuseClient()
        assert client.base_url == "https://custom.langfuse.com"

    def test_base_url_property_default(self, monkeypatch):
        """base_url property should default to EU cloud."""
        monkeypatch.delenv("LANGFUSE_BASE_URL", raising=False)
        client = LangfuseClient()
        assert client.base_url == "https://cloud.langfuse.com"


class TestLangfuseClientFlush:
    """Tests for LangfuseClient flush() helper (ISC row 57)."""

    @pytest.fixture(autouse=True)
    def setup_env(self, monkeypatch):
        """Set up valid environment using monkeypatch."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

    def test_flush_exists(self):
        """flush() method should exist on LangfuseClient."""
        client = LangfuseClient()
        assert hasattr(client, "flush")
        assert callable(client.flush)

    def test_flush_without_langfuse_initialized(self):
        """flush() should not raise when langfuse client not yet initialized."""
        client = LangfuseClient()
        # Should not raise - langfuse property not accessed yet
        client.flush()

    def test_flush_calls_langfuse_flush(self):
        """flush() should call underlying Langfuse client's flush()."""
        mock_client = MagicMock()

        client = LangfuseClient()
        # Manually set the internal _langfuse to our mock
        client._langfuse = mock_client
        # Now flush
        client.flush()

        mock_client.flush.assert_called_once()


class TestLangfuseClientAuthCheck:
    """Tests for LangfuseClient auth_check() method."""

    @pytest.fixture(autouse=True)
    def setup_env(self, monkeypatch):
        """Set up valid environment using monkeypatch."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

    def test_auth_check_success(self):
        """auth_check() should return OK on successful auth."""
        mock_client = MagicMock()
        mock_client.auth_check.return_value = None  # Success

        client = LangfuseClient()
        # Inject mock client
        client._langfuse = mock_client
        result = client.auth_check()

        assert result.code == "OK"
        assert result.ok is True

    def test_auth_check_invalid_returns_auth_invalid(self):
        """auth_check() should return AUTH_INVALID for 401 errors."""
        mock_client = MagicMock()
        mock_client.auth_check.side_effect = Exception("401 Unauthorized")

        client = LangfuseClient()
        client._langfuse = mock_client
        result = client.auth_check()

        assert result.code == AUTH_INVALID
        assert result.ok is False

    def test_auth_check_rate_limited(self):
        """auth_check() should return RATE_LIMITED for 429 errors."""
        mock_client = MagicMock()
        mock_client.auth_check.side_effect = Exception("429 Rate limit exceeded")

        client = LangfuseClient()
        client._langfuse = mock_client
        result = client.auth_check()

        assert result.code == RATE_LIMITED
        assert result.ok is False

    def test_auth_check_network_error(self):
        """auth_check() should return NETWORK_ERROR for connection issues."""
        mock_client = MagicMock()
        mock_client.auth_check.side_effect = Exception("Connection refused")

        client = LangfuseClient()
        client._langfuse = mock_client
        result = client.auth_check(retry=False)  # Don't retry for unit tests

        # With no retry, network errors return NETWORK_TIMEOUT after exhausting retries
        assert result.code in (NETWORK_ERROR, NETWORK_TIMEOUT)
        assert result.ok is False

    def test_auth_check_retries_on_network_error(self):
        """auth_check() should retry on network errors with retry=True (ISC row 63)."""
        mock_client = MagicMock()
        # Fail first call, succeed on second
        mock_client.auth_check.side_effect = [
            Exception("Connection timeout"),
            None,  # Success
        ]

        client = LangfuseClient()
        client._langfuse = mock_client
        result = client.auth_check(retry=True)

        assert result.code == "OK"
        assert result.ok is True
        # Should have been called twice
        assert mock_client.auth_check.call_count == 2

    def test_auth_check_no_retry_on_auth_error(self):
        """auth_check() should NOT retry on auth errors (401)."""
        mock_client = MagicMock()
        mock_client.auth_check.side_effect = Exception("401 Unauthorized")

        client = LangfuseClient()
        client._langfuse = mock_client
        result = client.auth_check(retry=True)

        assert result.code == AUTH_INVALID
        # Should only be called once - no retry
        assert mock_client.auth_check.call_count == 1


class TestLangfuseClientDiagnose:
    """Tests for LangfuseClient diagnose() method (ISC rows 36-40)."""

    @pytest.fixture(autouse=True)
    def setup_env(self, monkeypatch):
        """Set up valid environment using monkeypatch."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
        monkeypatch.setenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")

    def test_diagnose_returns_healthy_on_success(self):
        """diagnose() should return healthy when all checks pass."""
        mock_client = MagicMock()
        mock_client.auth_check.return_value = None  # Success

        client = LangfuseClient()
        client._langfuse = mock_client
        result = client.diagnose()

        assert result.healthy is True
        assert len(result.issues) == 0

    def test_diagnose_detects_invalid_secret_key_format(self, monkeypatch):
        """diagnose() should detect invalid secret key format."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "invalid-key-format")

        mock_client = MagicMock()
        mock_client.auth_check.return_value = None  # Auth check itself passes

        client = LangfuseClient()
        client._langfuse = mock_client
        result = client.diagnose()

        assert result.healthy is False
        issue_codes = [issue.code for issue in result.issues]
        assert "INVALID_SECRET_KEY_FORMAT" in issue_codes

    def test_diagnose_detects_invalid_public_key_format(self, monkeypatch):
        """diagnose() should detect invalid public key format."""
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "invalid-key-format")

        mock_client = MagicMock()
        mock_client.auth_check.return_value = None

        client = LangfuseClient()
        client._langfuse = mock_client
        result = client.diagnose()

        assert result.healthy is False
        issue_codes = [issue.code for issue in result.issues]
        assert "INVALID_PUBLIC_KEY_FORMAT" in issue_codes

    def test_diagnose_includes_next_steps(self, monkeypatch):
        """diagnose() should provide next steps when issues found."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "invalid-key")

        mock_client = MagicMock()
        mock_client.auth_check.return_value = None

        client = LangfuseClient()
        client._langfuse = mock_client
        result = client.diagnose()

        assert result.healthy is False
        assert len(result.next_steps) > 0


class TestDiagnosisDataclasses:
    """Tests for diagnosis dataclasses."""

    def test_diagnosis_issue_has_required_fields(self):
        """DiagnosisIssue should have all required fields."""
        issue = DiagnosisIssue(
            code="TEST_CODE",
            severity="error",
            message="Test message",
            detail="Test detail",
        )
        assert issue.code == "TEST_CODE"
        assert issue.severity == "error"
        assert issue.message == "Test message"
        assert issue.detail == "Test detail"

    def test_diagnosis_result_has_required_fields(self):
        """DiagnosisResult should have all required fields."""
        result = DiagnosisResult(
            healthy=True, summary="All good", issues=[], next_steps=[]
        )
        assert result.healthy is True
        assert result.summary == "All good"
        assert result.issues == []
        assert result.next_steps == []


class TestModuleFileExists:
    """Tests for module file existence (ISC row 53)."""

    def test_langfuse_utils_file_exists(self):
        """lib/langfuse_utils.py should exist."""
        utils_path = Path(".claude/skills/langfuse/lib/langfuse_utils.py")
        assert utils_path.exists(), "langfuse_utils.py should exist in lib/"

    def test_lib_init_exists(self):
        """lib/__init__.py should exist for proper imports."""
        init_path = Path(".claude/skills/langfuse/lib/__init__.py")
        assert init_path.exists(), "__init__.py should exist in lib/"


class TestTraceInfoDataclass:
    """Tests for TraceInfo dataclass (ISC row 14)."""

    def test_trace_info_required_fields(self):
        """TraceInfo should have required fields: id, name, timestamp, status."""
        trace = TraceInfo(
            id="trace-123",
            name="test-trace",
            timestamp="2026-01-20T10:00:00",
            status="success",
        )
        assert trace.id == "trace-123"
        assert trace.name == "test-trace"
        assert trace.timestamp == "2026-01-20T10:00:00"
        assert trace.status == "success"

    def test_trace_info_optional_fields(self):
        """TraceInfo should have optional fields: user_id, session_id."""
        trace = TraceInfo(
            id="trace-123",
            name="test-trace",
            timestamp="2026-01-20T10:00:00",
            status="success",
            user_id="user-456",
            session_id="session-789",
        )
        assert trace.user_id == "user-456"
        assert trace.session_id == "session-789"

    def test_trace_info_optional_fields_default_none(self):
        """TraceInfo optional fields should default to None."""
        trace = TraceInfo(
            id="trace-123",
            name=None,
            timestamp="2026-01-20T10:00:00",
            status="success",
        )
        assert trace.name is None
        assert trace.user_id is None
        assert trace.session_id is None


class TestTraceListResultDataclass:
    """Tests for TraceListResult dataclass (ISC row 14)."""

    def test_trace_list_result_required_fields(self):
        """TraceListResult should have required fields."""
        result = TraceListResult(
            ok=True,
            code="OK",
            message="Found 1 trace(s)",
            traces=[],
        )
        assert result.ok is True
        assert result.code == "OK"
        assert result.message == "Found 1 trace(s)"
        assert result.traces == []

    def test_trace_list_result_optional_fields(self):
        """TraceListResult should have optional pagination fields."""
        result = TraceListResult(
            ok=True,
            code="OK",
            message="Found traces",
            traces=[],
            has_more=True,
            cursor="next-cursor",
        )
        assert result.has_more is True
        assert result.cursor == "next-cursor"

    def test_trace_list_result_optional_fields_default(self):
        """TraceListResult optional fields should have defaults."""
        result = TraceListResult(
            ok=True,
            code="OK",
            message="Found traces",
            traces=[],
        )
        assert result.has_more is False
        assert result.cursor is None


class TestLangfuseClientFetchTraces:
    """Tests for LangfuseClient fetch_traces() method (ISC row 14)."""

    @pytest.fixture(autouse=True)
    def setup_env(self, monkeypatch):
        """Set up valid environment using monkeypatch."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

    def test_fetch_traces_returns_trace_list_result(self):
        """fetch_traces() should return TraceListResult."""
        mock_langfuse = MagicMock()
        mock_response = MagicMock()
        mock_response.data = []
        mock_response.meta = MagicMock()
        mock_response.meta.cursor = None
        mock_langfuse.api.trace.list.return_value = mock_response

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_traces()

        assert isinstance(result, TraceListResult)

    def test_fetch_traces_success_empty_list(self):
        """fetch_traces() should handle empty trace list."""
        mock_langfuse = MagicMock()
        mock_response = MagicMock()
        mock_response.data = []
        mock_response.meta = None
        mock_langfuse.api.trace.list.return_value = mock_response

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_traces()

        assert result.ok is True
        assert result.code == "OK"
        assert len(result.traces) == 0

    def test_fetch_traces_success_with_traces(self):
        """fetch_traces() should process trace data correctly."""
        mock_langfuse = MagicMock()

        # Create mock trace objects
        mock_trace1 = MagicMock()
        mock_trace1.id = "trace-123"
        mock_trace1.name = "chatbot"
        mock_trace1.timestamp = "2026-01-20T10:00:00"
        mock_trace1.user_id = "user-1"
        mock_trace1.session_id = "sess-1"

        mock_trace2 = MagicMock()
        mock_trace2.id = "trace-456"
        mock_trace2.name = "analyzer"
        mock_trace2.timestamp = "2026-01-20T09:00:00"
        mock_trace2.level = "ERROR"  # Indicates error status
        mock_trace2.user_id = None
        mock_trace2.session_id = None

        mock_response = MagicMock()
        mock_response.data = [mock_trace1, mock_trace2]
        mock_response.meta = None
        mock_langfuse.api.trace.list.return_value = mock_response

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_traces()

        assert result.ok is True
        assert len(result.traces) == 2
        assert result.traces[0].id == "trace-123"
        assert result.traces[0].name == "chatbot"
        assert result.traces[0].status == "success"
        assert result.traces[1].id == "trace-456"
        assert result.traces[1].status == "error"  # Because level was ERROR

    def test_fetch_traces_passes_filters(self):
        """fetch_traces() should pass filter parameters to API."""
        mock_langfuse = MagicMock()
        mock_response = MagicMock()
        mock_response.data = []
        mock_response.meta = None
        mock_langfuse.api.trace.list.return_value = mock_response

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        client.fetch_traces(
            limit=20,
            name="chatbot",
            user_id="user-123",
            session_id="sess-456",
        )

        mock_langfuse.api.trace.list.assert_called_once_with(
            limit=20,
            name="chatbot",
            user_id="user-123",
            session_id="sess-456",
        )

    def test_fetch_traces_handles_pagination(self):
        """fetch_traces() should return pagination info when available."""
        mock_langfuse = MagicMock()
        mock_response = MagicMock()
        mock_response.data = []
        mock_response.meta = MagicMock()
        mock_response.meta.cursor = "next-page-cursor"
        mock_langfuse.api.trace.list.return_value = mock_response

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_traces()

        assert result.has_more is True
        assert result.cursor == "next-page-cursor"

    def test_fetch_traces_handles_auth_error(self):
        """fetch_traces() should handle 401 auth errors."""
        mock_langfuse = MagicMock()
        mock_langfuse.api.trace.list.side_effect = Exception("401 Unauthorized")

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_traces()

        assert result.ok is False
        assert result.code == AUTH_INVALID
        assert len(result.traces) == 0

    def test_fetch_traces_handles_rate_limit(self):
        """fetch_traces() should handle rate limit errors."""
        mock_langfuse = MagicMock()
        mock_langfuse.api.trace.list.side_effect = Exception("429 Rate limit")

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_traces()

        assert result.ok is False
        assert result.code == RATE_LIMITED
        assert len(result.traces) == 0

    def test_fetch_traces_handles_not_found(self):
        """fetch_traces() should handle 404 not found errors."""
        mock_langfuse = MagicMock()
        mock_langfuse.api.trace.list.side_effect = Exception("404 Not Found")

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_traces()

        assert result.ok is False
        assert result.code == NOT_FOUND
        assert len(result.traces) == 0

    def test_fetch_traces_handles_generic_error(self):
        """fetch_traces() should handle generic errors."""
        mock_langfuse = MagicMock()
        mock_langfuse.api.trace.list.side_effect = Exception("Some random error")

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_traces()

        assert result.ok is False
        assert result.code == API_ERROR
        assert "Some random error" in result.message


class TestObservationInfoDataclass:
    """Tests for ObservationInfo dataclass (ISC rows 15, 20)."""

    def test_observation_info_required_fields(self):
        """ObservationInfo should have required fields."""
        obs = ObservationInfo(
            id="obs-123",
            type="GENERATION",
            name="llm-call",
            start_time="2026-01-20T10:00:00",
            end_time="2026-01-20T10:00:01",
            duration_ms=1000.0,
            level=None,
            status_message=None,
            model="gpt-4",
            input="Hello",
            output="Hi there",
        )
        assert obs.id == "obs-123"
        assert obs.type == "GENERATION"
        assert obs.name == "llm-call"
        assert obs.model == "gpt-4"

    def test_observation_info_token_fields(self):
        """ObservationInfo should have optional token fields."""
        obs = ObservationInfo(
            id="obs-123",
            type="GENERATION",
            name="llm-call",
            start_time="2026-01-20T10:00:00",
            end_time=None,
            duration_ms=None,
            level=None,
            status_message=None,
            model="gpt-4",
            input=None,
            output=None,
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
            cost=0.001,
        )
        assert obs.input_tokens == 100
        assert obs.output_tokens == 50
        assert obs.total_tokens == 150
        assert obs.cost == 0.001

    def test_observation_info_parent_field(self):
        """ObservationInfo should have parent_observation_id for hierarchy."""
        obs = ObservationInfo(
            id="obs-child",
            type="SPAN",
            name="child-span",
            start_time="2026-01-20T10:00:00",
            end_time=None,
            duration_ms=None,
            level=None,
            status_message=None,
            model=None,
            input=None,
            output=None,
            parent_observation_id="obs-parent",
        )
        assert obs.parent_observation_id == "obs-parent"


class TestTraceDetailDataclass:
    """Tests for TraceDetail dataclass (ISC rows 15, 20)."""

    def test_trace_detail_required_fields(self):
        """TraceDetail should have required fields."""
        detail = TraceDetail(
            id="trace-123",
            name="my-trace",
            timestamp="2026-01-20T10:00:00",
            session_id="sess-1",
            user_id="user-1",
            input="Hello",
            output="World",
            metadata={"key": "value"},
            tags=["prod"],
            observations=[],
        )
        assert detail.id == "trace-123"
        assert detail.name == "my-trace"
        assert detail.session_id == "sess-1"
        assert detail.user_id == "user-1"
        assert detail.tags == ["prod"]
        assert detail.observations == []

    def test_trace_detail_with_observations(self):
        """TraceDetail should contain observations list."""
        obs = ObservationInfo(
            id="obs-1",
            type="GENERATION",
            name="gen-1",
            start_time="2026-01-20T10:00:00",
            end_time=None,
            duration_ms=None,
            level=None,
            status_message=None,
            model="gpt-4",
            input=None,
            output=None,
        )
        detail = TraceDetail(
            id="trace-123",
            name="my-trace",
            timestamp="2026-01-20T10:00:00",
            session_id=None,
            user_id=None,
            input=None,
            output=None,
            metadata=None,
            tags=None,
            observations=[obs],
        )
        assert len(detail.observations) == 1
        assert detail.observations[0].id == "obs-1"


class TestTraceGetResultDataclass:
    """Tests for TraceGetResult dataclass (ISC row 15)."""

    def test_trace_get_result_success(self):
        """TraceGetResult should represent successful fetch."""
        detail = TraceDetail(
            id="trace-123",
            name="my-trace",
            timestamp="2026-01-20T10:00:00",
            session_id=None,
            user_id=None,
            input=None,
            output=None,
            metadata=None,
            tags=None,
            observations=[],
        )
        result = TraceGetResult(
            ok=True,
            code="OK",
            message="Found trace",
            trace=detail,
        )
        assert result.ok is True
        assert result.code == "OK"
        assert result.trace is not None
        assert result.trace.id == "trace-123"

    def test_trace_get_result_not_found(self):
        """TraceGetResult should represent not found case."""
        result = TraceGetResult(
            ok=False,
            code=NOT_FOUND,
            message="Trace not found: invalid-id",
            trace=None,
        )
        assert result.ok is False
        assert result.code == NOT_FOUND
        assert result.trace is None


class TestLangfuseClientFetchTrace:
    """Tests for LangfuseClient fetch_trace() method (ISC rows 15, 20)."""

    @pytest.fixture(autouse=True)
    def setup_env(self, monkeypatch):
        """Set up valid environment using monkeypatch."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

    def test_fetch_trace_returns_trace_get_result(self):
        """fetch_trace() should return TraceGetResult."""
        mock_langfuse = MagicMock()

        # Mock trace.get response
        mock_trace = MagicMock()
        mock_trace.id = "trace-123"
        mock_trace.name = "test-trace"
        mock_trace.timestamp = "2026-01-20T10:00:00"
        mock_trace.session_id = None
        mock_trace.user_id = None
        mock_trace.input = None
        mock_trace.output = None
        mock_trace.metadata = None
        mock_trace.tags = None
        mock_langfuse.api.trace.get.return_value = mock_trace

        # Mock observations response
        mock_obs_response = MagicMock()
        mock_obs_response.data = []
        mock_obs_response.meta = None
        mock_langfuse.api.observations_v_2.get_many.return_value = mock_obs_response

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_trace("trace-123")

        assert isinstance(result, TraceGetResult)

    def test_fetch_trace_success_basic(self):
        """fetch_trace() should fetch trace with basic info."""
        mock_langfuse = MagicMock()

        mock_trace = MagicMock()
        mock_trace.id = "trace-abc"
        mock_trace.name = "chatbot"
        mock_trace.timestamp = "2026-01-20T10:00:00"
        mock_trace.session_id = "sess-1"
        mock_trace.user_id = "user-1"
        mock_trace.input = "Hello"
        mock_trace.output = "World"
        mock_trace.metadata = {"key": "val"}
        mock_trace.tags = ["prod"]
        mock_langfuse.api.trace.get.return_value = mock_trace

        mock_obs_response = MagicMock()
        mock_obs_response.data = []
        mock_obs_response.meta = None
        mock_langfuse.api.observations_v_2.get_many.return_value = mock_obs_response

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_trace("trace-abc")

        assert result.ok is True
        assert result.trace is not None
        assert result.trace.id == "trace-abc"
        assert result.trace.name == "chatbot"
        assert result.trace.session_id == "sess-1"
        assert result.trace.tags == ["prod"]

    def test_fetch_trace_with_observations(self):
        """fetch_trace() should fetch trace with observations (ISC row 20)."""
        mock_langfuse = MagicMock()

        mock_trace = MagicMock()
        mock_trace.id = "trace-123"
        mock_trace.name = "test"
        mock_trace.timestamp = "2026-01-20T10:00:00"
        mock_trace.session_id = None
        mock_trace.user_id = None
        mock_trace.input = None
        mock_trace.output = None
        mock_trace.metadata = None
        mock_trace.tags = None
        mock_langfuse.api.trace.get.return_value = mock_trace

        # Mock observation
        mock_obs = MagicMock()
        mock_obs.id = "obs-1"
        mock_obs.type = "GENERATION"
        mock_obs.name = "llm-call"
        mock_obs.start_time = "2026-01-20T10:00:01"
        mock_obs.end_time = "2026-01-20T10:00:02"
        mock_obs.level = None
        mock_obs.status_message = None
        mock_obs.model = "gpt-4"
        mock_obs.input = "Hello"
        mock_obs.output = "Hi"
        mock_obs.usage = MagicMock()
        mock_obs.usage.input = 10
        mock_obs.usage.output = 5
        mock_obs.usage.total = 15
        mock_obs.calculated_total_cost = 0.001
        mock_obs.parent_observation_id = None

        mock_obs_response = MagicMock()
        mock_obs_response.data = [mock_obs]
        mock_obs_response.meta = None
        mock_langfuse.api.observations_v_2.get_many.return_value = mock_obs_response

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_trace("trace-123")

        assert result.ok is True
        assert result.trace is not None
        assert len(result.trace.observations) == 1
        assert result.trace.observations[0].id == "obs-1"
        assert result.trace.observations[0].type == "GENERATION"
        assert result.trace.observations[0].model == "gpt-4"
        assert result.trace.observations[0].cost == 0.001

    def test_fetch_trace_not_found(self):
        """fetch_trace() should handle 404 not found (negative case)."""
        mock_langfuse = MagicMock()
        mock_langfuse.api.trace.get.side_effect = Exception("404 Not Found")

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_trace("invalid-trace-id")

        assert result.ok is False
        assert result.code == NOT_FOUND
        assert "Trace not found" in result.message
        assert "invalid-trace-id" in result.message

    def test_fetch_trace_auth_error(self):
        """fetch_trace() should handle auth errors."""
        mock_langfuse = MagicMock()
        mock_langfuse.api.trace.get.side_effect = Exception("401 Unauthorized")

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_trace("trace-123")

        assert result.ok is False
        assert result.code == AUTH_INVALID

    def test_fetch_trace_rate_limit(self):
        """fetch_trace() should handle rate limit errors."""
        mock_langfuse = MagicMock()
        mock_langfuse.api.trace.get.side_effect = Exception("429 Rate limit")

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_trace("trace-123")

        assert result.ok is False
        assert result.code == RATE_LIMITED

    def test_fetch_trace_generic_error(self):
        """fetch_trace() should handle generic errors."""
        mock_langfuse = MagicMock()
        mock_langfuse.api.trace.get.side_effect = Exception("Unknown error")

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_trace("trace-123")

        assert result.ok is False
        assert result.code == API_ERROR
        assert "Unknown error" in result.message

    def test_fetch_trace_observation_hierarchy(self):
        """fetch_trace() should capture parent_observation_id for hierarchy."""
        mock_langfuse = MagicMock()

        mock_trace = MagicMock()
        mock_trace.id = "trace-123"
        mock_trace.name = "test"
        mock_trace.timestamp = "2026-01-20T10:00:00"
        mock_trace.session_id = None
        mock_trace.user_id = None
        mock_trace.input = None
        mock_trace.output = None
        mock_trace.metadata = None
        mock_trace.tags = None
        mock_langfuse.api.trace.get.return_value = mock_trace

        # Root observation
        mock_obs_root = MagicMock()
        mock_obs_root.id = "obs-root"
        mock_obs_root.type = "SPAN"
        mock_obs_root.name = "root-span"
        mock_obs_root.start_time = "2026-01-20T10:00:00"
        mock_obs_root.end_time = None
        mock_obs_root.level = None
        mock_obs_root.status_message = None
        mock_obs_root.model = None
        mock_obs_root.input = None
        mock_obs_root.output = None
        mock_obs_root.usage = None
        mock_obs_root.calculated_total_cost = None
        mock_obs_root.parent_observation_id = None

        # Child observation
        mock_obs_child = MagicMock()
        mock_obs_child.id = "obs-child"
        mock_obs_child.type = "GENERATION"
        mock_obs_child.name = "child-gen"
        mock_obs_child.start_time = "2026-01-20T10:00:01"
        mock_obs_child.end_time = None
        mock_obs_child.level = None
        mock_obs_child.status_message = None
        mock_obs_child.model = "gpt-4"
        mock_obs_child.input = None
        mock_obs_child.output = None
        mock_obs_child.usage = None
        mock_obs_child.calculated_total_cost = None
        mock_obs_child.parent_observation_id = "obs-root"

        mock_obs_response = MagicMock()
        mock_obs_response.data = [mock_obs_root, mock_obs_child]
        mock_obs_response.meta = None
        mock_langfuse.api.observations_v_2.get_many.return_value = mock_obs_response

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.fetch_trace("trace-123")

        assert result.ok is True
        assert len(result.trace.observations) == 2

        # Find child observation and verify parent reference
        child_obs = next(o for o in result.trace.observations if o.id == "obs-child")
        assert child_obs.parent_observation_id == "obs-root"


class TestTraceAnalyzeDataclasses:
    """Tests for trace analysis dataclasses (ISC rows 16, 21, 69)."""

    def test_bottleneck_info_fields(self):
        """BottleneckInfo should have required fields."""
        from langfuse_utils import BottleneckInfo

        bottleneck = BottleneckInfo(
            observation_id="obs-123",
            observation_name="slow-span",
            observation_type="SPAN",
            duration_ms=2500.0,
            percentage_of_total=75.0,
            model="gpt-4",
        )
        assert bottleneck.observation_id == "obs-123"
        assert bottleneck.observation_name == "slow-span"
        assert bottleneck.duration_ms == 2500.0
        assert bottleneck.percentage_of_total == 75.0
        assert bottleneck.model == "gpt-4"

    def test_error_info_fields(self):
        """ErrorInfo should have required fields."""
        from langfuse_utils import ErrorInfo

        error = ErrorInfo(
            observation_id="obs-err",
            observation_name="failed-call",
            observation_type="GENERATION",
            level="ERROR",
            status_message="Rate limit exceeded",
            timestamp="2026-01-20T10:00:00",
        )
        assert error.observation_id == "obs-err"
        assert error.level == "ERROR"
        assert error.status_message == "Rate limit exceeded"

    def test_latency_stats_fields(self):
        """LatencyStats should have required fields."""
        from langfuse_utils import LatencyStats

        stats = LatencyStats(
            total_ms=3200.0,
            p50_ms=400.0,
            p95_ms=2800.0,
            p99_ms=3000.0,
            observation_count=10,
        )
        assert stats.total_ms == 3200.0
        assert stats.p50_ms == 400.0
        assert stats.p95_ms == 2800.0
        assert stats.p99_ms == 3000.0
        assert stats.observation_count == 10

    def test_trace_analysis_fields(self):
        """TraceAnalysis should have required fields."""
        from langfuse_utils import LatencyStats, TraceAnalysis

        analysis = TraceAnalysis(
            trace_id="trace-123",
            trace_name="test-trace",
            has_timing_data=True,
            has_errors=False,
            summary="Total latency: 1000ms",
            latency=LatencyStats(total_ms=1000.0, observation_count=3),
            bottlenecks=[],
            errors=[],
            total_cost=0.001,
            cost_by_model={"gpt-4": 0.001},
        )
        assert analysis.trace_id == "trace-123"
        assert analysis.has_timing_data is True
        assert analysis.summary == "Total latency: 1000ms"

    def test_trace_analyze_result_success(self):
        """TraceAnalyzeResult should represent successful analysis."""
        from langfuse_utils import LatencyStats, TraceAnalysis, TraceAnalyzeResult

        analysis = TraceAnalysis(
            trace_id="trace-123",
            trace_name="test",
            has_timing_data=True,
            has_errors=False,
            summary="Analysis complete",
            latency=LatencyStats(total_ms=1000.0, observation_count=2),
            bottlenecks=[],
            errors=[],
            total_cost=None,
            cost_by_model=None,
        )
        result = TraceAnalyzeResult(
            ok=True,
            code="OK",
            message="Analysis complete",
            analysis=analysis,
        )
        assert result.ok is True
        assert result.code == "OK"
        assert result.analysis is not None

    def test_trace_analyze_result_no_timing_data(self):
        """TraceAnalyzeResult should handle no timing data case."""
        from langfuse_utils import TraceAnalyzeResult

        result = TraceAnalyzeResult(
            ok=False,
            code="NO_TIMING_DATA",
            message="Cannot analyze: no timing data available",
            analysis=None,
        )
        assert result.ok is False
        assert result.code == "NO_TIMING_DATA"


class TestLangfuseClientAnalyzeTrace:
    """Tests for LangfuseClient analyze_trace() method (ISC rows 16, 21, 69)."""

    @pytest.fixture(autouse=True)
    def setup_env(self, monkeypatch):
        """Set up valid environment using monkeypatch."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

    def _create_mock_trace_with_observations(
        self, trace_id: str, observations: list[dict]
    ) -> tuple[MagicMock, MagicMock]:
        """Helper to create mock trace and observations."""
        mock_langfuse = MagicMock()

        mock_trace = MagicMock()
        mock_trace.id = trace_id
        mock_trace.name = "test-trace"
        mock_trace.timestamp = "2026-01-20T10:00:00"
        mock_trace.session_id = None
        mock_trace.user_id = None
        mock_trace.input = None
        mock_trace.output = None
        mock_trace.metadata = None
        mock_trace.tags = None
        mock_langfuse.api.trace.get.return_value = mock_trace

        mock_obs_list = []
        for obs_data in observations:
            mock_obs = MagicMock()
            mock_obs.id = obs_data.get("id", "obs-1")
            mock_obs.type = obs_data.get("type", "SPAN")
            mock_obs.name = obs_data.get("name", "test-obs")
            mock_obs.start_time = obs_data.get("start_time", "2026-01-20T10:00:00")
            mock_obs.end_time = obs_data.get("end_time")
            mock_obs.level = obs_data.get("level")
            mock_obs.status_message = obs_data.get("status_message")
            mock_obs.model = obs_data.get("model")
            mock_obs.input = obs_data.get("input")
            mock_obs.output = obs_data.get("output")
            mock_obs.usage = obs_data.get("usage")
            mock_obs.calculated_total_cost = obs_data.get("cost")
            mock_obs.parent_observation_id = obs_data.get("parent_id")
            mock_obs_list.append(mock_obs)

        mock_obs_response = MagicMock()
        mock_obs_response.data = mock_obs_list
        mock_obs_response.meta = None
        mock_langfuse.api.observations_v_2.get_many.return_value = mock_obs_response

        return mock_langfuse, mock_trace

    def test_analyze_trace_returns_analyze_result(self):
        """analyze_trace() should return TraceAnalyzeResult."""
        from datetime import datetime, timedelta

        from langfuse_utils import TraceAnalyzeResult

        start = datetime(2026, 1, 20, 10, 0, 0)
        end = start + timedelta(seconds=1)

        mock_langfuse, _ = self._create_mock_trace_with_observations(
            "trace-123",
            [
                {
                    "id": "obs-1",
                    "type": "GENERATION",
                    "name": "llm-call",
                    "start_time": start,
                    "end_time": end,
                }
            ],
        )

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.analyze_trace("trace-123")

        assert isinstance(result, TraceAnalyzeResult)

    def test_analyze_trace_identifies_bottlenecks(self):
        """analyze_trace() should identify slowest observations (ISC row 16)."""
        from datetime import datetime, timedelta

        start = datetime(2026, 1, 20, 10, 0, 0)

        mock_langfuse, _ = self._create_mock_trace_with_observations(
            "trace-123",
            [
                {
                    "id": "obs-1",
                    "type": "GENERATION",
                    "name": "fast-call",
                    "start_time": start,
                    "end_time": start + timedelta(milliseconds=200),
                },
                {
                    "id": "obs-2",
                    "type": "SPAN",
                    "name": "slow-span",
                    "start_time": start,
                    "end_time": start + timedelta(milliseconds=2800),
                },
                {
                    "id": "obs-3",
                    "type": "SPAN",
                    "name": "medium-span",
                    "start_time": start,
                    "end_time": start + timedelta(milliseconds=500),
                },
            ],
        )

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.analyze_trace("trace-123")

        assert result.ok is True
        assert result.analysis is not None
        # Should identify bottlenecks sorted by duration
        assert len(result.analysis.bottlenecks) == 3
        # Slowest should be first
        assert result.analysis.bottlenecks[0].observation_name == "slow-span"
        assert result.analysis.bottlenecks[0].duration_ms == 2800.0

    def test_analyze_trace_calculates_percentiles(self):
        """analyze_trace() should calculate p50, p95, p99 (ISC row 16)."""
        from datetime import datetime, timedelta

        start = datetime(2026, 1, 20, 10, 0, 0)

        # Create 5 observations with different durations for percentile calculation
        mock_langfuse, _ = self._create_mock_trace_with_observations(
            "trace-123",
            [
                {"id": f"obs-{i}", "type": "SPAN", "name": f"span-{i}",
                 "start_time": start, "end_time": start + timedelta(milliseconds=d)}
                for i, d in enumerate([100, 200, 300, 400, 500])
            ],
        )

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.analyze_trace("trace-123")

        assert result.ok is True
        assert result.analysis is not None
        assert result.analysis.latency is not None
        # Should have percentiles with 5 data points
        assert result.analysis.latency.p50_ms is not None
        assert result.analysis.latency.p95_ms is not None
        assert result.analysis.latency.p99_ms is not None

    def test_analyze_trace_highlights_errors(self):
        """analyze_trace() should highlight error observations (ISC row 16)."""
        from datetime import datetime, timedelta

        start = datetime(2026, 1, 20, 10, 0, 0)

        mock_langfuse, _ = self._create_mock_trace_with_observations(
            "trace-err",
            [
                {
                    "id": "obs-ok",
                    "type": "SPAN",
                    "name": "success-span",
                    "start_time": start,
                    "end_time": start + timedelta(milliseconds=100),
                    "level": "INFO",
                },
                {
                    "id": "obs-err",
                    "type": "GENERATION",
                    "name": "failed-call",
                    "start_time": start,
                    "end_time": start + timedelta(milliseconds=500),
                    "level": "ERROR",
                    "status_message": "Rate limit exceeded",
                },
            ],
        )

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.analyze_trace("trace-err")

        assert result.ok is True
        assert result.analysis is not None
        assert result.analysis.has_errors is True
        assert len(result.analysis.errors) == 1
        assert result.analysis.errors[0].level == "ERROR"
        assert result.analysis.errors[0].observation_name == "failed-call"

    def test_analyze_trace_no_timing_data(self):
        """analyze_trace() with no timing data returns appropriate error (ISC row 16)."""
        mock_langfuse, _ = self._create_mock_trace_with_observations(
            "trace-no-time",
            [
                {
                    "id": "obs-1",
                    "type": "EVENT",
                    "name": "event-only",
                    "start_time": "2026-01-20T10:00:00",
                    # No end_time = no duration
                },
            ],
        )

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.analyze_trace("trace-no-time")

        # Should return error for no timing data
        assert result.ok is False
        assert result.code == "NO_TIMING_DATA"
        assert "no timing data" in result.message.lower()

    def test_analyze_trace_not_found(self):
        """analyze_trace() should handle trace not found."""
        mock_langfuse = MagicMock()
        mock_langfuse.api.trace.get.side_effect = Exception("404 Not Found")

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.analyze_trace("invalid-trace-id")

        assert result.ok is False
        assert result.code == NOT_FOUND

    def test_analyze_trace_collects_costs(self):
        """analyze_trace() should collect cost information."""
        from datetime import datetime, timedelta

        start = datetime(2026, 1, 20, 10, 0, 0)

        mock_langfuse, _ = self._create_mock_trace_with_observations(
            "trace-cost",
            [
                {
                    "id": "obs-1",
                    "type": "GENERATION",
                    "name": "gpt4-call",
                    "model": "gpt-4",
                    "start_time": start,
                    "end_time": start + timedelta(milliseconds=500),
                    "cost": 0.002,
                },
                {
                    "id": "obs-2",
                    "type": "GENERATION",
                    "name": "gpt35-call",
                    "model": "gpt-3.5-turbo",
                    "start_time": start,
                    "end_time": start + timedelta(milliseconds=200),
                    "cost": 0.0005,
                },
            ],
        )

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.analyze_trace("trace-cost")

        assert result.ok is True
        assert result.analysis is not None
        assert result.analysis.total_cost == 0.0025
        assert result.analysis.cost_by_model is not None
        assert "gpt-4" in result.analysis.cost_by_model
        assert "gpt-3.5-turbo" in result.analysis.cost_by_model

    def test_analyze_trace_summary_format(self):
        """analyze_trace() should return insight-first summary (ISC row 21, 69)."""
        from datetime import datetime, timedelta

        start = datetime(2026, 1, 20, 10, 0, 0)

        mock_langfuse, _ = self._create_mock_trace_with_observations(
            "trace-123",
            [
                {
                    "id": "obs-1",
                    "type": "SPAN",
                    "name": "embedding-lookup",
                    "start_time": start,
                    "end_time": start + timedelta(milliseconds=2800),
                },
                {
                    "id": "obs-2",
                    "type": "SPAN",
                    "name": "fast-span",
                    "start_time": start,
                    "end_time": start + timedelta(milliseconds=400),
                },
            ],
        )

        client = LangfuseClient()
        client._langfuse = mock_langfuse
        result = client.analyze_trace("trace-123")

        assert result.ok is True
        assert result.analysis is not None
        # Summary should mention key insight
        assert "embedding-lookup" in result.analysis.summary or "3200" in result.analysis.summary
        # Summary should be present in message
        assert result.message == result.analysis.summary
