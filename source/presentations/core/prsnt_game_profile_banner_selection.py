# -*- coding: cp1254 -*-
import string
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
#SB: import skills from ID_skills import *
from module_constants import *
##diplomacy start+ Import for use with terrain advantage
from header_terrain_types import *
from module_items import *
#SB : import colors
from module_factions import *
from header_items import *
##diplomacy end
from compiler import *

game_profile_banner_selection = ("game_profile_banner_selection", 0, mesh_load_window, [
    (ti_on_presentation_load, [
      (set_fixed_point_multiplier, 1000),
      (str_store_string, s1, "str_profile_banner_selection_text"),
      (create_text_overlay, reg1, s1, tf_center_justify),
      (position_set_x, pos1, 500),
      (position_set_y, pos1, 600),
      (overlay_set_position, reg1, pos1),
      (overlay_set_text, reg1, s1),
      (create_button_overlay, "$g_presentation_obj_profile_banner_selection_1", "@Next Page", tf_center_justify),
      (position_set_x, pos1, 700),
      (position_set_y, pos1, 50),
      (overlay_set_position, "$g_presentation_obj_profile_banner_selection_1", pos1),

      (create_button_overlay, "$g_presentation_obj_profile_banner_selection_2", "str_use_default_banner", tf_center_justify),
      (position_set_x, pos1, 300),
      (position_set_y, pos1, 50),
      (overlay_set_position, "$g_presentation_obj_profile_banner_selection_2", pos1),

      (assign, ":x_pos", 150),
      (assign, ":y_pos", 575),
      (store_mul, ":starting_banner", 16, "$g_presentation_page_no"),
      (store_add, ":ending_banner", ":starting_banner", 16),
      (store_add, "$g_presentation_banner_start", "$g_presentation_obj_profile_banner_selection_2", 1),
      (assign, ":num_valid_banners", 0),
      (try_for_range, ":cur_banner_mesh", banner_meshes_begin, banner_meshes_end_minus_one),
        (assign, ":already_used", 0),
        (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
          (faction_slot_eq, ":cur_faction", slot_faction_banner, ":cur_banner_mesh"),
          (assign, ":already_used", 1),
        (try_end),
        (eq, ":already_used", 0),
        (val_add, ":num_valid_banners", 1),
        (gt, ":num_valid_banners", ":starting_banner"),
        (le, ":num_valid_banners", ":ending_banner"),
        (create_image_button_overlay, reg1, ":cur_banner_mesh", ":cur_banner_mesh"),
        (position_set_x, pos1, ":x_pos"),
        (position_set_y, pos1, ":y_pos"),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 100),
        (position_set_y, pos1, 100),
        (overlay_set_size, reg1, pos1),
        (val_add, ":x_pos", 100),
        (ge, ":x_pos", 900),
        (assign, ":x_pos", 150),
        (val_sub, ":y_pos", 250),
      (try_end),
      (presentation_set_duration, 999999),
      ]),

    (ti_on_presentation_event_state_change, [
      (store_trigger_param_1, ":object"),
      (try_begin),
        (eq, ":object", "$g_presentation_obj_profile_banner_selection_1"),
        (val_add, "$g_presentation_page_no", 1),
        (val_mod, "$g_presentation_page_no", 8),
        (presentation_set_duration, 0),
        (start_presentation, "prsnt_game_profile_banner_selection"),
      (else_try),
        (eq, ":object", "$g_presentation_obj_profile_banner_selection_2"),
        (profile_set_banner_id, -1),
        (presentation_set_duration, 0),
      (else_try),
        (store_sub, ":selected_banner", ":object", "$g_presentation_banner_start"),
        (store_mul, ":page_adder", 16, "$g_presentation_page_no"),
        (val_add, ":selected_banner", ":page_adder"),
        (assign, ":num_valid_banners", 0),
        (assign, ":end_cond", banner_meshes_end_minus_one),
        (try_for_range, ":cur_banner_mesh", banner_meshes_begin, ":end_cond"),
          (assign, ":already_used", 0),
          (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
            (faction_slot_eq, ":cur_faction", slot_faction_banner, ":cur_banner_mesh"),
            (assign, ":already_used", 1),
          (try_end),
          (eq, ":already_used", 0),
          (try_begin),
            (eq, ":selected_banner", ":num_valid_banners"),
            (store_sub, ":selected_banner_index", ":cur_banner_mesh", banner_meshes_begin),
            (profile_set_banner_id, ":selected_banner_index"),
            (assign, ":end_cond", 0), #break
          (try_end),
          (val_add, ":num_valid_banners", 1),
        (try_end),
        (presentation_set_duration, 0),
      (try_end),
      ]),
    ])
