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

dplmc_get_current_item_for_autoloot_scripts = [
##diplomacy end+
("dplmc_get_current_item_for_autoloot",
  [
    (store_script_param_1, ":slot_no"),

    #(try_begin),
      (assign, ":dest_slot", ":slot_no"),
      (troop_get_inventory_slot, ":item", "$temp", ":dest_slot"),
    #(else_try),
    #  (store_sub, ":dest_slot", "$temp", companions_begin),
    #  (val_mul, ":dest_slot", 4),
    #  (val_add, ":dest_slot", 10),
    #  (val_add, ":dest_slot", ":slot_no"),
    #  (troop_get_inventory_slot, ":item", "trp_merchants_end", ":dest_slot"),
    #(try_end),
    (try_begin),
      (ge, ":item", 0),
      (str_store_item_name, s10, ":item"),
    (else_try),
      (str_store_string, s10, "str_dplmc_none"),
    (try_end),
  ])
]
