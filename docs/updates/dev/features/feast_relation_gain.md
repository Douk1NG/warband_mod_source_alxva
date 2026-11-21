# Feast Relation Gain

While hosting a feast, resting in the feast center improves relation with attending lords once per day.

## source/module_triggers.py
- Checks once per hour while resting inside the active player feast center
- Requires feast quality at least 20 (`script_internal_politics_rate_feast_to_s9`)
- Throttled by `slot_troop_last_talk_time` (24h cooldown per lord)
- Relation gain: +1 per eligible lord per day
