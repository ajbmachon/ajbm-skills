#!/usr/bin/env python3
"""
Smart PreToolUse guard for Claude:
- Blocks truly dangerous operations without being intrusive
- Prevents reading/writing sensitive files
- Blocks destructive commands
"""

import json
import re
import sys
from typing import Any

# Files that should NEVER be read or modified
SENSITIVE_FILES = [
    r"(^|/)\.env(\.[^/]*)?$",  # .env files (must be actual filename) 
    r"(^|/)\devcontainer.local(\.[^/]*)?$",  # devcontainer secrets file (must be actual filename)
    r"(^|/)\.ssh(/|$)",  # SSH directory
    r"\.(pem|key|crt|cer|pfx|p12)$",  # Private keys and certificates
    r"(^|/)\.netrc$",  # Network credentials
    r"(^|/)\.npmrc$",  # NPM credentials
    r"(^|/)\.pypirc$",  # PyPI credentials
    r"(^|/)\.aws/credentials",  # AWS credentials
    r"(^|/)\.kube/config",  # Kubernetes config
    r"(^|/)etc/shadow",  # System passwords
    r"(^|/)\.gnupg(/|$)",  # GPG keys directory
]

# Dangerous bash patterns
DANGEROUS_COMMANDS = [
    r"\brm\s+-rf\s+/(?:\s|$)",  # rm -rf / (root)
    r"\brm\s+-rf\s+\*(?:\s|$)",  # rm -rf * (everything in current dir)
    r"\brm\s+-rf\s+\.\.(?:/|\s|$)",  # rm -rf .. (parent directory)
    r"\brm\s+-rf\s+~(?:/|\s|$)",  # rm -rf ~/ (home directory)
    r">\s*/dev/[sh]d[a-z]",  # Overwrite disk devices
    r"\bdd\s+.*\bof=/dev/[sh]d[a-z](?:\d)?(?:\s|$)",  # dd to disk devices
    r"\bmkfs\.\w+",  # Format filesystem commands
    r":\(\)\s*\{\s*:\|\s*:&\s*\}",  # Fork bomb pattern
    r"\bchmod\s+777\s+/",  # chmod 777 on root
    r"\>\s*/dev/null\s*&&\s*rm",  # Destructive redirects with rm
]


def is_sensitive_file(path: str) -> bool:
    """Check if a file path is sensitive."""
    if not path:
        return False
    return any(re.search(pattern, path, re.IGNORECASE) for pattern in SENSITIVE_FILES)


def is_dangerous_command(command: str) -> bool:
    """Check if a bash command is dangerous."""
    if not command:
        return False
    return any(
        re.search(pattern, command, re.IGNORECASE) for pattern in DANGEROUS_COMMANDS
    )


def check_bash_for_sensitive_read(command: str) -> bool:
    """Check if bash command tries to read sensitive files."""
    # Look for commands that read files
    read_patterns = [
        r"\bcat\s+([^\s;|&>]+)",  # cat filename (no pipes/redirects)
        r"\bless\s+([^\s;|&>]+)",  # less filename
        r"\bmore\s+([^\s;|&>]+)",  # more filename
        r"\bhead\s+(?:-\w+\s+)*([^\s;|&>]+)",  # head with optional flags
        r"\btail\s+(?:-\w+\s+)*([^\s;|&>]+)",  # tail with optional flags
        r"\bgrep\s+(?:-\w+\s+)*\w+\s+([^\s;|&>]+)",  # grep pattern filename
        r"\bawk\s+.*\s+([^\s;|&>]+)$",  # awk script filename
        r"\bsed\s+.*\s+([^\s;|&>]+)$",  # sed command filename
    ]

    for pattern in read_patterns:
        match = re.search(pattern, command)
        if match:
            file_path = match.group(1).strip()
            # Remove quotes and check
            file_path = file_path.strip("\"'")
            if is_sensitive_file(file_path):
                return True
    return False


def main() -> int:
    try:
        data: dict[str, Any] = json.load(sys.stdin)
    except Exception:
        # If stdin isn't JSON, allow operation
        return 0

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Check Bash commands
    if tool_name == "Bash":
        command = tool_input.get("command", "")

        # Check for dangerous commands
        if is_dangerous_command(command):
            print(
                json.dumps(
                    {
                        "decision": "block",
                        "reason": f"Dangerous command blocked: {command[:50]}...",
                    }
                )
            )
            return 2

        # Check for reading sensitive files
        if check_bash_for_sensitive_read(command):
            print(
                json.dumps(
                    {"decision": "block", "reason": "Command would read sensitive file"}
                )
            )
            return 2

    # Check Read operations
    elif tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        if is_sensitive_file(file_path):
            print(
                json.dumps(
                    {
                        "decision": "block",
                        "reason": f"Reading sensitive file blocked: {file_path}",
                    }
                )
            )
            return 2

    # Check Write/Edit operations
    elif tool_name in ["Write", "Edit", "MultiEdit"]:
        # Single file operations
        file_path = tool_input.get("file_path", "")
        if is_sensitive_file(file_path):
            print(
                json.dumps(
                    {
                        "decision": "block",
                        "reason": f"Modifying sensitive file blocked: {file_path}",
                    }
                )
            )
            return 2

        # MultiEdit operations
        if tool_name == "MultiEdit":
            for edit in tool_input.get("edits", []):
                if is_sensitive_file(edit.get("file_path", "")):
                    print(
                        json.dumps(
                            {
                                "decision": "block",
                                "reason": "Modifying sensitive file blocked",
                            }
                        )
                    )
                    return 2

    # Allow all other operations
    return 0


if __name__ == "__main__":
    sys.exit(main())
