from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def test_deserters_have_cautious_personality_without_bandit_behavior():
    source = (ROOT / "source/module_party_templates.py").read_text(encoding="cp1254")
    template = next((line for line in source.splitlines() if '("deserters"' in line), None)

    assert template, "Could not find the deserter party template."
    assert "aggressiveness_3|courage_5" in template
    assert "bandit_personality" not in template
