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

color_selection = ("color_selection", 0, mesh_load_window,
   [
     (ti_on_presentation_load,
      [
        (set_fixed_point_multiplier, 1000),
        (create_text_overlay, reg1, "str_choose_color", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 600),
        (overlay_set_position, reg1, pos1),

        (assign, ":pos_x", 125),
        (assign, ":pos_y", 450),
        (try_for_range, ":i_color", 0, 42),
          (call_script, "script_get_custom_banner_color_from_index", ":i_color"),
          (assign, ":cur_color", reg0),
          (create_image_button_overlay_with_tableau_material, reg1, "mesh_color_picker", "tableau_color_picker", ":cur_color"),
          (position_set_x, pos1, ":pos_x"),
          (position_set_y, pos1, ":pos_y"),
          (val_add, ":pos_x", 50),
          (try_begin),
            (store_mod, ":mod_i_color", ":i_color", 7),
            (eq, ":mod_i_color", 6),
            (assign, ":pos_x", 125),
            (val_sub, ":pos_y", 50),
          (try_end),
          (overlay_set_position, reg1, pos1),
          (position_set_x, pos1, 500),
          (position_set_y, pos1, 500),
          (overlay_set_size, reg1, pos1),
          (store_mul, ":trp_slot_index", ":i_color", 2),
          (store_add, ":trp_slot_color", ":trp_slot_index", 1),
          (troop_set_slot, "trp_temp_array_a", ":trp_slot_index", reg1),
          (troop_set_slot, "trp_temp_array_a", ":trp_slot_color", ":cur_color"),
        (try_end),
        (presentation_set_duration, 999999),
        ]),
     (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (assign, ":end_cond", 64),
        (try_for_range, ":i_color", 0, ":end_cond"),
          (store_mul, ":trp_slot_index", ":i_color", 2),
          (troop_slot_eq, "trp_temp_array_a", ":trp_slot_index", ":object"),
          (store_add, ":trp_slot_color", ":trp_slot_index", 1),
          (troop_get_slot, ":output_color", "trp_temp_array_a", ":trp_slot_color"),
          (troop_set_slot, "$g_edit_banner_troop", "$g_presentation_output_slot", ":output_color"),
          (assign, ":end_cond", 0),
        (try_end),
        (try_begin),
          (gt, "$g_presentation_next_presentation", 0),
          (start_presentation, "$g_presentation_next_presentation"),
        (else_try),
          (presentation_set_duration, 0),
        (try_end),
        ]),
     ])
