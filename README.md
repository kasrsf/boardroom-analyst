# CEO Datamart Insights

CEO Datamart Insights is a premium agent skill pack for turning a local,
dbt-documented DuckDB datamart into trusted executive analysis.

The pack is designed for founders, operators, and CEOs who want direct answers
from a well-documented data mart without turning every question into a custom
analytics project. It prioritizes provenance over polish: every material claim
should trace back to dbt documentation, read-only SQL, row counts, result hashes,
and caveats.

## What It Includes

The marketplace plugin lives at `plugins/ceo-datamart-insights` and ships three
skills:

- `datamart-onboarding`: validates dbt artifacts and builds `datamart_context.json`.
- `ceo-insight-brief`: creates a CEO-facing brief with SQL-backed findings, chart data, caveats, and a query appendix.
- `ceo-query-analyst`: answers follow-up executive questions through a local read-only DuckDB query loop.

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

## Getting Started

Create the Python environment with `uv`:

```bash
uv venv --python python3
uv pip install -e ".[dev]"
```

Run the test suite:

```bash
.venv/bin/python -m pytest
```

Validate the Codex plugin manifest:

```bash
python3 /Users/kasra/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/ceo-datamart-insights
```

Validate individual skill files:

```bash
python3 /Users/kasra/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/ceo-datamart-insights/skills/datamart-onboarding
python3 /Users/kasra/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/ceo-datamart-insights/skills/ceo-insight-brief
python3 /Users/kasra/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/ceo-datamart-insights/skills/ceo-query-analyst
```

## Usage Guide

Set the plugin root once for easier commands:

```bash
PLUGIN_ROOT="plugins/ceo-datamart-insights"
```

### 1. Build Semantic Context

Use this before asking CEO-level business questions:

```bash
.venv/bin/python "$PLUGIN_ROOT/scripts/build_datamart_context.py" \
  --dbt-project path/to/dbt_project \
  --output datamart_context.json
```

The output summarizes documented models, columns, metrics, grain, joins, caveats,
priority questions, trust level, and warnings. If key documentation is missing,
the skills should qualify or refuse unsupported CEO claims.

### 2. Run a Read-Only Query

Run a SQL string:

```bash
.venv/bin/python "$PLUGIN_ROOT/scripts/run_duckdb_query.py" \
  --database path/to/warehouse.duckdb \
  --query-id q001 \
  --sql "select segment, sum(mrr) as mrr from mrr_by_month group by 1 order by 1" \
  --output analysis_runs/q001.json
```

Or run SQL from a file:

```bash
.venv/bin/python "$PLUGIN_ROOT/scripts/run_duckdb_query.py" \
  --database path/to/warehouse.duckdb \
  --query-id q001 \
  --sql-file queries/q001.sql \
  --output analysis_runs/q001.json
```

The SQL guard rejects writes, extension loading, database attachment, and
multi-statement SQL before execution.

### 3. Export Chart Data

The pack exports chart data as CSV so any agent or UI can render it without
re-running the query:

```bash
.venv/bin/python "$PLUGIN_ROOT/scripts/export_chart_csv.py" \
  --query-result analysis_runs/q001.json \
  --output reports/run_001/charts/mrr_by_segment.csv
```

### 4. Write the CEO Brief

Create an `analysis_run.json` that contains the CEO question, summary, findings,
chart specs, query metadata, and caveats. Then render the brief:

```bash
.venv/bin/python "$PLUGIN_ROOT/scripts/write_insight_brief.py" \
  --run analysis_run.json \
  --output-dir reports/run_001
```

This writes:

- `reports/run_001/brief.md`
- `reports/run_001/analysis_run.json`

## Agent Workflow

In Codex or Claude Code, invoke the relevant skill:

```text
Use $datamart-onboarding to validate my DuckDB datamart and dbt docs.
```

```text
Use $ceo-insight-brief to explain why revenue slowed last month using this datamart.
```

```text
Use $ceo-query-analyst to drill into which customer segment drove the change.
```

The intended loop is:

1. Onboard the datamart and produce `datamart_context.json`.
2. Ask a CEO question.
3. Let the agent propose a small query plan.
4. Execute read-only DuckDB SQL through the helper script.
5. Generate chart CSVs and a brief.
6. Ask follow-up questions and reuse the same provenance trail.

## Trust Model

The pack is intentionally conservative:

- dbt docs are the authority for metric meaning, table grain, joins, and caveats.
- Undocumented metrics should not be invented from column names.
- Every material claim needs a source query ID.
- Every query result records SQL, row count, SQL hash, result hash, and elapsed time.
- Every chart should document source query, filters, time range, and caveats.
- Raw data stays local; the helper scripts do not make network calls.

## Marketplace Status

This repository is marketplace-ready but does not enforce payment at runtime.

Included:

- Codex plugin manifest: `plugins/ceo-datamart-insights/.codex-plugin/plugin.json`
- Claude plugin manifest: `plugins/ceo-datamart-insights/.claude-plugin/plugin.json`
- Codex marketplace entry: `.agents/plugins/marketplace.json`
- Claude marketplace entry: `.claude-plugin/marketplace.json`
- Release metadata and checksums: `plugins/ceo-datamart-insights/release.json`

Deferred:

- Hosted marketplace UI
- Checkout and payment processing
- License-key or entitlement checks
- Cloud warehouse connectors
- Interactive dashboard UI

## Development Notes

The synthetic fixture at `fixtures/saas_dbt` is used by the smoke test to verify
the packaged CLI scripts end to end.

Useful test commands:

```bash
.venv/bin/python -m pytest tests/test_sql_safety.py
.venv/bin/python -m pytest tests/test_dbt_context.py
.venv/bin/python -m pytest tests/test_duckdb_runner.py
.venv/bin/python -m pytest tests/test_cli_smoke.py
.venv/bin/python -m pytest
```

Generated runtime artifacts such as `reports/`, `datamart_context.json`, and
`analysis_run.json` are ignored by git.
