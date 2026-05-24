#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SCRIPTS = ROOT / "plugins" / "boardroom-analyst" / "scripts"
sys.path.insert(0, str(PLUGIN_SCRIPTS))

from boardroom_analyst.dbt_context import build_datamart_context, write_datamart_context
from boardroom_analyst.duckdb_runner import execute_read_only_query, write_query_result
from boardroom_analyst.report_builder import write_insight_brief


OUTPUT = ROOT / "demo" / "output"
REPORT_DIR = OUTPUT / "reports" / "boardroom-demo"
ANALYSIS_DIR = OUTPUT / "analysis_runs"


def main() -> int:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    (REPORT_DIR / "charts").mkdir(parents=True, exist_ok=True)
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

    db_path = OUTPUT / "boardroom_demo.duckdb"
    _create_demo_database(db_path)

    context = build_datamart_context(ROOT / "fixtures" / "saas_dbt")
    write_datamart_context(context, OUTPUT / "datamart_context.json")

    q001 = execute_read_only_query(
        db_path,
        (ROOT / "demo" / "queries" / "q001_segment_mrr.sql").read_text(encoding="utf-8"),
        query_id="q001_segment_mrr",
    )
    q002 = execute_read_only_query(
        db_path,
        (ROOT / "demo" / "queries" / "q002_growth_waterfall.sql").read_text(encoding="utf-8"),
        query_id="q002_growth_waterfall",
    )
    write_query_result(q001, ANALYSIS_DIR / "q001_segment_mrr.json")
    write_query_result(q002, ANALYSIS_DIR / "q002_growth_waterfall.json")
    _write_chart_csv(q001, REPORT_DIR / "charts" / "mrr_by_segment.csv")
    _write_chart_csv(q002, REPORT_DIR / "charts" / "growth_waterfall.csv")

    run = _analysis_run(q001, q002)
    write_insight_brief(run, REPORT_DIR)

    print(
        json.dumps(
            {
                "database": str(db_path),
                "context": str(OUTPUT / "datamart_context.json"),
                "brief": str(REPORT_DIR / "brief.md"),
            },
            indent=2,
        )
    )
    return 0


def _create_demo_database(db_path: Path) -> None:
    con = duckdb.connect(str(db_path))
    con.execute(
        """
        create table mrr_by_month as
        select * from (
          values
            (date '2026-01-01', 'enterprise', 420000),
            (date '2026-01-01', 'mid-market', 225000),
            (date '2026-01-01', 'smb', 118000),
            (date '2026-02-01', 'enterprise', 438000),
            (date '2026-02-01', 'mid-market', 246000),
            (date '2026-02-01', 'smb', 132000),
            (date '2026-03-01', 'enterprise', 421000),
            (date '2026-03-01', 'mid-market', 258000),
            (date '2026-03-01', 'smb', 142000)
        ) as t(month, segment, mrr)
        """
    )
    con.close()


def _write_chart_csv(query_result: dict, output: Path) -> None:
    import csv

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=query_result["columns"])
        writer.writeheader()
        writer.writerows(query_result["rows"])


def _analysis_run(q001: dict, q002: dict) -> dict:
    return {
        "run_id": "boardroom-demo",
        "question": "Why did net revenue growth slow in March?",
        "summary": (
            "MRR still grew in March, but the growth rate slowed from +$53K in February "
            "to +$5K in March because enterprise contraction offset continued SMB and "
            "mid-market expansion."
        ),
        "findings": [
            {
                "claim": "Total MRR increased from $816K to $821K in March, but monthly growth dropped from +$53K to +$5K.",
                "query_id": "q002_growth_waterfall",
                "confidence": "high",
                "caveats": ["Fixture uses documented recurring revenue only and excludes one-time services."],
            },
            {
                "claim": "Enterprise MRR fell by $17K in March, while mid-market and SMB added $22K combined.",
                "query_id": "q001_segment_mrr",
                "confidence": "high",
                "caveats": ["Segment-level attribution is based on the documented model grain: one row per month and customer segment."],
            },
        ],
        "charts": [
            {
                "title": "MRR by segment",
                "path": "charts/mrr_by_segment.csv",
                "query_id": "q001_segment_mrr",
                "filters": "All documented rows in demo fixture",
                "time_range": "2026-01 to 2026-03",
                "caveats": ["Demo data is synthetic."],
            },
            {
                "title": "Monthly MRR growth",
                "path": "charts/growth_waterfall.csv",
                "query_id": "q002_growth_waterfall",
                "filters": "All documented rows in demo fixture",
                "time_range": "2026-01 to 2026-03",
                "caveats": ["Demo data is synthetic."],
            },
        ],
        "queries": [
            _query_metadata(q001),
            _query_metadata(q002),
        ],
        "caveats": [
            "Demo uses a synthetic SaaS revenue mart.",
            "The brief does not infer metrics outside documented dbt context.",
        ],
    }


def _query_metadata(query_result: dict) -> dict:
    return {
        "query_id": query_result["query_id"],
        "sql": query_result["sql"],
        "row_count": query_result["row_count"],
        "result_hash": query_result["result_hash"],
    }


if __name__ == "__main__":
    raise SystemExit(main())
