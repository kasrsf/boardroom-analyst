from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

import duckdb

from .sql_safety import validate_read_only_sql


def execute_read_only_query(
    database_path: str | Path,
    sql: str,
    *,
    query_id: str | None = None,
    max_rows: int = 500,
) -> dict[str, Any]:
    """Execute one validated read-only query against a DuckDB database."""

    safe_sql = validate_read_only_sql(sql)
    db_path = Path(database_path)
    if not db_path.exists():
        raise FileNotFoundError(f"DuckDB database does not exist: {db_path}")

    start = time.perf_counter()
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        cursor = con.execute(safe_sql)
        columns = [description[0] for description in cursor.description or []]
        raw_rows = cursor.fetchmany(max_rows + 1)
    finally:
        con.close()

    elapsed_ms = round((time.perf_counter() - start) * 1000, 3)
    truncated = len(raw_rows) > max_rows
    raw_rows = raw_rows[:max_rows]
    rows = [dict(zip(columns, row, strict=False)) for row in raw_rows]
    canonical_rows = json.dumps(rows, sort_keys=True, default=str, separators=(",", ":"))
    sql_hash = hashlib.sha256(safe_sql.encode("utf-8")).hexdigest()
    result_hash = hashlib.sha256(canonical_rows.encode("utf-8")).hexdigest()

    return {
        "query_id": query_id or f"q_{sql_hash[:12]}",
        "database": str(db_path),
        "sql": safe_sql,
        "sql_hash": sql_hash,
        "columns": columns,
        "rows": json.loads(json.dumps(rows, default=str)),
        "row_count": len(rows),
        "truncated": truncated,
        "result_hash": result_hash,
        "elapsed_ms": elapsed_ms,
    }


def write_query_result(result: dict[str, Any], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True, default=str), encoding="utf-8")
    return output
