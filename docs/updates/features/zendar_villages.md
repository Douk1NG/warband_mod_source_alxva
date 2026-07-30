# Zendar and Villages

Added the town of Zendar (`town_23`) and two villages — Hrafnvik (`village_111`), Vargdal (`village_112`).

## source/module_parties.py
- Added `town_23` (Zendar), `village_111` (Hrafnvik), `village_112` (Vargdal)

## source/module_scenes.py
- Added scene entries: `town_23_center`, `town_23_castle`, `town_23_tavern`, `town_23_store`, `town_23_arena`, `town_23_prison`, `town_23_walls`, `town_23_alley`, `village_111`, `village_112`

## source/module_troops.py
- Added NPCs: Zendar seneschal, arena master, armorer, weaponsmith, tavernkeeper, merchant, horse merchant, mayor, master craftsman
- Added village elders for Hrafnvik and Vargdal

## source/scripts/ (scene reuse)
- No new .sco files — existing in-game scenes assigned via script
- Zendar party slots populated from existing scenes
- Village scenes mapped: `p_village_111` → `scn_village_80`, `p_village_112` → `scn_village_62`

## Integration
- Zendar added to faction assignment flow
- Zendar-specific trade routes added
- New villages integrated into economy/production setup
- Tournament: Zendar arena scene added, tournament city settings added for `p_town_23`
