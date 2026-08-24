# Player-Managed Guard Picker ("Pick Guards") — Design & Task Plan

Replaces the **automatic guard selection** approach (see
`guard_kct_integration_tasks.md`). Auto-selection has proven unreliable in-game
and is being retired in favour of a fully **player-managed** guard picker.

---

## 1. Why we are abandoning the automatic scan (context)

The automatic scan worked like this: at Save time, a generated script walked the
tree's candidate units top-down, classified each one by checking whether it is
infantry/archer (class override slot 533 + equipment: horse -> cavalry,
bow/crossbow -> archer, else infantry), and picked the first "eligible" unit for
each guard slot.

Two defects were found:

1. **Compiled scan bug (fixed but not enough).** `_emit_class_scan_ops`
   (`kct_scripts/guard_replacements.py`) called
   `script_kct_guard_cf_troop_eligible` but **never checked its result**: the
   first candidate always won. This is why the hall guard was always the
   strongest high-tier unit (F1 / crusader on preset 4). The gate
   `(eq, reg0, 1)` was added and verified in the compiled `scripts.txt`, but the
   player still saw cavalry guards after re-Saving.
2. **Runtime class detection is unreliable.** The eligibility predicate depends
   on `script_kct_cf_troop_has_horse` / `script_kct_cf_troop_has_bow_or_crossbow`,
   which scan the **real troop's inventory** (`troop_get_inventory_capacity` /
   `troop_get_inventory_slot`) at Save time. If that inventory does not hold the
   horse at the exact moment the apply runs, the predicate marks a cavalry unit
   as "eligible" and the gate lets it through. The horse detection has not
   proven trustworthy at runtime.

**Conclusion:** automatic class detection cannot be trusted for guard selection.
The write path is proven (the player's custom cavalry troop *does* appear in the
hall -> faction-slot writes reach enter_court), so the fix is to let the **player
choose** each guard unit explicitly. No detection, no scan.

---

## 2. Decisions locked with the user (2026-08-15)

1. **Fully player-managed:** the player picks every guard troop themselves.
2. **Scope — ALL guard-eligible slots:**
   - Town streets: `slot_faction_tier_2_troop`, `slot_faction_tier_3_troop`,
     `slot_faction_tier_4_troop`
   - Hall guard: `slot_faction_guard_troop`
   - Castle outer guard: `slot_faction_castle_guard_troop`
   - Prison guard: `slot_faction_prison_guard_troop`
3. **Streets are player-picked too** (not left on the old auto behaviour).
4. **Persistence:** the picks are saved **in the tree file** (WSE2 JSON) so that
   importing a tree restores its guard picks; they are also written to faction
   slots (which persist in the save).
5. Guards are **only changed by the picker** — the creator's Save button stops
   writing guard slots entirely (nothing auto-overwrites the player's choices).
6. If the player never uses the picker, guards stay native (enter_court already
   falls back to `trp_hired_blade` when the slot is <= 0).

---

## 3. Slot -> role table

| Role (picker label) | Faction slot constant | Key in tree file |
|---|---|---|
| Streets Tier 2 | `slot_faction_tier_2_troop` | `g_tier2` |
| Streets Tier 3 | `slot_faction_tier_3_troop` | `g_tier3` |
| Streets Tier 4 | `slot_faction_tier_4_troop` | `g_tier4` |
| Hall Guard | `slot_faction_guard_troop` | `g_guard` |
| Castle Guard (outside) | `slot_faction_castle_guard_troop` | `g_castle` |
| Prison Guard | `slot_faction_prison_guard_troop` | `g_prison` |

Each slot is written to **both** `fac_culture_player` and
`fac_player_supporters_faction` (the same pair the old apply used; enter_court
reads the player-fief slots from these).

---

## 4. Design

### 4.1 New presentation: `prsnt_kct_pick_guards`

- Opened from the creator screen via a new **"Guards"** button (placed next to
  the Save button).
- Depends on globals already set when entering the creator:
  - `$cstm_selected_tree` (0..3), `$cstm_selected_gender` (0/1) — set by the
    tree picker.
  - `$cstm_troops_begin` / `$cstm_troops_end` / `$cstm_num_tiers` — set by the
    creator load (`branch_display.py`); recomputed on the picker load via
    `script_kct_compute_tree_range` for safety.
- Load ops:
  - For each of the 6 roles: a label + a combo button overlay listing **every
    unit of the selected tree/gender** (display name taken from the troop's
    dummy, `cstm_slot_troop_dummy`, via `str_store_troop_name`).
  - Preselect each combo with the **current slot value**: read
    `faction_get_slot` from `fac_player_supporters_faction` for that role; if
    the value is inside `$cstm_troops_begin..end`, index = value - begin; else
    select 0.
  - Optional nicety: a troop preview mesh for the currently selected combo.
- Event ops (`ti_on_presentation_event_state_change`):
  - Combo change -> update the preview (and nothing else).
  - **Apply** -> `call_script script_kct_apply_guard_picks`; return to creator.
  - **Cancel / Exit** -> return to creator without changes.

### 4.2 New script: `script_kct_apply_guard_picks`

- No params; reads the 6 combos' current values (indices) from the presentation
  (via `overlay_get_val` on globals or direct index globals), converts each to a
  troop id = `$cstm_troops_begin + index`, and writes all 6 slots to
  `fac_culture_player` **and** `fac_player_supporters_faction`.
- Registers the 6 indices into globals (e.g. `$kct_pick_tier2`, `$kct_pick_tier3`,
  `$kct_pick_tier4`, `$kct_pick_guard`, `$kct_pick_castle`, `$kct_pick_prison`)
  so the export can read them even if the slot later changes.
- Result is immediate: applying and entering the hall shows the chosen unit.

### 4.3 Creator Save no longer touches guard slots

- Remove the `call_script "script_kct_apply_guard_replacements"` from the Save
  button handler (`branch_display.py:340`).
- Retire the auto-scan: drop `script_kct_guard_cf_troop_eligible` and
  `script_kct_apply_guard_replacements` from `guard_replacements.py` (and the
  generated candidates/write builders). Keep `script_kct_restore_native_guards`
  unchanged (it only heals native-kingdom slots; it never touches the player
  factions).
- The Save button keeps its recruitment wiring: tier_1 troop + center cultures.

### 4.4 Tree file round-trip (`tree_io.py`)

Export (`script_kct_export_tree_to_file`) — after the per-troop loop, add 6 keys
to `$kct_export_dict`:
- For each role: `faction_get_slot` the current troop from
  `fac_player_supporters_faction`; index = value - `$cstm_troops_begin`
  (clamped to `0..kct_count-1`); `dict_set_int` for the role's key.

Import (`script_kct_import_tree_from_file`) — after the tree is applied:
- For each role: `dict_get_int` (default 0), clamp, troop =
  `$cstm_troops_begin + index`; `faction_set_slot` on both player factions.

Storage note: indices (not troop ids) are stored because the import already
iterates the troop range with a running index, so an index maps directly and
survives re-imports into the same tree structure.

---

## 5. Files to touch

| File | Change |
|---|---|
| `modmerger/mods/kingdom_custom_troop_tree_creator/kct_presentations/pick_guards.py` | **New** — `prsnt_kct_pick_guards` presentation (load/run/event) + layout constants |
| `modmerger/mods/kingdom_custom_troop_tree_creator/kct_scripts/guard_replacements.py` | Remove auto-scan scripts (`kct_guard_cf_troop_eligible`, `kct_apply_guard_replacements`); keep `kct_restore_native_guards` |
| `modmerger/mods/kingdom_custom_troop_tree_creator/kct_scripts/tree_io.py` | Export: add `g_*` keys; Import: read `g_*` and write slots |
| `modmerger/mods/kingdom_custom_troop_tree_creator/kct_presentations/branch_display.py` | Add "Guards" button + event branch; remove the old apply call from Save |
| Mod registration (presentations/scripts entry point) | Register the new presentation + script |

Note: `script_kct_apply_guard_picks` may live in `guard_replacements.py` (renamed
purpose) or a new `kct_scripts/guard_picks.py`; decide at implementation.

---

## 6. Implementation steps (ordered)

1. Add `script_kct_apply_guard_picks` (new script) + `g_*` storage globals.
2. Build `prsnt_kct_pick_guards` presentation (combos, preselection, preview).
3. Wire the "Guards" button into `branch_display.py` (creator) and remove the
   old `apply_guard_replacements` call from the Save handler.
4. Remove the auto-scan scripts from `guard_replacements.py`.
5. Extend `tree_io.py` export/import with the `g_*` keys.
6. Register the new presentation + script.
7. Compile: `python compiler\compile.py tag` -> COMPILATION SUCCESSFUL.

---

## 7. Verification (in-game, after implementation)

1. Recompile; enter the creator -> **Guards** button opens the picker showing the
   current tree's units with the current slot values preselected.
2. Pick a foot unit for Hall Guard, Apply, enter your town/castle hall -> the
   chosen unit appears.
3. Pick castle outer + prison guards, walk the castle outside / enter prison ->
   chosen units appear.
4. Streets Tier 2/3/4 -> walking the town streets shows the chosen units.
5. Export the tree, re-import it in a new test -> the guard picks come back
   (check the slots).
6. Save & reload the game -> guard slots persist (no re-pick needed).
7. NEW game without touching the picker -> native guards (no custom writes).

---

## 8. Notes / edge cases

- The picker lists every unit of the tree for every role (full control); default
  selection is the current slot value, falling back to the first unit.
- If the slot currently holds a troop from a *different* tree/gender (stale),
  preselection falls back to 0; the player re-picks.
- `script_kct_restore_native_guards` must stay as-is: it only restores
  `fac_kingdom_1..fac_kingdoms_end`, so player-faction picks survive loads.
- The tree file is a snapshot of tree + guard picks; exporting after picking
  captures the picks (reads from the slots, which the picker already wrote).
- Khergit culture native guard is mounted (`trp_khergit_horseman`); irrelevant
  here because the picker is fully player-chosen — the player picks what they
  want for the hall.

## 9. Open questions

- None blocking. Optional: preview mesh of the selected unit in the picker
  (reuse store preview helpers if available; otherwise name + level only).
