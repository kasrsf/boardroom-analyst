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
