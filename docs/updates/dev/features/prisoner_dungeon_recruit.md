# Constable Dungeon Prisoner Recruit to Garrison

Constable can recruit eligible dungeon prisoners directly into the current garrison.

## source/module_dialogs.py, scripts/diplomacy/diplomacy_scripts.py
- Uses `script_dplmc_recruit_all_prisoners_to_garrison`
- Scans a center's prisoner stacks and converts eligible regular prisoners into normal garrison members of the same troop type
- Eligibility follows `script_game_check_prisoner_can_be_sold` (lord prisoners remain in dungeon)
- Supports dry-run mode for dialog confirmation and execute mode for actual conversion
- After success, a log message reports how many were added
