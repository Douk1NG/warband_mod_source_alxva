# Cheat: Remove All Ships

Adds a cheat option to remove all ship parties from the map.

## source/game_menus/mnu_camp_cheat.py
- Added "CHEAT: Remove all ships." option
- Iterates all parties and disables any matching `spt_ship` party type
- Displays "All ships removed." message
