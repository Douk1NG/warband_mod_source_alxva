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

place_player_banner_near_inventory_bms_scripts = [
# script_place_player_banner_near_inventory_bms
# Input: none
# Output: none
("place_player_banner_near_inventory_bms",
    [
    	    	#normal_banner_begin
    	(troop_get_slot, ":troop_banner_object", "trp_player", slot_troop_banner_scene_prop),
    	    	#custom_banner_begin
      (troop_get_slot, ":flag_spr", "trp_player", slot_troop_custom_banner_flag_type),
     (try_begin),
       (try_begin),
    	    	#normal_banner_begin
           (gt, ":troop_banner_object", 0),
           (replace_scene_props, banner_scene_props_begin, ":troop_banner_object"),
       (else_try),
    	    	#custom_banner_begin
           (eq, ":troop_banner_object", -1),
           (ge, ":flag_spr", 0),
           (val_add, ":flag_spr", custom_banner_flag_scene_props_begin),
           (replace_scene_props, banner_scene_props_begin, ":flag_spr"),
       (try_end),
     (try_end),
     ])
]
