import pytest

from ceo_datamart_insights.sql_safety import UnsafeSqlError, validate_read_only_sql


def test_allows_single_select_and_normalizes_trailing_semicolon():
    assert validate_read_only_sql(" select * from revenue ; ") == "select * from revenue"


def test_rejects_mutating_keywords_outside_strings_and_comments():
    unsafe = [
        "insert into revenue values (1)",
        "update revenue set mrr = 0",
        "delete from revenue",
        "create table x as select 1",
        "drop table revenue",
        "copy revenue to 'out.csv'",
        "attach 'other.duckdb' as other",
        "alter table revenue add column x int",
        "install httpfs",
        "load httpfs",
    ]

    for sql in unsafe:
        with pytest.raises(UnsafeSqlError):
            validate_read_only_sql(sql)


def test_allows_danger_words_inside_literals_and_comments():
    sql = """
    -- drop is only text in a comment
    select 'delete is only text' as note, segment
    from revenue
    where segment <> 'copy'
    """

    assert "delete" in sql.lower()
    assert validate_read_only_sql(sql).startswith("-- drop is only text")


def test_rejects_multi_statement_sql_even_when_each_statement_is_select():
    with pytest.raises(UnsafeSqlError):
        validate_read_only_sql("select 1; select 2")
