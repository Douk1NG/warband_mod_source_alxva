# -*- coding: cp1254 -*-
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *

# Formation shared UI - hub-aware (mirrors prsnt_formation_mod_option)
# is_hub 0 = standalone mesh_load_window (Screen_* coords), 1 = inside camp_hub container 300,0,650,720
formation_shared_ui_scripts = [
  ("formation_create_ui", [
      (store_script_param, ":is_hub", 1),
      (set_fixed_point_multiplier, 1000),
      (try_begin),
        (eq, ":is_hub", 1),
        # hub: inside scrollable container, parchment coordinates
        # (no inline title — the view name lives on the blue cartouche)
        # Top air: the container pins the highest overlay to the window top,
        # so reserve 170u here — the first row then renders below the title bar
        (create_mesh_overlay, reg1, "mesh_white_plane"),
        (position_set_x, pos1, 20), (position_set_y, pos1, 415), (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 50), (position_set_y, pos1, 50), (overlay_set_size, reg1, pos1),
        (assign, ":y_pos", 245),
        # Disable formations
        (create_text_overlay, reg1, "@Disable mod formations: ", tf_right_align),
        (position_set_x, pos1, 300), (position_set_y, pos1, ":y_pos"), (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 850), (position_set_y, pos1, 850), (overlay_set_size, reg1, pos1),
        (create_check_box_overlay, "$form_options_overlay_1", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 380), (position_set_y, pos1, ":y_pos"), (overlay_set_position, "$form_options_overlay_1", pos1),
        (overlay_set_val, "$form_options_overlay_1", "$FormAI_off"),
        (val_sub, ":y_pos", 40),
        (val_sub, ":y_pos", 55),
        # Player division assignment
        (create_text_overlay, reg1, "@Put player in division: ", tf_right_align),
        (position_set_x, pos1, 300), (position_set_y, pos1, ":y_pos"), (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 850), (position_set_y, pos1, 850), (overlay_set_size, reg1, pos1),
        (create_number_box_overlay, "$form_options_overlay_2", 0, 10),
        (position_set_x, pos1, 380), (position_set_y, pos1, ":y_pos"), (overlay_set_position, "$form_options_overlay_2", pos1),
        (position_set_x, pos1, 800), (position_set_y, pos1, 800), (overlay_set_size, "$form_options_overlay_2", pos1),
        (overlay_set_val, "$form_options_overlay_2", "$FormAI_player_in_division"),
        (store_sub, reg2, "$FormAI_player_in_division", 1),
        (try_begin), (lt, reg2, 0), (str_store_string, s1, "@None"), (else_try), (str_store_class_name, s1, reg2), (try_end),
        (create_text_overlay, reg1, "@{s1}", tf_left_align),
        (position_set_x, pos1, 450), (position_set_y, pos1, ":y_pos"), (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 850), (position_set_y, pos1, 850), (overlay_set_size, reg1, pos1),
        (val_sub, ":y_pos", 40),
        # Autorotate
        (create_text_overlay, reg1, "@Army rotates to face enemy center: ", tf_right_align),
        (position_set_x, pos1, 300), (position_set_y, pos1, ":y_pos"), (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 850), (position_set_y, pos1, 850), (overlay_set_size, reg1, pos1),
        (create_check_box_overlay, "$form_options_overlay_3", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 380), (position_set_y, pos1, ":y_pos"), (overlay_set_position, "$form_options_overlay_3", pos1),
        (overlay_set_val, "$form_options_overlay_3", "$FormAI_autorotate"),
        (val_sub, ":y_pos", 40),
        # Prevent AI defensive
        (create_text_overlay, reg1, "@Prevent AI from taking defensive: ", tf_right_align),
        (position_set_x, pos1, 300), (position_set_y, pos1, ":y_pos"), (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 850), (position_set_y, pos1, 850), (overlay_set_size, reg1, pos1),
        (create_check_box_overlay, "$form_options_overlay_4", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 380), (position_set_y, pos1, ":y_pos"), (overlay_set_position, "$form_options_overlay_4", pos1),
        (overlay_set_val, "$form_options_overlay_4", "$FormAI_AI_no_defense"),
        # no Done in hub - hub's Done handles it
      (else_try),
        # standalone - original Screen_* layout on mesh_load_window
        (create_text_overlay, reg1, "@Extended Formations and AI Options", tf_center_justify),
        (position_set_x, pos1, 512), (position_set_y, pos1, 600), (overlay_set_position, reg1, pos1),
        (assign, ":y_pos", 450),
        (create_text_overlay, reg1, "@Disable mod formations: ", tf_right_align),
        (position_set_x, pos1, 512), (position_set_y, pos1, ":y_pos"), (overlay_set_position, reg1, pos1),
        (create_check_box_overlay, "$form_options_overlay_1", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 512), (store_add, reg2, ":y_pos", 7), (position_set_y, pos1, reg2), (overlay_set_position, "$form_options_overlay_1", pos1),
        (overlay_set_val, "$form_options_overlay_1", "$FormAI_off"),
        (val_sub, ":y_pos", 40),
        (create_text_overlay, reg1, "@Put player in division: ", tf_right_align),
        (position_set_x, pos1, 512), (position_set_y, pos1, ":y_pos"), (overlay_set_position, reg1, pos1),
        (create_number_box_overlay, "$form_options_overlay_2", 0, 10),
        (position_set_x, pos1, 512), (position_set_y, pos1, ":y_pos"), (overlay_set_position, "$form_options_overlay_2", pos1),
        (overlay_set_val, "$form_options_overlay_2", "$FormAI_player_in_division"),
        (store_sub, reg2, "$FormAI_player_in_division", 1),
        (try_begin), (lt, reg2, 0), (str_store_string, s1, "@None"), (else_try), (str_store_class_name, s1, reg2), (try_end),
        (create_text_overlay, reg1, "@{s1}", tf_left_align),
        (position_set_x, pos1, 650), (position_set_y, pos1, ":y_pos"), (overlay_set_position, reg1, pos1),
        (val_sub, ":y_pos", 40),
        (create_text_overlay, reg1, "@Army rotates to face enemy center: ", tf_right_align),
        (position_set_x, pos1, 512), (position_set_y, pos1, ":y_pos"), (overlay_set_position, reg1, pos1),
        (create_check_box_overlay, "$form_options_overlay_3", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 512), (store_add, reg2, ":y_pos", 7), (position_set_y, pos1, reg2), (overlay_set_position, "$form_options_overlay_3", pos1),
        (overlay_set_val, "$form_options_overlay_3", "$FormAI_autorotate"),
        (val_sub, ":y_pos", 40),
        (create_text_overlay, reg1, "@Prevent AI from taking defensive: ", tf_right_align),
        (position_set_x, pos1, 512), (position_set_y, pos1, ":y_pos"), (overlay_set_position, reg1, pos1),
        (create_check_box_overlay, "$form_options_overlay_4", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 512), (store_add, reg2, ":y_pos", 7), (position_set_y, pos1, reg2), (overlay_set_position, "$form_options_overlay_4", pos1),
        (overlay_set_val, "$form_options_overlay_4", "$FormAI_AI_no_defense"),
        (val_sub, ":y_pos", 40),
        (create_game_button_overlay, "$form_options_overlay_exit", "str_done"),
        (position_set_x, pos1, 683), (position_set_y, pos1, 25), (overlay_set_position, "$form_options_overlay_exit", pos1),
      (try_end),
  ]),
  ("formation_handle_event", [
      (store_script_param, ":object", 1),
      (store_script_param, ":value", 2),
      (try_begin),
        (eq, ":object", "$form_options_overlay_1"), (assign, "$FormAI_off", ":value"),
      (else_try), (eq, ":object", "$form_options_overlay_2"), (assign, "$FormAI_player_in_division", ":value"), (start_presentation, "prsnt_camp_hub"),
      (else_try), (eq, ":object", "$form_options_overlay_3"), (assign, "$FormAI_autorotate", ":value"),
      (else_try), (eq, ":object", "$form_options_overlay_4"), (assign, "$FormAI_AI_no_defense", ":value"),
      (else_try), (eq, ":object", "$form_options_overlay_exit"), (presentation_set_duration, 0),
      (try_end),
  ]),
]
