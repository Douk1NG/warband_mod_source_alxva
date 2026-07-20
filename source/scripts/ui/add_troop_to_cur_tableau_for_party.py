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

add_troop_to_cur_tableau_for_party_scripts = [
("add_troop_to_cur_tableau_for_party",
    [
       (store_script_param, ":troop_no",1),
       (store_mod, ":hide_weapons", ":troop_no", 2), #hide_weapons flag is inside troop_no value
       (val_div, ":troop_no", 2), #removing the flag bit

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       (try_begin),
         (eq, ":hide_weapons", 1),
         (cur_tableau_set_override_flags, af_override_fullhelm|af_override_head|af_override_weapons),
       (try_end),

       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 450),
       (assign, ":camera_yaw", 15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),

       (troop_get_inventory_slot, ":horse_item", ":troop_no", ek_horse),
       (try_begin),
         (gt, ":horse_item", 0),
         (eq, ":hide_weapons", 0),
         (cur_tableau_add_horse, ":horse_item", pos2, "anim_horse_stand", 0),
         (assign, ":animation", "anim_ride_0"),
         (assign, ":camera_yaw", 23),
         (assign, ":cam_height", 150),
         (assign, ":camera_distance", 550),
       (try_end),
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
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
