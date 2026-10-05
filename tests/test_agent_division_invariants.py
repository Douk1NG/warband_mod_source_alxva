"""Tests for `agent_fix_division` — troop-to-division assignment at battle start.

User-reported 2026-10-04: "My heroes dont have horse for moment, they are
in group cavalry but if i join a battle, heroes i see is on group 4,
group 3 is cavalry. I need manual every time to charge them because they
just follow me."

Root cause: cascade from the auto-loot horse-loss bug.

  1. `dplmc_auto_loot_troop.py` (lines 117-135) deletes the troop's ek_horse
     on every loot cycle when `:upg_horses != 0`. Even though it then
     looks for a replacement in the loot pool, it can fail to find a
     better one and the troop ends up with `ek_horse = -1`.

  2. `agent_fix_division.py` (this script) decides each agent's battle
     division by checking `(agent_get_horse, ":horse", ":agent")` and
     comparing `>= 0`. If `agent_fix_division` ran on companions at battle
     start, a horse-less companion would land in `grc_infantry` instead
     of `grc_cavalry`.

  3. In `agent_fix_division`, lines 28-29 (the entry guard) skip the
     whole script if the agent is on the player's team AND the player
     is alive. So companions of the player NEVER get re-divisioned by
     this code path. They keep whatever division the engine put them in
     at spawn time.

The combined effect: a cavalry companion who lost his horse to the
auto-loot bug stays in `grc_cavalry` slot-wise (engine decides based on
troop class) but has no horse at spawn — so when battle begins, the
formation UI shows them in the cavalry group, but the agents themselves
are positioned with the infantry and behave as infantry.

These tests pin the relevant shape so we can verify the cascade root.
"""
from __future__ import annotations

import re

import pytest

from tests._helpers import read_text


AGENT_FIX_DIVISION = "scripts/agent_fix_division.py"


@pytest.mark.bandit
def test_agent_fix_division_default_division_is_infantry():
    """The default `:target_division` must be `grc_infantry`.

    If the default is something else (e.g. grc_cavalry), then a horse-less
    agent whose troop class doesn't guarantee a horse would still be put
    into cavalry, causing the "agent is on group 4 (infantry) but formation
    UI shows group 3 (cavalry)" symptom the user reported.

    We use a flexible check: find any `(assign, ":target_division", grc_infantry)`
    line, and verify the next `agent_get_horse` is reachable without an
    intervening `(assign, ":target_division", grc_cavalry)`.
    """
    text = read_text(AGENT_FIX_DIVISION)
    infantry_assign = re.search(
        r"\(assign,\s*\":target_division\",\s*grc_infantry\)",
        text,
    )
    assert infantry_assign, (
        f"`{AGENT_FIX_DIVISION}` does not initialize `:target_division` to "
        "grc_infantry. The default matters: horse-less troops MUST go to "
        "infantry first, then promote to cavalry if they have a horse."
    )
    cavalry_assign = re.search(
        r"\(assign,\s*\":target_division\",\s*grc_cavalry\)",
        text,
    )
    assert cavalry_assign, (
        f"`{AGENT_FIX_DIVISION}` does not promote to grc_cavalry at all."
    )
    # The infantry default must come BEFORE the cavalry promotion. If
    # they're swapped (cavalry first), the default is wrong.
    assert infantry_assign.start() < cavalry_assign.start(), (
        "The `:target_division = grc_infantry` default comes AFTER the "
        "cavalry promotion. Default must be infantry."
    )
    # The default must appear before the (agent_get_horse, ":horse", ":agent")
    # call (so the script checks the horse BEFORE deciding whether to override).
    horse_get = re.search(
        r"\(agent_get_horse,\s*\":horse\",\s*\":agent\"\)",
        text,
    )
    assert horse_get, "agent_fix_division doesn't call agent_get_horse."
    assert infantry_assign.start() < horse_get.start(), (
        "`:target_division = grc_infantry` must come before `agent_get_horse`."
    )


@pytest.mark.bandit
def test_agent_fix_division_cavalry_when_has_horse_or_guaranteed():
    """A troop with a horse OR a `troop_is_guarantee_horse` flag must be
    classified as `grc_cavalry`.

    This covers both:
      - the agent has a horse right now (`:horse >= 0`), AND
      - the troop is a mounted unit by class (cavalry) even if the agent
        happens to be missing a horse for some reason.
    """
    text = read_text(AGENT_FIX_DIVISION)
    assert re.search(
        r"\(this_or_next\s*\|\s*ge,\s*\":horse\",\s*0\),\s*"
        r"\(troop_is_guarantee_horse,\s*\":troop_no\"\),\s*"
        r"\(assign,\s*\":target_division\",\s*grc_cavalry\)",
        text,
    ), (
        f"`{AGENT_FIX_DIVISION}` does not promote to grc_cavalry when "
        "either the agent has a horse OR the troop is a guaranteed "
        "mounted unit. Without this, mounted troops end up in infantry "
        "when their horse slot is empty (e.g. due to the auto-loot "
        "horse-loss bug)."
    )


@pytest.mark.bandit
def test_agent_fix_division_skips_player_team_companions():
    """Pin the documented limitation: this script skips player-team agents.

    Lines 28-29 in the current code:
        (this_or_next | main_hero_fallen),
        (neq, ":team", ":player_team"),
    If the agent is on the player's team and the player is alive, the
    whole re-division block is skipped. Player companions therefore keep
    whatever division the engine spawn gave them — which is based on
    troop class, not current horse status.

    This test pins that limitation as a known fact so any change to
    `agent_fix_division` that "fixes" it is intentional (and the test
    must be updated alongside).
    """
    text = read_text(AGENT_FIX_DIVISION)
    assert re.search(
        r"\(this_or_next\s*\|\s*main_hero_fallen\),\s*"
        r"\(neq,\s*\":team\",\s*\":player_team\"\)",
        text,
    ), (
        f"`{AGENT_FIX_DIVISION}` no longer has the "
        "`(this_or_next | main_hero_fallen), (neq, \":team\", \":player_team\")` "
        "guard. If you removed it intentionally to fix the cascade "
        "user-reported bug, also remove the test below."
    )


@pytest.mark.bandit
def test_companion_horse_loss_cascade_is_documented():
    """The companion-horse cascade is documented somewhere.

    The user's report combines three bugs (auto-loot drops ek_horse,
    no re-division for player team, formation UI shows cavalry while
    agent is infantry). Until all three are fixed, the cascade remains
    — and a future agent/developer needs to know about it.

    This test asserts that the cascade is recorded in `AGENTS.md` or a
    sibling file. If the auto-loot bug is fixed, this test can be
    relaxed.
    """
    cascade_re = re.compile(
        r"companion.{0,40}horse.{0,40}cascad|horse.{0,40}division.{0,40}cascade",
        re.IGNORECASE | re.DOTALL,
    )
    cascade_re_b = re.compile(
        r"horse.{0,40}loss.{0,40}division|cavalry.{0,40}group.{0,40}infantry|"
        r"group 4.{0,40}group 3",
        re.IGNORECASE | re.DOTALL,
    )
    try:
        ag_text = read_text("AGENTS.md")
    except FileNotFoundError:
        ag_text = ""
    has_doc = bool(
        cascade_re.search(ag_text) or cascade_re_b.search(ag_text)
    )
    assert has_doc, (
        "The companion-horse cascade (auto-loot drops ek_horse -> "
        "agent_fix_division skips player team -> formation shows cavalry, "
        "agent behaves as infantry) is NOT documented in AGENTS.md. "
        "Until all three root causes are fixed, future agents need this "
        "context. Add a section like:\n\n"
        "## Horse-loss cascade (2026-10-04)\n"
        "`dplmc_auto_loot_troop` deletes ek_horse when no better horse "
        "is in the pool. `agent_fix_division` skips player-team agents, "
        "so horse-less companions retain their engine-assigned division "
        "(based on troop class), creating the 'formation shows cavalry, "
        "agent is infantry' symptom. Fix root = fix auto-loot; do NOT "
        "patch agent_fix_division in isolation."
    )