# Guard System Analysis - Dickplomacy Mod

## 1. Guard Troop Types Initialization (`source/scripts/initialize_faction_troop_types.py`)
- Sets faction guard slots per culture (6 cultures: Swadian, Vaegir, Khergit, Nord, Rhodok, Sarranid)
- **Guard troops**: `trp_swadian_sergeant`, `trp_vaegir_guard`, `trp_khergit_horseman`, `trp_nord_warrior`, `trp_rhodok_veteran_spearman`, `trp_sarranid_castle_guard`
- **Prison guards**: `trp_swadian_prison_guard`, `trp_vaegir_prison_guard`, `trp_khergit_prison_guard`, `trp_nord_prison_guard`, `trp_rhodok_prison_guard`, `trp_sarranid_prison_guard`
- **Castle guards**: `trp_swadian_castle_guard`, `trp_vaegir_castle_guard`, `trp_khergit_castle_guard`, `trp_nord_castle_guard`, `trp_rhodok_castle_guard`, `trp_sarranid_castle_guard`

## 2. Castle Scene Guard Setup (`source/scripts/enter_court.py:72-107`)
- Gets guard troop from player's culture via `faction_get_slot`
- Falls back to `trp_hired_blade` if guard troop slot is 0 (lines 95-104)
- Sets visitors at positions 6 and 7: `(set_visitor, 6, ":guard_troop")`, `(set_visitor, 7, ":guard_troop")`
- **Uses `$g_player_culture`** which may not reflect KCT-customized troop trees

## 3. Town Street Guards - "Take a walk around the streets" (`source/game_menus/mnu_town.py:502-638`, `town_center` menu)
- Normal (non-prison-break) town entry spawns the **street patrol**:
  - visitor 23 = `:troop_castle_guard` (from `slot_faction_castle_guard_troop`)
  - visitor 24 = `:troop_prison_guard` (from `slot_faction_prison_guard_troop`)
  - visitors 25-28 = 4 shuffled patrol troops drawn from faction tier troops
    (reg0/reg1 = `slot_faction_tier_3_troop`, reg2/reg3 = `slot_faction_tier_2_troop`, via `shuffle_range,0,4`)
  - **Faction resolution**: `$g_encountered_party_faction` for non-player towns; for player-controlled towns uses `$current_town` `slot_center_original_faction` (lines 589-601). Guards come from faction guard slots **not** tier-2/3 troops if `(gt,":tier_2_troop",0)` else defaults to `trp_vaegir_*`.
- **Night/day/fire variations** (lines 594-638): 6 street guards at day (23,24 plus 2+1+2+1 on 25-28), 4 at night (1+1+1+1); when a nearby village fire is active, guards redeploy and only 1-2 remain on patrol.
- **Disguise interaction**: if `$sneaked_into_town > disguise_none`, the mission is launched in `tcm_disguised` (lines 564-572) and entry override flags (`af_override_everything`) are applied so guards don't auto-attack the disguised player. Disguise set chosen via `mnu_dplmc_choose_disguise` (`disguise_none=0`, `disguise_pilgrim=1`, `disguise_farmer=2`, `disguise_hunter=4`, `disguise_guard=8`, `disguise_merchant=16`, `disguise_bard=32`).

## 3b. Town Guard Behavior at Runtime (`script_activate_town_guard`, `source/scripts/activate_town_guard.py`)
- Called from `module_mission_templates.py` on `mt_town_center` / `mt_castle_visit` when `$talk_context == tc_escape` (lines 4718 and 6728).
- Re-assigns agent teams so the spawned guards actually engage: soldiers (`soldiers_begin..soldiers_end`) -> team 1 (enemy), and clears scripted mode on walkers/merchants so civilians flee rather than fight.
- **Gap noted**: this only runs in the escape (`tc_escape`) context. The normal day-to-day street guards spawned by section 3 above are NOT put on team 1 by this script on a plain town walk — their hostility on crime comes from elsewhere.

## 4. Prison Break Guard Setup (`source/game_menus/mnu_town.py:509-576`, `tc_prison_break` context)
- When `tc_prison_break`: sets `$talk_context = tc_escape`, `$g_mt_mode = tcm_escape`.
- Spawns tiered guards on visitors 25-28 from faction tier-2/3/4 troops (25-28), day vs night (lines 524-561), with fire-deployable reductions (lines 545-560).
- visitor 39 = `trp_player`; `set_jump_mission = mt_town_center`.
- **VERIFIED** (lines 516-518): `:tier_2_troop` is fetched via `slot_faction_tier_3_troop` — a mislabelling in the variable name: visitors 25/26 use the tier-3 slot troop, not tier-2. `:tier_4_troop` is the only reader of `slot_faction_tier_4_troop` in this flow.

## 5. Castle Courtyard ("Wall") Guards (`mnu_town.py` `castle_inspect` menu, "To the castle courtyard", lines 1061-1189)
- `mt_castle_visit` mission; visitor 7 = `trp_player`.
- Spawns the enemy party's garrison as guards at visitors 40-47 (`set_visitor, :guard_no, :cur_troop_id, :troop_dna`), with nearby-fire redeploy logic (same pattern as town patrol).
- Also sets prison guard at visitor 24 (lines 1127-1144), and applies disguise entry overrides on `mt_castle_visit` entries 0-7 (lines 1172-1176).
- Prison-break variant (`tc_prison_break`): same garrison-spawn at 40-47, line 7 player (lines 1067-1099).

## 5b. KCT Mod Integration (`modmerger/mods/kingdom_custom_troop_tree_creator/kingdom_custom_troop_tree_creator_scripts.py`)
- Line 62: `(assign, "$cstm_items_array", cstm_items_arrays_begin)` - sets item arrays
- Line 63: `(call_script, "script_kct_setup_item_arrays")` - initializes item arrays
- Lines 84-85: Sets item types of arrays via `troop_set_slot`
- **Critical**: KCT mod modifies `$cstm_troops_*` globals but does **NOT** modify faction guard slots

## 6. Additional Guard Encounter Points (previously undocumented gaps)

- **Castle gate — "Approach the gates and hail the guard"** (`mnu_castle_outside.py:446-471` → `mnu_castle_guard` → `mnu_castle_entry_granted.py`):
  - The approach is a **non-mission menu chain** (`jump_to_menu, "mnu_castle_guard"`), so no guard troop is spawned on the scene here.
  - Lines 462-466 are **commented-out** code that *would* put `slot_faction_guard_troop` (`:cur_guard`) on `scn_conversation_scene` as visitor 17 with `tc_castle_gate`. Since it's commented out, the castle-gate guard shown to the player is the conversation-troop, not a scene-spawned guard — inconsistent with the courtyard path which spawns real guards.
- **Captivity-defeat prison guard** (`mnu_fucked_by_enemy_prison.py:13-30`): "guards infuriated by refusal to pay the ransom" spawns `slot_faction_prison_guard_troop` from `$capturer_party`'s faction, fallback to `trp_hired_blade` when slot == -1 (`eq, ":troop_prison_guard", -1` — note this checks **-1**, unlike the castle/town paths which check `== 0`). Troops placed in `trp_temp_array_a` slots 0-3 then `script_start_fucking` runs on `scn_dungeon`.

## 7. Disguise System (gates guard hostility)

- **`$sneaked_into_town`** flag (`module_constants.py`): `disguise_none=0`, `disguise_pilgrim=1`, `disguise_farmer=2`, `disguise_hunter=4`, `disguise_guard=8`, `disguise_merchant=16`, `disguise_bard=32`.
- **`$g_mt_mode`**: `tcm_default=0`, `tcm_disguised=1`, `tcm_prison_break=2`; set in `mnu_dplmc_choose_disguise` (line 138 sets `tcm_disguised`) and in the enter-town flow (`mnu_town.py:586`/`mnu_town.py:649` set `tcm_default`).
- Hostility gating in `mt_town_center` / `mt_castle_visit` (lines 4629, 4632, 4647-4648, 6757-6765): inventory use, item pickup and tab-exit are only allowed in `tcm_default`/`tcm_disguised`; the `activate_town_guard` team-flip is gated on `tc_escape`, so **disguised plain walks do not get soldiers re-teamed** — the mod relies on the disguise flag to suppress crime detection rather than re-assigning teams.
- **Gap**: the actual "player loots in town while not disguised → street guards become hostile" trigger was not located in mod code in this repo (likely native engine / stock `mt_town_center` crime triggers); KCT troop-tree swaps that change `soldiers_begin..soldiers_end` membership **may affect** `activate_town_guard`'s `is_between ... soldiers_begin/soldiers_end` classification.

## 8. Potential KCT Interaction Considerations

| Area | Note |
|------|-------|
| **Guard troop override** | `enter_court.py` uses `$g_player_culture` guard slot, but KCT may change which troops are available |
| **Prison escape guards** | `mnu_town.py` uses `$current_town` faction guards - KCT modifying faction troop types could alter what appears |
| **Wall / courtyard guards (§5)** | Spawns garrison companions (visitors 40-46) on `mt_castle_visit`, NOT `slot_faction_*_guard_troop`; if KCT replaces the party's garrison stacks with unavailable troops the courtyard/gate guards could fail to spawn |
| **Street patrol hostility (§3b/§7)** | `script_activate_town_guard` only re-teams soldiers on `tc_escape`; on a disguise-free street walk, hostility depends on the native crime trigger whose soldier-class check (`soldiers_begin..soldiers_end`) KCT may affect |
| **Mixed fallback sentinels** | Castle/town/courtyard paths test slots `== 0` for fallback to `trp_hired_blade`; `mnu_fucked_by_enemy_prison.py` tests `== -1` — inconsistent; KCT zeroing a slot vs -1 could skip the fallback |
| **Faction guard slots** | `initialize_faction_troop_types.py` runs at game start; revisit if KCT modifies these later |

## 9. Key Interaction Points

The KCT mod:
- Creates custom troop trees with preset setups (preset 4 gets reinforcement templates)
- Sets `$cstm_troops_*`, `$cstm_reinforcement_templates_*`, `$cstm_num_tiers` globals
- Initializes item arrays via `script_kct_setup_item_arrays`
- **Does NOT modify** `slot_faction_guard_troop`, `slot_faction_prison_guard_troop`, or `slot_faction_castle_guard_troop`

## 10. KCT Interaction Risk

The KCT mod's custom troop trees may change which troops are available, so guard selection code (`enter_court.py` lines 78-92, `mnu_town.py` lines 591-601) should be verified to still resolve valid troops. Where guards are drawn from **faction guard slots** (visitors 23/24 and `enter_court`), a stale/invalid slot falls back to `trp_hired_blade`. Where guards are drawn from **party garrison stacks** (courtyard/castle wall, visitors 40-46), a KCT-removed stack type means guards could fail to appear with no fallback.

**This would surface as:**
- Different guard troops appearing in castle/prison scenes than expected
- Guards not appearing at all (slot value 0 → fallback to `trp_hired_blade`)
- Mismatched guard types between castle, prison, and walls
- Castle courtyard/wall guards vanishing entirely (garrison-stack path has no fallback)

## 11. KCT Guard-Wiring Verification Findings (2026-08-15) — VERIFIED against source

Verified findings from reviewing the tier→slot mapping (§3 of `guard_kct_integration_tasks.md`) against all four preset tree structures and the guard-consuming code. **These supersede the provisional notes in §8/§9/§10.**

### 11.1 Which faction slot each guard site actually reads (player-fief case)

| Guard site | Code | Slot(s) read | Player-fief faction resolved to |
|---|---|---|---|
| Castle court (enter_court) | `enter_court.py:73-93` | `slot_faction_guard_troop` | `:center_faction` = **`fac_player_supporters_faction`** (see 11.2) |
| Town street — normal path | `mnu_town.py:587-601` | `prison_guard`, `castle_guard`, `tier_2`, `tier_3` | For player-owned towns: **`slot_center_original_faction`**, NOT the player's factions (see 11.3) |
| Town street — prison break | `mnu_town.py:515-543` | `tier_3` (×2: mislabelled `:tier_2_troop` + `:tier_3_troop`), `tier_4` | `:town_faction` = **`fac_player_supporters_faction`** (player towns) |
| Captivity (ransom refused) | `mnu_fucked_by_enemy_prison.py:13-30` | `slot_faction_prison_guard_troop` | `$capturer_party` faction (not player-controlled) |
| Castle courtyard/wall | `mnu_town.py` castle_inspect | garrison stacks (visitors 40-47) | N/A — not slot-based |

### 11.2 `enter_court` guard resolution (player castle court)

- `enter_court.py:75-93`: three branches — (1) `center_faction == $players_kingdom` AND `$g_player_culture` in `npc_kingdoms_begin..end` → guard from `$g_player_culture`; (2) multicultural empires branch (lord `slot_troop_original_faction`, NPC kingdom) → guard from that faction; (3) else → guard from `:center_faction`.
- `$g_player_culture` is set by the chancellor's kingdom-culture select (`module_dialogs.py:5868`, choices restricted to `npc_kingdoms_begin..end` at :5822) and is a **native kingdom** faction (`fac_kingdom_1..6`), or 0 when never chosen. It is **never** `fac_culture_player` (33, which is outside the range).
- Consequence for a player castle court:
  - If `$g_player_culture` is a native kingdom (the normal case after founding a kingdom and picking a culture) → branch (1) matches → guard = that **native kingdom's** guard slot. Writing `fac_culture_player` / `fac_player_supporters_faction` has **NO effect** here.
  - Only if `$g_player_culture` is 0 / out-of-range → branch (3) → guard from `:center_faction` = `fac_player_supporters_faction`.
- **Implication:** to guarantee the player's castle court shows custom-tree guards in all cases, `enter_court.py` must be patched (when `$cstm_troops_begin > 0` AND `center_faction == $players_kingdom`, read the player's custom guard slot instead of `$g_player_culture`; keep native logic otherwise). Writing faction slots alone is insufficient when a culture was chosen.

### 11.3 Town street normal path reads `slot_center_original_faction` for player towns

- `mnu_town.py:589-601`: if `:town_faction != fac_player_supporters_faction` → prison/castle guard from `$g_encountered_party_faction`, tier_2/tier_3 from `:town_faction`. **Else (player's own town)** → ALL FOUR slots read from `:town_original_faction` = `slot_center_original_faction` of `$current_town`.
- `slot_center_original_faction` is set at game start and **never updated on transfer** (`give_center_to_faction_aux.py:56-60` only sets `slot_center_ex_faction`). Note: the CSTM mod does inject an override into `give_center_to_faction_aux` (`custom_troops_scripts.py:2821-2842`) that calls `script_cstm_center_set_culture(center, fac_culture_player)` when a center is given to the player faction — that only re-points the center's **culture** slot, not `slot_center_original_faction`.
- **Implication:** for the player's **captured** towns, street guards (visitors 23/24 + 25-28) show the town's ORIGINAL faction's troops. Writing guard/tier slots on `fac_player_supporters_faction` or `fac_culture_player` does **NOT** affect the player-town street. Options: (a) modify `mnu_town.py:595-601` to read the player's culture/tree slots when `town_faction == fac_player_supporters_faction`; (b) also write the same slots on every NPC kingdom faction that has a player-held fief — rejected: leaks custom guards into NPC-owned towns. Option (a) is the clean route (source change, so it belongs in the task plan as its own task).

### 11.4 Faction-slot initialization gap for `fac_culture_player`

- `initialize_faction_troop_types` loops `kingdoms_begin..kingdoms_end` (which **includes** `fac_player_supporters_faction`, since `kingdoms_begin = fac_player_supporters_faction`), but the guard/castle/prison/deserter/reinforcement assignment is a hardcoded `try/else_try` chain for **`fac_culture_1..6` only**. `fac_culture_player` matches no branch → the player faction's guard slots are never set from the custom culture.
- At game start `game_start.py:253-255` sets `fac_player_supporters_faction`'s culture to `fac_culture_1`, and `initialize_faction_troop_types` (called at `game_start.py:261`) copies culture→kingdom slots — so the player faction's guard/prison/castle slots default to **Swadian** troops and stay that way.
- The CSTM mod's `new_start_operations` (`custom_troops_scripts.py:30-33`) then **re-points** `fac_player_supporters_faction`'s `slot_faction_culture` to `fac_culture_player` — but this runs AFTER `script_game_start`, so the already-copied Swadian guard slots are NOT refreshed.
- **Implication:** the KCT apply step (Save button) must itself `faction_set_slot` the guard/castle/prison/tier slots on the target faction; native init will not do it.

### 11.5 Verified troop-ID/layout schemes (per preset) — basis for the mapping

- **Presets 1–3** (`custom_troops_troop_trees.py` `CustomTroopTree.get_custom_troop_id`): id = `cstm_custom_troop_<tree_id>_<skin>_<branch>_<tier>`; module order is **tier-major**: `for tier in range(num_tiers): for branch in range(min(tier+1, num_branches))` (`add_to_troop_list_with_skin`). Branch 0 exists in **every** tier.
  - `PRESET_TREES_1_3` (`layout.py:33`, mirrored in `tree_io.py:36`): `("1_tier",1 branch,7 tiers)`, `("2_tiers",2,6)`, `("3_tiers",3,5)`.
  - Levels: `levels_start=4 + tier*levels_per_upgrade(5)` → tier0 lvl4 … tier6 lvl34.
- **Preset 4** (`kingdom_custom_troop_tree_creator_constants.py`): id = `cstm_custom_troop_4_<skin>_<node>_0`, node = index into `PRESET_4_UNITS` (0..21, 22 units); 6 tiers: tier0 = node 0 (A, lvl4), tier1 = 1-2 (B1,B2, lvl10), tier2 = 3-6 (C1-C4, lvl18), tier3 = 7-12 (D1-D6, lvl26), tier4 = 13-18 (E1-E6, lvl34), tier5 = 19-21 (F1-F3, lvl40). Troops appended **at the end** of the troop list (skin 0 nodes 0-21, then skin 1), with own sentinel `trp_cstm_custom_troop_4_end`.
- `$cstm_troops_begin` = (tree, skin, branch 0, tier 0) = the recruit troop; already wired as `fac_culture_player` tier_1 by `_build_apply_kingdom_setup_ops` (`branch_display.py:87-103`), which also re-runs `script_cstm_center_set_culture` on all player-faction walled centers. It does **NOT** write any other faction slot.

### 11.6 Oddities found in the KCT implementation (flagged)

1. **`mnu_town.py:516-517` mislabelling** — `:tier_2_troop` reads `slot_faction_tier_3_troop` (and line 517 reads it again). Not a KCT bug, but the prison-break guard level is higher than the variable name implies.
2. **`_build_apply_kingdom_setup_ops` only wires tier_1** — guard/castle/prison/tier_2+ slots are never written by KCT; and the town-street source for player towns (`slot_center_original_faction`, 11.3) is not addressed at all.
3. **Duplicated range logic** — `branch_display._build_create_setup_ops` (`branch_display.py:35-85`) and `tree_io._build_compute_range_ops` (`tree_io.py:42-77`) duplicate the same preset-range computation; drift risk if one changes.
4. **`enter_court` custom-culture branch never matches** — `fac_culture_player` is not in the npc-kingdom range, so the player court relies on `$g_player_culture` (a native kingdom, if a culture was chosen) or the generic `center_faction` fallback (see 11.2). Patching `enter_court.py` is needed for guaranteed custom court guards.
5. **`initialize_faction_troop_types` has no `fac_culture_player` case** — player-faction guard slots remain Swadian defaults even after a KCT tree is created (see 11.4).
6. **Fallback sentinel inconsistency** — `mnu_fucked_by_enemy_prison.py` tests `== -1`; all other guard paths test `== 0` (see §8, row "Mixed fallback sentinels").

---

**Usage**: This file serves as the primary reference for guards in castle, town, prison, and wall scenes. Update this file whenever the guard system behavior changes or new KCT features are added.