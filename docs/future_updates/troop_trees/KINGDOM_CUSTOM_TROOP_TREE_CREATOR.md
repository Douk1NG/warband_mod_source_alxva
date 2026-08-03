# Kingdom Custom Troop Tree Creator — Handoff Contract

This document is the handoff contract for the **creation step** of the Kingdom Custom
Troop Tree Creator mod. A new agent will use this to replace the creation stub with the
real troop-tree creation UI.

Mod: `modmerger/mods/kingdom_custom_troop_tree_creator/`
Active mods (must stay): `custom_troops` + `kingdom_custom_troop_tree_creator` (`modmerger/modmerger_options.py`).

---

## 1. What is already DONE (do not redo)

- **M1 picker** `prsnt_cstm_choose_troop_tree` (`..._presentations.py`): two label→combo rows
  at the top (tree select "Choose your kingdom's troop tree", gender select), the selected
  tree drawn HORIZONTAL (root-left, tiers as columns) in the centre. "Choose" hands off to
  the stub; "Exit"/ESC returns to camp.
- **6 ported helper scripts** `script_kct_*` in `..._scripts.py` (create_mesh_overlay,
  create_text_overlay, create_game_button_overlay, create_combo_button_overlay, prsnt_lines,
  prsnt_lines_to). Self-contained — no `script_gpu_*`/`script_prsnt_*` calls.
- **Preset-4 troop source** `PRESET_4_UNITS` in `..._troops.py` (22 units × 2 skins = 44
  `trp_cstm_custom_troop_4_<skin>_<node>_0` records; matches `extended_progression_tree.md`).
- **Camp test entry** "Test troop tree picker" (`mno_kct_test_tree_picker`) in `..._game_menus.py`.
- **Layout tuning** (verified in `presentations.txt`): tree is smaller and sits ~200 units
  clear of the buttons. See §5 for current constants.

---

## 2. State available on entry to `prsnt_cstm_create_troop_tree`

Set by the picker's "Choose" button (`(start_presentation, "prsnt_cstm_create_troop_tree")`
+ `presentation_set_duration 0`):

| Global | Values | Meaning |
|--------|--------|---------|
| `$cstm_selected_tree`   | 0..3 | index into `PRESET_NAMES` (0-2 = presets 1-3, **3 = preset 4**) |
| `$cstm_selected_gender` | 0/1  | skin id (0 = male, 1 = female) |

Nothing else is set. The creation agent computes troop ranges itself.

---

## 3. What the agent must do

Replace the stub's load/event ops in `..._presentations.py` (`_build_create_load_ops`,
`_build_create_run_ops`, `_build_create_event_ops`) with the real creation UI. The stub
currently draws a title, two debug lines (tree/gender), and an Exit button
(`$cstm_create_tree_exit`); "Exit" → `(change_screen_return)`. You may keep
`$cstm_create_tree_exit` or use your own. Do not remove the `prsnt_cstm_create_troop_tree`
presentation entry — the picker jumps to it by name.

---

## 4. Engine facts (verified)

- Combo button → returns overlay id in `reg1` via `script_kct_create_combo_button_overlay(x, y)`.
- Combo items: `(str_store_string, s0, "@label")` then `(overlay_add_item, overlay, s0)`.
- `(overlay_set_val, overlay, current)` sets the shown selection.
- Presentation events: `store_trigger_param_1` (object), `store_trigger_param_2` (value).
- Restart a presentation: `(start_presentation, "prsnt_...")`.
- ESC close: `key_clicked key_escape` + `presentation_set_duration 0`.
- Screen coords: y-up (0 = bottom of screen), `set_fixed_point_multiplier 1000`.
- **IMPORTANT:** the only accepted string-register argument to `call_script` is `str_s0`
  (W.R.E.C.K. rejects `str_s1`). Always `str_store_string s0` immediately before the call.

---

## 5. Current layout constants (`..._presentations.py`)

```python
NODE_LABEL_SIZE = 750
NODE_LABEL_W    = 170
NODE_LABEL_H    = 45
PREVIEW = (500, 430, 920, 470)   # (cx, cy, width, height) — horizontal tree area
```

- Selects (unchanged): tree label (20,680) font 900, combo (420,660); gender label (610,680),
  combo (810,660).
- Buttons (unchanged): Choose (880,50), Exit (100,50).
- With `PREVIEW` above: preset-4 nodes span x≈40–960, lowest y≈262 (~212 above buttons),
  highest y≈598 (~80 below the selects).

---

## 6. Preset data (troop IDs)

- **Presets 1-3**: `trp_cstm_custom_troop_<tree>_0_<branch>_<tier>` where tree =
  `1_tier`/`2_tiers`/`3_tiers` (requires `custom_troops` mod). Branch/tier indexing matches
  `PRESET_TREES_1_3` in the presentations file.
- **Preset 4**: `trp_cstm_custom_troop_4_<skin>_<node>_0`; 22 nodes × 2 skins; levels
  2/10/18/26/34/40; 11 `upgrade()` + 5 `upgrade2()` links.
- Skins: `tf_male = 0`, `tf_female = 1` (`custom_troops/custom_troops_constants.py`).
- See `docs/future_updates/troop_trees/CSTM_TROOP_TREES_SPEC.md` §3/§4.

---

## 7. Files

- `modmerger/mods/kingdom_custom_troop_tree_creator/kingdom_custom_troop_tree_creator_presentations.py` — picker + creation stub
- `modmerger/mods/kingdom_custom_troop_tree_creator/kingdom_custom_troop_tree_creator_scripts.py` — `script_kct_*` helpers
- `modmerger/mods/kingdom_custom_troop_tree_creator/kingdom_custom_troop_tree_creator_troops.py` — `PRESET_4_UNITS`
- `modmerger/mods/kingdom_custom_troop_tree_creator/kingdom_custom_troop_tree_creator_game_menus.py` — camp test entry
- `modmerger/modmerger_options.py` — `mods_active`

## 8. Build / test

- Compile: `python compiler\compile.py tag` from repo root → expect "COMPILATION SUCCESSFUL".
- Export target: `C:\Program Files (x86)\Steam\steamapps\common\MountBlade Warband\Modules\Dickplomacy Reloaded\`
- In-game: Camp → "Test troop tree picker".
- Default `python` is Python 2.7.18.
