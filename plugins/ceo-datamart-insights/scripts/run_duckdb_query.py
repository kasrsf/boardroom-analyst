#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from ceo_datamart_insights.duckdb_runner import execute_read_only_query, write_query_result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one read-only DuckDB query with provenance.")
    parser.add_argument("--database", required=True, help="Path to DuckDB database.")
    parser.add_argument("--sql", help="SQL string. Mutually exclusive with --sql-file.")
    parser.add_argument("--sql-file", help="Path to a SQL file. Mutually exclusive with --sql.")
    parser.add_argument("--query-id", help="Stable query ID for provenance.")
    parser.add_argument("--output", required=True, help="Output query result JSON path.")
    parser.add_argument("--max-rows", type=int, default=500, help="Maximum rows to store.")
    args = parser.parse_args()

    if bool(args.sql) == bool(args.sql_file):
        parser.error("Provide exactly one of --sql or --sql-file.")

    sql = args.sql if args.sql else open(args.sql_file, encoding="utf-8").read()
    result = execute_read_only_query(
        args.database,
        sql,
        query_id=args.query_id,
        max_rows=args.max_rows,
    )
    output = write_query_result(result, args.output)
    print(json.dumps({"output": str(output), "query_id": result["query_id"], "row_count": result["row_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
