# Guard <-> KCT (Kingdom Custom Troop Tree) Integration — Task Plan

Companion to `guard_system_analysis.md`. Defines the work to make every guard
location in the game use the player's custom troop tree once that tree is
created, while guaranteeing that **no replacement ever happens unless the user
actually creates/saves a custom troop tree**.

---

## 1. Design constraint (read first)

> "The tree definition can be done or not, so the replacement must NOT run
> automatically — it must be correlated to the creation of the new troop tree."

Rules that follow from this:

1. **No tree -> native guards.** All guard sites keep their current fallbacks
   (`trp_hired_blade`, vaegir/kingdom defaults) untouched.
2. **Tree created -> replace.** Guard-slot replacement is a step of the
   tree-creation/apply flow, not a game-start or load-time step.
3. **Single source of truth.** The chosen tree is described by the KCT globals
   already set by `kct_presentations/branch_display.py:36-96`:
   `$cstm_troops_begin`, `$cstm_troops_end`, `$cstm_num_tiers`,
   `$cstm_presentation_troop`, `$cstm_reinforcement_templates_begin/_end`.
   No new tree-state global is invented; guards read the same values the
   recruitment wiring already reads.
4. **Persistence.** Faction slots are serialised into saves, so a one-shot
   replacement at tree creation persists; it must NOT be re-applied on load
   (that would violate "not automatic").

---

## 2. What the tree provides vs. what guards consume

The custom tree has `$cstm_num_tiers` tiers (presets 1-3: 5-7 tiers; preset 4:
6 tiers). The native guard system consumes *per-faction* troop slots:

| Faction slot | Consumed by (analysis ref) |
|---|---|
| `slot_faction_guard_troop` | castle court (enter_court.py:72-107, visitors 6-7), town street visitor 23, castle-gate slot code (currently commented out) |
| `slot_faction_prison_guard_troop` | town street visitor 24, castle courtyard prison guard, captivity-defeat guard (mnu_fucked_by_enemy_prison.py:13-30) |
| `slot_faction_castle_guard_troop` | castle courtyard visitors 40-46 fallback / gate code |
| `slot_faction_tier_2_troop`, `slot_faction_tier_3_troop` | town street visitors 25-28 (shuffled 2x tier-2 + 2x tier-3), prison break (mnu_town.py:509-576) |
| (garrison stacks, NOT slots) | castle courtyard wall guards (mnu_town.py:1061-1189) |

### Which faction(s) to write — VERIFIED (analysis §11)

Per-site resolution for a **player-owned** fief, confirmed against source:

| Site | Slot(s) | Player-fief read target |
|---|---|---|
| Castle court (`enter_court.py:73-93`) | `slot_faction_guard_troop` | `$g_player_culture` when it is a native kingdom (branch 1, the normal case); else `fac_player_supporters_faction` (branch 3) |
| Town street, normal (`mnu_town.py:589-601`) | prison_guard, castle_guard, tier_2, tier_3 | **`slot_center_original_faction`** — NOT the player's factions |
| Town street, prison break (`mnu_town.py:515-543`) | tier_3 (×2), tier_4 | `:town_faction` = `fac_player_supporters_faction` for player towns |
| Captivity (`mnu_fucked_by_enemy_prison.py:13-30`) | `slot_faction_prison_guard_troop` | capturer faction (not player-controlled) |
| Castle courtyard (`mnu_town.py` castle_inspect) | garrison stacks (visitors 40-47) | N/A — not slot-based |

**Key consequences for the write targets:**
1. `fac_culture_player` — its `tier_1` is already wired by the apply flow
   (`branch_display.py:96`); extend it with the remaining guard/tier slots so
   future/patched readers can use it. BUT native readers mostly do NOT read it:
   the court reads `$g_player_culture`/`center_faction`, the street reads
   `slot_center_original_faction`.
2. `fac_player_supporters_faction` — genuinely read by the **prison break**
   (player towns) and by the court fallback branch 3. Its slots are *copied
   from its culture* by `initialize_faction_troop_types`, but that copy runs at
   game start only (and from `fac_culture_1` — the CSTM re-points culture to
   `fac_culture_player` only in `new_start_operations`, *after* the copy). So a
   mid-game tree change must write the player kingdom faction's slots directly.
3. `slot_center_original_faction` — read by the **normal town street** of
   player-owned towns; never updated on transfer. → Requires a `mnu_town.py`
   change (see T5).

> **T0 — VERIFIED DONE (analysis §11):** the per-site read targets above replace
> the earlier "culture vs kingdom faction" uncertainty. The full evidence is in
> `guard_system_analysis.md` §11.1-11.6.

---

## 3. Tier -> slot mapping decision — VERIFIED against all four presets

A tree with N tiers must feed 3 dedicated guard slots + up to 3 tier slots.
Mapping (verified against `custom_troops_troop_trees.py`, `layout.py` PRESET_TREES_1_3
and `kingdom_custom_troop_tree_creator_constants.py` PRESET_4_UNITS; see analysis §11.5):

| Native slot | Source tier (0-based tree index) | Representative troop |
|---|---|---|
| `slot_faction_tier_1_troop` | tree tier 0 | `$cstm_troops_begin` (already wired) |
| `slot_faction_tier_2_troop` | tree tier 1 | branch/node 0 of tier 1 |
| `slot_faction_tier_3_troop` | tree tier 2 | branch/node 0 of tier 2 |
| `slot_faction_tier_4_troop` | tree tier 3 | branch/node 0 of tier 3 (needed for prison break) |
| `slot_faction_guard_troop` | top tier (index N-1) | branch/node 0 of top tier |
| `slot_faction_castle_guard_troop` | top tier (index N-1) | same as guard |
| `slot_faction_prison_guard_troop` | mid tier (index ≈ N/2) | branch/node 0 of mid tier |

**Representative = first troop of the tier** — for presets 1-3 that is always
`(tree, skin, branch 0, tier)`, which exists in every tier (branch 0 is always
generated). For preset 4 the tier's first node index is:

- tier 0 → node 0 (A), tier 1 → node 1 (B1), tier 2 → node 3 (C1),
  tier 3 → node 7 (D1), tier 4 → node 13 (E1), tier 5 → node 19 (F1).

**Troop-ID templates (both skins, `s` = skin 0/1):**
- Presets 1-3 (`1_tier` 7 tiers / `2_tiers` 6 / `3_tiers` 5):
  `trp_cstm_custom_troop_<tree_id>_<s>_0_<tier>` (branch 0).
- Preset 4: `trp_cstm_custom_troop_4_<s>_<node>_0`.

**T1 — task:** derive the per-tier troop IDs for a chosen tree from the selected
preset (via `$cstm_selected_tree`/`$cstm_selected_gender` + the templates above).
A helper `script_kct_guard_troop_for_tier(tier_index, guard_role)` is proposed
(see T2); do not duplicate the layout logic — reuse the ID templates only.

---

## 4. Tasks

### T0 (verification) — Confirm per-site faction resolution
- **Where:** `mnu_town.py:502-638`, `enter_court.py:72-107`,
  `mnu_fucked_by_enemy_prison.py:13-30`, `activate_town_guard.py`.
- **Goal:** write down, for a *player-owned* town/castle, exactly which faction
  ID each guard site reads (culture vs `fac_player_supporters_faction`), so the
  write targets in T2 are correct.
- **Acceptance:** a one-line note per site in this file.
- **Status: DONE.** Results recorded in §2 table + `guard_system_analysis.md` §11.
  Highlights: court reads `$g_player_culture` (native kingdom) or the
  `center_faction` fallback; normal street reads `slot_center_original_faction`;
  prison break reads `fac_player_supporters_faction` tier slots.

### T1 (design) — Tier -> slot mapping
- **Where:** this file, section 3.
- **Goal:** fixed mapping table from tree tier index -> `slot_faction_*` value,
  validated against all four presets (including preset 4's 6-tier / 22-unit
  layout).
- **Acceptance:** mapping table present; no preset produces an out-of-range tier.
- **Status: DONE.** Mapping verified in §3 (guard = top tier, castle_guard = top
  tier, prison_guard = mid tier, tier_2/3/4 = tree tiers 1/2/3, all branch/node 0).

### T2 (core) — New helper `script_kct_apply_guard_replacements`
- **New file:** `modmerger/mods/kingdom_custom_troop_tree_creator/kct_scripts/`
  (e.g. `guard_replacements.py`), exposing
  `script_kct_apply_guard_replacements`.
- **Behaviour (invoked ONLY from tree-creation flow):**
  1. Guard `$cstm_troops_begin` > 0 (a tree is actually active).
  2. Compute guard/castle/prison/tier-2/tier-3/tier-4 troop IDs via the T1
     mapping (helper `script_kct_guard_troop_for_tier(tier, role)`.
  3. `faction_set_slot` the guard slots + tier slots on
     **`fac_culture_player`** (single source of truth for the tree).
  4. Do the same on **`fac_player_supporters_faction`** (prison break + court
     fallback read this faction directly for player fiefs).
  5. Keep it idempotent — calling it again with the same tree is a no-op.
- **Acceptance:** script compiles; slots visible in game after Save.

### T3 (core) — Wire the helper into the tree-creation flow
- **Where:** `kct_presentations/branch_display.py`
  - `_build_apply_kingdom_setup_ops()` (line 87) — the ops already run on
    presentation load AND are re-emitted by the Save button handler
    (`$kct_apply_tree_button`, line 330-339). Append the
    `script_kct_apply_guard_replacements` call here so it runs exactly when the
    tree is created/saved.
- **Constraint:** do NOT call it from `kingdom_custom_troop_tree_creator_simple_triggers.py`
  (load-time) or `game_start.py`. Load-time re-application is forbidden (rule 2).
- **Acceptance:** saving a tree updates guards in-game; loading a save does NOT
  (slots persist from the save).

### T4 — Castle court guards (enter_court.py:72-107)
- **Action:** this site reads `$g_player_culture` first (a native kingdom when a
  culture was chosen) and only falls back to `fac_player_supporters_faction`.
  Since `fac_culture_player` is not in `npc_kingdoms_begin..end`, the custom tree
  never wins on its own. **Required source change** in `enter_court.py` (branch 1):
  before reading `$g_player_culture`, add a check — if `$cstm_troops_begin > 0`
  AND `:center_faction == $players_kingdom`, read the guard slot from
  `fac_culture_player` (or the KCT-computed guard troop) and skip the native
  branches.
- **Acceptance:** after Save, castle-court guards are the tree's top-tier unit.

### T5 — Town street guards (mnu_town.py:502-638) + prison break (509-576)
- **Action — two parts:**
  1. **Prison break (515-543)** reads `fac_player_supporters_faction` tier_3/tier_4
     directly for player towns — T2's write already covers it. No source change.
  2. **Normal street (589-601)** reads `slot_center_original_faction` for
     player-owned towns, which T2 cannot cover. **Required source change** in
     `mnu_town.py:595-601`: in the `else_try` (player-own) branch, when
     `$cstm_troops_begin > 0`, read the four slots from
     `fac_culture_player`/`fac_player_supporters_faction` instead of
     `:town_original_faction` (keep the original-faction read as fallback when no
     tree is active).
- **Acceptance:** walking the player's town streets shows custom units; prison
  break escapes are fought with custom tier-2/3 units.

### T6 — Castle courtyard wall guards (mnu_town.py:1061-1189)
- **Action:** document decision. These are spawned from the party's **garrison
  stacks** (not faction slots). Options: (a) leave native — garrison is already
  custom troops if the player's fiefs recruit via the tree; (b) later, feed the
  top-tier custom troop into the stack.
- **Acceptance:** decision recorded; no code change unless (b) chosen.

### T7 — Castle gate code (mnu_castle_outside.py:446-471)
- **Action:** leave the commented-out `slot_faction_guard_troop` code as-is
  (menu chain only, no scene guard) unless a specific gate-scene need appears.
  Record in this file.
- **Acceptance:** nothing changes.

### T8 — Captivity-defeat prison guard (mnu_fucked_by_enemy_prison.py:13-30)
- **Action:** the site already reads the prison-guard slot of the capturer's
  faction. **Fix noted in analysis:** fallback checks `== -1` while every other
  site checks `== 0` (inconsistent). Standardise to `== 0`.
  - If the capturer is the player's own faction, T2's write makes it a custom
    unit; otherwise native.
- **Acceptance:** fallback constant consistent with the rest of the module.

### T9 — `activate_town_guard.py` team classification
- **Action:** confirm `soldiers_begin..soldiers_end` range still covers the
  custom troops (they are kingdom-tagged `fac_player_supporters_faction`
  troops; verify they fall inside the range or are handled by the faction
  check). No automatic tree work here.
- **Acceptance:** tc_escape town guards (custom troops) get flipped to the
  attacking team correctly.

---

## 5. Out of scope / explicitly NOT automatic

- No new simple trigger, no `game_start.py` change, no load-time re-apply.
- No change to the KCT picker/creator UI beyond the Save-flow hook (T3).
- No change to village volunteer recruitment (already wired to the tree).
- No change to `prsnt_all_items.py`.
- **Allowed source changes** (modmerger injects these into native scripts; NOT
  automatic — they only read `$cstm_troops_begin`, which is 0 until a tree is
  saved):
  - `enter_court.py` branch 1 (T4) — prefer the player's custom guard when a
    tree is active.
  - `mnu_town.py:595-601` player-town street branch (T5) — read the player's
    culture slots when a tree is active.
  - `mnu_fucked_by_enemy_prison.py` (T8) — fallback `== -1` → `== 0`.
- These changes are *condition-based*, not *apply-based*: they fire per-load from
  persisted faction slots, but only after a tree was created (rule 2 is about the
  *write*, which stays in the Save flow only).

## 6. Verification (required after implementation)

1. `python compiler\compile.py tag` from repo root -> `COMPILATION SUCCESSFUL`.
2. In-game: create/save a tree, visit your castle court + a player-owned town
   + trigger a prison break -> all show custom units.
3. Start a NEW game without touching the picker -> all native guards remain.
4. Load a save made after a tree Save -> custom guards persist (no re-apply).
5. Conquer a NEW enemy town AFTER the tree is saved, then walk its streets
   -> custom guards appear (validates the T5 `slot_center_original_faction`
   bypass works on freshly captured towns).

---

## 7. Open questions for the user

- **RESOLVED:** T1 tier->slot mapping verified against all four presets (§3):
  guard = top tier, castle_guard = top tier, prison_guard = mid tier,
  tier_2/3/4 = tree tiers 1/2/3, all = branch/node 0 representative.
- Confirm T4/T5 source changes are acceptable (they are condition-based, not
  apply-based — see §5).
- Confirm T6 option (a) leave courtyard garrison-based vs (b) inject custom
  top-tier into the stack.
- Confirm T8 fallback standardisation (`== 0`) is wanted.
