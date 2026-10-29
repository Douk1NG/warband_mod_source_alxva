"""Keep camp hub event handlers on Native-supported presentation operations."""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_camp_hub_scroll_state_uses_native_event_value_not_opcode_4900():
    source = (ROOT / "source/presentations/prsnt_camp_hub.py").read_text(encoding="utf-8")
    assert "overlay_get_val" not in source
    assert '(store_trigger_param_2, ":value")' in source
    assert '(assign, "$g_camp_hub_scroll", ":value")' in source
