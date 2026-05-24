# Boardroom Brief

Run: `boardroom-demo`
Question: Why did net revenue growth slow in March?

## Executive Summary

MRR still grew in March, but the growth rate slowed from +$53K in February to +$5K in March because enterprise contraction offset continued SMB and mid-market expansion.

## Findings

- Total MRR increased from $816K to $821K in March, but monthly growth dropped from +$53K to +$5K. [`q002_growth_waterfall`] Confidence: `high`
  - Caveat: Fixture uses documented recurring revenue only and excludes one-time services.
- Enterprise MRR fell by $17K in March, while mid-market and SMB added $22K combined. [`q001_segment_mrr`] Confidence: `high`
  - Caveat: Segment-level attribution is based on the documented model grain: one row per month and customer segment.

## Charts

- MRR by segment: `charts/mrr_by_segment.csv`
  - Source query: `q001_segment_mrr`
  - Filters: All documented rows in demo fixture
  - Time range: 2026-01 to 2026-03
  - Caveat: Demo data is synthetic.
- Monthly MRR growth: `charts/growth_waterfall.csv`
  - Source query: `q002_growth_waterfall`
  - Filters: All documented rows in demo fixture
  - Time range: 2026-01 to 2026-03
  - Caveat: Demo data is synthetic.

## Caveats

- Demo uses a synthetic SaaS revenue mart.
- The brief does not infer metrics outside documented dbt context.

## SQL Appendix

### `q001_segment_mrr`

```sql
select
  month,
  segment,
  mrr
from mrr_by_month
order by month, segment
```

Rows: `9`; result hash: `1991adb8a4e5a0be53cc73cb73eae45b5ef14d15d356ba3a73f11564f8657649`

### `q002_growth_waterfall`

```sql
with totals as (
  select
    month,
    sum(mrr) as total_mrr
  from mrr_by_month
  group by 1
),
changes as (
  select
    month,
    total_mrr,
    total_mrr - lag(total_mrr) over (order by month) as mrr_change
  from totals
)
select *
from changes
order by month
```

Rows: `3`; result hash: `f72494034f10d50445b1dd32f57fed95101e59762a310c658ba09c2866633fe1`
