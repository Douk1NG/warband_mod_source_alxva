# Constable Dungeon Prisoner Sell-All

Constable can sell all eligible prisoners from the current dungeon directly, without the temporary garrison-prisoner trade screen.

## source/module_dialogs.py, scripts/diplomacy/diplomacy_scripts.py
- Always-visible direct sell-all option in constable menu
- If dungeon has no sellable prisoners, constable reports none
- Sells only regular (non-hero) prisoners accepted by `script_game_check_prisoner_can_be_sell`
- Avoids moving dungeon prisoners through `p_main_party`
- Avoids opening the prisoner trade screen
- Uses `script_dplmc_sell_all_prisoners_from_party` (party-specific) for current dungeon prisoners
