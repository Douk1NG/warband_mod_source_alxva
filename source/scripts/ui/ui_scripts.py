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

ui_scripts = [

("add_notification_menu",
    [
      (try_begin),
        (eq, "$g_infinite_camping", 0),
        (store_script_param, ":menu_no", 1),
        (store_script_param, ":menu_var_1", 2),
        (store_script_param, ":menu_var_2", 3),
        (assign, ":end_cond", 1),
        (try_for_range, ":cur_slot", 0, ":end_cond"),
          (try_begin),
            (troop_slot_ge, "trp_notification_menu_types", ":cur_slot", 1),
            (val_add, ":end_cond", 1),
          (else_try),
            (troop_set_slot, "trp_notification_menu_types", ":cur_slot", ":menu_no"),
            (troop_set_slot, "trp_notification_menu_var1", ":cur_slot", ":menu_var_1"),
            (troop_set_slot, "trp_notification_menu_var2", ":cur_slot", ":menu_var_2"),
          (try_end),
        (try_end),
      (try_end),
      ]),

("describe_relation_to_s63",
    [(store_script_param_1, ":relation"),
      (store_add, ":normalized_relation", ":relation", 100),
      (val_add, ":normalized_relation", 5),
      (store_div, ":str_offset", ":normalized_relation", 10),
      (val_clamp, ":str_offset", 0, 20),
      (store_add, ":str_id", "str_relation_mnus_100",  ":str_offset"),
      (str_store_string, s63, ":str_id"),
  ]),

("update_agent_position_on_map",
   [(store_script_param_1, ":agent_no"),
    (agent_get_slot, ":agent_overlay", ":agent_no", slot_agent_map_overlay_id),

    (get_player_agent_no, ":player_agent"),
    (try_begin),
      (le, ":agent_overlay", 0),
      (set_fixed_point_multiplier, 1000),
      (try_begin),
        (eq, ":agent_no", ":player_agent"),
        (create_mesh_overlay, reg1, "mesh_player_dot"),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 500),
        (overlay_set_size, reg1, pos1),
      (else_try),
        (create_mesh_overlay, reg1, "mesh_white_dot"),
        (position_set_x, pos1, 200),
        (position_set_y, pos1, 200),
        (overlay_set_size, reg1, pos1),
      (try_end),
      (overlay_set_alpha, reg1, 0x88),
      (agent_set_slot, ":agent_no", slot_agent_map_overlay_id, reg1),
      (assign, ":agent_overlay", reg1),
    (try_end),

    (try_begin),
      (neq, ":agent_no", ":player_agent"),
      (agent_get_party_id, ":agent_party", ":agent_no"),
      (try_begin),
        (eq, ":agent_party", "p_main_party"),
        (agent_get_division, ":agent_division", ":agent_no"),
        (try_begin),
          (eq, ":agent_division", 0),
          (overlay_set_color, ":agent_overlay", 0x8d5220),
        (else_try),
          (eq, ":agent_division", 1),
          (overlay_set_color, ":agent_overlay", 0x34c6e4),
        (else_try),
          (eq, ":agent_division", 2),
          (overlay_set_color, ":agent_overlay", 0x569619),
        (else_try),
          (eq, ":agent_division", 3),
          (overlay_set_color, ":agent_overlay", 0xFFE500),
        (else_try),
          (eq, ":agent_division", 4),
          (overlay_set_color, ":agent_overlay", 0x990099),
        (else_try),
          (eq, ":agent_division", 5),
          (overlay_set_color, ":agent_overlay", 0x99FE80),
        (else_try),
          (eq, ":agent_division", 6),
          (overlay_set_color, ":agent_overlay", 0x9DEFFE),
        (else_try),
          (eq, ":agent_division", 7),
          (overlay_set_color, ":agent_overlay", 0xFECB9D),
        (else_try),
          (eq, ":agent_division", 8),
          (overlay_set_color, ":agent_overlay", 0xB19C9C),
        (try_end),
      (else_try),
        (agent_is_ally, ":agent_no"),
        (overlay_set_color, ":agent_overlay", 0x5555FF),
      (else_try),
        (overlay_set_color, ":agent_overlay", 0xFF0000),
      (try_end),
    (try_end),

    (try_begin),
      (eq, ":agent_no", ":player_agent"),
      (agent_get_look_position, pos1, ":agent_no"),
      (position_get_rotation_around_z, ":rot", pos1),
      (init_position, pos10),
      (position_rotate_z, pos10, ":rot"),
      (overlay_set_mesh_rotation, ":agent_overlay", pos10),
      (call_script, "script_convert_3d_pos_to_map_pos"),
    (else_try),
      (agent_get_position, pos1, ":agent_no"),
      (call_script, "script_convert_3d_pos_to_map_pos"),
    (try_end),
    (overlay_set_position, ":agent_overlay", pos0),
  ]),

("convert_3d_pos_to_map_pos",
   [(set_fixed_point_multiplier, 1000),
    (position_transform_position_to_local, pos3, pos2, pos1),
    (position_get_x, ":agent_x_pos", pos3),
    (position_get_y, ":agent_y_pos", pos3),
    (val_div, ":agent_x_pos", "$g_battle_map_scale"),
    (val_div, ":agent_y_pos", "$g_battle_map_scale"),
    (set_fixed_point_multiplier, 1000),
    (store_sub, ":map_x", 980, "$g_battle_map_width"),
    (store_sub, ":map_y", 730, "$g_battle_map_height"),
    (val_add, ":agent_x_pos", ":map_x"),
    (val_add, ":agent_y_pos", ":map_y"),
    (position_set_x, pos0, ":agent_x_pos"),
    (position_set_y, pos0, ":agent_y_pos"),
  ]),

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
     ]),

("add_troop_to_cur_tableau_for_character",
    [
       (store_script_param, ":troop_no",1),

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       (cur_tableau_set_override_flags, af_override_fullhelm),
##       (cur_tableau_set_override_flags, af_override_head|af_override_weapons),

       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 4, 8, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 150),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 360),
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
     ]),

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
     ]),

("add_troop_to_cur_tableau_for_profile",
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

       (profile_get_banner_id, ":profile_banner"),
       (try_begin),
         (ge, ":profile_banner", 0),
         (init_position, pos2),
         (val_add, ":profile_banner", banner_meshes_begin),
         (position_set_x, pos2, -175),
         (position_set_y, pos2, -300),
         (position_set_z, pos2, 180),
         (position_rotate_x, pos2, 90),
         (position_rotate_y, pos2, -15),
         (cur_tableau_add_mesh, ":profile_banner", pos2, 0, 0),
       (try_end),

       (init_position, pos2),
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
     ]),

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
     ]),

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
    ]),

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
     ]),

("iterate_pointer_arrow",
    [
      (store_mission_timer_a_msec, ":cur_time"),
      (try_begin),
        (assign, ":up_down", ":cur_time"),
        (assign, ":turn_around", ":cur_time"),
        (val_mod, ":up_down", 1080),
        (val_div, ":up_down", 3),
        (scene_prop_get_instance, ":prop_instance", "spr_pointer_arrow", 0),
        (prop_instance_get_position, pos0, ":prop_instance"),
        (position_set_z_to_ground_level, pos0),
        (position_move_z, pos0, "$g_pointer_arrow_height_adder", 1),
        (set_fixed_point_multiplier, 100),
        (val_mul, ":up_down", 100),
        (store_sin, ":up_down_sin", ":up_down"),
        (position_move_z, pos0, ":up_down_sin", 1),
        (position_move_z, pos0, 100, 1),
        (val_mod, ":turn_around", 2880),
        (val_div, ":turn_around", 8),
        (init_position, pos1),
        (position_rotate_z, pos1, ":turn_around"),
        (position_copy_rotation, pos0, pos1),
        (prop_instance_set_position, ":prop_instance", pos0),
      (try_end),
     ]),

("check_concilio_calradi_achievement",
  [
   (try_begin),
     (eq, "$players_kingdom", "fac_player_supporters_faction"),
     (faction_get_slot, ":player_faction_king", "fac_player_supporters_faction", slot_faction_leader),
     (eq, ":player_faction_king", "trp_player"),
     (assign, ":number_of_vassals", 0),
     (try_for_range, ":cur_troop", active_npcs_begin, active_npcs_end),
       (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
       (store_faction_of_troop, ":cur_faction", ":cur_troop"),
       (eq, ":cur_faction", "fac_player_supporters_faction"),
       (val_add, ":number_of_vassals", 1),
     (try_end),
     (ge, ":number_of_vassals", 3),
     (unlock_achievement, ACHIEVEMENT_CONCILIO_CALRADI),
   (try_end),
  ]),

("overlay_container_add_listbox_item", [
        (store_script_param, ":line_y", 1),
        (store_script_param, ":npc_id", 2),

        (set_container_overlay, "$g_jrider_character_relation_listbox"),

        # create text overlay for entry
        (create_text_overlay, reg10, s1, tf_left_align),
        (overlay_set_color, reg10, 0xDDDDDD),
        (position_set_x, pos1, 650),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg10, pos1),
        (position_set_x, pos1, 0),
        (position_set_y, pos1, ":line_y"),
        (overlay_set_position, reg10, pos1),

        # create button
        (create_image_button_overlay, reg10, "mesh_white_plane", "mesh_white_plane"),
        (position_set_x, pos1, 0), # 590 real, 0 scrollarea
        (position_set_y, pos1, ":line_y"),
        (overlay_set_position, reg10, pos1),
        (position_set_x, pos1, 16000),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg10, pos1),
        (overlay_set_alpha, reg10, 0),
        (overlay_set_color, reg10, 0xDDDDDD),

        # store relation of button id to character number for use in triggers
        (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", reg10),
        (troop_set_slot, "trp_temp_array_b", ":current_storage_index", "$num_charinfo_candidates"),

        # reset variables if appropriate flags are up
        (try_begin),
            (try_begin),
                (this_or_next|eq, "$g_jrider_pres_called_from_menu", 1),
                (ge, "$g_jrider_reset_selected_on_faction", 1),

                (assign, "$character_info_id", ":npc_id"),
                (assign, "$g_jrider_last_checked_indicator", reg10),
                (assign, "$g_latest_character_relation_entry", "$num_charinfo_candidates"),
            (try_end),
        (try_end),

        # close the container
        (set_container_overlay, -1),
   ]),

("fill_relation_canditate_list_for_presentation",
    [
        (store_script_param, ":pres_type", 1),
        (store_script_param, ":base_candidates_y", 2),

        # Type of list from global variable: 0 courtship, 1 known lords
        (try_begin),
        ## For courtship:
            (eq, ":pres_type", 0),

            (try_for_range_backwards, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
                (troop_slot_ge, ":lady", slot_troop_met, 1), # met or better
                (troop_slot_eq, ":lady", slot_troop_spouse, -1), # unmarried

                # use faction filter
                (store_troop_faction, ":lady_faction", ":lady"),
                (val_sub, ":lady_faction", kingdoms_begin),
                (this_or_next|eq, "$g_jrider_faction_filter", -1),
                (eq, "$g_jrider_faction_filter", ":lady_faction"),

                (call_script, "script_troop_get_relation_with_troop", "trp_player", ":lady"),
                (gt, reg0, 0),
                (assign, reg3, reg0),

                (str_store_troop_name, s2, ":lady"),

                (store_current_hours, ":hours_since_last_visit"),
                (troop_get_slot, ":last_visit_hour", ":lady", slot_troop_last_talk_time),
                (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
                (store_div, ":days_since_last_visit", ":hours_since_last_visit", 24),
                (assign, reg4, ":days_since_last_visit"),

                #(str_store_string, s1, "str_s1_s2_relation_reg3_last_visit_reg4_days_ago"),
                (str_store_string, s1, "@{s2}: {reg3}, {reg4} days"),

                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", ":lady"),

                # candidate found, store troop id for later use
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", ":lady"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
        ## End courtship relations
        (else_try),
        ## For lord relations
            (eq, ":pres_type", 1),

            # Loop to identify
            (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
                (troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
            (try_end),

            (try_for_range, ":unused", active_npcs_begin, active_npcs_end),

                (assign, ":score_to_beat", 101),
                (assign, ":best_relation_remaining_npc", -1),

                (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
                        (troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
                        (troop_slot_ge, ":active_npc", slot_troop_met, 1),
                        (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

                        (call_script, "script_troop_get_player_relation", ":active_npc"),
                        (assign, ":relation_with_player", reg0),
                        (le, ":relation_with_player", ":score_to_beat"),

                        (assign, ":score_to_beat", ":relation_with_player"),
                        (assign, ":best_relation_remaining_npc", ":active_npc"),
                (try_end),
                (gt, ":best_relation_remaining_npc", -1),

                (str_store_troop_name, s4, ":best_relation_remaining_npc"),
                (assign, reg4, ":score_to_beat"),

                (str_store_string, s1, "@{s4}: {reg4}"),
                (troop_set_slot, ":best_relation_remaining_npc", slot_troop_temp_slot, 1),

                # use faction filter
                (store_troop_faction, ":npc_faction", ":best_relation_remaining_npc"),
                (val_sub, ":npc_faction", kingdoms_begin),
                (this_or_next|eq, "$g_jrider_faction_filter", -1),
                (eq, "$g_jrider_faction_filter", ":npc_faction"),

                # candidate found,
                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", ":best_relation_remaining_npc"),

                #store troop id for later use (could be merged with the object id)
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", ":best_relation_remaining_npc"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
        ## END Lords relations
        (else_try),
        ## Character and Companions
            (eq, ":pres_type", 2),

            # companions
            (try_for_range_backwards, ":companion", companions_begin, companions_end),
                (troop_slot_eq, ":companion", slot_troop_occupation, slto_player_companion),

                (str_store_troop_name, s1, ":companion"),

        (try_begin),
                    (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_kingsupport),
                    (str_store_string, s1, "@{s1}(gathering support)"),
                (else_try),
                    (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_gather_intel),
                    (str_store_string, s1, "@{s1} (intelligence)" ),
                (else_try),
                    (troop_slot_ge, ":companion", slot_troop_current_mission, npc_mission_peace_request),
                    (neg|troop_slot_eq, ":companion", slot_troop_current_mission, 8),
                    (str_store_string, s1, "@{s1} (ambassy)"),
                (else_try),
                        (eq, ":companion", "$g_player_minister"),
                    (str_store_string, s1, "@{s1} (minister"),
                (else_try),
                    (main_party_has_troop, ":companion"),
                    (str_store_string, s1, "@{s1} (under arms)"),
                (else_try),
                    (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible),
                    (str_store_string, s1, "@{s1} (attempting to rejoin)"),
                (else_try),
                    (troop_slot_ge, ":companion", slot_troop_cur_center, 1),
                    (str_store_string, s1, "@{s1} (separated after battle)"),
                (try_end),
                # candidate found,
                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", ":companion"),

                #store troop id for later use (could be merged with the object id)
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", ":companion"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
            # END companions

            # Wife/Betrothed
            # END Wife/Betrothed

            (try_begin),
            # Character
                (str_store_troop_name, s1, "trp_player"),

                # candidate found,
                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", "trp_player"),

                #store troop id for later use (could be merged with the object id)
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", "trp_player"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
            # End Character

        (try_end),
        ## END Character and Companions
    ]),

("get_troop_relation_to_player_string",
     [
         (store_script_param, ":target_string", 1),
         (store_script_param, ":troop_no", 2),

         (call_script, "script_troop_get_player_relation", ":troop_no"),
         (assign, ":relation", reg0),
         (str_clear, s61),

         (store_add, ":normalized_relation", ":relation", 100),
         (val_add, ":normalized_relation", 5),
         (store_div, ":str_offset", ":normalized_relation", 10),
         (val_clamp, ":str_offset", 0, 20),
         (store_add, ":str_rel_id", "str_relation_mnus_100_ns",  ":str_offset"),

         ## Make something if troop has relation but not strong enought to warrant a string
         (try_begin),
           (neq, ":str_rel_id", "str_relation_plus_0_ns"),
           (str_store_string, s61, ":str_rel_id"),
         (else_try),
           (neg|eq, reg0, 0),
           (str_is_empty, s61),
           (str_store_string, s61, "@ knows of you."),
         (else_try),
           (eq, reg0, 0),
           (str_is_empty, s61),
           (str_store_string, s61, "@ has no opinion about you."),
         (try_end),

         ## copy result string to target string
         (str_store_string_reg, ":target_string", s61),
     ]),

("get_troop_holdings",
     [
         (store_script_param, ":troop_no", 1),

         (assign, ":owned_centers", 0),
         (assign, ":num_centers", 0),
         (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
             (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
             (try_begin),
               (eq, ":num_centers", 0),
               (str_store_party_name, s50, ":cur_center"),
               (val_add, ":owned_centers", 1),
             (else_try),
               (eq, ":num_centers", 1),
               (str_store_party_name, s57, ":cur_center"),
               (str_store_string, s50, "@{s57} and {s50}"),
               (val_add, ":owned_centers", 1),
             (else_try),
               (str_store_party_name, s57, ":cur_center"),
               (str_store_string, s50, "@{!}{s57}, {s50}"),
               (val_add, ":owned_centers", 1),
             (try_end),
             (val_add, ":num_centers", 1),
         (try_end),
         (assign, reg50, ":owned_centers"),
     ]),

("generate_extended_troop_relation_information_string",
     [
         (store_script_param, ":troop_no", 1),

         # clear the strings and registers we'll use to prevent external interference
         (str_clear, s1),
         (str_clear, s2),
         (str_clear, s60),
         (str_clear, s42),
         (str_clear, s43),
         (str_clear, s44),
         (str_clear, s45),
         (str_clear, s46),
         (str_clear, s47),
         (str_clear, s48),
         (str_clear, s49),
         (str_clear, s50),
         (assign, reg40,0),
         (assign, reg41,0),
         (assign, reg43,0),
         (assign, reg44,0),
         (assign, reg46,0),
         (assign, reg47,0),
         (assign, reg48,0),
         (assign, reg49,0),
         (assign, reg50,0),
         (assign, reg51,0),

         (try_begin),
             (eq, ":troop_no", "trp_player"),
             (overlay_set_display, "$g_jrider_character_faction_filter", 0),

             # Troop name
             (str_store_troop_name, s1, ":troop_no"),

             # Get renown - slot_troop_renown
             (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
             (assign, reg40, ":renown"),

             # Controversy - slot_troop_controversy
             (troop_get_slot, ":controversy", ":troop_no", slot_troop_controversy),
             (assign, reg41, ":controversy"),

             # Honor - $player_honor
             (assign, reg42, "$player_honor"),

             # Right to rule - $player_right_to_rule
             (assign, reg43, "$player_right_to_rule"),

             # Current faction
             (store_add, reg45, "$players_kingdom"),
             (try_begin),
                 (is_between, "$players_kingdom", "fac_player_supporters_faction", npc_kingdoms_end),
                 (str_store_faction_name, s45, "$players_kingdom"),
             (else_try),
                 (assign, reg45, 0),
                 (str_store_string, s45, "@Calradia."),
             (try_end),

             # status
             (assign, ":origin_faction", "$players_kingdom"),
             #SB : gender strings
             (try_begin),
                 (is_between, ":origin_faction", npc_kingdoms_begin, npc_kingdoms_end),
                 (str_store_string, s44, "@sworn {man/woman}"),
             (else_try),
                 (eq, ":origin_faction", "fac_player_supporters_faction"),
                 (str_store_string, s44, "@ruler"),
             (else_try),
                 (str_store_string, s44, "@free {man/woman}"),
             (try_end),

             # Current liege and relation
             (faction_get_slot, ":liege", "$players_kingdom", slot_faction_leader),
             (str_store_troop_name, s46, ":liege"),
             (try_begin),
                 (eq, ":liege", ":troop_no"),
                 (assign, reg46, 0),
             (else_try),
                 (assign, reg46, ":liege"),
                 (str_clear, s47),
                 (str_clear, s60),

                 # Relation to liege
                 (call_script, "script_get_troop_relation_to_player_string", s47, ":liege"),
             (end_try),

             # Holdings
             (call_script, "script_get_troop_holdings", ":troop_no"),

             #### Final Storage
             (str_store_string, s1, "@{s1} Renown: {reg40}, Controversy: {reg41}^Honor: {reg42}, Right to rule: {reg43}^\
You are a {s44} of {s45}^{reg45?{reg46?Your liege, {s46},{s47}:You are the ruler of {s45}}:}^^Friends: ^Enemies: ^^Fiefs:^  {reg50?{s50}:no fief}"),
         #######################
         # END Player information
         (else_try),
         #######################
         # Lord information
             (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),

             # Troop name
             (str_store_troop_name, s1, ":troop_no"),

             # relation to player
             (str_clear, s2),
             (str_clear, s60),
             (call_script, "script_get_troop_relation_to_player_string", s2, ":troop_no"),

             # Get renown - slot_troop_renown
             (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
             (assign, reg40, ":renown"),

             # Controversy - slot_troop_controversy
             (troop_get_slot, ":controversy", ":troop_no", slot_troop_controversy),
             (assign, reg41, ":controversy"),

             # Get Reputation type - slot_lord_reputation_type
             (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
             (assign, reg42, "str_personality_archetypes"),
             (val_add, reg42, ":reputation"),
             (str_store_string, s42, reg42),

             (assign, reg42, ":reputation"),
             # Intrigue impatience - slot_troop_intrigue_impatience
             (troop_get_slot, ":impatience", ":troop_no", slot_troop_intrigue_impatience),
             (assign, reg43, ":impatience"),

             # Current faction - store_troop_faction
             (store_troop_faction, ":faction", ":troop_no"),
             (troop_get_slot, ":origin_faction", ":troop_no", slot_troop_original_faction),

             # Original faction - slot_troop_original_faction
             (try_begin), #SB : do not display original faction string if same
               (neq, ":faction", ":origin_faction"),
               (val_sub, ":origin_faction", npc_kingdoms_begin),
               (val_add, ":origin_faction", "str_kingdom_1_adjective"),
               (str_store_string, s44, ":origin_faction"),
               (assign, reg44, 1),
             (else_try), #if same, start line with capitalized Noble
               (assign, reg44, 0),
             (try_end), #actually skip this line altogether if ruler
             (str_store_faction_name, s45, ":faction"),

             # Current liege - deduced from current faction
             (faction_get_slot, ":liege", ":faction", slot_faction_leader),
             (try_begin),
               #When a member of a faction without a valid leader
               (lt, ":liege", 0),
               (assign, reg46, ":liege"),
               (str_store_string, s46, "str_noone"),
               (assign, reg47, 0),
             (else_try),
               (str_store_troop_name, s46, ":liege"),
               (try_begin),
                 (eq, ":liege", ":troop_no"),
                 (assign, reg46, 0),
               (else_try),
                 (assign, reg46, ":liege"),
                 # Relation to liege
                 (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":liege"),
                 (assign, reg47, reg0),
               (end_try),
             (try_end),

             # Promised a fief ?
             (troop_get_slot, reg51, ":troop_no", slot_troop_promised_fief),

             # Holdings
             (call_script, "script_get_troop_holdings", ":troop_no"),

              # slot_troop_prisoner_of_party
              (assign, reg48, 0),
              (try_begin),
                (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
                (assign, reg48, 1),
                (troop_get_slot, ":prisoner_party", ":troop_no", slot_troop_prisoner_of_party),
                (store_faction_of_party, ":party_faction", ":prisoner_party"),
                (str_store_faction_name, s48, ":party_faction"),
              (try_end),

              # Days since last meeting
              (store_current_hours, ":hours_since_last_visit"),
              (troop_get_slot, ":last_visit_hour", ":troop_no", slot_troop_last_talk_time),
              (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
              (store_div, reg49, ":hours_since_last_visit", 24),

              #### Final Storage (8 lines)
              (str_store_string, s1, "@{s1}{s2} {reg46?Reputed to be {s42}:}^Renown: {reg40}, Controversy: {reg41} {reg46?Impatience: {reg43}:}^\
{reg46?{reg44?{s44} noble:Noble} of the {s45}^Liege: {s46}, Relation: {reg47}:Ruler of the {s45}}^^{reg48?Currently prisoner of the {s48}:}^\
Days since last meeting: {reg49}^^Fiefs {reg51?(was promised a fief):}:^  {reg50?{s50}:no fief}"),
        ######################
        ## END lord infomation
        (else_try),
        #########################
        # kingdom lady, unmarried
             (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
             (troop_slot_eq, ":troop_no", slot_troop_spouse, -1),

             (str_store_troop_name, s1, ":troop_no"),

             # relation to player
             (str_clear, s2),
             (str_clear, s60),
             (call_script, "script_get_troop_relation_to_player_string", s2, ":troop_no"),

             # Controversy - slot_troop_controversy
             (troop_get_slot, ":controversy", ":troop_no", slot_troop_controversy),
             (assign, reg41, ":controversy"),

             # Reputation type
             (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
             (try_begin),
                 (eq, ":reputation", lrep_conventional),
                 (str_store_string, s42, "@conventional"),
             (else_try),
                 (eq, ":reputation", lrep_adventurous),
                 (str_store_string, s42, "@adventurous"),
             (else_try),
                 (eq, ":reputation", lrep_otherworldly),
                 (str_store_string, s42, "@otherwordly"),
             (else_try),
                 (eq, ":reputation", lrep_ambitious),
                 (str_store_string, s42, "@ambitious"),
             (else_try),
                 (eq, ":reputation", lrep_moralist),
                 (str_store_string, s42, "@moralist"),
             (else_try),
                 (assign, reg42, "str_personality_archetypes"),
                 (val_add, reg42, ":reputation"),
                 (str_store_string, s42, reg42),
             (try_end),

             # courtship state - slot_troop_courtship_state
             (troop_get_slot, ":courtship_state", ":troop_no", slot_troop_courtship_state),
             (try_begin),
               (eq, ":courtship_state", 1),
               (str_store_string, s43, "@just met"),
             (else_try),
               (eq, ":courtship_state", 2),
               (str_store_string, s43, "@admirer"),
             (else_try),
               (eq, ":courtship_state", 3),
               (str_store_string, s43, "@promised"),
             (else_try),
               (eq, ":courtship_state", 4),
               (str_store_string, s43, "@breakup"),
             (else_try),
               (str_store_string, s43, "@unknown"),
             (try_end),

             # Current faction - store_troop_faction
             (store_troop_faction, ":faction", ":troop_no"),
             (troop_get_slot, ":origin_faction", ":troop_no", slot_troop_original_faction),

             # Original faction - slot_troop_original_faction
             (try_begin),
               (val_sub, ":origin_faction", npc_kingdoms_begin),
               (val_add, ":origin_faction", "str_kingdom_1_adjective"),
               (str_store_string, s44, ":origin_faction"),
             (end_try),
             (str_store_faction_name, s45, ":faction"),

             # Father/Guardian
             (assign, reg46, 0),
             (try_begin),
                 (troop_slot_ge, ":troop_no", slot_troop_father, 0),
                 (troop_get_slot, ":guardian", ":troop_no", slot_troop_father),
                 (assign, reg46, 1),
             (else_try),
                 (troop_get_slot, ":guardian", ":troop_no", slot_troop_guardian),
             (try_end),
             (str_store_troop_name, s46, ":guardian"),

             # Relation with player
             (str_clear, s47),
             (str_clear, s60),
             (call_script, "script_get_troop_relation_to_player_string", s47, ":guardian"),

             # courtship permission - slot_lord_granted_courtship_permission
             (try_begin),
                 (troop_slot_ge, ":guardian", slot_lord_granted_courtship_permission, 1),
                 (assign, reg45, 1),
             (else_try),
                 (assign, reg45, 0),
             (try_end),

             # betrothed
             (assign, reg48, 0),
             (try_begin),
                 (troop_slot_ge, ":troop_no", slot_troop_betrothed, 0),
                 (troop_get_slot, reg48, ":troop_no", slot_troop_betrothed),
                 (str_store_troop_name, s48, reg48),
                 (assign, reg48, 1),
             (try_end),

             # Days since last meeting
             (store_current_hours, ":hours_since_last_visit"),
             (troop_get_slot, ":last_visit_hour", ":troop_no", slot_troop_last_talk_time),
             (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
             (store_div, reg49, ":hours_since_last_visit", 24),

             # Heard poems
             (assign, reg50, 0),
             (str_clear, s50),

             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_heroic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Heroic {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_allegoric_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Allegoric {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_comic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Comic {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_mystic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Mystic {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_tragic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Tragic {s50}"),
             (try_end),

             #### Final Storage (8 lines)
             (str_store_string, s1, "@{s1}{s2} Controversy: {reg41}^Reputation: {s42}, Courtship state: {s43}^\
Belongs to the {s45}^{reg46?Her father, {s46}:Her guardian, {s46}}{s47}^Allowed to visit: {reg45?yes:no} {reg48?Betrothed to {s48}:}^^\
Days since last meeting: {reg49}^^Poems:^  {reg50?{s50}:no poem heard}"),
        #########################
        # END kingdom lady, unmarried
        (else_try),
        #########################
        # companions
            (is_between, ":troop_no", companions_begin, companions_end),
            (overlay_set_display, "$g_jrider_character_faction_filter", 0),

            (str_store_troop_name, s1, ":troop_no"),

            (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),

            (assign, reg42, "str_personality_archetypes"),
            (val_add, reg42, ":reputation"),
            (str_store_string, s42, reg42),

            # birthplace
            (troop_get_slot, ":home", ":troop_no", slot_troop_home),
            (str_store_party_name, s43, ":home"),

            # contacts town - slot_troop_town_with_contacts
            (troop_get_slot, ":contact_town", ":troop_no", slot_troop_town_with_contacts),
            (str_store_party_name, s44, ":contact_town"),

            # current faction of contact town
            (store_faction_of_party, ":town_faction", ":contact_town"),
            (str_store_faction_name, s45, ":town_faction"),

            # slot_troop_prisoner_of_party
            (assign, reg48, 0),
            (try_begin),
                (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
                (assign, reg48, 1),
                (troop_get_slot, ":prisoner_party", ":troop_no", slot_troop_prisoner_of_party),
                (store_faction_of_party, ":party_faction", ":prisoner_party"),
                (str_store_faction_name, s48, ":party_faction"),
            (try_end),

            # Days since last meeting
            (store_current_hours, ":hours_since_last_visit"),
            (troop_get_slot, ":last_visit_hour", ":troop_no", slot_troop_last_talk_time),
            (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
            (store_div, reg49, ":hours_since_last_visit", 24),

            (try_begin), # Companion gathering support for Right to Rule
                (troop_slot_eq, ":troop_no", slot_troop_current_mission, npc_mission_kingsupport),
                (str_store_string, s50, "@Gathering support"),
            (else_try), # Companion gathering intelligence
                (troop_slot_eq, ":troop_no", slot_troop_current_mission, npc_mission_gather_intel),
                (troop_get_slot, ":contact_town", ":troop_no", slot_troop_town_with_contacts),
                (store_faction_of_party, ":town_faction", ":contact_town"),
                (str_store_faction_name, s66, ":town_faction"),
                (str_store_string, s50, "@Gathering intelligence in the {s66}"),
            (else_try), # Companion on peace mission
                (troop_slot_ge, ":troop_no", slot_troop_current_mission, npc_mission_peace_request),
                (neg|troop_slot_ge, ":troop_no", slot_troop_current_mission, 8),

                (troop_get_slot, ":troop_no", ":troop_no", slot_troop_mission_object),
                (str_store_faction_name, s66, ":faction"),

                (str_store_string, s50, "@Ambassy to {s66}"),
            (else_try), # Companion is serving as minister player has court
                (eq, ":troop_no", "$g_player_minister"),
                (str_store_string, s50, "@Minister"),
            (else_try),
                (str_store_string, s50, "str_dplmc_none"),
        (try_end),

            # days left
            (troop_get_slot, reg50, ":troop_no", slot_troop_days_on_mission),

            #### Final Storage (8 lines)
            (str_store_string, s1, "@{s1}, {s2}^Reputation: {s42}^\
Born at {s43}^Contact in {s44} of the {s45}.^\
^{reg48?Currently prisoner of the {s48}:}^Days since last talked to: {reg49}^^Current mission:^  {s50}{reg50?, back in {reg50} days.:}"),
        #########################
        # END companions
        (try_end),
    ]),

("generate_known_poems_string",
     [
        # Known poems string
        (assign, ":num_poems", 0),
        (str_store_string, s1, "str_s1__poems_known"),
        (try_begin),
            (gt, "$allegoric_poem_recitations", 0),
            (str_store_string, s1, "str_s1_storming_the_castle_of_love_allegoric"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$tragic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_kais_and_layali_tragic"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$comic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_a_conversation_in_the_garden_comic"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$heroic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_helgered_and_kara_epic"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$mystic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_a_hearts_desire_mystic"),
            (val_add, ":num_poems", 1),
        (try_end),

        # fill blank lines
        (try_for_range, ":num_poems", 5),
            (str_store_string, s1, "@{s1}^"),
        (try_end),
    ]),

("create_wpn_slot_overlay", [
      (store_script_param, ":slot", 1),
      (store_script_param, ":pos", 2),
      (init_position, pos1),
      (position_set_x, pos1, 270),
      (position_set_y, pos1, ":pos"),
      (create_combo_button_overlay, ":obj"),
      (overlay_set_position, ":obj", pos1),
      (assign, ":sub_overlay_id", 0),
      (store_add, ":upgrade_slot", ":slot", dplmc_slot_upgrade_wpn_0),

      # #SB : add meta-types
      # (overlay_add_item, ":obj", "str_dplmc_hero_wpn_slot_pikes"),
      # (overlay_add_item, ":obj", "str_dplmc_hero_wpn_slot_lance"),
      # (overlay_add_item, ":obj", "str_dplmc_hero_wpn_slot_morningstar"),
      # (try_for_range_backwards, ":item_type", dplmc_itp_morningstar, dplmc_itp_pike + 1),
        # (troop_slot_eq, "$temp", ":upgrade_slot", ":item_type"),
        # (overlay_set_val, ":obj", ":sub_overlay_id"),
      # (else_try),
        # (val_add, ":sub_overlay_id", 1),
      # (try_end),
      (call_script, "script_dplmc_get_current_item_for_autoloot", ":slot"), #goes to "keep current", s10
      (try_for_range_backwards, ":item_type", 0, itp_type_animal),
        (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_goods),
        (this_or_next|is_between, ":item_type", itp_type_pistol, itp_type_animal),
        (eq, ":item_type", 0),
        (store_add, ":out_string", "str_dplmc_hero_wpn_slot_none", ":item_type"),
        (overlay_add_item, ":obj", ":out_string"),
        (try_begin), #find base type
          (troop_get_slot, ":cur_value", "$temp", ":upgrade_slot"),
          (val_mod, ":cur_value", meta_itp_mask),
          (eq, ":cur_value", ":item_type"),
          (overlay_set_val, ":obj", ":sub_overlay_id"),
        (try_end),
        (val_add, ":sub_overlay_id", 1),
      (try_end),

      #store id in slot
      (troop_set_slot, "trp_stack_selection_ids", ":slot", ":obj"),
      # # only works for original button, not drop-down lists
      # (overlay_set_additional_render_height, ":obj", 99),

      (assign, reg1, ":obj"), #return overlay id
  ]),

("update_wpn_slot_itp", [
      (store_script_param, ":slot", 1),
      (store_script_param, ":value", 2),
      (troop_get_slot, ":item_type", "trp_temp_array_c", ":value"),
      (troop_get_slot, ":slot_value", "$temp", ":slot"),
      (try_begin), #if new value supports metamods, inherit
        (call_script, "script_cf_item_type_has_advanced_autoloot", ":item_type"),
        (store_mod, ":original_value", ":slot_value", meta_itp_mask),
        (val_sub, ":slot_value", ":original_value"), #remove original itp
        (val_add, ":slot_value", ":item_type"), #add new
      (else_try), #otherwise replace value
        (assign, ":slot_value", ":item_type"),
      (try_end),
      (troop_set_slot, "$temp", ":slot", ":slot_value"),
      (assign, "$temp_2", ":slot"),
      #restart presentation instead of updating overlay value (because we can't)
      (start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
  ]),

("display_policy_string_to_reg", [
    (store_script_param, ":faction_no", 1),
    (store_script_param, reg2, 2), #whether it is third person "the" or first person "our"
    (store_script_param, reg3, 3), #spaces or line breaks as the postfix delimiter

    (str_store_faction_name_link, s5, ":faction_no"),
    (assign, ":string", "str_dplmc_neither_centralize_nor_decentralized"),
    (faction_get_slot, ":centralization", ":faction_no", dplmc_slot_faction_centralization),
    (val_add, ":string", ":centralization"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}{reg2?Our government:The goverment of the {s5}} is {s0}.{reg3?^: }"),

    (assign, ":string", "str_dplmc_neither_aristocratic_nor_plutocratic"),
    (faction_get_slot, ":aristocraty", ":faction_no", dplmc_slot_faction_aristocracy),
    (val_add, ":string", ":aristocraty"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}The upper class society is {s0}.{reg3?^: }"),

    (assign, ":string", "str_dplmc_mixture_serfs"),
    (faction_get_slot, ":serfdom", ":faction_no", dplmc_slot_faction_serfdom),
    (val_add, ":string", ":serfdom"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}{reg2?Our:The} people are {s0}.{reg3?^: }"),

    (assign, ":string", "str_dplmc_mediocre_quality"),
    (faction_get_slot, ":quality", ":faction_no", dplmc_slot_faction_quality),
    (val_add, ":string", ":quality"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}{reg2?Our:The} troops have {s0}.{reg3?^: }"),

    ##nested diplomacy start+ add mercantilism
    (assign, ":string", "str_dplmc_neither_mercantilist_nor_laissez_faire"),
    (faction_get_slot, ":mercantilism", ":faction_no", dplmc_slot_faction_mercantilism),
    (val_add, ":string", ":mercantilism"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}{reg2?Our:The government's} approach to trade is {s0}.{reg3?^: }"),
  ]),

("build_background_answer_story", [
        (store_script_param_1, ":sreg"),
        (assign, reg11, "$character_gender"),
        (store_sub, ":string", "$background_answer_4", cb4_revenge),
        (val_add, ":string", "str_story_reason_revenge"),
        (str_store_string, s13, ":string"),
        (store_sub, ":string", "$background_answer_3", dplmc_cb3_bravo),
        (val_add, ":string", "str_story_job_bravo"),
        (str_store_string, s12, ":string"),
        (store_sub, ":string", "$background_answer_2", cb2_page), #values for this start from 0
        (val_add, ":string", "str_story_childhood_page"),
        (str_store_string, s11, ":string"),
        (store_sub, ":string", "$background_type", cb_noble),
        (val_add, ":string", "str_story_parent_noble"),
        (str_store_string, s10, ":string"),
        (str_store_string, ":sreg", "str_story_all"),
    ]),

("update_map_bar",
   [
    (set_fixed_point_multiplier, 1000),

    (get_player_agent_no, ":player_agent"),
    (try_for_agents,":cur_agent"),
      (agent_is_human, ":cur_agent"),
      (agent_get_slot, ":agent_overlay", ":cur_agent", slot_agent_map_overlay_id),
      (try_begin),
        (agent_is_alive, ":cur_agent"),
        (call_script, "script_update_agent_position_on_map_bar", ":cur_agent"),
      (else_try),
        (overlay_set_alpha, ":agent_overlay", 0),
      (try_end),
    (try_end),
    # player_chest
    (try_begin),
      (scene_prop_get_instance, ":player_chest", "spr_inventory", 0),
      (ge, ":player_chest", 0),
      (prop_instance_get_position, pos1, ":player_chest"),
      (call_script, "script_convert_3d_pos_to_map_bar_pos", -5),
      (overlay_set_position, "$g_player_chest_overlay", pos0),
      (overlay_set_alpha, "$g_player_chest_overlay", 0xFF),
    (else_try),
      (overlay_set_alpha, "$g_player_chest_overlay", 0),
    (try_end),
    # Horse Stamina
    #(agent_get_horse, ":horse_agent", ":player_agent"),
    #(try_begin),
    #  (eq, "$g_horse_charging_for_player", 1),
    #  (ge, ":horse_agent", 0),
    #  (agent_get_slot, ":horse_stamina", ":player_agent", slot_agent_horse_stamina),
    #  (store_agent_hit_points, ":horse_hp", ":horse_agent"),
    #  (assign, reg1, ":horse_stamina"),
    #  (assign, reg2, ":horse_hp"),
    #  (overlay_set_text, "$g_horse_stamina_overlay", "@Horse Stamina: {reg1}/{reg2}"),
    #  (overlay_set_alpha, "$g_horse_stamina_overlay", 0xFF),
    #(else_try),
    #  (overlay_set_alpha, "$g_horse_stamina_overlay", 0),
    #(try_end),
    # enemies-allies-us
    (assign, ":num_us_ready_men", 0),
    (assign, ":num_allies_ready_men", 0),
    (assign, ":num_enemies_ready_men", 0),
    (agent_get_team, ":player_team", ":player_agent"),
    (try_for_agents,":agent_no"),
      (agent_is_human, ":agent_no"),
      (agent_is_alive, ":agent_no"),
      (neq, ":agent_no", ":player_agent"),
      (agent_get_team, ":agent_team", ":agent_no"),
      (try_begin),
        (neg|agent_is_ally, ":agent_no"),
        (val_add, ":num_enemies_ready_men", 1),
      (else_try),
        (eq, ":agent_team", ":player_team"),
        (val_add, ":num_us_ready_men", 1),
      (else_try),
        (val_add, ":num_allies_ready_men", 1),
      (try_end),
    (try_end),
    (assign, reg10, ":num_enemies_ready_men"),
    (assign, reg11, ":num_allies_ready_men"),
    (assign, reg12, ":num_us_ready_men"),
    (overlay_set_text, "$g_battle_enemies_ready", "@{!}{reg10}"),
    (overlay_set_text, "$g_battle_allies_ready", "@{!}{reg11}"),
    (overlay_set_text, "$g_battle_us_ready", "@{!}{reg12}"),
  ]),

("prsnt_line",
    [
      (store_script_param, ":size_x", 1),
      (store_script_param, ":size_y", 2),
      (store_script_param, ":pos_x", 3),
      (store_script_param, ":pos_y", 4),
      (store_script_param, ":color", 5),

      (create_mesh_overlay, reg1, "mesh_white_plane"),
      (val_mul, ":size_x", 50),
      (val_mul, ":size_y", 50),
      (position_set_x, pos0, ":size_x"),
      (position_set_y, pos0, ":size_y"),
      (overlay_set_size, reg1, pos0),
      (position_set_x, pos0, ":pos_x"),
      (position_set_y, pos0, ":pos_y"),
      (overlay_set_position, reg1, pos0),
      (overlay_set_color, reg1, ":color"),
  ]),

("update_agent_position_on_map_bar",
   [(store_script_param_1, ":agent_no"),
    (agent_get_slot, ":agent_overlay", ":agent_no", slot_agent_map_overlay_id),

    (get_player_agent_no, ":player_agent"),
    (try_begin),
      (le, ":agent_overlay", 0),
      (set_fixed_point_multiplier, 1000),
      (try_begin),
        (eq, ":agent_no", ":player_agent"),
        (create_mesh_overlay, reg1, "mesh_player_dot"),
        (position_set_x, pos1, 800),
        (position_set_y, pos1, 800),
        (overlay_set_size, reg1, pos1),
      (else_try),
        (create_mesh_overlay, reg1, "mesh_white_dot"),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, 300),
        (overlay_set_size, reg1, pos1),
      (try_end),
      (agent_set_slot, ":agent_no", slot_agent_map_overlay_id, reg1),
      (assign, ":agent_overlay", reg1),
    (try_end),

    (agent_get_team, ":player_team", ":player_agent"),
    (try_begin),
      (neq, ":agent_no", ":player_agent"),
      (agent_get_team, ":agent_team", ":agent_no"),
      (try_begin),
        (neg|agent_is_ally, ":agent_no"),
        (overlay_set_color, ":agent_overlay", 0xFF4040),
        (assign, ":y_offset", 10),
      (else_try),
        (eq, ":agent_team", ":player_team"),
        (overlay_set_color, ":agent_overlay", 0x80FF80),
        (assign, ":y_offset", -10),
      (else_try),
        (overlay_set_color, ":agent_overlay", 0x8080FF),
        (assign, ":y_offset", 0),
      (try_end),
    (try_end),

    (try_begin),
      (eq, ":agent_no", ":player_agent"),
      (agent_get_look_position, pos1, ":agent_no"),
      (position_get_rotation_around_z, ":rot", pos1),
      (init_position, pos10),
      (position_rotate_z, pos10, ":rot"),
      (overlay_set_mesh_rotation, ":agent_overlay", pos10),
      (position_set_x, pos0, 620),
      (position_set_y, pos0, 721),
    (else_try),
      (agent_get_position, pos1, ":agent_no"),
      (call_script, "script_convert_3d_pos_to_map_bar_pos", ":y_offset"),
    (try_end),
    (overlay_set_position, ":agent_overlay", pos0),
  ]),

("convert_3d_pos_to_map_bar_pos",
   [
    (store_script_param_1, ":y_offset"),

    (set_fixed_point_multiplier, 1000),
    (position_move_z, pos1, 170),
    (position_get_screen_projection, pos3, pos1),
    (position_get_x, ":pos_x", pos3),
    (try_begin),
      (is_between, ":pos_x", -200, 1201),
      (val_clamp, ":pos_x", 0, 1001),
    (else_try), # hide on the left
      (lt, ":pos_x", -200),
      (assign, ":pos_x", -250),
    (else_try), # hide on the right
      (gt, ":pos_x", 1200),
      (assign, ":pos_x", 1250),
    (try_end),
    (val_sub, ":pos_x", 500),
    (val_mul, ":pos_x", 20),
    (val_div, ":pos_x", 100),
    (val_add, ":pos_x", 500),
    (store_add, ":pos_y", 721, ":y_offset"),
    (position_set_x, pos0, ":pos_x"),
    (position_set_y, pos0, ":pos_y"),
  ]),

("update_agent_hp_bar",
   [
    (set_fixed_point_multiplier, 1000),

    (get_player_agent_no, ":player_agent"),
    (try_for_agents,":agent_no"),
      (agent_is_human, ":agent_no"),
      (neq, ":agent_no", ":player_agent"),
      (agent_get_slot, ":agent_hp_overlay", ":agent_no", slot_agent_hp_bar_overlay_id),
      (agent_get_slot, ":agent_hp_bg_overlay", ":agent_no", slot_agent_hp_bar_bg_overlay_id),
      #(agent_get_slot, ":agent_name_overlay", ":agent_no", slot_agent_name_overlay_id),
      (try_begin),
        (agent_is_alive, ":agent_no"),
        # (agent_get_slot, ":agent_hp_overlay", ":agent_no", slot_agent_hp_bar_overlay_id),
        # (agent_get_slot, ":agent_hp_bg_overlay", ":agent_no", slot_agent_hp_bar_bg_overlay_id),
        # (agent_get_slot, ":agent_name_overlay", ":agent_no", slot_agent_name_overlay_id),

        (assign, ":create_hp_bar", 0),
        #(assign, ":create_name", 0),
        (try_begin), # create or not
          (agent_is_ally, ":agent_no"),
          (assign, ":create_hp_bar", "$g_hp_bar_ally"),
          #(assign, ":create_name", "$g_name_of_ally"),
        (else_try),
          (assign, ":create_hp_bar", "$g_hp_bar_enemy"),
          #(assign, ":create_name", "$g_name_of_enemy"),
        (try_end),

        (try_begin),
          (le, ":agent_hp_overlay", 0),
          (le, ":agent_hp_bg_overlay", 0),
          #(le, ":agent_name_overlay", 0),
          (set_fixed_point_multiplier, 1000),
          (try_begin),
            (eq, ":create_hp_bar", 1),
            # hp bg
            (create_mesh_overlay, reg1, "mesh_white_plane"),
            (overlay_set_alpha, reg1, 0x44),
            (agent_set_slot, ":agent_no", slot_agent_hp_bar_bg_overlay_id, reg1),
            (assign, ":agent_hp_bg_overlay", reg1),
            # hp
            (create_mesh_overlay, reg1, "mesh_white_plane"),
            (overlay_set_alpha, reg1, 0x44),
            (agent_set_slot, ":agent_no", slot_agent_hp_bar_overlay_id, reg1),
            (assign, ":agent_hp_overlay", reg1),
          (try_end),
          # (try_begin),
            # (eq, ":create_name", 1),
            ## name
            # (agent_get_troop_id, ":troop_id", ":agent_no"),
            # (str_store_troop_name, s1, ":troop_id"),
            # (create_text_overlay, reg1, "@{s1}", tf_center_justify),
            # (overlay_set_alpha, reg1, 0xCC),
            # (agent_set_slot, ":agent_no", slot_agent_name_overlay_id, reg1),
            # (assign, ":agent_name_overlay", reg1),
          # (try_end),
        (try_end),

        # color
        (agent_get_team, ":player_team", ":player_agent"),
        (agent_get_team, ":agent_team", ":agent_no"),
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        (try_begin),
          (eq, ":agent_team", ":player_team"),
          (assign, ":dest_color", 0x00FF00),
        (else_try),
          (agent_is_ally, ":agent_no"),
          (assign, ":dest_color", 0x0000FF),
        (else_try),
          (troop_is_hero, ":troop_id"),
          (assign, ":dest_color", 0xFFFF00),
        (else_try),
          (assign, ":dest_color", 0xFF0000),
        (try_end),
        (try_begin),
          (gt, ":agent_hp_overlay", 0),
          (gt, ":agent_hp_bg_overlay", 0),
          (overlay_set_color, ":agent_hp_overlay", ":dest_color"),
          (overlay_set_color, ":agent_hp_bg_overlay", 0x000000),
        (try_end),
        # (try_begin),
          # (gt, ":agent_name_overlay", 0),
          # (overlay_set_color, ":agent_name_overlay", ":dest_color"),
        # (try_end),

        # size & position
        # (this_or_next|gt, ":agent_name_overlay", 0),
        (gt, ":agent_hp_overlay", 0),

        (agent_get_position, pos1, ":agent_no"),
        (agent_get_horse, ":horse_agent", ":agent_no"),
        (try_begin),
          (ge, ":horse_agent", 0),
          (position_move_z, pos1, 280, 1),
        (else_try),
          (position_move_z, pos1, 180, 1),
        (try_end),
        (position_get_screen_projection, pos2, pos1),
        (position_get_x, ":head_x_pos", pos2),
        (position_get_y, ":head_y_pos", pos2),
        # base size
        (copy_position, pos6, pos1),
        (copy_position, pos7, pos1),
        (position_move_z, pos7, 100, 1),
        (position_get_screen_projection, pos6, pos6),
        (position_get_screen_projection, pos7, pos7),
        (position_get_y, ":screen_y_pos_1", pos6),
        (position_get_y, ":screen_y_pos_2", pos7),
        (store_sub, ":base_x", ":screen_y_pos_2", ":screen_y_pos_1"),
        (val_mul, ":base_x", 3),
        (val_div, ":base_x", 4),
        (val_clamp, ":base_x", 20, 161),
        (store_div, ":base_y", ":base_x", 20),
        (try_begin),
          (is_between, ":head_x_pos", -100, 1100),
          (is_between, ":head_y_pos", -100, 850),
          (agent_get_position, pos3, ":agent_no"),
          (agent_get_position, pos4, ":player_agent"),
          (get_distance_between_positions_in_meters, ":distance", pos3, pos4),
          (try_begin),
            (troop_is_hero, ":troop_id"),
            (val_div, ":distance", 2),
          (try_end),
          (le, ":distance", "$g_hp_bar_dis_limit"),
          # agent no
          (agent_get_horse, ":horse_agent", ":agent_no"),
          (try_begin),
            (ge, ":horse_agent", 0),
            (position_move_z, pos3, 280, 1),
          (else_try),
            (position_move_z, pos3, 180, 1),
          (try_end),
          # player agent
          (agent_get_horse, ":player_horse", ":player_agent"),
          (try_begin),
            (ge, ":player_horse", 0),
            (position_move_z, pos4, 280, 1),
          (else_try),
            (position_move_z, pos4, 180, 1),
          (try_end),
          (position_move_z, pos3, 50, 1),
          (position_move_z, pos4, 50, 1),
          (position_has_line_of_sight_to_position, pos3, pos4),

          (try_begin),
            (gt, ":agent_hp_overlay", 0),
            (gt, ":agent_hp_bg_overlay", 0),
            ## hp bg
            (assign, ":x_offset", ":base_x"),
            (val_div, ":x_offset", 2),
            (val_add, ":x_offset", 1),
            (store_sub, ":hp_bg_x", ":head_x_pos", ":x_offset"),
            (store_sub, ":hp_bg_y", ":head_y_pos", 1),
            (position_set_x, pos1, ":hp_bg_x"),
            (position_set_y, pos1, ":hp_bg_y"),
            (overlay_set_position, ":agent_hp_bg_overlay", pos1),
            (store_add, ":bg_width", ":base_x", 2),
            (val_mul, ":bg_width", 50),
            (store_add, ":bg_height", ":base_y", 2),
            (val_mul, ":bg_height", 50),
            (position_set_x, pos1, ":bg_width"),
            (position_set_y, pos1, ":bg_height"),
            (overlay_set_size, ":agent_hp_bg_overlay", pos1),
            (overlay_set_alpha, ":agent_hp_bg_overlay", 0x44),
            ## hp
            (store_add, ":hp_x", ":hp_bg_x", 1),
            (store_add, ":hp_y", ":hp_bg_y", 1),
            (position_set_x, pos1, ":hp_x"),
            (position_set_y, pos1, ":hp_y"),
            (overlay_set_position, ":agent_hp_overlay", pos1),
            (store_agent_hit_points, ":agent_hp",":agent_no"),
            (store_mul, ":hp_width", ":agent_hp", 50),
            (val_mul, ":hp_width", ":base_x"),
            (val_div, ":hp_width", 100),
            (val_min, ":hp_width", ":bg_width"),
            (store_mul, ":hp_height", ":base_y", 50),
            (position_set_x, pos1, ":hp_width"),
            (position_set_y, pos1, ":hp_height"),
            (overlay_set_size, ":agent_hp_overlay", pos1),
            (overlay_set_alpha, ":agent_hp_overlay", 0x44),
          (try_end),

          # name
          # (try_begin),
            # (gt, ":agent_name_overlay", 0),
            # (assign, ":name_x", ":head_x_pos"),
            # (store_add, ":name_y", ":head_y_pos", 5),
            # (position_set_x, pos1, ":name_x"),
            # (position_set_y, pos1, ":name_y"),
            # (overlay_set_position, ":agent_name_overlay", pos1),
            # (store_mul, ":name_size", ":base_x", 9),
            # (position_set_x, pos1, ":name_size"),
            # (position_set_y, pos1, ":name_size"),
            # (overlay_set_size, ":agent_name_overlay", pos1),
            # (overlay_set_alpha, ":agent_name_overlay", 0xCC),
          # (try_end),
        (else_try),
          (overlay_set_alpha, ":agent_hp_overlay", 0),
          (overlay_set_alpha, ":agent_hp_bg_overlay", 0),
          # (overlay_set_alpha, ":agent_name_overlay", 0),
        (try_end),
      (else_try),
        (try_begin),
          (gt, ":agent_hp_overlay", 0),
          (gt, ":agent_hp_bg_overlay", 0),
          (overlay_set_alpha, ":agent_hp_overlay", 0),
          (overlay_set_alpha, ":agent_hp_bg_overlay", 0),
        (try_end),
        # (try_begin),
          # (gt, ":agent_name_overlay", 0),
          # (overlay_set_alpha, ":agent_name_overlay", 0),
        # (try_end),
        (agent_set_slot, ":agent_no", slot_agent_hp_bar_overlay_id, 0),
        (agent_set_slot, ":agent_no", slot_agent_hp_bar_bg_overlay_id, 0),
        #(agent_set_slot, ":agent_no", slot_agent_name_overlay_id, 0),
      (try_end),
    (try_end),
  ]),
]