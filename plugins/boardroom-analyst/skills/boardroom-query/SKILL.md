---
name: boardroom-query
description: Answer executive follow-up questions by running local read-only DuckDB SQL against a dbt-documented datamart, citing query provenance and caveats. Use when the user asks drill-down questions after a Boardroom Analyst brief or wants to query executive metrics interactively.
---

# Boardroom Query

Answer follow-up questions through a local query loop with provenance.

## Workflow

1. Read `datamart_context.json` and the latest `analysis_run.json` when available.
2. Restate the CEO's question as a metric, segment, cohort, or time comparison only if the dbt docs support that interpretation.
3. Generate the smallest read-only SQL query that answers the question. Do not use undocumented joins or inferred metric formulas.
4. Execute with:

```bash
python <plugin-root>/scripts/run_duckdb_query.py --database <warehouse.duckdb> --query-id q_followup_001 --sql-file <query.sql> --output analysis_runs/q_followup_001.json
```

5. Answer in five parts: direct answer, evidence table or chart data, source query, caveats, and suggested next drill-down.

## Guardrails

- Local DuckDB only. Do not send raw data to external services.
- Read-only SQL only; the helper rejects mutating statements and multiple statements.
- If documentation is missing, say what cannot be concluded and what dbt metadata is needed.
- Cite source query IDs for all material claims.

Use `../../references/artifacts.md` when updating an existing run manifest.
