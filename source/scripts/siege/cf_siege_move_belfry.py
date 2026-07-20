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

cf_siege_move_belfry_scripts = [
("cf_siege_move_belfry",
   [(neq, "$last_belfry_object_pos", slot_scene_belfry_props_begin),
    (entry_point_get_position,pos1,50),
    (entry_point_get_position,pos4,55),
    (get_distance_between_positions, ":total_distance", pos4, pos1),
    (store_current_scene, ":cur_scene"),
    (scene_get_slot, ":first_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
    (prop_instance_get_position, pos2, ":first_belfry_object"),
    (entry_point_get_position,pos1,"$cur_belfry_pos"),
    (position_transform_position_to_parent, pos3, pos1, pos_belfry_begin),
    (position_transform_position_to_parent, pos5, pos4, pos_belfry_begin),
    (get_distance_between_positions, ":cur_distance", pos2, pos3),
    (get_distance_between_positions, ":distance_left", pos2, pos5),
    (try_begin),
      (le, ":cur_distance", 10),
      (val_add, "$cur_belfry_pos", 1),
      (entry_point_get_position,pos1,"$cur_belfry_pos"),
      (position_transform_position_to_parent, pos3, pos1, pos_belfry_begin),
      (get_distance_between_positions, ":cur_distance", pos2, pos3),
    (try_end),
    (neq, "$cur_belfry_pos", 50),

    (assign, ":base_speed", 20),
    (store_div, ":slow_range", ":total_distance", 60),
    (store_sub, ":distance_moved", ":total_distance", ":distance_left"),

    (try_begin),
      (lt, ":distance_moved", ":slow_range"),
      (store_mul, ":base_speed", ":distance_moved", -60),
      (val_div, ":base_speed", ":slow_range"),
      (val_add, ":base_speed", 80),
    (else_try),
      (lt, ":distance_left", ":slow_range"),
      (store_mul, ":base_speed", ":distance_left", -60),
      (val_div, ":base_speed", ":slow_range"),
      (val_add, ":base_speed", 80),
    (try_end),
    (store_mul, ":belfry_speed", ":cur_distance", ":base_speed"),
    (try_begin),
      (eq, "$belfry_num_men_pushing", 0),
      (assign, ":belfry_speed", 1000000),
    (else_try),
      (val_div, ":belfry_speed", "$belfry_num_men_pushing"),
    (try_end),

    (try_begin),
      (le, "$cur_belfry_pos", 55),
      (init_position, pos3),
      (position_rotate_x, pos3, ":distance_moved"),
      (scene_get_slot, ":base_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
      (prop_instance_get_position, pos4, ":base_belfry_object"),
      (entry_point_get_position,pos1,"$cur_belfry_pos"),
      (try_for_range, ":i_belfry_object_pos", slot_scene_belfry_props_begin, "$last_belfry_object_pos"),
        (scene_get_slot, ":cur_belfry_object", ":cur_scene", ":i_belfry_object_pos"),
        (try_begin),
          (ge, ":i_belfry_object_pos", "$belfry_rotating_objects_begin"),
          (prop_instance_get_starting_position, pos5, ":base_belfry_object"),
          (prop_instance_get_starting_position, pos6, ":cur_belfry_object"),
          (position_transform_position_to_local, pos7, pos5, pos6),
          (position_transform_position_to_parent, pos5, pos4, pos7),
          (position_transform_position_to_parent, pos6, pos5, pos3),
          (prop_instance_set_position, ":cur_belfry_object", pos6),
        (else_try),
          (assign, ":pos_no", pos_belfry_begin),
          (val_add, ":pos_no", ":i_belfry_object_pos"),
          (val_sub, ":pos_no", slot_scene_belfry_props_begin),
          (position_transform_position_to_parent, pos2, pos1, ":pos_no"),
          (prop_instance_animate_to_position, ":cur_belfry_object", pos2, ":belfry_speed"),
        (try_end),
      (try_end),
    (try_end),
    (gt, "$cur_belfry_pos", 55),
    (assign, "$belfry_positioned", 1),
  ])
]
