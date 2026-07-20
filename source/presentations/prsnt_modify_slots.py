# ======================================================================
# SHARED DEPENDENCY
# Entity: modify_slots (presentation)
# Called by menus in 2 domains: kingdom_management, town
# ======================================================================

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

modify_slots = ("modify_slots", 0, 0, [
    (ti_on_presentation_load,
      [ (set_show_messages, 0),
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        (create_mesh_overlay, reg0, "mesh_message_window"),
        (position_set_x, pos1, 224),
        (position_set_y, pos1, 230),
        (overlay_set_position, reg0, pos1),

        (try_begin),
          (eq, "$g_presentation_input", rename_center),
          (party_get_slot, ":slot_value", "$g_encountered_party", "$g_presentation_state"),
        (else_try),
          (eq, "$g_presentation_input", rename_companion),
          (troop_get_slot, ":slot_value", "$g_talk_troop", "$g_presentation_state"),
        (else_try),
          (eq, "$g_presentation_input", rename_kingdom),
          (faction_get_slot, ":slot_value", "$g_cheat_selected_faction", "$g_presentation_state"),
        (try_end),
        (assign, reg1, ":slot_value"),
        (create_text_overlay, reg0, "@{reg1}^value", tf_center_justify|tf_vertical_align_center),
        (position_set_x, pos1, 630),
        (position_set_y, pos1, 320),
        (overlay_set_position, reg0, pos1),

        (assign, reg2, "$g_presentation_state"),
        (create_text_overlay, reg0, "@{reg2}^index", tf_center_justify|tf_vertical_align_center),
        (position_set_x, pos1, 370),
        (position_set_y, pos1, 320),
        (overlay_set_position, reg0, pos1),

        (position_set_x, pos1, 340),
        (position_set_y, pos1, 380),
        (create_number_box_overlay, "$g_presentation_obj_1", 0, 1000),
        (overlay_set_position, "$g_presentation_obj_1", pos1),
        (overlay_set_val, "$g_presentation_obj_1", "$g_presentation_state"),

        (position_set_x, pos1, 600),
        (position_set_y, pos1, 380),
        (create_number_box_overlay, "$g_presentation_obj_2", -10000, 10000), #probably sufficient
        (overlay_set_position, "$g_presentation_obj_2", pos1),
        (overlay_set_val, "$g_presentation_obj_2", ":slot_value"),

        # (create_game_button_overlay, "$g_presentation_obj_3", "str_done"),
        (try_begin),
          (eq, "$g_presentation_input", rename_center),
          (str_store_party_name, s1, "$g_encountered_party"),
        (else_try),
          (eq, "$g_presentation_input", rename_companion),
          (str_store_troop_name, s1, "$g_talk_troop"),
        (else_try),
          (eq, "$g_presentation_input", rename_kingdom),
          (str_store_faction_name, s1, "$g_cheat_selected_faction"),
        (try_end),
        (create_game_button_overlay, "$g_presentation_obj_3", s1),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 250),
        (overlay_set_position, "$g_presentation_obj_3", pos1),
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_begin), #change slots
          (eq, ":object", "$g_presentation_obj_1"),
          (assign, "$g_presentation_state", ":value"),
          (start_presentation, "prsnt_modify_slots"),
        (else_try), #change values
          (eq, ":object", "$g_presentation_obj_2"),
          (try_begin),
            (eq, "$g_presentation_input", rename_center),
            (party_set_slot, "$g_encountered_party", "$g_presentation_state", ":value"),
          (else_try),
            (eq, "$g_presentation_input", rename_companion),
            (troop_set_slot, "$g_talk_troop", "$g_presentation_state", ":value"),
          (else_try),
            (eq, "$g_presentation_input", rename_kingdom),
            (faction_set_slot, "$g_cheat_selected_faction", "$g_presentation_state", ":value"),
          (try_end),
          # (start_presentation, "prsnt_modify_slots"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_3"),
          (set_show_messages, 1),
          (presentation_set_duration, 0),
        (try_end),
    ]),
  ])
