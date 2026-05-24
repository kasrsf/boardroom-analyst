import duckdb
import pytest

from ceo_datamart_insights.duckdb_runner import execute_read_only_query
from ceo_datamart_insights.sql_safety import UnsafeSqlError


def create_saas_db(path):
    con = duckdb.connect(str(path))
    con.execute(
        """
        create table mrr_by_month as
        select * from (
          values
            (date '2026-01-01', 'enterprise', 1000),
            (date '2026-02-01', 'enterprise', 900),
            (date '2026-02-01', 'smb', 300)
        ) as t(month, segment, mrr)
        """
    )
    con.close()


def test_executes_select_read_only_and_records_provenance(tmp_path):
    db_path = tmp_path / "saas.duckdb"
    create_saas_db(db_path)

    result = execute_read_only_query(
        db_path,
        "select segment, sum(mrr) as mrr from mrr_by_month group by 1 order by 1",
        query_id="q001",
    )

    assert result["query_id"] == "q001"
    assert result["row_count"] == 2
    assert result["columns"] == ["segment", "mrr"]
    assert result["rows"][0] == {"segment": "enterprise", "mrr": 1900}
    assert result["sql_hash"]
    assert result["result_hash"]
    assert result["elapsed_ms"] >= 0
    assert result["database"].endswith("saas.duckdb")


def test_rejects_writes_before_opening_database(tmp_path):
    db_path = tmp_path / "saas.duckdb"
    create_saas_db(db_path)

    with pytest.raises(UnsafeSqlError):
        execute_read_only_query(db_path, "delete from mrr_by_month")


def test_read_only_connection_does_not_allow_validated_write_bypass(tmp_path):
    db_path = tmp_path / "saas.duckdb"
    create_saas_db(db_path)

    with pytest.raises(UnsafeSqlError):
        execute_read_only_query(db_path, "copy (select * from mrr_by_month) to 'out.csv'")
