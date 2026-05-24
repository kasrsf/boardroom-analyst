# Runtime Artifacts

## `datamart_context.json`

Produced by `scripts/build_datamart_context.py`.

Required fields:
- `version`: pack artifact version.
- `project_name`: dbt project name.
- `tables[]`: documented models with `name`, `schema`, `description`, `grain`, `columns`, `metrics`, `joins`, `priority_questions`, `trust_level`, and `warnings`.
- `metrics[]`: dbt semantic metrics from `manifest.json`.
- `warnings[]`: context-level trust warnings.

## `analysis_run.json`

The agent creates this after running SQL.

Required fields:
- `run_id`: stable run identifier.
- `question`: CEO question.
- `summary`: concise supported answer.
- `findings[]`: `claim`, `query_id`, `confidence`, `caveats`.
- `charts[]`: `title`, `path`, `query_id`, `filters`, `time_range`, `caveats`.
- `queries[]`: query result metadata from `run_duckdb_query.py`.
- `caveats[]`: global limitations.

The report writer stores a copy next to `brief.md`.
