import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "boardroom-analyst"


def test_plugin_manifests_and_three_skills_exist():
    skill_names = {"boardroom-onboarding", "boardroom-brief", "boardroom-query"}

    for manifest_path in [
        PLUGIN / ".codex-plugin" / "plugin.json",
        PLUGIN / ".claude-plugin" / "plugin.json",
    ]:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["name"] == "boardroom-analyst"
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
    assert openai_yaml["interface"]["display_name"] == "Boardroom Analyst"
    assert "$boardroom-brief" in openai_yaml["interface"]["default_prompt"]

    release = json.loads((PLUGIN / "release.json").read_text(encoding="utf-8"))
    assert release["name"] == "boardroom-analyst"
    assert release["version"] == "0.1.0"
    assert release["license_policy"]["runtime_entitlement_checks"] is False
    assert release["checksums"]


def test_repo_marketplace_points_to_local_plugin():
    marketplace = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    assert marketplace["name"] == "skills-marketplace"
    entry = marketplace["plugins"][0]
    assert entry["name"] == "boardroom-analyst"
    assert entry["source"]["path"] == "./plugins/boardroom-analyst"
    assert entry["policy"]["installation"] == "AVAILABLE"
