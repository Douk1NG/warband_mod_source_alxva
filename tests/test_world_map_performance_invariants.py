"""Performance invariants for world-map scripts.

User-reported 2026-10-04: extreme lag while navigating the world map.
This file contains static-analysis tests that detect two common sources
of Warband module lag:
  (1) O(n²) loops (try_for_range nested inside another try_for_range over a
     large range like active_npcs or towns).
  (2) Hot-path opcode bloat: a simple_trigger that runs frequently (every
     few seconds) calling many `store_random` / `call_script` / `is_between`
     ops per iteration.

These are STATIC tests — they count tokens in the .py source. They do not
measure wall-clock time. They detect patterns that are well-known to
cause measurable frame drops on mid-range hardware.

Run with:  python -m pytest tests/test_world_map_performance_invariants.py -v
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests._helpers import REPO_ROOT, read_text


SIMPLE_TRIGGERS_DIR = REPO_ROOT / "source" / "simple_triggers"
TRIGGERS_DIR = REPO_ROOT / "source" / "triggers"


def _iter_python_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(p for p in directory.glob("*.py") if p.is_file())


# Map: trigger file -> (interval_in_hours, loop_range_regex).
# We bias loop detection toward the largest ranges known to be slow:
#   active_npcs_begin..end     (~200-300 iterations)
#   towns_begin..end           (~60 iterations)
#   villages_begin..end        (~80 iterations)
#   centers_begin..end         (~140 iterations)
#   kingdoms_begin..end        (~8 iterations, ignore)
LARGE_RANGE_OPENERS = re.compile(
    r"\(try_for_range,\s*\"?:(\w+)\"?,\s*"
    r"(active_npcs_begin|active_npcs_end|towns_begin|towns_end|"
    r"villages_begin|villages_end|centers_begin|centers_end|"
    r"lords_begin|lords_end|companions_begin|companions_end)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Test 1 — Nested try_for_range over a large range
# ---------------------------------------------------------------------------


@pytest.mark.performance
def test_no_nested_loops_over_large_ranges_in_simple_triggers():
    """No simple_trigger may nest a try_for_range inside another over a
    large range (active_npcs, towns, villages, etc.).

    A nested `active_npcs × active_npcs` is O(n²) = ~40000 iterations per
    trigger fire. With a trigger interval of 1 hour, that's 960000
    operations/day. Symptom: visible frame drops while on the world map.

    The rule is: if you find two `try_for_range` blocks in the same file,
    the inner one must use a SMALL range (party slots, item slots, etc.)
    — not a large range like active_npcs.
    """
    offenders: list[tuple[str, str, str]] = []  # (file, outer_var, inner_var)
    for path in _iter_python_files(SIMPLE_TRIGGERS_DIR):
        text = path.read_text(encoding="utf-8", errors="replace")
        # Find all try_for_range lines.
        for_range_iter = list(
            re.finditer(
                r"\(try_for_range,\s*\"?:(\w+)\"?,\s*(\w+),\s*(\w+)\)",
                text,
            )
        )
        # Build ranges of each try_for_range in the file.
        ranges = []
        for m in for_range_iter:
            var, lo, hi = m.group(1), m.group(2), m.group(3)
            # Heuristic: classify as large if `lo` or `hi` matches a known
            # big-range constant. We check both, since the convention is
            # `try_for_range, ":x", BIG_BEGIN, BIG_END`.
            is_large = bool(
                re.search(
                    r"^(active_npcs|towns|villages|centers|lords|companions|"
                    r"heroes|parties|factions)",
                    lo + hi,
                    re.IGNORECASE,
                )
            )
            ranges.append((m.start(), m.end(), var, lo, hi, is_large))
        # For each pair (outer, inner) where outer.end < inner.start AND
        # both are large, flag.
        for i, outer in enumerate(ranges):
            outer_start, outer_end, outer_var, outer_lo, outer_hi, outer_large = outer
            if not outer_large:
                continue
            for inner in ranges[i + 1 :]:
                in_start, in_end, in_var, in_lo, in_hi, in_large = inner
                if not in_large:
                    continue
                # Make sure the inner loop is truly nested (within the
                # outer body's extent, which we approximate as 1500 chars).
                if outer_end <= in_start <= outer_end + 1500:
                    offenders.append(
                        (str(path.relative_to(REPO_ROOT)), outer_var, in_var)
                    )

    assert not offenders, (
        "Nested try_for_range over LARGE ranges detected (O(n²) hot path):\n"
        + "\n".join(
            f"  {f}: outer :{loop_var} contains inner :{inner_var}"
            for f, loop_var, inner_var in offenders
        )
        + "\n\nFix shape: replace the inner loop with a precomputed map or "
        "filter the outer loop (e.g. only iterate heroes in the player's faction "
        "instead of all active_npcs). See `decide_faction_ai_flag.py` and "
        "`decide_vassal_ai.py` for examples of correctly filtered inner loops."
    )


# ---------------------------------------------------------------------------
# Test 2 — Total try_for_range count per simple_trigger (hot-path budget)
# ---------------------------------------------------------------------------


@pytest.mark.performance
def test_simple_trigger_loop_budget_per_file():
    """A simple_trigger file should not contain more than 6 try_for_range
    blocks over large ranges in its body. More than that and a single
    trigger fire becomes expensive.

    This is a configurable threshold. Bump it if you legitimately add more
    loops; the goal is to make a refactor that quietly doubles loop count
    fail loudly.
    """
    THRESHOLD = 6
    offenders: list[tuple[str, int]] = []
    for path in _iter_python_files(SIMPLE_TRIGGERS_DIR):
        text = path.read_text(encoding="utf-8", errors="replace")
        large_loops = 0
        for m in re.finditer(
            r"\(try_for_range,\s*\"?:(\w+)\"?,\s*(\w+),\s*(\w+)\)",
            text,
        ):
            lo, hi = m.group(2), m.group(3)
            if re.search(
                r"^(active_npcs|towns|villages|centers|lords|companions|"
                r"heroes|parties|factions)",
                lo + hi,
                re.IGNORECASE,
            ):
                large_loops += 1
        if large_loops > THRESHOLD:
            offenders.append((str(path.relative_to(REPO_ROOT)), large_loops))

    assert not offenders, (
        f"Simple triggers exceeding the {THRESHOLD}-large-loop budget:\n"
        + "\n".join(f"  {f}: {n} large loops" for f, n in offenders)
        + "\n\nEither split the trigger into multiple files with smaller "
        "intervals, or replace one of the loops with a precomputed list."
    )


# ---------------------------------------------------------------------------
# Test 3 — call_script count in common volume per file
# ---------------------------------------------------------------------------


CALL_SCRIPT_RE = re.compile(
    r"\(call_script,\s*\"script_(\w+)\","
)


@pytest.mark.performance
def test_simple_trigger_call_script_budget_per_file():
    """A simple_trigger should not call more than 10 distinct scripts.

    Each call_script adds engine dispatch overhead. Many call_scripts in
    a frequently-fired trigger add up.

    Threshold = 10. Adjust if you add more scripts intentionally.
    """
    THRESHOLD = 10
    offenders: list[tuple[str, int, list[str]]] = []
    for path in _iter_python_files(SIMPLE_TRIGGERS_DIR):
        text = path.read_text(encoding="utf-8", errors="replace")
        calls = CALL_SCRIPT_RE.findall(text)
        unique_calls = sorted(set(calls))
        if len(unique_calls) > THRESHOLD:
            offenders.append(
                (str(path.relative_to(REPO_ROOT)), len(unique_calls), unique_calls)
            )

    assert not offenders, (
        f"Simple triggers exceeding the {THRESHOLD}-call_script budget:\n"
        + "\n".join(
            f"  {f}: {n} scripts -> {calls}"
            for f, n, calls in offenders
        )
    )


# ---------------------------------------------------------------------------
# Test 4 — store_random in simple_triggers
# ---------------------------------------------------------------------------


STORE_RANDOM_RE = re.compile(r"\(store_random(?:_in_range)?,")


@pytest.mark.performance
def test_simple_trigger_store_random_budget():
    """Each simple_trigger should use at most 8 `store_random` ops.

    Random ops are cheap individually but they're a smell: a hot path
    that uses many `store_random` calls is usually doing per-NPC random
    behavior, which can usually be batched.
    """
    THRESHOLD = 8
    offenders: list[tuple[str, int]] = []
    for path in _iter_python_files(SIMPLE_TRIGGERS_DIR):
        text = path.read_text(encoding="utf-8", errors="replace")
        n = len(STORE_RANDOM_RE.findall(text))
        if n > THRESHOLD:
            offenders.append((str(path.relative_to(REPO_ROOT)), n))

    assert not offenders, (
        f"Simple triggers with >{THRESHOLD} store_random ops:\n"
        + "\n".join(f"  {f}: {n}" for f, n in offenders)
    )


# ---------------------------------------------------------------------------
# Test 5 — store_random_in_range over active_npcs
# ---------------------------------------------------------------------------


@pytest.mark.performance
def test_no_store_random_in_range_within_large_loops_in_simple_triggers():
    """Detect `store_random_in_range` (or any random op) INSIDE a large
    try_for_range loop body. This is a strong indicator of per-NPC
    randomness, which is the worst case for world-map lag.

    Example anti-pattern:
            (try_for_range, ":i", active_npcs_begin, active_npcs_end),
                (store_random_in_range, ":r", 0, 100),
                (troop_set_slot, ":i", slot_x, ":r"),
            (try_end),

    Fix shape: compute one random number per trigger fire and reuse it,
    or batch the slot writes after the loop.
    """
    offenders: list[tuple[str, int]] = []
    for path in _iter_python_files(SIMPLE_TRIGGERS_DIR):
        text = path.read_text(encoding="utf-8", errors="replace")
        # Find every large try_for_range and check whether a store_random
        # appears within ~1500 chars after it (i.e. inside the loop body).
        for m in re.finditer(
            r"\(try_for_range,\s*\"?:(\w+)\"?,\s*(\w+),\s*(\w+)\)",
            text,
        ):
            lo, hi = m.group(2), m.group(3)
            if not re.search(
                r"^(active_npcs|towns|villages|centers|lords|companions|"
                r"heroes|parties|factions)",
                lo + hi,
                re.IGNORECASE,
            ):
                continue
            body = text[m.end() : m.end() + 1500]
            randoms = STORE_RANDOM_RE.findall(body)
            if randoms:
                offenders.append(
                    (str(path.relative_to(REPO_ROOT)), len(randoms))
                )

    assert not offenders, (
        "store_random inside large try_for_range loops (per-NPC random is "
        "the worst-case world-map lag pattern):\n"
        + "\n".join(
            f"  {f}: {n} store_random ops inside large loops"
            for f, n in offenders
        )
        + "\n\nFix shape: hoist `store_random_in_range` BEFORE the loop and "
        "reuse the value, OR move randomness to a one-shot per-cycle "
        "trigger instead of per-NPC."
    )


# ---------------------------------------------------------------------------
# Test 6 — nested try_for_range in triggers/ (manual triggers, called once
# per event but can still be expensive)
# ---------------------------------------------------------------------------


@pytest.mark.performance
def test_no_nested_large_loops_in_manual_triggers():
    """Same rule as Test 1 but for `triggers/` (manual triggers).

    Manual triggers fire less often but they can still block the main
    thread. Same nested-loop rule applies.
    """
    offenders: list[tuple[str, str, str]] = []
    for path in _iter_python_files(TRIGGERS_DIR):
        text = path.read_text(encoding="utf-8", errors="replace")
        for_range_iter = list(
            re.finditer(
                r"\(try_for_range,\s*\"?:(\w+)\"?,\s*(\w+),\s*(\w+)\)",
                text,
            )
        )
        ranges = []
        for m in for_range_iter:
            var, lo, hi = m.group(1), m.group(2), m.group(3)
            is_large = bool(
                re.search(
                    r"^(active_npcs|towns|villages|centers|lords|companions|"
                    r"heroes|parties|factions)",
                    lo + hi,
                    re.IGNORECASE,
                )
            )
            ranges.append((m.start(), m.end(), var, is_large))
        for i, outer in enumerate(ranges):
            if not outer[3]:
                continue
            for inner in ranges[i + 1 :]:
                if not inner[3]:
                    continue
                if outer[1] <= inner[0] <= outer[1] + 1500:
                    offenders.append(
                        (str(path.relative_to(REPO_ROOT)), outer[2], inner[2])
                    )

    assert not offenders, (
        "Nested large-range loops in manual triggers:\n"
        + "\n".join(
            f"  {f}: outer :{outer_var} contains inner :{inner_var}"
            for f, outer_var, inner_var in offenders
        )
    )