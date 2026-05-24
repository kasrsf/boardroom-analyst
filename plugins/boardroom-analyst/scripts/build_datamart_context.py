#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from boardroom_analyst.dbt_context import build_datamart_context, write_datamart_context


def main() -> int:
    parser = argparse.ArgumentParser(description="Build datamart_context.json from dbt artifacts.")
    parser.add_argument("--dbt-project", required=True, help="Path to the dbt project directory.")
    parser.add_argument("--output", default="datamart_context.json", help="Output JSON path.")
    args = parser.parse_args()

    context = build_datamart_context(args.dbt_project)
    output = write_datamart_context(context, args.output)
    print(json.dumps({"output": str(output), "warnings": len(context["warnings"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
