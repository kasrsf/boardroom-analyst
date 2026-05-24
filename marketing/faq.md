# Boardroom Analyst FAQ

## Is this a dashboard replacement?

No. It complements dashboards by explaining why a metric moved and producing a
reviewable brief. Dashboards remain useful for monitoring and self-serve slicing.

## Why start with DuckDB?

DuckDB keeps the pilot local, fast, and low-risk. It avoids cloud credentials
while proving the governed analyst loop.

## Why use dbt docs?

The agent needs a semantic source of truth. dbt artifacts provide metric
definitions, model descriptions, column docs, grain, caveats, and lineage hooks.

## What prevents hallucinated metrics?

The skills instruct the agent to refuse or qualify claims when metric
definitions, grain, or joins are missing. The helper scripts also require
read-only SQL and preserve query provenance.

## What is the security model?

The demo runtime is local-only. SQL is validated before execution, DuckDB is
opened read-only, and the scripts do not make network calls.

## What would a real pilot need?

One documented datamart, one executive workflow, one data owner, and a review
loop for generated briefs.

## What should we measure?

Measure answer correctness, data-owner trust, stakeholder usefulness, and
analyst time saved on recurring KPI explanations.
