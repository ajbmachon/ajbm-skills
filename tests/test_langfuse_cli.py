"""Tests for scripts/langfuse.py CLI entry point.

Tests verify acceptance criteria from US-004:
- scripts/langfuse.py created as single entry point
- Subcommands implemented: trace, evaluate, experiment, setup
- Uses argparse for CLI parsing
- Imports from lib/langfuse_utils.py for shared functionality
- Auth validation before any operation (calls auth_check from utils)
- Example: 'python scripts/langfuse.py setup check' -> validates connection
- Example: 'python scripts/langfuse.py trace list' -> shows help for trace subcommand
- Negative case: 'python scripts/langfuse.py unknown' -> clear error about valid subcommands

ISC Reference: rows 7-13
"""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Get project root for absolute paths
PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / ".claude" / "skills" / "langfuse" / "scripts"
LIB_DIR = PROJECT_ROOT / ".claude" / "skills" / "langfuse" / "lib"

# Add lib directory first so langfuse_utils can be imported
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

# Load the langfuse.py script as a module using importlib to avoid conflicts
# with the langfuse SDK package
spec = importlib.util.spec_from_file_location(
    "langfuse_cli", SCRIPTS_DIR / "langfuse.py"
)
langfuse_cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(langfuse_cli)
main = langfuse_cli.main


class TestCLIEntryPoint:
    """Tests for CLI entry point existence and basic structure (ISC row 7)."""

    def test_langfuse_script_exists(self):
        """scripts/langfuse.py should exist."""
        script_path = Path(".claude/skills/langfuse/scripts/langfuse.py")
        assert script_path.exists(), "langfuse.py should exist in scripts/"

    def test_main_function_exists(self):
        """main() function should exist as entry point."""
        assert callable(main)

    def test_main_accepts_argv(self):
        """main() should accept argv parameter."""
        # Should not raise - empty argv shows help
        exit_code = main([])
        assert exit_code == 0


class TestSubcommandStructure:
    """Tests for subcommand structure (ISC row 9)."""

    def test_trace_subcommand_exists(self, capsys):
        """'trace' subcommand should exist."""
        # Calling with just 'trace' should show help, not error
        exit_code = main(["trace"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "trace" in captured.out.lower()

    def test_evaluate_subcommand_exists(self, capsys):
        """'evaluate' subcommand should exist."""
        exit_code = main(["evaluate"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "evaluate" in captured.out.lower()

    def test_experiment_subcommand_exists(self, capsys):
        """'experiment' subcommand should exist."""
        exit_code = main(["experiment"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "experiment" in captured.out.lower()

    def test_setup_subcommand_exists(self, capsys):
        """'setup' subcommand should exist."""
        exit_code = main(["setup"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "setup" in captured.out.lower()


class TestInvalidCommand:
    """Tests for invalid command handling (ISC acceptance criteria)."""

    def test_unknown_command_shows_error(self, capsys):
        """Unknown command should show clear error about valid subcommands.

        Acceptance criteria: 'python scripts/langfuse.py unknown' -> clear error
        """
        with pytest.raises(SystemExit) as exc_info:
            main(["unknown"])

        # argparse exits with code 2 for invalid arguments
        assert exc_info.value.code == 2

        captured = capsys.readouterr()
        # Error message should mention the invalid argument
        assert "unknown" in captured.err.lower() or "invalid" in captured.err.lower()


class TestSetupCheckCommand:
    """Tests for 'setup check' command (ISC row 35)."""

    @pytest.fixture(autouse=True)
    def mock_env(self, monkeypatch):
        """Set up valid environment for auth."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
        monkeypatch.setenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")

    def test_setup_check_validates_connection(self, capsys):
        """'setup check' should validate connection.

        Acceptance criteria: 'python scripts/langfuse.py setup check' -> validates connection
        """
        # Mock the auth_check to simulate successful connection
        mock_client = MagicMock()
        mock_client.auth_check.return_value = None  # Success

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True, code="OK")
            mock_instance.base_url = "https://cloud.langfuse.com"

            exit_code = main(["setup", "check"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show connection info
            assert "langfuse" in captured.out.lower()
            # Should show success indicator
            assert "✓" in captured.out or "ok" in captured.out.lower()

    def test_setup_check_fails_with_invalid_auth(self, capsys, monkeypatch):
        """'setup check' should fail clearly with invalid auth."""
        # Mock the LangfuseClient to simulate auth failure
        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(
                ok=False, code="AUTH_INVALID", message="Invalid API keys"
            )

            exit_code = main(["setup", "check"])

            assert exit_code == 1
            captured = capsys.readouterr()
            assert "invalid" in captured.err.lower() or "failed" in captured.err.lower()

    def test_setup_check_shows_next_step_on_failure(self, capsys):
        """'setup check' should show next step when auth fails."""
        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(
                ok=False, code="AUTH_INVALID", message="Invalid API keys"
            )

            exit_code = main(["setup", "check"])

            assert exit_code == 1
            captured = capsys.readouterr()
            # Should suggest running diagnose
            assert "diagnose" in captured.err.lower()


class TestSetupDiagnoseCommand:
    """Tests for 'setup diagnose' command (ISC rows 36-40)."""

    @pytest.fixture(autouse=True)
    def mock_env(self, monkeypatch):
        """Set up valid environment for auth."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
        monkeypatch.setenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")

    def test_setup_diagnose_runs_diagnostics(self, capsys):
        """'setup diagnose' should run diagnostics."""
        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.diagnose.return_value = MagicMock(
                healthy=True,
                summary="All checks passed.",
                issues=[],
                next_steps=[],
            )

            exit_code = main(["setup", "diagnose"])

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "diagnostic" in captured.out.lower() or "check" in captured.out.lower()

    def test_setup_diagnose_shows_issues(self, capsys):
        """'setup diagnose' should show found issues."""
        mock_issue = MagicMock()
        mock_issue.code = "AUTH_INVALID"
        mock_issue.severity = "error"
        mock_issue.message = "Authentication failed"
        mock_issue.detail = "Check your API keys"

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.diagnose.return_value = MagicMock(
                healthy=False,
                summary="Found 1 issue(s)",
                issues=[mock_issue],
                next_steps=["Fix your credentials"],
            )

            exit_code = main(["setup", "diagnose"])

            assert exit_code == 1
            captured = capsys.readouterr()
            assert "auth_invalid" in captured.out.lower()

    def test_setup_diagnose_handles_missing_credentials(self, capsys, monkeypatch):
        """'setup diagnose' should handle missing credentials gracefully."""
        # Clear credentials
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
        monkeypatch.setattr("langfuse_utils.load_dotenv", lambda *args, **kwargs: None)

        exit_code = main(["setup", "diagnose"])

        assert exit_code == 1
        captured = capsys.readouterr()
        # Should show helpful message about missing credentials
        assert "missing" in captured.out.lower() or "credential" in captured.out.lower()


class TestSetupGuideCommand:
    """Tests for 'setup guide' command (ISC row 37)."""

    def test_setup_guide_shows_steps(self, capsys):
        """'setup guide' should show step-by-step instructions."""
        exit_code = main(["setup", "guide"])

        assert exit_code == 0
        captured = capsys.readouterr()
        # Should contain step-by-step content
        assert "step" in captured.out.lower()
        # Should mention key components
        assert "langfuse" in captured.out.lower()
        assert "env" in captured.out.lower() or ".env" in captured.out.lower()

    def test_setup_guide_shows_regions(self, capsys):
        """'setup guide' should show both EU and US regions."""
        exit_code = main(["setup", "guide"])

        assert exit_code == 0
        captured = capsys.readouterr()
        # Should mention both regions
        assert "eu" in captured.out.lower()
        assert "us" in captured.out.lower()

    def test_setup_guide_shows_api_key_format(self, capsys):
        """'setup guide' should show correct API key format."""
        exit_code = main(["setup", "guide"])

        assert exit_code == 0
        captured = capsys.readouterr()
        # Should mention key prefixes
        assert "sk-lf" in captured.out.lower()
        assert "pk-lf" in captured.out.lower()


class TestTraceSubcommandActions:
    """Tests for trace subcommand actions (ISC rows 14-21)."""

    @pytest.fixture(autouse=True)
    def mock_auth(self, monkeypatch):
        """Mock auth for all trace tests."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

    def test_trace_list_action_exists(self, capsys):
        """'trace list' action should exist.

        Acceptance criteria: 'python scripts/langfuse.py trace list' -> fetches traces
        """
        # Import TraceListResult from langfuse_utils
        from langfuse_utils import TraceListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            # Mock fetch_traces to return empty list (valid response)
            mock_instance.fetch_traces.return_value = TraceListResult(
                ok=True,
                code="OK",
                message="Found 0 trace(s)",
                traces=[],
                has_more=False,
                cursor=None,
            )

            exit_code = main(["trace", "list"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show "no traces found" message for empty result
            assert "no traces found" in captured.out.lower()

    def test_trace_list_shows_traces(self, capsys):
        """'trace list' should display traces in table format (ISC row 14)."""
        from langfuse_utils import TraceInfo, TraceListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_traces.return_value = TraceListResult(
                ok=True,
                code="OK",
                message="Found 2 trace(s)",
                traces=[
                    TraceInfo(
                        id="trace-id-123",
                        name="chatbot",
                        timestamp="2026-01-20T10:00:00",
                        status="success",
                    ),
                    TraceInfo(
                        id="trace-id-456",
                        name="analyzer",
                        timestamp="2026-01-20T09:00:00",
                        status="error",
                    ),
                ],
                has_more=False,
                cursor=None,
            )

            exit_code = main(["trace", "list"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show trace IDs
            assert "trace-id-123" in captured.out
            assert "trace-id-456" in captured.out
            # Should show trace names
            assert "chatbot" in captured.out
            assert "analyzer" in captured.out
            # Should show status indicators
            assert "✓" in captured.out  # Success indicator
            assert "✗" in captured.out  # Error indicator

    def test_trace_list_accepts_limit(self, capsys):
        """'trace list --limit 5' should pass limit to fetch_traces."""
        from langfuse_utils import TraceListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_traces.return_value = TraceListResult(
                ok=True,
                code="OK",
                message="Found 0 trace(s)",
                traces=[],
                has_more=False,
                cursor=None,
            )

            exit_code = main(["trace", "list", "--limit", "5"])

            assert exit_code == 0
            # Verify fetch_traces was called with limit=5
            mock_instance.fetch_traces.assert_called_once_with(
                limit=5,
                name=None,
                user_id=None,
                session_id=None,
            )

    def test_trace_list_accepts_name_filter(self, capsys):
        """'trace list --name chatbot' should filter by name (ISC row 14)."""
        from langfuse_utils import TraceInfo, TraceListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_traces.return_value = TraceListResult(
                ok=True,
                code="OK",
                message="Found 1 trace(s)",
                traces=[
                    TraceInfo(
                        id="trace-chatbot",
                        name="chatbot",
                        timestamp="2026-01-20T10:00:00",
                        status="success",
                    ),
                ],
                has_more=False,
                cursor=None,
            )

            exit_code = main(["trace", "list", "--name", "chatbot"])

            assert exit_code == 0
            # Verify fetch_traces was called with name filter
            mock_instance.fetch_traces.assert_called_once_with(
                limit=10,
                name="chatbot",
                user_id=None,
                session_id=None,
            )

    def test_trace_list_accepts_user_id_filter(self, capsys):
        """'trace list --user-id user123' should filter by user ID (ISC row 14)."""
        from langfuse_utils import TraceListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_traces.return_value = TraceListResult(
                ok=True,
                code="OK",
                message="Found 0 trace(s)",
                traces=[],
                has_more=False,
                cursor=None,
            )

            exit_code = main(["trace", "list", "--user-id", "user123"])

            assert exit_code == 0
            mock_instance.fetch_traces.assert_called_once_with(
                limit=10,
                name=None,
                user_id="user123",
                session_id=None,
            )

    def test_trace_list_accepts_session_id_filter(self, capsys):
        """'trace list --session-id sess123' should filter by session ID (ISC row 14)."""
        from langfuse_utils import TraceListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_traces.return_value = TraceListResult(
                ok=True,
                code="OK",
                message="Found 0 trace(s)",
                traces=[],
                has_more=False,
                cursor=None,
            )

            exit_code = main(["trace", "list", "--session-id", "sess123"])

            assert exit_code == 0
            mock_instance.fetch_traces.assert_called_once_with(
                limit=10,
                name=None,
                user_id=None,
                session_id="sess123",
            )

    def test_trace_list_handles_api_error(self, capsys):
        """'trace list' should handle API errors gracefully."""
        from langfuse_utils import TraceListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_traces.return_value = TraceListResult(
                ok=False,
                code="API_ERROR",
                message="Failed to fetch traces: Connection timeout",
                traces=[],
            )

            exit_code = main(["trace", "list"])

            assert exit_code == 1
            captured = capsys.readouterr()
            assert "error" in captured.err.lower()

    def test_trace_list_shows_pagination_hint(self, capsys):
        """'trace list' should indicate when more traces are available."""
        from langfuse_utils import TraceInfo, TraceListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_traces.return_value = TraceListResult(
                ok=True,
                code="OK",
                message="Found 10 trace(s)",
                traces=[
                    TraceInfo(
                        id=f"trace-{i}",
                        name=f"trace-name-{i}",
                        timestamp="2026-01-20T10:00:00",
                        status="success",
                    )
                    for i in range(10)
                ],
                has_more=True,
                cursor="next-page-cursor",
            )

            exit_code = main(["trace", "list"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show hint about more traces
            assert "more" in captured.out.lower()

    def test_trace_get_requires_trace_id(self, capsys):
        """'trace get' should require trace_id argument."""
        with pytest.raises(SystemExit) as exc_info:
            main(["trace", "get"])

        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "trace_id" in captured.err.lower()

    def test_trace_get_accepts_trace_id(self, capsys):
        """'trace get <id>' should accept trace ID."""
        from langfuse_utils import TraceDetail, TraceGetResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_trace.return_value = TraceGetResult(
                ok=True,
                code="OK",
                message="Found trace with 0 observation(s)",
                trace=TraceDetail(
                    id="test-trace-123",
                    name="test-trace",
                    timestamp="2026-01-20T10:00:00",
                    session_id=None,
                    user_id=None,
                    input=None,
                    output=None,
                    metadata=None,
                    tags=None,
                    observations=[],
                ),
            )

            exit_code = main(["trace", "get", "test-trace-123"])

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "test-trace-123" in captured.out

    def test_trace_get_displays_observations(self, capsys):
        """'trace get <id>' should display observations with hierarchy (ISC row 20)."""
        from langfuse_utils import ObservationInfo, TraceDetail, TraceGetResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_trace.return_value = TraceGetResult(
                ok=True,
                code="OK",
                message="Found trace with 2 observation(s)",
                trace=TraceDetail(
                    id="trace-with-obs",
                    name="chatbot",
                    timestamp="2026-01-20T10:00:00",
                    session_id="session-123",
                    user_id="user-456",
                    input="Hello",
                    output="World",
                    metadata=None,
                    tags=["production"],
                    observations=[
                        ObservationInfo(
                            id="obs-gen-1",
                            type="GENERATION",
                            name="llm-call",
                            start_time="2026-01-20T10:00:01",
                            end_time="2026-01-20T10:00:02",
                            duration_ms=1000.0,
                            level=None,
                            status_message=None,
                            model="gpt-4",
                            input="Hello there",
                            output="Hi!",
                            input_tokens=10,
                            output_tokens=5,
                            total_tokens=15,
                            cost=0.0001,
                            parent_observation_id=None,
                        ),
                        ObservationInfo(
                            id="obs-span-1",
                            type="SPAN",
                            name="process-response",
                            start_time="2026-01-20T10:00:02",
                            end_time="2026-01-20T10:00:03",
                            duration_ms=500.0,
                            level=None,
                            status_message=None,
                            model=None,
                            input=None,
                            output=None,
                            parent_observation_id="obs-gen-1",
                        ),
                    ],
                ),
            )

            exit_code = main(["trace", "get", "trace-with-obs"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show trace ID
            assert "trace-with-obs" in captured.out
            # Should show session ID (hierarchy)
            assert "session-123" in captured.out
            # Should show observation types
            assert "[GEN]" in captured.out
            assert "[SPAN]" in captured.out
            # Should show observation names
            assert "llm-call" in captured.out
            assert "process-response" in captured.out
            # Should show model
            assert "gpt-4" in captured.out
            # Should show cost
            assert "0.0001" in captured.out
            # Should show tokens
            assert "in: 10" in captured.out
            assert "out: 5" in captured.out

    def test_trace_get_invalid_id_returns_not_found(self, capsys):
        """'trace get <invalid-id>' should return 'Trace not found' (negative case)."""
        from langfuse_utils import TraceGetResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_trace.return_value = TraceGetResult(
                ok=False,
                code="NOT_FOUND",
                message="Trace not found: invalid-trace-id",
                trace=None,
            )

            exit_code = main(["trace", "get", "invalid-trace-id"])

            assert exit_code == 1
            captured = capsys.readouterr()
            # Should show not found error message
            assert "trace not found" in captured.err.lower()
            assert "invalid-trace-id" in captured.err

    def test_trace_get_handles_api_error(self, capsys):
        """'trace get' should handle API errors gracefully."""
        from langfuse_utils import TraceGetResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_trace.return_value = TraceGetResult(
                ok=False,
                code="API_ERROR",
                message="Failed to fetch trace: Connection timeout",
                trace=None,
            )

            exit_code = main(["trace", "get", "some-trace-id"])

            assert exit_code == 1
            captured = capsys.readouterr()
            assert "error" in captured.err.lower()

    def test_trace_get_shows_event_observations(self, capsys):
        """'trace get' should display EVENT type observations."""
        from langfuse_utils import ObservationInfo, TraceDetail, TraceGetResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_trace.return_value = TraceGetResult(
                ok=True,
                code="OK",
                message="Found trace with 1 observation(s)",
                trace=TraceDetail(
                    id="trace-event",
                    name="event-trace",
                    timestamp="2026-01-20T10:00:00",
                    session_id=None,
                    user_id=None,
                    input=None,
                    output=None,
                    metadata=None,
                    tags=None,
                    observations=[
                        ObservationInfo(
                            id="obs-event-1",
                            type="EVENT",
                            name="user-feedback",
                            start_time="2026-01-20T10:00:01",
                            end_time=None,
                            duration_ms=None,
                            level="INFO",
                            status_message="User provided positive feedback",
                            model=None,
                            input=None,
                            output=None,
                            parent_observation_id=None,
                        ),
                    ],
                ),
            )

            exit_code = main(["trace", "get", "trace-event"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show EVENT type
            assert "[EVENT]" in captured.out
            assert "user-feedback" in captured.out

    def test_trace_analyze_accepts_trace_id(self, capsys):
        """'trace analyze <id>' should accept trace ID."""
        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None

            exit_code = main(["trace", "analyze", "test-trace-456"])

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "test-trace-456" in captured.out


class TestEvaluateSubcommandActions:
    """Tests for evaluate subcommand actions (ISC rows 22-28)."""

    @pytest.fixture(autouse=True)
    def mock_auth(self, monkeypatch):
        """Mock auth for all evaluate tests."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

    def test_evaluate_score_requires_trace_id(self, capsys):
        """'evaluate score' should require trace_id argument."""
        with pytest.raises(SystemExit):
            main(["evaluate", "score"])

    def test_evaluate_score_accepts_arguments(self, capsys):
        """'evaluate score' should accept required arguments."""
        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None

            exit_code = main(
                [
                    "evaluate",
                    "score",
                    "trace-123",
                    "--name",
                    "quality",
                    "--value",
                    "0.8",
                ]
            )

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "trace-123" in captured.out
            assert "quality" in captured.out
            assert "0.8" in captured.out


class TestExperimentSubcommandActions:
    """Tests for experiment subcommand actions (ISC rows 29-34)."""

    @pytest.fixture(autouse=True)
    def mock_auth(self, monkeypatch):
        """Mock auth for all experiment tests."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

    def test_experiment_create_dataset_requires_name(self, capsys):
        """'experiment create-dataset' should require --name."""
        with pytest.raises(SystemExit):
            main(["experiment", "create-dataset"])

    def test_experiment_create_dataset_accepts_name(self, capsys):
        """'experiment create-dataset --name X' should work."""
        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None

            exit_code = main(
                ["experiment", "create-dataset", "--name", "test-dataset"]
            )

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "test-dataset" in captured.out


class TestAuthValidationBeforeOperations:
    """Tests for auth validation before operations (ISC row 11)."""

    @pytest.fixture(autouse=True)
    def clean_env(self, monkeypatch):
        """Clean environment - no auth credentials."""
        monkeypatch.setattr("langfuse_utils.load_dotenv", lambda *args, **kwargs: None)
        monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
        monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)

    def test_trace_list_requires_auth(self, capsys):
        """'trace list' should fail without auth."""
        exit_code = main(["trace", "list"])

        # Should fail due to missing auth
        assert exit_code == 1
        captured = capsys.readouterr()
        # Should mention auth error
        assert "auth" in captured.err.lower() or "missing" in captured.err.lower()

    def test_evaluate_design_requires_auth(self, capsys):
        """'evaluate design' should fail without auth."""
        exit_code = main(["evaluate", "design"])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "auth" in captured.err.lower() or "missing" in captured.err.lower()

    def test_experiment_run_requires_auth(self, capsys):
        """'experiment run' should fail without auth."""
        exit_code = main(["experiment", "run", "--dataset", "test"])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "auth" in captured.err.lower() or "missing" in captured.err.lower()


class TestHelpMessages:
    """Tests for help message display."""

    def test_no_args_shows_help(self, capsys):
        """Running with no arguments should show help."""
        exit_code = main([])

        assert exit_code == 0
        captured = capsys.readouterr()
        # Help should list available commands
        assert "trace" in captured.out.lower()
        assert "evaluate" in captured.out.lower()
        assert "experiment" in captured.out.lower()
        assert "setup" in captured.out.lower()

    def test_help_flag_shows_help(self, capsys):
        """Running with --help should show help."""
        with pytest.raises(SystemExit) as exc_info:
            main(["--help"])

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "langfuse" in captured.out.lower()

    def test_subcommand_help_shows_actions(self, capsys):
        """'<subcommand> --help' should show available actions."""
        with pytest.raises(SystemExit) as exc_info:
            main(["trace", "--help"])

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "list" in captured.out.lower()
        assert "get" in captured.out.lower()
        assert "analyze" in captured.out.lower()
