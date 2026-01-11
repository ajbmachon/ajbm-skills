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

Use `AskUserQuestion` tool with 4 questions at a time.

### Early Interview (Challenger Phase)
- Focus on: Viability, alternatives, failure modes
- Tone: Probing, skeptical
- Goal: Validate the idea deserves to be built

### Deep Interview (Partner Phase)
- Focus on: Implementation details, edge cases, integration
- Tone: Thorough, collaborative
- Goal: Capture everything needed to build well

### Late Interview
- Focus on: Verification, gaps, open questions
- Tone: Confirmatory but thorough
- Goal: Ensure nothing is missing

---

## Fewer Questions Toward the End

As the interview progresses:

- You should have fewer questions (convergence)
- Questions should be more specific (refinement)
- It's OK to ask 2-3 questions instead of 4

If you're still generating many broad questions late in the interview, something went wrong earlier.
