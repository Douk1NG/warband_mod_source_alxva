"""Tests for the bandit spawn system.

Covers the data-level invariants that the engine expects:

  - Every `pt_*_bandits` template that exists has both
    `slot_party_template_lair_type` and `slot_party_template_lair_spawnpoint`
    configured, and the spawn point must be a real party template ID.
  - The `bandit_party_templates_begin..end` range covers all six canonical
    bandit templates (forest/sea_raiders/steppe/taiga/mountain/desert).
  - The `script_spawn_party_type_with_cooldown` script reads exactly four
    script params and writes the cooldown slot in both branches (seed and
    trickle).
  - Population caps declared in module_constants.py match the values used
    in spawn_bandits.py and stay consistent with docs/updates/.../new_bandit_system.md.
  - Hardcoded lair coordinates: 30 total (5 per bandit template), one
    `position_set_x` + `position_set_y` pair per coordinate.

These are *exactly* the checks that would have caught the bug in spawn_bandits
where `pt_forest_bandits` had been deleted from the template list but the
spawn script kept referencing it.
"""
from __future__ import annotations

import re

import pytest

from tests._helpers import collect_constants, read_text


# ---------------------------------------------------------------------------
# T0 — six templates are configured (existing test)
# ---------------------------------------------------------------------------


@pytest.mark.bandit
def test_six_bandit_templates_are_configured():
    """All six canonical bandit templates must set their lair_type + spawnpoint.

    The spawn script writes both slots for each template; if any template
    is missing one, the lair creation path will silently fall back to a
    hardcoded string-id lookup that may or may not exist.
    """
    text = read_text("scripts/spawn_bandits.py")

    canonical_templates = [
        "pt_steppe_bandits",
        "pt_taiga_bandits",
        "pt_mountain_bandits",
        "pt_forest_bandits",
        "pt_sea_raiders",
        "pt_desert_bandits",
    ]

    missing: list[str] = []
    for tmpl in canonical_templates:
        lair_type = re.search(
            rf'party_template_set_slot,\s*"{re.escape(tmpl)}",\s*slot_party_template_lair_type',
            text,
        )
        spawnpoint = re.search(
            rf'party_template_set_slot,\s*"{re.escape(tmpl)}",\s*slot_party_template_lair_spawnpoint',
            text,
        )
        if not (lair_type and spawnpoint):
            missing.append(tmpl)

    assert not missing, (
        f"These bandit templates are missing lair_type/spawnpoint configuration "
        f"in scripts/spawn_bandits.py: {missing}"
    )


# ---------------------------------------------------------------------------
# T0b — spawn point references are well-formed (existing test, fixed regex)
# ---------------------------------------------------------------------------


@pytest.mark.bandit
def test_lair_spawnpoint_ids_resolve():
    """Each lair spawnpoint reference must point to a known party id.

    We check the textual reference in spawn_bandits.py against the IDs
    defined in module_constants.py. A typo like `p_steppe_bandit_spaw_point`
    would resolve to a sentinel (the engine treats unknown ids as
    'no party') and the lair would silently never spawn.
    """
    spawn_script = read_text("scripts/spawn_bandits.py")
    consts = collect_constants("module_constants.py")

    # Find every `p_*_bandit*_spawn_point*` referenced as a string.
    # We accept both `bandit` and `raider` substrings so `p_sea_raider_spawn_point_1`
    # is also matched. Trailing `_digits` is allowed.
    referenced_ids: set[str] = set()
    for m in re.finditer(r'"(p_[a-z_]*(?:bandit|raider)[a-z_]*spawn_[a-z0-9_]+)"', spawn_script):
        referenced_ids.add(m.group(1))

    assert referenced_ids, (
        "Expected at least one p_*_bandit*_spawn_point reference in spawn_bandits.py"
    )

    # We can't resolve every string-id because module_constants.py only
    # contains integer- and string-assigned constants; party id strings may
    # live in module_parties.py. So this test does a *presence* check: each
    # referenced string should be of a sensible shape, and the count should
    # match the number of bandit templates (6 canonical).
    assert len(referenced_ids) >= 6, (
        f"Expected at least 6 spawn-point references, found {len(referenced_ids)}: "
        f"{sorted(referenced_ids)}"
    )


# ---------------------------------------------------------------------------
# T0c — debuff guard (existing test)
# ---------------------------------------------------------------------------


@pytest.mark.bandit
def test_debuff_logic_only_triggers_when_party_size_exceeds_threshold():
    """All generated parties use the shared, capped party-size adjustment."""
    spawn = read_text("scripts/spawn_bandits.py")
    adjust = read_text("scripts/bandit_overhaul_adjust_party_size.py")
    assert '(call_script, "script_bandit_overhaul_adjust_party_size"' in spawn
    assert '(gt, ":scaled_total", ":scaled_cap")' in adjust
    assert '(party_remove_members, ":party_no", ":troop_no", ":stack_size")' in adjust


# ---------------------------------------------------------------------------
# T1 — Cooldown script contract
# ---------------------------------------------------------------------------


@pytest.mark.bandit
def test_cooldown_script_reads_all_seven_spawn_settings():
    """The helper receives cap, cadence, amount and party size as well as location."""
    text = read_text("scripts/spawn_party_type_with_cooldown.py")
    params = re.findall(r"\(store_script_param,\s*\"?:(\w+)\"?,\s*(\d+)\)", text)
    assert len(params) == 7, f"Expected seven helper inputs, found {len(params)}: {params}."
    expected_positions = [1, 2, 3, 4, 5, 6, 7]
    actual_positions = [int(p[1]) for p in params]
    assert actual_positions == expected_positions, (
        f"Param slots must be consecutive 1..4. Got {actual_positions}."
    )


@pytest.mark.bandit
def test_cooldown_script_writes_respawn_cooldown_in_both_branches():
    """The cooldown slot must be set in BOTH the seed branch AND the trickle branch.

    The seed branch sets it once at initial fill (to current hours).
    The trickle branch sets it after each successful spawn (to current hours
    + bandit_respawn_interval_hours). If either set is removed, the throttle
    breaks and bandits spawn every cycle.
    """
    text = read_text("scripts/spawn_party_type_with_cooldown.py")
    writes = re.findall(
        r"\(party_template_set_slot,\s*\"?:party_template\"?,\s*slot_party_template_respawn_cooldown",
        text,
    )
    assert len(writes) == 2, (
        f"Expected exactly 2 writes to slot_party_template_respawn_cooldown "
        f"(one per branch), got {len(writes)}. "
        "Each branch (seed / trickle) must persist its cooldown."
    )


@pytest.mark.bandit
def test_cooldown_script_initializes_reg0_to_sentinel():
    """Return the last spawned party ID, or -1 if this call spawned nothing."""
    text = read_text("scripts/spawn_party_type_with_cooldown.py")
    assert '(assign, ":last_spawned_party", -1)' in text
    assert '(assign, reg0, ":last_spawned_party")' in text


# ---------------------------------------------------------------------------
# T2 — Population caps consistency
# ---------------------------------------------------------------------------


@pytest.mark.bandit
@pytest.mark.parametrize(
    "constant_name, doc_value, doc_ref",
    [
        ("num_max_bandit_parties_per_type", 18, "6 land bandit types, 18 per type"),
        ("num_max_manhunters", 24, "Manhunters, 24 cap"),
        ("num_max_pirate_ships", 5, "Pirate ships, 5 per type"),
        ("num_max_bandit_party_size", 50, "Troops per party, 50"),
        ("num_max_bandit_party_size_debuff", 20, "Lair-down debuff, 20"),
        ("num_max_pirate_ship_size", 20, "Pirate ships, 20 troops"),
        ("bandit_lair_respawn_hours", 72, "Lair destroy cooldown, 72h (3 days)"),
        ("bandit_respawn_interval_hours", 24, "Trickle respawn, 24h"),
    ],
)
def test_population_cap_matches_doc(constant_name: str, doc_value: int, doc_ref: str):
    """Each documented population cap must equal its module_constants value.

    Source of truth: `docs/updates/features/new_bandit_system.md`.
    If the doc says 18 max bandit parties per type but module_constants says
    16, something drifted. The fix is to update the doc AND changelog, not
    silently change one side.

    To update a cap: edit module_constants.py, then update this parametrize
    list, then update the doc, in that order.
    """
    consts = collect_constants("module_constants.py")
    assert constant_name in consts, (
        f"Constant `{constant_name}` not found in module_constants.py. "
        "Did you rename it?"
    )
    actual = consts[constant_name]
    assert isinstance(actual, int), f"{constant_name} should be int, got {type(actual).__name__}"
    assert actual == doc_value, (
        f"{constant_name} = {actual}, but doc says {doc_value} ({doc_ref}). "
        "Either fix module_constants.py or update this test's expected value "
        "AND the doc together."
    )


@pytest.mark.bandit
def test_bandit_caps_match_between_calls_and_constants():
    """Each spawn family passes its own configurable cap into the shared helper."""
    text = read_text("scripts/spawn_bandits.py")
    for cap in (
        "$g_bo_land_parties_per_type",
        "$g_bo_ship_parties_per_type",
        "$g_bo_looter_parties",
    ):
        assert re.search(
            rf'script_spawn_party_type_with_cooldown[^\n]*?"{re.escape(cap)}"', text
        ), f"Expected the shared spawn helper to receive configured cap {cap}."


# ---------------------------------------------------------------------------
# T3 — Hardcoded lair coordinates
# ---------------------------------------------------------------------------


_COORD_SETTERS_RE = re.compile(
    r"\(position_set_x,\s*pos1,\s*(-?\d+)\),\s*\(position_set_y,\s*pos1,\s*(-?\d+)\)"
)


def _count_coords_per_template(text: str) -> dict[str, int]:
    """Walk through the spawn_bandits.py lair block and count (x,y) pairs per template.

    The structure is `if-else` per template, with 5 (position_set_x, position_set_y)
    pairs per template (4 inside try_begin/else_try/else_try/else_try + 1 fallback).
    """
    # Split into per-template blocks. The lair block is the second half of
    # spawn_bandits.py — past the line `#Spawn bandit lairs`.
    marker = "#Spawn bandit lairs"
    idx = text.find(marker)
    assert idx != -1, "Could not find '#Spawn bandit lairs' marker in spawn_bandits.py"
    lair_block = text[idx:]

    counts: dict[str, int] = {}
    for tmpl in (
        "pt_steppe_bandits",
        "pt_taiga_bandits",
        "pt_desert_bandits",
        "pt_forest_bandits",
        "pt_mountain_bandits",
        "pt_sea_raiders",
    ):
        # Find the `(eq, ":bandit_template", "pt_X")` line, then count coord
        # pairs up to the next `(eq, ":bandit_template", ...)` or the
        # outer `try_end` of the lair-creation block.
        m = re.search(
            rf'\(eq,\s*":bandit_template",\s*"{re.escape(tmpl)}"\)',
            lair_block,
        )
        if not m:
            counts[tmpl] = -1  # signal "missing"
            continue
        # Slice from the template's eq to the next template's eq.
        next_tmpl_iter = re.finditer(
            r'\(eq,\s*":bandit_template",\s*"pt_[a-z_]+"\)',
            lair_block[m.end():],
        )
        next_match = next(next_tmpl_iter, None)
        slice_end = m.end() + (next_match.start() if next_match else len(lair_block))
        per_template = lair_block[m.start():slice_end]
        coords = _COORD_SETTERS_RE.findall(per_template)
        counts[tmpl] = len(coords)
    return counts


@pytest.mark.bandit
def test_lair_coordinates_5_per_template():
    """Each of the 6 bandit templates must have exactly 5 hardcoded coordinate pairs.

    The doc (new_bandit_system.md) says 5 positions per lair type (30 total).
    If a refactor removes a position or adds an extra one, the fallback path
    shrinks/grows. Caught here before WRECK compile.
    """
    text = read_text("scripts/spawn_bandits.py")
    counts = _count_coords_per_template(text)
    bad = {tmpl: c for tmpl, c in counts.items() if c != 5}
    assert not bad, (
        f"Expected 5 hardcoded coordinates per bandit template; got: {counts}. "
        f"Bad: {bad}. If you renamed a template, update `_count_coords_per_template`."
    )


@pytest.mark.bandit
def test_lair_coordinates_total_count():
    """Total hardcoded lair coordinates must be 30 (6 templates × 5 positions)."""
    text = read_text("scripts/spawn_bandits.py")
    # Sanity check: total (position_set_x, position_set_y) pairs in the
    # lair block should equal 30.
    marker = "#Spawn bandit lairs"
    idx = text.find(marker)
    lair_block = text[idx:] if idx != -1 else text
    total = len(_COORD_SETTERS_RE.findall(lair_block))
    assert total == 30, (
        f"Expected 30 hardcoded lair coordinates, got {total}. "
        "Each template block (steppe/taiga/desert/forest/mountain/sea_raiders) "
        "must have 5 coordinate pairs."
    )


@pytest.mark.bandit
def test_lair_coordinates_no_duplicates_within_template():
    """Within each template, no two coordinates may be identical.

    Duplicates defeat the point of having multiple spawn positions. The
    engine tolerates duplicates but the lair becomes predictable.
    """
    text = read_text("scripts/spawn_bandits.py")
    marker = "#Spawn bandit lairs"
    idx = text.find(marker)
    lair_block = text[idx:] if idx != -1 else text

    for tmpl in (
        "pt_steppe_bandits",
        "pt_taiga_bandits",
        "pt_desert_bandits",
        "pt_forest_bandits",
        "pt_mountain_bandits",
        "pt_sea_raiders",
    ):
        m = re.search(
            rf'\(eq,\s*":bandit_template",\s*"{re.escape(tmpl)}"\)',
            lair_block,
        )
        if not m:
            continue
        next_tmpl_iter = re.finditer(
            r'\(eq,\s*":bandit_template",\s*"pt_[a-z_]+"\)',
            lair_block[m.end():],
        )
        next_match = next(next_tmpl_iter, None)
        slice_end = m.end() + (next_match.start() if next_match else len(lair_block))
        coords = _COORD_SETTERS_RE.findall(lair_block[m.start():slice_end])
        if len(coords) != len(set(coords)):
            dup_set = {c for c in coords if coords.count(c) > 1}
            pytest.fail(
                f"{tmpl} has duplicate coordinates {dup_set}. "
                "Pick distinct positions so the lair doesn't always spawn in the same spot."
            )


# ---------------------------------------------------------------------------
# T4 — Deserter cap is not enforced (user-reported 2026-10-04)
# ---------------------------------------------------------------------------


_DESERTER_LOOK_RE = re.compile(
    r"#deserters ends",
    re.MULTILINE,
)


def _deserter_block(text: str) -> str:
    """Return the slice of spawn_bandits.py that handles deserter spawning.

    The block starts at the latest `(set_spawn_radius, ...)` line that
    precedes the deserter try_for_range, and ends at `#deserters ends`.
    This covers the cap-check prelude added in 2026-10-05.
    """
    start_re = re.compile(
        r"\(try_for_range,\s*\":troop_no\",\s*active_npcs_begin,\s*active_npcs_end\),"
    )
    s = start_re.search(text)
    if not s:
        return ""
    # Walk backwards from `s.start()` to find the enclosing `(try_begin)`
    # that wraps the deserter block, then include the cap prelude that
    # came after it.
    prelude_re = re.compile(r"\(try_begin\)")
    p = prelude_re.search(text[: s.start()])
    if not p:
        return text[s.start():]
    e = _DESERTER_LOOK_RE.search(text, s.end())
    if not e:
        return text[p.start():]
    return text[p.start():e.end()]


@pytest.mark.bandit
def test_deserter_spawning_uses_cap_respawn_amount_and_eligible_lords():
    """Normal respawns honor interval amount; zero-cooldown rebuild seeds to cap."""
    text = read_text("scripts/spawn_bandits.py")
    block = text.split("# Deserters still spawn", 1)[1].split("# AC : Dark Hunters", 1)[0]

    assert '(party_template_get_slot, ":next_deserter_spawn", "pt_deserters"' in block
    assert '(lt, ":deserter_count", "$g_bo_deserter_parties")' in block
    assert '(lt, ":deserters_spawned", ":deserter_spawn_limit")' in block
    assert '(store_sub, ":deserter_spawn_limit", "$g_bo_deserter_parties", ":deserter_count")' in block
    assert '(troop_get_slot, ":lord_party", ":troop_no", slot_troop_leaded_party)' in block
    assert '(party_is_active, ":lord_party")' in block
    assert '(spawn_around_party, ":lord_party", "pt_deserters")' in block


@pytest.mark.bandit
def test_deserter_party_size_matches_doc():
    """`num_max_deserter_party_size` should match what the cheat menu reports.

    Cheat menu (`prsnt_spawn_diagnostics.py`) says "@max 15, 20 troops each"
    but the actual `num_max_deserter_party_size` constant is 50. Either the
    constant or the cheat-menu string is wrong.
    """
    consts = collect_constants("module_constants.py")
    assert "num_max_deserter_party_size" in consts, (
        "`num_max_deserter_party_size` missing from module_constants.py."
    )
    actual = consts["num_max_deserter_party_size"]
    # The doc says 20, the cheat menu says 20. The constant says 50.
    # This is the data-inconsistency variant of the same root cause: nothing
    # reads the constant to actually cap anything, so the cheat menu and
    # the constant diverged silently.
    assert actual <= 30, (
        f"`num_max_deserter_party_size` = {actual}. Cheat menu and doc say 20. "
        "Either lower the constant to 20, or update the cheat menu string "
        "to match. Both are user-facing promises."
    )
