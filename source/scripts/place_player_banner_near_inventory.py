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

place_player_banner_near_inventory_scripts = [
##  #script_shield_item_set_banner
# Input: none
# Output: none
("place_player_banner_near_inventory",
    [
    	#normal_banner_begin
    	(troop_get_slot, ":troop_banner_object", "trp_player", slot_troop_banner_scene_prop),
    	#custom_banner_begin
    	(troop_get_slot, ":flag_spr", "trp_player", slot_troop_custom_banner_flag_type),

     (try_begin),
       (assign, ":flag_object", -1),
       (try_begin),
    	#normal_banner_begin
           (gt, ":troop_banner_object", 0),
           (scene_prop_get_instance, ":flag_object", ":troop_banner_object", 0),
    	#custom_banner_begin
       (else_try),
           (eq, ":troop_banner_object", -1),
           (ge, ":flag_spr", 0),
           (val_add, ":flag_spr", custom_banner_flag_scene_props_begin),
           (scene_prop_get_instance, ":flag_object", ":flag_spr", 0),
       (try_end),
       (try_begin),
         (ge, ":flag_object", 0),
         (get_player_agent_no, ":player_agent"),
         (agent_get_look_position, pos1, ":player_agent"),
         (position_move_y, pos1, -500),
         (position_rotate_z, pos1, 180),
         (position_set_z_to_ground_level, pos1),
         (position_move_z, pos1, 300),
         (prop_instance_set_position, ":flag_object", pos1),
       (try_end),
       (scene_prop_get_instance, ":pole_object", "spr_banner_pole", 0),
       (try_begin),
         (ge, ":pole_object", 0),
         (position_move_z, pos1, -320),
         (prop_instance_set_position, ":pole_object", pos1),
       (try_end),
     (else_try),
       (init_position, pos1),
       (position_move_z, pos1, -1000000),
       (scene_prop_get_instance, ":flag_object", banner_scene_props_begin, 0),
       (try_begin),
         (ge, ":flag_object", 0),
         (prop_instance_set_position, ":flag_object", pos1),
       (try_end),
       (scene_prop_get_instance, ":pole_object", "spr_banner_pole", 0),
       (try_begin),
         (ge, ":pole_object", 0),
         (prop_instance_set_position, ":pole_object", pos1),
       (try_end),
     (try_end),
     ])
]
