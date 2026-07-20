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

multiplayer_initialize_belfry_wheel_rotations_scripts = [
#script_multiplayer_initialize_belfry_wheel_rotations
# Input: none
# Output: none
("multiplayer_initialize_belfry_wheel_rotations",
   [
##    (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_a"),
##    (try_for_range, ":belfry_no", 0, ":num_belfries"),
##      (store_mul, ":wheel_no", ":belfry_no", 3),
##      (scene_prop_get_instance, ":belfry_wheel_1_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_1_scene_prop_id"),
##      #belfry wheel_2
##      (val_add, ":wheel_no", 1),
##      (scene_prop_get_instance, ":belfry_wheel_2_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_2_scene_prop_id"),
##      #belfry wheel_3
##      (val_add, ":wheel_no", 1),
##      (scene_prop_get_instance, ":belfry_wheel_3_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_3_scene_prop_id"),
##    (try_end),
##
##    (scene_prop_get_num_instances, ":num_belfries_a", "spr_belfry_a"),
##
##    (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_b"),
##    (try_for_range, ":belfry_no", 0, ":num_belfries"),
##      (store_add, ":wheel_no_plus_num_belfries_a", ":wheel_no", ":num_belfries_a"),
##      (store_mul, ":wheel_no_plus_num_belfries_a", ":belfry_no", 3),
##      (scene_prop_get_instance, ":belfry_wheel_1_scene_prop_id", "spr_belfry_wheel", ":wheel_no_plus_num_belfries_a"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_1_scene_prop_id"),
##      #belfry wheel_2
##      (val_add, ":wheel_no_plus_num_belfries_a", 1),
##      (scene_prop_get_instance, ":belfry_wheel_2_scene_prop_id", "spr_belfry_wheel", ":wheel_no_plus_num_belfries_a"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_2_scene_prop_id"),
##      #belfry wheel_3
##      (val_add, ":wheel_no_plus_num_belfries_a", 1),
##      (scene_prop_get_instance, ":belfry_wheel_3_scene_prop_id", "spr_belfry_wheel", ":wheel_no_plus_num_belfries_a"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_3_scene_prop_id"),
##    (try_end),

      (scene_prop_get_num_instances, ":num_wheel", "spr_belfry_wheel"),
      (try_for_range, ":wheel_no", 0, ":num_wheel"),
        (scene_prop_get_instance, ":wheel_id", "spr_belfry_wheel", ":wheel_no"),
        (prop_instance_initialize_rotation_angles, ":wheel_id"),
      (try_end),

      (scene_prop_get_num_instances, ":num_winch", "spr_winch"),
      (try_for_range, ":winch_no", 0, ":num_winch"),
        (scene_prop_get_instance, ":winch_id", "spr_winch", ":winch_no"),
        (prop_instance_initialize_rotation_angles, ":winch_id"),
      (try_end),

      (scene_prop_get_num_instances, ":num_winch_b", "spr_winch_b"),
      (try_for_range, ":winch_b_no", 0, ":num_winch_b"),
        (scene_prop_get_instance, ":winch_b_id", "spr_winch_b", ":winch_b_no"),
        (prop_instance_initialize_rotation_angles, ":winch_b_id"),
      (try_end),
     ])
]
