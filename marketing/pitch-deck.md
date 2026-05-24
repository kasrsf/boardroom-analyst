# Boardroom Analyst Pitch Deck

## Slide 1: Title

Boardroom Analyst

Governed executive analytics from documented datamarts.

Talk track: We are not pitching another dashboard. We are pitching a safe way
for executives to ask why a metric moved and get a reviewable answer.

Demo framing: use a Pinterest-style Bill Ready question around ad revenue,
shopping intent, visual search, and performance advertising.

## Slide 2: The Problem

Dashboards answer "what changed." Leaders ask "why did it change?"

Proof points:
- Analysts repeatedly explain the same KPI movements.
- Dashboard exports lose semantic context.
- Generic AI can hallucinate metric definitions.

## Slide 3: The Insight

The governed datamart already contains the trust layer. We need to make it
agent-readable and force the agent to show its work.

## Slide 4: Product Concept

Boardroom Analyst reads dbt docs, runs local read-only DuckDB SQL, and produces
an executive brief with query IDs, chart data, result hashes, and caveats.

For the showcase, the mart is a synthetic Pinterest-style model:
`ad_revenue_by_surface`, with Performance Shopping Ads, Visual Search Ads, and
Brand Video Ads.

## Slide 5: Demo Flow

1. Onboard dbt + DuckDB.
2. Ask why ad revenue growth slowed.
3. Run read-only SQL.
4. Generate the brief.
5. Ask which monetization surface Bill should ask the ads team about first.

## Slide 6: Governance Model

Trust gates:
- dbt docs are the authority.
- No mutating SQL.
- Every claim cites a query.
- Missing metadata becomes a caveat or refusal.

## Slide 7: Why This Is A Good Internal Build

It uses our existing data modeling investment, starts with a contained local
runtime, and creates a reusable pattern for packaged agent skills.

The Pinterest-style demo makes the business value concrete: a CEO can see
whether growth is coming from strategic shopping-intent surfaces or being
dragged by a weaker advertising surface, without accepting unsupported agent
narrative.

## Slide 8: Pilot Ask

Approve one datamart, one recurring executive question, one data owner, and a
two-week pilot focused on answer quality and analyst time saved.
