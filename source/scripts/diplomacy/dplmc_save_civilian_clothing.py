# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_save_civilian_clothing_scripts = [
# "script_dplmc_get_closest_center_or_two"
#"script_dplmc_save_civilian_clothing"
##Save civilian clothing so it will still appear later
#
#INPUT: troop number
#OUTPUT: none
("dplmc_save_civilian_clothing", [
     (store_script_param, ":troop_no", 1),
     #SB : this interferes with auto-loot
     (try_begin),
        (gt, ":troop_no", 0),#deliberately exclude player
        (troop_is_hero, ":troop_no"),#only applies to unique characters
        (try_for_range, ":dest_slot", dplmc_ek_alt_items_begin, min(dplmc_ek_alt_items_end, dplmc_ek_alt_items_begin + 4)),
           (store_add, ":source_slot", ":dest_slot", ek_head - dplmc_ek_alt_items_begin),
           (troop_get_inventory_slot, ":item_id", ":troop_no", ":dest_slot"),
           (lt, ":item_id", 1),#do not overwrite an existing item in the destination slot
           (troop_get_inventory_slot, ":item_id", ":troop_no", ":source_slot"),
           (troop_set_inventory_slot, ":troop_no", ":dest_slot", ":item_id"),
        (try_end),
     (try_end),
   ])
]
