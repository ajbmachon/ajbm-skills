# Multi-Session Persistence

Strategies for long-running agents that span multiple context windows. The model forgets everything between sessions -- your harness must not.

## Quick Summary

**Impact:** Enables complex tasks that exceed a single context window
**When to use:** Multi-hour tasks, overnight agents, any work spanning multiple sessions
**Mechanism:** Structured state files, git checkpoints, and session startup protocols

## The Core Problem

When a session ends, the model starts fresh. **Solution:** Write state to disk. Read state at startup.

## State Tracking with JSON

JSON is more robust than markdown for machine-readable state.

```json
{
  "goal": "Implement user authentication system",
  "status": "in_progress",
  "completed": ["database schema", "password hashing", "login endpoint"],
  "current": "registration endpoint",
  "decisions": ["bcrypt over argon2 (library support)", "JWT 24h + refresh 7d"],
  "next": ["registration with email verify", "password reset"]
}
```

## Session Startup Checklist

```
At the start of every session, before doing ANY work:
1. Read progress.json for current task state
2. Read last 20 lines of activity.log for recent context
3. Run the test suite to verify current state
4. Summarize what you found, then ask for confirmation
```

## Fresh Context vs Degraded Context

**Degraded (turn 47):** Half-remembers decisions, mixes up files, subtle errors.
**Fresh (turn 1):** Reads progress.json, crisp state, confident decisions.

**Rule of thumb:** If the model starts making mistakes it wasn't making earlier, start a fresh session.

## Two-Agent Harness Pattern

```
INITIALIZER (short-lived): reads state, decides next task, writes task.md
WORKER (does the work): reads task.md, executes, updates progress.json, commits
INITIALIZER runs again -> reads updated state -> assigns next task
```

Both agents always have fresh context.

## Tips

- JSON state files over markdown
- Keep progress.json under 100 lines
- Commit after every green test suite, not every file change
- Include "session_count" field to track how many sessions a task has taken

See also: [context-engineering](context-engineering.md) for within-session management
