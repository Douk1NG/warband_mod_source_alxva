# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

multiplayer_get_item_value_for_troop_scripts = [
#script_multiplayer_get_item_value_for_troop
# Input: arg1 = item_no, arg2 = troop_no
# Output: reg0: item_value
("multiplayer_get_item_value_for_troop",
   [
     (store_script_param, ":item_no", 1),
     (store_script_param, ":troop_no", 2),
     (try_begin),
       (call_script, "script_cf_multiplayer_is_item_default_for_troop", ":item_no", ":troop_no"),
       (assign, ":item_value", 0),
     (else_try),
       (store_item_value, ":item_value", ":item_no"),
       (store_troop_faction, ":faction_no", ":troop_no"),
       (store_sub, ":faction_slot", ":faction_no", npc_kingdoms_begin),
       (val_add, ":faction_slot", slot_item_multiplayer_faction_price_multipliers_begin),
       (item_get_slot, ":price_multiplier", ":item_no", ":faction_slot"),
       (val_mul, ":item_value", ":price_multiplier"),
       (val_div, ":item_value", 100),
     (try_end),
     (assign, reg0, ":item_value"),
     ])
]
