# Agent-Skill Composition

When and how skills should invoke subagents.

## Decision Framework

### Skill vs Agent vs Skill+Agent

| Need | Solution | Example |
|------|----------|---------|
| Guidance/workflow | **Skill only** | `prompt-craft` - templates and techniques |
| Autonomous work | **Agent only** | `debugger` - investigates and fixes |
| Guidance + delegation | **Skill + Agent** | `interview` skill invokes `docs-research-specialist` |

### When Skills Should Invoke Agents

**Invoke agents when:**
- Task requires focused, autonomous work
- Context isolation benefits the task
- Specialized tools/permissions needed
- Parallel execution possible

**Keep in skill when:**
- User interaction required
- Single-turn guidance sufficient
- Context sharing critical
- Workflow is linear, not delegable

---

## Composition Patterns

### Pattern 1: Research Delegation

Skill handles user interaction; agent handles research.

**Example:** `interview` skill invokes `docs-research-specialist`

```markdown
# In SKILL.md

## Phase 1: Research Foundation (BLOCKING)

Launch research agent for:
- Technology verification
- Existing solution discovery
- Current best practices

**Wait for results.** Only proceed when you can challenge INTELLIGENTLY.
```

**When to use:**
- Skill needs current information
- Research is blocking (must complete before continuing)
- Results feed into skill workflow

---

### Pattern 2: Background Delegation

Skill continues while agent works asynchronously.

**Example:** `interview` Phase 3+ with background research

```markdown
# In SKILL.md

## Phase 3: Deep Interview

**Research is now BACKGROUND (async):**
- While user answers, launch background agents to verify claims
- Surface findings asynchronously: "While you answered, I researched X..."
```

**When to use:**
- Research is non-blocking
- Multiple parallel investigations possible
- Results enhance but don't gate progress

---

### Pattern 3: Verification Delegation

Skill produces output; agent validates it.

**Example:** Implementation skill invokes `clean-code-reviewer`

```markdown
# In SKILL.md

## Post-Implementation

After code is written:
1. Invoke clean-code-reviewer agent
2. Apply 🟢 SYNTACTIC fixes automatically
3. Present 🟡 SEMANTIC suggestions to user
4. Flag 🔴 ARCHITECTURAL issues for discussion
```

**When to use:**
- Output needs quality check
- Validation requires specialized analysis
- Two-commit workflow (implement → review → fix)

---

### Pattern 4: Specialized Tool Access

Agent has tools the skill shouldn't have.

```markdown
# In agent definition

---
name: deployment-agent
tools: Bash  # Skill doesn't need Bash
---
```

**When to use:**
- Skill is advisory (no write access)
- Dangerous operations need isolation
- Permission escalation for specific tasks

---

## Implementation Guide

### Defining Agent Invocation in Skills

```markdown
# SKILL.md

## Agent Integration

This skill invokes the following agents:

| Phase | Agent | Purpose | Blocking? |
|-------|-------|---------|-----------|
| Research | docs-research-specialist | Verify tech claims | Yes |
| Validation | clean-code-reviewer | Code quality | No |

### Invoking Agents

Use the Task tool with subagent_type matching your agent:

```
Task: "Research current React 19 patterns for [topic]"
subagent_type: docs-research-specialist
```
```

### Agent Coordination

**Sequential (blocking):**
```markdown
1. Invoke Agent A
2. **Wait for results**
3. Use results in next step
4. Invoke Agent B
```

**Parallel (background):**
```markdown
1. Invoke Agents A, B, C in parallel
2. Continue with user interaction
3. Surface results as they arrive
```

### Result Handling

**Blocking results:**
```markdown
Agent returns → Parse findings → Integrate into workflow → Proceed
```

**Background results:**
```markdown
Agent returns → Queue findings → Surface when relevant → "While you answered, I found..."
```

---

## Anti-Patterns

### Over-Delegation

**Bad:** Every task spawns an agent.
**Reality:** Agent startup has overhead. Simple tasks don't need delegation.

### Context Loss

**Bad:** Skill delegates, then ignores agent results.
**Good:** Skill explicitly uses agent findings in subsequent phases.

### Unclear Handoff

**Bad:** "Use the agent to help."
**Good:** "Invoke docs-research-specialist to verify React 19 Server Components patterns. Wait for results before recommending architecture."

### Missing Tool Specification

**Bad:** Agent inherits all tools by default.
**Good:** Agent has minimal tools needed for its task.

---

## Example: Interview Skill Composition

```
interview/
├── SKILL.md                 # User interaction, workflow
├── references/
│   ├── research-protocol.md # When/how to invoke agents
│   └── ...
```

**Composition flow:**
1. User starts interview → Skill handles
2. Need tech research → Invoke `docs-research-specialist` (BLOCKING)
3. Continue interview → Skill handles
4. Verify claims → Invoke research agent (BACKGROUND)
5. Output spec → Skill handles

**Key insight:** The skill orchestrates; agents do focused work.

---

## Checklist: When to Add Agent Invocation

- [ ] Task requires autonomous investigation
- [ ] Work benefits from context isolation
- [ ] Parallel execution would speed up workflow
- [ ] Specialized tools/permissions needed
- [ ] Results integrate back into skill workflow

If 2+ checked, consider agent composition.

---

**Line count:** ~180
**Related:** [sub-agents.md](sub-agents.md), [patterns-library.md](patterns-library.md)
