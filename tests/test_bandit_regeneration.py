"""Source-contract tests for Bandit Overhaul reset and hourly spawning.

These tests guard the requested rules and cost-sensitive call flow. They do
not emulate Warband's map-party engine; final spawn placement still needs an
in-game check.
"""
from tests._helpers import read_text


def test_button_calls_regeneration_and_reports_user_facing_result():
    presentation = read_text("presentations/prsnt_bandit_overhaul_settings.py")
    handler = presentation.split('(eq, ":object", "$g_boh_regenerate")', 1)[1]
    assert '(call_script, "script_bandit_overhaul_regenerate_parties")' in handler
    assert '@Bandit regeneration completed.' in handler
    assert '@Bandit regeneration did not complete.' in handler


def test_ships_are_refilled_directly_before_the_general_spawn_pass():
    spawn_script = read_text("scripts/spawn_bandits.py")
    regenerate = spawn_script.split('("bandit_overhaul_regenerate_parties",', 1)[1]
    first_ship_fill = regenerate.index('(call_script, "script_spawn_party_type_with_cooldown", "pt_sea_raiders_ship"')
    second_ship_fill = regenerate.index('(call_script, "script_spawn_party_type_with_cooldown", "pt_corsair_ship"')
    third_ship_fill = regenerate.index('(call_script, "script_spawn_party_type_with_cooldown", "pt_pirate_ship"')
    general_spawn = regenerate.index('(call_script, "script_spawn_bandits")')
    assert first_ship_fill < second_ship_fill < third_ship_fill < general_spawn
    assert '(party_template_set_slot, "pt_sea_raiders_ship", slot_party_template_respawn_cooldown, 0)' in regenerate
    assert '(party_template_set_slot, "pt_corsair_ship", slot_party_template_respawn_cooldown, 0)' in regenerate
    assert '(party_template_set_slot, "pt_pirate_ship", slot_party_template_respawn_cooldown, 0)' in regenerate


def test_button_reports_completion_or_interruption_after_synchronous_call():
    presentation = read_text("presentations/prsnt_bandit_overhaul_settings.py")
    handler = presentation.split('(eq, ":object", "$g_boh_regenerate")', 1)[1].split(
        '(else_try),\n          (eq, ":object", "$g_boh_growth")', 1
    )[0]
    call = handler.index('(call_script, "script_bandit_overhaul_regenerate_parties")')
    success = handler.index('(display_message, "@Bandit regeneration completed.')
    failure = handler.index('(display_message, "@Bandit regeneration did not complete.')
    assert '(assign, "$g_bo_regenerate_completed", 0)' in handler[:call]
    assert call < success < failure

    spawn_script = read_text("scripts/spawn_bandits.py")
    regenerate = spawn_script.split('("bandit_overhaul_regenerate_parties",', 1)[1]
    completed = regenerate.index('(assign, "$g_bo_regenerate_completed", 1)')
    counts_done = regenerate.index('(try_for_parties, ":party_no")', regenerate.index("# Count resulting populations"))
    assert completed > counts_done
    assert completed < regenerate.index('@Bandits {reg0} -> {reg1}/{reg2}.')


def test_regeneration_uses_one_normal_spawn_pass_after_lairs_are_ready():
    spawn_script = read_text("scripts/spawn_bandits.py")
    main_spawn = spawn_script.split('("spawn_bandits",', 1)[1].split(
        '("bandit_overhaul_regenerate_parties",', 1
    )[0]
    regenerate = spawn_script.split('("bandit_overhaul_regenerate_parties",', 1)[1]

    assert main_spawn.index("#Spawn bandit lairs") < main_spawn.index("# Mountain Bandits")
    assert regenerate.count('(call_script, "script_spawn_bandits")') == 1
    assert 'assign, "$g_bo_regenerate_mode", 1' in regenerate
    assert 'assign, "$g_bo_regenerate_mode", 0' in regenerate
    assert "temporary parties" not in regenerate


def test_regeneration_preserves_manhunters_and_reconciles_to_cap():
    spawn_script = read_text("scripts/spawn_bandits.py")
    regenerate = spawn_script.split('("bandit_overhaul_regenerate_parties",', 1)[1]
    deletion = regenerate.split("# Rebuild land bandits", 1)[1].split(
        "# Keep manhunters up to cap", 1
    )[0]

    assert '(eq, ":party_template", "pt_manhunters")' not in deletion
    assert '(store_num_parties_of_template, ":manhunter_count", "pt_manhunters")' in regenerate
    assert '(store_sub, ":manhunters_to_remove", ":manhunter_count", "$g_bo_manhunter_parties")' in regenerate
    assert '"pt_manhunters"' in regenerate[regenerate.index("# Keep manhunters up to cap") :]


def test_manual_deserter_seed_fills_configured_cap_subject_to_lord_availability():
    spawn_script = read_text("scripts/spawn_bandits.py")
    assert '(eq, ":next_deserter_spawn", 0)' in spawn_script
    assert '(store_sub, ":deserter_spawn_limit", "$g_bo_deserter_parties", ":deserter_count")' in spawn_script
    assert '(lt, ":deserters_spawned", ":deserter_spawn_limit")' in spawn_script


def test_hourly_spawn_checks_do_not_scan_party_counts_before_cooldown_is_due():
    trigger = read_text("simple_triggers/spawn_bandits.py")
    helper = read_text("scripts/spawn_party_type_with_cooldown.py")
    assert "(1," in trigger

    first_count = helper.index('(store_num_parties_of_template, ":num_parties", ":party_template")')
    first_due_check = helper.index('(eq, ":next_spawn", 0)')
    assert first_due_check < first_count
    assert '(ge, ":current_hours", ":next_spawn")' in helper
    assert 'Only scan parties when this template is due' in helper
    assert helper.count('(store_num_parties_of_template, ":num_parties", ":party_template")') == 2


def test_each_spawned_ship_and_looter_gets_its_own_metadata():
    helper = read_text("scripts/spawn_party_type_with_cooldown.py")
    spawn_bandits = read_text("scripts/spawn_bandits.py")

    # Metadata must be applied in the shared helper after every spawn, including
    # both the initial fill and later respawns (not just to reg0 after a batch).
    spawn_paths = helper.split('(assign, ":spawned_party", reg0)')[1:]
    assert len(spawn_paths) == 2
    for path in spawn_paths:
        per_spawn = path.split('(call_script, "script_bandit_overhaul_adjust_party_size"', 1)[0]
        assert '(party_set_slot, ":spawned_party", slot_party_ship_type, 1)' in per_spawn
        assert '(party_set_slot, ":spawned_party", slot_party_ship_type, 2)' in per_spawn
        assert '(party_set_slot, ":spawned_party", slot_party_ship_type, 4)' in per_spawn
        assert '(party_set_flags, ":spawned_party", pf_quest_party, 1)' in per_spawn
        assert '(party_set_flags, ":spawned_party", pf_quest_party, 0)' in per_spawn

    # The caller no longer tries to annotate only the last reg0 from a batch.
    assert '(party_set_slot, reg0, slot_party_ship_type,' not in spawn_bandits
    looter_call = spawn_bandits.split('# Looters', 1)[1].split('# Manhunters', 1)[0]
    assert 'pf_quest_party' not in looter_call


def test_regeneration_reports_actual_before_and_after_counts_by_family():
    spawn_script = read_text("scripts/spawn_bandits.py")
    regenerate = spawn_script.split('("bandit_overhaul_regenerate_parties",', 1)[1]
    expected = (
        "@Bandits {reg0} -> {reg1}/{reg2}.",
        "@Pirate ships {reg0} -> {reg1}/{reg2}.",
        "@Looters {reg0} -> {reg1}/{reg2}.",
        "@Deserters {reg0} -> {reg1}/{reg2}; eligible lords limit this.",
        "@Manhunters {reg0} -> {reg1}/{reg2}.",
    )
    for message in expected:
        assert message in regenerate


def test_regeneration_has_no_temporary_debug_traces():
    presentation = read_text("presentations/prsnt_bandit_overhaul_settings.py")
    spawn_script = read_text("scripts/spawn_bandits.py")
    helper = read_text("scripts/spawn_party_type_with_cooldown.py")

    assert "[BO-REGEN]" not in presentation
    assert "[BO-REGEN]" not in spawn_script
    assert "[BO-REGEN]" not in helper


def test_settings_initializer_does_not_abort_callers_when_already_initialized():
    initializer = read_text("scripts/initialize_bandit_overhaul_settings.py")
    guarded_init = initializer.split("# Keep the already-initialized path", 1)[1]
    guard_start = guarded_init.index("(try_begin)")
    guard_condition = guarded_init.index('(neq, "$g_bandit_overhaul_settings_initialized", 1)')
    initialized_flag = guarded_init.index('(assign, "$g_bandit_overhaul_settings_initialized", 1)')
    guard_end = guarded_init.index("(try_end)", initialized_flag)
    assert guard_start < guard_condition < initialized_flag < guard_end


def test_default_deserter_cap_and_respawn_batch_match_requested_values():
    constants = read_text("module_constants.py")
    assert "bandit_overhaul_default_deserter_parties = 50" in constants
    assert "bandit_overhaul_default_deserter_respawn_amount = 60" in constants

    presentation = read_text("presentations/prsnt_bandit_overhaul_settings.py")
    assert "(create_number_box_overlay, \"$g_boh_option_14\", 0, 101)" in presentation
    assert "(create_number_box_overlay, \"$g_boh_option_17\", 1, 101)" in presentation
