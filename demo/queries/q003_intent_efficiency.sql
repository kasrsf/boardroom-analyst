select
  month,
  surface,
  commercial_searches_billions,
  engaged_users_millions,
  commercial_searches_billions * 1000 / engaged_users_millions as commercial_events_per_user,
  net_revenue_millions / engaged_users_millions as revenue_per_engaged_user
from ad_revenue_by_surface
order by month, surface
