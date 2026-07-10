# Update 002 — Added Zendar and two villages: Hrafnvik and Vargdal

## Purpose
This update documents the new Zendar location and village additions.
The work consists of adding `town_23` (Zendar), `village_111` (Hrafnvik) and `village_112` (Vargdal), creating the matching scenes and troops, and wiring the new locations into the existing diplomacy and economy systems.

## Files and detailed changes

### 1) source/module_parties.py
- Added the new Zendar center party:
  - `town_23` named Zendar.
- Added the two new Zendar villages:
  - `village_111` named Hrafnvik.
  - `village_112` named Vargdal.
- Important: the base Zendar party is not modified beyond adding the new location entries.
  - This was intentional to avoid the conflicts that occurred when changing the original Zendar definition.

### 2) source/module_scenes.py
- Added scene definitions matching the new parties:
  - `town_23_center`
  - `town_23_castle`
  - `town_23_tavern`
  - `town_23_store`
  - `town_23_arena`
  - `town_23_prison`
  - `town_23_walls`
  - `town_23_alley`
  - `village_111`
  - `village_112`
- Nothing fancy here: these are the scene entries needed by the new parties.

### 3) source/module_scripts.py
- Added the Zendar scene reuse trick:
  - The script assigns `p_town_23` scene slots from existing scenes instead of creating new Zendar files.
  - This avoids new .sco file creation.
- Added village scene mapping for the two new villages:
  - `p_village_111` to `scn_village_80`
  - `p_village_112` to `scn_village_62`
- Integrated Zendar into the diplomacy/economy system:
  - Added the new center to the faction assignment flow.
  - Added Zendar-specific trade routes.
  - Added the new villages into the economy/production setup.

### 4) source/module_troops.py
- Added all necessary troops for the new Zendar locations:
  - `town_23` seneschal, arena master, armorer, weaponsmith, tavernkeeper, merchant, horse merchant, mayor, master craftsman.
  - `village_111` elder.
  - `village_112` elder.

### 5) source/tournament_scenes.py
- Added the alternate arena scene entry for `town_23`.

### 6) source/tournament_scripts.py
- Added a Zendar-specific tournament city settings branch for `p_town_23`.

## Notes
- This update is about adding Zendar (location) + 2 villages, making sure the new parties have scenes and troops, and avoiding new Zendar scene file creation by reusing existing scenes.
- Lore was not considered in this update; the focus was on the technical integration of the new locations into the module's system.
