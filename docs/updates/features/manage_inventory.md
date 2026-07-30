# Manage Inventory Screen

Inventory management accessible from the camp action menu or by pressing [M]. Uses `prsnt_equip_npcs` (replaces old `prsnt_manage_inventory`).

## source/game_menus/mnu_camp_action.py
- Camp action option "Manage your inventory." opens `prsnt_equip_npcs`

## source/presentations/prsnt_equip_npcs.py
- Equipped items panel (slots 0-8) with lock toggles
- Inventory grid (6×8 = 48 per page) with pagination
- Red overlay on items the selected troop cannot use
- Lock toggles on all items (uses `trp_temp_array_lock`)
- Hero sidebar — scrollable list of heroes; gold highlight for selected
- Weapon set selector (Arms 1 / Arms 2)
- Mass actions: Upgrade all / Remove all / Copy all + Apply
- action checkboxes: Weapon 1-4, Armors, Horse
- Re-sort button, Tips button
- Arrow keys / WASD to switch heroes; F key to toggle weapon sets
- Uses `trp_temp_array_a/b/c/d/e/f` for overlay/item/hero tracking

## source/scripts/exchange_two_items_of_slots.py
- Rewritten to use `$g_selected_troop` and `$g_cur_page_of_loot_pool`

## source/module_simple_triggers.py
- Hotkey [M] opens `prsnt_equip_npcs` (not `prsnt_manage_inventory`)
