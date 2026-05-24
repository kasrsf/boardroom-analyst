# Boardroom Analyst Demo Script

## Setup

Open the recorded demo or run the local showcase:

```bash
open demo/showcase/index.html
```

Suggested opening line:

> This is Boardroom Analyst, a governed executive analytics skill pack. The
> demo is framed as a CEO review for a visual-discovery commerce business: why
> did ad revenue growth slow, and which monetization surface should leadership
> inspect first? The answer is backed by dbt docs, read-only DuckDB SQL, and
> explicit caveats.

## Scene 1: Product Promise

Say:

> The user asks a CEO question: why did ad revenue growth slow in March? The
> system does not jump straight to a narrative. It first checks whether the
> visual-discovery datamart is documented enough to trust.

## Scene 2: Onboarding

Say:

> The onboarding skill reads dbt artifacts and creates a context file with
> model descriptions, grain, metrics, columns, caveats, and warning levels.

## Scene 3: Query Plan

Say:

> The agent proposes small read-only queries. This is the important governance
> move: every claim is planned against a query ID before the brief is written.

## Scene 4: Evidence

Say:

> The result shows that total ad revenue still grew, but the growth rate slowed.
> Performance Shopping Ads and Visual Search Ads kept expanding, while Brand
> Video Ads declined and absorbed part of that strategic momentum.

## Scene 5: Executive Brief

Say:

> The brief is concise enough for leadership but still auditable. It includes
> SQL, chart sources, row counts, hashes, and caveats.

## Scene 6: Follow-Up

Say:

> The executive can ask a follow-up question without starting over. The answer
> points to the first surface to inspect and keeps the same source query trail.

## Close

Say:

> The pilot ask is simple: connect this to one internal datamart and measure
> whether the generated explanations are trusted by the data owner and useful to
> the stakeholder. The best first pilot would be ad monetization or
> shopping-intent analytics because those are already strategic CEO-level
> operating questions.
