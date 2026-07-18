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

dplmc_shopping_list_of_food = ("dplmc_shopping_list_of_food", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        ## back
        (create_game_button_overlay, "$g_presentation_obj_1", "str_done"),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 25),
        (overlay_set_position, "$g_presentation_obj_1", pos1),

        ## buy food automatically when leaving
        (create_text_overlay, reg0, "@Buy food automatically when leaving:", tf_vertical_align_center),
        (position_set_x, pos1, 170),
        (position_set_y, pos1, 690),
        (overlay_set_position, reg0, pos1),

        (create_check_box_overlay, "$g_presentation_obj_2", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 150),
        (position_set_y, pos1, 682),
        (overlay_set_position, "$g_presentation_obj_2", pos1),
        (overlay_set_val, "$g_presentation_obj_2", "$g_dplmc_buy_food_when_leaving"),

        (assign, ":pos_x", 60),
        (assign, ":pos_y", 550),
        (try_for_range, ":cur_food", "itm_raw_date_fruit", food_end),
          (neq, ":cur_food", "itm_furs"),
          # frame
          (create_mesh_overlay, reg1, "mesh_inv_slot"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, reg1, pos1),
          (position_set_x, pos1, ":pos_x"),
          (position_set_y, pos1, ":pos_y"),
          (overlay_set_position, reg1, pos1),
          # back ground
          (create_mesh_overlay, reg1, "mesh_mp_inventory_choose"),
          (position_set_x, pos1, 640),
          (position_set_y, pos1, 640),
          (overlay_set_size, reg1, pos1),
          (position_set_x, pos1, ":pos_x"),
          (position_set_y, pos1, ":pos_y"),
          (overlay_set_position, reg1, pos1),
          # item overlay
          (troop_set_slot, "trp_temp_array_a", ":cur_food", reg1),
          (create_mesh_overlay_with_item_id, reg1, ":cur_food"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, reg1, pos1),
          (store_add, ":item_x", ":pos_x", 40),
          (store_add, ":item_y", ":pos_y", 40),
          (position_set_x, pos1, ":item_x"),
          (position_set_y, pos1, ":item_y"),
          (overlay_set_position, reg1, pos1),
          (troop_set_slot, "trp_temp_array_b", ":cur_food", reg1),
          # text *
          (create_text_overlay, reg1, "@*", tf_center_justify|tf_vertical_align_center),
          (store_add, ":text_x", ":pos_x", 100),
          (store_add, ":text_y", ":pos_y", 40),
          (position_set_x, pos1, ":text_x"),
          (position_set_y, pos1, ":text_y"),
          (overlay_set_position, reg1, pos1),
          # number_box
          (create_number_box_overlay, reg1, 0, 5),
          (store_add, ":number_box_x", ":pos_x", 115),
          (store_add, ":number_box_y", ":pos_y", 30),
          (position_set_x, pos1, ":number_box_x"),
          (position_set_y, pos1, ":number_box_y"),
          (overlay_set_position, reg1, pos1),
          (item_get_slot, ":food_portion", ":cur_food", dplmc_slot_item_food_portion),
          (overlay_set_val, reg1, ":food_portion"),
          (troop_set_slot, "trp_temp_array_c", ":cur_food", reg1),
          # next
          (val_add, ":pos_x", 240),
          (try_begin),
            (eq, ":pos_x", 1020),
            (assign, ":pos_x", 60),
            (val_sub, ":pos_y", 120),
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

    (ti_on_presentation_mouse_enter_leave,
      [
      (store_trigger_param_1, ":object"),
      (store_trigger_param_2, ":enter_leave"),

      (try_begin),
        (eq, ":enter_leave", 0),
        #SB : show actual modifier
        (try_begin),
          (is_between, "$current_town", towns_begin, towns_end),
          (party_get_slot, ":merchant", "$current_town", slot_town_merchant),
        (else_try),
          (is_between, "$current_town", villages_begin, villages_end),
          (party_get_slot, ":merchant", "$current_town", slot_town_elder),
        (else_try),
          (assign, ":merchant", -1),
        (try_end),
        (try_for_range, ":cur_food", "itm_raw_date_fruit", food_end),
          (neq, ":cur_food", "itm_furs"),
          (troop_slot_eq, "trp_temp_array_a", ":cur_food", ":object"),
          (troop_get_slot, ":target_obj", "trp_temp_array_b", ":cur_food"),
          (overlay_get_position, pos0, ":target_obj"),
          (try_begin),
            (le, ":merchant", 0),
            (show_item_details, ":cur_food", pos0, 100),
          (else_try),
            (call_script, "script_dplmc_get_item_buy_price_factor", ":cur_food", "$current_town", "trp_player", ":merchant"),
            (show_item_details, ":cur_food", pos0, reg0),
          (try_end),
          (assign, "$g_current_opened_item_details", ":cur_food"),
        (try_end),
      (else_try),
        (try_for_range, ":cur_food", "itm_raw_date_fruit", food_end),
          (neq, ":cur_food", "itm_furs"),
          (troop_slot_eq, "trp_temp_array_a", ":cur_food", ":object"),
          (try_begin),
            (eq, "$g_current_opened_item_details", ":cur_food"),
            (close_item_details),
          (try_end),
        (try_end),
      (try_end),
    ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_for_range, ":cur_food", "itm_raw_date_fruit", food_end),
          (neq, ":cur_food", "itm_furs"),
          (troop_slot_eq, "trp_temp_array_c", ":cur_food", ":object"),
          (item_set_slot, ":cur_food", dplmc_slot_item_food_portion, ":value"),
        (try_end),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_2"),
          (assign, "$g_dplmc_buy_food_when_leaving", ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_1"),
          (presentation_set_duration, 0),
        (try_end),
    ]),
  ])
