# Camp Hub

## What it is

A redesigned Camp menu (`mnu_camp` → `prsnt_camp_hub`) that replaces the overwhelming linear menu with a sidebar + right-panel layout.

- **Sidebar** (fixed, 0–260 wide): 16 categories (4 settings + camp actions + cheats). Selection highlight in `0xC8A000`.
- **Right panel** (scrollable, 280–970 wide): the active category's view (book, recruit, food, inventory, autoloot, walk, wait, retire, settings, formations, tournament, camera, cheats, etc.).

Background is `mesh_hud` / `hud.dds 1024` — already provides the sidebar+parchment look, no overlay hacks required.

## How to extend

Add a new sidebar entry in `source/presentations/prsnt_camp_hub.py:38-148` (the `:`pos_y` chain under "Sidebar list starts below the blue cartouche"). Set the selected index, then add the corresponding right-panel branch in the `try_begin` chain that starts at `:185` (the right-panel container block).

Each right-panel category resets `$g_camp_hub_container` and uses `set_container_overlay` to add its own children. See existing implementations for examples (`g_camp_hub_selected_index` 0, 1, 2, 3, 4, 5, 6, 10, 11 are simple views; 12/13/14 use shared UI helpers in `source/scripts/settings_content_ui.py`, `formation_shared_ui.py`, `tournament_shared_ui.py`).

## Cheat mode show/hide (sidebar)

The Cheats sidebar entry is always created but its visibility is toggled based on `$cheat_mode`. The handler in `settings_content_handle_event` for `$g_settings_btn_24` updates the sidebar entry's `overlay_set_display` without restarting the presentation (preserves scroll position).

## Hub helper scripts

15 canonical `prsnt_create_*` scripts under `source/scripts/` are the building blocks (`mesh_overlay`, `text_overlay`, `check_box`, `game_button`, `combo_button`, `text_box`, `troop_image`, `troop_image_size`, `lines`, `lines_to`, `grid_position`, `scrollable_container`, `item_overlay`, `combo_label`, `number_box`). New code should call these directly instead of the legacy `modmerger/mods/kingdom_custom_troop_tree_creator/kct_scripts/ui_helpers.py` (which is now a thin wrapper for backward compat with KCTT).

## Main Settings single-column layout (2026-10-20)

The Main Settings panel (`$g_camp_hub_selected_index == 12`) is **single-column** for the first time in the mod.

### Categories in order
1. **Features** — Cheat Mode, Spawn Black Khergits, Decapitation, Horse Speed, Battle Continuation, Auto Upgrade (6 items)
2. **Dickplomacy** — Sexual Content, Polygamy, Disable Gay, Feast Dancers (4 items)
3. **Diplomacy** — Prejudice, AI Changes, Economy Changes, Disguise System, Returning from Exile (5 items)
4. **Battle** — Minimap, Shield Bash, Troop HP Bars, HP Bar Distance Limit, Troop Ratio Bar, Realistic Casualties, Terrain Advantage (7 items)
5. **Companions** — Keep Companions, Companion Bodyguards, Disable Companion Complaints (3 items)

Total: 22 items + 5 headers.

### Y chain pattern (XGM-style)

`source/scripts/settings_content_ui.py:25` sets `cur_y = 1225` (total content height = sum of all rows + headers + top-air reserve). Each row subtracts its row height via `val_sub, ":cur_y", N`. The **last item lands at exactly Y=0**, which is required for the container's `tf_scrollable` to render all children correctly.

Container is `tf_scrollable` at (280, 0), area size 690×590. Scroll range is `1225 - 590 = 635u`. Wheel scroll works natively.

See AGENTS.md "tf_scrollable Y chain" entry for the full debug checklist.

### Tooltips

`source/module_strings.py:4947-4964` adds 18 `tip_settings_*` strings for: cheat_mode, sexual_content, polygamy, disable_gay, black_khergits, decapitation, realistic_wounding, terrain_advantage, battle_continuation, prejudice, ai_changes, economy_changes, disguise, lord_recycling, keep_companions, companion_bodyguards, companion_complaints, auto_upgrade.

`tip_settings_horse_speed` and `tip_settings_feast_dancers` are intentionally absent — user was unsure of exact semantics. Add later if needed.

## Container resize note (in `prsnt_camp_hub.py:197`)

The Main Settings container was tweaked during this iteration:
- Width 690 (was 720), positioned at X=280 — keeps the scrollbar visible inside the parchment frame (X=300 earlier put the right edge at 1020, off-screen under the frame).
- Comment block at `:184-191` documents the resize history.
