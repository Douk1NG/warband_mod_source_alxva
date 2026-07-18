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

food_options = ("food_options", 0, mesh_load_window, [
    (ti_on_presentation_load, [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        (create_text_overlay, "$g_presentation_food_start", "@Food Consumption", tf_center_justify),
        (position_set_x, pos0, Screen_Width/2),
        #  (position_set_y, pos0, Screen_Title_Height),
        (position_set_y, pos0, 600),
        (overlay_set_position, "$g_presentation_food_start", pos0),

        #  (assign, ":y_pos", Screen_Title_Height-Screen_Text_Height-Screen_Text_Height),
        (assign, ":y_pos", 450),
        (assign, ":x_pos", 50),

        (position_set_x, pos1, 800),
        (position_set_y, pos1, 800),


        #Disable formations option
        (try_for_range, ":item", "itm_raw_date_fruit", food_end),
            (neq, ":item", "itm_furs"),

            (try_begin),
                (gt, ":x_pos", 900),
                (assign, ":x_pos", 50),
                (val_sub, ":y_pos", 100),
            (try_end),

            (position_set_x, pos0, ":x_pos"),
            (position_set_y, pos0, ":y_pos"),
            (create_image_button_overlay, ":cur_obj", "mesh_mp_inventory_slot_empty", "mesh_mp_inventory_slot_empty"),
            (overlay_set_size, ":cur_obj", pos1),
            (overlay_set_position, ":cur_obj", pos0),
            (create_mesh_overlay_with_item_id, reg0, ":item"),
            (item_get_slot, ":edible", ":item", slot_item_edible),
            (try_begin),
              (eq, ":edible", 0),
              (overlay_set_color, reg0, 0x000000),
            (try_end),
            (store_add, ":item_x", ":x_pos", 50),
            (store_add, ":item_y", ":y_pos", 50),
            (position_set_x, pos2, ":item_x"),
            (position_set_y, pos2, ":item_y"),
            (overlay_set_position, reg0, pos2),
            (val_add, ":x_pos", 100),
        (try_end),

        # This is for Done button
        (assign, "$food_options_overlay_exit", 0), # forced initialization
        (create_game_button_overlay, "$food_options_overlay_exit", "str_done"),
        (position_set_x, pos1, 2*Screen_Width/3),
        (position_set_y, pos1, Screen_Border_Width),
        (overlay_set_position, "$food_options_overlay_exit", pos1),
    ]),

    (ti_on_presentation_run, [
        (try_begin),
          (this_or_next|key_clicked, key_escape),
          (key_clicked, key_xbox_start),
          (presentation_set_duration, 0),
        (try_end),
    ]),

    (ti_on_presentation_event_state_change, [
        (store_trigger_param_1, ":object"),
        #(store_trigger_param_2, ":value"),

        (try_begin),
          (eq, ":object", "$food_options_overlay_exit"),
          (presentation_set_duration, 0),
        (else_try),
          (store_sub, ":selected_food", ":object", "$g_presentation_food_start"),
          (val_div, ":selected_food", 2),
          (try_begin),
            (gt, ":selected_food", 0),
            (val_add, ":selected_food", 1),
          (try_end),
          (val_add, ":selected_food", "itm_raw_date_fruit"),
          (str_store_item_name, s0, ":selected_food"),

          (try_begin),
            (item_get_slot, reg1, ":selected_food", slot_item_edible),
            (store_add, ":food_icon", ":object", 1),
            (try_begin),
              (eq, reg1, 1),
              (overlay_set_color, ":food_icon", 0x000000),
            (else_try),
              (overlay_set_color, ":food_icon", 0xFFFFFF),
            (try_end),

            (val_clamp, reg1, 0, 2),
            (store_sub, reg1, 1, reg1),
            (item_set_slot, ":selected_food", slot_item_edible, reg1),
          (try_end),

          (display_message, "@Your party will {reg1?now:no longer} consume {s0}"),
        (try_end),
    ]),
])
