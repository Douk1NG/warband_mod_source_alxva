# Faction Color Editor

A presentation for changing faction colors, replacing the old `prsnt_change_color` and `change_color` scripts.

## Access
Camp action menu → Change the color of factions.

## source/game_menus/mnu_camp_action.py
- Uncommented "Change the color of factions." option
- Opens `prsnt_cc_color_editor` (replaces old `prsnt_change_color`)

## source/presentations/prsnt_cc_color_editor.py
- New presentation with color slider and preview for each faction
- Saves changes to faction slot `slot_faction_color`
- Old files `_unused/change_color.py` and `_unused/prsnt_change_color.py`
