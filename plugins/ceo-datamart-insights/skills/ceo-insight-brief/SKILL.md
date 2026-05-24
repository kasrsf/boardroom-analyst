---
name: ceo-insight-brief
description: Create a concise CEO insight brief with SQL-backed findings, chart data, query appendix, provenance, and caveats from a dbt-documented DuckDB datamart. Use when the user asks for an executive data brief, business performance diagnosis, KPI explanation, or board-ready insight from a local datamart.
---

# CEO Insight Brief

Produce a trust-first executive memo, not a generic dashboard.

## Inputs

Require:
- DuckDB database path.
- `datamart_context.json`; if missing, run `$datamart-onboarding` first.
- CEO question or decision context.

## Workflow

1. Read `datamart_context.json` and identify documented tables, metric definitions, grain, caveats, and priority questions.
2. Draft a short query plan. Each planned claim must map to one query ID.
3. Execute only read-only SQL:

```bash
python <plugin-root>/scripts/run_duckdb_query.py --database <warehouse.duckdb> --query-id q001 --sql-file <query.sql> --output analysis_runs/q001.json
```

4. For chart-ready tables, export source data with:

```bash
python <plugin-root>/scripts/export_chart_csv.py --query-result analysis_runs/q001.json --output reports/<run-id>/charts/<chart-name>.csv
```

5. Create `analysis_run.json` with question, summary, findings, chart specs, caveats, and query result metadata. Then write the brief:

```bash
python <plugin-root>/scripts/write_insight_brief.py --run analysis_run.json --output-dir reports/<run-id>
```

## Output Requirements

- Start with the ranked answer to the CEO question.
- Every numeric or directional claim must cite a source query like ``[`q001`]``.
- Every chart must include source query, filters, time range, and caveats.
- Include a SQL appendix and result hashes.
- Refuse or qualify conclusions when dbt docs do not define the metric, grain, or join path.

Use `../../references/trust-policy.md` for claim confidence and caveat rules.
