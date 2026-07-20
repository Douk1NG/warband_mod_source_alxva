# update-014 — game_menus granular split + thematic re-classification

## What changed

`source/game_menus/` (formerly a handful of big topic files such as
`sneak.py`, `camp.py`, `dplmc.py`) was first split into one file per menu
tuple, then the menus were re-filed into real thematic topic folders.

Each menu file exports a single `<menu_id>_menu` list containing exactly one
6-field menu tuple:

```
source/game_menus/
  __init__.py                 <- imports each topic sub-package, extends in topic order
  <topic>/__init__.py         <- imports each mnu_*.py, extends into <topic>_menus
  <topic>/mnu_<menu_id>.py    <- one menu tuple
  ...
```

The extend sequence IS the order — it drives the generated menu IDs. Reordering
shifts `ID_menus.py` numbers (expected; save-incompatible by design). It is
generated output and must never be hand-edited or trusted as source of truth.

## Final topic folders (22)

After the re-classification the corpus holds **291 menus** across these folders:

| Folder | Contents (theme) |
|---------|--------------------|
| `battle` | former `battle_results` + `join_battle`, plus `mnu_bandit_lair` (bandit-lair attack menu) |
| `camp` | camp actions, retirement, `mnu_content_options`, `mnu_startgame_mod_options`, `mnu_close`, cheat menus moved to `cheats` |
| `captivity` | captivity / prisoner menus (minus the kingdom-army-quest ones, moved to `kingdom_management`) |
| `castle` | castle entry/meeting/taken (minus `mnu_castle_besiege`, moved to `siege`) |
| `center_management` | center improve/manage |
| `character_creation` | start/creation/tutorial (minus the two `custom_battle_*` menus) |
| `cheats` | all `camp_cheat*`, `cheat_*`, `town_cheats*`, `party_cheat`, `cheat_reports`, `mnu_test_scene` |
| `court` | `establish_court`, `choose_banner`, `lady_visit`, minister/feast visit content |
| `custom_battle` | `mnu_custom_battle_end`, `mnu_custom_battle_scene` |
| `diplomacy` | all `dplmc_*` + faction war/peace/center notifications + `faction_battle/*` + `mnu_dickplo_town_manage` + dplmc trade/loot menus |
| `dickplomacy` | adult/NSFW content (`fuck*`, `fucked_by_enemy*`, `town_tavern_prostitution*`, `village_enslave_complete`, `recruit_volunteers_dickplo_main`) |
| `kingdom_management` | faction orders, vassalage invites, peace offer, marshal selection, minister, kingdom-army quest chain (no longer holds `bandit_lair`) |
| `notifications` | all `mnu_notification_*` (returned here from `diplomacy`/`kingdom_management`) + debug/loot/garden/merchant |
| `reports` | character/center/faction/morale/economy reports |
| `scenes` | map encounter / scene-entry points: `battlefields`, `dhorak_keep`, `four_ways_inn`, `salt_mine`, `zendar` (formerly `/locations`) |
| `siege` | siege menus + `mnu_castle_besiege` + `mnu_siege_started_defender` |
| `town` | town services + `sneak/*` (merged in) + town trade/hire/auction |
| `training` | `training_ground*` menus (peasant-training `train_peasants_*` moved to `village`) |
| `village` | village menus + cattle-herd + `train_peasants_against_bandits*` |
| `taxes` | `collect_taxes*` (split out of former `taxes_training`) |
| `tournament` | tournament menus |

Every `mnu_*.py` and `__init__.py` carries the
`# -*- coding: cp1254 -*-` header and the standard `header_*` / `module_constants`
imports.

## Verification method (reused for every move batch)

- **Content fidelity**: AST-compare `ast.dump(tuple)` of each menu in the
  pre-change committed state vs the new state — must be identical. (Simple
  relocations keep byte-identical content; confirmed per move.)
- **Order fidelity**: the authored extend sequence in `__init__.py` is the
  source of truth, not `ID_menus.py`. A manifest (`topic|menu_id` per line,
  ordered by original global position) is kept in sync with disk; assert
  manifest ↔ disk have 0 missing / 0 mismatched entries (291 each).
- **Gate**: `compile.bat` → **COMPILATION SUCCESSFUL**.

## Gotchas encountered (and fixed)

- **Never diff `ID_menus.py`** to judge correctness — it is generated and
  shifts on every reorder. Verify the authored list order instead.
- **Double `mnu_` prefix bug**: when regenerating `<topic>/__init__.py`, the
  menu id already contains `mnu_`, so the import must be
  `from game_menus.<topic>.mnu_<id> import <id-without-mnu->_menu`
  — do not prepend another `mnu_`.
- **Topic-order list must include every folder**: a regeneration once omitted
  `notifications` from the top-level topic order, so `notifications_menus`
  was never imported into the global `game_menus` list → compile failed with
  `illegal reference mnu.debug_alert_from_s65`. Always regenerate the
  top-level `__init__.py` from the complete folder list and recompile.
- **Manifest can desync from disk** after ad-hoc edits; rebuild the manifest
  from disk truth (sorted by original global position) before regenerating.

## Notes for future edits

- To **edit** a menu: open `source/game_menus/<topic>/mnu_<menu_id>.py`.
- To **add** a menu: create `mnu_<id>.py` in the right topic folder, then add
  a `from game_menus.<topic>.mnu_<id> import <id>_menu` line and an
  `<topic>_menus.extend(<id>_menu)` line to that folder's `__init__.py`, and
  add the topic (if new) to the top-level `__init__.py`.
- To **move** a menu: move the file, update both source and destination
  `<topic>/__init__.py`, and keep the intended position in the extend sequence.
  Regenerate the top-level `__init__.py` from the full folder list and recompile.
- `ID_menus.py` is regenerated every compile; do not hand-edit or treat its
  numbers as stable across reorders.
