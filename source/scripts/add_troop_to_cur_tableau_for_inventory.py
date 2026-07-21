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

add_troop_to_cur_tableau_for_inventory_scripts = [
("add_troop_to_cur_tableau_for_inventory",
    [
       (store_script_param, ":troop_no",1),
       (store_mod, ":side", ":troop_no", 4), #side flag is inside troop_no value
       (val_div, ":troop_no", 4), #removing the flag bit
       (val_mul, ":side", 90), #to degrees

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       #SB : override appearance while disguised and buying stuff
       (try_begin),
         (gt, "$sneaked_into_town", disguise_none),
         (cur_tableau_set_override_flags, af_override_everything),
         (try_begin),
           (eq, "$sneaked_into_town", disguise_pilgrim),
           (cur_tableau_add_override_item, "itm_pilgrim_hood"),
           (cur_tableau_add_override_item, "itm_pilgrim_disguise"),
           (cur_tableau_add_override_item, "itm_wrapping_boots"),
         (else_try),
           (eq, "$sneaked_into_town", disguise_farmer),
           (cur_tableau_add_override_item, "itm_felt_hat"),
           (cur_tableau_add_override_item, "itm_coarse_tunic"),
           (cur_tableau_add_override_item, "itm_nomad_boots"),
         (else_try),
           (eq, "$sneaked_into_town", disguise_hunter),
           (cur_tableau_add_override_item, "itm_black_hood"),
           (cur_tableau_add_override_item, "itm_leather_gloves"),
           (cur_tableau_add_override_item, "itm_light_leather"),
           (cur_tableau_add_override_item, "itm_light_leather_boots"),
         (else_try),
           (eq, "$sneaked_into_town", disguise_merchant),
           (cur_tableau_add_override_item, "itm_leather_jacket"),
           (cur_tableau_add_override_item, "itm_woolen_hose"),
           (cur_tableau_add_override_item, "itm_felt_steppe_cap"),
         (else_try),
           (eq, "$sneaked_into_town", disguise_guard),
           (cur_tableau_add_override_item, "itm_footman_helmet"),
           (cur_tableau_add_override_item, "itm_mail_mittens"),
           (cur_tableau_add_override_item, "itm_mail_shirt"),
           (cur_tableau_add_override_item, "itm_leather_jerkin"),
           (cur_tableau_add_override_item, "itm_mail_chausses"),
         (else_try),
           (eq, "$sneaked_into_town", disguise_bard),
           (cur_tableau_add_override_item, "itm_linen_tunic"),
           (cur_tableau_add_override_item, "itm_leather_boots"),
         (try_end),
       (try_end),
       (init_position, pos2),
       (position_rotate_z, pos2, ":side"),
       (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 380),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),

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
