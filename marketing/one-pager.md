# Boardroom Analyst One-Pager

## Positioning

Boardroom Analyst is a governed executive analytics skill pack that turns a
documented DuckDB datamart into boardroom-ready answers with traceable SQL,
chart-ready data, and explicit caveats.

## Audience

Internal leadership teams, data teams, and operating executives who already have
dbt-modeled business data but still rely on analysts to manually explain every
KPI movement.

## Problem

Dashboards show what changed, but executives ask why. Generic AI tools can draft
plausible narratives, but they are risky around business metrics because they
may infer definitions, use the wrong grain, or skip caveats.

## Solution

Boardroom Analyst packages a safer agent workflow:

- Reads dbt artifacts to understand metric definitions, model grain, and caveats.
- Runs local DuckDB queries in read-only mode.
- Produces executive briefs where every claim cites a source query.
- Exports chart-ready data and stores result hashes for review.
- Handles follow-up questions without losing provenance.

## Why Now

Frontier models are good enough to reason over data semantics, but executive
analytics needs guardrails. The winning internal product is not "AI charts"; it
is a governed analyst loop that turns trusted datamarts into trusted decisions.

## Internal Value

- Faster recurring executive readouts.
- Lower analyst toil on first-pass KPI explanations.
- Better governance than ad hoc spreadsheet exports.
- A reusable pattern for future agent skills and marketplace distribution.

## Demo Promise

In three minutes, a manager can see:

1. A documented datamart is onboarded.
2. The agent answers why growth slowed.
3. The answer includes SQL, chart data, hashes, and caveats.
4. A follow-up question reuses the same governed context.

## Suggested Ask

Approve a short internal pilot with one real DuckDB/dbt datamart, one executive
use case, and two success measures: answer quality accepted by the data owner,
and analyst time saved on recurring leadership questions.
