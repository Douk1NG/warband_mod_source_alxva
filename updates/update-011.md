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

pending:: better folder structure for presentations based on game use (e.g. reports, camp, and so on...)