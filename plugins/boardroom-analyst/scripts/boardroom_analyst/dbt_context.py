from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def build_datamart_context(dbt_project_dir: str | Path) -> dict[str, Any]:
    """Build normalized semantic context from dbt artifacts and YAML docs."""

    project_dir = Path(dbt_project_dir)
    manifest = _read_json(project_dir / "target" / "manifest.json")
    catalog = _read_json(project_dir / "target" / "catalog.json", default={"nodes": {}})
    yaml_models = _load_schema_yaml_models(project_dir)

    warnings: list[str] = []
    tables: list[dict[str, Any]] = []
    catalog_nodes = catalog.get("nodes", {})

    for node_id, node in sorted(manifest.get("nodes", {}).items()):
        if node.get("resource_type") != "model":
            continue

        name = node.get("alias") or node.get("name") or node_id.rsplit(".", 1)[-1]
        yaml_model = yaml_models.get(node.get("name") or name, {})
        table_warnings: list[str] = []
        meta = _merged_meta(yaml_model, node)
        description = node.get("description") or yaml_model.get("description") or ""
        grain = meta.get("grain") or meta.get("entity_grain") or ""
        documented_metrics = _normalise_metric_list(meta.get("metrics", []))
        columns = _build_columns(node, yaml_model, catalog_nodes.get(node_id, {}))
        priority_questions = list(meta.get("priority_questions") or [])
        joins = list(meta.get("joins") or [])

        if not description:
            table_warnings.append(f"table {name} missing description")
        if not grain:
            table_warnings.append(f"table {name} missing grain")
        if not documented_metrics:
            table_warnings.append(f"table {name} has no documented metrics")

        for column_name, column in columns.items():
            if not column.get("description"):
                table_warnings.append(f"table {name} column {column_name} missing description")

        warnings.extend(table_warnings)
        tables.append(
            {
                "node_id": node_id,
                "name": name,
                "database": node.get("database") or "",
                "schema": node.get("schema") or "",
                "description": description,
                "grain": grain,
                "columns": columns,
                "metrics": documented_metrics,
                "joins": joins,
                "priority_questions": priority_questions,
                "trust_level": _trust_level(table_warnings),
                "warnings": table_warnings,
            }
        )

    return {
        "version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_name": _project_name(project_dir, manifest),
        "source": {
            "dbt_project_dir": str(project_dir),
            "manifest": str(project_dir / "target" / "manifest.json"),
            "catalog": str(project_dir / "target" / "catalog.json"),
        },
        "tables": tables,
        "metrics": _build_manifest_metrics(manifest),
        "warnings": warnings,
    }


def write_datamart_context(context: dict[str, Any], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(context, indent=2, sort_keys=True, default=str), encoding="utf-8")
    return output


def _read_json(path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        if default is not None:
            return default
        raise FileNotFoundError(f"Missing required dbt artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _load_schema_yaml_models(project_dir: Path) -> dict[str, dict[str, Any]]:
    models: dict[str, dict[str, Any]] = {}
    for yaml_path in sorted(project_dir.rglob("*.yml")) + sorted(project_dir.rglob("*.yaml")):
        if "target" in yaml_path.parts:
            continue
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
        for model in data.get("models", []) or []:
            name = model.get("name")
            if name:
                models[name] = _deep_merge(models.get(name, {}), model)
    return models


def _merged_meta(yaml_model: dict[str, Any], node: dict[str, Any]) -> dict[str, Any]:
    yaml_meta = _deep_merge(
        yaml_model.get("meta") or {},
        (yaml_model.get("config") or {}).get("meta") or {},
    )
    return _deep_merge(yaml_meta, node.get("meta") or {})


def _build_columns(
    node: dict[str, Any],
    yaml_model: dict[str, Any],
    catalog_node: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    columns: dict[str, dict[str, Any]] = {}
    yaml_columns = {column.get("name"): column for column in yaml_model.get("columns", []) or []}
    manifest_columns = node.get("columns") or {}
    catalog_columns = catalog_node.get("columns") or {}

    for column_name in sorted(set(manifest_columns) | set(yaml_columns) | set(catalog_columns)):
        manifest_column = manifest_columns.get(column_name) or {}
        yaml_column = yaml_columns.get(column_name) or {}
        catalog_column = catalog_columns.get(column_name) or {}
        columns[column_name] = {
            "name": column_name,
            "type": catalog_column.get("type") or manifest_column.get("data_type") or "",
            "description": manifest_column.get("description") or yaml_column.get("description") or "",
            "meta": _deep_merge(yaml_column.get("meta") or {}, manifest_column.get("meta") or {}),
            "stats": catalog_column.get("stats") or {},
        }

    return columns


def _normalise_metric_list(metrics: Any) -> list[dict[str, Any]]:
    if isinstance(metrics, dict):
        iterable = [{"name": name, **(value or {})} for name, value in metrics.items()]
    elif isinstance(metrics, list):
        iterable = metrics
    else:
        iterable = []

    normalised = []
    for metric in iterable:
        if isinstance(metric, str):
            normalised.append({"name": metric, "description": "", "formula": ""})
        elif isinstance(metric, dict):
            normalised.append(
                {
                    "name": metric.get("name") or "",
                    "description": metric.get("description") or "",
                    "formula": metric.get("formula") or metric.get("expression") or "",
                    "caveats": list(metric.get("caveats") or []),
                }
            )
    return [metric for metric in normalised if metric["name"]]


def _build_manifest_metrics(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = []
    for metric_id, metric in sorted((manifest.get("metrics") or {}).items()):
        metrics.append(
            {
                "metric_id": metric_id,
                "name": metric.get("name") or metric_id.rsplit(".", 1)[-1],
                "description": metric.get("description") or "",
                "type": metric.get("type") or "",
                "type_params": metric.get("type_params") or {},
            }
        )
    return metrics


def _project_name(project_dir: Path, manifest: dict[str, Any]) -> str:
    metadata_name = (manifest.get("metadata") or {}).get("project_name")
    if metadata_name:
        return metadata_name
    project_yml = project_dir / "dbt_project.yml"
    if project_yml.exists():
        data = yaml.safe_load(project_yml.read_text(encoding="utf-8")) or {}
        if data.get("name"):
            return data["name"]
    return project_dir.name


def _trust_level(table_warnings: list[str]) -> str:
    if not table_warnings:
        return "high"
    if any("missing description" in warning or "missing grain" in warning or "no documented metrics" in warning for warning in table_warnings):
        return "low"
    return "medium"


def _deep_merge(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    merged = dict(left)
    for key, value in right.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged
