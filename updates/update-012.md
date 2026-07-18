# Update 012 - Module Scripts Domain Reorganization (2nd refactor pass)

## Summary

Second pass at restructuring `source/scripts/`. This pass resequences/re-labels the
"everything-at-top-level" domains into a cleaner taxonomy, dissolves the catch-all
`misc/` folder entirely, renames three misnamed domains, splits `feats/` into its
constituent concerns, and migrates the last inline legacy scripts out of
`module_scripts.py` so that file is now a pure import + `.extend()` re-assembly.

The result is **27 domain files** under `source/scripts/`, grouped into a shallow
domain tree (e.g. `battle/`, `features/`, `quests/`, `faction_ai/`).
`module_scripts.py`'s `scripts = [ ]` block is now **empty** — there are no
duplicate/inline script copies anywhere in the tree.

A follow-up adjustment flattened the `features/` sub-folders (`inventory/`,
`modifiers/`, `weapon_toggle/`) into direct files, and moved `tavern/`,
`features/courtship/`, `features/feast/`, `features/rebellion/` up into their
proper domains (`centers/`, `quests/`, `faction_ai/`) so the `features/` folder
holds only inventory-related files. The final `features/` layout is flat:
`features/inventory_scripts.py`, `features/item_modifiers_scripts.py`,
`features/weapon_toggle_scripts.py`.

## Changes

### Renames / moves (git mv — history preserved)

| Before | After |
| ------ | ----- |
| `scripts/core/core_scripts.py` | `scripts/engine/engine_scripts.py` |
| `scripts/heraldry/heraldry_scripts.py` | `scripts/banners/banners_scripts.py` |
| `scripts/orders/orders_scripts.py` | `scripts/battle/formation_orders/formation_orders_scripts.py` |
| `scripts/feats/all_items_scripts.py` | `scripts/features/item_modifiers_scripts.py` |
| `scripts/feats/manage_inventory_scripts.py` | `scripts/features/inventory_scripts.py` |
| `scripts/feats/toggle_weapons_scripts.py` | `scripts/features/weapon_toggle_scripts.py` |
| `scripts/tavern/tavern_scripts.py` | `scripts/centers/tavern_scripts.py` |
| `scripts/features/courtship/courtship_scripts.py` | `scripts/quests/courtship_scripts.py` |
| `scripts/features/feast/feast_scripts.py` | `scripts/quests/feast_scripts.py` |
| `scripts/features/rebellion/rebellion_scripts.py` | `scripts/faction_ai/rebellion_scripts.py` |

### New top-level domains created (extracted from `misc/`)

- `scripts/player/player_scripts.py` (16 scripts) — player-party / character features
- `scripts/centers/tavern_scripts.py` (1 script) — `initialize_tavern_variables`
- `scripts/ui/ui_scripts.py` (28 scripts) — notifications, presentation hooks
- `scripts/battle/tactics/tactics_scripts.py` (33 scripts) — team-field tactics
- `scripts/quests/courtship_scripts.py` (11 scripts) — weddings
- `scripts/quests/feast_scripts.py` (1 script) — feast rate calc
- `scripts/faction_ai/rebellion_scripts.py` (4 scripts) — rebellions

### `features/` flattened to direct files

The intermediate sub-folders under `features/` (`inventory/`, `modifiers/`,
`weapon_toggle/`) were removed; the scripts now live directly under `features/`:
`features/inventory_scripts.py`, `features/item_modifiers_scripts.py`,
`features/weapon_toggle_scripts.py`. `tavern/`, `features/courtship/`,
`features/feast/`, `features/rebellion/` were moved up into `centers/`, `quests/`,
and `faction_ai/` respectively — there is no longer an `items/` folder.

### `misc/` dissolved

`scripts/misc/misc_scripts.py`, `misc_scripts_extra.py`, `misc_scripts_extra2.py`
were **deleted**. Their 359 scripts were redistributed into proper domains:
multiplayer, encounters, player, siege, party_ai, economy, engine, morale,
training_ground, npcs, diplomacy, items, ui, centers, battle/tactics,
battle/formation_orders, quests, rebellion, music, courtship, feast, inventory,
banners, weapon_toggle, features/inventory.

### Inline legacy scripts migrated out of `module_scripts.py`

The 7 scripts that previously lived inline in `module_scripts.py`'s `scripts = [...]`
block were moved into their proper domains:

- `calculate_castle_prosperities_by_using_its_villages` → `centers/centers_scripts.py`
- `change_player_relation_with_lords_after_battle` → `npcs/npcs_scripts.py`
- `faction_last_reconnoitered_center` → `faction_ai/faction_ai_scripts.py`
- (remaining 4 previously migrated: `npc_decision_checklist_peace_or_war`,
  `diplomacy_faction_get_diplomatic_status_with_faction`,
  `npc_decision_checklist_faction_ai_alt`, `reduce_exact_number_to_estimate`)

### Shared Python helpers relocated

- `keys_array()` → `engine/engine_scripts.py` (was in `misc_scripts_extra.py`)
- `make_noswing_weapons(items)` → `features/weapon_toggle_scripts.py`
  (was in `misc_scripts_extra.py`; its `from module_items import items` import now
  lives at the top of the weapon_toggle file)

### `__init__.py` stubs

All domain `__init__.py` files are now empty encoding-only stubs. The old
`feats/__init__.py` that concatenated three files no longer exists (the domain was
split). `__init__.py` stubs were added where missing for Python 2.7 package support
(`battle/`, `battle/formation_orders/`, `battle/tactics/`, `player/`, `centers/`
had been missing them in earlier passes). After the flatten, `features/` keeps only
its own `__init__.py` (no sub-folder stubs).

### `module_scripts.py` import/extend list

Updated to import every new/renamed domain file and `scripts.extend(...)` it in a
fixed order. Imports now read `scripts.features.item_modifiers_scripts`,
`scripts.features.inventory_scripts`, `scripts.features.weapon_toggle_scripts`,
`scripts.centers.tavern_scripts`, `scripts.quests.courtship_scripts`,
`scripts.quests.feast_scripts`, `scripts.faction_ai.rebellion_scripts`. No inline
`scripts = [...]` content remains.

### `module_simple_triggers.py` — save-compat placeholder triggers

Two **no-op** simple triggers (`(1.0, [(assign, ":ctdn_1", 0)])` and `(1.0,
[(assign, ":ctdn_2", 0)])`) were added immediately after the `ti_simulate_battle`
trigger. These do nothing and exist only to **preserve the simple_trigger count** so
existing save files do not desync/corrupt after the domain changes. They are
intentionally temporary debug scaffolding — remove them once the save-compat concern
is resolved (and adjust the trigger count accordingly). They emit two harmless
"declared but never used" warnings at compile time.

## Build / verification

- Full W.R.E.C.K. compile passes: `COMPILATION SUCCESSFUL` under Python 2.7.18.
- All 57 `source/scripts/**/*.py` files pass `py_compile` (py2.7 syntax).
- The two placeholder triggers in `module_simple_triggers.py` are the only
  behavior-neutral additions (debug scaffolding, not gameplay logic).

## Notes

- **Maintenance-only** for the rename/split — no script *behavior* changed; only file
  locations and `module_scripts.py` wiring changed. The `misc/` deletion is a
  structural cleanup, not a logic change.
- The `feats/` domain no longer exists. Any reference to `feats_scripts`,
  `feats/all_items_scripts.py`, etc. in other docs/skills is now stale — see
  `references/domain_index.md` for the current 27-file layout.
- Re-running the build regenerates `source/ids/ID_*.py` (expected; never hand-edit).
- Future devs: there are no duplicate script copies anymore. To find a script, grep
  `source/scripts/**/*.py` and consult `references/domain_index.md`.
