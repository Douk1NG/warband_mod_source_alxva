# Update 011 — Presentations modularization (2-phase split)

## Summary

Split the monolithic `module_presentations.py` (23,070 lines, 75 entries, 74 unique) into individual files under `source/presentations/`, following the same domain-split pattern established by `source/scripts/`.

## Phase 1: Domain-level split

14 submodule files across 11 domain subdirectories:

```
presentations/
  arena/arena_presentations.py
  campaign/campaign_presentations.py
  character/character_presentations.py
  character/marshall_selection_presentations.py
  core/game_ui_presentations.py
  core/tutorial_presentations.py
  diplomacy/dplmc_presentations.py
  diplomacy/relations_report_presentations.py
  inventory/inventory_presentations.py
  minigames/minigames_presentations.py
  minimap/minimap_presentations.py
  multiplayer/multiplayer_presentations.py
  party/party_presentations.py
  retirement/retirement_presentations.py
```

Aggregated by `presentations/__init__.py`, imported by `module_presentations.py` (preserving modmerger hooks).

## Phase 2: One file per presentation

Further split all 14 domain files into 74 individual `prsnt_<name>.py` files — one Python file per Warband presentation tuple. Each file is self-contained with its own imports.

Structure:
```
presentations/
  __init__.py                    <- aggregates all 74
  arena/prsnt_arena_training.py
  campaign/prsnt_world_map.py
  campaign/prsnt_troop_ratio_bar.py
  character/prsnt_name_kingdom.py
  character/prsnt_change_color.py
  ...                            <- 74 files total
  multiplayer/prsnt_multiplayer_welcome_message.py
  multiplayer/prsnt_multiplayer_team_select.py
  ...
  retirement/prsnt_spawn_diagnostics.py
  retirement/prsnt_modify_slots.py
```

## Issues encountered and resolved

- **Commented-out presentations**: 5 presentations (`troop_ratio_bar`, `three_card`, `dices_game`, `bank_quickview`, `blackjack`) had commented or inline-commented triggers. `troop_ratio_bar` was fully commented out (every line `#`); replaced with `[]` (valid but empty triggers). The other 4 had inline comments after field values (e.g. `0,#find the lady`) — the initial fix was over-broad and collapsed their triggers too.
- **Duplicate `battle`**: Two entries named `battle` existed; last occurrence kept.
- **Inline comments with parentheses**: Presentation operations use `(...)` syntax, and inline comments like `# (display_message, ...)` contain parentheses. The verification script's bracket-counting parser needed `#` comment skipping to avoid counting these — the original extraction script's bracket-level gating (`bracket_count == 1` for presentation end) handled this implicitly.

## Phase 3: Folder restructuring by verified game use

The 11 original domain subfolders (arena, campaign, character, core, diplomacy,
inventory, minigames, minimap, multiplayer, party, retirement) were an initial
guess and mixed concepts. They were reorganized so that only presentations whose
gameplay context is **verified** (via the menus that `start_presentation` them,
and the `scripts/` domain vocabulary) get a dedicated folder. Everything else is
left as flat files directly under `presentations/` — a wrong category is worse
than no category.

### Folders created (verified context)

| Folder | Presentations | Verified basis |
| --- | --- | --- |
| `multiplayer` | all 30 `multiplayer_*` files | name + `scripts/multiplayer` domain |
| `minigames` | `prsnt_blackjack.py`, `prsnt_dices_game.py`, `prsnt_three_card.py` | name + `module_dialogs.py` context |
| `reports` | `prsnt_budget_report.py`, `prsnt_spawn_diagnostics.py`, `prsnt_jrider_character_relation_report.py`, `prsnt_jrider_faction_relations_report.py`, `prsnt_companion_overview.py`, `prsnt_bank_quickview.py`, `prsnt_all_items.py` | all started from `mnu_reports` / `mnu_reports_economy` / `mnu_dplmc_economic_report` |
| `camp` | `prsnt_retirement.py` (`mnu_camp`), `prsnt_food_options.py`, `prsnt_formation_mod_option.py`, `prsnt_order_display.py` (all `mnu_camp_action`) | verified camp-options menus |

### Left flat in `presentations/` (no agreed category yet)

The old `character/`, `inventory/`, `core/`, `diplomacy/`, `campaign/`,
`arena/`, `party/`, `retirement/`, `minimap/` subfolders were deleted after
moving their files up to `presentations/` root. Flat files:

- banner_background_selection, banner_charge_positioning, banner_charge_selection,
  banner_flag_map_type_selection, banner_flag_type_selection, banner_selection,
  custom_banner, change_color, color_selection, sliders, redefine_keys,
  marshall_selection, name_kingdom  (was `character/`)
- bank, customize_armor, deposit_withdraw_money, manage_inventory, auto_trade_options
  (was `inventory/` + `party/`)
- game_before_quit, game_credits, game_custom_battle_designer,
  tutorial_show_mouse_movement, modify_slots, game_profile_banner_selection
  (was `core/`)
- dplmc_auto_sell_options, dplmc_autoloot_upgrade_management, dplmc_peace_terms,
  dplmc_policy_management, dplmc_set_vassal_title, dplmc_shopping_list_of_food
  (was `diplomacy/`)
- world_map, troop_ratio_bar, mini_map, mini_map_bar  (was `campaign/` + `minimap/`)
- arena_training  (was `arena/`)
- battle, battle_old  (was `party/`; `battle_old` kept as an unregistered file)

### Notes

- External references to presentations are all by **string name** (`"prsnt_..."`),
  never by import path, so moving files between folders required **no edits** to
  `module_game_menus.py`, `module_mission_templates.py`, `module_dialogs.py`,
  `module_simple_triggers.py`, `module_presentations.py`, or any `scripts/` file.
- Only `presentations/__init__.py` was regenerated (imports + `presentations = [...]`
  list, order preserved for ID stability). Per-folder `__init__.py` stubs added
  for the new folders; stale subfolder `__init__.py` files removed.
- `prsnt_battle_old.py` is intentionally excluded from the `presentations` list
  (superseded duplicate kept as a dormant file).
- `compile.bat` → `COMPILATION SUCCESSFUL`; the 74 registered presentation IDs
  remain in their original order (save-compatible).
- The 16 additional entries in `ID_presentations.py` (e.g. `prsnt_mod_option`,
  `prsnt_recruit_volunteers`) are registered via modmerger/xgm patches elsewhere
  and were unaffected.

This resolves the previously-pending `better folder structure for presentations`
item. Further categorization of the flat remainder is deferred until the concepts
can be agreed rather than guessed.