# Extract workflow

Step-by-step execution flow for content-adaptive wisdom extraction from any content source.

## Input sources

| Source | Method |
|--------|--------|
| YouTube URL | Use a transcript tool (e.g., `fabric -y "URL"` if installed, `yt-dlp --write-auto-sub`, or a captioning service) to get the transcript. |
| Article URL | WebFetch to retrieve content. |
| File path | Read the file directly. |
| Pasted text | Use directly from the message. |

If no transcript tool is available for YouTube, ask the user to paste the transcript or provide another content source.

## Execution steps

### Step 1: Get the content

Obtain the full text or transcript. Save to a working file if the content is large enough that repeated reading would be inefficient.

### Step 2: Deep read

Read the entire content. Don't extract yet. Notice:

- What domains of wisdom are present?
- What made you stop and think?
- What's genuinely novel vs. commonly known?
- What would a sharp reader highlight if they were reading this?
- What quotes land perfectly?

### Step 3: Select dynamic sections

Based on the deep read, pick section names according to the chosen depth level. Rules:

- Section names must be conversational, not academic.
- Each section must have at least 3 quality bullets (except Fast, where 3 is the section).
- Always include "Quotes That Hit Different" if the source has quotable moments.
- Always include "First-Time Revelations" if genuinely new ideas exist.
- Be specific — "Agentic Engineering Philosophy," not "Technology Insights."

### Step 4: Extract per section

For each section, extract 3–15 bullets. Apply the tone rules from `SKILL.md`:

- 8–20 words per bullet, flexible for clarity
- Specific details, not vague summaries
- Speaker's words when they're good
- No hedging language
- Every bullet worth telling someone about

### Step 5: Add closing sections

Append according to depth level (see the Phase 4 table in `SKILL.md`):

1. **One-Sentence Takeaway** (15–20 words)
2. **If You Only Have 2 Minutes** (5–7 essential points)
3. **References & Rabbit Holes** (people, projects, books, tools mentioned)
4. **Themes & Connections** (Comprehensive only)

### Step 6: Quality check

Run the quality checklist from `SKILL.md` before delivering.

### Step 7: Output

Present the complete extraction in the format specified in `SKILL.md`.
