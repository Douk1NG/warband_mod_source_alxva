# Project Rules

- Ask before changing ANYTHING. No guessing, no assumptions.
- User is in charge — they say what to do and how.
- If a request is ambiguous, ask for clarification before acting.
- NEVER run `git checkout`, `git revert`, `git reset`, `git clean` or any destructive/history-rewriting git command without explicit user authorization. Ask first.
- ALWAYS compile (`compile.bat`) after ANY code change. No exceptions.

## Slot collision: dplmc autoloot vs DtheHun tattoo/armor (2026-09-05)

Slots 155–160 are double-booked:
- 155 = `slot_troop_encounters` (DtheHun) AND `dplmc_slot_upgrade_armor` (autoloot)
- 156 = `slot_troop_assaults` (DtheHun) AND `dplmc_slot_upgrade_horse` (autoloot)
- 157 = `slot_troop_entertainer` (DtheHun) AND `dplmc_slot_upgrade_wpn_0` (autoloot)
- 158 = `slot_troop_tattoo` (DtheHun, used as material name in `cur_item_set_material`) AND `dplmc_slot_upgrade_wpn_1` (autoloot) ← **this is the "Unable to find material You_can't_be_serious!" / "Intelligence" bug**
- 159 = `slot_troop_armor_slots_begin` AND `dplmc_slot_upgrade_wpn_2`
- 160 = `slot_troop_helm_slots_begin` AND `dplmc_slot_upgrade_wpn_3`

**Why it manifests as "Unable to find material <random string>":** Customizable armor `ti_on_init_item` does
```python
(troop_get_slot, ":color", ":troop_no", slot_troop_tattoo),  # reads slot 158
(gt, ":color", 0),
(val_add, ":color", "str_ca_skin"),                            # color + 3630
(str_store_string, s1, ":color"),
(cur_item_set_material, s1, 1),                                # s1 treated as material NAME
```
When autoloot writes an `itp_type` value (2-20) to slot 158, the engine looks for a material with the name of whatever string happens to be at that offset in `strings.txt` — e.g. offset 9 → `str_censure_response_3` ("You can't be serious!"), offset 18 → `str_attribute_str` ("Strength"), offset 20 → `str_attribute_int` ("Intelligence").

**Current layout (post-2026-09-05 fix):** dplmc autoloot slots moved to 166–171, contiguous, clear of the DtheHun range. Save compat loss: existing saves will have 0 in the new slots and the old values orphaned at 155–160. Tattoo/armor-mesh/helm-mesh data in those slots from the old saves is **lost** — user must re-select tattoos and re-toggle armor/helm mesh components after first load.

**When debugging "Unable to find material <text>" warnings:** check if the string is a `str_censure_response_*` or `str_attribute_*` value. If yes, the bug is the slot collision. If no, look for an actual missing material in `materials.txt` / item mesh setup.

## Second slot collision: dplmc autoloot vs custom armor init range (2026-09-06)

After moving dplmc slots to 166–171, a **second** collision surfaced: `set_custom_armor_slots.py` writes `-1` (sentinel for "no component") to **every** slot in `[slot_troop_armor_slots_begin=159, slot_troop_helm_slots_end=176)` for every troop from 0 to `trp_coop_companion_equipment_ui_0`. The dplmc wpn slots 168–171 sit inside that range, so they get clobbered with `-1` on every new game start. The `create_wpn_slot_overlay` loop iterates over the combo items (itp_type 0, 2-8, 14-18) and `val_mod 100` on `-1` doesn't match any, so the combo defaults to position 0 = "Bullets" — the user sees "Bullets" for a fresh save and thinks the autoloot is broken.

**Why the original 155–160 range was safe:** the dplmc slots lived at 155–160, *below* the custom-armor range (159–176). The move to 166–171 placed them inside the range.

**Why the user reported "it persists on the companion but resets on the player":** `set_custom_armor_slots.py` only iterates from troop 0 up to `trp_coop_companion_equipment_ui_0`. Companions above that ID are untouched (slots stay 0). Heroes below it (including trp_player) get `-1` written.

**Fixes applied (commit pending):**
1. **`source/scripts/set_custom_armor_slots.py`** — added `(neg|is_between, ":slot_no", dplmc_slot_upgrade_wpn_0, dplmc_slot_upgrade_wpn_3 + 1)` guard so dplmc slots 168–171 are skipped. Root cause fix; takes effect for new inits.
2. **`source/scripts/dplmc_initialize_autoloot.py`** — one-time migration: when `$g_autoloot` flips from != 2 to 2, iterates trp_player..heroes_end and sets any dplmc slot < 0 to 0. Fixes existing saves that were corrupted by the pre-fix version of `set_custom_armor_slots.py`.
3. **`source/scripts/create_wpn_slot_overlay.py`** — defensive display: if `raw < 0`, treat as `cur_value = 0` so the combo shows "Keep current" instead of defaulting to "Bullets".
4. **`source/scripts/update_wpn_slot_itp.py`** — defensive write: if `:slot_value < 0`, sanitize to 0 before the `slot_value - (slot_value mod 100) + item_type` arithmetic, which otherwise yields a garbage negative.
5. **`source/game_menus/mnu_camp_action.py`** — `camp_autoloot` menu now sets `$temp = trp_player` in addition to `$g_selected_troop`. The presentation reads `$temp`, not `$g_selected_troop`, and the menu was leaving `$temp` to whatever was left over from a prior session.
6. **`source/presentations/prsnt_dplmc_autoloot_upgrade_management.py`** — hero list iteration changed from `i_stack, 0, :num_stacks` to `i_stack, 1, :num_stacks` to match the original Dickplomacy Reloaded2 behavior. The fork had accidentally included the player in the clickable hero list, so clicking any companion row by accident silently switched `$temp` to that companion — the user would then configure the companion thinking they were configuring the player, and on re-opening the menu (which resets `$temp` to trp_player) saw the player slots "reset" to the unchanged values. The click→write pipeline was always correct; the bug was the silent `$temp` switch.

**Lesson for future slot moves:** when picking new positions for troop slots in this module, run `grep -n "slot_.*_begin\s*=\|slot_.*_end\s*=" source/module_constants.py` and check that the new positions don't fall inside any `*_begin .. *_end` range. Common offenders: `slot_troop_armor_slots_begin..slot_troop_helm_slots_end` (159–176, custom armor), `slot_troop_presentation_slot_*` ranges, any `dplmc_slot_*_begin..dplmc_slot_*_end` range from the diplomacy module.

**Lesson for hero list iterations:** when iterating `p_main_party` companion stacks, always start from `i_stack = 1`, not `0`. The player is always at stack 0; including it in the clickable list will silently overwrite any `$temp` the user just configured. The original Dickplomacy Reloaded2 used `1, :num_stacks` — the fork had been changed to `0, :num_stacks` at some point, which caused confusing "reset" symptoms whenever the user clicked the wrong row.

## Presentations — margins are user-requested, not default (2026-09-08)

This is not CSS or a web page. NEVER add default margins/padding to a presentation. The parchment `mesh_hud`/`hud.dds 1024` frame is the border — content at `X 0`/`Y 0` is already inside. Only add a margin when the user explicitly requests it (e.g. "X20→X680 Y0→Y800"). When defining a grid, store `X_MIN/X_MAX/Y_MIN/Y_MAX` from the user, not from `280,80,700,580` or `700×580` assumptions. Go to the limit the user gave first, then refine -20, never increment +10 to the border.

## `tf_scrollable` Y chain: end at Y=0, not negative (2026-10-20, Main Settings single-col rewrite)

**Symptom:** in `prsnt_camp_hub.py` Main Settings panel (index 12), the bottom items (Battle, Companions) don't render even though the engine compiles clean. The container is `tf_scrollable` with `s0` (empty text), area 690x590. Children rendered with the standard `val_sub, ":cur_y", N` pattern.

**Root cause:** the Warband engine's `tf_scrollable` / `tf_scrollable_style_2` does NOT scroll content rendered at negative Y. The Y chain in `source/scripts/settings_content_ui.py` started at `cur_y = 700` and the last item landed at Y=-490. The engine just clipped everything below Y=0 silently.

**The fix:** follow the XGM real pattern at `modmerger/mods/xgm_mod_options/xgm_mod_options_presentations.py:72-76`:
1. Before adding children, calculate `total_height = sum of all rows + headers` (here: 1225u for 22 items + 5 headers)
2. If `total_height < pane_height`, clamp to `pane_height - item_height/2` (so short panels fill the visible area)
3. Set `cur_y = total_height` � **NOT** a hardcoded high number like 700
4. The last item lands at exactly Y=0 (or Y > 0 if clamped)
5. Container `area_size_y` stays at 590; scroll range is `total_height - area_size_y` automatically

**Things that LOOK like fixes but DO NOT work** (verified this session):
- `tf_scrollable` ? `tf_scrollable_style_2` swap: no effect on scroll range
- `s0` (empty) ? `str_empty_string` swap (`"str_empty_string"` is `" "` per `module_strings.py:7`): no effect
- Increasing `area_size_y` from 590 to 1280: content above Y=area_size_y is still cut off
- Adding a `mesh_white_plane` "scroll anchor" at negative Y: internet myth � those lines are **commented out** in the actual XGM source (`xgm_mod_options_presentations.py:110, 128, 146`)

**Debug checklist when scroll doesn't show items** (in order of likelihood):
1. Confirm `cur_y` lands at exactly Y=0 for the last item (not negative)
2. If multiple items missing, check they aren't clipped by the container's `area_size_y` � `overlay_set_area_size` defines the visible window
3. If using `tf_scrollable_style_2`, confirm `area_size_y >= total_height` or the bottom rows will be clipped regardless of scroll
4. Working panels to compare: `prsnt_equip_npcs.py:258-260`, `prsnt_manage_inventory.py:135-137`. Both compute `cur_posy` from item count, not hardcoded.

**Applied in:** `source/scripts/settings_content_ui.py` (Main Settings, single-col rewrite). `cur_y = 1225` covers 22 items + 5 headers; container `area_size_y = 590` gives 635u of scroll range.
