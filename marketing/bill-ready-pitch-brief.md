# Bill Ready Pitch Brief

## Objective

Position Boardroom Analyst as an internal operating system for trusted CEO
analytics at Pinterest: a way for Bill Ready and staff teams to ask why a KPI
moved and receive a concise answer that is grounded in dbt context, read-only
SQL, result hashes, and caveats.

## Why This Should Resonate

Pinterest's public strategy emphasizes AI-powered visual search, commercial
intent, shopping, and performance advertising. That maps naturally to the
Boardroom Analyst trust model because those themes require cross-functional
metric interpretation across users, engagement, shopping behavior, advertisers,
and revenue.

The demo mirrors that strategy with synthetic data:

- `Performance Shopping Ads`
- `Visual Search Ads`
- `Brand Video Ads`
- `engaged_users_millions`
- `commercial_searches_billions`
- `net_revenue_millions`

The sample question is intentionally CEO-level:

> Bill Ready asks: why did ad revenue growth slow in March?

## Funding Angle

This is not another dashboard. It is a governed analyst loop for the moments
when dashboards create follow-up questions:

- What changed?
- Why did it change?
- Which team should inspect it first?
- What caveats should leadership know before acting?

The project should be funded as a two-week internal pilot because it can reuse
existing dbt documentation, run locally on DuckDB, and produce auditable output
without needing a full BI replacement.

## Talk Track

1. Pinterest has a clear strategic arc: visual discovery, shopping intent, and
   performance advertising.
2. Those workflows create nuanced executive questions that dashboards alone do
   not answer.
3. Boardroom Analyst turns the governed datamart into an agent-readable context
   layer.
4. The agent can answer only when metric definitions, grain, SQL, and caveats
   are present.
5. A successful pilot would save analyst time while increasing trust in
   agent-assisted business analysis.

## Public Context Used For Framing

- Pinterest reported Q2 2025 revenue growth and record MAUs, and Bill Ready
  described the company as a personalized shopping destination and AI-powered
  performance platform for advertisers.
- Pinterest's 2026 proxy statement identifies Bill Ready as CEO and director
  since 2022.
- The same proxy letter emphasizes AI-powered visual search, commercial intent,
  moving users from inspiration to action, and performance advertising.

## Caveat For The Demo

All sample data is synthetic. The demo is designed to feel relevant to
Pinterest's business model and leadership priorities, not to reproduce
Pinterest financials or internal metrics.
