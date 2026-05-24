# Boardroom Analyst

Boardroom Analyst is a governed executive analytics skill pack for local,
dbt-documented DuckDB datamarts.

It gives leaders a way to ask boardroom-level questions such as "Why did growth
slow last month?" or "Which segment is driving churn?" and receive answers that
are grounded in documented metrics, read-only SQL, chart-ready data, and explicit
caveats.

The core idea: **make agentic analytics credible enough for executive review by
forcing every claim to show its work.**

## Demo

<video controls src="demo/output/boardroom-analyst-demo.mp4" title="Boardroom Analyst demo recording"></video>

The recording shows the end-to-end pitch flow: a leadership question, dbt
semantic context, read-only SQL, evidence, an executive brief, and a governed
follow-up answer.

## Why It Exists

Most companies already have useful datamarts, but the last mile from governed
data to executive insight is still slow. Analysts answer recurring leadership
questions manually, dashboards rarely explain the "why", and generic AI tools
can hallucinate metrics or silently use the wrong grain.

Boardroom Analyst packages a safer workflow:

- Use dbt docs as the semantic authority.
- Query local DuckDB data in read-only mode.
- Attach every material claim to source SQL and result hashes.
- Produce an executive brief plus a follow-up query loop.
- Refuse or qualify answers when metric definitions, grain, or joins are missing.

## What Ships

The plugin lives at `plugins/boardroom-analyst` and includes three skills:

- `boardroom-onboarding`: validates dbt artifacts and builds `datamart_context.json`.
- `boardroom-brief`: creates an executive brief with SQL-backed findings, chart data, caveats, and a query appendix.
- `boardroom-query`: answers follow-up executive questions through local read-only DuckDB queries.

It also includes deterministic helper scripts for:

- Parsing dbt `manifest.json`, `catalog.json`, and YAML model metadata.
- Rejecting mutating or multi-statement SQL.
- Running local DuckDB queries in read-only mode.
- Exporting chart-ready CSV data.
- Writing `brief.md` and `analysis_run.json`.

## Requirements

- Python 3.11+
- `uv`
- A DuckDB database file
- dbt-compatible documentation:
  - Required: `target/manifest.json`
  - Recommended: `target/catalog.json`
  - Recommended: model YAML docs with metric, grain, caveat, join, and priority-question metadata

## Setup

Create the Python environment with `uv`:

```bash
uv venv --python python3
uv pip install -e ".[dev]"
```

Run the test suite:

```bash
.venv/bin/python -m pytest
```

Validate the plugin:

```bash
python3 /Users/kasra/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/boardroom-analyst
```

Validate individual skills:

```bash
python3 /Users/kasra/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/boardroom-analyst/skills/boardroom-onboarding
python3 /Users/kasra/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/boardroom-analyst/skills/boardroom-brief
python3 /Users/kasra/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/boardroom-analyst/skills/boardroom-query
```

## Usage

Set the plugin root once:

```bash
PLUGIN_ROOT="plugins/boardroom-analyst"
```

### 1. Build Semantic Context

```bash
.venv/bin/python "$PLUGIN_ROOT/scripts/build_datamart_context.py" \
  --dbt-project path/to/dbt_project \
  --output datamart_context.json
```

This produces a normalized context file covering documented models, columns,
metrics, grain, joins, caveats, priority questions, trust level, and warnings.

### 2. Run a Read-Only Query

```bash
.venv/bin/python "$PLUGIN_ROOT/scripts/run_duckdb_query.py" \
  --database path/to/warehouse.duckdb \
  --query-id q001 \
  --sql "select segment, sum(mrr) as mrr from mrr_by_month group by 1 order by 1" \
  --output analysis_runs/q001.json
```

The SQL guard rejects writes, extension loading, database attachment, and
multi-statement SQL before execution.

### 3. Export Chart Data

```bash
.venv/bin/python "$PLUGIN_ROOT/scripts/export_chart_csv.py" \
  --query-result analysis_runs/q001.json \
  --output reports/run_001/charts/mrr_by_segment.csv
```

### 4. Write the Executive Brief

```bash
.venv/bin/python "$PLUGIN_ROOT/scripts/write_insight_brief.py" \
  --run analysis_run.json \
  --output-dir reports/run_001
```

This writes:

- `reports/run_001/brief.md`
- `reports/run_001/analysis_run.json`

## Agent Workflow

Example prompts:

```text
Use $boardroom-onboarding to validate my DuckDB datamart and dbt docs.
```

```text
Use $boardroom-brief to explain why revenue slowed last month using this datamart.
```

```text
Use $boardroom-query to drill into which customer segment drove the change.
```

The intended loop is:

1. Onboard the datamart and produce `datamart_context.json`.
2. Ask an executive question.
3. Let the agent propose a small query plan.
4. Execute read-only DuckDB SQL through the helper script.
5. Generate chart CSVs and a brief.
6. Ask follow-up questions and reuse the same provenance trail.

## Demo And Pitch Materials

This repo includes a manager-ready pitch package:

- `marketing/one-pager.md`: concise product one-pager.
- `marketing/manager-pitch.md`: internal proposal framing.
- `marketing/pitch-deck.md`: slide-by-slide talk track.
- `marketing/demo-script.md`: narration for a live or recorded demo.
- `marketing/faq.md`: likely manager questions and crisp answers.
- `demo/build_demo.py`: builds a complete synthetic demo.
- `demo/showcase/index.html`: browser showcase used for the recording.
- `demo/output/boardroom-analyst-demo.mp4`: short demo recording artifact.

Rebuild the demo:

```bash
.venv/bin/python demo/build_demo.py
```

## Trust Model

Boardroom Analyst is intentionally conservative:

- dbt docs are the authority for metric meaning, table grain, joins, and caveats.
- Undocumented metrics are not invented from column names.
- Every material claim needs a source query ID.
- Every query result records SQL, row count, SQL hash, result hash, and elapsed time.
- Every chart documents source query, filters, time range, and caveats.
- Raw data stays local; the helper scripts do not make network calls.

## Marketplace Status

Included:

- Codex plugin manifest: `plugins/boardroom-analyst/.codex-plugin/plugin.json`
- Claude plugin manifest: `plugins/boardroom-analyst/.claude-plugin/plugin.json`
- Codex marketplace entry: `.agents/plugins/marketplace.json`
- Claude marketplace entry: `.claude-plugin/marketplace.json`
- Release metadata and checksums: `plugins/boardroom-analyst/release.json`

Deferred:

- Hosted marketplace UI
- Checkout and payment processing
- License-key or entitlement checks
- Cloud warehouse connectors
- Interactive dashboard UI

## Development Notes

Useful test commands:

```bash
.venv/bin/python -m pytest tests/test_sql_safety.py
.venv/bin/python -m pytest tests/test_dbt_context.py
.venv/bin/python -m pytest tests/test_duckdb_runner.py
.venv/bin/python -m pytest tests/test_cli_smoke.py
.venv/bin/python -m pytest
```

Generated runtime artifacts such as `reports/`, `datamart_context.json`, and
`analysis_run.json` are ignored by git. Demo outputs under `demo/output` are
kept intentionally because they support the pitch package.
