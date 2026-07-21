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

add_troop_to_cur_tableau_scripts = [
("add_troop_to_cur_tableau",
    [
       (store_script_param, ":troop_no",1),

       (cur_tableau_clear_override_items),

#       (cur_tableau_set_override_flags, af_override_fullhelm),
       (cur_tableau_set_override_flags, af_override_head|af_override_weapons),

       (set_fixed_point_multiplier, 100),
       (assign, ":banner_mesh", -1),
       (troop_get_slot, ":banner_spr", ":troop_no", slot_troop_banner_scene_prop),
       (try_begin),
           (eq, ":banner_spr", -1),
           (try_begin),
              # (this_or_next|eq, ":troop_no", "trp_player"),
              # (is_between, ":troop_no", npcs_begin, npcs_end),
              (troop_get_slot, ":flag_icon", ":troop_no", slot_troop_custom_banner_map_flag_type),
              (ge, ":flag_icon", 0),
              (troop_get_slot, ":banner", ":troop_no", slot_troop_custom_banner_flag_type),
              (ge, ":banner", 0),
              (val_add, ":banner", "itm_banner_background1"),
              (cur_tableau_add_override_item, ":banner"),
           (try_end),
       (else_try),
           (gt, ":banner_spr", 0),
           (store_add, ":banner_scene_props_end", banner_scene_props_end_minus_one, 1),
           (try_begin),
             (is_between, ":banner_spr", banner_scene_props_begin, ":banner_scene_props_end"),
             (val_sub, ":banner_spr", banner_scene_props_begin),
             (store_add, ":banner_mesh", ":banner_spr", banner_meshes_begin),
           (try_end),
       (try_end),



       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":eye_height", 162),
       (store_mul, ":camera_distance", ":troop_no", 87323),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 139),
       (store_mul, ":camera_yaw", ":troop_no", 124337),
       (val_mod, ":camera_yaw", 50),
       (val_add, ":camera_yaw", -25),
       (store_mul, ":camera_pitch", ":troop_no", 98123),
       (val_mod, ":camera_pitch", 20),
       (val_add, ":camera_pitch", -14),
       (assign, ":animation", "anim_stand_man"),

##       (troop_get_inventory_slot, ":horse_item", ":troop_no", ek_horse),
##       (try_begin),
##         (gt, ":horse_item", 0),
##         (assign, ":eye_height", 210),
##         (cur_tableau_add_horse, ":horse_item", pos2, anim_horse_stand, 0),
##         (assign, ":animation", anim_ride_0),
##         (position_set_z, pos5, 125),
##         (try_begin),
##           (is_between, ":camera_yaw", -10, 10), #make sure horse head doesn't obstruct face.
##           (val_min, ":camera_pitch", -5),
##         (try_end),
##       (try_end),
       (position_set_z, pos5, ":eye_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (ge, ":banner_mesh", 0),
         (eq, "$black_jack",0),#plus blackjack 21


         (init_position, pos1),
         (position_set_z, pos1, -1500),
         (position_set_x, pos1, 265),
         (position_set_y, pos1, 400),
         (position_transform_position_to_parent, pos3, pos5, pos1),
         (cur_tableau_add_mesh, ":banner_mesh", pos3, 400, 0),
       (try_end),
       (cur_tableau_add_troop, ":troop_no", pos2, ":animation" , 0),

       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30),
       (position_rotate_x, pos8, -60),
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ])
]
