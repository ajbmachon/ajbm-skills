# Skill Triggers Reference

Complete guide for configuring skill auto-activation in Claude Code.

## Table of Contents

- [Two-Hook Architecture](#two-hook-architecture)
- [Skill Types](#skill-types)
- [Trigger Types](#trigger-types)
- [skill-rules.json Schema](#skill-rulesjson-schema)
- [Enforcement Levels](#enforcement-levels)
- [Skip Conditions](#skip-conditions)
- [Testing Triggers](#testing-triggers)

---

## Two-Hook Architecture

### UserPromptSubmit Hook (Proactive Suggestions)

- **File**: `.claude/hooks/skill-activation-prompt.ts`
- **Trigger**: BEFORE Claude sees user's prompt
- **Purpose**: Suggest relevant skills based on keywords + intent patterns
- **Method**: Injects formatted reminder as context
- **Use Cases**: Topic-based skills, implicit work detection

### PreToolUse Hook (Blocking Guardrails)

- **Trigger**: BEFORE tool execution (Edit, Write, etc.)
- **Purpose**: Block operations until skill is used
- **Method**: Exit code 2 sends stderr to Claude
- **Use Cases**: Critical mistakes prevention, data integrity

**Philosophy:** Use gentle post-response reminders where possible. Reserve blocking for critical guardrails only.

### Configuration File

**Location**: `.claude/skills/skill-rules.json`

Defines all skills, trigger conditions, enforcement levels, and skip conditions.

---

## Skill Types

### Guardrail Skills

**Purpose:** Enforce critical best practices that prevent errors

**Characteristics:**
- Type: `"guardrail"`
- Enforcement: `"block"`
- Priority: `"critical"` or `"high"`
- Block file edits until skill used
- Session-aware (don't repeat in same session)

**When to Use:**
- Mistakes that cause runtime errors
- Data integrity concerns
- Critical compatibility issues

### Domain Skills

**Purpose:** Provide comprehensive guidance for specific areas

**Characteristics:**
- Type: `"domain"`
- Enforcement: `"suggest"`
- Priority: `"high"` or `"medium"`
- Advisory, not mandatory
- Topic or domain-specific

**When to Use:**
- Complex systems requiring deep knowledge
- Best practices documentation
- Architectural patterns, how-to guides

---

## Trigger Types

### Keyword Triggers (Explicit)

Case-insensitive substring matching in user's prompt.

```json
"promptTriggers": {
  "keywords": ["layout", "grid", "toolbar", "submission"]
}
```

**Best Practices:**
- Use specific, unambiguous terms
- Include common variations
- Avoid overly generic words ("system", "work", "create")

### Intent Pattern Triggers (Implicit)

Regex pattern matching to detect user's intent.

```json
"promptTriggers": {
  "intentPatterns": [
    "(create|add|implement).*?(feature|endpoint)",
    "(how does|explain).*?(layout|workflow)"
  ]
}
```

**Best Practices:**
- Use non-greedy matching: `.*?` instead of `.*`
- Capture common action verbs: `(create|add|modify|build|implement)`
- Test at https://regex101.com/
- Don't make patterns too broad (false positives) or too specific (false negatives)

### File Path Triggers

Glob pattern matching against file paths being edited.

```json
"fileTriggers": {
  "pathPatterns": [
    "frontend/src/**/*.tsx",
    "form/src/**/*.ts"
  ],
  "pathExclusions": [
    "**/*.test.ts",
    "**/*.spec.ts"
  ]
}
```

**Glob Syntax:**
- `**` = Any number of directories (including zero)
- `*` = Any characters within a directory name
- Example: `frontend/src/**/*.tsx` = All .tsx files in frontend/src and subdirs

### Content Pattern Triggers

Regex pattern matching against file content.

```json
"fileTriggers": {
  "contentPatterns": [
    "import.*[Pp]risma",
    "PrismaService",
    "\\.findMany\\("
  ]
}
```

**Best Practices:**
- Match imports: `import.*[Pp]risma`
- Escape special regex chars: `\\.findMany\\(`
- Test against real file content

---

## skill-rules.json Schema

### Complete TypeScript Schema

```typescript
interface SkillRules {
    version: string;
    skills: Record<string, SkillRule>;
}

interface SkillRule {
    type: 'guardrail' | 'domain';
    enforcement: 'block' | 'suggest' | 'warn';
    priority: 'critical' | 'high' | 'medium' | 'low';

    promptTriggers?: {
        keywords?: string[];
        intentPatterns?: string[];  // Regex strings
    };

    fileTriggers?: {
        pathPatterns: string[];     // Glob patterns
        pathExclusions?: string[];  // Glob patterns
        contentPatterns?: string[]; // Regex strings
        createOnly?: boolean;       // Only trigger on file creation
    };

    blockMessage?: string;  // For guardrails, {file_path} placeholder

    skipConditions?: {
        sessionSkillUsed?: boolean;      // Skip if used in session
        fileMarkers?: string[];          // e.g., ["@skip-validation"]
        envOverride?: string;            // e.g., "SKIP_DB_VERIFICATION"
    };
}
```

### Example: Guardrail Skill

```json
{
  "database-verification": {
    "type": "guardrail",
    "enforcement": "block",
    "priority": "critical",

    "promptTriggers": {
      "keywords": ["prisma", "database", "table", "column", "schema"],
      "intentPatterns": [
        "(add|create|implement).*?(user|login|auth|feature)",
        "(modify|update|change).*?(table|column|schema)"
      ]
    },

    "fileTriggers": {
      "pathPatterns": [
        "**/schema.prisma",
        "database/src/**/*.ts",
        "form/src/**/*.ts"
      ],
      "pathExclusions": ["**/*.test.ts"],
      "contentPatterns": [
        "import.*[Pp]risma",
        "PrismaService",
        "\\.findMany\\("
      ]
    },

    "blockMessage": "BLOCKED - Database Operation Detected\n\nREQUIRED: Use Skill tool 'database-verification'\nFile: {file_path}",

    "skipConditions": {
      "sessionSkillUsed": true,
      "fileMarkers": ["@skip-validation"],
      "envOverride": "SKIP_DB_VERIFICATION"
    }
  }
}
```

### Example: Domain Skill

```json
{
  "frontend-dev-guidelines": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",

    "promptTriggers": {
      "keywords": ["react", "component", "frontend", "UI"],
      "intentPatterns": [
        "(create|add|make|build).*?(component|UI|page|modal)"
      ]
    },

    "fileTriggers": {
      "pathPatterns": ["frontend/src/**/*.tsx"],
      "pathExclusions": ["**/*.test.tsx"]
    }
  }
}
```

---

## Enforcement Levels

### BLOCK (Critical Guardrails)

- Physically prevents Edit/Write tool execution
- Exit code 2 from hook, stderr → Claude
- Claude must use skill to proceed
- **Use For**: Critical mistakes, data integrity, security

### SUGGEST (Recommended)

- Reminder injected before Claude sees prompt
- Claude is aware but not enforced
- **Use For**: Domain guidance, best practices, how-to guides

### WARN (Optional)

- Low priority suggestions
- Advisory only, minimal enforcement
- **Rarely used** - most skills are BLOCK or SUGGEST

---

## Skip Conditions

### Session Tracking

Don't nag repeatedly in same session.

**How it works:**
1. First edit → Hook blocks, updates session state
2. Second edit (same session) → Hook allows
3. Different session → Blocks again

**State File:** `.claude/hooks/state/skills-used-{session_id}.json`

### File Markers

Permanent skip for verified files.

**Marker:** `// @skip-validation`

```typescript
// @skip-validation
import { PrismaService } from './prisma';
// This file has been manually verified
```

**Use sparingly** - defeats the purpose if overused.

### Environment Variables

Emergency disable, temporary override.

```bash
# Global disable
export SKIP_SKILL_GUARDRAILS=true

# Skill-specific
export SKIP_DB_VERIFICATION=true
```

---

## Testing Triggers

### Test UserPromptSubmit

```bash
echo '{"session_id":"test","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

### Test PreToolUse

```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{
  "session_id": "test",
  "tool_name": "Edit",
  "tool_input": {"file_path": "/path/to/test/file.ts"}
}
EOF
```

### Validate JSON

```bash
cat .claude/skills/skill-rules.json | jq .
```

### Validation Checklist

- [ ] JSON syntax valid
- [ ] All skill names match SKILL.md filenames
- [ ] Guardrails have `blockMessage`
- [ ] Block messages use `{file_path}` placeholder
- [ ] Intent patterns are valid regex
- [ ] File path patterns use correct glob syntax
- [ ] Content patterns escape special characters
- [ ] No duplicate skill names

---

**Related:**
- [hook-architecture.md](hook-architecture.md) - Hook internals
- [patterns-library.md](patterns-library.md) - Ready-to-use patterns
- [troubleshooting.md](troubleshooting.md) - Debug issues
