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

game_get_use_string_scripts = [
#script_game_get_use_string
# This script is called from the game engine for getting using information text
# INPUT: used_scene_prop_id
# OUTPUT: s0
("game_get_use_string",
   [
     (store_script_param, ":instance_id", 1),

     (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),

     (try_begin),
       (this_or_next|eq, ":scene_prop_id", "spr_winch_b"),
       (eq, ":scene_prop_id", "spr_winch"),
       (assign, ":effected_object", "spr_portcullis"),
     (else_try),
       (this_or_next|eq, ":scene_prop_id", "spr_door_destructible"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_b"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_6m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_8m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_10m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_12m"),
       (eq, ":scene_prop_id", "spr_siege_ladder_move_14m"),
       (assign, ":effected_object", ":scene_prop_id"),
     (try_end),

     (scene_prop_get_slot, ":item_situation", ":instance_id", scene_prop_open_or_close_slot),

     (try_begin), #opening/closing portcullis
       (eq, ":effected_object", "spr_portcullis"),

       (try_begin),
         (eq, ":item_situation", 0),
         (str_store_string, s0, "str_open_gate"),
       (else_try),
         (str_store_string, s0, "str_close_gate"),
       (try_end),
     (else_try), #opening/closing door
       (this_or_next|eq, ":effected_object", "spr_door_destructible"),
       (this_or_next|eq, ":effected_object", "spr_castle_f_door_b"),
       (this_or_next|eq, ":effected_object", "spr_castle_e_sally_door_a"),
       (this_or_next|eq, ":effected_object", "spr_castle_f_sally_door_a"),
       (this_or_next|eq, ":effected_object", "spr_earth_sally_gate_left"),
       (this_or_next|eq, ":effected_object", "spr_earth_sally_gate_right"),
       (this_or_next|eq, ":effected_object", "spr_viking_keep_destroy_sally_door_left"),
       (this_or_next|eq, ":effected_object", "spr_viking_keep_destroy_sally_door_right"),
       (eq, ":effected_object", "spr_castle_f_door_a"),

       (try_begin),
         (eq, ":item_situation", 0),
         (str_store_string, s0, "str_open_door"),
       (else_try),
         (str_store_string, s0, "str_close_door"),
       (try_end),
     (else_try), #raising/dropping ladder
       (try_begin),
         (eq, ":item_situation", 0),
         (str_store_string, s0, "str_raise_ladder"),
       (else_try),
         (str_store_string, s0, "str_drop_ladder"),
       (try_end),
     (try_end),
   ])
]
