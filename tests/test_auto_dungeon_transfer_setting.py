from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_auto_dungeon_transfer_setting_controls_town_prisoner_move():
    settings = (ROOT / "source/scripts/settings_content_ui.py").read_text(encoding="cp1254")
    town_menu = (ROOT / "source/game_menus/mnu_town.py").read_text(encoding="cp1254")
    camp_hub = (ROOT / "source/presentations/prsnt_camp_hub.py").read_text(encoding="cp1254")

    assert '"@Auto Dungeon Transfer:"' in settings
    assert '"$g_settings_btn_25"' in settings
    assert '"$g_auto_dungeon_transfer", 2' in settings
    assert '"$g_auto_dungeon_transfer", 2' in town_menu
    assert '(call_script, "script_party_prisoners_add_party_prisoners", "$current_town", "p_main_party")' in town_menu
    assert '"$g_settings_btn_25", -1' in camp_hub
