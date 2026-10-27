"""Regression checks for the Equip Companions "Remove all" action.

These inspect the module-system operation source. They catch regressions in
the action's selection and slot coverage, but do not execute Warband opcodes.
"""
from __future__ import annotations

import re

from tests._helpers import read_text


PRESENTATION = "presentations/prsnt_equip_npcs.py"


def _remove_all_block() -> str:
    text = read_text(PRESENTATION)
    start = text.index('(eq, "$g_autoloot_mass_action_mode", 1)')
    end = text.index('(eq, "$g_autoloot_mass_action_mode", 2)', start)
    return text[start:end]


def test_remove_all_covers_every_equipment_slot_without_autoloot_filters():
    """Remove all must cover weapon, armor, and horse slots regardless of
    the selected hero's separate auto-upgrade settings.
    """
    block = _remove_all_block()

    assert re.search(
        r'\(try_for_range,\s*":slot_no",\s*0,\s*9\)', block
    ), "Remove all must iterate equipment slots 0 through 8, including weapons and horse."
    assert '(eq, ":do_upgrade", 1)' not in block, (
        "Remove all must not be gated by an auto-upgrade setting."
    )
    assert 'troop_get_slot, ":do_upgrade", "$g_selected_troop"' not in block, (
        "Remove all must not read auto-upgrade settings from the selected hero."
    )
    assert re.search(
        r'\(troop_set_inventory_slot,\s*":stack_troop",\s*":slot_no",\s*-1\)',
        block,
    ), "Remove all must clear the companion's equipped slot."
    assert re.search(
        r'\(troop_set_inventory_slot,\s*"trp_player",\s*":i_slot",\s*":cur_item"\)',
        block,
    ), "Removed equipment must be transferred into the player's inventory when space exists."
