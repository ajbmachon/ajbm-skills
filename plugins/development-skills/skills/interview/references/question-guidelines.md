# Question Guidelines

How to ask questions that surface real insights, not just fill time.

---

## Core Principles

### Think Deeply About THIS Situation

Don't use canned questions. Formulate questions based on:

- What you learned from the user's input
- What you discovered in codebase research
- What assumptions seem shaky
- What could go wrong with THIS specific idea

### Every Question Should Earn Its Place

Before asking, consider:
- Could I answer this myself through research?
- Does this question surface something non-obvious?
- Will the answer change how we build this?

If no to all three → Don't ask it.

---

## What To Do

### Be Challenging

Disagreement is more valuable than agreement. Don't ask questions just to confirm - ask to probe.

```
❌ "So you want to use React for this, right?"
✅ "Why React specifically? Have you considered [alternative] given [your codebase pattern]?"
```

### Quote the Spec/Input

Reference specific parts to prove you read it carefully.

```
✅ "You mentioned 'handling edge cases gracefully' - what does graceful mean here? Silent failure? User notification? Retry?"
```

### Flag Training Assumptions

Be explicit when you're working from general knowledge vs. verified facts.

```
✅ "I'm assuming X based on common patterns - is this correct for your codebase, or do you do it differently?"
```

### Ask Failure Questions

Focus on what could go wrong, not just what should happen.

```
✅ "What would make this fail?"
✅ "How could this break in production?"
✅ "What's the worst case if this doesn't work?"
```

### Surface Uncertainties

State clearly what you don't know.

```
✅ "I'm not sure how this interacts with [system] - can you clarify?"
✅ "I couldn't determine from the codebase whether [X] - what's the current behavior?"
```

### Use Codebase Findings

Incorporate what you discovered in research.

```
✅ "I noticed your project uses [pattern] in [location] - does that apply here?"
✅ "Your codebase has [existing component] - should this integrate with it or be separate?"
```

### Probe Assumptions

Challenge both user's assumptions AND your own.

```
✅ "You seem to be assuming [X] - is that definitely true?"
✅ "I was assuming [Y] but now I'm not sure - can we verify?"
```

---

## What To Avoid

### Obvious Questions

Don't ask what you could find yourself.

```
❌ "What files exist in your project?"
❌ "What framework are you using?"
→ Research this before asking
```

### Generic Questions

Don't use templates that could apply to any project.

```
❌ "What are your requirements?"
❌ "How should this work?"
→ Be specific to THIS situation
```

### Assumption-Based Questions

Don't assume from training data without flagging it.

```
❌ "Since you're using React, you'll want hooks for this..."
✅ "I'm assuming React hooks would work here - but I should verify against current patterns. Is that right?"
```

### Agreement-Seeking Questions

Don't ask just to confirm what you think you know.

```
❌ "So this should be pretty straightforward, right?"
✅ "What's the non-obvious complexity here that I might be missing?"
```

### Filler Questions

Don't pad the interview with low-value questions.

```
❌ "Is there anything else you want to add?"
✅ [Specific follow-up based on what they said]
```

---

## Question Themes

Cover these areas, but craft SPECIFIC questions for THIS project:

### Alternatives
- What else could solve this?
- Why this approach over others?
- What did you consider and reject?

### Failure Modes
- How could this break?
- What makes this fail?
- What's the blast radius if it goes wrong?

### Success Criteria
- How do you know it worked?
- What does "done" look like?
- How will you test this?

### Edge Cases
- What happens when [unusual input]?
- How does this behave under [stress condition]?
- What if [dependency] is unavailable?

### Integration
- How does this interact with [existing system]?
- What needs to change elsewhere?
- Who/what else is affected?

---

## Asking Pattern

Use `AskUserQuestion` tool. Up to 4 questions at a time.

### Question Cadence

| Mode | Questions | When | Format |
|------|-----------|------|--------|
| **Standard** | 2-4 | Normal probing, exploring options | Multiple questions, text descriptions |
| **Showpiece** | 1 | Critical structural fork where text is ambiguous | Single question with `markdown` previews showing each option visually |

**Showpiece questions** are rare (max 3-4 per interview) and powerful. Use them when two reasonable developers could imagine different shapes from the same text description. See **Visual Decision Questions** below.

### Field Usage

| Field | Guidance |
|-------|----------|
| `label` | 1-5 words. The option name the user clicks. |
| `description` | 1-2 sentences. State the benefit or implication of this choice. |
| `header` | Max 12 chars. Short chip label for the question. Examples: "Architecture", "Database", "Auth Model", "Scope". |
| `markdown` | Monospace preview for structural options (Showpiece only). Show ASCII trees, schemas, file layouts. 8-20 lines sweet spot. |

### Phase-Level Cadence

**Early Interview (Challenger Phase)**
- Focus on: Viability, alternatives, failure modes
- Tone: Probing, skeptical
- Goal: Validate the idea deserves to be built
- Questions: Standard only (2-4 questions). **Never use Showpiece** — wrong tempo for rapid challenging.
- Headers: Use descriptive chips — "Viability", "Scope", "Approach"

**Deep Interview (Partner Phase)**
- Focus on: Implementation details, edge cases, integration
- Tone: Thorough, collaborative
- Goal: Capture everything needed to build well
- Questions: Mix of Standard and Showpiece. This is the **primary zone for markdown previews** — architectural forks, data model choices, deployment topology.
- Headers: Use technical chips — "Database", "Auth Flow", "API Design"

**Late Interview**
- Focus on: Verification, gaps, open questions
- Tone: Confirmatory but thorough
- Goal: Ensure nothing is missing
- Questions: Mostly Standard (2-3 questions). Showpiece only for remaining structural forks.
- Headers: Use closing chips — "Confirm", "Gap Check", "Priority"

---

## Visual Decision Questions

Use markdown previews when the interview hits a **structural fork** — a decision where text alone is ambiguous about the shape of the solution.

### The "Two Reasonable Developers" Test

> If two developers could imagine different structures from the same text description, show both structures visually. If the choice is well-known or abstract (e.g., "SQL vs NoSQL"), text is fine.

### When to Use Previews

- **Architecture forks** — monorepo vs multi-repo vs template repo
- **Data model choices** — table schemas, JSON structures, entity relationships
- **API design** — REST resource layout vs GraphQL schema vs RPC
- **Deployment topology** — single server vs distributed vs serverless
- **Assumption surfacing** — when self-challenge catches "I'm assuming X...", show BOTH interpretations so the ambiguity is impossible to miss

### When NOT to Use Previews

- Simple preferences ("TypeScript or Python?")
- Yes/no confirmations
- Challenger phase (Phase 2) — wrong tempo for visual aids
- Multi-select questions — `markdown` previews only work with single-select
- Late verification — unless a genuine structural fork remains

### Constraints

- `markdown` is a **per-option field** on `AskUserQuestion` options (not a top-level field)
- Only works with **single-select** questions (`multiSelect` must be `false` or omitted)
- Content renders in a **monospace preview pane** — use ASCII art, trees, and schemas
- **8-20 lines** is the sweet spot — enough to show structure, short enough to scan
- **Max 3-4 Showpiece questions** per interview to prevent fatigue

### Example 1: Architecture Fork

```json
{
  "questions": [{
    "question": "How should customer codebases be organized?",
    "header": "Architecture",
    "multiSelect": false,
    "options": [
      {
        "label": "Monorepo",
        "description": "All customers share one repo with per-customer config. Simplest CI/CD but couples deployments.",
        "markdown": "repo/\n├── packages/\n│   ├── core/           # shared logic\n│   ├── ui/             # shared components\n│   └── config/         # per-customer\n│       ├── acme.ts\n│       └── globex.ts\n├── apps/\n│   ├── acme/           # customer app\n│   └── globex/         # customer app\n└── turbo.json\n\n+ Pro: Single CI pipeline, easy code sharing\n- Con: One bad deploy affects everyone\n- Con: Repo grows with each customer"
      },
      {
        "label": "Template repo",
        "description": "Generate a fresh repo per customer from a template. Full isolation but harder to push updates.",
        "markdown": "template-repo/        (source of truth)\n├── src/\n├── package.json\n└── .scaffold.yaml\n        ↓ generate\ncustomer-acme/        (standalone repo)\n├── src/\n├── package.json      # frozen at generation\n└── acme.config.ts\n\n+ Pro: Full isolation per customer  <- H1 ✓\n+ Pro: Independent deploy cycles\n- Con: Updates require re-scaffolding\n- Con: Drift between customers over time"
      },
      {
        "label": "Git submodules",
        "description": "Shared core as a submodule pulled into each customer repo. Middle ground with git complexity.",
        "markdown": "shared-core/          (submodule repo)\n├── src/\n└── package.json\n\ncustomer-acme/        (customer repo)\n├── core/ → shared-core  (submodule)\n├── src/\n└── acme.config.ts\n\ncustomer-globex/      (customer repo)\n├── core/ → shared-core  (submodule)\n├── src/\n└── globex.config.ts\n\n+ Pro: Isolation + shared core       <- H1 ✓\n- Con: Git submodule complexity\n- Con: Version pinning overhead"
      }
    ]
  }]
}
```

### Example 2: Data Model Choice

```json
{
  "questions": [{
    "question": "How should permissions be modeled?",
    "header": "Auth Model",
    "multiSelect": false,
    "options": [
      {
        "label": "RBAC tables",
        "description": "Role-based access with SQL tables. Mature pattern, easy to audit, but rigid for fine-grained rules.",
        "markdown": "users\n  id, email, name\n\nroles\n  id, name          # 'admin', 'editor', 'viewer'\n\nuser_roles\n  user_id → users\n  role_id → roles\n\npermissions\n  id, action        # 'read', 'write', 'delete'\n  resource          # 'posts', 'users', 'billing'\n\nrole_permissions\n  role_id → roles\n  permission_id → permissions\n\n+ Pro: SQL joins, easy audit trail\n- Con: New permission = migration"
      },
      {
        "label": "ABAC JSON",
        "description": "Attribute-based policies stored as JSON. Flexible rules but harder to reason about at scale.",
        "markdown": "users\n  id, email, name\n  attributes: jsonb   # {dept: 'eng', level: 3}\n\npolicies\n  id, name\n  effect: 'allow' | 'deny'\n  conditions: jsonb\n  # {\n  #   \"resource\": \"posts\",\n  #   \"action\": \"write\",\n  #   \"when\": {\n  #     \"user.dept\": \"eng\",\n  #     \"user.level\": {\"gte\": 2}\n  #   }\n  # }\n\n+ Pro: No migrations for new rules\n+ Pro: Arbitrary conditions\n- Con: Hard to audit \"who can do what\"\n- Con: Policy debugging is complex"
      }
    ]
  }]
}
```

### Writing Good Previews

1. **Show structure, not prose** — ASCII art, trees, schemas, file layouts
2. **Add tradeoff annotations** — `+ Pro` / `- Con` lines at the bottom
3. **Add constraint annotations** when relevant — `<- H1 ✓` to show which option honors which constraint
4. **Match the user's tech stack** — TypeScript examples for TS users, Python for Python users
5. **Keep scannable** — the user should grasp the difference between options in 3 seconds

---

## Convergence

As the interview progresses, questions should converge:

**Convergence signals** (you're ready for output):
- No new constraints emerged in the last 2 Q&A rounds
- You could write the spec without guessing on any section
- User's answers are getting shorter and more confirmatory
- All hard constraints have been tested against at least one recommendation

**Late interview behavior:**
- Fewer questions (2-3, not 4)
- Questions are more specific (refinement, not exploration)
- Use a final Showpiece question for any remaining structural fork before closing
- If you're still generating many broad questions late in the interview, something went wrong earlier
