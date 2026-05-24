from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_insight_brief(run: dict[str, Any], output_dir: str | Path) -> Path:
    """Write analysis_run.json and a provenance-first CEO brief."""

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "analysis_run.json").write_text(
        json.dumps(run, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )

    brief = _render_brief(run)
    brief_path = destination / "brief.md"
    brief_path.write_text(brief, encoding="utf-8")
    return brief_path


def _render_brief(run: dict[str, Any]) -> str:
    lines = [
        "# CEO Insight Brief",
        "",
        f"Run: `{run.get('run_id', 'untracked')}`",
        f"Question: {run.get('question', '')}",
        "",
        "## Executive Summary",
        "",
        run.get("summary") or "No supported summary was provided.",
        "",
        "## Findings",
        "",
    ]

    findings = run.get("findings") or []
    if not findings:
        lines.append("- No supported findings. Review caveats and query appendix.")
    for finding in findings:
        query_id = finding.get("query_id", "untracked")
        confidence = finding.get("confidence", "unknown")
        lines.append(f"- {finding.get('claim', '')} [`{query_id}`] Confidence: `{confidence}`")
        for caveat in finding.get("caveats") or []:
            lines.append(f"  - Caveat: {caveat}")

    lines.extend(["", "## Charts", ""])
    charts = run.get("charts") or []
    if not charts:
        lines.append("- No charts generated.")
    for chart in charts:
        lines.append(f"- {chart.get('title', 'Untitled chart')}: `{chart.get('path', '')}`")
        lines.append(f"  - Source query: `{chart.get('query_id', 'untracked')}`")
        lines.append(f"  - Filters: {chart.get('filters', 'none documented')}")
        lines.append(f"  - Time range: {chart.get('time_range', 'not documented')}")
        for caveat in chart.get("caveats") or []:
            lines.append(f"  - Caveat: {caveat}")

    lines.extend(["", "## Caveats", ""])
    caveats = run.get("caveats") or []
    if not caveats:
        lines.append("- No caveats documented.")
    for caveat in caveats:
        lines.append(f"- {caveat}")

    lines.extend(["", "## SQL Appendix", ""])
    queries = run.get("queries") or []
    if not queries:
        lines.append("- No queries recorded.")
    for query in queries:
        lines.append(f"### `{query.get('query_id', 'untracked')}`")
        lines.append("")
        lines.append("```sql")
        lines.append(query.get("sql", "").strip())
        lines.append("```")
        lines.append("")
        lines.append(
            f"Rows: `{query.get('row_count', 0)}`; result hash: `{query.get('result_hash', '')}`"
        )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
