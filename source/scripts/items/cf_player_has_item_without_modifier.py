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

cf_player_has_item_without_modifier_scripts = [
("cf_player_has_item_without_modifier",
    [
      (store_script_param, ":item_id", 1),
      (store_script_param, ":modifier", 2),
      (player_has_item, ":item_id"),
      #checking if any of the meat is not rotten
      (assign, ":has_without_modifier", 0),
      (troop_get_inventory_capacity, ":inv_size", "trp_player"),
      (try_for_range, ":i_slot", 0, ":inv_size"),
        (troop_get_inventory_slot, ":cur_item", "trp_player", ":i_slot"),
        (eq, ":cur_item", ":item_id"),
        (troop_get_inventory_slot_modifier, ":cur_modifier", "trp_player", ":i_slot"),
        (neq, ":cur_modifier", ":modifier"),
        (assign, ":has_without_modifier", 1),
        (assign, ":inv_size", 0), #break
      (try_end),
      (eq, ":has_without_modifier", 1),
  ])
]
