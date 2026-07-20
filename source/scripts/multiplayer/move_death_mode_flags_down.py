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

move_death_mode_flags_down_scripts = [
("move_death_mode_flags_down",
   [
     (try_begin),
       (scene_prop_get_instance, ":pole_1_id", "spr_headquarters_pole_code_only", 0),
       (prop_instance_get_position, pos0, ":pole_1_id"),
       (position_move_z, pos0, -2000),
       (prop_instance_set_position, ":pole_1_id", pos0),
     (try_end),

     (try_begin),
       (scene_prop_get_instance, ":pole_2_id", "spr_headquarters_pole_code_only", 1),
       (prop_instance_get_position, pos1, ":pole_2_id"),
       (position_move_z, pos1, -2000),
       (prop_instance_set_position, ":pole_2_id", pos1),
     (try_end),

     (try_begin),
       (scene_prop_get_instance, ":pole_1_id", "spr_headquarters_pole_code_only", 0),
       (prop_instance_get_position, pos0, ":pole_1_id"),
       (scene_prop_get_instance, ":flag_1_id", "$team_1_flag_scene_prop", 0),
       (prop_instance_stop_animating, ":flag_1_id"),
       (position_move_z, pos0, multi_headquarters_flag_initial_height),
       (prop_instance_set_position, ":flag_1_id", pos0),
     (try_end),

     (try_begin),
       (scene_prop_get_instance, ":pole_2_id", "spr_headquarters_pole_code_only", 1),
       (prop_instance_get_position, pos1, ":pole_2_id"),
       (scene_prop_get_instance, ":flag_2_id", "$team_2_flag_scene_prop", 0),
       (prop_instance_stop_animating, ":flag_2_id"),
       (position_move_z, pos1, multi_headquarters_flag_initial_height),
       (prop_instance_set_position, ":flag_2_id", pos1),
     (try_end),
   ])
]
