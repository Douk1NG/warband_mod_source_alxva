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

formation_mod_option = ("formation_mod_option", 0, mesh_load_window, [
    (ti_on_presentation_load, [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
        (create_text_overlay, reg1, "@Extended Formations and AI Options", tf_center_justify),
        (position_set_x, pos0, Screen_Width/2),
        #  (position_set_y, pos0, Screen_Title_Height),
        (position_set_y, pos0, 600),
        (overlay_set_position, reg1, pos0),

        #  (assign, ":y_pos", Screen_Title_Height-Screen_Text_Height-Screen_Text_Height),
        (assign, ":y_pos", 450),

        #Disable formations option
        (create_text_overlay, reg1, "@Disable mod formations: ", tf_right_align),
        (position_set_y, pos0, ":y_pos"),
        (overlay_set_position, reg1, pos0),

        (create_check_box_overlay, "$form_options_overlay_1", "mesh_checkbox_off", "mesh_checkbox_on"),
        (copy_position, pos1, pos0),
        (store_add, reg2, ":y_pos", Screen_Checkbox_Height_Adj),
        (position_set_y, pos1, reg2),
        (overlay_set_position, "$form_options_overlay_1", pos1),

        (overlay_set_val, "$form_options_overlay_1", "$FormAI_off"),

        (val_sub, ":y_pos", Screen_Text_Height),

        #Player division assignment
        (create_text_overlay, reg1, "@Put player in division: ", tf_right_align),
        (position_set_y, pos0, ":y_pos"),
        (overlay_set_position, reg1, pos0),

        (create_number_box_overlay, "$form_options_overlay_2", 0, 10),
        (copy_position, pos1, pos0),
        (overlay_set_position, "$form_options_overlay_2", pos0),

        (overlay_set_val, "$form_options_overlay_2", "$FormAI_player_in_division"),

        (store_sub, reg2, "$FormAI_player_in_division", 1),
        (try_begin),
          (lt, reg2, 0),
          (str_store_string, s1, "@None"),
        (else_try),
          (str_store_class_name, s1, reg2),
        (try_end),
        (create_text_overlay, reg1, "@{s1}", tf_left_align),
        (copy_position, pos1, pos0),
        (store_add, reg2, Screen_Width/2, Screen_Numberbox_Width+5),
        (position_set_x, pos1, reg2),
        (overlay_set_position, reg1, pos1),

        (val_sub, ":y_pos", Screen_Text_Height),

        #Autorotate formations option
        (create_text_overlay, reg1, "@Army rotates to face enemy center: ", tf_right_align),
        (position_set_y, pos0, ":y_pos"),
        (overlay_set_position, reg1, pos0),

        (create_check_box_overlay, "$form_options_overlay_3", "mesh_checkbox_off", "mesh_checkbox_on"),
        (copy_position, pos1, pos0),
        (store_add, reg2, ":y_pos", Screen_Checkbox_Height_Adj),
        (position_set_y, pos1, reg2),
        (overlay_set_position, "$form_options_overlay_3", pos1),

        (overlay_set_val, "$form_options_overlay_3", "$FormAI_autorotate"),

        (val_sub, ":y_pos", Screen_Text_Height),

        #Prevent AI from taking defensive
        (create_text_overlay, reg1, "@Prevent AI from taking defensive: ", tf_right_align),
        (position_set_y, pos0, ":y_pos"),
        (overlay_set_position, reg1, pos0),

        (create_check_box_overlay, "$form_options_overlay_4", "mesh_checkbox_off", "mesh_checkbox_on"),
        (copy_position, pos1, pos0),
        (store_add, reg2, ":y_pos", Screen_Checkbox_Height_Adj),
        (position_set_y, pos1, reg2),
        (overlay_set_position, "$form_options_overlay_4", pos1),

        (overlay_set_val, "$form_options_overlay_4", "$FormAI_AI_no_defense"),

        (val_sub, ":y_pos", Screen_Text_Height),

        # This is for Done button
        (assign, "$form_options_overlay_exit", 0), # forced initialization
        (create_game_button_overlay, "$form_options_overlay_exit", "str_done"),
        (position_set_x, pos1, 2*Screen_Width/3),
        (position_set_y, pos1, Screen_Border_Width),
        (overlay_set_position, "$form_options_overlay_exit", pos1),
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
        (store_trigger_param_2, ":value"),

        (try_begin),
          (eq, ":object", "$form_options_overlay_1"),
          (assign, "$FormAI_off", ":value"),
        (else_try),
          (eq, ":object", "$form_options_overlay_2"),
          (assign, "$FormAI_player_in_division", ":value"),
          (start_presentation, "prsnt_formation_mod_option"),
        (else_try),
          (eq, ":object", "$form_options_overlay_3"),
          (assign, "$FormAI_autorotate", ":value"),
        (else_try),
          (eq, ":object", "$form_options_overlay_4"),
          (assign, "$FormAI_AI_no_defense", ":value"),
        (else_try),
          (eq, ":object", "$form_options_overlay_exit"),
          (presentation_set_duration, 0),
        (try_end),
    ]),
])
