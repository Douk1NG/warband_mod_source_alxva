# Update 010 - Bandit / Pirate Population Control + Enterprise Economy Retune

## Summary

Two feature areas plus small fixes:

1. **Bandit & pirate population control** — bandits/looters capped per type, roaming parties shrunk, respawns changed from bursts to a steady 1-every-24h trickle (seed to cap on first run), pirate ships merged into one capped pool, manhunters now scale 2:1 with the live bandit count, lairs stay gone 3 days after destruction
2. **Enterprise economy retune** — all 9 businesses rebalanced to a ~25-week cost-proportional payback, enterprises buy raw materials at the cheaper price, town prosperity now scales production quantity, operating enterprises boost their host town's prosperity and merchant stock, and retuned values are re-applied to existing saves on load.

Bundled fixes: recruiter trigger hardened against `-1` faction errors, a player-troop combat-bonus bug fixed, and a TPE save-repair trigger added (its script body is currently commented out — see Notes).

---

## Feature 1 — Bandit / Pirate Population Control & Respawn Rework

- **Tunable constants** (`source/module_constants.py`): added caps (bandits 18/type, looters 18, deserters ≤20 troops, pirate ships 5 total / 15 per ship, manhunters cap 36) and timing (`bandit_lair_respawn_hours = 72`, `bandit_respawn_interval_hours = 24`). A new free slot `slot_party_template_respawn_cooldown = 2` stores each type's next-spawn time. `bandit_respawn_cooldown_hours = 336` is kept but now legacy (no wipe-block).
- **All bandit/pirate spawn scripts** (`source/scripts/feats/bandit_spawn_scripts.py`, new file): `script_spawn_bandits` (the full orchestrator — land bandits, looters, deserters, pirate-ship pool, dark hunters, merchant ships, lairs), its trickle helper `script_spawn_party_type_with_cooldown`, `script_spawn_one_pirate_ship`, and `script_get_spawn_report_line`. Registered in `source/scripts/feats/__init__.py`. None of this logic remains in `misc_scripts.py`.
- **Land bandits + looters** (`source/scripts/misc/misc_scripts.py`): the six land-bandit blocks collapsed to one helper call each (lair gate preserved), looters now capped at 18 (was 42).
- **Pirate ships → one pool** (`source/scripts/misc/misc_scripts.py`): the three ship templates combined into a single 5-ship trickle via new `script_spawn_one_pirate_ship` (spawns the least-represented type). Ships are not lair-linked; the trickle bounds them.
- **Party-size caps** (`source/module_party_templates.py`): land bandits/looters capped at `num_max_bandit_party_size` (20); ships at `num_max_pirate_ship_size` (15).
- **Deserter size cap** (`source/scripts/misc/misc_scripts.py`): level-scaled size `level*2+11` clamped to 20 via `val_min`.
- **Free recruit when outmatched** (`source/module_dialogs.py`): new `deserter_recruit_free` talk option (player stronger, `party_can_join`) merges the party in with no denars/penalty.
- **Lair respawn delay on all paths** (`source/module_game_menus.py`): destroyed lairs now wait `bandit_lair_respawn_hours` (72h) before returning on all three removal paths (previously only the loot-screen path delayed).
- **Manhunter scaling** (`source/module_triggers.py`): cap = active bandits / 2, clamped `[4, 36]`; spawns from a random town while below cap.
- **Diagnostics report** (`source/module_presentations.py`, `source/module_game_menus.py`, `source/ids/*`): new `prsnt_spawn_diagnostics` (per-type `active/cap`, next-spawn hours, lair flag, ship total, manhunter/deserter counts) with `script_get_spawn_report_line`; reachable from Reports → Economic.

---

## Feature 2 — Enterprise Economy Retune, Saved-Game Fix & Town-Prosperity Production

- **Buy at cheaper price** (`source/scripts/centers/centers_scripts.py`): enterprise raw-material price now uses `val_min` (was `val_max`), so it pays the lower of local/imported.
- **Profit rebalance** (`source/scripts/core/core_scripts.py`): retuned input/output/overhead for all 9 goods so weekly profit ≈ `building_cost / 25` (velvet overhead 160→850, the standout earner). 
- **Prosperity → production tiers** (`source/scripts/misc/misc_scripts_extra.py`, `source/module_presentations.py`): new `script_get_enterprise_prosperity_numerator` (×0.5 poor → ×2.0 very rich) scales produced/consumed goods and profit in `process_player_enterprise` and the enterprise presentation.
- **Town benefits** (`source/module_presentations.py`): on each applied run, `+1 + floor(Trade/5)` prosperity and merchant stock `outputs * (1 + floor(Trade/10))`.
- **Saved-game fix** (`source/module_simple_triggers.py`): one-shot trigger re-applies `script_initialize_item_info` on load (guarded by `$g_enterprise_init_done`) so old saves get the new economy.

---

## Bundled Fixes

- **Recruiter trigger hardening** (`source/module_simple_triggers.py`): `store_relation` calls guarded against `-1` factions; broken recruiters reset to `ai_bhvr_hold` to stop error spam.
- **Player-troop combat bonus** (`source/scripts/dickplomacy/dickplomacy_scripts.py`): now resolves the troop from the player agent before reading strength (was reading the agent id).
- **TPE save-repair trigger** (`source/module_simple_triggers.py`): one-shot trigger calls `script_tpe_fix_save` — but that script's body in `tournament_scripts.py` is currently commented out, so the call is a no-op until restored.

## Notes

- All changes are behavior-affecting (gameplay balance).
- Respawn is a trickle (seed to cap, then 1/24h); there is no 2-week wipe block anymore.
- Tunables live in `module_constants.py`, `core_scripts.py`, and `misc_scripts_extra.py`.
- Known cosmetic bug: the diagnostics report labels Looters "cap 42" in its header text, but the value shown uses the real cap 18.
- Compiles successfully via `python compiler/compile.py tag` (COMPILATION SUCCESSFUL).

---

## Update 010 additions — Manhunter rework + prisoner buy dialog

### Manhunter changes
- **Party template** (`source/module_party_templates.py:47`): `trp_slaver_chief` moved to front of troop list
- **Cap reduced** (`source/module_constants.py:1884`): `num_max_manhunters` 36 → 24
- **Spawn logic rewritten** (`source/scripts/spawn_bandits.py:171-219`): spawns near active bandit lairs (radius 10) with round-robin equal distribution; fallback to spawn points if no lairs
- **Spawn diagnostics fixed** (`source/presentations/prsnt_spawn_diagnostics.py:169-175`): uses fixed `num_max_manhunters` cap instead of deleted ratio constant
- **`manhunter_bandits_per_manhunter` deleted** from `module_constants.py:1884`

### Manhunter prisoner buy system
- **New scripts** (`source/scripts/mnh_give_manhunter_prisoners.py`): `mnh_give_manhunter_prisoners` (gives specific party bandit prisoners), `mnh_get_manhunter_prisoner_price` (calculates ransom broker price), `mnh_buy_manhunter_prisoners` (transfers prisoners to player for gold)
- **Registered** in `source/module_scripts.py` (import line 647, extend line 1482)
- **Dialog chain** (`source/module_dialogs.py:2680-2701`): 5 entries — "I'd like to buy some of your prisoners" → price display → deal/cancel → transfer
- **Pricing formula**: `((troop_level + 10)²) / 6` per prisoner (matches existing ransom broker formula)
- **No auto-fill on spawn**: manhunters start empty; they acquire prisoners by defeating bandits on the map

---

##((deserters — scripts that contain deserter logic (for later isolation review)

No script is *named* deserter; the logic is embedded. Listed by containing script, file, and line context. (Data defs — party_templates, factions, troops, meshes, strings, menus — are out of scope; only scripts here.)

1. **`script_spawn_bandits`** — `source/scripts/feats/bandit_spawn_scripts.py` (~lines 107–143)
   Deserter *party* spawn: picks a lord's party, spawns `pt_deserters`, tags faction icon, clamps size to `num_max_deserter_party_size`. (update-010 owned.)

2. **weekly-report simple trigger** — `source/module_simple_triggers.py` (trigger header ~4944; desertion block ~4973–5072)
   Morale-leak desertion: removes troops from `p_main_party` by morale, builds the "X deserted" message. This is inline in the trigger, not a named script — would need extraction into `script_process_party_desertions` to isolate.

3. **`script_give_center_to_faction`** — `source/scripts/centers/centers_scripts.py` (~1458)
   Reinforcement party that fails to reach a center is converted into a `pt_deserters` party (`#SB : reinforcements becomes deserters`).

4. **deserter dialog tree** — `source/module_dialogs.py` (~37495–37700)
   `deserter_talk` / `deserter_paid_talk` / `deserter_recruit` / `deserter_recruit_free` / `deserter_barter*` blocks. Engine-locked to `module_dialogs.py` (can't move to a feat file).

5. **`prsnt_spawn_diagnostics`** — `source/module_presentations.py` (~12990)
   `store_num_parties_of_template, ":num_des", "pt_deserters"` line (update-010 diagnostics).

6. **`mnu_dplmc_deserters`** — `source/module_game_menus.py` (~20467)
   Deserter notification menu (opened from the weekly-report trigger at simple_triggers ~497). Plus encounter-background checks keyed on `pt_deserters`/`fac_deserters` (~4425, 5139, 10099, 16777, 21860, 21924).

7. **deserter-troop setup** — `source/scripts/faction_ai/faction_ai_scripts.py` (~389–444)
   `slot_faction_deserter_troop` assignment per kingdom (which culture deserter troop each faction uses).

8. **deserter references in other scripts** (minor, not spawn logic):
   - `source/scripts/misc/misc_scripts_extra.py` (~4907 deserter troops 10% chance; ~12643 deserters have military training)
   - `source/scripts/diplomacy/diplomacy_scripts.py` (~1411 counts deserters in a party → reg0)
   - `source/scripts/heraldry/heraldry_scripts.py` (~570, ~745 `pt_deserters` banner coloring)
   - `source/scripts/npcs/npcs_scripts.py` (~262 comment: deserters captured a companion)
   - `source/scripts/quests/quest_scripts.py` (~831+ all commented-out `qst_bring_back_deserters` quest)

