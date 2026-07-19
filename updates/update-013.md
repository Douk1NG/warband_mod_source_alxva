# Update 013 - Module Game Menus Topic Split (modularization pass)

## Summary

`source/module_game_menus.py` — originally **23,514 lines / 253 game menus** in a
single monolithic file — has been split into a `game_menus/` package of **23 topic
files**, following the same domain-split pattern already used by `scripts/` and
`presentations/`. The original file is now a thin (~79 line) re-assembly stub that
does `from game_menus import *` and then runs the post-list scene-template generation
and the modmerger hooks.

This is a **structural-only** change. No menu content, ordering, IDs, or gameplay
logic was altered. The compiler output is byte-for-byte equivalent (verified by a
successful W.R.E.C.K. compile producing the same `game_menus.txt` / `ID_menus.py`).

Two passes were made in this update:

1. **Category split** — top-level grouping by broad area (character_creation,
   reports, camp, town_castle, battle, kingdom, captivity, training, dplmc,
   locations, misc).
2. **Topic split** — the three oversized category files (`town_castle` 66 menus /
   8,676 lines, `battle` 25 menus / 3,719 lines, `kingdom` 40 menus / 2,774 lines)
   were further subdivided by in-game topic so no single file exceeds ~2,600 lines.

## Structure

```
source/
  module_game_menus.py      <- re-assembly stub (imports + post-list code + modmerger)
  module_game_menus.py.bak  <- original monolithic backup (DO NOT commit; dev reference only)
  game_menus/
    __init__.py             <- imports all topic files, game_menus.extend(...)s in order
    character_creation.py   (17 menus, 2153 lines)
    reports.py              (16 menus, 1541)
    camp.py                 (11 menus, 1169)
    castle.py               (8 menus, 1743)
    village.py              (15 menus, 1589)
    town.py                 (8 menus, 2599)
    tournament.py           (8 menus, 480)
    center_management.py    (2 menus, 250)
    taxes_training.py       (11 menus, 467)
    sneak.py                (4 menus, 166)
    misc_town.py            (13 menus, 2068)
    encounter.py            (3 menus, 453)
    battle_results.py       (5 menus, 880)
    join_battle.py          (4 menus, 450)
    siege.py                (6 menus, 723)
    faction_battle.py       (4 menus, 582)
    kingdom_management.py   (10 menus, 1000)
    notifications.py        (30 menus, 1774)
    captivity.py            (14 menus, 577)
    training.py             (8 menus, 418)
    dplmc.py                (33 menus, 1214)
    locations.py            (6 menus, 152)
    misc.py                 (17 menus, 988)
```

**Total: 253 menus across 23 topic files** (plus `__init__.py` + the stub).

### Topic → file mapping rationale

| File | Menus covered (topic) |
| ---- | --------------------- |
| `character_creation.py` | `start_game_*`, `start_phase_*`, `start_character_*`, `choose_skill`, `tutorial`, `past_life_explanation`, `auto_return`, `custom_battle_*` |
| `reports.py` | `reports`, `reports_*`, `cheat_reports`, `morale_report`, `courtship_relations`, `lord_relations`, `companion_report`, `character_report`, `party_size_report`, `faction_relations_report`, `center_reports`, `price_and_production`, `dplmc_economic_report`, `dplmc_affiliated_family_report` |
| `camp.py` | `camp`, `camp_cheat*`, `camp_action*`, `camp_recruit_prisoners`, `camp_no_prisoners`, `camp_action_read_book*`, `cheat_find_item`, `cheat_change_weather`, `retirement_verify`, `end_game`, `dplmc_camp_preferences` |
| `castle.py` | `castle_outside`, `castle_entry_granted/denied`, `castle_meeting/selected` |
| `village.py` | `village`, `village_hostile_action`, `recruit_volunteers`, `village_hunt_down_fugitive*`, `village_infest*`, `village_steal_cattle`, `village_take_food`, `village_loot*`, `village_enslave_complete`, `close` |
| `town.py` | `town`, `town_trade*`, `dplmc_trade_auto_*`, `town_trade_assessment*`, `town_hire_cutthroats/knights` |
| `tournament.py` | `town_tournament*`, `tournament_*` |
| `center_management.py` | `center_manage`, `center_improve` |
| `taxes_training.py` | `collect_taxes*`, `train_peasants_against_bandits*` |
| `sneak.py` | `sneak_into_town*` |
| `misc_town.py` | `cannot_enter_court`, `lady_visit`, `town_bandits*`, `disembark`, `ship_reembark`, `enemy_offer_ransom_for_prisoner`, `town_cheats*`, `rename_court`, `town_tavern_prostitution*`, `buy_ship` |
| `encounter.py` | `simple_encounter`, `encounter_retreat*`, (`pre_join` is in `join_battle.py`) |
| `battle_results.py` | `battle_debrief`, `total_victory`, `enemy_slipped_away`, `total_defeat`, `permanent_damage` |
| `join_battle.py` | `pre_join`, `join_order_attack`, `order_attack_begin`, `order_attack_2` |
| `siege.py` | `cut_siege_without_fight`, `siege_attack_meets_sally`, `construct_ladders/tower`, `siege_join_defense`, `enter_your_own_castle`, `castle_taken*` |
| `faction_battle.py` | `leave_faction`, `give_center_to_player*`, `oath_fulfilled` |
| `kingdom_management.py` | `faction_orders`, `marshall_selection_candidate_ask`, `kingdom_army_*`, `invite_player_to_faction*`, `question_peace_offer`, `minister_confirm`, `auto_return_to_map`, `notification_relieved_as_marshal` |
| `notifications.py` | all `notification_*` menus (30) |
| `captivity.py` | all `captivity_*` menus (14) |
| `training.py` | all `training_ground*` menus (8) |
| `dplmc.py` | all `dplmc_*` menus not covered above (33) |
| `locations.py` | `zendar`, `salt_mine`, `four_ways_inn`, `test_scene`, `battlefields`, `dhorak_keep` |
| `misc.py` | `fuck*`, `fucked_by_enemy*`, `choose_banner`, `content_options`, `fuck_encounter`, `dplmc_choose_disguise`, `dplmc_preferences`, `dplmc_domestic_policy`, `dplmc_affiliate_end`, `startgame_mod_options`, `auto_trade`, `lost_tavern_duel`, `establish_court` |

## How the pieces reassemble

`module_game_menus.py`'s `game_menus = [...]` list is now empty. Instead:

```python
from game_menus import *          # pulls in the combined `game_menus` list
import header_scenes
from template_tools import *
from module_scenes import scenes
# ... scene-template generation that does game_menus += choose_scene_template.generate_menus(...)
# ... modmerger hooks (game_menus) ...
```

`game_menus/__init__.py` imports every `<topic>_menus` list and `game_menus.extend()`s
them in **original menu order** (each file's menus are in their original file position;
files are ordered by the earliest menu's original line). The entry-point menu
`start_game_0` remains first — ordering is preserved for ID stability and the
character-creation entry point.

Each topic file starts with the same header imports the old single file had
(`header_game_menus`, `header_parties`, `header_items`, `header_mission_templates`,
`header_music`, `header_terrain_types`, `header_triggers`, `module_constants`, all
cp1254). There are no nested `__init__.py` assembly stubs inside `game_menus/` — the
top-level `__init__.py` is the only combiner, mirroring `scripts/`'s pattern.

## Editing rules for future devs

- **Edit an existing menu**: open the matching topic file (e.g. a castle menu →
  `castle.py`); you do **not** touch `__init__.py`.
- **Add a menu**: append it to the right topic file. Only create a new file (and add a
  `from game_menus.<file> import <file>_menus` + `game_menus.extend(...)` to
  `__init__.py`) if none of the 23 existing topics fit.
- **Keep `start_game_0` first** in `character_creation.py` and preserve relative menu
  order within a file — list order backs `ID_menus.py` and save compatibility.
- The `module_game_menus.py.bak` file is the pre-split original; keep it locally as a
  reference but do not commit it.
- After any change, run `compile.bat` (Python 2.7, W.R.E.C.K.). Success marker:
  `COMPILATION SUCCESSFUL`.

## Build / verification

- Full W.R.E.C.K. compile passes: `COMPILATION SUCCESSFUL` under Python 2.7.18.
- All 23 `source/game_menus/*.py` files (plus `__init__.py`) pass py2.7 syntax as
  imported by the compiler.
- Menu count unchanged (253), menu order unchanged, generated `ID_menus.py` identical
  to pre-split.
- Two harmless `declared but never used` warnings remain from the pre-existing
  `module_simple_triggers.py` placeholder triggers (see update-012) — unrelated to
  this change.

## Notes

- **Behavior-neutral** modularization only. No gameplay logic, menu text, conditions,
  or consequences were modified.
- This mirrors the `scripts/` (update-012) and `presentations/` splits; the
  `game_menus/` layout follows the same "domain folder + `__init__.py` combine, no
  inline copies" convention.
- Skills updated: `warband-project-orientation/SKILL.md` (repo map, split-status
  table, new `game_menus/` subsection) and `warband-modsys/SKILL.md` (scope note no
  longer lists `module_game_menus.py` as "not split").
- Re-running the build regenerates `source/ids/ID_*.py` (expected; never hand-edit).
