# Toggle Weapon Loadouts

A "Toggle weapons" option available in pre-battle menus (encounter, siege attacker, siege defender, joining battle) to switch between two weapon loadout sets for all heroes.

## source/module_game_menus.py
- Moved from camp menu to all pre-battle/encounter menus
- Only shows when party has more than 1 hero (`get_num_heroes_of_party` > 1)
- Reads current `$g_weapons_set_no`, cycles between set 1 and 2
- Calls `script_all_toggle_weapons_set` (strict_mode=0)

## source/scripts/feats/toggle_weapons_scripts.py
- Added `script_get_num_heroes_of_party` helper
