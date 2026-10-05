"""Tests for `script_upgrade_armors_and_horse_for_troop`.

This script is called when the user clicks "Apply" in the
`prsnt_equip_npcs` presentation (Inventory -> Heroes -> Select Gear).
User-reported 2026-10-04: heroes appear un-equipped after opening that
presentation.

The safe behavior is: only replace the troop's current item if the player
inventory contains a strictly better item of the same type. If no better
item exists, leave the troop's gear untouched.

These tests pin that behavior.
"""
from __future__ import annotations

import re

import pytest

from tests._helpers import read_text


UPGRADE_SCRIPT = "scripts/upgrade_armors_and_horse_for_troop.py"


@pytest.mark.bandit
def test_horse_upgrade_loop_iterates_ek_horse_too():
    """The upgrade loop must include ek_horse (= 8).

    If the loop only goes up to `ek_horse` (exclusive), it never touches
    the horse slot and heroes silently lose the auto-upgrade path for
    their horse.
    """
    text = read_text(UPGRADE_SCRIPT)
    # The loop should be `try_for_range, ":ek_slot", ek_head, ek_horse+1`
    # (inclusive on the high end so ek_horse=8 is included).
    loop_re = re.compile(
        r"\(try_for_range,\s*\":ek_slot\",\s*ek_head,\s*ek_horse\s*\+\s*1\)"
    )
    assert loop_re.search(text), (
        f"`{UPGRADE_SCRIPT}` loop does not iterate up to `ek_horse+1`. "
        "Horse upgrades silently skip. Fix shape: "
        "`(try_for_range, \":ek_slot\", ek_head, ek_horse+1)`"
    )


@pytest.mark.bandit
def test_horse_upgrade_keeps_original_when_no_better_in_player_inv():
    """When no item in the player inv beats the troop's current item, the
    troop's item must remain unchanged.

    Repro: open the presentation, click Apply, hero's horse disappears.

    The expected shape is:
        1. Capture the troop's current item into `:troop_item`
           (`:troop_imod`, capability `:best_val`).
        2. Walk the player inv from slot 10 onward, looking for items of
           matching type with capability `> best_val`.
        3. Only when a strictly-better candidate is found, swap.
        4. If no candidate is found, leave `:troop_item` alone (i.e. do
           not `troop_set_inventory_slot, ":troop", ":ek_slot", -1`).

    The test below verifies the shape: the original `:troop_item` capture
    exists, and the swap is gated on a `:best_slot >= 10` check (which
    means the swap is only reached when a player-inv candidate won).
    """
    text = read_text(UPGRADE_SCRIPT)
    assert "(store_script_param, \":troop\", 1)" in text, (
        "Expected the script to take `:troop` as param 1."
    )
    # The troop's current item must be captured into :troop_item.
    assert (
        '(troop_get_inventory_slot, ":troop_item", ":troop", ":ek_slot")' in text
    ), "Expected `(troop_get_inventory_slot, \":troop_item\", \":troop\", \":ek_slot\")`."
    # The :best_val starts at 0 and gets the troop's capability if non-empty.
    assert "(assign, \":best_val\", 0)" in text, (
        "Expected `:best_val = 0` initialization."
    )
    # The branch that swaps gear must be guarded by `:best_slot >= 10`,
    # proving the swap only fires when a player-inv slot won.
    assert "(ge, \":best_slot\", 10)" in text, (
        "Expected a `(ge, \":best_slot\", 10)` guard before swapping. "
        "Without this guard, the troop's items disappear whenever the "
        "loop ends without finding a player-inv replacement."
    )
    # The else- branch must NOT unconditionally clear the troop's slot.
    # If the script has a `(troop_set_inventory_slot, ":troop", ":ek_slot", -1)`
    # NOT inside the `:best_slot >= 10` branch, that's the bug.
    swap_pattern = re.compile(
        r'\(troop_set_inventory_slot,\s*":troop",\s*":ek_slot",\s*-1\)'
    )
    bad_swaps = []
    for m in swap_pattern.finditer(text):
        # Look backward ~400 chars for the (ge, ":best_slot", 10) check.
        preceding = text[max(0, m.start() - 400) : m.start()]
        if "(ge, \":best_slot\", 10)" not in preceding:
            bad_swaps.append(m.start())
    assert not bad_swaps, (
        f"BUG: {UPGRADE_SCRIPT} clears `:troop`'s `:ek_slot` to -1 at "
        f"line offsets {bad_swaps} WITHOUT being inside a `(ge, \":best_slot\", 10)` "
        "guard. This means the troop loses its current item even when no "
        "replacement was found in the player inventory — symptom: heroes "
        "appear un-equipped after clicking Apply in prsnt_equip_npcs."
    )


@pytest.mark.bandit
def test_horse_dest_type_is_itp_type_horse():
    """The horse ek_slot (8) must map to `itp_type_horse` so the search
    loop filters player inv by the correct item type.
    """
    text = read_text(UPGRADE_SCRIPT)
    # Find the (else_try) branch that handles ek_horse specifically.
    assert re.search(
        r"\(else_try\),\s*\(\s*eq,\s*\":ek_slot\",\s*ek_horse\s*\),\s*"
        r"\(\s*assign,\s*\":dest_type\",\s*itp_type_horse\s*\)",
        text,
    ), (
        f"`{UPGRADE_SCRIPT}` does not map ek_horse to itp_type_horse. "
        "The player-inv search will fail to find horses because of "
        "`item_get_type` returning a different mask."
    )


@pytest.mark.bandit
def test_search_starts_at_correct_slot():
    """The player-inv search must start at slot 10 (above the player's
    equipped gear) and use a non-magic-number. If `dplmc_ek_alt_items_end`
    ever moves, this test must move with it.
    """
    text = read_text(UPGRADE_SCRIPT)
    m = re.search(r"\(try_for_range,\s*\":i_slot\",\s*(\d+),\s*\":inv_cap\"\)", text)
    assert m, "Could not find the player-inv search loop"
    start = int(m.group(1))
    assert start >= 10, (
        f"Player-inv search starts at slot {start}, which is below the "
        "player's equipped gear (slots 0-9). This would let the search "
        "consider the player's own equipped items as candidates for "
        "swapping onto the troop, which would un-equip the player."
    )
    # Pin: this is the slot right above ek_food (9). If `dplmc_ek_alt_items_end`
    # moves up, the test must follow it.
    # Note: we cannot easily read header_items.py constants here, so we
    # just assert >= 10 as a floor.
    assert start <= 14, (
        f"Player-inv search starts at slot {start}, well above "
        "ek_food (=9). Either the constant changed or there's a "
        "magic-number bug. Update this test's bound or the source."
    )


@pytest.mark.bandit
def test_temp_array_lock_is_respected_in_search():
    """The player-inv search must skip slots locked in `trp_temp_array_lock`.

    Without the lock check, the same item is offered to multiple troops
    in a single Apply click — leading to duplicate equpping or items
    being assigned to a slot whose `:best_slot` is below 10 (i.e. a slot
    in the player's own equipped range).
    """
    text = read_text(UPGRADE_SCRIPT)
    assert re.search(
        r'\(troop_slot_eq,\s*"trp_temp_array_lock",\s*":i_slot",\s*0\)',
        text,
    ), (
        f"`{UPGRADE_SCRIPT}` does not respect `trp_temp_array_lock` in the "
        "player-inv search loop. Without the lock, multiple troops may "
        "be assigned the same player-inv item in one click, leaving "
        "heroes partially equipped."
    )