import duckdb
import pytest

from boardroom_analyst.duckdb_runner import execute_read_only_query
from boardroom_analyst.sql_safety import UnsafeSqlError


def create_visual_discovery_style_db(path):
    con = duckdb.connect(str(path))
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


def test_executes_select_read_only_and_records_provenance(tmp_path):
    db_path = tmp_path / "visual_discovery.duckdb"
    create_visual_discovery_style_db(db_path)

    result = execute_read_only_query(
        db_path,
        """
        select surface, sum(net_revenue_millions) as net_revenue_millions
        from ad_revenue_by_surface
        group by 1
        order by 1
        """,
        query_id="q001",
    )

    assert result["query_id"] == "q001"
    assert result["row_count"] == 2
    assert result["columns"] == ["surface", "net_revenue_millions"]
    assert result["rows"][0] == {"surface": "Brand Video Ads", "net_revenue_millions": 300}
    assert result["sql_hash"]
    assert result["result_hash"]
    assert result["elapsed_ms"] >= 0
    assert result["database"].endswith("visual_discovery.duckdb")


def test_rejects_writes_before_opening_database(tmp_path):
    db_path = tmp_path / "visual_discovery.duckdb"
    create_visual_discovery_style_db(db_path)

    with pytest.raises(UnsafeSqlError):
        execute_read_only_query(db_path, "delete from ad_revenue_by_surface")


def test_read_only_connection_does_not_allow_validated_write_bypass(tmp_path):
    db_path = tmp_path / "visual_discovery.duckdb"
    create_visual_discovery_style_db(db_path)

    with pytest.raises(UnsafeSqlError):
        execute_read_only_query(db_path, "copy (select * from ad_revenue_by_surface) to 'out.csv'")
