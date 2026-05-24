#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export query result rows to chart-ready CSV.")
    parser.add_argument("--query-result", required=True, help="Path to query result JSON.")
    parser.add_argument("--output", required=True, help="CSV output path.")
    args = parser.parse_args()

    query_result = json.loads(open(args.query_result, encoding="utf-8").read())
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    columns = query_result.get("columns") or []
    rows = query_result.get("rows") or []
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"output": str(output), "query_id": query_result.get("query_id"), "rows": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
