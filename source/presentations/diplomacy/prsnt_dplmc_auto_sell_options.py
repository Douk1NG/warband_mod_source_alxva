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

dplmc_auto_sell_options = ("dplmc_auto_sell_options", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        ## do auto-sell automaticly when leaving
        (create_text_overlay, reg0, "@Sell items automatically when leaving:", tf_vertical_align_center),
        (position_set_x, pos1, 170),
        (position_set_y, pos1, 660),
        (overlay_set_position, reg0, pos1),

        (create_check_box_overlay, "$g_presentation_obj_1", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 150),
        (position_set_y, pos1, 652),
        (overlay_set_position, "$g_presentation_obj_1", pos1),
        (overlay_set_val, "$g_presentation_obj_1", "$g_dplmc_sell_items_when_leaving"),

        ## price_limit
        (create_text_overlay, reg0, "@Price limit for auto-sell:", tf_vertical_align_center),
        (position_set_x, pos1, 150),
        (position_set_y, pos1, 610),
        (overlay_set_position, reg0, pos1),

        (create_number_box_overlay, "$g_presentation_obj_2", 10, 10000),
        (position_set_x, pos1, 600),
        (position_set_y, pos1, 596),
        (overlay_set_val, "$g_presentation_obj_2", "$g_dplmc_auto_sell_price_limit"),
        (overlay_set_position, "$g_presentation_obj_2", pos1),

        # done
        (create_game_button_overlay, "$g_presentation_obj_3", "str_done"),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 25),
        (overlay_set_position, "$g_presentation_obj_3", pos1),

        ## Item types
        (create_text_overlay, reg0, "@Item types for auto-sell:", tf_vertical_align_center),
        (position_set_x, pos1, 150),
        (position_set_y, pos1, 578),
        (overlay_set_position, reg0, pos1),

        # select all
        (create_image_button_overlay, "$g_presentation_obj_5", "mesh_drop_button_child", "mesh_drop_button_child_down"),
        (position_set_x, pos1, 160),
        (position_set_y, pos1, 528),
        (overlay_set_position, "$g_presentation_obj_5", pos1),
        (create_text_overlay, reg1, "@Select all", tf_center_justify|tf_vertical_align_center),
        (position_set_x, pos1, 265),
        (position_set_y, pos1, 538),
        (overlay_set_position, reg1, pos1),

        # select invert
        (create_image_button_overlay, "$g_presentation_obj_6", "mesh_drop_button_child", "mesh_drop_button_child_down"),
        (position_set_x, pos1, 385),
        (position_set_y, pos1, 528),
        (overlay_set_position, "$g_presentation_obj_6", pos1),
        (create_text_overlay, reg1, "@Select invert", tf_center_justify|tf_vertical_align_center),
        (position_set_x, pos1, 490),
        (position_set_y, pos1, 538),
        (overlay_set_position, reg1, pos1),

        (assign, ":pos_x", 160),
        (assign, ":pos_y", 500),
        (try_for_range, ":cur_type", 0, 20),
          (store_add, ":cur_item_type", itp_type_horse, ":cur_type"),
          (neq, ":cur_item_type", itp_type_goods),
          (neq, ":cur_item_type", itp_type_animal),
          (neq, ":cur_item_type", itp_type_book),
          # button
          (position_set_x, pos1, ":pos_x"),
          (position_set_y, pos1, ":pos_y"),
          (create_mesh_overlay, reg1, "mesh_drop_button_child"),
          (overlay_set_position, reg1, pos1),
          # text
          (store_add, ":text_pos_x", ":pos_x", 120),
          (store_add, ":text_pos_y", ":pos_y", 10),
          (position_set_x, pos1, ":text_pos_x"),
          (position_set_y, pos1, ":text_pos_y"),
          (store_add, ":out_string", "str_dplmc_hero_wpn_slot_horse", ":cur_type"),#<- dplmc+ added "dplmc" prefix
          (str_store_string, s1, ":out_string"),
          (create_text_overlay, reg1, "@{s1}", tf_center_justify|tf_vertical_align_center),
          (overlay_set_position, reg1, pos1),
          # checkbox
          (store_add, ":checkbox_pos_x", ":pos_x", 0),
          (store_add, ":checkbox_pos_y", ":pos_y", 4),
          (position_set_x, pos1, ":checkbox_pos_x"),
          (position_set_y, pos1, ":checkbox_pos_y"),
          (create_check_box_overlay, reg1, "mesh_checkbox_off", "mesh_checkbox_on"),
          (overlay_set_position, reg1, pos1),
          (store_add, ":item_type", itp_type_horse, ":cur_type"),
          (item_get_slot, ":for_sell", ":item_type", dplmc_slot_item_type_not_for_sell),
          (store_sub, ":for_sell", 1, ":for_sell"),
          (overlay_set_val, reg1, ":for_sell"),
          (troop_set_slot, "trp_temp_array_b", ":cur_type", reg1),
          # focous
          (val_add, ":pos_x", 225),
          (try_begin),
            (eq, ":pos_x", 835),
            (assign, ":pos_x", 160),
            (val_sub, ":pos_y", 28),
          (try_end),
        (try_end),

        ####### mouse fix pos system #######
        #(call_script, "script_mouse_fix_pos_ready"),
        ####### mouse fix pos system #######
      ]),

      #(ti_on_presentation_run,
        #[
        ####### mouse fix pos system #######
        #(call_script, "script_mouse_fix_pos_run"),
        ####### mouse fix pos system #######
      #]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_1"),
          (assign, "$g_dplmc_sell_items_when_leaving", ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_2"),
          (assign, "$g_dplmc_auto_sell_price_limit", ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_3"),
          (presentation_set_duration, 0),
        (else_try),
          ## select all
          (eq, ":object", "$g_presentation_obj_5"),
          (try_for_range, ":cur_type", 0, 20),
            (store_add, ":cur_item_type", itp_type_horse, ":cur_type"),
            (neq, ":cur_item_type", itp_type_goods),
            (neq, ":cur_item_type", itp_type_animal),
            (neq, ":cur_item_type", itp_type_book),
            (item_set_slot, ":cur_item_type", dplmc_slot_item_type_not_for_sell, 0),
            (troop_get_slot, ":dest_checkbox", "trp_temp_array_b", ":cur_type"),
            (overlay_set_val, ":dest_checkbox", 1),
          (try_end),
        (else_try),
          ## select invert
          (eq, ":object", "$g_presentation_obj_6"),
          (try_for_range, ":cur_type", 0, 20),
            (store_add, ":cur_item_type", itp_type_horse, ":cur_type"),
            (neq, ":cur_item_type", itp_type_goods),
            (neq, ":cur_item_type", itp_type_animal),
            (neq, ":cur_item_type", itp_type_book),
            (item_get_slot, ":for_sell", ":cur_item_type", dplmc_slot_item_type_not_for_sell),
            (val_add, ":for_sell", 1),
            (val_mod, ":for_sell", 2),
            (item_set_slot, ":cur_item_type", dplmc_slot_item_type_not_for_sell, ":for_sell"),
            (troop_get_slot, ":dest_checkbox", "trp_temp_array_b", ":cur_type"),
            (store_sub, ":dest_val", 1, ":for_sell"),
            (overlay_set_val, ":dest_checkbox", ":dest_val"),
          (try_end),
        (try_end),

        ## checkboxes
        (try_for_range, ":slot_item_type_checkbox", 0, 20),
          (troop_slot_eq, "trp_temp_array_b", ":slot_item_type_checkbox", ":object"),
          (store_add, ":item_type", itp_type_horse, ":slot_item_type_checkbox"),
          (store_sub, ":for_sell", 1, ":value"),
          (item_set_slot, ":item_type", dplmc_slot_item_type_not_for_sell, ":for_sell"),
        (try_end),
      ]),
    ])
