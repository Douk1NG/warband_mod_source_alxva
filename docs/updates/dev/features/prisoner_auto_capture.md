# Automatic Captured Prisoner Selection

Prisoners are automatically selected before the prisoner exchange screen opens, prioritizing quest targets then highest-level prisoners.

## source/module_game_menus.py
- Runs in the `total_victory` flow before `change_screen_exchange_with_party`
- Moves newly captured prisoners into `p_temp_party`
- Clears existing prisoners from `p_main_party`
- Checks player's free prisoner capacity (renown-based bonus added)
- Priority 1: quest-relevant prisoners (`qst_follow_spy`: `trp_spy` / `trp_spy_partner`; `qst_capture_prisoners`: quest target troop up to requested amount)
- Priority 2: highest-level available prisoners to fill remaining capacity
- Normal exchange screen still opens afterward for manual adjustments
