# Tree of Thoughts

Explore multiple reasoning branches before converging. Best for complex problems with exploration value.

## Quick Summary

**Impact:** +20-50% on exploration tasks
**When to use:** Complex problems, puzzles, multi-path decisions, planning
**Mechanism:** Branch-and-explore reveals paths that linear reasoning misses

## The Pattern

```
Explore this problem using tree of thoughts:

1. Generate 2-3 initial approaches (branches)
2. For each branch, take 1-2 reasoning steps
3. Evaluate: Which branch is most promising?
4. Continue exploring the best branch(es)
5. Backtrack if a branch fails
6. Converge on the best solution
```

## Visualization

```
                    [Problem]
                   /    |    \
             [A]      [B]      [C]
            /  \       |      (pruned)
         [A1]  [A2]   [B1]
                |      |
              (fail)  [B1.1] ← Continue best
                        |
                     [Solution]
```

## Example

### Problem
"How can we reduce customer churn by 20%?"

### Tree of Thoughts Approach
```
BRANCH A: Product improvements
├─ A1: Add requested features → Evaluate: High cost, uncertain impact
└─ A2: Improve onboarding → Evaluate: Promising, test further
   └─ A2.1: Personalized onboarding flow → High potential

BRANCH B: Customer success interventions
├─ B1: Proactive outreach → Evaluate: Promising
└─ B2: Usage monitoring alerts → Evaluate: Low cost, test further
   └─ B2.1: Automated health scores + intervention → High potential

BRANCH C: Pricing changes
└─ C1: Loyalty discounts → Evaluate: Margin risk, may attract wrong customers
   └─ (Pruned - conflict with business model)

CONVERGENCE:
Best paths: A2.1 (personalized onboarding) + B2.1 (health score interventions)
Recommendation: Implement both, starting with B2.1 (lower cost to test)
```

## When to Use

- Problems with multiple valid solution paths
- Puzzles and games
- Strategic planning with branching decisions
- When "first answer" is likely suboptimal
- Research/exploration tasks

## When NOT to Use

- Simple, linear problems
- Speed-critical tasks (exploration takes time)
- Well-defined tasks with obvious approach
- When branches aren't meaningfully different

## Implementation Tips

```
"Before committing to a solution:
1. List 3 different approaches
2. Explore each with 2 steps of reasoning
3. Evaluate which is most promising and why
4. Continue on the best path
5. Note: If you hit a dead end, backtrack to try another branch"
```

## Evaluation Criteria

At each branch point, evaluate on:
- Feasibility: Can this work?
- Progress: Does this move toward the goal?
- Cost: Resources required to continue
- Risk: What could go wrong?

## Compared to Other Techniques

| Technique | Structure | Best For |
|-----------|-----------|----------|
| Chain-of-Thought | Linear | Step-by-step reasoning |
| Self-Consistency | Multiple linear | Verification |
| Tree of Thoughts | Branching | Exploration |

Tree of Thoughts is most valuable when the problem space genuinely has multiple viable paths worth exploring.
