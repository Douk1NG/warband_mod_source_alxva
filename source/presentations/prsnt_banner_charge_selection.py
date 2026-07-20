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

banner_charge_selection = ("banner_charge_selection", 0, mesh_load_window,
   [
     (ti_on_presentation_load,
      [
        (set_fixed_point_multiplier, 1000),
        (create_text_overlay, reg1, "str_choose_charge", tf_center_justify),

        (position_set_x, pos1, 500),
        (position_set_y, pos1, 650),
        (overlay_set_position, reg1, pos1),
        (assign, ":pos_x", 100),
        (assign, ":pos_y", 600),
        (try_for_range, ":cur_charge", custom_banner_charges_begin, custom_banner_charges_end),
          (create_image_button_overlay, reg1, ":cur_charge", ":cur_charge"),
          (position_set_x, pos1, ":pos_x"),
          (position_set_y, pos1, ":pos_y"),
          (val_add, ":pos_x", 100),
          (try_begin),
            (gt, ":pos_x", 900),
            (assign, ":pos_x", 100),
            (val_sub, ":pos_y", 100),
          (try_end),
          (overlay_set_position, reg1, pos1),
          (position_set_x, pos1, 80),
          (position_set_y, pos1, 80),
          (overlay_set_size, reg1, pos1),
          (store_sub, ":slot_index", ":cur_charge", custom_banner_charges_begin),
          (troop_set_slot, "trp_temp_array_a", ":slot_index", reg1),
        (try_end),
        (presentation_set_duration, 999999),
        ]),
     (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (assign, ":end_cond", custom_banner_charges_end),
        (val_sub, ":end_cond", custom_banner_charges_begin),
        (try_for_range, ":trp_slot_index", 0, ":end_cond"),
          (troop_slot_eq, "trp_temp_array_a", ":trp_slot_index", ":object"),
          (troop_set_slot, "$g_edit_banner_troop", "$g_presentation_output_slot", ":trp_slot_index"),
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
