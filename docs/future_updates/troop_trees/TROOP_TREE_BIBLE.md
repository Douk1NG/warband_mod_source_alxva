# KCT Troop-Tree System — Project Bible

This file is the **source of truth** for the Kingdom Custom Troop Tree (KCT) mod.
Always load it at the start of every session and update it whenever requirements,
research or status change. It survives context resets / compact commands.

---

## The Golden Rule (workflow)

- **No implementation changes** to any open problem until BOTH are true:
  1. research for that problem is declared **done** by the agent, and
  2. the user says the magic words: **"we can start now"**.
- Only then are changes made for that problem.
- When in doubt: **ask**. Never guess, never assume.
- Research is logged in the "Research notes" section of this file as it happens.

---

## The 3 open problems

### Problem 1 — Custom Troop Funds
- Idea: **Cheat menu → Mod Options → Custom Troop Funds** selector with 3 tiers:
  - **Balanced** — a fair funds value, to be determined by research.
  - **Boost** — based on the balanced value, give more gold without going crazy about it.
  - **Cheater** — unlimited funds.
- Affects the equipment-funds budget of the KCT store (the "Remaining funds: X denars" mechanic).

### Problem 2 — Attribute / Skill Tooltips + Layout
- When hovering (in the KCT customise presentation) over any **skill label** or the
  **STR / AGI / INT** labels, show a brief, clear tooltip explaining what it does
  (like the game's item tooltips). Examples:
  - STR gives more health (and more melee damage).
  - AGI increases movement speed and gives weapon points.
  - "Ironflesh — what does this actually do?" (user forgot; tooltips must explain it).
- Research task: identify the game's attribute/skill concepts, understand them, and
  apply them to tooltip text for every shown stat.
- **Layout change:** remove the **Charisma** box (char is pointless; we need space).
  Move the boxes so **STR[BOX] AGI[BOX] INT[BOX]** all sit on the **same horizontal
  line**.
- In addition, beside the level, show the troop's **current health** and **current
  agility** values.
- If positioning is difficult, the user will help — but the agent must point at the
  exact code to modify.

### Problem 3 — Proficiency Points System (layout redesign)
- The two selectors (Role / Weapon presets) are the right approach, but lack
  information — "you just pray the auto-distribution works and forget".
- New design: show **all proficiency values again but as read-only labels**, not
  boxes, e.g. **`1H Weapon : X`** for each.
- The proficiency selectors sit **on top** of these labels.
- New vertical order for the stats section:
  1. **Attributes** (single row / column)
  2. **Skill points**
  3. **Proficiency selectors, and behind/below them the read-only labels**
     (`1H Weapon : X` ... and so on).

---

## Research notes (in progress)

### Problem 1 — funds implementation + mod-options infra (RESEARCHED)
- **Mod Options infra:** presentation `prsnt_mod_option` (`mods/xgm_mod_options/
  xgm_mod_options_presentations.py`) is launched from the **camp menu option "Main
  Settings"** (`source/game_menus/mnu_dplmc_preferences.py:19`, option id
  `camp_mod_opition`) and from `mnu_startgame_mod_options.py:19` ("Change Settings").
  It is NOT currently in the cheat menu — user's "cheat menu → mod options" wording
  probably means this; confirm when starting.
- **Option list:** `mods/xgm_mod_options/xgm_mod_options.py` `mod_options` list.
  Tuple format: `("id", type, params, "Label:", flags, "desc", flags,
  [init block → must put value in reg1], [update block → value arrives in reg1])`.
  Types in `xgm_mod_options_header.py` (`xgm_ov_combolabel`, `xgm_ov_checkbox`,
  `xgm_ov_numberbox`, `xgm_ov_line`...). A 3-tier funds selector is exactly the
  `xgm_ov_combolabel` pattern used by e.g. `dplmc_ai_changes` (line 291).
- **IMPORTANT:** the auto-collation of `{modname}_mod_options.py` files is **commented
  out** in `xgm_mod_options.py:504-542` — a new option must be appended **directly to
  the `mod_options` list** (do NOT rely on a separate `{mod}_mod_options.py` file).
- **Funds flow:** `$cstm_total_funds` read from `trp_cstm_inventory_values` slot
  `:troop_level` (`..._presentations.py:903`). "Remaining funds: X denars" at
  `:1033-1042`; Save button gated on `remaining_funds >= 0` at `:1160`.
- **Funds table is a SHARED resource filled in 3 places with the SAME 1.5x formula**
  (`equipment_funds_available(i) * 1.5` for i in 0..63):
  1. base `custom_troops_scripts.py:67` (game start),
  2. base save-fix trigger `custom_troops_simple_triggers.py:33-36` (guarded by
     `$g_cstm_save_fix_applied`), and
  3. KCT start ops `kingdom_custom_troop_tree_creator_scripts.py:2740-2743`.
  `equipment_funds_available` = `round(480 * exp(level*0.13) - 225, -1)`
  (`custom_troops_constants.py:13`).
- **Tier design hook (cleanest):** scale at the KCT read point only —
  `$cstm_total_funds = table[level] * tier_multiplier` (global set by the mod option).
  This leaves the base custom_troops store (presets 1-3) untouched. Do NOT rewrite the
  shared table, or presets 1-3 change too. Cheater tier = multiply by a huge number or
  bypass the `remaining_funds >= 0` gate at `:1160`.

### Problem 2 — tooltip + layout research (RESEARCHED)
- **Native tooltip op exists:** `overlay_set_tooltip` = 950,
  `(overlay_set_tooltip, <overlay_id>, <string_id>)` — `headers/header_operations.py:403`.
  Applied directly to the label overlays; no fake hover-overlay needed.
- **String tables:** `mods/custom_troops/custom_troops_strings.py`. Attribute display
  strings `str_cstm_ca_*`: STR / AGI / INT / CHA. Skills `str_cstm_skill_*`: all 36.
  Proficiencies `str_cstm_wpt_*`: 7 (1H Weapon, 2H Weapon, Polearm, Archery, Crossbow,
  Throwing, Firearm). New tooltip strings can be added here (e.g. `str_kct_tip_*`).
- **Shown skills = ACTIVE_FIGHTING_SKILLS** (`..._presentations.py:112-113`) — 9 STR/AGI
  combat skills in module order: Power Draw, Power Throw, Power Strike, Ironflesh,
  Horse Archery, Riding, Athletics, Shield, Weapon Master (STR: ironflesh, power_draw,
  power_throw, power_strike; AGI: horse_archery, riding, athletics, shield, weapon_master).
- **Attribute boxes:** `..._presentations.py:1058-1096`. Grid via
  `script_kct_get_grid_position` count=4, `KCT_STATS_ATTR_CONT_WIDTH=2` (2 cols x 2 rows).
  Level text at `:1054-1056`. The stats column is x=600..960 (~360 wide,
  `KCT_STATS_SIZE_X = 960 - KCT_STATS_POS_X`), so 3 boxes on ONE horizontal line need
  ~120px boxes (ATTR_COL_WIDTH=185 → must shrink or reposition). Layout rework must also
  shift the Level y-offset math (`:1056`).
- **Tooltip text source (prose, confirm exact numbers at impl):** STR → +health & melee
  damage; AGI → +movement speed & weapon points; INT → skill-point learning rate;
  Ironflesh → +hit points; Power Strike → +melee damage; Power Draw → +bow damage;
  Power Throw → +thrown damage; Athletics → +foot speed; Riding → ride faster/better
  horses + mounted combat; Shield → better shield use/blocking; Weapon Master →
  +weapon proficiency points/handling; Horse Archery → shoot bows on horseback.
  Exact formulas available in base `module_scripts.py` if we want numbers.

### Problem 3 — proficiency layout research (RESEARCHED)
- **7 proficiencies** (`wpt_*`, string table above) — stored on the dummy as skill
  levels via `script_kct_proficiency_apply_preset` (`..._scripts.py:2526+`; focus
  weapon = `:proficiency` 1-7, 0 = Balanced spread; cap 40*wm+60 unless leaf). Read-only
  labels read each via `store_skill_level`/`troop_get_skill` on the dummy.
- **Current PROF section:** `..._presentations.py:1098-1119` — Fallback selector (only
  when `$cstm_proficiency_role_selected != 0`) + Proficiency (Role) selector; both
  750x750 combo buttons; globals `$cstm_proficiency_role_selected` /
  `$cstm_proficiency_weapon_selected`; apply on change at `:1420`.
- **Section stacking is BOTTOM-UP in this presentation** (y=0 at points, then skills,
  then proficiency, then attributes, then level at the largest offset). New order
  Attributes → Skill points → Proficiency selectors+labels means remapping the section
  y-offset formulas (`:1056`, `:1061`, `:1098`, and the skills grid offset).
- 7 labels at ~18px = ~126px of read-only "1H Weapon : X" rows under the selectors.

---
### Open clarifications to ask when implementation starts
- (RESOLVED) "Cheat menu → Mod Options": user confirmed it's the existing mod options
  screen (`prsnt_mod_option`, Camp → Main Settings) — not a new cheat-menu entry.

---

## Status log

### Research complete (awaiting "we can start now")
- All 3 problems are implemented and compiled — see "Done & compiled" below.
- (RESOLVED) "Cheat menu → Mod Options": existing mod options screen
  (`prsnt_mod_option`, Camp → Main Settings) — not a new cheat-menu entry.
- (RESOLVED) Points-line placement: user chose "glue each points line to its section"
  (Attribute points with attrs, Skill points with skills, Proficiency points with
  selectors/labels).

### Done & compiled (do not redo)
- **Problem 1 — Custom Troop Funds (COMPLETE):**
  - Mod option `kct_funds_tier` appended to `mod_options` in
    `mods/xgm_mod_options/xgm_mod_options.py` (after `op_cheatmode`): combo
    `["Balanced","Boost","Cheater"]`, stored in `$g_kct_funds_tier`.
  - Scaled only at the KCT read point in
    `kingdom_custom_troop_tree_creator_presentations.py` right after the
    `troop_get_slot` of `$cstm_total_funds` from `trp_cstm_inventory_values`:
    tier 1 → `store_mul ×2`; tier 2 → `assign 50000000` (gate never binds).
    Base custom_troops store (presets 1-3) untouched.
- **Problem 2 — Tooltips + Layout (COMPLETE):**
  - Tooltip strings `kct_tip_*` appended to `custom_troops_strings.py`:
    strength/agility/intelligence FIRST (so `str_kct_tip_strength + attribute_id`
    resolves) + 10 skill tips. NOTE: **ACTIVE_FIGHTING_SKILLS is 10 skills, not 9** —
    `looting` is `sf_base_att_agi` in this mod (`module_skills.py:65`) and IS shown,
    so `kct_tip_looting` exists too.
  - `overlay_set_tooltip` (op 950) wired onto: attribute label overlays via
    `str_kct_tip_strength + :attribute`; skill label overlays via
    `"str_kct_tip_" + skill[0]` (compile-time string).
  - Layout: CHA removed (range `attributes_begin..ca_intelligence+1`); STR/AGI/INT on
    ONE row (ATTR_COL_WIDTH=120, ATTR_CONT_WIDTH=3, grid num_items=3); Level line now
    `Level {reg0}    HP {reg1}    AGI {reg2}` (`store_troop_health` 2175 absolute=1,
    `store_attribute_level` ca_agility); points lines glued to sections.
- **Problem 3 — Proficiency read-only labels (COMPLETE):**
  - Order now Attributes → Skills → Proficiency selectors + read-only labels.
  - Labels via `store_proficiency_level` (2176) on `:dummy`, rendered as label + value
    overlays (label at x=0, value at x=COL_WIDTH-75). No number boxes.
  - Proficiency points line glued below the labels.
- **Impl gotchas (do not repeat):**
  - W.R.E.C.K. compiler rejects string-register args beyond `str_s0` to scripts
    ("illegal reference `s.s1`") — render "Label value" as TWO overlays instead of one
    combined s1 string.
  - Section heights now include their points row; `KCT_STATS_POINTS_*` constants must be
    defined BEFORE the section-height formulas (Python forward ref → NameError).
  - Skill points line y must be `GAP_Y + ATTR_SECTION_HEIGHT + SKL_GRID_HEIGHT`
    (grid spans base..base+grid, so the points line sits at the grid's top edge).
  - Skill grid bottom-up: 10 skills / 2 cols = 5 rows (SKL_GRID_HEIGHT dynamic).
- **Problem 1-3 all compiled** via `python compiler\compile.py tag` — COMPILATION
  SUCCESSFUL (only the 2 pre-existing harmless l.mouse_state/l.object notices).
- (Earlier, still valid) Script-error overlay spam fixed; 314 proficiency points on save
  fixed; Reset/Exit buttons dynamic; naked-dummy re-equip fixed; gear propagation
  restored per user decision; raising a skill raises the whole subtree live.

### Accepted output caveats (baseline-verified)
- script order changed (save-safe); customise_troop combo block ordering; menus.txt
  structure; presentations.txt troop-tree-editor block moved to its own mod file.
