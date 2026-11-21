# Code Maintenance

## 001 — Build Notice Cleanup

Removed dead code and unused parameters that were generating build warnings.

### source/module_game_menus.py
- Removed unnecessary `(assign, ":can_meet_guild_master", 1)` in guild master meeting menu
- Removed unused troop-slot read `(troop_get_slot, ":dna", "trp_temp_array_c", 17)`

### source/module_mission_templates.py
- Removed unused player-agent lookup in retreat mission `(get_player_agent_no, ":player_agent")` and `(agent_get_team, ":agent_team", ":player_agent")`

### source/module_presentations.py
- Replaced hardcoded `(overlay_set_color, reg1, 0xFF0000)` with reusable `:color` variable
- Removed unused local trigger setup from troop ratio bar presentation

### source/module_scripts.py
- Removed unused parameter reads from: `game_get_troop_wage`, `agent_troop_get_banner_mesh`, `debug_variables`, attrition script, `calculate_improvement_limit`, WSE message/window callbacks, `game_missile_dives_into_water`
- Removed unnecessary `slot_troop_controversy` read from `change_player_controversy` (value was immediately overwritten)

### source/sort_scripts.py
- Renamed unused loop variable `:unused` → `:sort_pass`
- Added guard `(ge, ":sort_pass", 0)` for explicit loop intent
