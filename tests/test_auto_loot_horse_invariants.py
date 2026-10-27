"""Tests for the auto-loot system and the horse-loss bug.

User-reported 2026-10-04: "My horse is gone, when i play the game my horse
and companion horse is gone. I think is the problem: 1. When i attack Castle
or town. 2. Auto upgrade equipment after battle."

Root cause (in `dplmc_auto_loot_troop.py`):
  - The script iterates `try_for_range, ":i_slot", ek_head, ek_food`
    (slots 4..9), which INCLUDES `ek_horse` (slot 8).
  - For each armor/horse slot, it deletes the troop's current item
    (`troop_set_inventory_slot, ":troop", ":i_slot", -1`) before scanning
    the loot pool.
  - If `:upg_horses != 0` AND the troop had a horse, the horse goes to the
    pool. The script then searches the pool for a better horse and assigns
    it only if `score > best_horse_val` (which starts at 0).
  - If no horse in the pool beats the original (or the pool has NO horses
    at all), `:best_horse_val` stays at 0, `:best_horse_slot` stays at -1,
    and the assignment branch never fires. **The troop ends up with no
    horse permanently.**

The fix shape is one of:
  (a) Skip `:upg_horse` deletion entirely — only swap if a strictly better
      horse exists in the pool, otherwise leave the original in place.
  (b) Set `:best_horse_val` to the current horse's score before deletion,
      so the original is always re-assigned if nothing better is found.

These tests pin the bug down without touching the engine.
"""
from __future__ import annotations

import re

import pytest

from tests._helpers import read_text


DPLMC_AUTO_LOOT_TROOP = "scripts/dplmc_auto_loot_troop.py"


# Marker: the loop that handles ek_head..ek_food (armor + horse).
_EK_LOOP_RE = re.compile(
    r"\(try_for_range,\s*\":i_slot\",\s*ek_head,\s*ek_food\)"
)


def _ek_loop_block(text: str) -> str:
    """Return the slice from `(try_for_range, ":i_slot", ek_head, ek_food)`
    up to the next `(try_end)` at the same indentation level.

    This is the loop that processes armor AND horse slots in
    dplmc_auto_loot_troop.py — the loop where the horse gets deleted.
    """
    m = _EK_LOOP_RE.search(text)
    if not m:
        return ""
    # Walk forward, counting try_begin depth; stop at the matching try_end.
    depth = 1
    pos = m.end()
    while pos < len(text) and depth > 0:
        next_begin = text.find("(try_begin)", pos)
        next_else = text.find("(else_try)", pos)
        next_end = text.find("(try_end)", pos)
        candidates = sorted(
            [(c, t) for c, t in [
                (next_begin, "begin"),
                (next_else, "else"),  # doesn't change depth
                (next_end, "end"),
            ] if c != -1]
        )
        if not candidates:
            return ""
        c, t = candidates[0]
        if t == "begin":
            depth += 1
        elif t == "end":
            depth -= 1
        pos = c + 1
    return text[m.start():pos]


# ---------------------------------------------------------------------------
# Bug — Horse deletion is unconditional; original is lost when nothing better
# is found in the pool.
# ---------------------------------------------------------------------------


@pytest.mark.bandit
def test_horse_inventory_kept_when_no_better_in_pool():
    """The dplmc auto-loot script must NOT leave ek_horse empty when the
    pool contains no better horse.

    Symptom: troop's horse disappears after every battle/town attack.
    Repro: the loop iterates ek_head..ek_food (which includes ek_horse = 8)
    and unconditionally deletes the troop's current horse before searching
    the pool. If the pool has no horses (typical for inland battles), the
    troop ends up with no horse.

    Fix shape:
      (a) Skip the deletion when `:upg_horses != 0` AND the troop's current
          horse score is already 0 (no original to compare against), OR
      (b) Initialize `:best_horse_val` to the original horse's score
          BEFORE the deletion so the original is always re-assigned if no
          pool horse is strictly better.

    Whichever fix shape is chosen, the test asserts that:
      - the loop exists,
      - it operates on `ek_horse`,
      - and it does NOT unconditionally `troop_set_inventory_slot, ":troop",
        ":i_slot", -1` for `:i_slot == ek_horse` without a "no original"
        guard.
    """
    text = read_text(DPLMC_AUTO_LOOT_TROOP)
    block = _ek_loop_block(text)
    assert block, (
        "Could not find the ek_head..ek_food loop in dplmc_auto_loot_troop.py. "
        "If you renamed the loop, update `_ek_loop_block`."
    )

    # The block must reference ek_horse (otherwise this isn't the right loop).
    assert "ek_horse" in block, (
        "BUG REPRO: The ek_head..ek_food loop in dplmc_auto_loot_troop.py "
        "doesn't mention ek_horse. Either the loop was narrowed, or the "
        "horse-loss is happening elsewhere."
    )

    # Look for the unconditional horse deletion: a branch where the script
    # sets ":troop"'s ek_horse slot to -1 without checking whether a
    # replacement has been found.
    # Pattern: (troop_set_inventory_slot, ":troop", ":i_slot", -1) AND
    # a prior (eq, ":i_slot", ek_horse) check. The fix must be SOMEWHERE
    # in the script (capture the original before the delete, OR baseline
    # :best_horse_val afterwards) — we accept either.
    delete_re = re.compile(
        r'\(troop_set_inventory_slot,\s*":troop",\s*":i_slot",\s*-1\)'
    )
    # Read the FULL script (not just the loop block) so we can detect
    # fixes that live outside the loop body (capture-before + assign-after).
    full_text = read_text(DPLMC_AUTO_LOOT_TROOP)
    for m in delete_re.finditer(block):
        # Look backward ~600 chars for an (eq, ":i_slot", ek_horse) check.
        preceding = block[max(0, m.start() - 600) : m.start()]
        if re.search(r'\(eq,\s*":i_slot",\s*ek_horse\)', preceding):
            # Acceptable guards (any of these):
            guard_patterns = [
                # Capture-and-keep guard inside the loop body
                r'\(troop_get_inventory_slot,\s*":[a-z_][\w]*",\s*":troop",\s*ek_horse\)',
                # Score-baseline guard
                r'\(assign,\s*":best_horse_val",\s*":[a-z_]+\)"',
                # Negation guard
                r'\(troop_slot_eq,[^,]+,\s*":i_slot",\s*-1\)',
            ]
            guarded_near = any(
                re.search(p, preceding, re.MULTILINE)
                for p in guard_patterns
            )
            # Also accept a baseline that lives OUTSIDE the loop
            # (capture-before + assign-after).
            baseline_after_loop = re.search(
                r'\(assign,\s*":best_horse_val",\s*":[a-z_][a-z0-9_]*"\)',
                full_text,
            )
            assert guarded_near or baseline_after_loop, (
                "BUG REPRO: The horse slot is being deleted in the "
                "ek_head..ek_food loop of dplmc_auto_loot_troop.py without "
                "any guard that captures the original score (inside the "
                "loop) or baselines `:best_horse_val` after the loop. "
                "This causes the troop's horse to disappear whenever the "
                "loot pool has no horse (typical for non-cavalry battles). "
                "Symptom: 'My horse is gone'.\n"
                "Fix shape: BEFORE deleting ek_horse, capture the original "
                "horse's score into a local like `:orig_horse_score`, "
                "THEN after the loop, seed `:best_horse_val` with it. That "
                "way the post-pool `best_horse_val > 0` check still passes "
                "when no pool horse beats it, and the troop keeps its "
                "original."
            )


# ---------------------------------------------------------------------------
# Companion horses — the same bug propagates to companions via
# dplmc_auto_loot_all.py calling dplmc_auto_loot_troop per companion.
# ---------------------------------------------------------------------------


@pytest.mark.bandit
def test_companion_horse_loss_path_exists():
    """`dplmc_auto_loot_all.py` calls `dplmc_auto_loot_troop` per companion.

    If `dplmc_auto_loot_troop` has the horse-deletion bug, EVERY companion
    also loses their horse on every loot cycle. This test enforces that
    the caller exists (so the bug is reachable for companions too).
    """
    text = read_text("scripts/dplmc_auto_loot_all.py")
    assert "dplmc_auto_loot_troop" in text, (
        "Expected `dplmc_auto_loot_all.py` to call `dplmc_auto_loot_troop` "
        "per companion. If you renamed the script, update this test."
    )


@pytest.mark.bandit
def test_original_horse_is_not_scored_when_equipment_slot_is_empty():
    """Auto-loot may only ask the item-scoring script to score a real horse.

    Troops without a horse have -1 in ek_horse. Scoring that sentinel can
    produce a burst of script errors when auto-loot processes the party.
    """
    text = read_text(DPLMC_AUTO_LOOT_TROOP)
    capture = text.index(
        '(troop_get_inventory_slot, ":orig_horse", ":troop", ek_horse)'
    )
    score = text.index(
        '(call_script, "script_dplmc_get_item_score_with_imod", ":orig_horse", ":orig_imod")',
        capture,
    )
    assert re.search(r'\(ge, ":orig_horse", 0\)', text[capture:score]), (
        "The original horse score call must be skipped when ek_horse is empty (-1)."
    )


@pytest.mark.bandit
def test_every_item_score_call_rejects_empty_item_slots():
    """All autoloot score calls must validate their item ID before scoring."""
    text = read_text(DPLMC_AUTO_LOOT_TROOP)
    calls = list(re.finditer(
        r'\(call_script, "script_dplmc_get_item_score_with_imod",\s*"(:[^\"]+)"',
        text,
    ))
    assert calls, "Expected the autoloot script to score candidate items."
    for call in calls:
        item_var = call.group(1)
        preceding = text[max(0, call.start() - 600):call.start()]
        assert re.search(
            r'\(ge,\s*"%s",\s*0\)' % re.escape(item_var), preceding
        ), "Item score call for %s is not guarded against the -1 empty-slot sentinel." % item_var


@pytest.mark.bandit
def test_original_horse_is_only_returned_to_loot_if_replaced():
    """Keep the original in its temporary cache unless a better horse wins.

    The previous flow both appended the original horse to the loot inventory
    and re-equipped it from the cached ek_horse slot, creating a duplicate.
    """
    text = read_text(DPLMC_AUTO_LOOT_TROOP)
    horse_branch_start = text.index(
        "(eq, \":i_slot\", ek_horse), # it's a horse slot"
    )
    horse_branch_end = text.index("(try_end),", horse_branch_start)
    horse_branch = text[horse_branch_start:horse_branch_end]
    assert '(troop_set_inventory_slot, ":troop", ":i_slot", -1)' in horse_branch
    assert '(troop_add_item, ":pool", ":item", ":imod")' not in horse_branch, (
        "Do not copy the original horse into loot while it is also cached for re-equipping."
    )

    # A replaced horse still belongs in the pool; the unchanged cached horse
    # should instead be restored directly to ek_horse and cleared from cache.
    best_horse_assignment = text.index(
        '(assign, ":best_slot", ":best_horse_slot")'
    )
    end = text.index('# (try_for_range, ":i_slot", ek_item_0, ek_head)', best_horse_assignment)
    assignment = text[best_horse_assignment:end]
    assert '(troop_set_inventory_slot, ":troop", ek_horse, ":item")' in assignment
    assert '(troop_set_inventory_slot, ":pool", ":best_slot", -1)' in assignment
    assert '(neq, ":best_slot", ek_horse)' in assignment
    assert '(troop_add_item, ":pool", ":old_horse", ":old_horse_imod")' in assignment
    assert '(troop_set_inventory_slot, ":pool", ek_horse, -1)' in assignment


# ---------------------------------------------------------------------------
# Sanity: the loop must NOT touch ek_food (slot 9) — it's food, not equipment.
# ---------------------------------------------------------------------------


@pytest.mark.bandit
def test_horse_loop_does_not_touch_ek_food():
    """The ek_head..ek_food loop must end BEFORE ek_food (slot 9).

    The Python range `range(ek_head, ek_food)` in Python sense would be
    exclusive at the high end, but module-system `try_for_range` is
    exclusive at the LOW end (`[low, high)`). So `try_for_range, ek_head,
    ek_food` = [4, 9), which DOES include ek_horse=8 but NOT ek_food=9.

    This test verifies the loop's high-end is ek_food (not ek_food+1 or
    some larger value), confirming food isn't being processed.
    """
    text = read_text(DPLMC_AUTO_LOOT_TROOP)
    m = _EK_LOOP_RE.search(text)
    assert m, "ek_head..ek_food loop not found"
    # The captured upper bound must literally be `ek_food`, not a constant
    # or a number. We rely on the regex literal above; this is a smoke test.
    # (The regex already enforces `ek_food`.)
    assert "ek_food" in m.group(0)
    # And NOT something larger like ek_food + 1.
    bigger = re.search(
        r"\(try_for_range,\s*\":i_slot\",\s*ek_head,\s*ek_food\s*\+\s*1\)",
        text,
    )
    assert not bigger, (
        "BUG: The ek_head..ek_food loop has been changed to ek_head..ek_food+1. "
        "This would also iterate ek_food (slot 9), which is food. Don't process "
        "food in the equipment loop — use a separate handler."
    )
