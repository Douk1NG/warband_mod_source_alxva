"""Invariants for companion battle-division assignment."""
from __future__ import annotations

import re

import pytest

from tests._helpers import read_text


AGENT_FIX_DIVISION = "scripts/agent_fix_division.py"


@pytest.mark.bandit
def test_agent_fix_division_processes_player_team_companions():
    """The player-team guard must not prevent companion reassignment."""
    text = read_text(AGENT_FIX_DIVISION)
    assert '(neq, ":agent", ":player")' in text
    assert "main_hero_fallen" not in text
    assert 'agent_get_group, ":player_team"' not in text
    assert 'agent_get_group, ":team"' not in text


@pytest.mark.bandit
def test_agent_fix_division_preserves_custom_divisions():
    """Divisions above cavalry are treated as custom and left unchanged."""
    text = read_text(AGENT_FIX_DIVISION)
    custom_guard = re.search(
        r'\(agent_get_division,\s*":division",\s*":agent"\),\s*'
        r'\(gt,\s*":division",\s*grc_cavalry\),\s*'
        r'\(else_try\),',
        text,
    )
    assert custom_guard, "Custom divisions must bypass the reassignment branch."
    assert '(agent_set_division, ":agent", ":target_division")' in text


@pytest.mark.bandit
def test_agent_fix_division_prioritizes_bow_and_crossbow_over_horse():
    """Equipped bows/crossbows take archer precedence over being mounted."""
    text = read_text(AGENT_FIX_DIVISION)
    assert '(assign, ":target_division", grc_infantry)' in text
    assert '(this_or_next | eq, ":item_type", itp_type_bow)' in text
    assert '(eq, ":item_type", itp_type_crossbow)' in text
    archer_branch = text.index('(assign, ":target_division", grc_archers)')
    horse_check = text.index('(agent_get_horse, ":horse", ":agent")')
    cavalry_branch = text.index('(assign, ":target_division", grc_cavalry)')
    assert archer_branch < horse_check < cavalry_branch
    assert "script_cf_is_weapon_ranged" not in text


@pytest.mark.bandit
def test_agent_fix_division_uses_current_horse_then_infantry_fallback():
    """A horse-less non-archer is infantry; a mounted one is cavalry."""
    text = read_text(AGENT_FIX_DIVISION)
    assert '(agent_get_horse, ":horse", ":agent")' in text
    assert '(ge, ":horse", 0)' in text
    assert "troop_is_guarantee_horse" not in text
    assert '(assign, ":target_division", grc_infantry)' in text
    assert '(assign, ":target_division", grc_cavalry)' in text

