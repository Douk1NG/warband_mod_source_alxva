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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

initialize_all_scene_prop_slots_scripts = [
#script_initialize_all_scene_prop_slots
# INPUT: arg1 = scene_prop_no
# OUTPUT: none
("initialize_all_scene_prop_slots",
   [
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_6m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_8m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_10m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_12m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_14m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_castle_e_sally_door_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_castle_f_sally_door_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_earth_sally_gate_left"),
     (call_script, "script_initialize_scene_prop_slots", "spr_earth_sally_gate_right"),
     (call_script, "script_initialize_scene_prop_slots", "spr_viking_keep_destroy_sally_door_left"),
     (call_script, "script_initialize_scene_prop_slots", "spr_viking_keep_destroy_sally_door_right"),
     (call_script, "script_initialize_scene_prop_slots", "spr_castle_f_door_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_belfry_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_belfry_b"),
     (call_script, "script_initialize_scene_prop_slots", "spr_winch_b"),
    ])
]
