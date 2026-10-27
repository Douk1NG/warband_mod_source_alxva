"""Source-level regression checks for auto-loot change notifications."""
from __future__ import annotations

from tests._helpers import read_text


SCRIPT = "scripts/dplmc_auto_loot_troop.py"


def _summary_block() -> str:
    source = read_text(SCRIPT)
    start = source.index("#SB : string storage")
    end = source.index("# (try_end),", start)
    return source[start:end]


def test_change_flag_resets_for_each_equipment_slot():
    block = _summary_block()
    loop = block.index('(try_for_range, ":i_slot", ek_item_0, ek_food)')
    reset = block.index('(assign, ":item_changed", 0)', loop)
    classification = block.index('(try_begin), #keep current', loop)

    assert loop < reset < classification
    assert '(assign, ":item_no", -1)' in block[loop:classification]


def test_horse_summary_compares_against_the_pre_loot_equipment():
    source = read_text(SCRIPT)
    block = _summary_block()

    assert '(assign, ":orig_horse_imod", ":orig_imod")' in source
    assert '(eq, ":i_slot", ek_horse)' in block
    assert '(neq, ":upg_horses", 0)' in block
    assert '(assign, ":old_item", ":orig_horse")' in block
    assert '(assign, ":old_imod", ":orig_horse_imod")' in block


def test_summary_uses_clear_actions_and_names_the_troop():
    block = _summary_block()

    assert '(str_store_string, s1, "@equipped: {s20}")' in block
    assert '(str_store_string, s1, "@returned to loot: {s20}")' in block
    assert '(str_store_string, ":sreg", "@{s0}: {s1}")' in block
    assert '(le, ":num_changes", 0)' in block
    assert '(str_clear, ":sreg")' in block
