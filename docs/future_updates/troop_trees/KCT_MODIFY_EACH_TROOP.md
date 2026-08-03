# Kingdom Custom Troop Tree Creator — Step 2: "Modify Each Troop" (Customisation Store)

Handoff contract for the **next agent session**. Replaces the node-click stub of the
creation viewer (`prsnt_cstm_create_troop_tree`) with the full per-troop customisation
store (name, stats, skills, proficiencies, equipment).

Predecessor contract: `KINGDOM_CUSTOM_TROOP_TREE_CREATOR.md` (the M1 picker + bridge).
This doc assumes that is DONE and builds on it.

---

## 1. What is already DONE (do not redo)

- **M1 picker** `prsnt_cstm_choose_troop_tree`: tree + gender selects, horizontal tree
  preview, "Choose" hands off to `prsnt_cstm_create_troop_tree`.
- **Creation viewer** `prsnt_cstm_create_troop_tree`: draws the selected tree (presets
  1-3 via `script_kct_create_troop_tree_images`; preset 4 via per-node dummy portraits +
  branch lines + name labels), a prefix text box, an Exit button, ESC-to-picker.
- **Self-contained `script_kct_*` copies** in `..._scripts.py` (create_mesh_overlay,
  create_text_overlay, create_game_button_overlay, create_combo_button_overlay,
  prsnt_lines, prsnt_lines_to, create_text_box_overlay, create_troop_image,
  create_troop_image_size, troop_refresh_name, create_troop_tree_images).
- **Preset-4 troops** (22 nodes x 2 skins + dummies) in `..._troops.py`; dummy/custom
  slot linkage (500/501) set at game start.
- **State set by the creation viewer** before the store opens: `$cstm_selected_tree`,
  `$cstm_selected_gender`, `$cstm_troops_begin/end`, `$cstm_num_tiers`,
  `$cstm_presentation_troop`.
- Node clicks currently show `"{s0} - customisation coming soon"` in
  `_build_create_event_ops` — **this is the code to replace.**

Active mods (must stay, see `modmerger_options.py`): `custom_troops` +
`kingdom_custom_troop_tree_creator` (+ the rest of the stock list).

---

## 2. The task (user-approved approach: SELF-CONTAINED PORT)

The user picked **"Port self-contained copy"**: add a new presentation
`prsnt_kct_customise_troop` to the kct mod — a modified copy of the working
`prsnt_cstm_customise_troop` store (in `custom_troops_presentations.py`) — whose Exit
returns to `prsnt_cstm_create_troop_tree`. Then wire the creation viewer's node click to
open it.

### 2a. New presentation `prsnt_kct_customise_troop`

Source: `modmerger/mods/custom_troops/custom_troops_presentations.py:220-927`
(`"cstm_customise_troop"` record) **plus its `modmerge` additions at
`:945-1049`** (item-type combo items + active-skill grid). Port ALL of it into
`..._presentations.py`, renamed to `kct_customise_troop`, with these changes:

1. **Exit button** must do `(start_presentation, "prsnt_cstm_create_troop_tree")`
   instead of `(start_presentation, "prsnt_cstm_view_custom_troop_tree")`
   (line ~907). Keep the `$cstm_item_modifier_selected`/`$cstm_item_page_no` resets.
2. Rename the presentation ID and every `(start_presentation,
   "prsnt_cstm_customise_troop")` self-restart inside it to the new ID.
3. All `script_cstm_*`/`script_gpu_*` calls become `script_kct_*` calls (see §3 — port
   those scripts into the kct scripts file).
4. Do NOT keep the debug `display_message`/commented-out blocks — port only live ops.
5. Import/use the SAME string IDs and array troop IDs that `custom_troops` provides
   (`str_cstm_*`, `trp_cstm_items_*`, `trp_cstm_inventory_values`, `trp_cstm_overlay_*`,
   `trp_cstm_proficiency_requirements`). Do NOT re-declare them — `custom_troops` is
   active and mandatory, so reusing avoids duplicate-ID conflicts. (Same convention as
   the kct mod already uses for `trp_cstm_overlay_troops`, `trp_cstm_presentation_troop_*`.)

### 2b. Wire the node click in the creation viewer

In `_build_create_event_ops` (`..._presentations.py:703-708`), replace the
"customisation coming soon" branch with the reference entry sequence
(`custom_troops_presentations.py:188-203`):

- `(assign, "$cstm_troop_being_customised", ":troop")` — `:troop` is already read from
  `trp_cstm_overlay_troops` on the current branch.
- Back up the dummy's name/plural onto `$cstm_presentation_troop` (needed by the store's
  Reset path).
- `(start_presentation, "prsnt_kct_customise_troop")`.

The store reads `$cstm_items_array` on load (slot `cstm_slot_array_item_type`). Ensure
it is set before the first store open — `custom_troops` sets it to
`cstm_items_arrays_begin` in its game_start ops, but the kct store should not depend on
that silently; initialize it in the creation viewer load (or on node click) if unset,
and reset `$cstm_item_modifier_selected = 0`, `$cstm_item_page_no = 0` when entering.

---

## 3. Scripts the store needs (port into `..._scripts.py` as `script_kct_*`)

All defined in `modmerger/mods/custom_troops/custom_troops_scripts.py` (self-contained
copies — do NOT `call_script "script_cstm_*"` at runtime; that would reintroduce the
dependency the mod avoids). Port each verbatim, rename to `kct_*`, keep identical
operation bodies. This is the bulk of the work.

### UI helpers (replace `script_gpu_*` calls)
| kct name (new) | cstm source (line) |
|---|---|
| `kct_create_scrollable_container` | `gpu_create_scrollable_container` 2205 |
| `kct_create_item_overlay` | `gpu_create_item_overlay` 2314 |
| `kct_create_combo_label_overlay` | `gpu_create_combo_label_overlay` 2345 |
| `kct_create_number_box_overlay` | `gpu_create_number_box_overlay` 2358 |
| *(already ported)* `kct_create_troop_image` | `gpu_create_troop_image` 2373 |
| *(already ported)* mesh/text/game_button/combo/text_box | — |

### Store logic (replace `script_cstm_*` calls)
| kct name (new) | cstm source (line) | notes |
|---|---|---|
| `kct_setup_item_arrays` | `cstm_setup_item_arrays` 1419 | must run at game start (see §5) |
| `kct_get_grid_position` | `cstm_get_grid_position` 2051 | |
| `kct_get_item_from_array` | `cstm_get_item_from_array` 1943 | |
| `kct_troop_get_inventory_value` | `cstm_troop_get_inventory_value` 1742 | |
| `kct_item_get_price_with_modifier` | `cstm_item_get_price_with_modifier` 1717 | |
| `kct_troop_copy_inventory` | `cstm_troop_copy_inventory` 1953 | |
| `kct_cf_cci_imod_appropriate_for_item` | `cf_cci_imod_appropriate_for_item` 1529 | |
| `kct_cf_troop_can_use_item_with_modifier` | `cf_troop_can_use_item_with_modifier` 1632 | |
| `kct_store_item_requirement_stat_to_s0` | `cstm_store_item_requirement_stat_to_s0` 1694 | |
| `kct_dummy_set_attribute` | `cstm_dummy_set_attribute` 437 | |
| `kct_dummy_set_proficiency` | `cstm_dummy_set_proficiency` 1054 | |
| `kct_dummy_set_skill` | `cstm_dummy_set_skill` 735 | |
| `kct_cf_troop_stats_are_different` | `cstm_cf_troop_stats_are_different` 1084 | |
| `kct_cf_troop_equipments_are_different` | `cstm_cf_troop_equipments_are_different` 1125 | |
| `kct_cf_troop_has_horse` | `cstm_cf_troop_has_horse` 1167 | |
| `kct_cf_troop_has_bow_or_crossbow` | `cstm_cf_troop_has_bow_or_crossbow` 1188 | |
| `kct_replace_custom_troop_with_dummy` | `cstm_replace_custom_troop_with_dummy` 2031 | |
| `kct_copy_custom_troop_to_dummy` | `cstm_copy_custom_troop_to_dummy` 2012 | |
| `kct_troop_tree_copy_inventory_if_unmodified` | `cstm_troop_tree_copy_inventory_if_unmodified` 1971 | |
| `kct_troop_tree_copy_stats_if_higher` | `cstm_troop_tree_copy_stats_if_higher` 1308 | |
| `kct_troop_tree_update_stat_minimums` | `cstm_troop_tree_update_stat_minimums` 1342 | |
| `kct_print_skill_to_s0` | `cstm_print_skill_to_s0` 135 | |
| `kct_print_attribute_to_s0` | `cstm_print_attribute_to_s0` 126 | |
| `kct_print_proficiency_to_s0` | `cstm_print_proficiency_to_s0` 144 | |

### Attribute / skill / proficiency point math (transitive deps — trace `call_script` inside the above and port everything referenced)

Attribute: `cstm_get_attribute_points` 175, `cstm_get_attribute_points_spent` 186,
`cstm_get_attribute_points_available` 200, `cstm_get_attribute_points_available_to_upgrade` 213,
`cstm_troop_get_attribute_min_from_points` 234, `cstm_troop_get_attribute_min_from_tree` 277,
`cstm_troop_get_attribute_max_from_points` 343, `cstm_troop_get_attribute_max_from_upgrade` 357,
`cstm_troop_get_attribute_max_from_tree` 375.

Skill: `cstm_get_skill_points` 493, `cstm_get_skill_points_spent` 507,
`cstm_get_skill_points_available` 521, `cstm_get_skill_points_available_to_upgrade` 534,
`cstm_troop_get_skill_min_from_points` 555, `cstm_troop_get_skill_min_from_tree` 564,
`cstm_troop_get_skill_max_from_points` 641, `cstm_troop_get_skill_max_from_upgrade` 655,
`cstm_troop_get_skill_max_from_tree` 673.

Proficiency: `cstm_get_proficiency_points` 803, `cstm_get_proficiency_points_spent` 826,
`cstm_get_proficiency_points_available` 841, `cstm_get_proficiency_points_available_to_upgrade` 854,
`cstm_troop_get_highest_proficiency_from_points` 876, `cstm_troop_get_proficiency_min_from_points` 895,
`cstm_troop_get_proficiency_min_from_tree` 904, `cstm_troop_get_proficiency_max_from_points` 958,
`cstm_troop_get_proficiency_max_from_upgrade` 972, `cstm_troop_get_proficiency_max_from_tree` 992.

Copy/tree helpers: `cstm_troop_copy_stats` 1210, `cstm_troop_copy_stats_if_higher` 1238,
`cstm_troop_tree_copy_stats` 1276, `cstm_troop_reset_stats` 153.

Item filters used by imod/requirement scripts: `cf_item_is_ranged` 1486,
`cf_item_type_is_ranged` 1495, `cf_item_is_missile` 1507, `cf_item_type_is_missile` 1516,
`cstm_item_type_get_cost_modifier` 2551, `cstm_cf_item_is_eligible_equipment_option` 2754.

> **Checklist rule:** after the first port pass, run `grep -o
> 'call_script, "script_[a-z_0-9]*"'` over the new presentation + new scripts and
> confirm every referenced script has a kct_* port. No `script_cstm_*` /
> `script_gpu_*` / `script_prsnt_*` may remain in the kct mod.

---

## 4. Constants to copy into the kct presentations file

From `custom_troops_presentations.py:28-70` (store layout) — rename to `KCT_*` or keep
a local prefix to avoid clashing with the custom_troops module:

- `ACTIVE_FIGHTING_SKILLS` (line 25) — needed by the skill-grid modmerge block.
- `CSTM_INV_*`, `CSTM_STORE_*`, `CSTM_STATS_*`, `CSTM_NAME_*` (lines 28-69), plus
  `CSTM_STATS_GAP_Y`, section heights and points-row constants referenced in the
  skill-grid block (`CSTM_STATS_*_SECTION_HEIGHT`, `CSTM_STATS_POINTS_*`).
- Import `cstm_item_type_strings` from `modmerger/mods/shared/cstm_item_helpers/item_types.py`
  (the custom_troops mod imports it the same way).
- Store slot/string constants come from `custom_troops_constants.py`:
  `cstm_slot_array_num_items/item_type/items_begin`, `cstm_items_arrays_begin/end`,
  `cstm_slot_troop_dummy/custom_troop/base_troop/equipment_modified`,
  `modifier_strings_begin`, `cstm_attribute_strings_begin`, `cstm_skill_strings_begin`,
  `cstm_proficiency_strings_begin`. Either import them or re-declare as local copies
  (the kct scripts file already re-declares the two slot constants it needs).

---

## 5. Game-start operations to add (kct `..._scripts.py`)

The store needs populated item arrays + funds + proficiency requirements. `custom_troops`
already does all of this in its own game_start, but the kct store must be self-contained:
add to the kct `new_start_operations` (which already has the preset-4 slot links):

- `(assign, "$cstm_items_array", cstm_items_arrays_begin)`.
- `(call_script, "script_kct_setup_item_arrays")` — ported from `cstm_setup_item_arrays`.
- Funds per level: the loop over `equipment_funds_available(i)` storing into
  `trp_cstm_inventory_values` (copy `custom_troops_scripts.py:65-67`; port the small
  `equipment_funds_available` helper into the kct file).
- Proficiency requirements loop into `trp_cstm_proficiency_requirements`
  (`custom_troops_scripts.py:54-61`; copy `cstm_proficiency_requirements` from
  `custom_troops_proficiency_requirements.py`).
- Item-type slots on each array troop (`custom_troops_scripts.py:76-77`).
- Presets 1-3 base-troop slot linking is already done by `custom_troops`' own
  game_start — do not duplicate.

> Note: both mods calling these stores duplicate `$cstm_items_array` init and the array
> rebuild; harmless (idempotent slot writes), but keep the kct copies `kct_*`-named so
> the scripts themselves never collide.

---

## 6. Engine facts (verified)

- Combo/number-box/container scripts return the overlay id in `reg1`.
- Store event handler: `store_trigger_param_1` (object), `store_trigger_param_2` (value).
- Restart store after every edit: `(start_presentation, "prsnt_kct_customise_troop")`.
- ESC closes: `key_clicked key_escape` + `presentation_set_duration 0` (already in run ops).
- Screen coords y-up (0 = bottom), `set_fixed_point_multiplier 1000`.
- **The only accepted string-register argument to `call_script` is `str_s0`** (W.R.E.C.K.
  rejects `str_s1`). `str_store_string s0` immediately before the call.
- Custom-troop slots: `cstm_slot_troop_dummy = 500`, `cstm_slot_troop_custom_troop = 501`
  (already in the kct scripts file).
- Save button flow (keep intact): marks `cstm_slot_troop_equipment_modified`, auto-sets
  troop class (cavalry/archers/infantry), copies dummy→real, propagates inventory/stats
  to upgrade children, `troop_sort_inventory` + `troop_equip_items`.

---

## 7. Files

- `modmerger/mods/kingdom_custom_troop_tree_creator/kingdom_custom_troop_tree_creator_presentations.py` — add `prsnt_kct_customise_troop` + node-click wiring
- `modmerger/mods/kingdom_custom_troop_tree_creator/kingdom_custom_troop_tree_creator_scripts.py` — add all `script_kct_*` ports + game-start additions
- `modmerger/mods/custom_troops/custom_troops_presentations.py` — REFERENCE ONLY (do not edit)
- `modmerger/mods/custom_troops/custom_troops_scripts.py` — REFERENCE ONLY (do not edit)
- `modmerger/mods/custom_troops/custom_troops_constants.py` — REFERENCE ONLY
- `modmerger/mods/shared/cstm_item_helpers/item_types.py` — `cstm_item_type_strings` source
- `modmerger/modmerger_options.py` — `mods_active` (unchanged)

## 8. Build / test

- Compile: `python compiler\compile.py tag` from repo root → expect "COMPILATION SUCCESSFUL".
- Export target: `C:\Program Files (x86)\Steam\steamapps\common\MountBlade Warband\Modules\Dickplomacy Reloaded\`
- In-game: Camp → "Test troop tree picker" → pick tree + gender → "Choose" → click a node
  portrait → store opens → edit name/attributes/skills/proficiencies, buy items, Save,
  Exit returns to the creation viewer.
- Default `python` is Python 2.7.18.
- After editing code, ALWAYS compile and confirm "COMPILATION SUCCESSFUL" before stopping.
