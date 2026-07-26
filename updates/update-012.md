# Update 012 — Auto Upgrade Troops

## Summary

New feature: automatic troop upgrading based on configurable mode. Troops upgrade immediately after battles, training, and at midnight as backup.

---

## Feature

Configurable auto-upgrade for `p_main_party` troops via XGM mod options.

### Modes

| Value | Mode | Behavior |
|-------|------|----------|
| 0 | Off | Disabled |
| 1 | Balanced | Split each stack evenly between available upgrade paths |
| 2 | Infantry | Upgrade to infantry path, fallback to first path |
| 3 | Archers | Upgrade to archer path, fallback to first path |
| 4 | Cavalry | Upgrade to cavalry path, fallback to first path |

### Behavior

- Only upgrades troops that have enough XP (`party_stack_get_num_upgradeable`)
- Deducts gold from player personal gold (not treasury)
- Preserves wounded troops (not upgraded, re-wounded after swap)
- Uses forced swap (remove all stack → add back kept + upgraded) to clear XP pool and prevent phantom "ready to upgrade" flags

### Trigger Points

| Trigger | Location | When |
|---------|----------|------|
| Field battle victory | `mnu_total_victory.py:348` | After `party_give_xp_and_gold` |
| Siege assault victory | `mnu_besiegers_camp_with_allies.py:110` | After `party_give_xp_and_gold` |
| Training ground | `mnu_training_ground_training_result.py:91` | After all 3 training XP calls |
| Midnight backup | `module_simple_triggers.py:314` | Hour 0, every game day |

---

## Files Created

- `source/scripts/auto_upgrade_troops.py` — Core script with 5 modes, gold check, XP-based upgradeability, forced swap

## Files Edited

- `source/variables.txt` — Added `g_auto_upgrade_mode` at line 1302
- `source/module_scripts.py` — Added import + extend for `auto_upgrade_troops_scripts`
- `source/module_simple_triggers.py` — Added separate `(1,` hourly trigger at midnight (hour 0)
- `source/game_menus/mnu_total_victory.py` — Added `script_auto_upgrade_troops` call after XP grant
- `source/game_menus/mnu_besiegers_camp_with_allies.py` — Added `script_auto_upgrade_troops` call after XP grant
- `source/game_menus/mnu_training_ground_training_result.py` — Added `script_auto_upgrade_troops` call after training XP
- `modmerger/mods/xgm_mod_options/xgm_mod_options.py` — Added combolabel for 5 modes

---

## Notes

- The forced swap approach (remove all + add back) was necessary because `party_remove_members` does not scale XP proportionally when removing troops from a stack, causing phantom upgrade flags on remaining troops
- Reverse iteration was initially considered but `try_for_range_backwards` resolved stack index shifting during forward iteration
- `party_upgrade_with_xp` with 0 XP does not process existing stack XP — it only distributes the XP amount passed to it
- Engine-native party screen upgrade button is C++ code, not accessible from module scripts
- Behavior-affecting: new feature, no existing behavior changed
