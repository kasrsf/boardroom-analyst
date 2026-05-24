#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from ceo_datamart_insights.report_builder import write_insight_brief


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a CEO insight brief from analysis_run.json.")
    parser.add_argument("--run", required=True, help="Path to analysis_run.json.")
    parser.add_argument("--output-dir", required=True, help="Directory for brief.md and analysis_run.json.")
    args = parser.parse_args()

    run = json.loads(open(args.run, encoding="utf-8").read())
    output = write_insight_brief(run, args.output_dir)
    print(json.dumps({"output": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
