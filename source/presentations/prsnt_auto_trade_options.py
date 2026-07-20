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

auto_trade_options = ("auto_trade_options", 0, mesh_load_window, [
    (ti_on_presentation_load, [      
      (presentation_set_duration, 999999), 
      (set_fixed_point_multiplier, 1000),

      (create_game_button_overlay, "$g_presentation_obj_1", "@Done"),
      (position_set_x, pos1, 900),
      (position_set_y, pos1, 25),
      (overlay_set_position, "$g_presentation_obj_1", pos1),

      #Allows user to set a minimum wealth value for auto buying so they don't accidentally spend all their money
      (create_text_overlay, reg0, "@Only buy goods if wealth is above:", tf_vertical_align_center),
      (position_set_x, pos1, 50),
      (position_set_y, pos1, 700),
      (overlay_set_position, reg0, pos1),

      (create_number_box_overlay, "$g_presentation_obj_2", 0, 100000),
      (position_set_x, pos1, 400),
      (position_set_y, pos1, 692),
      (overlay_set_val, "$g_presentation_obj_2", "$g_auto_trade_minimum_wealth"),
      (overlay_set_position, "$g_presentation_obj_2", pos1),

      #Allows the user to autotrade when leaving a town or village
      (assign, ":pos_y", 650),
      (create_text_overlay, reg0, "@Trade automatically when leaving:", tf_vertical_align_center),
      (position_set_x, pos1, 50),
      (position_set_y, pos1, 675),
      (overlay_set_position, reg0, pos1),

      (create_check_box_overlay, "$g_presentation_obj_3", "mesh_checkbox_off", "mesh_checkbox_on"),
      (position_set_x, pos1, 400),
      (position_set_y, pos1, 667),
      (overlay_set_position, "$g_presentation_obj_3", pos1),
      (overlay_set_val, "$g_presentation_obj_3", "$g_auto_trade_items_when_leaving"),

      (create_game_button_overlay, "$g_presentation_obj_4", "@Next Page"),
      (position_set_x, pos1, 700),
      (position_set_y, pos1, 25),
      (overlay_set_position, "$g_presentation_obj_4", pos1),

      #Column headers
      (assign, ":pos_y", 650),
      (create_text_overlay, reg0, "@Buy", tf_vertical_align_center),
      (position_set_x, pos1, 215),
      (position_set_y, pos1, ":pos_y",),
      (overlay_set_position, reg0, pos1),

      (create_text_overlay, reg0, "@If Under:", tf_vertical_align_center),
      (position_set_x, pos1, 270),
      (overlay_set_position, reg0, pos1),

      (create_text_overlay, reg0, "@Sell", tf_vertical_align_center),
      (position_set_x, pos1, 400),
      (overlay_set_position, reg0, pos1),

      (create_text_overlay, reg0, "@If Over:", tf_vertical_align_center),
      (position_set_x, pos1, 455),
      (overlay_set_position, reg0, pos1),

      (create_text_overlay, reg0, "@Min Qty:", tf_vertical_align_center),
      (position_set_x, pos1, 600),
      (overlay_set_position, reg0, pos1),

      (create_text_overlay, reg0, "@Max Qty:", tf_vertical_align_center),
      (position_set_x, pos1, 700),
      (overlay_set_position, reg0, pos1),

      (assign, ":items_per_page", 17), #If changes this also needs to be changed in the state change block
      (store_mul, ":starting_trade_good", ":items_per_page", "$g_auto_trade_page_no"),
      (val_add, ":starting_trade_good", trade_goods_begin),
      (store_add, ":ending_trade_good", ":starting_trade_good", ":items_per_page"),
      (val_min, ":ending_trade_good", trade_goods_end),
      (val_sub, ":pos_y", 30),
      (try_for_range, ":cur_item", ":starting_trade_good", ":ending_trade_good"),

        #Item name column
        (str_store_item_name, s4, ":cur_item"),
        (create_text_overlay, reg0, s4, tf_vertical_align_center),
        (position_set_x, pos1, 50),
        (position_set_y, pos1, ":pos_y"),
        (overlay_set_position, reg0, pos1),

        #Buy price column
        (store_sub, ":number_box_y", ":pos_y", 8),
        (create_number_box_overlay, reg0, 0, 100000),
        (position_set_x, pos1, 275),
        (position_set_y, pos1, ":number_box_y"),
        (item_get_slot, ":buy_under", ":cur_item", slot_item_auto_trade_buy_under_price),
        (overlay_set_val, reg0, ":buy_under"),
        (overlay_set_position, reg0, pos1),
        (troop_set_slot, "trp_temp_array_a", ":cur_item", reg0),

        #Sell price column
        (create_number_box_overlay, reg0, 0, 100000),
        (position_set_x, pos1, 460),
        (item_get_slot, ":sell_over", ":cur_item", slot_item_auto_trade_sell_over_price),
        (overlay_set_val, reg0, ":sell_over"),
        (overlay_set_position, reg0, pos1),
        (troop_set_slot, "trp_temp_array_b", ":cur_item", reg0),
        
        #Buy enabled column
        (store_sub, ":check_box_y", ":pos_y", 5),
        (create_check_box_overlay, reg0, "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 220),
        (position_set_y, pos1, ":check_box_y"),
        (overlay_set_position, reg0, pos1),
        (item_get_slot, ":buy_enabled", ":cur_item", slot_item_auto_trade_buy_enabled),
        (overlay_set_val, reg0, ":buy_enabled"),
        (troop_set_slot, "trp_temp_array_c", ":cur_item", reg0),

        #Sell enabled column
        (create_check_box_overlay, reg0, "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 405),
        (overlay_set_position, reg0, pos1),
        (item_get_slot, ":sell_enabled", ":cur_item", slot_item_auto_trade_sell_enabled),
        (overlay_set_val, reg0, ":sell_enabled"),
        (troop_set_slot, "trp_temp_array_d", ":cur_item", reg0),

        #Minimum Quantity Column
        (create_number_box_overlay, reg0, 0, 100000),
        (position_set_x, pos1, 605),
        (position_set_y, pos1, ":number_box_y"),
        (item_get_slot, ":min_quantity", ":cur_item", slot_item_auto_trade_min_quantity),
        (overlay_set_val, reg0, ":min_quantity"),
        (overlay_set_position, reg0, pos1),
        (troop_set_slot, "trp_temp_array_e", ":cur_item", reg0),

        #Maximum Quantity Column
        (create_number_box_overlay, reg0, 0, 100000),
        (position_set_x, pos1, 705),
        (position_set_y, pos1, ":number_box_y"),
        (item_get_slot, ":max_quantity", ":cur_item", slot_item_auto_trade_max_quantity),
        (overlay_set_val, reg0, ":max_quantity"),
        (overlay_set_position, reg0, pos1),
        (troop_set_slot, "trp_temp_array_f", ":cur_item", reg0),

        (val_sub, ":pos_y", 30),
    
      (try_end),
    ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
        
        (assign, ":items_per_page", 17),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_1"),
          (presentation_set_duration, 0),
        (else_try),
          (eq, ":object", "$g_presentation_obj_2"),
          (assign, "$g_auto_trade_minimum_wealth", ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_3"),
          (assign, "$g_auto_trade_items_when_leaving", ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_4"),
          (store_sub, ":num_trade_goods", trade_goods_end, trade_goods_begin),
          (store_div, ":num_trade_pages", ":num_trade_goods", ":items_per_page"),
          #If there's a remainder add a page for the extra items
          (try_begin),
            (store_mod, ":remainder", ":num_trade_goods", ":items_per_page"),
            (gt, ":remainder", 0),
            (val_add, ":num_trade_pages", 1),
          (try_end),
          (val_add, "$g_auto_trade_page_no", 1),
          (val_mod, "$g_auto_trade_page_no", ":num_trade_pages"),
          (start_presentation, "prsnt_auto_trade_options"),
        (else_try),
          #Iterating through all items caused a bug where changing one page would affect the other(s)
          (store_mul, ":starting_trade_good", ":items_per_page", "$g_auto_trade_page_no"),
          (val_add, ":starting_trade_good", trade_goods_begin),
          (store_add, ":ending_trade_good", ":starting_trade_good", ":items_per_page"),
          (val_min, ":ending_trade_good", trade_goods_end),
          (try_for_range, ":cur_item", ":starting_trade_good", ":ending_trade_good"),
            (try_begin),
              (troop_slot_eq, "trp_temp_array_a", ":cur_item", ":object"),
              (item_set_slot, ":cur_item", slot_item_auto_trade_buy_under_price, ":value"),
            (else_try),
              (troop_slot_eq, "trp_temp_array_b", ":cur_item", ":object"),
              (item_set_slot, ":cur_item", slot_item_auto_trade_sell_over_price, ":value"),
            (else_try),
              (troop_slot_eq, "trp_temp_array_c", ":cur_item", ":object"),
              (item_set_slot, ":cur_item", slot_item_auto_trade_buy_enabled, ":value"),
            (else_try),
              (troop_slot_eq, "trp_temp_array_d", ":cur_item", ":object"),
              (item_set_slot, ":cur_item", slot_item_auto_trade_sell_enabled, ":value"),
            (else_try),
              (troop_slot_eq, "trp_temp_array_e", ":cur_item", ":object"),
              (item_set_slot, ":cur_item", slot_item_auto_trade_min_quantity, ":value"),
            (else_try),
              (troop_slot_eq, "trp_temp_array_f", ":cur_item", ":object"),
              (item_set_slot, ":cur_item", slot_item_auto_trade_max_quantity, ":value"),
            (try_end),
          (try_end),
        (try_end),
    ]),
  ])
