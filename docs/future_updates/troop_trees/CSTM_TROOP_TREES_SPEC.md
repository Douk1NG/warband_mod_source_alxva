# CSTM Custom Troop Trees — New System Spec

Specification for the rewrite of the custom troop tree system in the CSTM mod
(`modmerger/mods/custom_troops/`). This is a clean rewrite,
not a patch of the current (buggy) approach, and must be portable so a third-party
"troop creator" can drop it into their own mod without bugs.

## 1. Overview & Goals

- Define the entire mod behavior up front: **branches, levels, gold, proficiency
  points, restrictions, presets + export/import**.
- Replace the current tree config + persistence with a data-driven, pre-generated design.
- Fix the customisation-loss-on-load bug with a clean, engine-correct persistence model.
- Keep the existing UI (store interface, grids, selectors) — it is correct.
- Everything below builds on the already-verified CSTM architecture; slot allocation,
  item-array scheme, and merge wiring stay as they are.

## 2. Engine Constraints (verified)

These cannot be worked around and shape the whole design:

| Constraint | Consequence |
|---|---|
| Max **2 upgrade choices per troop** (`upgrade`/`upgrade2`, troop fields `[14]`/`[15]`) | 3-way splits must be expressed as binary chains (e.g. `Recruit → (Infantry, Skirmisher)`, then `Skirmisher → (Cavalry, Archer)`). |
| No `troop_set_upgrade_troop`, no `troop_set_level` | Upgrade links and troop level are baked at compile time. Tree shape must be decided and generated at compile time — **runtime tree-drawing is impossible**. |
| No `export_import_export_char` / `export_import_import_char` ops | Native character export/import is engine-side via the character screen (C → Statistics → Export/Import → `CharExport.txt`). Transfers stats, skills, proficiencies, gold, XP, name — **not equipment/inventory**. |
| **WSE file I/O exists**: `array_save_file` (5003), `array_load_file` (5004), `array_delete_file` (5005), `dict_save` (3204), `dict_load_file` (3202), `dict_save_json` (3218), `dict_load_file_json` (3217) | Presets round-trip as **real txt files** in the WSE managed directory — no string-register codec required. |
| Equipment-funds table is capped at `xrange(64)` (`custom_troops_simple_triggers.py:33`, `custom_troops_scripts.py:65`) | Max troop level = 63. Level tables below must never exceed it. |
| Advanced string ops exist: `str_store_join` (4222), `str_split` (4213), `str_to_num` (4211), `str_store_string` (2320), `str_store_string_reg` (2321) | Available if an in-memory encoding is ever needed: `str_store_string` copies a string into a register, `str_store_string_reg` copies register→register, `str_to_num` parses a register's digits into a value, `str_split` splits a string by a delimiter across registers, `str_store_join` re-joins them. |

## 3. Branches — Four Presets

- Player picks **one** preset at kingdom creation (`mnu_cstm_choose_troop_tree`),
  once per campaign.
- **Four presets** this release. All four presets (1–4) are **functionally identical**
  in every gameplay aspect: gold budgets (§5), equipment filtering, modifier systems,
  proficiency restrictions, persistence design, and guard/recruitment behavior.
  The only difference is the **tree structure** (shape of branches and tiers), as
  detailed below. Presets 1–3 retain their original shapes; preset 4 introduces a
  new binary-fork structure with quality tiers and superunits.
- Dynamic branch builder = future option, beyond the four presets.

| Preset | Status | Shape (as shipped) |
|---|---|---|
| **1** | unchanged | 1 Branch, 7 Tiers (levels 4–34) |
| **2** | unchanged | 2 Branches, 6 Tiers (levels 4–31) |
| **3** | unchanged | 3 Branches, 5 Tiers (levels 4–28) |
| **4 (new)** | built now | `Recruit → (Infantry, Skirmisher)`; `Skirmisher → (Cavalry, Archer)`; 2 sub-branches each × 3 quality tiers; A-lines extend to `****` superunit |

**Sub-branch naming — no player concepts.** The game/code does not know archetypes
(e.g. "Shieldbreaker", "Line", "Heavy Cavalry"). Sub-branches are simply
**Unit A / Unit B**; strength is measured by the quality tier `*`.


**Superunits** (`****`):
- Only in preset 4: one per **Unit A** sub-branch (Infantry A, Cavalry A, Archer A).
- Not shared between sub-branches; max 3 total. **Unit B** lines stop at `***`.

## 4. Levels

Uniform role-based ladder for preset 4 (no power tradeoff between presets):

| Node | Level |
|---|---|
| Recruit | 2 |
| Primary (incl. Skirmisher fork troop) | 10 |
| Sub `*` | 18 |
| Sub `**` | 26 |
| Sub `***` | 34 |
| Sub `****` superunit | 40 |

`63` remains a hard safety ceiling only.

## 5. Gold

- **Per-tree equipment budget** (replaces the old global `kct_funds_tier` mod option,
  which was removed). Each of the four trees carries its own budget in one of four
  slots `cstm_slot_tree_budget_begin + tree` (521–524) on the **shared prefix troop**
  (`cstm_troop_tree_prefix` = `trp_cstm_custom_troops_end`), so switching trees keeps
  each one's budget. Values:
  - **0 Balanced / 1 Boosted / 2 Cheater** — the three explicit level tables, stored
    contiguously in `trp_cstm_inventory_values` (64 entries each — slot =
    `level + tier * 64`). Written at game start and re-written by the save-fix trigger
    so boot and load agree. **All four presets (1–4) share the same tables** — only
    the per-tree selection differs.
  - **3 Auto** — the funds equal the troop's **current gear cost** at the moment the
    store opens. This is the **import default** (templates without `@kct_budget`,
    i.e. exported before this feature, adapt to whatever budget model they were
    authored under): the store opens editable with remaining exactly 0 and no free
    denars.
- Band table `EQUIPMENT_FUNDS_BANDS`: levels 1–3, 4–6, 7–9, 10–12, 13–15, 16–18,
  19–21, 22–24, 25–27, 28–30, 31–34, 35–40. Levels 0 and 41–63 clamp to the
  first / last band.
- Boosted = Balanced × 1.5; Cheater = Balanced × 3, **capped at 60000** for 35–40.
- Key budgets (Balanced): L3 = 110 · L6 = 472 · L9 = 970 · L12 = 1807 ·
  L15 = 2116 · L18 = 3010 · L21 = 3942 · L24 = 7613 · L27 = 9668 ·
  L30 = 11702 · L34 = 17887 · L40 = 20000 (Boosted ×1.5, Cheater ×3, cap 60k).
- The budget is chosen with the **"Budget:" dropdown in the creator**
  (`prsnt_cstm_create_troop_tree`, below the prefix input; the "Budget:" prefix is
  baked into every option, so there is no separate label). **Balanced is the default**
  for trees that were never configured (slot 0); **Auto** is the default for
  imported trees (re-import once to apply it to already-imported templates).
- The store computes `$cstm_total_funds` **only on the session's fresh entry**
  (captured from `$g_kct_recalc_baseline` before it is consumed). Internal reloads
  (add/remove item, class, stat boxes, Reset) never re-derive the budget from the
  evolving gear, so removing equipment frees funds (remaining goes positive and is
  spendable) and adding beyond the budget shows negative (red) until balanced — the
  Save button requires `remaining >= 0`.
- **Snapshot floor**: for the explicit tiers, funds = `max(table[level], gear_cost)`
  — a tree authored on a higher budget (or after the budget is lowered below the
  gear) costs more than the tier allows and would otherwise open negative; the floor
  covers the gap exactly so remaining = 0 and a raised budget never hands out free
  denars.
- Item cost = item value + (modifier cost ÷ `CSTM_IMOD_COST_DIVISOR`).
- **Known balance issue (2nd iteration):** low tiers end up starved of gold while
  high tiers have gold to throw. Rebalance is deferred, not dropped.

## 6. Proficiency Points

- **TBD — define later.** All options are on the table (interactive per-WPT boxes,
  role/fallback selectors, internal auto-distribution, etc.). Not finalised in this
  revision; decided one-by-one later.

## 7. Restrictions

- **Bottom-up editing**: the editor walks `Recruit → … → ****`; a troop's customise
  entry unlocks only after its upgrade parent(s) are configured. You cannot customise
  the superunit before the recruit.
- **Non-decreasing invariant** along the upgrade path (no troop weaker than its parent)
  for attributes, skills, and proficiencies — enforced via `min_from_tree` /
  `max_from_upgrade` scripts.
- Equipment gated by funds + native item difficulty (stat/skill requirements).

## 8. Presets

- **Preset = a fully pre-configured tree**: branch type, unit progression tree,
  equipment, skills — everything about the tree.
- **The user authors the preset for the new tree (preset 4).** Presets for the
  existing trees (1–3) may be authored too — the assistant can create those
  (acting as another player).
- **Mechanism:** a preset is a structure that can be **exported to a txt file** and
  **imported from a txt file** (WSE file I/O, see §11). Export shares a tree;
  import rebuilds it.

## 9. UI Flow

1. Kingdom creation → pick one of the four presets (`mnu_cstm_choose_troop_tree`) → pick skin.
2. View tree (`prsnt_cstm_view_custom_troop_tree`).
3. **Troop tree editor**: branch select on top, branch-structure image behind,
   **Continue** button at bottom. Branches presented low → high (per §7).
4. Customise troop (`prsnt_cstm_customise_troop`, store interface): attributes,
   skills, proficiencies, name, equipment.
5. Export / import a preset to / from a txt file.

## 10. Persistence Design

- **Source of truth = the custom troop's own slots.** Troop slots persist for all
  troops across save/load (engine behaviour, not a quirk to work around). Every
  customisation (attributes, skills, proficiencies, equipment as item+modifier
  lists, name) is stored in the custom troop's own slots.
- **Deterministic rebuild on load** (simple trigger, interval 0): re-apply the
  slot data to the troop after every load. No marker item, no "did inventories
  reset?" detection, no hero-dummy copy/restore.
- Remove the current `fix_operations` / `$g_cstm_save_fix_applied_2` one-shot hacks
  (`custom_troops_simple_triggers.py`) and `trp_cstm_load_check`.
- Exact slot layout and name handling are confirmed one-by-one during implementation.

## 11. Export / Import — Preset Files

- Preset files use **WSE file I/O**: pack the whole tree structure (branch type,
  progression tree, per-troop name/attributes/skills/proficiencies/equipment-with-
  modifiers) into an array or dict and `array_save_file` / `dict_save` it as a
  txt file in the WSE managed directory.
- The file also carries the tree's equipment budget as `@kct_budget` (0–3). Import
  defaults to **Auto (3)** when the key is absent, so templates exported before this
  feature adapt to their gear cost instead of a fixed level table. The key is
  additive — `kct_version` stays 1.
- Import: `array_load_file` / `dict_load_file` → rebuild the tree.
- This is the only mechanism that round-trips equipment, and it is a real file,
  not a copy-pasted code string.

## 12. Constants, Slots & Data Structures

- Keep `next_troop_slot()` allocator and `NEW_TROOP_SLOTS_BEGIN = 500` /
  `NEW_PARTY_SLOTS_BEGIN = 500` (`custom_troops_constants.py`).
- Keep troop-as-container item arrays (`cstm_items_arrays_begin`/`_end`,
  `cstm_slot_array_*`) and overlay troops.
- Shared helper module `shared/cstm_item_helpers/` keeps its name (it was not
  renamed together with the mod folder).
- Extend `CustomTroopTree` (`custom_troops_troop_trees.py`) with:
  - preset 4's shape data (levels ladder, fork wiring)
  - generated id/text helpers (current `get_custom_troop*`/`add_to_troop_list_with_skin`
    remain, driven by the new shape data).

## 13. Acceptance Criteria

1. `python compiler\compile.py tag` from repo root → "COMPILATION SUCCESSFUL".
2. All four presets in §3 appear in `mnu_cstm_choose_troop_tree`; presets 1–3 unchanged.
3. Superunit (`****`) reachable only in preset 4's Unit A lines, at level 40.
4. Bottom-up editing enforced; no troop weaker than its upgrade parent.
5. Preset export → txt file → import round-trips the whole tree (branch type,
   progression, per-troop name/stats/skills/proficiencies/equipment with modifiers).
6. Customisation persists across save → load without marker item or dummy restore.
7. Gold budgets are **per-tree** (Balanced/Boosted/Cheater tables, cap 60k, plus
   Auto = gear cost) chosen via the creator's Budget dropdown; the store freezes
   funds at session entry (removing gear frees budget, adding over it blocks Save);
   boot-time + load-restore tables agree.
8. No save-game regressions from changed entity ordering.
