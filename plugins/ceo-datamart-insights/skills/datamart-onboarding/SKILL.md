---
name: datamart-onboarding
description: Validate a local DuckDB database and dbt artifacts, then build datamart_context.json for trusted CEO analysis. Use when the user connects a DuckDB datamart, dbt project, manifest.json, catalog.json, or asks whether their data mart is ready for executive insight.
---

# Datamart Onboarding

Build the semantic context before answering business questions.

## Workflow

1. Locate the DuckDB database and dbt project directory. Require `target/manifest.json`; use `target/catalog.json` and dbt YAML docs when present.
2. Run the context builder from this skill pack:

```bash
python <plugin-root>/scripts/build_datamart_context.py --dbt-project <dbt-project> --output datamart_context.json
```

3. Check the database can be opened read-only:

```bash
python <plugin-root>/scripts/run_duckdb_query.py --database <warehouse.duckdb> --query-id q_healthcheck --sql "select 1 as ok" --output analysis_runs/q_healthcheck.json
```

4. Read `datamart_context.json`. Report table coverage, documented metrics, warning count, and any low-trust tables.
5. Do not produce CEO findings yet if context has warnings about missing metric definitions, missing grain, or undocumented joins. Explain what documentation is missing.

## Trust Rules

- Treat dbt docs as the authority for metric meaning, table grain, joins, and caveats.
- If a table or metric is undocumented, label it low trust instead of inferring semantics from names.
- Every later claim must cite a source query or provenance entry.

For artifact fields and refusal behavior, read `../../references/artifacts.md` and `../../references/trust-policy.md` when needed.
