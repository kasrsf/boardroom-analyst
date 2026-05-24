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
