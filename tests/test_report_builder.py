import json

from boardroom_analyst.report_builder import write_insight_brief


def test_writes_brief_with_claim_provenance_chart_sources_and_sql_appendix(tmp_path):
    run = {
        "run_id": "run_20260524_000001",
        "question": "Why did ad revenue growth slow last month?",
        "summary": "Revenue growth slowed because Brand Video Ads offset shopping and visual search expansion.",
        "findings": [
            {
                "claim": "Brand Video Ads fell 10% month over month.",
                "query_id": "q001",
                "confidence": "high",
                "caveats": ["Demo data is synthetic."],
            }
        ],
        "charts": [
            {
                "title": "Ad revenue by surface",
                "path": "charts/revenue_by_surface.csv",
                "query_id": "q001",
                "filters": "month between 2026-01-01 and 2026-02-01",
                "time_range": "2026-01 to 2026-02",
                "caveats": ["Small sample fixture."],
            }
        ],
        "queries": [
            {
                "query_id": "q001",
                "sql": "select surface, sum(net_revenue_millions) from ad_revenue_by_surface group by 1",
                "row_count": 2,
                "result_hash": "abc123",
            }
        ],
        "caveats": ["Only documented dbt models were used."],
    }

    output = write_insight_brief(run, tmp_path)

    assert output.name == "brief.md"
    brief = output.read_text(encoding="utf-8")
    assert "# Boardroom Brief" in brief
    assert "Brand Video Ads fell 10% month over month. [`q001`]" in brief
    assert "Ad revenue by surface" in brief
    assert "Source query: `q001`" in brief
    assert "```sql" in brief
    assert "result hash: `abc123`" in brief
    assert json.loads((tmp_path / "analysis_run.json").read_text(encoding="utf-8"))["run_id"] == run["run_id"]
