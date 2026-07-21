# Update 011 — Features Tracking (features_tracking.md port)

## Summary

Porting features from 1175 and Custom Commander references, plus internal fixes. Implemented one-by-one with testing between each.

---

## Implementation Log

| # | Feature | Status | Notes |
|---|---------|--------|-------|
| 1.1 | Enable manhunter → slave_driver upgrade | DONE | Uncommented module_troops.py:2760 |
| 1.2 | Remove "View the world map" report | DONE | Deleted option from mnu_reports.py |
| 1.3 | Remove all ships cheat (1175) | DONE | Added to mnu_camp_cheat.py |
| 1.4 | Autosell respects inventory lock | DONE | Added lock check to dplmc_auto_sell.py |
| 1.5 | Recruit lords → right to rule | DONE | +3 for kings/pretenders (minister dialog), +1 for lords/companions in module_dialogs.py |
| 1.6 | TPE cheat autowin | DONE | Added to tpe_town_tournament menu |
| 2.1 | CC relations report presentation | PENDING | New presentation, add alongside existing |
| 2.2 | CC faction color editor | PENDING | New presentation, add alongside existing |
| 2.3 | Combined morale + size report | PENDING | New presentation from CC |
| 2.4 | Equip all NPC presentation | PENDING | Major port from CC |
| 2.5 | All items + troop tree bugfix | PENDING | Last task |
| 3.1 | ~~Fix inventory dark mesh~~ | DONE | User removed the .dds texture |
| 3.2 | Fief granting relation bug | PENDING | give_center_to_lord.py investigation |
| 3.3 | Inventory presentation overhaul | PENDING | Port from 1175 |
| 3.4 | Copy new locations from CC | PENDING | Defer (massive) |

---

## Detailed Changes Per Feature

### 1.1 Enable manhunter → slave_driver upgrade
- **File:** `source/module_troops.py:2760`
- **Change:** Uncomment `upgrade(troops,"manhunter","slave_driver")`
