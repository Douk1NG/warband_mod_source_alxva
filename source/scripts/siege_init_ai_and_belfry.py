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

siege_init_ai_and_belfry_scripts = [
("siege_init_ai_and_belfry",
   [(assign, "$cur_belfry_pos", 50),
    (assign, ":cur_belfry_object_pos", slot_scene_belfry_props_begin),
    (store_current_scene, ":cur_scene"),
    #Collecting belfry objects
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_a", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_a", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_b", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (assign, "$belfry_rotating_objects_begin", ":cur_belfry_object_pos"),
    (try_for_range, ":i_belfry_instance", 0, 5),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_wheel", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (assign, "$last_belfry_object_pos", ":cur_belfry_object_pos"),

    #Lifting up the platform  at the beginning
    (try_begin),
      (scene_prop_get_instance, ":belfry_object_to_rotate", "spr_belfry_platform_a", 0),
    (try_end),

    #Moving the belfry objects to their starting position
    (entry_point_get_position,pos1,55),
    (entry_point_get_position,pos3,50),
    (try_for_range, ":i_belfry_object_pos", slot_scene_belfry_props_begin, "$last_belfry_object_pos"),
      (assign, ":pos_no", pos_belfry_begin),
      (val_add, ":pos_no", ":i_belfry_object_pos"),
      (val_sub, ":pos_no", slot_scene_belfry_props_begin),
      (scene_get_slot, ":cur_belfry_object", ":cur_scene", ":i_belfry_object_pos"),
      (prop_instance_get_position, pos2, ":cur_belfry_object"),
      (try_begin),
        (eq, ":cur_belfry_object", ":belfry_object_to_rotate"),
        (position_rotate_x, pos2, 90),
      (try_end),
      (position_transform_position_to_local, ":pos_no", pos1, pos2),
      (position_transform_position_to_parent, pos4, pos3, ":pos_no"),
      (prop_instance_animate_to_position, ":cur_belfry_object", pos4, 1),
    (try_end),
    (assign, "$belfry_positioned", 0),
    (assign, "$belfry_num_slots_positioned", 0),
    (assign, "$belfry_num_men_pushing", 0),

    (set_show_messages, 0),
    (team_give_order, "$attacker_team", grc_everyone, mordr_stand_ground),
    (team_give_order, "$attacker_team_2", grc_everyone, mordr_stand_ground),
    (set_show_messages, 1),
  ])
]
