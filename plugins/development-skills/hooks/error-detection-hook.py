#!/usr/bin/env python3
"""
PostToolUse hook for automatic skill suggestion when errors are detected.
Monitors Bash tool output for test failures, build errors, and runtime exceptions.

Suggests:
- systematic-debugging: Always when errors detected (investigate before fixing)
- testing-anti-patterns: When test failures detected (avoid common testing mistakes)
"""

import json
import re
import sys

# Error pattern categories
TEST_FAILURE_PATTERNS = [
    r'\bFAIL\b',
    r'\bfailed\b.*test',
    r'test.*\bfailed\b',
    r'AssertionError',
    r'assertion failed',
    r'Expected.*but (got|received)',
    r'expected.*to (equal|be|match)',
    r'\d+ (failed|failing)',
    r'FAILED',
    r'✗|✕|×',  # Common failure symbols
    r'jest.*failed',
    r'vitest.*failed',
    r'pytest.*failed',
    r'mocha.*failing',
    r'Test failed',
    r'Tests? failed',
]

BUILD_ERROR_PATTERNS = [
    r'error\[E\d+\]',  # Rust errors
    r'error:.*\n.*\^',  # Compiler errors with caret
    r'SyntaxError:',
    r'TypeError:',
    r'ReferenceError:',
    r'cannot find module',
    r'Module not found',
    r'compilation failed',
    r'Build failed',
    r'npm ERR!',
    r'yarn error',
    r'cargo error',
    r'tsc.*error',
    r'error TS\d+:',  # TypeScript errors
]

RUNTIME_ERROR_PATTERNS = [
    r'Traceback \(most recent call last\)',
    r'Exception:',
    r'Error:',
    r'panic:',  # Go/Rust panic
    r'ECONNREFUSED',
    r'ENOENT',
    r'EPERM',
    r'Segmentation fault',
    r'stack trace',
    r'at .*:\d+:\d+',  # JS stack trace lines
    r'File ".*", line \d+',  # Python stack trace
    r'^\s+at\s+',  # Indented stack trace
]


def detect_error_type(output: str) -> dict:
    """
    Analyze output for error patterns.
    Returns dict with error types detected and matched patterns.
    """
    result = {
        "has_error": False,
        "test_failure": False,
        "build_error": False,
        "runtime_error": False,
        "matched_patterns": [],
    }

    # Check for test failures
    for pattern in TEST_FAILURE_PATTERNS:
        if re.search(pattern, output, re.IGNORECASE | re.MULTILINE):
            result["has_error"] = True
            result["test_failure"] = True
            result["matched_patterns"].append(f"test: {pattern}")
            break  # One match is enough per category

    # Check for build errors
    for pattern in BUILD_ERROR_PATTERNS:
        if re.search(pattern, output, re.IGNORECASE | re.MULTILINE):
            result["has_error"] = True
            result["build_error"] = True
            result["matched_patterns"].append(f"build: {pattern}")
            break

    # Check for runtime errors
    for pattern in RUNTIME_ERROR_PATTERNS:
        if re.search(pattern, output, re.IGNORECASE | re.MULTILINE):
            result["has_error"] = True
            result["runtime_error"] = True
            result["matched_patterns"].append(f"runtime: {pattern}")
            break

    return result


def format_suggestion(error_info: dict) -> str:
    """Format the skill suggestion based on detected errors."""
    if not error_info["has_error"]:
        return ""

    lines = [
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "⚠️  ERROR DETECTED IN OUTPUT",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]

    # Describe what was detected
    error_types = []
    if error_info["test_failure"]:
        error_types.append("Test failure")
    if error_info["build_error"]:
        error_types.append("Build error")
    if error_info["runtime_error"]:
        error_types.append("Runtime error")

    lines.append(f"Detected: {', '.join(error_types)}")
    lines.append("")

    # Suggest skills
    lines.append("📚 RECOMMENDED SKILLS:")
    lines.append("  ⚡ systematic-debugging (investigate root cause FIRST)")

    if error_info["test_failure"]:
        lines.append("  ⚡ testing-anti-patterns (avoid common testing mistakes)")

    lines.extend([
        "",
        "⛔ DO NOT attempt quick fixes without investigation!",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    ])

    return "\n".join(lines)


def main():
    """Main entry point."""
    try:
        # Read JSON input from stdin
        input_data = sys.stdin.read()
        if not input_data.strip():
            sys.exit(0)

        payload = json.loads(input_data)

        # PostToolUse provides tool_name and tool_output
        tool_name = payload.get("tool_name", "")
        tool_output = payload.get("tool_output", "")

        # Only process Bash tool output
        if tool_name != "Bash":
            sys.exit(0)

        # Skip if no output
        if not tool_output:
            sys.exit(0)

        # Detect errors in output
        error_info = detect_error_type(tool_output)

        # Output suggestion if errors found
        if error_info["has_error"]:
            suggestion = format_suggestion(error_info)
            print(suggestion)

    except json.JSONDecodeError:
        pass
    except Exception:
        pass

    # Always exit 0 (non-blocking)
    sys.exit(0)


if __name__ == "__main__":
    main()
