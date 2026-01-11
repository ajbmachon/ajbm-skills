# Patterns Library

Ready-to-use regex and glob patterns for skill triggers. Copy and customize.

## Table of Contents

- [Intent Patterns (Regex)](#intent-patterns-regex)
- [File Path Patterns (Glob)](#file-path-patterns-glob)
- [Content Patterns (Regex)](#content-patterns-regex)
- [Usage Example](#usage-example)
- [Pattern Best Practices](#pattern-best-practices)

---

## Intent Patterns (Regex)

### Feature/Endpoint Creation
```regex
(add|create|implement|build).*?(feature|endpoint|route|service|controller)
```

### Component Creation
```regex
(create|add|make|build).*?(component|UI|page|modal|dialog|form)
```

### Database Work
```regex
(add|create|modify|update).*?(user|table|column|field|schema|migration)
(database|prisma).*?(change|update|query)
```

### Error Handling
```regex
(fix|handle|catch|debug).*?(error|exception|bug)
(add|implement).*?(try|catch|error.*?handling)
```

### Explanation Requests
```regex
(how does|how do|explain|what is|describe|tell me about).*?
```

### Workflow Operations
```regex
(create|add|modify|update).*?(workflow|step|branch|condition)
(debug|troubleshoot|fix).*?workflow
```

### Testing
```regex
(write|create|add).*?(test|spec|unit.*?test)
```

---

## File Path Patterns (Glob)

### Frontend
```glob
frontend/src/**/*.tsx        # All React components
frontend/src/**/*.ts         # All TypeScript files
frontend/src/components/**   # Only components directory
```

### Backend Services
```glob
form/src/**/*.ts            # Form service
email/src/**/*.ts           # Email service
users/src/**/*.ts           # Users service
projects/src/**/*.ts        # Projects service
```

### Database
```glob
**/schema.prisma            # Prisma schema (anywhere)
**/migrations/**/*.sql      # Migration files
database/src/**/*.ts        # Database scripts
```

### Workflows
```glob
form/src/workflow/**/*.ts              # Workflow engine
form/src/workflow-definitions/**/*.json # Workflow definitions
```

### Test Exclusions
```glob
**/*.test.ts                # TypeScript tests
**/*.test.tsx               # React component tests
**/*.spec.ts                # Spec files
```

---

## Content Patterns (Regex)

### Prisma/Database
```regex
import.*[Pp]risma                # Prisma imports
PrismaService                    # PrismaService usage
prisma\.                         # prisma.something
\.findMany\(                     # Prisma query methods
\.create\(
\.update\(
\.delete\(
```

### Controllers/Routes
```regex
export class.*Controller         # Controller classes
router\.                         # Express router
app\.(get|post|put|delete|patch) # Express app routes
```

### Error Handling
```regex
try\s*\{                        # Try blocks
catch\s*\(                      # Catch blocks
throw new                        # Throw statements
```

### React/Components
```regex
export.*React\.FC               # React functional components
export default function.*       # Default function exports
useState|useEffect              # React hooks
```

---

## Usage Example

```json
{
  "my-skill": {
    "promptTriggers": {
      "keywords": ["react", "component", "frontend"],
      "intentPatterns": [
        "(create|add|build).*?(component|UI|page)"
      ]
    },
    "fileTriggers": {
      "pathPatterns": [
        "frontend/src/**/*.tsx"
      ],
      "pathExclusions": [
        "**/*.test.tsx"
      ],
      "contentPatterns": [
        "export.*React\\.FC",
        "useState|useEffect"
      ]
    }
  }
}
```

---

## Pattern Best Practices

### DO
- Use non-greedy matching: `.*?` instead of `.*`
- Escape special regex chars: `\\.findMany\\(`
- Test patterns at https://regex101.com/
- Be specific to avoid false positives
- Include common variations of keywords

### DON'T
- Use overly generic keywords ("system", "work")
- Make patterns too broad (causes false positives)
- Make patterns too specific (causes false negatives)
- Forget to test with real prompts/files

---

**Related:**
- [skill-triggers.md](skill-triggers.md) - Trigger configuration
- [troubleshooting.md](troubleshooting.md) - Debug pattern issues
