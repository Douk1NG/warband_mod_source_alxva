# Autosell Changes

## Direct Liquidation

Merchant autosell liquidates items directly from player inventory instead of transferring to merchant inventory.

## source/scripts/dplmc_auto_sell.py (029c931)
- Removed merchant gold and merchant free-space requirements from both quote calculation and sale execution
- Center autosell (cleanup mode): skips backup-equipment protection, starts from first inventory slot after equipped items and food slot
- Price limits, item range, rotten-food exception, book/trade-good exclusions, lordly-item protection unchanged
- Merchant-dialog autosell still uses personal-equipment safety checks
- Autotrade buying remains merchant-based

## Ignores Locked Item Slots

Autosell skips inventory slots that have the lock flag set, leaving those items untouched.

## source/scripts/dplmc_auto_sell.py (520f27f)
- Added `(troop_slot_eq, "trp_temp_array_lock", ":i_slot", 0)` check — locked slots are not sold
