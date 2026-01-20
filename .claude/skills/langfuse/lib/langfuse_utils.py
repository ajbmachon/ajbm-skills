"""Shared Langfuse utilities for consistent auth, client init, and error handling.

This module provides:
- LangfuseClient wrapper class for consistent client initialization
- Auth loading from .env (LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_BASE_URL)
- Error code constants with human-readable messages
- flush() helper for short-lived operations

ISC Reference: rows 53-59
"""

from __future__ import annotations

import os
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
NETWORK_ERROR = "NETWORK_ERROR"
RATE_LIMITED = "RATE_LIMITED"

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
        "Langfuse authentication failed. Check your API keys are correct and not expired. "
        "Keys should start with 'sk-lf-' (secret) and 'pk-lf-' (public). "
        "Also verify LANGFUSE_BASE_URL matches your region (EU vs US)."
    ),
    NETWORK_ERROR: (
        "Could not connect to Langfuse. Check your internet connection and "
        "verify LANGFUSE_BASE_URL is correct. "
        "EU: https://cloud.langfuse.com | US: https://us.cloud.langfuse.com"
    ),
    RATE_LIMITED: (
        "Langfuse API rate limit exceeded. Please wait a moment before retrying. "
        "For high-volume usage, consider implementing request batching."
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

    def auth_check(self) -> AuthResult:
        """Verify authentication and connection to Langfuse.

        Returns:
            AuthResult with code and message indicating status.

        Note:
            Does not raise exceptions - returns error codes for handling.
        """
        try:
            # Attempt to make a simple API call to verify auth
            # Using auth_check() from the SDK if available, otherwise a simple operation
            self.langfuse.auth_check()
            return AuthResult(code="OK", message="Successfully connected to Langfuse")
        except Exception as e:
            error_str = str(e).lower()

            # Detect auth issues
            if "401" in error_str or "unauthorized" in error_str:
                return AuthResult(
                    code=AUTH_INVALID,
                    message=ERROR_MESSAGES[AUTH_INVALID],
                )

            # Detect rate limiting
            if "429" in error_str or "rate" in error_str:
                return AuthResult(
                    code=RATE_LIMITED,
                    message=ERROR_MESSAGES[RATE_LIMITED],
                )

            # Detect network issues
            if any(
                term in error_str
                for term in ["connection", "timeout", "network", "dns", "refused"]
            ):
                return AuthResult(
                    code=NETWORK_ERROR,
                    message=ERROR_MESSAGES[NETWORK_ERROR],
                )

            # Unknown error - include original message
            return AuthResult(
                code=NETWORK_ERROR,
                message=f"Langfuse connection failed: {e}",
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
