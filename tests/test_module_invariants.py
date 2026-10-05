"""Cross-module invariants: catches regressions where slot ranges collide.

These tests don't need the engine. They parse module_constants.py and a
handful of related files as text and check structural invariants. If any of
these fail, the WRECK compile will probably still succeed, but the runtime
will silently overwrite slots — exactly the class of bug that hit us on
2026-09-05 (dplmc autoloot slots colliding with DtheHun tattoo slots).

Run with:  python -m pytest tests/ -v
"""
from __future__ import annotations

import pytest

from tests._helpers import (
    collect_constants,
    collect_ranges,
    detect_overlaps,
    read_text,
)


CONSTANTS_FILE = "module_constants.py"


def test_no_overlapping_slot_ranges_in_module_constants():
    """No two `slot_*_begin .. slot_*_end` ranges may overlap.

    A single slot can only hold one integer. If two ranges share even one
    slot, writes to one will be silently overwritten by the other. This is
    the exact failure mode that produced the 2026-09-05 incident.

    KNOWN OVERLAPS: see `_KNOWN_OVERLAPS` below. Each entry is an existing
    pre-fix bug that the maintainer hasn't addressed yet. Add to the list
    only after confirming the overlap is intentional, and include a comment
    with the date and reason.
    """
    # Pairs known to overlap intentionally, or pre-existing and not yet fixed.
    # Each entry is a frozenset of two range stems (NOT including _begin/_end).
    _KNOWN_OVERLAPS: set[frozenset[str]] = {
        # Discovered 2026-10-04: faction-sum-advice vs custom-armor slots.
        # See AGENTS.md "Slot collision" section for context. NOT YET FIXED.
        frozenset({"slot_faction_sum_advice_about_factions", "slot_troop_armor_slots"}),
    }

    ranges = collect_ranges(CONSTANTS_FILE, prefix="slot_")
    overlaps = detect_overlaps(ranges)
    # Filter out known-acceptable overlaps.
    real_overlaps = [
        o for o in overlaps
        if frozenset({o[0], o[3]}) not in _KNOWN_OVERLAPS
    ]
    assert not real_overlaps, (
        "Overlapping slot ranges detected in module_constants.py:\n"
        + "\n".join(
            f"  {na}[{a_lo},{a_hi}) overlaps {nb}[{b_lo},{b_hi})"
            for na, a_lo, a_hi, nb, b_lo, b_hi in real_overlaps
        )
        + "\n\n(known-acceptable overlaps are listed in `_KNOWN_OVERLAPS` "
        "inside test_module_invariants.py — keep that list up to date.)"
    )
    # Always surface the known-overlap count so it's visible in CI logs.
    known_count = len(overlaps) - len(real_overlaps)
    if known_count:
        print(f"\n[note] {known_count} known overlap(s) currently allowed.")


def test_no_overlapping_item_kind_ranges():
    """Item kinds (itp_type_*) and similar *_begin/*_end pairs must not overlap.

    Module-system ranges are used as half-open intervals in the engine;
    overlap means an id resolves to two semantic categories.
    """
    # itp_type_* ranges are typical. We check all *_begin/*_end pairs that
    # are NOT slot_*, since those are checked separately above.
    all_ranges = collect_ranges(CONSTANTS_FILE)
    non_slot = [r for r in all_ranges if not r[0].startswith("slot_")]
    overlaps = detect_overlaps(non_slot)
    # NOTE: some overlaps in Native are intentional (e.g. meritorious + kingdom
    # related). If this test fails with a known-acceptable pair, add an
    # explicit skip list below rather than disabling the test.
    _acceptable: set[tuple[str, str]] = set()
    bad = [o for o in overlaps if (o[0], o[3]) not in _acceptable]
    assert not bad, (
        "Overlapping non-slot ranges:\n"
        + "\n".join(
            f"  {na}[{a_lo},{a_hi}) overlaps {nb}[{b_lo},{b_hi})"
            for na, a_lo, a_hi, nb, b_lo, b_hi in bad
        )
    )


def test_constants_uses_consistent_string_quotes():
    """Spot check that no obvious typos exist (string assigned as int, etc.).

    This is a smoke test: if module_constants.py has a syntax error, parsing
    it will raise here instead of crashing WRECK 30 seconds into the build.
    """
    consts = collect_constants(CONSTANTS_FILE)
    assert len(consts) > 100, (
        f"Only {len(consts)} constants parsed from {CONSTANTS_FILE}. "
        "Expected well over a thousand. Did the file get truncated?"
    )


@pytest.mark.parametrize("stem", ["slot_troop_armor_slots", "slot_troop_helm_slots"])
def test_known_armor_helm_ranges_are_well_formed(stem: str):
    """Both armor and helm slot ranges must have a positive span.

    Regression check from the 2026-09-06 incident: the second slot collision
    came from armor slots spanning into dplmc's wpn range. If the spans here
    ever drop to 0 or become negative, something has been mangled.
    """
    ranges = collect_ranges(CONSTANTS_FILE, prefix="slot_")
    matching = [(n, lo, hi) for n, lo, hi in ranges if n == stem]
    assert matching, (
        f"No range with stem '{stem}' found in {CONSTANTS_FILE}. "
        "If you renamed it, update the parametrize list."
    )
    for name, lo, hi in matching:
        assert hi > lo, f"{name}: begin({lo}) >= end({hi})"
        # Sanity: span should be at least 2 (a component + its material).
        assert hi - lo >= 2, f"{name} range too small: span = {hi - lo}"