# Boardroom Brief

Run: `boardroom-demo`
Question: Bill Ready asks: why did ad revenue growth slow in March?

## Executive Summary

Synthetic Pinterest-style ad revenue still grew in March, but the growth rate slowed from +$69M in February to +$48M in March because Brand Video Ads swung from +$7M growth to a -$14M decline while shopping and visual search kept expanding.

## Findings

- Total ad revenue increased from $925M to $973M in March, but monthly growth slowed from +$69M to +$48M. [`q002_revenue_growth_waterfall`] Confidence: `high`
  - Caveat: Fixture is synthetic and should not be read as Pinterest reported results.
- Brand Video Ads declined by $14M in March, offsetting a combined +$62M from Performance Shopping Ads and Visual Search Ads. [`q001_surface_revenue`] Confidence: `high`
  - Caveat: Surface attribution is based on the documented model grain: one row per month and monetization surface.
- Shopping-intent surfaces remained the strategic bright spot: Performance Shopping Ads added $39M and Visual Search Ads added $23M in March. [`q001_surface_revenue`] Confidence: `high`
  - Caveat: Commercial search and engaged-user fields are synthetic proxies for demo purposes.

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

- Demo uses synthetic Pinterest-style advertising and engagement data.
- The fixture is tailored for an internal pitch to Bill Ready and is not Pinterest reported data.
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
