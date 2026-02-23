# Multi-Session Persistence

Strategies for long-running agents that span multiple context windows or sessions. The model forgets everything between sessions -- your harness must not.

## Quick Summary

**Impact:** Enables complex tasks that exceed a single context window
**When to use:** Multi-hour tasks, overnight agents, any work spanning multiple sessions
**Mechanism:** Structured state files, git checkpoints, and session startup protocols

## The Core Problem

When a session ends, the model starts fresh. Without persistence, all progress is lost.
**Solution:** Write state to disk. Read state at startup. The filesystem is long-term memory.

## State Tracking with JSON

JSON is more robust than markdown for machine-readable state. Models parse it more reliably.

### progress.json (task-level state)
```json
{
  "goal": "Implement user authentication system",
  "status": "in_progress",
  "completed": ["database schema", "password hashing", "login endpoint"],
  "current": "registration endpoint",
  "blocked": [],
  "decisions": ["bcrypt over argon2 (library support)", "JWT 24h + refresh 7d"],
  "next": ["registration with email verify", "password reset", "session middleware"]
}
```

### features.json (feature-level tracking)
```json
{
  "features": [
    {"name": "login", "status": "done", "tests": "passing"},
    {"name": "registration", "status": "in_progress", "tests": "3/5 passing"},
    {"name": "password_reset", "status": "not_started", "tests": "none"}
  ]
}
```

## Git Checkpoints as Rollback Points

```
"After completing each feature, commit with a descriptive message.
If an approach is wrong, revert to the last good commit rather
than trying to untangle broken code."
```

**Checkpoint rhythm:** Commit after every green test suite, not after every file change.

## Session Startup Checklist

Every new session should begin with orientation:

```
At the start of every session, before doing ANY work:
1. Run `pwd` to confirm working directory
2. Read progress.json for current task state
3. Read the last 20 lines of activity.log for recent context
4. Run the test suite to verify current state
5. Summarize what you found, then ask for confirmation before proceeding
```

This prevents re-doing completed work or breaking working code.

## Fresh Context vs Degraded Context

**Degraded:** Long session where early messages are compressed, tool outputs stale, working memory cluttered.
**Fresh:** New session that reads state from disk. Clean working memory, full attention budget.

```
Degraded (turn 47):  Half-remembers decisions, mixes up files, subtle errors.
Fresh (turn 1):      Reads progress.json, crisp state, confident decisions.
```

**Rule of thumb:** If the model starts making mistakes it wasn't making earlier, start a fresh session.

## Context Window Awareness Prompting

Tell the model to save state proactively:
```
If approaching your context limit: 1) update progress.json,
2) commit working code, 3) write handoff note to activity.log,
4) tell the user you need a fresh session.
```

## Two-Agent Harness Pattern

```
INITIALIZER (short-lived): reads state, decides next task, writes task.md
WORKER (does the work):    reads task.md, executes, updates progress.json, commits
INITIALIZER runs again  →  reads updated state → assigns next task
```

Both agents always have fresh context. The initializer plans, the worker executes. Neither degrades.

## When to Use

- Tasks taking more than 1-2 hours of agent time
- Overnight or background agent runs
- Projects with many features to implement sequentially
- Any workflow where context degradation causes errors

## When NOT to Use

- Tasks that fit comfortably in a single session
- Quick one-off questions or small fixes
- When human is actively pairing (human provides the continuity)

## Tips

- JSON state files over markdown -- models parse structured data more reliably
- Keep progress.json under 100 lines; archive completed items to a done.json
- Test the startup checklist manually before relying on it in automation
- The two-agent pattern adds complexity; start with single-agent + good state files
- Include a "session_count" field in progress.json to track how many sessions a task has taken

See also: [context-engineering](context-engineering.md) for within-session context management
