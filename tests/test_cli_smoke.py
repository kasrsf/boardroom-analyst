import json
import subprocess
import sys

import duckdb


def test_packaged_scripts_smoke_with_synthetic_fixture(tmp_path):
    root = __import__("pathlib").Path(__file__).resolve().parents[1]
    plugin_scripts = root / "plugins" / "boardroom-analyst" / "scripts"
    db_path = tmp_path / "visual_discovery.duckdb"
    con = duckdb.connect(str(db_path))
    con.execute(
        """
        create table ad_revenue_by_surface as
        select * from (
          values
            (date '2026-01-01', 'Performance Shopping Ads', 1000),
            (date '2026-02-01', 'Performance Shopping Ads', 1200),
            (date '2026-02-01', 'Brand Video Ads', 300)
        ) as t(month, surface, net_revenue_millions)
        """
    )
    con.close()

    context_path = tmp_path / "datamart_context.json"
    subprocess.run(
        [
            sys.executable,
            str(plugin_scripts / "build_datamart_context.py"),
            "--dbt-project",
            str(root / "fixtures" / "visual_discovery_dbt"),
            "--output",
            str(context_path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert json.loads(context_path.read_text(encoding="utf-8"))["warnings"] == []

    query_path = tmp_path / "q001.json"
    subprocess.run(
        [
            sys.executable,
            str(plugin_scripts / "run_duckdb_query.py"),
            "--database",
            str(db_path),
            "--query-id",
            "q001",
            "--sql",
            """
            select surface, sum(net_revenue_millions) as net_revenue_millions
            from ad_revenue_by_surface
            group by 1
            order by 1
            """,
            "--output",
            str(query_path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    query = json.loads(query_path.read_text(encoding="utf-8"))
    assert query["row_count"] == 2

    csv_path = tmp_path / "reports" / "run_1" / "charts" / "revenue_by_surface.csv"
    subprocess.run(
        [
            sys.executable,
            str(plugin_scripts / "export_chart_csv.py"),
            "--query-result",
            str(query_path),
            "--output",
            str(csv_path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert csv_path.read_text(encoding="utf-8").splitlines()[0] == "surface,net_revenue_millions"

    run_path = tmp_path / "analysis_run.json"
    run_path.write_text(
        json.dumps(
            {
                "run_id": "run_1",
                "question": "Why did ad revenue growth slow last month?",
                "summary": "Brand Video Ads offset shopping and visual search growth.",
                "findings": [
                    {
                        "claim": "Brand Video Ads were the drag on monetization surface growth.",
                        "query_id": "q001",
                        "confidence": "high",
                        "caveats": [],
                    }
                ],
                "charts": [
                    {
                        "title": "Ad revenue by surface",
                        "path": str(csv_path),
                        "query_id": "q001",
                        "filters": "all fixture rows",
                        "time_range": "2026-01 to 2026-02",
                        "caveats": [],
                    }
                ],
                "queries": [query],
                "caveats": ["Synthetic fixture only."],
            }
        ),
        encoding="utf-8",
    )
    subprocess.run(
        [
            sys.executable,
            str(plugin_scripts / "write_insight_brief.py"),
            "--run",
            str(run_path),
            "--output-dir",
            str(tmp_path / "reports" / "run_1"),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert (tmp_path / "reports" / "run_1" / "brief.md").exists()
