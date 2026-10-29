"""Regression checks for runtime Native/WSE2 auto-upgrade behavior."""
from __future__ import annotations

from tests._helpers import read_text


AUTO_UPGRADE_TROOPS = "scripts/auto_upgrade_troops.py"
SETTINGS_UI = "scripts/settings_content_ui.py"
AUTO_UPGRADE_TOOLTIP = "module_strings.py"
AUTO_UPGRADE_TRIGGER = "simple_triggers/auto_upgrade_troops.py"


def test_one_script_runtime_selects_native_or_wse2_backend():
    script = read_text(AUTO_UPGRADE_TROOPS)
    assert '("auto_upgrade_troops", [' in script
    assert "(is_vanilla_warband)" in script
    assert script.index("(is_vanilla_warband)") < script.index("(party_stack_get_num_upgradeable")
    native = script[script.index("(is_vanilla_warband)"):script.index("(else_try),", script.index("(is_vanilla_warband)"))]
    assert '(store_sub, ":native_upgrade_path", "$g_auto_upgrade_mode", 1)' in native
    assert '(party_upgrade_with_xp, "p_main_party", 1, ":native_upgrade_path")' in native
    assert '"@Auto-upgrade checked the party (random path)."' in native
    assert '(neq, "$g_auto_upgrade_mode", 0)' in native


def test_wse2_branch_preserves_per_stack_class_selection_and_cost():
    script = read_text(AUTO_UPGRADE_TROOPS)
    wse2 = script[script.index("(party_stack_get_num_upgradeable"):]
    assert '(eq, "$g_auto_upgrade_mode", 1)' in wse2
    assert '(eq, "$g_auto_upgrade_mode", 2)' in wse2
    assert '(eq, "$g_auto_upgrade_mode", 3)' in wse2
    assert '(assign, ":target_class", grc_archers)' in wse2
    assert '(call_script, "script_cf_troop_is_class", ":target_class", ":upg0")' in wse2
    assert '(call_script, "script_cf_troop_is_class", ":target_class", ":upg1")' in wse2
    assert '(store_mul, ":cost", ":to_upgrade", ":cpt")' in wse2
    assert '(troop_remove_gold, "trp_player", ":gold_spent")' in wse2
    assert '"@Auto-upgrade complete: {reg6} troops upgraded for {reg7} denars."' in wse2
    assert '(eq, ":matched", 0)' in wse2


def test_settings_detect_runtime_engine_for_available_upgrade_modes():
    ui = read_text(SETTINGS_UI)
    assert "auto_upgrade_selector_ops = [" in ui
    assert "(is_vanilla_warband)" in ui
    assert '(overlay_add_item, "$g_settings_btn_16", "@Random path")' in ui
    assert '(overlay_add_item, "$g_settings_btn_16", "@Prioritize first path")' in ui
    assert '(overlay_add_item, "$g_settings_btn_16", "@Prioritize second path")' in ui
    assert '(overlay_add_item, "$g_settings_btn_16", "@Balanced")' in ui
    assert '(overlay_add_item, "$g_settings_btn_16", "@Archers")' in ui
    assert '(overlay_add_item, "$g_settings_btn_16", "@Cavalry")' in ui
    strings = read_text(AUTO_UPGRADE_TOOLTIP)
    assert '("tip_settings_auto_upgrade", "Automatically upgrades party troops.")' in strings


def test_auto_upgrade_runs_at_day_end_and_after_campaign_events():
    trigger = read_text(AUTO_UPGRADE_TRIGGER)
    assert "(1," in trigger
    assert '(eq, ":cur_hour", 0)' in trigger
    assert '(call_script, "script_auto_upgrade_troops")' in trigger
    for path in (
        "game_menus/mnu_total_victory.py",
        "game_menus/mnu_besiegers_camp_with_allies.py",
        "game_menus/mnu_training_ground_training_result.py",
    ):
        assert '(call_script, "script_auto_upgrade_troops")' in read_text(path)


def test_build_has_no_second_backend_or_module_folder():
    compile_bat = read_text("../compile.bat")
    module_info = read_text("module_info.py")
    assert "compile_wse2" not in compile_bat
    assert "Dickplomacy Reloaded WSE2" not in module_info
    assert "DPLMC_AUTO_UPGRADE_BACKEND" not in read_text(AUTO_UPGRADE_TROOPS)
