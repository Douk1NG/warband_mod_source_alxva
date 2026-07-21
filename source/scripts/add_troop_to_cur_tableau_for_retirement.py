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

add_troop_to_cur_tableau_for_retirement_scripts = [
("add_troop_to_cur_tableau_for_retirement", [
    (store_script_param, ":type", 1),
    (try_begin),
      (is_between, ":type", 0, 10),
      (cur_tableau_set_override_flags, af_override_everything),
    (try_end),

    (try_begin),
      (eq, ":type", 0),
      (cur_tableau_add_override_item, "itm_pilgrim_hood"),
      (cur_tableau_add_override_item, "itm_pilgrim_disguise"),
      (cur_tableau_add_override_item, "itm_wrapping_boots"),
      (assign, ":animation", "anim_pose_1"),
    (else_try),
      (eq, ":type", 1),
      (cur_tableau_add_override_item, "itm_pilgrim_hood"),
      (cur_tableau_add_override_item, "itm_red_tunic"),
      (cur_tableau_add_override_item, "itm_wrapping_boots"),
      (cur_tableau_add_override_item, "itm_dagger"),
      (assign, ":animation", "anim_pose_1"),
    (else_try),
      (eq, ":type", 2),
      (cur_tableau_add_override_item, "itm_linen_tunic"),
      (cur_tableau_add_override_item, "itm_wrapping_boots"),
      (assign, ":animation", "anim_pose_2"),
    (else_try),
      (eq, ":type", 3),
      (cur_tableau_add_override_item, "itm_nomad_vest"),
      (cur_tableau_add_override_item, "itm_nomad_boots"),
      (assign, ":animation", "anim_pose_2"),
    (else_try),
      (eq, ":type", 4),
      (cur_tableau_add_override_item, "itm_leather_apron"),
      (cur_tableau_add_override_item, "itm_leather_boots"),
      (assign, ":animation", "anim_pose_3"),
    (else_try),
      (eq, ":type", 5),
      (cur_tableau_add_override_item, "itm_red_shirt"),
      (cur_tableau_add_override_item, "itm_woolen_hose"),
      (cur_tableau_add_override_item, "itm_fur_hat"),
      (assign, ":animation", "anim_pose_3"),
    (else_try),
      (eq, ":type", 6),
      (cur_tableau_add_override_item, "itm_red_gambeson"),
      (cur_tableau_add_override_item, "itm_leather_boots"),
      (cur_tableau_add_override_item, "itm_sword_medieval_c"),
      (assign, ":animation", "anim_pose_4"),
    (else_try),
      (eq, ":type", 7),
      (cur_tableau_add_override_item, "itm_nobleman_outfit"),
      (cur_tableau_add_override_item, "itm_blue_hose"),
      (cur_tableau_add_override_item, "itm_sword_medieval_c"),
      (assign, ":animation", "anim_pose_4"),
    (else_try),
      (eq, ":type", 8),
      (cur_tableau_add_override_item, "itm_courtly_outfit"),
      (cur_tableau_add_override_item, "itm_woolen_hose"),
      (cur_tableau_add_override_item, "itm_sword_medieval_c"),
      (assign, ":animation", "anim_pose_4"),
    (else_try),
      (eq, ":type", 9),
      (cur_tableau_add_override_item, "itm_heraldic_mail_with_surcoat_for_tableau"),
      (cur_tableau_add_override_item, "itm_mail_boots_for_tableau"),
      (cur_tableau_add_override_item, "itm_sword_medieval_c"),
      (assign, ":animation", "anim_pose_5"),
    (try_end),

##    (set_fixed_point_multiplier, 100),
##    (cur_tableau_set_background_color, 0x00000000),
##    (cur_tableau_set_ambient_light, 10,11,15),

##     (init_position, pos8),
##     (position_set_x, pos8, -210),
##     (position_set_y, pos8, 200),
##     (position_set_z, pos8, 300),
##     (cur_tableau_add_point_light, pos8, 550,500,450),


    (set_fixed_point_multiplier, 100),
    (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),
    (assign, ":cam_height", 155),
    (assign, ":camera_distance", 575),
    (assign, ":camera_yaw", -5),
    (assign, ":camera_pitch", 10),

    (init_position, pos5),
    (position_set_z, pos5, ":cam_height"),
    # camera looks towards -z axis
    (position_rotate_x, pos5, -90),
    (position_rotate_z, pos5, 180),
    # now apply yaw and pitch
    (position_rotate_y, pos5, ":camera_yaw"),
    (position_rotate_x, pos5, ":camera_pitch"),
    (position_move_z, pos5, ":camera_distance", 0),
    (position_move_x, pos5, 60, 0),

    (init_position, pos2),
    (cur_tableau_add_troop, "trp_player", pos2, ":animation", 0),
    (cur_tableau_set_camera_position, pos5),

    (copy_position, pos8, pos5),
    (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
    (position_rotate_z, pos8, 30),
    (position_rotate_x, pos8, -60),
    (cur_tableau_add_sun_light, pos8, 175,150,125),
    ])
]
