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


class TestTraceSubcommandActions:
    """Tests for trace subcommand actions (ISC rows 14-21)."""

    @pytest.fixture(autouse=True)
    def mock_auth(self, monkeypatch):
        """Mock auth for all trace tests."""
        monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
        monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")

    def test_trace_list_action_exists(self, capsys):
        """'trace list' action should exist.

        Acceptance criteria: 'python scripts/langfuse.py trace list' -> shows help
        """
        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None

            exit_code = main(["trace", "list"])

            assert exit_code == 0
            captured = capsys.readouterr()
            # Should show that command was recognized
            assert "list" in captured.out.lower() or "trace" in captured.out.lower()

    def test_trace_list_accepts_limit(self, capsys):
        """'trace list --limit 5' should accept limit parameter."""
        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None

            exit_code = main(["trace", "list", "--limit", "5"])

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "5" in captured.out

    def test_trace_get_requires_trace_id(self, capsys):
        """'trace get' should require trace_id argument."""
        with pytest.raises(SystemExit) as exc_info:
            main(["trace", "get"])

        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "trace_id" in captured.err.lower()

    def test_trace_get_accepts_trace_id(self, capsys):
        """'trace get <id>' should accept trace ID."""
        with patch.object(langfuse_cli, "LangfuseClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.auth_check.return_value = MagicMock(ok=True)
            mock_instance.flush.return_value = None

            exit_code = main(["trace", "get", "test-trace-123"])

            assert exit_code == 0
            captured = capsys.readouterr()
            assert "test-trace-123" in captured.out

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
