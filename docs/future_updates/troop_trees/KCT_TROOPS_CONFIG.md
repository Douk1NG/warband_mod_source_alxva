# Kingdom Custom Troop Tree Creator — Step 3: "Troops Config" (Store Parameter Polish)

Handoff contract for the **next agent session**. The store presentation
`prsnt_kct_customise_troop` is now fully ported (Step 2, `KCT_MODIFY_EACH_TROOP.md`) and
compiles. This step makes that presentation work end-to-end and adjusts ALL of its
parameters — money (gold), XP/level, skill points, attribute points, proficiency points,
equipment — per the product spec `become_king_troop_config.md` and the new-system spec
`CSTM_TROOP_TREES_SPEC.md`.

Predecessor contracts (assume DONE, build on them):
- `KINGDOM_CUSTOM_TROOP_TREE_CREATOR.md` — M1 picker + bridge.
- `KCT_MODIFY_EACH_TROOP.md` — self-contained port of the store + scripts + node-click wiring.

---

## 1. What is already DONE (do not redo)

- **Store `prsnt_kct_customise_troop`** lives in
  `..._presentations.py:831-1553` (`kct_customise_core` at 831, node-click wiring +
  store registration in `modmerge`). It is a self-contained copy of
  `prsnt_cstm_customise_troop`; Exit returns to `prsnt_cstm_create_troop_tree`.
- **All `script_kct_*` ports** in `..._scripts.py` (attribute/skill/proficiency math,
  item arrays, price/imod helpers, tree-copy helpers, UI helpers, `equipment_funds_available`).
- **Game-start ops** (`..._scripts.py:2454-2487`): preset-4 dummy slot links, item-array
  build (`script_kct_setup_item_arrays`), `trp_cstm_proficiency_requirements` table,
  `trp_cstm_inventory_values` funds table, per-array item-type slots, `$cstm_items_array`
  init.
- **Store layout constants** `KCT_*` (inventory grid, store grid, stats grid, name,
  buttons) at `..._presentations.py:109-159`.
- **`ACTIVE_FIGHTING_SKILLS`** at `..._presentations.py:106-107` (module skills filtered
  to non-inactive strength/agility skills).
- **Gold unified at 1.5×** (§2b DONE): kct game-start writes
  `int(round(equipment_funds_available(i) * 1.5))` into `trp_cstm_inventory_values`, so
  boot-time and load-restore agree (matches the `custom_troops` save-fix). Item cost
  already uses `CSTM_IMOD_COST_DIVISOR` via `kct_item_get_price_with_modifier`.
- **Proficiency auto-allocating selectors** (§2c DONE): the 7 per-WPT number boxes are
  replaced by a **Role preset** combo + **Primary weapon** combo. New script
  `kct_proficiency_apply_preset(dummy, role, weapon)` reallocates on Save only
  (`$cstm_proficiency_changed` flag, cleared on Save/Reset).
- **Bug fixes (in-game verification iteration)**:
  1. Preset-4 real↔dummy slot links are re-applied in the create viewer
     (`_build_preset4_viewer_ops`, `..._presentations.py:628-629`), so saves created
     before the kct game-start linkage no longer resolve `:dummy` to `trp_player`
     (which loaded the player's name, items and stats into the store). NOTE: the first
     attempt was a silent no-op — the two ops were bare tuples, never `ops.append`ed,
     so they never compiled in. They are now real ops and verified in the exported
     `presentations.txt` (`troop_set_slot real 500 dummy` / `dummy 501 real`). The
     `game_start` ops remain as a redundant second source of the link.
  2. All proficiency-point displays removed (user decision): the 7 per-WPT readout rows
     and the "Proficiency points: X" total row are gone. The store's proficiency area
     shows only the two selector combos; the points summary is one row (Attribute
     points + Skill points).
  3. "Manual" role preset removed and default = Balanced (user decision): the role combo
     is `Balanced, Archer, Infantry, Cavalry, Gunman, Spearman` (combo index 0 =
     Balanced, mapped to preset key 1 via `:role = selected + 1` in the save flow).
     `$cstm_proficiency_changed` defaults to 1 on load, so a fresh Save applies the
     Balanced preset even if the player never touches the combos.
- Verified: no `script_cstm_*` / `script_gpu_*` / `script_prsnt_*` remain in the kct mod;
  compile = `python compiler\compile.py tag` → "COMPILATION SUCCESSFUL" (verified).

Active mods (must stay, `modmerger_options.py`): `custom_troops` +
`kingdom_custom_troop_tree_creator` (+ stock list).

---

## 2. The task (user-approved approach: "make the new presentation work and adjust all parameters in it")

Work ONLY in `prsnt_kct_customise_troop` and its kct scripts. Do not touch
`custom_troops` sources (REFERENCE ONLY). User scope words: "focus on troops config, like,
money, xp, skills points, proficiency, in general troops creation".

Three target areas, each with a clear deliverable:

### 2a. Make the store work end-to-end (in-game verify + fix)

The port compiles but has not been exercised in-game. Verify and fix the full flow:

1. Camp → "Test troop tree picker" → pick tree + gender → "Choose" → click a node
   portrait → store opens on that troop's dummy.
2. **Name**: type singular → plural auto-suffixed with `s`; save persists.
3. **Attributes**: 4 number boxes (strength/agility/intelligence/charisma) with
   min/max from `min_from_points` / `min_from_tree` / points-available; +/- steps the
   dummy; Save persists.
4. **Skills**: `ACTIVE_FIGHTING_SKILLS` grid with per-skill number boxes bounded by
   points-available and the attribute cap (`attr_level/3 + 1`).
5. **Proficiencies**: **Role preset** + **Primary weapon** selectors (per §2c); no
   proficiency-point numbers are displayed. Picking either selector enables Save; Save
   auto-allocates ("all you can" to primary, then role-weighted remainder, weapon-master
   capped except at the leaf tier).
6. **Equipment**: item-type combo + imod combo + page selector; click item to buy into
   dummy inventory (requirement-checked, funds-decremented), right-click to remove;
   "Remaining funds:" line turns red when negative.
7. **Save / Reset / Exit** buttons and ESC; Save propagates stats/inventory to upgrade
   children and re-equips; Reset restores the dummy from the real troop; Exit returns to
   the creation viewer.
8. Recompile after any change and confirm "COMPILATION SUCCESSFUL".

Report each verified item; if any op sequence is visibly wrong (e.g. wrong overlay,
missing bounds, funds not decrementing), fix it with the smallest change.

**Status**: code implementation for §2a (flow), §2b (gold) and §2c (proficiency selectors)
is COMPLETE and compiles. In-game verification surfaced three issues, all fixed: the store
loaded the player's character on stale saves (root cause: the preset-4 slot-link self-heal
was a bare-tuple no-op and never compiled in — fixed and verified in the export, §1 bug 1);
the proficiency readout rows still showed (removed, see §2c); and "Manual" was dropped with
Balanced as the default (see §2c). The remaining §2a work is the rest of the in-game
verification checklist above — no further code changes are expected unless a check fails.

### 2b. Money — unify gold at 1.5× (spec §5)

`CSTM_TROOP_TREES_SPEC.md §5`:
- `equipment_funds_available(level) = round(480 * e^(0.13 * level) - 225, -1)` (kept),
  table stored 0-63 via `trp_cstm_inventory_values`.
- **Unified at 1.5× everywhere** — boot-time table AND load-restore must agree (fixes
  the current mismatch where boot uses 1× and the save-fix overwrites with 1.5×).
- Item cost = item value + (modifier cost ÷ `CSTM_IMOD_COST_DIVISOR`).
- Budgets at 1.5×: level 2 ≈ 0.4k · 10 ≈ 1.5k · 18 ≈ 5.0k · 26 ≈ 13.9k · 34 ≈ 39.7k ·
  40 ≈ 130k.
- Known balance issue (2nd iteration): low tiers starved, high tiers flush — rebalance
  deferred, not dropped.

Current state: DONE. kct game-start (`..._scripts.py`, `new_start_operations`) writes
`equipment_funds_available(i) * 1.5` (rounded via `int(round(..., 0))`) for i in 0..63,
matching the save-fix the `custom_troops` mod applies at load — boot-time and restore now
agree. Item cost already uses the divisor — verified unchanged.

### 2c. Proficiency — replace free-form boxes with auto-allocating selectors (become_king spec)

`become_king_troop_config.md` ("Asignación de valores"): the value-assignment
presentation is built; **"Solo tiene un cambio: pericia de arma — en vez de libertad,
unos selectores que permiten hacerlo automáticamente"**. I.e. weapon proficiency should
NOT be free per-point number boxes; instead **selectors that allocate proficiency points
automatically**. Pending review: the weapon-master rule and how it affects this
("Pendiente a revisar: la regla de dominio de armas (weapon master) y cómo afecta esto").

Deliverable: DONE. The per-weapon number boxes are replaced by a selector-based
auto-allocation UI. Final design (user-approved, Spanish discussion):

- **Two selectors** (both combos, sized per the established 750×750 pattern):
  - **Role preset** (`$cstm_proficiency_role_selector` → `$cstm_proficiency_role_selected`):
    `Balanced`, `Archer`, `Infantry`, `Cavalry`, `Gunman`, `Spearman` (no "Manual").
    Defines
    the **secondary** distribution weights (`KCT_PROF_ROLE_WEIGHTS`, 7-WPT order = one
    handed, two handed, polearm, archery, crossbow, throwing, firearm; e.g. Archer
    `[1,1,1,4,3,2,1]`, Infantry `[3,3,3,1,1,2,1]`, Cavalry `[3,1,3,2,2,1,1]`, Gunman
    `[1,1,1,2,3,1,4]`, Spearman `[2,1,5,1,1,1,1]`, Balanced `[2,2,2,2,2,2,2]`).
  - **Primary weapon** (`$cstm_proficiency_weapon_selector` → `$cstm_proficiency_weapon_selected`):
    `Auto`, `One Handed`, `Two Handed`, `Polearm`, `Archery`, `Crossbow`, `Throwing`,
    `Firearm`. The **primary** target — "all you can to 1st, remaining to 2nd". `Auto` uses
    the role's natural primary (`KCT_PROF_ROLE_PRIMARY`: Archer→archery, Infantry→one
    handed, Cavalry/Spearman→polearm, Gunman→firearm, Balanced→none).
- **Applied on Save click only** — never live, never on open. Default role = `Balanced`
  (combo index 0); the save flow maps it to preset key 1 via `:role = selected + 1`.
  `$cstm_proficiency_changed` is set to 1 on every load (so a fresh Save applies the
  Balanced preset even with no interaction) and cleared on Save and Reset.
- **Weapon-master cap** = `40*wm + 60` per WPT (level), EXCEPT at the last tier (leaf
  troop with no upgrade path) where restrictions are ignored and the whole pool goes in.
- **Pool** = the entire calculated pool (`kct_get_proficiency_points` minus the points
  held at the per-WPT floors). Floors per WPT = `max(40, kct_troop_get_proficiency_min
  _from_tree)` preserve the bottom-up invariant. Allocation converts points↔levels via
  `trp_cstm_proficiency_requirements`.
- **New script** `kct_proficiency_apply_preset(dummy, role, weapon)` (`..._scripts.py:2479`),
  called in the Save flow before `script_kct_replace_custom_troop_with_dummy`.
- The "Proficiency points: {reg0}" total row is **removed** (bug-fix iteration, user
  decision: no proficiency numbers are shown anywhere). The points summary is now a
  single row showing Attribute points + Skill points only.

This is the one explicitly user-requested behaviour change in the store. Money/XP/skills
are verification + spec alignment; proficiency is a real UI change.

---

## 3. Store anatomy (line map, `..._presentations.py`)

| Block | Lines | Notes |
|---|---|---|
| `ACTIVE_FIGHTING_SKILLS` | 106-107 | non-inactive, strength/agility skills |
| Layout constants `KCT_*` | 109-159 | inventory/store/stats/name/buttons geometry |
| `kct_customise_core` record | 834-1454 | the presentation tuple |
| load trigger | 837-1158 | overlay reset, funds, inventory copy, grids, selectors, buttons |
| item-type + imod combos | 905-937 | `kct_cf_cci_imod_appropriate_for_item`-filtered |
| store grid (buy) | 962-984 | `kct_get_item_from_array`, page-sliced |
| funds line | 988-1002 | red when negative |
| stats container | 1004-1092 | attributes (1017-1065), role/weapon preset selectors (1071-1089), `$cstm_proficiency_changed=1` default (1067); no proficiency readout |
| name boxes | 1097-1106 | singular + plural |
| Save/Reset/Exit | 1124-1157 | Save only when changes made + funds >= 0 |
| mouse enter/leave | 1161-1209 | item details |
| mouse press | 1211-1264 | left buy, right remove |
| run (ESC) | 1268-1273 | `presentation_set_duration 0` |
| event state change | 1277-1450 | name, selectors, attribute/skill boxes, role/weapon presets, save/reset/exit |
| save flow | 1354-1406 | marks equipment-modified, sets class, applies proficiency preset (1384, role = selected+1), copies dummy→real, tree propagation |
| reset flow | 1417-1422 | restore from real troop |
| exit flow | 1431-1437 | resets modifier/page, `start_presentation prsnt_cstm_create_troop_tree` |
| modmerge additions | 1460-1570 | item-type combo items + role/weapon preset combo items (1468-1478) + skill grid + points rows (1549-1558) |

Point-math scripts (`..._scripts.py`, all ported as `kct_*`): attributes 346-606,
skills 664-972, proficiencies 974-1223, prices/items 1625-2078, imod eligibility
1665-1829, inventory value 1878-2147, grid/combo/box helpers 2187-2270,
`kct_item_type_get_cost_modifier` 2270-2400, eligibility 2401-2434, `kct_get_items_array`
2435-2452.

---

## 4. Specs to follow

- `become_king_troop_config.md` — product requirements (Spanish): tree picker done,
  tree presentation has import/export buttons (top-right) — note: import/export is a
  SEPARATE future step, do NOT build it here; template folder = WSE managed dir
  (`Documents\Mount&Blade Warband\WSE\<module>\`), NOT the savegame folder; auto-save on
  exit is pending; the one store change is the proficiency selector (§2c).
- `CSTM_TROOP_TREES_SPEC.md` — new-system spec: §5 gold (1.5×, budgets, cost formula),
  §6 proficiency points ("TBD — define later"), §7 restrictions (bottom-up editing,
  non-decreasing invariant), §10 persistence redesign (source of truth = troop slots;
  deterministic rebuild on load; remove `fix_operations`/`$g_cstm_save_fix_applied`
  hacks) — persistence is a SEPARATE future step, do NOT rework persistence here beyond
  what the store already does, but DO read §10 so the proficiency/gold changes don't
  fight the persistence design.
- Engine constraints (spec §2): no `troop_set_upgrade_troop`, no `troop_set_level` —
  tree shape and troop level are compile-time; max troop level 63 (funds table capped at
  `xrange(64)`); WSE file I/O exists (used by the future import/export step).

---

## 5. Rules & constraints (hard)

- `custom_troops/` sources and `mods/shared/` are REFERENCE ONLY. Never edit.
- Do NOT edit `modmerger_options.py`. Do NOT touch `cstm`/`custom_troops` mods' exports.
- Port stays self-contained: no `call_script "script_cstm_*"` / `script_gpu_*` /
  `script_prsnt_*` may appear in the kct mod.
- Reuse shared IDs (`str_cstm_*`, `trp_cstm_overlay_*`, `trp_cstm_inventory_values`,
  `trp_cstm_proficiency_requirements`, array troops) — do NOT re-declare.
- Only `str_s0` is accepted as a string-register `call_script` argument; `str_store_string
  s0` immediately before the call.
- `set_fixed_point_multiplier 1000`; y-up screen coords (0 = bottom).
- Combo/number-box/container scripts return the overlay id in `reg1`.
- No debug `display_message` leftovers; no new comments unless required.
- No gratuitous overlay resizing (don't add `overlay_set_size` to combos beyond the
  existing pattern).
- After EVERY code change: `python compiler\compile.py tag` from repo root → must say
  "COMPILATION SUCCESSFUL".

---

## 6. Files

- `modmerger/mods/kingdom_custom_troop_tree_creator/kingdom_custom_troop_tree_creator_presentations.py` — the store (WORK FILE)
- `modmerger/mods/kingdom_custom_troop_tree_creator/kingdom_custom_troop_tree_creator_scripts.py` — kct scripts + game-start ops (WORK FILE)
- `modmerger/mods/custom_troops/custom_troops_presentations.py` — REFERENCE ONLY
- `modmerger/mods/custom_troops/custom_troops_scripts.py` — REFERENCE ONLY
- `modmerger/mods/custom_troops/custom_troops_constants.py` — REFERENCE ONLY (`equipment_funds_available`, `CSTM_IMOD_COST_DIVISOR`, slots)
- `modmerger/mods/custom_troops/custom_troops_simple_triggers.py` — REFERENCE ONLY (see §10 for the persistence design it implements today)
- `modmerger/mods/shared/cstm_item_helpers/item_types.py` — `cstm_item_type_strings` source
- `docs/future_updates/troop_trees/become_king_troop_config.md` — product spec
- `docs/future_updates/troop_trees/CSTM_TROOP_TREES_SPEC.md` — new-system spec

## 7. Build / test

- Compile: `python compiler\compile.py tag` from repo root → "COMPILATION SUCCESSFUL".
- Export target: `C:\Program Files (x86)\Steam\steamapps\common\MountBlade Warband\Modules\Dickplomacy Reloaded\`
- In-game flow (§2a). Default `python` is Python 2.7.18.
- After editing code, ALWAYS compile and confirm before stopping.
