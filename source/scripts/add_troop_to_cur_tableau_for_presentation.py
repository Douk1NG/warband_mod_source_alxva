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

add_troop_to_cur_tableau_for_presentation_scripts = [
("add_troop_to_cur_tableau_for_presentation",
    [
        (store_script_param, ":troop_no",1),

        (set_fixed_point_multiplier, 100),

        (cur_tableau_clear_override_items),

        (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),

        (init_position, pos5),
        (assign, ":cam_height", 105),
        #       (val_mod, ":camera_distance", 5),
        (assign, ":camera_distance", 380),
        (assign, ":camera_yaw", -15),
        (assign, ":camera_pitch", -18),
        #transient pose seeds
        (troop_get_xp, ":random_seed", ":troop_no"),
        (val_add, ":random_seed", ":troop_no"),
        (val_mod, ":random_seed", 5),
        (store_add, ":animation", "anim_pose_1", ":random_seed"),

        (position_set_z, pos5, ":cam_height"),

        # camera looks towards -z axis

        (position_rotate_x, pos5, -90),
        (position_rotate_z, pos5, 180),
        # now apply yaw and pitch
        (position_rotate_y, pos5, ":camera_yaw"),
        (position_rotate_x, pos5, ":camera_pitch"),
        (position_move_z, pos5, ":camera_distance", 0),
        (position_move_x, pos5, 5, 0),

        #honestly we can just draw this in the presentation
       # (troop_get_slot, ":banner", ":troop_no", slot_troop_banner_scene_prop),
       # (try_begin), #default slot val = 0, exclude placeholders since we don't want to touch their slots
         # (ge, ":banner", 0),
         # (is_between, ":troop_no", heroes_begin, heroes_end),
         # (init_position, pos2),
         # (val_sub, ":banner", banner_scene_props_begin),
         # (val_add, ":banner", banner_meshes_begin),
         # (position_set_x, pos2, -175),
         # (position_set_y, pos2, -300),
         # (position_set_z, pos2, 180),
         # (position_rotate_x, pos2, 90),
         # (position_rotate_y, pos2, -15),
         # (cur_tableau_add_mesh, ":banner", pos2, 0, 0),
       # (try_end),

       (init_position, pos2),
       (try_begin),
         (troop_is_hero, ":troop_no"),
         (try_begin), #rotate character, not flag
           (call_script, "script_cf_dplmc_troop_is_female", ":troop_no"),
           (position_rotate_z, pos2, -45),
         (try_end),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30),
       (position_rotate_x, pos8, -60),
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ])
]
