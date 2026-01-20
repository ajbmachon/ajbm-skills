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
        """'trace analyze <id>' should accept trace ID (ISC row 16)."""
        from langfuse_utils import (
            BottleneckInfo,
            LatencyStats,
            TraceAnalysis,
            TraceAnalyzeResult,
        )

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.analyze_trace.return_value = TraceAnalyzeResult(
                ok=True,
                code="OK",
                message="Total latency: 1500ms, slowest: llm-call (1000ms, 67%)",
                analysis=TraceAnalysis(
                    trace_id="test-trace-456",
                    trace_name="test-trace",
                    has_timing_data=True,
                    has_errors=False,
                    summary="Total latency: 1500ms, slowest: llm-call (1000ms, 67%)",
                    latency=LatencyStats(
                        total_ms=1500.0,
                        p50_ms=500.0,
                        p95_ms=1000.0,
                        p99_ms=1000.0,
                        observation_count=3,
                    ),
                    bottlenecks=[
                        BottleneckInfo(
                            observation_id="obs-1",
                            observation_name="llm-call",
                            observation_type="GENERATION",
                            duration_ms=1000.0,
                            percentage_of_total=66.7,
                            model="gpt-4",
                        ),
                    ],
                    errors=[],
                    total_cost=0.001,
                    cost_by_model={"gpt-4": 0.001},
                ),
            )

            exit_code = main(["trace", "analyze", "test-trace-456"])

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "test-trace-456" in captured.out

    def test_trace_analyze_shows_insight_first(self, capsys):
        """'trace analyze' should show key findings before data (ISC row 21, 69)."""
        from langfuse_utils import (
            BottleneckInfo,
            LatencyStats,
            TraceAnalysis,
            TraceAnalyzeResult,
        )

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.analyze_trace.return_value = TraceAnalyzeResult(
                ok=True,
                code="OK",
                message="Total latency: 3200ms, slowest: embedding-lookup (2800ms, 88%)",
                analysis=TraceAnalysis(
                    trace_id="trace-abc",
                    trace_name="chatbot",
                    has_timing_data=True,
                    has_errors=False,
                    summary="Total latency: 3200ms, slowest: embedding-lookup (2800ms, 88%). p50: 400ms, p95: 2800ms",
                    latency=LatencyStats(
                        total_ms=3200.0,
                        p50_ms=400.0,
                        p95_ms=2800.0,
                        p99_ms=2800.0,
                        observation_count=5,
                    ),
                    bottlenecks=[
                        BottleneckInfo(
                            observation_id="obs-1",
                            observation_name="embedding-lookup",
                            observation_type="SPAN",
                            duration_ms=2800.0,
                            percentage_of_total=87.5,
                        ),
                    ],
                    errors=[],
                    total_cost=None,
                    cost_by_model=None,
                ),
            )

            exit_code = main(["trace", "analyze", "trace-abc"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Key findings should appear early in output
            assert "KEY FINDINGS" in captured.out
            # Should show slowest span
            assert "embedding-lookup" in captured.out
            # Should show percentiles
            assert "p95" in captured.out or "2800" in captured.out

    def test_trace_analyze_highlights_errors_first(self, capsys):
        """'trace analyze' should highlight errors first (ISC row 16)."""
        from langfuse_utils import (
            BottleneckInfo,
            ErrorInfo,
            LatencyStats,
            TraceAnalysis,
            TraceAnalyzeResult,
        )

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.analyze_trace.return_value = TraceAnalyzeResult(
                ok=True,
                code="OK",
                message="Found 1 error(s) in trace. Total latency: 1500ms",
                analysis=TraceAnalysis(
                    trace_id="trace-err",
                    trace_name="error-trace",
                    has_timing_data=True,
                    has_errors=True,
                    summary="Found 1 error(s) in trace. Total latency: 1500ms, slowest: failed-call (1000ms, 67%)",
                    latency=LatencyStats(
                        total_ms=1500.0,
                        observation_count=2,
                    ),
                    bottlenecks=[
                        BottleneckInfo(
                            observation_id="obs-err",
                            observation_name="failed-call",
                            observation_type="GENERATION",
                            duration_ms=1000.0,
                            percentage_of_total=66.7,
                            model="gpt-4",
                        ),
                    ],
                    errors=[
                        ErrorInfo(
                            observation_id="obs-err",
                            observation_name="failed-call",
                            observation_type="GENERATION",
                            level="ERROR",
                            status_message="Rate limit exceeded",
                            timestamp="2026-01-20T10:00:00",
                        ),
                    ],
                    total_cost=None,
                    cost_by_model=None,
                ),
            )

            exit_code = main(["trace", "analyze", "trace-err"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show errors section
            assert "ERRORS" in captured.out
            # Error should appear in output
            assert "ERROR" in captured.out
            assert "failed-call" in captured.out or "Rate limit exceeded" in captured.out

    def test_trace_analyze_no_timing_data(self, capsys):
        """'trace analyze' with no timing data shows error (negative case ISC row 16)."""
        from langfuse_utils import TraceAnalysis, TraceAnalyzeResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.analyze_trace.return_value = TraceAnalyzeResult(
                ok=False,
                code="NO_TIMING_DATA",
                message="Cannot analyze: no timing data available",
                analysis=TraceAnalysis(
                    trace_id="trace-no-time",
                    trace_name="no-timing-trace",
                    has_timing_data=False,
                    has_errors=False,
                    summary="Cannot analyze: no timing data available",
                    latency=None,
                    bottlenecks=[],
                    errors=[],
                    total_cost=None,
                    cost_by_model=None,
                ),
            )

            exit_code = main(["trace", "analyze", "trace-no-time"])

            # Should fail with appropriate message
            assert exit_code == 1
            captured = capsys.readouterr()
            assert "cannot analyze" in captured.err.lower() or "no timing data" in captured.err.lower()

    def test_trace_analyze_shows_cost_breakdown(self, capsys):
        """'trace analyze' should show cost breakdown when available."""
        from langfuse_utils import (
            BottleneckInfo,
            LatencyStats,
            TraceAnalysis,
            TraceAnalyzeResult,
        )

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.analyze_trace.return_value = TraceAnalyzeResult(
                ok=True,
                code="OK",
                message="Analysis complete",
                analysis=TraceAnalysis(
                    trace_id="trace-cost",
                    trace_name="cost-trace",
                    has_timing_data=True,
                    has_errors=False,
                    summary="Total latency: 1000ms",
                    latency=LatencyStats(total_ms=1000.0, observation_count=2),
                    bottlenecks=[
                        BottleneckInfo(
                            observation_id="obs-1",
                            observation_name="llm-call",
                            observation_type="GENERATION",
                            duration_ms=800.0,
                            percentage_of_total=80.0,
                            model="gpt-4",
                        ),
                    ],
                    errors=[],
                    total_cost=0.0025,
                    cost_by_model={"gpt-4": 0.002, "gpt-3.5-turbo": 0.0005},
                ),
            )

            exit_code = main(["trace", "analyze", "trace-cost"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show cost summary
            assert "COST" in captured.out
            assert "gpt-4" in captured.out

    def test_trace_analyze_handles_not_found(self, capsys):
        """'trace analyze' should handle not found error."""
        from langfuse_utils import TraceAnalyzeResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.analyze_trace.return_value = TraceAnalyzeResult(
                ok=False,
                code="NOT_FOUND",
                message="Trace not found: invalid-id",
                analysis=None,
            )

            exit_code = main(["trace", "analyze", "invalid-id"])

            assert exit_code == 1
            captured = capsys.readouterr()
            assert "not found" in captured.err.lower()


class TestTraceErrorsCommand:
    """Tests for 'trace errors' command (ISC row 17)."""

    @pytest.fixture(autouse=True)
    def mock_auth(self, monkeypatch):
        """Mock auth for all trace errors tests."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

    def test_trace_errors_finds_errors(self, capsys):
        """'trace errors' should find traces with errors (ISC row 17)."""
        from langfuse_utils import TraceErrorInfo, TraceErrorsResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_errors.return_value = TraceErrorsResult(
                ok=True,
                code="OK",
                message="Found 2 error(s) in last 24 hour(s)",
                errors=[
                    TraceErrorInfo(
                        trace_id="trace-err-1",
                        trace_name="failed-chatbot",
                        trace_timestamp="2026-01-20T10:00:00",
                        observation_id="obs-err-1",
                        observation_name="llm-call",
                        observation_type="GENERATION",
                        error_message="Rate limit exceeded",
                        error_level="ERROR",
                    ),
                    TraceErrorInfo(
                        trace_id="trace-err-2",
                        trace_name="failed-analyzer",
                        trace_timestamp="2026-01-20T09:00:00",
                        observation_id="obs-err-2",
                        observation_name="api-call",
                        observation_type="SPAN",
                        error_message="Connection timeout",
                        error_level="ERROR",
                    ),
                ],
                total_count=2,
                time_range="last 24 hour(s)",
            )

            exit_code = main(["trace", "errors"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show error count
            assert "2 error(s)" in captured.out
            # Should show trace IDs
            assert "trace-err-1" in captured.out
            assert "trace-err-2" in captured.out
            # Should show error messages
            assert "Rate limit exceeded" in captured.out
            assert "Connection timeout" in captured.out

    def test_trace_errors_no_errors_found(self, capsys):
        """'trace errors' with no errors shows appropriate message (negative case)."""
        from langfuse_utils import TraceErrorsResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_errors.return_value = TraceErrorsResult(
                ok=True,
                code="OK",
                message="No errors in the specified time range (last 24 hour(s))",
                errors=[],
                total_count=0,
                time_range="last 24 hour(s)",
            )

            exit_code = main(["trace", "errors"])

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "no errors in the specified time range" in captured.out.lower()

    def test_trace_errors_accepts_since(self, capsys):
        """'trace errors --since 7d' should filter by time range."""
        from langfuse_utils import TraceErrorsResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_errors.return_value = TraceErrorsResult(
                ok=True,
                code="OK",
                message="No errors in the specified time range (last 7 day(s))",
                errors=[],
                total_count=0,
                time_range="last 7 day(s)",
            )

            exit_code = main(["trace", "errors", "--since", "7d"])

            assert exit_code == 0
            # Verify fetch_errors was called with correct since
            mock_instance.fetch_errors.assert_called_once_with(
                since="7d",
                limit=20,
            )

    def test_trace_errors_accepts_limit(self, capsys):
        """'trace errors --limit 5' should limit results."""
        from langfuse_utils import TraceErrorsResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_errors.return_value = TraceErrorsResult(
                ok=True,
                code="OK",
                message="No errors",
                errors=[],
                total_count=0,
                time_range="last 24 hour(s)",
            )

            exit_code = main(["trace", "errors", "--limit", "5"])

            assert exit_code == 0
            mock_instance.fetch_errors.assert_called_once_with(
                since="24h",
                limit=5,
            )

    def test_trace_errors_handles_api_error(self, capsys):
        """'trace errors' should handle API errors gracefully."""
        from langfuse_utils import TraceErrorsResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_errors.return_value = TraceErrorsResult(
                ok=False,
                code="API_ERROR",
                message="Failed to fetch errors: Connection timeout",
                errors=[],
            )

            exit_code = main(["trace", "errors"])

            assert exit_code == 1
            captured = capsys.readouterr()
            assert "error" in captured.err.lower()


class TestTraceCostsCommand:
    """Tests for 'trace costs' command (ISC row 18)."""

    @pytest.fixture(autouse=True)
    def mock_auth(self, monkeypatch):
        """Mock auth for all trace costs tests."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

    def test_trace_costs_shows_by_model(self, capsys):
        """'trace costs --group-by model' shows cost breakdown by model (ISC row 18)."""
        from langfuse_utils import CostByModel, TraceCostsResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_costs.return_value = TraceCostsResult(
                ok=True,
                code="OK",
                message="Cost breakdown for last 7 day(s)",
                total_cost=0.0125,
                time_range="last 7 day(s)",
                group_by="model",
                by_model=[
                    CostByModel(model="gpt-4", total_cost=0.01, observation_count=10),
                    CostByModel(model="gpt-3.5-turbo", total_cost=0.0025, observation_count=50),
                ],
            )

            exit_code = main(["trace", "costs", "--group-by", "model"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show total cost
            assert "0.012500" in captured.out
            # Should show models
            assert "gpt-4" in captured.out
            assert "gpt-3.5-turbo" in captured.out
            # Should show cost by model
            assert "COST BY MODEL" in captured.out

    def test_trace_costs_shows_by_trace(self, capsys):
        """'trace costs --group-by trace' shows top expensive traces."""
        from langfuse_utils import CostByTrace, TraceCostsResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_costs.return_value = TraceCostsResult(
                ok=True,
                code="OK",
                message="Cost breakdown for last 7 day(s)",
                total_cost=0.05,
                time_range="last 7 day(s)",
                group_by="trace",
                by_trace=[
                    CostByTrace(
                        trace_id="trace-expensive-1",
                        trace_name="complex-query",
                        total_cost=0.03,
                        observation_count=15,
                    ),
                    CostByTrace(
                        trace_id="trace-expensive-2",
                        trace_name="summarization",
                        total_cost=0.02,
                        observation_count=8,
                    ),
                ],
            )

            exit_code = main(["trace", "costs", "--group-by", "trace"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show trace IDs
            assert "trace-expensive-1" in captured.out
            assert "trace-expensive-2" in captured.out
            # Should show trace names
            assert "complex-query" in captured.out
            assert "summarization" in captured.out
            # Should show "TOP" header
            assert "TOP" in captured.out

    def test_trace_costs_shows_by_day(self, capsys):
        """'trace costs --group-by day' shows cost per day."""
        from langfuse_utils import CostByDay, TraceCostsResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_costs.return_value = TraceCostsResult(
                ok=True,
                code="OK",
                message="Cost breakdown for last 7 day(s)",
                total_cost=0.07,
                time_range="last 7 day(s)",
                group_by="day",
                by_day=[
                    CostByDay(date="2026-01-20", total_cost=0.03, observation_count=100),
                    CostByDay(date="2026-01-19", total_cost=0.02, observation_count=80),
                    CostByDay(date="2026-01-18", total_cost=0.02, observation_count=60),
                ],
            )

            exit_code = main(["trace", "costs", "--group-by", "day"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show dates
            assert "2026-01-20" in captured.out
            assert "2026-01-19" in captured.out
            # Should show "COST BY DAY" header
            assert "COST BY DAY" in captured.out

    def test_trace_costs_accepts_since(self, capsys):
        """'trace costs --since 24h' should filter by time range."""
        from langfuse_utils import TraceCostsResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_costs.return_value = TraceCostsResult(
                ok=True,
                code="OK",
                message="Cost breakdown for last 24 hour(s)",
                total_cost=0.0,
                time_range="last 24 hour(s)",
                group_by="model",
            )

            exit_code = main(["trace", "costs", "--since", "24h"])

            assert exit_code == 0
            mock_instance.fetch_costs.assert_called_once_with(
                group_by="model",
                since="24h",
            )

    def test_trace_costs_handles_no_data(self, capsys):
        """'trace costs' with no cost data shows appropriate message."""
        from langfuse_utils import TraceCostsResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_costs.return_value = TraceCostsResult(
                ok=True,
                code="OK",
                message="Cost breakdown for last 7 day(s)",
                total_cost=0.0,
                time_range="last 7 day(s)",
                group_by="model",
                by_model=None,
            )

            exit_code = main(["trace", "costs"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show total cost as 0
            assert "0.000000" in captured.out

    def test_trace_costs_handles_api_error(self, capsys):
        """'trace costs' should handle API errors gracefully."""
        from langfuse_utils import TraceCostsResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_costs.return_value = TraceCostsResult(
                ok=False,
                code="API_ERROR",
                message="Failed to fetch costs: Connection timeout",
                total_cost=0.0,
                time_range="",
                group_by="model",
            )

            exit_code = main(["trace", "costs"])

            assert exit_code == 1
            captured = capsys.readouterr()
            assert "error" in captured.err.lower()


class TestEvaluateSubcommandActions:
    """Tests for evaluate subcommand actions (ISC rows 22-28)."""

    @pytest.fixture(autouse=True)
    def mock_auth(self, monkeypatch):
        """Mock auth for all evaluate tests."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

    def test_evaluate_design_shows_guidance(self, capsys):
        """'evaluate design' should show evaluation strategy guidance (ISC row 22)."""
        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None

            exit_code = main(["evaluate", "design"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show evaluation methods
            assert "EVALUATION" in captured.out
            # Should mention score types
            assert "NUMERIC" in captured.out
            assert "CATEGORICAL" in captured.out
            assert "BOOLEAN" in captured.out
            # Should mention LLM-as-a-Judge
            assert "LLM-AS-A-JUDGE" in captured.out
            # Should mention annotation queues
            assert "ANNOTATION" in captured.out

    def test_evaluate_score_requires_trace_id(self, capsys):
        """'evaluate score' should require trace_id argument."""
        with pytest.raises(SystemExit):
            main(["evaluate", "score"])

    def test_evaluate_score_requires_name(self, capsys):
        """'evaluate score <trace_id>' should require --name."""
        with pytest.raises(SystemExit):
            main(["evaluate", "score", "trace-123"])

    def test_evaluate_score_requires_value(self, capsys):
        """'evaluate score <trace_id> --name X' should require --value."""
        with pytest.raises(SystemExit):
            main(["evaluate", "score", "trace-123", "--name", "quality"])

    def test_evaluate_score_creates_numeric_score(self, capsys):
        """'evaluate score' should create a numeric score (ISC row 23).

        Example: 'evaluate score abc123 --name quality --value 0.8 --data-type numeric'
        """
        from langfuse_utils import ScoreCreateResult, ScoreInfo

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.create_score.return_value = ScoreCreateResult(
                ok=True,
                code="OK",
                message="Score 'quality' created for trace abc123",
                score=ScoreInfo(
                    id="abc123-quality",
                    trace_id="abc123",
                    name="quality",
                    value=0.8,
                    data_type="NUMERIC",
                    comment=None,
                ),
            )

            exit_code = main(
                [
                    "evaluate",
                    "score",
                    "abc123",
                    "--name",
                    "quality",
                    "--value",
                    "0.8",
                    "--data-type",
                    "numeric",
                ]
            )

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show success
            assert "SCORE CREATED" in captured.out
            assert "abc123" in captured.out
            assert "quality" in captured.out
            assert "0.8" in captured.out
            assert "NUMERIC" in captured.out

    def test_evaluate_score_creates_categorical_score(self, capsys):
        """'evaluate score' should create a categorical score."""
        from langfuse_utils import ScoreCreateResult, ScoreInfo

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.create_score.return_value = ScoreCreateResult(
                ok=True,
                code="OK",
                message="Score 'accuracy' created for trace trace-456",
                score=ScoreInfo(
                    id="trace-456-accuracy",
                    trace_id="trace-456",
                    name="accuracy",
                    value="partially correct",
                    data_type="CATEGORICAL",
                    comment=None,
                ),
            )

            exit_code = main(
                [
                    "evaluate",
                    "score",
                    "trace-456",
                    "--name",
                    "accuracy",
                    "--value",
                    "partially correct",
                    "--data-type",
                    "categorical",
                ]
            )

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "SCORE CREATED" in captured.out
            assert "CATEGORICAL" in captured.out

    def test_evaluate_score_creates_boolean_score(self, capsys):
        """'evaluate score' should create a boolean score."""
        from langfuse_utils import ScoreCreateResult, ScoreInfo

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.create_score.return_value = ScoreCreateResult(
                ok=True,
                code="OK",
                message="Score 'is_helpful' created for trace trace-789",
                score=ScoreInfo(
                    id="trace-789-is_helpful",
                    trace_id="trace-789",
                    name="is_helpful",
                    value=1.0,
                    data_type="BOOLEAN",
                    comment=None,
                ),
            )

            exit_code = main(
                [
                    "evaluate",
                    "score",
                    "trace-789",
                    "--name",
                    "is_helpful",
                    "--value",
                    "1",
                    "--data-type",
                    "boolean",
                ]
            )

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "SCORE CREATED" in captured.out
            assert "BOOLEAN" in captured.out

    def test_evaluate_score_with_comment(self, capsys):
        """'evaluate score' should accept --comment option."""
        from langfuse_utils import ScoreCreateResult, ScoreInfo

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.create_score.return_value = ScoreCreateResult(
                ok=True,
                code="OK",
                message="Score 'quality' created for trace trace-123",
                score=ScoreInfo(
                    id="trace-123-quality",
                    trace_id="trace-123",
                    name="quality",
                    value=0.9,
                    data_type="NUMERIC",
                    comment="Excellent response",
                ),
            )

            exit_code = main(
                [
                    "evaluate",
                    "score",
                    "trace-123",
                    "--name",
                    "quality",
                    "--value",
                    "0.9",
                    "--comment",
                    "Excellent response",
                ]
            )

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "Excellent response" in captured.out

    def test_evaluate_score_invalid_data_type(self, capsys):
        """'evaluate score' with invalid data-type shows error (negative case).

        Acceptance criteria: Invalid score type -> 'Invalid data-type. Use: numeric, categorical, boolean'
        """
        from langfuse_utils import ScoreCreateResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.create_score.return_value = ScoreCreateResult(
                ok=False,
                code="INVALID_DATA_TYPE",
                message="Invalid data-type. Use: numeric, categorical, boolean",
                score=None,
            )

            exit_code = main(
                [
                    "evaluate",
                    "score",
                    "trace-123",
                    "--name",
                    "quality",
                    "--value",
                    "0.8",
                    "--data-type",
                    "numeric",  # Simulating invalid type via mock
                ]
            )

            assert exit_code == 1
            captured = capsys.readouterr()
            assert "invalid data-type" in captured.err.lower()

    def test_evaluate_score_trace_not_found(self, capsys):
        """'evaluate score' with invalid trace_id shows not found error."""
        from langfuse_utils import ScoreCreateResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.create_score.return_value = ScoreCreateResult(
                ok=False,
                code="NOT_FOUND",
                message="Trace not found: invalid-trace-id",
                score=None,
            )

            exit_code = main(
                [
                    "evaluate",
                    "score",
                    "invalid-trace-id",
                    "--name",
                    "quality",
                    "--value",
                    "0.8",
                ]
            )

            assert exit_code == 1
            captured = capsys.readouterr()
            assert "not found" in captured.err.lower()

    def test_evaluate_scores_lists_scores(self, capsys):
        """'evaluate scores' should list scores for the project (ISC row 24)."""
        from langfuse_utils import ScoreInfo, ScoreListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_scores.return_value = ScoreListResult(
                ok=True,
                code="OK",
                message="Found 2 score(s)",
                scores=[
                    ScoreInfo(
                        id="score-1",
                        trace_id="trace-123",
                        name="quality",
                        value=0.8,
                        data_type="NUMERIC",
                        comment="Good response",
                    ),
                    ScoreInfo(
                        id="score-2",
                        trace_id="trace-456",
                        name="accuracy",
                        value="correct",
                        data_type="CATEGORICAL",
                        comment=None,
                    ),
                ],
                total_count=2,
            )

            exit_code = main(["evaluate", "scores"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show score count
            assert "2 score(s)" in captured.out
            # Should show score names
            assert "quality" in captured.out
            assert "accuracy" in captured.out
            # Should show trace IDs
            assert "trace-123" in captured.out
            assert "trace-456" in captured.out
            # Should show types
            assert "NUMERIC" in captured.out
            assert "CATEGORICAL" in captured.out

    def test_evaluate_scores_filters_by_trace(self, capsys):
        """'evaluate scores --trace abc123' should filter by trace ID.

        Example: 'evaluate scores --trace abc123' -> all scores for that trace
        """
        from langfuse_utils import ScoreInfo, ScoreListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_scores.return_value = ScoreListResult(
                ok=True,
                code="OK",
                message="Found 1 score(s)",
                scores=[
                    ScoreInfo(
                        id="score-1",
                        trace_id="abc123",
                        name="quality",
                        value=0.9,
                        data_type="NUMERIC",
                        comment=None,
                    ),
                ],
                total_count=1,
            )

            exit_code = main(["evaluate", "scores", "--trace", "abc123"])

            assert exit_code == 0
            # Verify fetch_scores was called with trace_id filter
            mock_instance.fetch_scores.assert_called_once_with(
                trace_id="abc123",
                name=None,
                limit=20,
            )

    def test_evaluate_scores_filters_by_name(self, capsys):
        """'evaluate scores --name quality' should filter by score name."""
        from langfuse_utils import ScoreListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_scores.return_value = ScoreListResult(
                ok=True,
                code="OK",
                message="Found 0 score(s)",
                scores=[],
                total_count=0,
            )

            exit_code = main(["evaluate", "scores", "--name", "quality"])

            assert exit_code == 0
            # Verify fetch_scores was called with name filter
            mock_instance.fetch_scores.assert_called_once_with(
                trace_id=None,
                name="quality",
                limit=20,
            )

    def test_evaluate_scores_accepts_limit(self, capsys):
        """'evaluate scores --limit 5' should limit results."""
        from langfuse_utils import ScoreListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_scores.return_value = ScoreListResult(
                ok=True,
                code="OK",
                message="Found 0 score(s)",
                scores=[],
                total_count=0,
            )

            exit_code = main(["evaluate", "scores", "--limit", "5"])

            assert exit_code == 0
            mock_instance.fetch_scores.assert_called_once_with(
                trace_id=None,
                name=None,
                limit=5,
            )

    def test_evaluate_scores_no_scores_found(self, capsys):
        """'evaluate scores' with no scores shows appropriate message."""
        from langfuse_utils import ScoreListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_scores.return_value = ScoreListResult(
                ok=True,
                code="OK",
                message="Found 0 score(s)",
                scores=[],
                total_count=0,
            )

            exit_code = main(["evaluate", "scores"])

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "no scores found" in captured.out.lower()

    def test_evaluate_scores_handles_api_error(self, capsys):
        """'evaluate scores' should handle API errors gracefully."""
        from langfuse_utils import ScoreListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_scores.return_value = ScoreListResult(
                ok=False,
                code="API_ERROR",
                message="Failed to fetch scores: Connection timeout",
                scores=[],
            )

            exit_code = main(["evaluate", "scores"])

            assert exit_code == 1
            captured = capsys.readouterr()
            assert "error" in captured.err.lower()

    def test_evaluate_scores_shows_pagination_hint(self, capsys):
        """'evaluate scores' should indicate when more scores are available."""
        from langfuse_utils import ScoreInfo, ScoreListResult

        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None
            mock_instance.fetch_scores.return_value = ScoreListResult(
                ok=True,
                code="OK",
                message="Found 20 score(s)",
                scores=[
                    ScoreInfo(
                        id=f"score-{i}",
                        trace_id=f"trace-{i}",
                        name="quality",
                        value=0.5 + i * 0.02,
                        data_type="NUMERIC",
                    )
                    for i in range(20)
                ],
                total_count=20,
                has_more=True,
                cursor="next-page-cursor",
            )

            exit_code = main(["evaluate", "scores"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show hint about more scores
            assert "more" in captured.out.lower()


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
