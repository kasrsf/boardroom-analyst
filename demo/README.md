# Boardroom Analyst Demo

Run the demo builder:

```bash
.venv/bin/python demo/build_demo.py
```

The builder creates:

- `demo/output/boardroom_demo.duckdb`
- `demo/output/datamart_context.json`
- `demo/output/analysis_runs/q001.json`
- `demo/output/reports/boardroom-demo/charts/mrr_by_segment.csv`
- `demo/output/reports/boardroom-demo/analysis_run.json`
- `demo/output/reports/boardroom-demo/brief.md`

The showcase page lives at `demo/showcase/index.html`. The recorded MP4 is
`demo/output/boardroom-analyst-demo.mp4`.

Rebuild the recording:

```bash
bash demo/render_recording.sh
```
