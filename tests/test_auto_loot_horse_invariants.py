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
    # a prior (eq, ":i_slot", ek_horse) check. If both appear within ~200
    # chars without an intervening guard, that's the bug.
    delete_re = re.compile(
        r'\(troop_set_inventory_slot,\s*":troop",\s*":i_slot",\s*-1\)'
    )
    for m in delete_re.finditer(block):
        # Look backward ~250 chars for an (eq, ":i_slot", ek_horse) check.
        preceding = block[max(0, m.start() - 250) : m.start()]
        if re.search(r'\(eq,\s*":i_slot",\s*ek_horse\)', preceding):
            # This is the horse deletion. Verify there's NO guard between
            # the eq and the delete that ensures the troop HAD a horse
            # that we can re-equip. A guard could be:
            #   (troop_get_inventory_slot, ":prev", ":troop", ":i_slot"),
            #   (ge, ":prev", 0),
            #   ... score lookup ...
            #   (assign, ":best_horse_val", ":prev_score"),
            # If none of these patterns appear between the eq and the
            # delete, the bug is present.
            guard_patterns = [
                # Capture-and-keep guard
                r'\(troop_get_inventory_slot,\s*":prev[_\w]*",\s*":troop",\s*":i_slot"\)',
                # Score-baseline guard
                r'\(assign,\s*":best_horse_val",\s*":[a-z_]+\)"',
                # Negation guard
                r'\(troop_slot_eq,[^,]+,\s*":i_slot",\s*-1\)',
            ]
            guarded = any(
                re.search(p, preceding, re.MULTILINE)
                for p in guard_patterns
            )
            assert guarded, (
                "BUG REPRO: The horse slot is being deleted in the "
                "ek_head..ek_food loop of dplmc_auto_loot_troop.py without "
                "any guard that captures the original score or skips deletion "
                "when the troop had no horse. This causes the troop's horse "
                "to disappear whenever the loot pool has no horse (typical "
                "for non-cavalry battles). Symptom: 'My horse is gone'.\n"
                "Fix shape: BEFORE deleting ek_horse, capture the original "
                "horse's score and seed `:best_horse_val` with it. That way "
                "the post-pool `best_horse_val > 0` check still passes when "
                "no pool horse beats it, and the troop keeps its original."
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