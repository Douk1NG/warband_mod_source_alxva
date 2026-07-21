# -*- coding: cp1254 -*-
import string
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
from header_terrain_types import *
from module_items import *
from module_factions import *
from header_items import *
from compiler import *

cc_relations_with_lords_by_faction = ("cc_relations_with_lords_by_faction", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        (assign, ":cur_faction", "$temp"),
        (str_store_faction_name, s1, ":cur_faction"),

        (create_text_overlay, reg1, "@Relation with the lords of {s1}", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 670),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 1500),
        (position_set_y, pos1, 1500),
        (overlay_set_size, reg1, pos1),

        (str_clear, s0),
        (create_text_overlay, "$g_presentation_obj_6", s0, tf_scrollable),
        (position_set_x, pos1, 15),
        (position_set_y, pos1, 80),
        (overlay_set_position, "$g_presentation_obj_6", pos1),
        (position_set_x, pos1, 950),
        (position_set_y, pos1, 570),
        (overlay_set_area_size, "$g_presentation_obj_6", pos1),
        (set_container_overlay, "$g_presentation_obj_6"),

        (assign, ":num_fit_lords", 0),
        (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
          (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
          (store_faction_of_troop, ":troop_faction", ":active_npc"),
          (eq, ":troop_faction", ":cur_faction"),
          (val_add, ":num_fit_lords", 1),
        (try_end),

        (assign, ":x_offset", 180),
        (assign, ":y_offset", 180),
        (store_mod, ":mod_value", ":num_fit_lords", 5),
        (try_begin),
          (eq, ":mod_value", 0),
          (assign, ":mod_value", 5),
        (try_end),
        (store_mul, ":cur_x", ":mod_value", ":x_offset"),
        (val_sub, ":cur_x", ":x_offset"),
        (val_add, ":cur_x", 35),
        (try_begin),
          (is_between, ":num_fit_lords", 1, 6),
          (assign, ":cur_y", 455),
        (else_try),
          (is_between, ":num_fit_lords", 6, 11),
          (assign, ":cur_y", 275),
        (else_try),
          (assign, ":cur_y", 95),
        (try_end),

        (try_for_range_backwards, ":active_npc", "trp_kingdom_heroes_including_player_begin", active_npcs_end),
          (assign, ":continue", 0),
          (try_begin),
            (eq, ":active_npc", "trp_kingdom_heroes_including_player_begin"), # add the king back
            (faction_get_slot, ":cur_faction_leader", ":cur_faction", slot_faction_leader),
            (assign, ":active_npc", ":cur_faction_leader"),
            (assign, ":continue", 1),
          (else_try),
            (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
            (store_faction_of_troop, ":troop_faction", ":active_npc"),
            (eq, ":troop_faction", ":cur_faction"),
            (neg|faction_slot_eq, ":cur_faction", slot_faction_leader, ":active_npc"), # exclude the king first
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (call_script, "script_troop_get_player_relation", ":active_npc"),
          (assign, ":cur_relation", reg0),

          # bar
          (create_mesh_overlay, reg1, "mesh_relation_bar_vertical"),
          (store_add, ":bar_x", ":cur_x", 20),
          (store_add, ":bar_y", ":cur_y", 45),
          (position_set_x, pos1, ":bar_x"),
          (position_set_y, pos1, ":bar_y"),
          (overlay_set_position, reg1, pos1),
          # pointer
          (create_mesh_overlay, reg1, "mesh_reln_pointer_vertical"),
          (store_sub, ":pointer_y", ":cur_relation", -100),
          (val_div, ":pointer_y", 2),
          (val_add, ":pointer_y", ":cur_y"),
          (val_add, ":pointer_y", 45),
          (store_add, ":pointer_x", ":cur_x", 20),
          (position_set_x, pos1, ":pointer_x"),
          (position_set_y, pos1, ":pointer_y"),
          (overlay_set_position, reg1, pos1),
          # name
          (store_add, ":name_x", ":cur_x", 80),
          (assign, ":name_y", ":cur_y"),
          (str_store_troop_name, s1, ":active_npc"),
          (create_text_overlay, reg1, "@{s1}", tf_center_justify),
          (position_set_x, pos1, ":name_x"),
          (position_set_y, pos1, ":name_y"),
          (overlay_set_position, reg1, pos1),
          # relation
          (store_add, ":text_x", ":cur_x", 35),
          (store_add, ":text_y", ":cur_y", 100),
          (assign, reg0, ":cur_relation"),
          (create_text_overlay, reg1, "@{reg0}", tf_center_justify),
          (position_set_x, pos1, ":text_x"),
          (position_set_y, pos1, ":text_y"),
          (overlay_set_position, reg1, pos1),
          (position_set_x, pos1, 750),
          (position_set_y, pos1, 750),
          (overlay_set_size, reg1, pos1),

          # troop
          (store_add, ":troop_x", ":cur_x", 20),
          (store_add, ":troop_y", ":cur_y", 35),
          (create_mesh_overlay_with_tableau_material, reg1, -1, "tableau_troop_note_mesh", ":active_npc"),
          (position_set_x, pos1, 320),
          (position_set_y, pos1, 320),
          (overlay_set_size, reg1, pos1),
          (position_set_x, pos1, ":troop_x"),
          (position_set_y, pos1, ":troop_y"),
          (overlay_set_position, reg1, pos1),

          (val_sub, ":cur_x", ":x_offset"),
          (try_begin),
            (eq, ":cur_x", -145),
            (assign, ":cur_x", 755),
            (val_add, ":cur_y", ":y_offset"),
          (try_end),
        (try_end),
        (set_container_overlay, -1),

        # Done
        (create_game_button_overlay, "$g_presentation_obj_5", "@Done"),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 25),
        (overlay_set_position, "$g_presentation_obj_5", pos1),
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_5"),
          (start_presentation, "prsnt_cc_relations_with_factions"),
        (try_end),
    ]),
  ])
