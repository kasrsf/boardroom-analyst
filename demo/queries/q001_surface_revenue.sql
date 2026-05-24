select
  month,
  surface,
  net_revenue_millions,
  engaged_users_millions,
  commercial_searches_billions
from ad_revenue_by_surface
order by month, surface
