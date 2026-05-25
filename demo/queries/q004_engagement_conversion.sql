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
