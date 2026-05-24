import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "ceo-datamart-insights"


def test_plugin_manifests_and_three_skills_exist():
    skill_names = {"datamart-onboarding", "ceo-insight-brief", "ceo-query-analyst"}

    for manifest_path in [
        PLUGIN / ".codex-plugin" / "plugin.json",
        PLUGIN / ".claude-plugin" / "plugin.json",
    ]:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["name"] == "ceo-datamart-insights"
        assert manifest["version"] == "0.1.0"
        assert manifest["skills"] == "./skills/"
        assert "license" in manifest

    for skill_name in skill_names:
        skill_path = PLUGIN / "skills" / skill_name / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        assert f"name: {skill_name}" in text
        assert "description:" in text
        assert "source query" in text.lower() or "provenance" in text.lower()


def test_openai_metadata_and_release_metadata_are_marketplace_ready():
    openai_yaml = yaml.safe_load((PLUGIN / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    assert openai_yaml["interface"]["display_name"] == "CEO Datamart Insights"
    assert "$ceo-insight-brief" in openai_yaml["interface"]["default_prompt"]

    release = json.loads((PLUGIN / "release.json").read_text(encoding="utf-8"))
    assert release["name"] == "ceo-datamart-insights"
    assert release["version"] == "0.1.0"
    assert release["license_policy"]["runtime_entitlement_checks"] is False
    assert release["checksums"]


def test_repo_marketplace_points_to_local_plugin():
    marketplace = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    assert marketplace["name"] == "skills-marketplace"
    entry = marketplace["plugins"][0]
    assert entry["name"] == "ceo-datamart-insights"
    assert entry["source"]["path"] == "./plugins/ceo-datamart-insights"
    assert entry["policy"]["installation"] == "AVAILABLE"
