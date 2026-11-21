# Faction/Lords Relations Report

A CC-sourced presentation that displays relations with all factions and their lords.

## source/game_menus/mnu_reports_faction.py
- Added option "View faction/lords relations report." opening `prsnt_cc_relations_with_factions`

## source/presentations/prsnt_cc_relations_with_factions.py
- Lists all factions with player relations
- Selecting a faction opens `prsnt_cc_relations_with_lords_by_faction`

## source/presentations/prsnt_cc_relations_with_lords_by_faction.py
- Lists all lords of the selected faction with their individual relations to the player
