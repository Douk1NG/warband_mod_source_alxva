# Civilian Clothes in Castle Courts

Entering a castle court temporarily switches the player to civilian body clothing.

## source/scripts/misc/misc_scripts.py
- Applied when entering `mt_visit_town_castle`, player entry 0
- Uses `af_override_all` for temporary override
- Equipment priority: currently equipped civilian body → first civilian body in inventory → `itm_tabard` fallback
- Mission-entry override only — does not change real inventory or equipped armor
