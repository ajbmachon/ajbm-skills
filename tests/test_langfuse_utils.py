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
    AUTH_INVALID,
    AUTH_MISSING,
    ERROR_MESSAGES,
    NETWORK_ERROR,
    RATE_LIMITED,
    AuthResult,
    LangfuseClient,
    LangfuseError,
)


class TestErrorCodeConstants:
    """Tests for error code constants (ISC row 58)."""

    def test_auth_missing_constant_exists(self):
        """AUTH_MISSING constant should be defined."""
        assert AUTH_MISSING == "AUTH_MISSING"

    def test_auth_invalid_constant_exists(self):
        """AUTH_INVALID constant should be defined."""
        assert AUTH_INVALID == "AUTH_INVALID"

    def test_network_error_constant_exists(self):
        """NETWORK_ERROR constant should be defined."""
        assert NETWORK_ERROR == "NETWORK_ERROR"

    def test_rate_limited_constant_exists(self):
        """RATE_LIMITED constant should be defined."""
        assert RATE_LIMITED == "RATE_LIMITED"


class TestErrorMessages:
    """Tests for human-readable error messages (ISC row 59)."""

    def test_all_error_codes_have_messages(self):
        """Every error code should have a human-readable message."""
        error_codes = [AUTH_MISSING, AUTH_INVALID, NETWORK_ERROR, RATE_LIMITED]
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
        result = client.auth_check()

        assert result.code == NETWORK_ERROR
        assert result.ok is False


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
