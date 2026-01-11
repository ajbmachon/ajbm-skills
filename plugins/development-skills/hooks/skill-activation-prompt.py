#!/usr/bin/env python3
"""
UserPromptSubmit hook for skill auto-suggestion.
Reads user prompt from stdin, matches against skill-rules.json, outputs suggestions.

v2.0 - Scoring system with multiple match types:
  - strongPhrases: Multi-word exact matches (+15)
  - exactKeywords: Word boundary matching (+10)
  - containsKeywords: Substring matching (+5)
  - intentPatterns: Regex patterns (+8)
  - excludePatterns: Negative patterns (-20)
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

# Scoring weights
SCORE_STRONG_PHRASE = 15
SCORE_EXACT_KEYWORD = 10
SCORE_INTENT_PATTERN = 8
SCORE_CONTAINS_KEYWORD = 5
SCORE_EXCLUDE_PENALTY = -20

# Default threshold
DEFAULT_THRESHOLD = 8


def load_rules() -> dict:
    """Load skill-rules.json configuration."""
    if not RULES_FILE.exists():
        return {"version": "2.0", "skills": {}}

    with open(RULES_FILE, "r") as f:
        return json.load(f)


def score_skill(prompt: str, skill_config: dict) -> float:
    """
    Calculate a confidence score for how well the prompt matches this skill.
    Higher score = stronger match.
    """
    score = 0.0
    prompt_lower = prompt.lower()

    # Strong phrases (highest value) - multi-word exact matches
    for phrase in skill_config.get("strongPhrases", []):
        if phrase.lower() in prompt_lower:
            score += SCORE_STRONG_PHRASE

    # Exact keywords (word boundary matching)
    for kw in skill_config.get("exactKeywords", []):
        try:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, prompt, re.IGNORECASE):
                score += SCORE_EXACT_KEYWORD
        except re.error:
            continue

    # Contains keywords (substring matching - legacy support)
    for kw in skill_config.get("containsKeywords", []):
        if kw.lower() in prompt_lower:
            score += SCORE_CONTAINS_KEYWORD

    # Legacy support: check old "promptTriggers.keywords" format
    triggers = skill_config.get("promptTriggers", {})
    for kw in triggers.get("keywords", []):
        if kw.lower() in prompt_lower:
            score += SCORE_CONTAINS_KEYWORD

    # Intent patterns (regex)
    for pattern in skill_config.get("intentPatterns", []):
        try:
            if re.search(pattern, prompt, re.IGNORECASE):
                score += SCORE_INTENT_PATTERN
        except re.error:
            continue

    # Legacy support: check old "promptTriggers.intentPatterns" format
    for pattern in triggers.get("intentPatterns", []):
        try:
            if re.search(pattern, prompt, re.IGNORECASE):
                score += SCORE_INTENT_PATTERN
        except re.error:
            continue

    # Exclude patterns (negative - prevent false positives)
    for pattern in skill_config.get("excludePatterns", []):
        try:
            if re.search(pattern, prompt, re.IGNORECASE):
                score += SCORE_EXCLUDE_PENALTY
        except re.error:
            continue

    return max(0, score)


def find_matching_skills(prompt: str, rules: dict) -> list[tuple[str, str, float]]:
    """
    Find all skills that match the prompt above their threshold.
    Returns list of (skill_name, priority, score) tuples, sorted by score descending.
    """
    matches = []

    for skill_name, skill_config in rules.get("skills", {}).items():
        # Only check skills with enforcement="suggest"
        if skill_config.get("enforcement") != "suggest":
            continue

        # Calculate score
        score = score_skill(prompt, skill_config)

        # Check against threshold
        threshold = skill_config.get("threshold", DEFAULT_THRESHOLD)
        if score >= threshold:
            priority = skill_config.get("priority", "medium")
            matches.append((skill_name, priority, score))

    # Sort by score (descending), then by priority
    matches.sort(key=lambda x: (-x[2], PRIORITY_ORDER.get(x[1], 99)))

    return matches


def format_output(matches: list[tuple[str, str, float]]) -> str:
    """Format matched skills for output to stdout."""
    if not matches:
        return ""

    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🎯 SKILL ACTIVATION CHECK",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "📚 RECOMMENDED SKILLS:",
    ]

    for skill_name, priority, score in matches:
        priority_indicator = "⚡" if priority in ("critical", "high") else "→"
        lines.append(f"  {priority_indicator} {skill_name} (score: {int(score)})")

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
