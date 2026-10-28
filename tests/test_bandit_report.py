"""Source contracts for the live Bandit & Spawn Report."""
from tests._helpers import read_text


def test_report_counts_live_parties_and_uses_current_configured_caps():
    report = read_text("presentations/prsnt_spawn_diagnostics.py")

    # Counts come from active campaign parties; caps come from saved settings.
    assert report.count('"$g_bo_land_parties_per_type", 1)') == 6
    assert '"pt_looters", "$g_bo_looter_parties", 0' in report
    assert '(store_num_parties_of_template, ":ns1", "pt_sea_raiders_ship")' in report
    assert '(store_mul, ":ship_cap", "$g_bo_ship_parties_per_type", 3)' in report
    assert '(assign, ":mh_cap", "$g_bo_manhunter_parties")' in report
    assert '"@Cap: {reg1} parties, size {reg2}"' in report
    assert '(assign, reg1, "$g_bo_deserter_parties")' in report
    assert '(assign, reg2, "$g_bo_deserter_party_size")' in report
    assert '(store_mul, ":bandit_cap", "$g_bo_land_parties_per_type", 6)' in report


def test_report_shows_remaining_ship_cooldowns_and_validates_lair_party():
    report = read_text("presentations/prsnt_spawn_diagnostics.py")
    helper = read_text("scripts/get_spawn_report_line.py")

    assert '"@CD h: R {reg1} C {reg2} P {reg3}"' in report
    assert '"@CD slot (raw)"' not in report
    assert '(store_num_parties_of_template, ":num", ":party_template")' in helper
    assert '(party_is_active, ":lair_party")' in helper
    assert '(eq, ":lair_type", spt_bandit_lair)' in helper
