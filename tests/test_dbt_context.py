import json

import yaml

from boardroom_analyst.dbt_context import build_datamart_context


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def test_builds_context_from_manifest_catalog_and_schema_yaml(tmp_path):
    dbt_dir = tmp_path / "dbt"
    write_json(
        dbt_dir / "target" / "manifest.json",
        {
            "metadata": {"project_name": "boardroom_mart"},
            "nodes": {
                "model.boardroom_mart.ad_revenue_by_surface": {
                    "resource_type": "model",
                    "name": "ad_revenue_by_surface",
                    "database": "local",
                    "schema": "main",
                    "alias": "ad_revenue_by_surface",
                    "description": "Monthly visual-discovery advertising revenue by monetization surface.",
                    "columns": {
                        "month": {"name": "month", "description": "Calendar month."},
                        "surface": {"name": "surface", "description": "Monetization surface."},
                        "net_revenue_millions": {
                            "name": "net_revenue_millions",
                            "description": "Net advertising revenue in USD millions.",
                        },
                    },
                    "meta": {
                        "grain": "one row per month and monetization surface",
                        "metrics": [
                            {
                                "name": "net_ad_revenue",
                                "description": "Net advertising revenue.",
                                "formula": "sum(net_revenue_millions)",
                                "caveats": ["Synthetic demo metric."],
                            }
                        ],
                        "joins": [
                            {
                                "name": "campaigns",
                                "relationship": "many_to_one",
                                "on": "ad_revenue_by_surface.campaign_id = campaigns.campaign_id",
                            }
                        ],
                    },
                }
            },
            "metrics": {
                "metric.boardroom_mart.commercial_search_intensity": {
                    "name": "commercial_search_intensity",
                    "description": "Commercial-intent searches per engaged user.",
                    "type": "simple",
                    "type_params": {"measure": "commercial_searches_billions"},
                }
            },
        },
    )
    write_json(
        dbt_dir / "target" / "catalog.json",
        {
            "nodes": {
                "model.boardroom_mart.ad_revenue_by_surface": {
                    "columns": {
                        "month": {"type": "DATE", "stats": {"count": {"value": 12}}},
                        "surface": {"type": "VARCHAR", "stats": {"count": {"value": 36}}},
                        "net_revenue_millions": {"type": "DOUBLE", "stats": {"count": {"value": 36}}},
                    }
                }
            }
        },
    )
    schema = {
        "version": 2,
        "models": [
            {
                "name": "ad_revenue_by_surface",
                "meta": {
                    "priority_questions": [
                        "Why did ad revenue growth slow last month?",
                        "Which monetization surface is driving expansion?",
                    ]
                },
            }
        ],
    }
    schema_path = dbt_dir / "models" / "schema.yml"
    schema_path.parent.mkdir(parents=True)
    schema_path.write_text(yaml.safe_dump(schema), encoding="utf-8")

    context = build_datamart_context(dbt_dir)

    assert context["project_name"] == "boardroom_mart"
    assert context["warnings"] == []
    table = context["tables"][0]
    assert table["name"] == "ad_revenue_by_surface"
    assert table["grain"] == "one row per month and monetization surface"
    assert table["columns"]["net_revenue_millions"]["type"] == "DOUBLE"
    assert table["columns"]["net_revenue_millions"]["description"] == "Net advertising revenue in USD millions."
    assert table["metrics"][0]["name"] == "net_ad_revenue"
    assert context["metrics"][0]["name"] == "commercial_search_intensity"
    assert table["priority_questions"] == [
        "Why did ad revenue growth slow last month?",
        "Which monetization surface is driving expansion?",
    ]


def test_context_warns_when_docs_are_not_trustworthy(tmp_path):
    dbt_dir = tmp_path / "dbt"
    write_json(
        dbt_dir / "target" / "manifest.json",
        {
            "nodes": {
                "model.boardroom_mart.ambiguous_revenue": {
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
