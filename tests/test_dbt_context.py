import json

import yaml

from ceo_datamart_insights.dbt_context import build_datamart_context


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def test_builds_context_from_manifest_catalog_and_schema_yaml(tmp_path):
    dbt_dir = tmp_path / "dbt"
    write_json(
        dbt_dir / "target" / "manifest.json",
        {
            "metadata": {"project_name": "ceo_mart"},
            "nodes": {
                "model.ceo_mart.mrr_by_month": {
                    "resource_type": "model",
                    "name": "mrr_by_month",
                    "database": "local",
                    "schema": "main",
                    "alias": "mrr_by_month",
                    "description": "Monthly recurring revenue by segment.",
                    "columns": {
                        "month": {"name": "month", "description": "Calendar month."},
                        "segment": {"name": "segment", "description": "Customer segment."},
                        "mrr": {"name": "mrr", "description": "Monthly recurring revenue."},
                    },
                    "meta": {
                        "grain": "one row per month and segment",
                        "metrics": [
                            {
                                "name": "mrr",
                                "description": "Monthly recurring revenue.",
                                "formula": "sum(mrr)",
                                "caveats": ["Excludes one-time services."],
                            }
                        ],
                        "joins": [
                            {
                                "name": "accounts",
                                "relationship": "many_to_one",
                                "on": "mrr_by_month.account_id = accounts.account_id",
                            }
                        ],
                    },
                }
            },
            "metrics": {
                "metric.ceo_mart.net_revenue_retention": {
                    "name": "net_revenue_retention",
                    "description": "NRR by cohort.",
                    "type": "ratio",
                    "type_params": {"numerator": "retained_mrr", "denominator": "starting_mrr"},
                }
            },
        },
    )
    write_json(
        dbt_dir / "target" / "catalog.json",
        {
            "nodes": {
                "model.ceo_mart.mrr_by_month": {
                    "columns": {
                        "month": {"type": "DATE", "stats": {"count": {"value": 12}}},
                        "segment": {"type": "VARCHAR", "stats": {"count": {"value": 36}}},
                        "mrr": {"type": "DOUBLE", "stats": {"count": {"value": 36}}},
                    }
                }
            }
        },
    )
    schema = {
        "version": 2,
        "models": [
            {
                "name": "mrr_by_month",
                "meta": {
                    "priority_questions": [
                        "Why did revenue slow last month?",
                        "Which segment is driving expansion?",
                    ]
                },
            }
        ],
    }
    schema_path = dbt_dir / "models" / "schema.yml"
    schema_path.parent.mkdir(parents=True)
    schema_path.write_text(yaml.safe_dump(schema), encoding="utf-8")

    context = build_datamart_context(dbt_dir)

    assert context["project_name"] == "ceo_mart"
    assert context["warnings"] == []
    table = context["tables"][0]
    assert table["name"] == "mrr_by_month"
    assert table["grain"] == "one row per month and segment"
    assert table["columns"]["mrr"]["type"] == "DOUBLE"
    assert table["columns"]["mrr"]["description"] == "Monthly recurring revenue."
    assert table["metrics"][0]["name"] == "mrr"
    assert context["metrics"][0]["name"] == "net_revenue_retention"
    assert table["priority_questions"] == [
        "Why did revenue slow last month?",
        "Which segment is driving expansion?",
    ]


def test_context_warns_when_docs_are_not_trustworthy(tmp_path):
    dbt_dir = tmp_path / "dbt"
    write_json(
        dbt_dir / "target" / "manifest.json",
        {
            "nodes": {
                "model.ceo_mart.ambiguous_revenue": {
                    "resource_type": "model",
                    "name": "ambiguous_revenue",
                    "schema": "main",
                    "columns": {"revenue": {"name": "revenue"}},
                    "meta": {},
                }
            }
        },
    )
    write_json(dbt_dir / "target" / "catalog.json", {"nodes": {}})

    context = build_datamart_context(dbt_dir)

    assert context["tables"][0]["trust_level"] == "low"
    assert any("missing description" in warning for warning in context["warnings"])
    assert any("missing grain" in warning for warning in context["warnings"])
    assert any("no documented metrics" in warning for warning in context["warnings"])
