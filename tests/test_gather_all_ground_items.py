"""Source-level regression checks for gathering items from the loot pools.

These checks verify the menu predicates and transfer operations in the
module-system source. They do not execute Warband's menu/opcode runtime.
"""
from __future__ import annotations

import re

from tests._helpers import read_text


MENU = "game_menus/mnu_dplmc_manage_loot_pool.py"


def _menu_option(option_id: str, next_option_id: str) -> str:
    source = read_text(MENU)
    start = source.index(f'("{option_id}",')
    end = source.index(f'("{next_option_id}",', start)
    return source[start:end]


def test_gather_all_requires_enough_space_and_items_on_ground():
    option = _menu_option("dplmc_leave_and_take_b", "dplmc_leave_and_take_c")

    assert re.search(r'\(ge, ":space", reg20\)', option)
    assert re.search(r'\(gt, reg20, 0\)', option)
    assert "Gather the remaining {reg20}" in option


def test_gather_what_fits_requires_partial_capacity_and_items():
    option = _menu_option("dplmc_leave_and_take_a", "dplmc_leave_and_take_b")

    assert re.search(r'\(lt, ":space", reg20\)', option)
    assert re.search(r'\(gt, ":space", 0\)', option)
    assert re.search(r'\(gt, reg20, 0\)', option)
    assert "Gather {reg0} of the {reg20} items on the ground" in option


def test_both_gather_actions_transfer_and_clear_items_from_all_three_pools():
    for option_id, next_option_id in (
        ("dplmc_leave_and_take_a", "dplmc_leave_and_take_b"),
        ("dplmc_leave_and_take_b", "dplmc_leave_and_take_c"),
    ):
        option = _menu_option(option_id, next_option_id)

        assert re.search(r'\(try_for_range, ":pool_idx", 0, 3\)', option)
        assert '"$pool_troop"' in option
        assert '"trp_dplmc_pool_2"' in option
        assert '"trp_dplmc_pool_3"' in option
        assert re.search(r'\(try_for_range, ":i_slot", 10, ":inv_cap"\)', option)
        assert re.search(
            r'\(troop_add_item, "trp_player", ":item_id", ":imod"\)', option
        )
        assert re.search(
            r'\(troop_set_inventory_slot, ":take_pool", ":i_slot", -1\)', option
        )
        assert re.search(
            r'\(troop_inventory_slot_set_item_amount, ":take_pool", ":i_slot", 0\)',
            option,
        )
        assert re.search(r'\(jump_to_menu, "\$dplmc_return_menu"\)', option)
