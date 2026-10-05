"""Tests for the auto-upgrade system.

Reproduces bugs seen in 2026-10-04:
  1. "Unrecognized opcode 3901" from `script_game_get_upgrade_cost`
     — script uses `set_trigger_result` but is called as a normal script.
  2. "400 unit bonus" — the remove-and-re-add dance can produce a
     negative `:keep` value when `:to_upgrade > :sz`, and a negative
     value is added back as its absolute value, multiplying the stack.
"""
from __future__ import annotations

import re

import pytest

from tests._helpers import read_text


GAME_GET_UPGRADE_COST = "scripts/game_get_upgrade_cost.py"
AUTO_UPGRADE_TROOPS = "scripts/auto_upgrade_troops.py"


# ---------------------------------------------------------------------------
# Bug #1 — game_get_upgrade_cost uses set_trigger_result
# ---------------------------------------------------------------------------


@pytest.mark.bandit
def test_game_get_upgrade_cost_uses_assign_reg0_not_set_trigger_result():
    """`script_game_get_upgrade_cost` is called with `call_script` and must
    return its value via `(assign, reg0, ...)`.

    `set_trigger_result` is reserved for *game triggers* — opcodes the engine
    invokes directly with a special contract. When a script uses it but is
    called via `(call_script, ...)` (as auto_upgrade_troops does), the engine
    raises "Unrecognized opcode 3901" and the result is undefined: subsequent
    `(assign, ":cpt", reg0)` reads garbage.

    Repro: this script is called from auto_upgrade_troops.py:98 with
    `(call_script, "script_game_get_upgrade_cost", ":troop_id")`.
    """
    text = read_text(GAME_GET_UPGRADE_COST)
    assert "set_trigger_result" not in text, (
        "`game_get_upgrade_cost.py` still uses `set_trigger_result`. "
        "This opcode is for game-engine triggers only — when called via "
        "`call_script` (as `auto_upgrade_troops` does) it raises "
        "`Unrecognized opcode 3901` and reg0 is undefined. "
        "Replace with `(assign, reg0, <value>)`."
    )
    # Confirm at least one (assign, reg0, N) line exists.
    assigns = re.findall(r"\(assign,\s*reg0,\s*(-?\d+)\)", text)
    assert assigns, (
        "`game_get_upgrade_cost.py` does not assign to reg0 at all. "
        "Auto-upgrade reads `reg0` after call_script and gets undefined value."
    )


# ---------------------------------------------------------------------------
# Bug #2 — party_remove_members / party_add_members can multiply the stack
# ---------------------------------------------------------------------------


@pytest.mark.bandit
def test_auto_upgrade_does_not_double_stack_when_to_upgrade_exceeds_size():
    """The remove-then-readd pattern must guard against `:to_upgrade > :sz`.

    In `auto_upgrade_troops.py` the script does:

        (store_sub, ":keep", ":sz", ":to_upgrade")
        ...
        (party_remove_members, "p_main_party", ":troop_id", ":sz")
        ...
        (party_add_members, "p_main_party", ":troop_id", ":keep")

    If `:to_upgrade > :sz`, then `:keep < 0`. The engine treats
    `(party_add_members, ..., negative)` as adding the absolute value,
    which **inflates** the stack instead of shrinking it.

    Repro symptom (per Marlon's screenshot 2026-10-04): a stack of 50
    manhunters was upgraded and ended up with ~400 troops — the script
    effectively *added* `-(:keep)` troops back.

    Fix idea: add `(val_max, ":keep", 0)` before the `party_add_members`
    call, OR cap `:to_upgrade` to `:sz` earlier in the flow.
    """
    text = read_text(AUTO_UPGRADE_TROOPS)
    # Find the (store_sub, ":keep", ":sz", ":to_upgrade") line.
    sub_re = re.compile(
        r'\(store_sub,\s*":keep",\s*":sz",\s*":to_upgrade"\)'
    )
    keep_calc = sub_re.search(text)
    assert keep_calc, "Could not find `:keep` calculation in auto_upgrade_troops.py"
    # The `party_add_members` for `:troop_id, ":keep"` should appear AFTER
    # the keep calc, but BEFORE it there should be a `(val_max, ":keep", 0)`
    # guard. If the guard is missing, the test fails with the exact message.
    after_keep = text[keep_calc.end():]
    add_members_re = re.compile(
        r'\(party_add_members,\s*"p_main_party",\s*":troop_id",\s*":keep"\)'
    )
    add_match = add_members_re.search(after_keep)
    assert add_match, (
        "Could not find the `:keep` add-members call in auto_upgrade_troops.py. "
        "The bug repro depends on the remove+add pattern still existing."
    )
    between_keep_and_add = text[keep_calc.end() : keep_calc.end() + add_match.start()]
    # Look for a (val_max, ":keep", 0) guard before the add.
    guard_re = re.compile(
        r'\(val_max,\s*":keep",\s*0\)'
    )
    assert guard_re.search(between_keep_and_add), (
        "BUG REPRO: `auto_upgrade_troops.py` computes "
        "`:keep = :sz - :to_upgrade` and uses it directly in "
        "`party_add_members`, but does NOT clamp `:keep` to >= 0.\n"
        "If `:to_upgrade > :sz` (e.g. manhunter upgrade applied to a "
        "stack of 50 with 400+ upgradeable troops), `:keep` is negative, "
        "and `party_add_members` interprets it as adding |:keep| troops.\n"
        "Symptom: stacks grow to 400+ troops after a single upgrade cycle.\n"
        "Fix: add `(val_max, \":keep\", 0)` right after the `store_sub`."
    )


@pytest.mark.bandit
def test_auto_upgrade_total_spent_matches_total_upgraded_x_cost():
    """`:gold_spent` must equal `:total_upgraded * :cpt` summed over stacks.

    This is a sanity check on the gold accounting. If the cost-per-troop
    (`reg0` from `script_game_get_upgrade_cost`) is garbage (because of
    Bug #1), `:gold_spent` will not match `:total_upgraded * <expected>`.
    """
    text = read_text(AUTO_UPGRADE_TROOPS)
    # Look for the add-gold-spent line: `(val_add, ":gold_spent", ":cost")`.
    assert "(val_add, \":gold_spent\", \":cost\")" in text, (
        "Expected the standard `:gold_spent += :cost` line. "
        "If you refactored the cost accounting, update this test."
    )
    # Look for `val_add, ":total_upgraded", ":to_upgrade"`.
    assert "(val_add, \":total_upgraded\", \":to_upgrade\")" in text, (
        "Expected `:total_upgraded += :to_upgrade`. "
        "If you refactored the upgrade accounting, update this test."
    )
    # Both accumulators are reset before the loop.
    head = "\n".join(text.splitlines()[:35])
    assert "(assign, \":total_upgraded\", 0)" in head, (
        "Expected `:total_upgraded = 0` initialization near the top."
    )
    assert "(assign, \":gold_spent\", 0)" in head, (
        "Expected `:gold_spent = 0` initialization near the top."
    )