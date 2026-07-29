# Bandit and Lair Respawn System Documentation

This document explains the architecture, logic flow, slots, and design decisions of the Bandit and Lair Respawn System in this module system. It is designed to help developers and AI agents understand what is intentional, where logic is divided, and how state is preserved.

---

## 1. Outlaw & Neutral Entities Breakdown

### A. The 6 Regional Bandit Types (Factional Outlaws)
Each of the 6 main factions suffers from a specific outlaw type associated with a regional lair:
1. **Steppe Bandits** (`pt_steppe_bandits`) -> **Steppe Bandit Lair** (`pt_steppe_bandit_lair`) -> Khergit region
2. **Tundra Bandits** (`pt_taiga_bandits`) -> **Tundra Bandit Lair** (`pt_taiga_bandit_lair`) -> Vaegir region
3. **Desert Bandits** (`pt_desert_bandits`) -> **Desert Bandit Lair** (`pt_desert_bandit_lair`) -> Sarranid region
4. **Forest Bandits** (`pt_forest_bandits`) -> **Forest Bandit Camp** (`pt_forest_camp_lair`) -> Swadian region
5. **Mountain Bandits** (`pt_mountain_bandits`) -> **Mountain Bandit Hideout** (`pt_mountain_bandit_lair`) -> Rhodok region
6. **Sea Raiders** (`pt_sea_raiders`) -> **Sea Raider Landing** (`pt_sea_raider_lair`) -> Nord region

**Behaviors:**
- **Lairs:** Lairs generate loot and act as spawners. If players defeat one, they earn substantial loot. If the player is defeated, the lair "relocates" (removed and spawned somewhere else in the region).
- **Lair Cooldowns:** A successfully defeated lair is set on a **72-hour** cooldown before it can spawn again. A non-defeated lair (where the player lost and it relocated) is set on a **24-hour** cooldown.
- **Trickle Spawning:** Daily triggers run to spawn new patrol parties. Spawning is set to a 24-hour cycle rhythm (`slot_party_template_respawn_cooldown`). If the lair is alive, patrols spawn directly on top of the lair. If the lair is down, patrols spawn at the regional spawn point inside a predefined radius (and receive a party size debuff).
- **Initialization:** At the first game start (`game_start.py`), all 6 lairs are spawned around their spawn points, and initial roaming bandits are generated directly at the same coordinates (on top of the newly generated lairs).

---

## 2. Lair Positioning Mechanics (Optimized)

### A. Explicit Hardcoded Coordinate Buffers
- **Predefined Coordinate Arrays:** To solve critical performance issues with native Warband lair placement, **5 explicitly valid coordinate coordinates** are stored for each regional lair type in `spawn_bandits`. 
- **The Native Placement Issue (Optimized out):** Originally, the engine used a randomized script that spawned a lair, ran validity checks (checking map terrain, sea bounds, obstacle collisions), and repeatedly deleted/respawned the camp if it was invalid. This native approach was highly inefficient and caused the intended 3-day (72 hours) respawn cycle to drag out to **10+ days** due to constant validation failures and retries.
- **Relocation/Spawn Logic:** The system now randomly selects one of the 5 pre-verified coordinates (`store_random_in_range, ":rand_sp", 0, 5`) and immediately updates the lair position without any expensive collision loops.

---

## 3. Lair Discovery, Reveal, and Debugging

### A. Lair Visibility Design (Intentional Gameplay Mechanics)
- **Lairs are Hidden on Purpose:** When spawned (at game start or during respawn cycles), lairs are flagged with `pf_disabled`. This makes them invisible and non-interactive on the world map.
- **Spotting/Discovery Mechanism:** To discover a lair, the player must walk near its coordinates. Every hour, a simple trigger computes the player party's spotting skill range. If the distance from the player to the hidden lair is less than the computed range, the lair's flags are updated to make it permanently visible:
  - `(party_set_flags, ":bandit_camp", pf_disabled, 0)`
  - `(party_set_flags, ":bandit_camp", pf_always_visible, 1)`
- **Following Bandits:** Since patrols spawn directly at the lair when it is alive, players can observe the movement patterns of roaming bandit parties heading back to their base to locate the hidden lair.

### B. Cheat & Debug Actions
To assist with debugging, several development actions are integrated:
- **Reveal Hideouts Action:** A normal camp option `camp_reveal_hideouts` ("Reveal all bandit hideouts on map.") is available to forcefully strip `pf_disabled` and set `pf_always_visible` on all active lairs.
- **Bandits Diagnostics Report:** The spawn diagnostics screen displays current roaming counts, caps, and remaining cooldowns for both patrols and lair respawns.
- **Cheat World Menu Actions:** Under the world cheat menu (`mnu_camp_cheat_world`), developers have access to:
  - **Force Daily Bandit Spawn:** Triggers `script_spawn_bandits` immediately.
  - **Clear Roaming Bandits:** Removes all roaming outlaws from the map and resets spawn timers to 0.
  - **Clear Bandit Lairs:** Removes all active lairs from the map and resets template slots (`slot_party_template_lair_party`, `slot_party_template_lair_next_spawn`, `slot_party_template_respawn_cooldown`) to 0, enabling immediate respawning.

---

## 4. Slots & State Persistence

All state is persisted on the **roaming bandit templates** (e.g., `pt_steppe_bandits`, `pt_taiga_bandits`, etc.), NOT the lair templates themselves.

| Slot Name | Target | Purpose | Initial Value / Default |
| :--- | :--- | :--- | :--- |
| `slot_party_template_lair_type` | Bandit Template | Holds the corresponding lair party template (e.g., `pt_steppe_bandit_lair`) | Assigned dynamically in `spawn_bandits` |
| `slot_party_template_lair_spawnpoint` | Bandit Template | Spawnpoint party on the map to anchor lair spawns (e.g., `p_steppe_bandit_spawn_point`) | Assigned dynamically in `spawn_bandits` |
| `slot_party_template_lair_party` | Bandit Template | Holds the **active party ID** of the lair on the map. If `0` or `1`, no lair is currently active. | Starts at `0` |
| `slot_party_template_lair_next_spawn` | Bandit Template | Timestamp (in current game hours) when the lair is allowed to try spawning again. | Starts at `0` |
| `slot_party_template_respawn_cooldown` | Bandit Template | Timestamp (in current game hours) when the next patrol party is allowed to spawn (trickle limit). | Starts at `0` |

---

## 5. Other Outlaws & Factions

### B. Sea Bandit Ships (Water Outlaws)
- **Templates:** `pt_sea_raiders_ship`, `pt_corsair_ship`, `pt_pirate_ship`
- **Behaviors:** Independent sea-based raiders. They are **not attached to any faction or lair**.
- **Spawning:** Spawned via `spawn_bandits` near reserved ports/markers (`p_reserved_1`, `p_reserved_2`, `p_reserved_3`). They do not respect a standard daily trickle cooldown (the script passes `0` as the cooldown to attempt to fill them to their cap `num_max_pirate_ships` of 5 per ship type).

### C. Looters (General Low-Tier Outlaws)
- **Template:** `pt_looters`
- **Behaviors:** Weakest roaming outlaws, **not attached to any lair**.
- **Spawning:** Spawned dynamically in `spawn_bandits` near villages (`villages_begin` to `villages_end`) up to a maximum cap of `num_max_looters = 50`. Also spawned initially around randomly selected villages (1/5 probability) at game start.

### D. Deserters (Faction Runaways)
- **Template:** `pt_deserters`
- **Behaviors:** Composed of troops that fled kingdom armies. They inherit faction troops and icons of the faction they deserted from.
- **Spawning:** Spawns are checked dynamically in `spawn_bandits.py` (capped at 15 parties max). They desert from active kingdom lords (`slot_troop_occupation = slto_kingdom_hero`) who are in the wilderness (not in town). There is a 5% chance per lord for deserters to spawn around their army, copying their kingdom's troop type (spawning tier 1 troops scaled by player level, and automatically upgrading them using a random XP pool). Their map icon changes based on the source faction.

### E. Manhunters (Outlaw Hunters)
- **Template:** `pt_manhunters`
- **Behaviors:** A neutral faction whose sole purpose is to hunt outlaw parties, rescuing prisoners and keeping bandit populations under control.
- **Spawning:** Spawns are dynamically updated in `spawn_bandits` up to a fixed cap of `num_max_manhunters = 36`. They are spawned around random regional bandit spawn points to maximize coverage and intercept roaming patrols.

---

## 6. Known Bugs & Solution Design

These issues have been identified and are slated for correction in the implementation plan:

1. **Stale Cooldown reading in reports (`get_spawn_report_line.py`):**
   - *Problem:* The report script checks `lair_party > 1` (lair active) before reading the lair's next spawn timer. When the lair is DOWN, this condition fails, leaving the cooldown read at `0` (which outputs "ready").
   - *Solution:* Read the `slot_party_template_lair_next_spawn` slot regardless of lair active status.

2. **Sea Raider Invalid Party ID 374 (`spawn_bandits.py` & `spawn_party_type_with_cooldown.py`):**
   - *Problem:* Sea Raiders pass `num_sea_raider_spawn_points = 2` as a parameter. When spawning near the lair, the script still applies this offset to the lair's party ID, producing `lair_party_id + 1` (which is often an invalid party).
   - *Solution:* Ensure `num_spawn_points = 1` is enforced when spawning patrol groups from an active lair. Add safety checks to skip spawning if the resolved party ID is inactive.

3. **Failed Patrol Spawns blocking future spawns (`spawn_party_type_with_cooldown.py`):**
   - *Problem:* The cooldown-setting logic is executed even if `spawn_around_party` fails due to an invalid party ID, locking out spawns for another 24 hours.
   - *Solution:* Nest the cooldown reset within the success condition of the spawn operation.
