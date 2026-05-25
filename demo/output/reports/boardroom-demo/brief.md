# Boardroom Brief

Run: `boardroom-demo`
Question: The CEO asks: why did ad revenue growth slow in March?

## Executive Summary

Synthetic visual-discovery ad revenue still grew in March, but the growth rate slowed from +$69M in February to +$48M in March because Brand Video Ads swung from +$7M growth to a -$14M decline while shopping and visual search kept expanding.

## Findings

- Total ad revenue increased from $925M to $973M in March, but monthly growth slowed from +$69M to +$48M. [`q002_revenue_growth_waterfall`] Confidence: `high`
  - Caveat: Fixture is synthetic and should not be read as reported company results.
- Brand Video Ads declined by $14M in March, offsetting a combined +$62M from Performance Shopping Ads and Visual Search Ads. [`q001_surface_revenue`] Confidence: `high`
  - Caveat: Surface attribution is based on the documented model grain: one row per month and monetization surface.
- Shopping-intent surfaces remained the strategic bright spot: Performance Shopping Ads added $39M and Visual Search Ads added $23M in March. [`q001_surface_revenue`] Confidence: `high`
  - Caveat: Commercial search and engaged-user fields are synthetic proxies for demo purposes.
- Shopping-intent efficiency is highest on Performance Shopping Ads, while Visual Search Ads show intent growth with lower revenue yield. [`q003_intent_efficiency`] Confidence: `medium`
  - Caveat: Revenue per engaged user is a derived sample metric, not a user-level causal analysis.
- Brand Video Ads show the clearest engagement-to-revenue conversion gap in the sample data. [`q004_engagement_conversion`] Confidence: `medium`
  - Caveat: The documented mart does not include advertiser cohorts, auction pressure, or campaign objectives.

## Charts

- Ad revenue by monetization surface: `charts/revenue_by_surface.csv`
  - Source query: `q001_surface_revenue`
  - Filters: All documented rows in demo fixture
  - Time range: 2026-01 to 2026-03
  - Caveat: Demo data is synthetic.
- Monthly ad revenue growth: `charts/revenue_growth_waterfall.csv`
  - Source query: `q002_revenue_growth_waterfall`
  - Filters: All documented rows in demo fixture
  - Time range: 2026-01 to 2026-03
  - Caveat: Demo data is synthetic.

## Caveats

- Demo uses synthetic visual-discovery advertising and engagement data.
- The fixture is tailored for internal product evaluation and is not reported company data.
- The brief does not infer metrics outside documented dbt context.

## SQL Appendix

### `q001_surface_revenue`

```sql
select
  month,
  surface,
  net_revenue_millions,
  engaged_users_millions,
  commercial_searches_billions
from ad_revenue_by_surface
order by month, surface
```

Rows: `9`; result hash: `6c12f54fd683ad7591b5b721f0e9ca933a4150bce253e9d087cfbff6faed03b6`

### `q002_revenue_growth_waterfall`

```sql
with totals as (
  select
    month,
    sum(net_revenue_millions) as total_revenue_millions
  from ad_revenue_by_surface
  group by 1
),
changes as (
  select
    month,
    total_revenue_millions,
    total_revenue_millions - lag(total_revenue_millions) over (order by month) as revenue_change_millions
  from totals
)
select *
from changes
order by month
```

Rows: `3`; result hash: `5b8108f4b3eb2a7d2a50bc7817b0190927884a199e2fbf1e3c1916af55d2cd03`

### `q003_intent_efficiency`

```sql
select
  month,
  surface,
  commercial_searches_billions,
  engaged_users_millions,
  commercial_searches_billions * 1000 / engaged_users_millions as commercial_events_per_user,
  net_revenue_millions / engaged_users_millions as revenue_per_engaged_user
from ad_revenue_by_surface
order by month, surface
```

Rows: `9`; result hash: `106541ee88b0918006743a242ef54f1e67e2e11c930ac10d5623e6b882c1bc3e`

### `q004_engagement_conversion`

```sql
with enriched as (
  select
    month,
    surface,
    net_revenue_millions,
    engaged_users_millions,
    net_revenue_millions / engaged_users_millions as revenue_per_engaged_user
  from ad_revenue_by_surface
)
select *
from enriched
order by month, revenue_per_engaged_user desc
```

Rows: `9`; result hash: `33453aab31d6e92101ab65784df1bb048727cd5f2ecbe5eda0841ed4a68a461f`
