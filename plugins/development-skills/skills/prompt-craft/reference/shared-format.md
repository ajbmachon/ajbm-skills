# Technique File Standard Format

Standard section order for core technique reference files. When writing new technique files, follow this structure.

## Required Sections (in order)

1. **Title + one-line description** -- What the technique does
2. **Mechanism** -- Why it works (2-3 sentences, cite research if available)
3. **When NOT to Use** -- Including reasoning model warnings where applicable
4. **Deep Example** -- One substantial example showing the technique applied well
5. **Model-Specific Notes** -- Table of per-model behavior
6. **Impact Footer** -- Impact metric, cost, best-for (3 lines)

## Sections Removed During Compression

- Table of Contents (navigable at file level)
- "Mechanism in one sentence" (restates title)
- Shallow examples (paradoxical interference -- showing bad examples primes bad output)
- Self-Check checklists (redundant with skill's Quality Gate)
- Multiple Patterns sections (keep only the best one)
- Common Mistakes (listing mistakes primes them via paradoxical interference)
- Variants (unless containing unique, non-obvious content)
