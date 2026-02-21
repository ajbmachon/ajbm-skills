# Design Review Workflow

Interview type for refining designs — UI/UX, system architecture, service design, or any structured creative output.

---

## Domain-Specific Research (Phase 1)

### BLOCKING Research Targets
- **Design context:** Current design state, design system, component library
- **User research:** Personas, user journeys, pain points
- **Accessibility standards:** WCAG compliance requirements
- **Platform constraints:** Device targets, browser support, performance budgets
- **Competitive designs:** How competitors solve similar problems

---

## Domain-Specific Challenge Angles (Phase 2)

- "Does this design solve the right problem?"
- "What's the simplest version that still works?"
- "What happens on the unhappy path — errors, empty states, edge cases?"
- "Is this accessible to all users?"
- "How does this scale — more content, more users, more complexity?"

---

## Domain-Specific Questions (Phase 3)

### User Experience
- What's the primary user flow?
- What happens when something goes wrong?
- How does a first-time user experience this vs. a power user?
- What's the most complex interaction?

### Visual & Interaction Design
- What design system or component library applies?
- What are the responsive breakpoints?
- What animations or transitions are needed?
- How does state change communicate to the user?

### Integration & Constraints
- What data drives this design?
- What are the performance constraints?
- What backend capabilities does this assume?
- How does this integrate with existing screens/flows?

### Visual Decision Questions

**Heavy use of markdown preview Showpiece questions** for this workflow. When the interview hits a structural fork (layout options, component arrangements, information hierarchy), use AskUserQuestion with markdown previews showing ASCII mockups of each option.

Example: Navigation structure choices, card layouts, form flows, dashboard arrangements.

---

## Domain-Specific Output Additions

### Design Decisions Log

```markdown
## Design Decisions

| Decision | Options Considered | Chosen | Rationale |
|----------|-------------------|--------|-----------|
| [Choice] | [Alternatives] | [Selected] | [Why] |
```

### Iteration Notes

```markdown
## Iteration Notes

### Round [N]
**Focus:** [What was refined]
**Changes:** [What changed and why]
**Open:** [What still needs resolution]
```

### Prototype Specs

```markdown
## Prototype Specification

**Fidelity:** [Wireframe / Low-fi / High-fi / Interactive]
**Key Screens:** [List with purpose]
**Interaction Notes:** [Transitions, animations, states]
**Handoff Format:** [Figma / Code / Annotated screenshots]
```
