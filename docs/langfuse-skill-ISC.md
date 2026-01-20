# Langfuse Skill - Ideal State Criteria (ISC)

**Request:** Design a Langfuse skill for Claude Code that enables AI developers to analyze traces, design evaluations, and iterate on AI applications.

**Effort:** THOROUGH | **Created:** 2026-01-20 | **Source:** Interview + Council Debate

---

## ISC Table

| # | What Ideal Looks Like | Source | Category | Status |
|---|----------------------|--------|----------|--------|
| **SKILL STRUCTURE** |||||
| 1 | SKILL.md exists at `langfuse/SKILL.md` | H8 | Structure | PENDING |
| 2 | SKILL.md under 200 lines (routing table only) | Council | Structure | PENDING |
| 3 | SKILL.md has description under 1024 chars with triggers | H8 | Structure | PENDING |
| 4 | SKILL.md triggers on: langfuse, traces, spans, generations, evals, scores, datasets, experiments | D13 | Structure | PENDING |
| 5 | Directory structure: SKILL.md + scripts/ + references/ + lib/ | H8, Council | Structure | PENDING |
| 6 | No nested reference files (one level deep only) | H8 | Structure | PENDING |
| **ENTRY POINT** |||||
| 7 | Single entry point: `scripts/langfuse.py` | Council | Entry | PENDING |
| 8 | Entry point uses Python only (no JS/TS) | H1 | Entry | PENDING |
| 9 | Entry point has subcommands: trace, evaluate, experiment, setup | Council | Entry | PENDING |
| 10 | Entry point reads auth from .env (LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_BASE_URL) | H9, D19 | Entry | PENDING |
| 11 | Entry point validates auth before operations (auth_check pattern) | D14 | Entry | PENDING |
| 12 | Entry point shows progress for operations >5 seconds | D12, Council | Entry | PENDING |
| 13 | Entry point outputs insight-first with evidence | D12 | Entry | PENDING |
| **TRACE SUBCOMMAND** |||||
| 14 | `trace list` - fetches recent traces with filters | D10, D16 | Trace | PENDING |
| 15 | `trace get <id>` - fetches single trace with observations | D10, D16 | Trace | PENDING |
| 16 | `trace analyze <id>` - analyzes latency, finds bottlenecks | D10, D16 | Trace | PENDING |
| 17 | `trace errors` - finds traces with errors | D10, D16 | Trace | PENDING |
| 18 | `trace costs` - shows cost breakdown | D10, D16 | Trace | PENDING |
| 19 | Trace commands use v2 Observations API with pagination | Research | Trace | PENDING |
| 20 | Trace output shows hierarchy: Session → Trace → Observations | Research | Trace | PENDING |
| 21 | Trace analysis presents findings first, then data | D12 | Trace | PENDING |
| **EVALUATE SUBCOMMAND** |||||
| 22 | `evaluate design` - helps design evaluation strategy | D10 | Evaluate | PENDING |
| 23 | `evaluate score <trace_id>` - creates score on trace | D10, D16 | Evaluate | PENDING |
| 24 | `evaluate scores` - lists scores for project | D10, D16 | Evaluate | PENDING |
| 25 | Supports all score types: NUMERIC, CATEGORICAL, BOOLEAN | Research | Evaluate | PENDING |
| 26 | Explains LLM-as-Judge concept when relevant (context-aware education) | D15 | Evaluate | PENDING |
| 27 | Explains annotation queues when relevant | D15 | Evaluate | PENDING |
| 28 | Uses analogies for non-experts: "Think of it like unit tests for AI responses" | D15 | Evaluate | PENDING |
| **EXPERIMENT SUBCOMMAND** |||||
| 29 | `experiment create-dataset` - creates dataset | D10, D16 | Experiment | PENDING |
| 30 | `experiment add-item` - adds item to dataset | D10, D16 | Experiment | PENDING |
| 31 | `experiment run` - runs experiment using run_experiment() API | D10, D16, Research | Experiment | PENDING |
| 32 | `experiment compare` - compares experiment runs | D10, D16 | Experiment | PENDING |
| 33 | Explains golden datasets concept when relevant | D15 | Experiment | PENDING |
| 34 | Handles concurrent execution (run_experiment() does this) | Research | Experiment | PENDING |
| **SETUP SUBCOMMAND** |||||
| 35 | `setup check` - verifies auth and connection | D14 | Setup | PENDING |
| 36 | `setup diagnose` - diagnoses common auth issues | D14 | Setup | PENDING |
| 37 | `setup guide` - walks through setup step-by-step | D14, D15 | Setup | PENDING |
| 38 | Setup detects wrong region (EU vs US) | D14 | Setup | PENDING |
| 39 | Setup detects expired/invalid keys | D14 | Setup | PENDING |
| 40 | Setup provides clear next steps on failure | D14 | Setup | PENDING |
| **REFERENCE FILES** |||||
| 41 | `references/getting-started.md` exists | D8 | Refs | PENDING |
| 42 | getting-started.md readable in <2 minutes | D8, Council | Refs | PENDING |
| 43 | getting-started.md covers: auth setup, first trace, three workflows | D8 | Refs | PENDING |
| 44 | `references/traces.md` exists with trace domain deep-dive | D7 | Refs | PENDING |
| 45 | traces.md has TOC (over 100 lines expected) | H8 | Refs | PENDING |
| 46 | traces.md covers: data model, observation types, cost tracking | Research | Refs | PENDING |
| 47 | `references/evals.md` exists with evaluation deep-dive | D7 | Refs | PENDING |
| 48 | evals.md has TOC (over 100 lines expected) | H8 | Refs | PENDING |
| 49 | evals.md covers: score types, LLM-as-Judge, annotation queues | Research | Refs | PENDING |
| 50 | `references/datasets.md` exists with dataset/experiment deep-dive | D7 | Refs | PENDING |
| 51 | datasets.md has TOC (over 100 lines expected) | H8 | Refs | PENDING |
| 52 | datasets.md covers: run_experiment(), golden datasets, linking | Research | Refs | PENDING |
| **SHARED UTILITIES** |||||
| 53 | `lib/langfuse_utils.py` exists with shared primitives | Council | Lib | PENDING |
| 54 | langfuse_utils.py handles client initialization | Council | Lib | PENDING |
| 55 | langfuse_utils.py handles auth loading from .env | H9 | Lib | PENDING |
| 56 | langfuse_utils.py handles pagination (cursor-based) | Research | Lib | PENDING |
| 57 | langfuse_utils.py calls flush() for short-lived operations | Research | Lib | PENDING |
| 58 | langfuse_utils.py has error code constants | Council | Lib | PENDING |
| 59 | langfuse_utils.py has human-readable error messages | Council | Lib | PENDING |
| **ERROR HANDLING** |||||
| 60 | Errors have codes (for Claude to reason) | Council | Errors | PENDING |
| 61 | Errors have diagnosis (for humans to understand) | Council, D14 | Errors | PENDING |
| 62 | Auth errors explain: what failed, why, how to fix | D14 | Errors | PENDING |
| 63 | Network timeouts retry with exponential backoff (3 attempts max) | Council | Errors | PENDING |
| 64 | Rate limits show "wait X seconds" message | Council | Errors | PENDING |
| 65 | No silent failures - fail loud and clear | Council | Errors | PENDING |
| **USER EXPERIENCE** |||||
| 66 | Non-experts can use skill without Langfuse knowledge | H5 | UX | PENDING |
| 67 | Context-aware education: quick inline + offer deep-dive | D15 | UX | PENDING |
| 68 | Progress indicators for operations >5 seconds | Council | UX | PENDING |
| 69 | Output is insight-first: conclusions before evidence | D12 | UX | PENDING |
| 70 | Workflow suggestions are suggestive, not mandatory | D5 | UX | PENDING |
| 71 | Claude acts as expert guide and sparring partner | D2, S3 | UX | PENDING |
| **TESTING & VALIDATION** |||||
| 72 | Scripts have unit tests | D18 | Testing | PENDING |
| 73 | Integration tests verify SDK calls work | D18 | Testing | PENDING |
| 74 | Manual testing with real Langfuse project | D17, D18 | Testing | PENDING |
| 75 | Acceptance criteria checklist exists | D18 | Testing | PENDING |
| 76 | MVP test passes: fetch traces and analyze them | D20 | Testing | PENDING |
| 77 | Tests run with .env in project root | H9, D19 | Testing | PENDING |
| **SUCCESS CRITERIA (from D9)** |||||
| 78 | Claude finds real issues in traces (surfaces problems user didn't see) | D9 | Success | PENDING |
| 79 | User can iterate faster on prompts (test variations without leaving Claude Code) | D9 | Success | PENDING |
| 80 | User understands their AI app better (Claude explains and teaches) | D9 | Success | PENDING |
| **CONSTRAINTS VERIFICATION** |||||
| 81 | Python SDK only - no JS/TS code | H1 | Constraint | PENDING |
| 82 | Uses existing research docs (docs/research/*.md) | H2 | Constraint | PENDING |
| 83 | No MCP server for actions - skill hits API directly | H3 | Constraint | PENDING |
| 84 | Progressive loading architecture | H4 | Constraint | PENDING |
| 85 | Pre-made scripts (not ad-hoc code generation) | H7 | Constraint | PENDING |
| 86 | Follows skill authoring best practices | H8 | Constraint | PENDING |

---

## Summary

- **Total ISC Rows:** 86
- **Categories:** Structure (6), Entry (7), Trace (8), Evaluate (7), Experiment (6), Setup (6), Refs (12), Lib (7), Errors (6), UX (6), Testing (6), Success (3), Constraints (6)
- **Source Distribution:** Interview constraints (H1-H9), Interview decisions (D1-D20), Council consensus, Research docs

## Verification Methods

| Category | Verification Method |
|----------|-------------------|
| Structure | File existence check (ls, glob) |
| Entry | Script execution + output validation |
| Subcommands | Integration test with real Langfuse |
| References | Read + length check + TOC presence |
| Lib | Unit tests |
| Errors | Test with invalid auth, network timeout simulation |
| UX | Manual walkthrough of three workflows |
| Testing | Test suite execution |
| Success | User validation against D9 criteria |
| Constraints | Code review against H1-H9 |
