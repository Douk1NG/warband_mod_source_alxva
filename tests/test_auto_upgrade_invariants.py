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
def test_game_get_upgrade_cost_uses_set_trigger_result():
    """`script_game_get_upgrade_cost` is a *game trigger*, not a normal script.

    Game triggers MUST use `(set_trigger_result, reg0)` to return their value.
    The engine calls them directly (no `call_script`). Calling this script with
    `call_script` would raise "Unrecognized opcode 3901" because the engine
    treats the call site as a script reference, not a game-trigger reference.

    Confirmed correct form: `set_trigger_result` at the end of the body,
    plus `(assign, reg0, N)` chains inside the body to compute the cost.

    The real bug is in `auto_upgrade_troops.py`, which references this name
    via `(call_script, "script_game_get_upgrade_cost", ...)`. That call site
    should be removed entirely — the engine invokes this trigger on its
    own when a troop upgrade happens. See test below.
    """
    text = read_text(GAME_GET_UPGRADE_COST)
    body = "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("#")
    )
    assert "set_trigger_result" in body, (
        "`game_get_upgrade_cost.py` lost its `set_trigger_result`. "
        "This is a game trigger — the engine expects it to return via "
        "`set_trigger_result`, not `assign reg0`."
    )
    assigns = re.findall(r"\(assign,\s*reg0,\s*(-?\d+)\)", text)
    assert assigns, (
        "`game_get_upgrade_cost.py` has no `(assign, reg0, N)` chain."
    )


@pytest.mark.bandit
def test_auto_upgrade_troops_does_not_call_script_game_get_upgrade_cost():
    """`auto_upgrade_troops.py` must NOT call `script_game_get_upgrade_cost`.

    `game_get_upgrade_cost` is a game trigger invoked by the engine, not a
    normal script. Calling it via `(call_script, ...)` raises "Unrecognized
    opcode 3901" because the engine treats the call as a script reference
    and fails to find the game-trigger signature.

    If `auto_upgrade_troops` needs the upgrade cost, it should either:
      (a) compute the cost inline (same level-based formula), OR
      (b) call a separate helper script (not a game trigger).

    Symptom this prevents: "Unrecognized opcode 3901" in rgl_log.txt on
    every auto-upgrade cycle.
    """
    text = read_text("scripts/auto_upgrade_troops.py")
    body = "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("#")
    )
    assert "script_game_get_upgrade_cost" not in body, (
        "`auto_upgrade_troops.py` calls `script_game_get_upgrade_cost` via "
        "(call_script, ...). This is a game trigger — the engine calls it "
        "automatically when a troop upgrades. The (call_script, ...) form "
        "raises 'Unrecognized opcode 3901' and reg0 becomes undefined.\n"
        "Fix shape: remove the (call_script, 'script_game_get_upgrade_cost', ...) "
        "line AND the (assign, ':cpt', reg0) line that follows it. "
        "Compute the cost inline, OR call a separate helper script."
    )


@pytest.mark.bandit
def test_auto_upgrade_inline_cost_matches_engine_trigger_levels():
    """The gold estimate must stay aligned with the engine's level-cost table."""
    script = read_text(AUTO_UPGRADE_TROOPS)
    trigger = read_text(GAME_GET_UPGRADE_COST)
    for low, high, cost in (
        (0, 6, 10),
        (6, 11, 20),
        (11, 16, 40),
        (16, 21, 80),
        (21, 26, 120),
        (26, 31, 160),
    ):
        check = r'\(is_between, ":troop_level", %d, %d\)' % (low, high)
        assign = r'\(assign, ":cpt", %d\)' % cost
        assert re.search(check, script), "Missing inline level range %d..%d." % (low, high)
        assert re.search(assign, script), "Missing inline cost %d." % cost
        assert re.search(check, trigger), "Engine trigger no longer has range %d..%d." % (low, high)
        assert re.search(r'\(assign, reg0, %d\)' % cost, trigger), (
            "Engine trigger no longer returns cost %d." % cost
        )
    assert '(assign, ":cpt", 200)' in script
    assert '(assign, reg0, 200)' in trigger


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

    Repro symptom (per user screenshot 2026-10-04): a stack of 50
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
