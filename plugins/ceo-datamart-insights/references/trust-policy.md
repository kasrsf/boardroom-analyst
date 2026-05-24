# Trust Policy

Use this policy for every CEO-facing answer.

## Claim Levels

- `high`: metric definition, table grain, filters, and source query are documented and executed.
- `medium`: source query is executed, but caveats materially affect interpretation.
- `low`: useful exploration only; do not present as an executive conclusion.

## Refusal Triggers

Refuse or qualify the answer when:
- The requested metric is not defined in dbt docs or table metadata.
- The necessary join path is not documented.
- Table grain is missing or conflicts with the requested aggregation.
- Query results contradict the documented metric definition.
- The question requires data outside the local DuckDB/datamart.

## CEO Brief Standard

Every material claim needs:
- Source query ID.
- SQL in the appendix.
- Row count and result hash.
- Time range and filters.
- Caveats from dbt docs and observed data coverage.
