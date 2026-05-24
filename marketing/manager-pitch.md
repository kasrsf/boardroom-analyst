# Internal Proposal: Boardroom Analyst

## Executive Summary

Boardroom Analyst is a prototype for governed agentic analytics. It lets an
executive ask natural-language business questions against a local DuckDB
datamart, while forcing the agent to ground every answer in dbt documentation,
read-only SQL, and auditable artifacts.

The goal is not to replace dashboards or analysts. The goal is to reduce the
manual loop between "the metric moved" and "here is the defensible explanation."

The demo is tailored for an executive review at a visual-discovery commerce
business. It uses synthetic advertising data across Performance Shopping Ads,
Visual Search Ads, and Brand Video Ads to show how a CEO question becomes a
governed answer.

## Why This Is Worth Building Internally

We already invest in semantic data models, metric definitions, and business
reporting. Boardroom Analyst turns that governed layer into an agent-ready
product surface. If it works on a local DuckDB datamart, the pattern can expand
to warehouse connectors, review workflows, and packaged skills for other teams.

## What Makes It Different

- It treats dbt docs as the source of truth.
- It blocks mutating SQL and extension loading.
- It records SQL, row counts, result hashes, and caveats.
- It is packaged as installable skills for Codex and Claude Code.
- It supports follow-up questions without losing provenance.

## Pilot Scope

Recommended pilot:

- One internal dbt-documented datamart.
- One recurring leadership workflow, such as ad revenue movement, shopping funnel quality, or engagement monetization review.
- One data owner validating metric definitions and caveats.
- One executive stakeholder reviewing whether the output is decision-useful.

Out of scope for the pilot:

- Production entitlement enforcement.
- Cloud warehouse connectors.
- Hosted BI dashboard replacement.
- Fully automated board reporting without analyst review.

## Success Criteria

- The generated brief is accepted by the data owner as metric-safe.
- Every material claim maps to SQL and documented context.
- The executive stakeholder can ask at least two follow-up questions without requiring a custom analyst handoff.
- The workflow saves measurable analyst time on a recurring review.

## Risks And Mitigations

- Metric ambiguity: refuse or qualify answers when dbt docs are incomplete.
- Trust gap: include SQL appendix, hashes, caveats, and data-owner review.
- Scope creep: start with DuckDB and one datamart before adding connectors.
- UX overbuild: ship as agent skills first, then decide whether a dashboard is needed.

## Decision Request

Approve a two-week internal pilot to connect Boardroom Analyst to one governed
datamart and evaluate whether it can produce executive-ready, reviewable KPI
explanations.

Recommended first question for the pitch: "The CEO asks why ad revenue growth
slowed in March. Which monetization surface should the ads leadership team
inspect first?"
