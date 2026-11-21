# Automatic Prisoner Dungeon Deposit

Entering a player-owned castle or town automatically moves prisoners from the player party into that center's dungeon.

## source/module_game_menus.py
- `mnu_town` entry hook for player-owned walled centers (`slot_town_lord` is `trp_player`)
- All prisoners in `p_main_party` moved into `$current_town`
- Uses `$g_move_heroes = 1` (lord and hero prisoners move with regular prisoners)
- Player receives a message reporting how many were moved
- Only triggers for centers directly owned by the player (not vassal-owned)
