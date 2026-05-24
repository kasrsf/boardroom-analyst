# Boardroom Analyst Demo

Run the demo builder:

```bash
.venv/bin/python demo/build_demo.py
```

The builder creates:

- `demo/output/boardroom_demo.duckdb`
- `demo/output/datamart_context.json`
- `demo/output/analysis_runs/q001_surface_revenue.json`
- `demo/output/analysis_runs/q002_revenue_growth_waterfall.json`
- `demo/output/reports/boardroom-demo/charts/revenue_by_surface.csv`
- `demo/output/reports/boardroom-demo/charts/revenue_growth_waterfall.csv`
- `demo/output/reports/boardroom-demo/analysis_run.json`
- `demo/output/reports/boardroom-demo/brief.md`

The fixture uses synthetic Pinterest-style advertising data: Performance
Shopping Ads, Visual Search Ads, Brand Video Ads, engaged users, and
commercial-intent searches. It is designed for a Bill Ready internal pitch and
does not represent Pinterest reported results.

The showcase page lives at `demo/showcase/index.html`. The recorded MP4 is
`demo/output/boardroom-analyst-demo.mp4`.

Rebuild the recording:

```bash
bash demo/render_recording.sh
```
