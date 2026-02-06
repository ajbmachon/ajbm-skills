"""Tests for project setup verification."""

from pathlib import Path


def test_skill_directory_exists():
    """Verify the langfuse skill directory structure exists."""
    skill_dir = Path(".claude/skills/langfuse")
    assert skill_dir.exists(), "Skill directory should exist"
    assert skill_dir.is_dir(), "Skill directory should be a directory"


def test_skill_md_exists():
    """Verify SKILL.md exists in the skill directory."""
    skill_md = Path(".claude/skills/langfuse/SKILL.md")
    assert skill_md.exists(), "SKILL.md should exist"


def test_required_directories_exist():
    """Verify required subdirectories exist."""
    required_dirs = ["scripts", "lib", "references"]
    skill_dir = Path(".claude/skills/langfuse")

    for dir_name in required_dirs:
        dir_path = skill_dir / dir_name
        assert dir_path.exists(), f"{dir_name}/ directory should exist"
        assert dir_path.is_dir(), f"{dir_name}/ should be a directory"


def test_pyproject_toml_exists():
    """Verify pyproject.toml exists at project root."""
    pyproject = Path("pyproject.toml")
    assert pyproject.exists(), "pyproject.toml should exist"


def test_pyproject_toml_has_dependencies():
    """Verify pyproject.toml has required dependencies."""
    pyproject = Path("pyproject.toml")
    content = pyproject.read_text()

    assert "langfuse" in content, "pyproject.toml should include langfuse dependency"
    assert "python-dotenv" in content, "pyproject.toml should include python-dotenv dependency"


def test_ruff_toml_exists():
    """Verify ruff.toml exists at project root."""
    ruff_toml = Path("ruff.toml")
    assert ruff_toml.exists(), "ruff.toml should exist"


def test_pyproject_has_pytest_config():
    """Verify pyproject.toml has pytest configuration."""
    pyproject = Path("pyproject.toml")
    content = pyproject.read_text()

    assert "[tool.pytest.ini_options]" in content, "pyproject.toml should have pytest configuration"
    assert 'testpaths = ["tests"]' in content, "pytest should be configured to use tests/ directory"
