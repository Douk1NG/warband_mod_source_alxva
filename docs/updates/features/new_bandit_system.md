# New Bandit System

Overhauled bandit, pirate, manhunter, and deserter systems with capped populations, trickle respawn, lair mechanics, and hardcoded coordinate placement.

## Population Caps

| Type | Parties | Troops/Party | Notes |
|------|---------|-------------|-------|
| 6 land bandit types | 18 per type | 50 (20 when lair down) | 24h trickle respawn |
| Looters | unlimited | 50 | Spawn near villages |
| Pirate ships (3 types) | 5 per type | 20 | Water spawn point fix |
| Manhunters | 24 | 10-15 manhunters, 10-15 slave drivers, 5-10 slave hunters, 4-9 slave crushers | Fill every cycle |
| Deserters | unlimited | 50 | Spawn from roaming lords |
| Dark Hunters / Black Khergits | 4 each | — | Legacy toggle (`$g_dark_hunters_enabled`) |

## Trickle Respawn

`spawn_party_type_with_cooldown` handles all bandit/patrol spawning:
- **Seed**: if cooldown slot is 0 (never spawned), fill straight to cap
- **Trickle**: after seed, 1 party per 24h per type (`bandit_respawn_interval_hours`)
- Lair-alive branch: spawns directly at the lair party (radius 0)
- Lair-dead branch: spawns at regional spawn point, applies size debuff

## Lair System

### Hidden on Map
Lairs spawn with `pf_disabled` (invisible, non-interactive). Players discover them by proximity — a trigger checks spotting skill range every hour. Once within range, the lair gets `pf_always_visible` permanently.

Players can also follow roaming bandit patrols back to their base.

### Spawn/Respawn
- **Hardcoded coordinates**: 5 positions per lair type (30 total). Chosen randomly via `store_random_in_range(0,5)`.
- **Why**: The native approach spawned a camp and ran expensive terrain-collision loops (sea bounds, obstacles, elevation) that caused 10+ day respawn delays. Hardcoded coords eliminated this entirely.
- **Overlap audit**: 12 coordinates were within 6 units of a town/castle/village center. All moved to ≥ 8 units.

### Defeat / Loss
- **Player wins** → lair removed, 72h cooldown (`bandit_lair_respawn_hours`), loot screen shown
- **Player loses** → lair slot cleared, 24h cooldown, lair respawns at a new coordinate
- During cooldown: lair-down debuff applies (parties capped at 20 troops)

## Manhunters

- **Cap**: 24 parties, fill to cap every daily cycle
- **Spawning**: random regional bandit spawn points (6 types, uniform random)
- **Composition**: `(trp_slaver_chief,1,1)`, `(trp_manhunter,10,15)`, `(trp_slave_driver,10,15)`, `(trp_slave_hunter,5,10)`, `(trp_slave_crusher,4,9)`
- **Speed bonus**: doubled (`val_mul, speed, 2`) only when in `ai_bhvr_attack_party` mode
- **Buy prisoners**: dialog option with any manhunter party that has prisoners. Price = sum of (level + 10)² / 6 per prisoner stack. Transfers all non-hero prisoners to player, deducts gold.

## Pirate Ships

3 types: Sea Raiders Ship, Corsair Ship, Pirate Ship. Each capped at 5 parties, 20 troops each.
- Spawned at reserved anchors (`p_reserved_1/2/3`) with water-position fix (`map_get_water_position_around_position`)
- Slot `slot_party_ship_type` marks type (1/2/4)
- Merchant ships (8 parties max) travel port-to-port independently

## Looters

Spawn near villages (`villages_begin` to `villages_end`) via cooldown system. No party cap (parameter passed to cooldown script is effectively unlimited). Quest-tagged for `qst_deal_with_looters`.

## Deserters

- **Spawn**: 5% chance per wandering kingdom lord per cycle
- **Composition**: faction tier-1 troops scaled by player level (level × 2 + 11), then auto-upgraded 1-3 times
- **Icon**: matches source faction (`icon_kingdom_X_soldier_a`)
- **Recruitment**: free recruit option requires `dplmc_deserter_recruit_renown` (500) + strength ratio > 100

## Cheat Menu (Reports)

Bandit/pirate diagnostics moved to **Reports → Cheat Reports** (requires cheat mode), available via `reports_cheat` → `cheat_spawn_diagnostics`. Shows:
- Active patrols / cap per type
- Patrol cooldown remaining
- Lair status (UP / DOWN)
- Lair respawn cooldown
- Pirate ship raw cooldown slot values

Additional world cheat menu actions: Clear roaming bandits, Remove all ships, Show bandit lairs
