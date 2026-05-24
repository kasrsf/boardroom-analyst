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

    context = build_datamart_context(ROOT / "fixtures" / "visual_discovery_dbt")
    write_datamart_context(context, OUTPUT / "datamart_context.json")

    q001 = execute_read_only_query(
        db_path,
        (ROOT / "demo" / "queries" / "q001_surface_revenue.sql").read_text(encoding="utf-8"),
        query_id="q001_surface_revenue",
    )
    q002 = execute_read_only_query(
        db_path,
        (ROOT / "demo" / "queries" / "q002_revenue_growth_waterfall.sql").read_text(encoding="utf-8"),
        query_id="q002_revenue_growth_waterfall",
    )
    write_query_result(q001, ANALYSIS_DIR / "q001_surface_revenue.json")
    write_query_result(q002, ANALYSIS_DIR / "q002_revenue_growth_waterfall.json")
    _write_chart_csv(q001, REPORT_DIR / "charts" / "revenue_by_surface.csv")
    _write_chart_csv(q002, REPORT_DIR / "charts" / "revenue_growth_waterfall.csv")

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
        create table ad_revenue_by_surface as
        select * from (
          values
            (date '2026-01-01', 'Performance Shopping Ads', 372.0, 182.0, 21.4),
            (date '2026-01-01', 'Visual Search Ads', 298.0, 165.0, 18.9),
            (date '2026-01-01', 'Brand Video Ads', 186.0, 124.0, 7.2),
            (date '2026-02-01', 'Performance Shopping Ads', 410.0, 190.0, 23.6),
            (date '2026-02-01', 'Visual Search Ads', 322.0, 171.0, 20.2),
            (date '2026-02-01', 'Brand Video Ads', 193.0, 126.0, 7.5),
            (date '2026-03-01', 'Performance Shopping Ads', 449.0, 199.0, 25.5),
            (date '2026-03-01', 'Visual Search Ads', 345.0, 178.0, 21.8),
            (date '2026-03-01', 'Brand Video Ads', 179.0, 127.0, 7.6)
        ) as t(month, surface, net_revenue_millions, engaged_users_millions, commercial_searches_billions)
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
        "question": "The CEO asks: why did ad revenue growth slow in March?",
        "summary": (
            "Synthetic visual-discovery ad revenue still grew in March, but the growth rate slowed "
            "from +$69M in February to +$48M in March because Brand Video Ads swung from "
            "+$7M growth to a -$14M decline while shopping and visual search kept expanding."
        ),
        "findings": [
            {
                "claim": "Total ad revenue increased from $925M to $973M in March, but monthly growth slowed from +$69M to +$48M.",
                "query_id": "q002_revenue_growth_waterfall",
                "confidence": "high",
                "caveats": ["Fixture is synthetic and should not be read as reported company results."],
            },
            {
                "claim": "Brand Video Ads declined by $14M in March, offsetting a combined +$62M from Performance Shopping Ads and Visual Search Ads.",
                "query_id": "q001_surface_revenue",
                "confidence": "high",
                "caveats": ["Surface attribution is based on the documented model grain: one row per month and monetization surface."],
            },
            {
                "claim": "Shopping-intent surfaces remained the strategic bright spot: Performance Shopping Ads added $39M and Visual Search Ads added $23M in March.",
                "query_id": "q001_surface_revenue",
                "confidence": "high",
                "caveats": ["Commercial search and engaged-user fields are synthetic proxies for demo purposes."],
            },
        ],
        "charts": [
            {
                "title": "Ad revenue by monetization surface",
                "path": "charts/revenue_by_surface.csv",
                "query_id": "q001_surface_revenue",
                "filters": "All documented rows in demo fixture",
                "time_range": "2026-01 to 2026-03",
                "caveats": ["Demo data is synthetic."],
            },
            {
                "title": "Monthly ad revenue growth",
                "path": "charts/revenue_growth_waterfall.csv",
                "query_id": "q002_revenue_growth_waterfall",
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
            "Demo uses synthetic visual-discovery advertising and engagement data.",
            "The fixture is tailored for an internal executive pitch and is not reported company data.",
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
