#!/usr/bin/env python3
"""
UserPromptSubmit hook for skill auto-suggestion.
Reads user prompt from stdin, matches against skill-rules.json, outputs suggestions.
"""

import json
import re
import sys
from pathlib import Path

# Look for skill-rules.json in the same directory as this script
SCRIPT_DIR = Path(__file__).parent
RULES_FILE = SCRIPT_DIR / "skill-rules.json"

# Priority ordering for output
PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def load_rules() -> dict:
    """Load skill-rules.json configuration."""
    if not RULES_FILE.exists():
        return {"version": "1.0", "skills": {}}

    with open(RULES_FILE, "r") as f:
        return json.load(f)


def match_keywords(prompt: str, keywords: list[str]) -> bool:
    """Check if any keyword appears in the prompt (case-insensitive)."""
    prompt_lower = prompt.lower()
    return any(kw.lower() in prompt_lower for kw in keywords)


def match_patterns(prompt: str, patterns: list[str]) -> bool:
    """Check if any regex pattern matches the prompt (case-insensitive)."""
    for pattern in patterns:
        try:
            if re.search(pattern, prompt, re.IGNORECASE):
                return True
        except re.error:
            # Skip invalid regex patterns
            continue
    return False


def find_matching_skills(prompt: str, rules: dict) -> list[tuple[str, str]]:
    """
    Find all skills that match the prompt.
    Returns list of (skill_name, priority) tuples.
    """
    matches = []

    for skill_name, skill_config in rules.get("skills", {}).items():
        # Only check skills with enforcement="suggest"
        if skill_config.get("enforcement") != "suggest":
            continue

        triggers = skill_config.get("promptTriggers", {})
        keywords = triggers.get("keywords", [])
        patterns = triggers.get("intentPatterns", [])

        # Check for matches
        if match_keywords(prompt, keywords) or match_patterns(prompt, patterns):
            priority = skill_config.get("priority", "medium")
            matches.append((skill_name, priority))

    return matches


def format_output(matches: list[tuple[str, str]]) -> str:
    """Format matched skills for output to stdout."""
    if not matches:
        return ""

    # Sort by priority
    matches.sort(key=lambda x: PRIORITY_ORDER.get(x[1], 99))

    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🎯 SKILL ACTIVATION CHECK",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "📚 RECOMMENDED SKILLS:",
    ]

    for skill_name, priority in matches:
        priority_indicator = "⚡" if priority in ("critical", "high") else "→"
        lines.append(f"  {priority_indicator} {skill_name}")

    lines.extend([
        "",
        "ACTION: Use Skill tool BEFORE responding",
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
        prompt = payload.get("prompt", "")

        if not prompt:
            sys.exit(0)

        # Load rules and find matches
        rules = load_rules()
        matches = find_matching_skills(prompt, rules)

        # Output suggestions (stdout goes to Claude as context)
        output = format_output(matches)
        if output:
            print(output)

    except json.JSONDecodeError:
        # Invalid JSON input - silently exit
        pass
    except Exception:
        # Fail open - don't block on errors
        pass

    # Always exit 0 (non-blocking)
    sys.exit(0)


if __name__ == "__main__":
    main()
