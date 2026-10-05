# Presentations Redesign — Spec & Context (for compact)

**Branch:** `new_presentations` (checked 2026-09-05, base `master`/`fix_besiege`)

## 1. Goal
Redesign all presentations (79 in `source/presentations/*.py:1` + 5 KCTT in `modmerger/mods/kingdom_custom_troop_tree_creator/kct_presentations/*.py:1`).
New UX: camp hub with **anchored left sidebar + right content panel** (replaces overwhelming linear `mnu_camp.py:18` + `mnu_camp_action.py:11` + `mnu_dplmc_preferences.py:11` menu). Sidebar permanent, right panel swaps content without closing presentation. Must resize from fullscreen 1000x750 to right-panel ~700x580.

## 2. Done — Neutral Helper Extraction (Option B)
**Problem:** `script_kct_create_*` lived only in `modmerger/mods/kingdom_custom_troop_tree_creator/kct_scripts/ui_helpers.py:1` (ModMerger-only, fragile for `source/presentations`).

**Solution:** Created 15 canonical scripts in `source/scripts/prsnt_*.py:1`:
- `prsnt_create_mesh_overlay`, `prsnt_create_text_overlay`, `prsnt_create_check_box_overlay`, `prsnt_create_game_button_overlay`, `prsnt_create_combo_button_overlay`, `prsnt_create_text_box_overlay`, `prsnt_create_troop_image`, `prsnt_create_troop_image_size`, `prsnt_prsnt_lines`, `prsnt_prsnt_lines_to`, `prsnt_get_grid_position`, `prsnt_create_scrollable_container`, `prsnt_create_item_overlay`, `prsnt_create_combo_label_overlay`, `prsnt_create_number_box_overlay`

Registered in `source/module_scripts.py:1774` (imports + `scripts.extend` appended at bottom, save-safe). `compile.bat` → SUCCESS.

Aliased `kct_scripts/ui_helpers.py:1` `UI_HELPER_SCRIPTS` to thin wrappers `call_script "script_prsnt_*"`. KCTT `kct_presentations/branch_selector.py:25` etc. still work; new code should call `script_prsnt_*` directly. `troop_editor.py` UI helpers still coexist (both IDs, not yet aliased — defer).

## 3. Camp Hub — Draft Spec
- Sidebar ~250x750 fixed, right panel ~700x580 scrollable (`prsnt_get_grid_position`, `prsnt_create_scrollable_container`).
- Left items = categories from `camp_action` + `preferences` + `cheat` (group later). Selected hilite `0xC8A000` as `tree_files.py:36`.
- Right panel: either SPA (rebuild container on sidebar click) or launcher (`start_presentation` original) — user to decide. Resizing needed: `overlay_set_size` mesh vs text scale different (900 vs 5000+). Define `RIGHT_PANEL = (280,80,700,580)`.

## 4. Next Steps (user at own pace)
1. User reviews presentations in-game one by one.
2. When ready, build `prsnt_camp_hub` wireframe using neutral helpers.
3. Migrate legacy presentations iteratively to right-panel size; first pilot `budget_report` or `bank`.

## 5. How to Test Current Branch
`git checkout new_presentations` → `compile.bat` → launch → test KCTT picker `prsnt_cstm_choose_troop_tree` visuals unchanged.
