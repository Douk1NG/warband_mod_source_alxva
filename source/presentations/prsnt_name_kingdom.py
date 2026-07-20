# ======================================================================
# SHARED DEPENDENCY
# Entity: name_kingdom (presentation)
# Called by menus in 5 domains: camp, character_creation, cheats, kingdom_management, town
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

name_kingdom = ("name_kingdom",0,mesh_load_window,[
      (ti_on_presentation_load,
       [(set_fixed_point_multiplier, 1000),
        # (str_store_string, s1, "str_name_kingdom_text"),
        #SB : set up text label
        (try_begin),
          (neg|is_between, "$g_presentation_state", rename_kingdom, rename_companion + 1),
          (assign, "$g_presentation_state", rename_kingdom),
        (try_end),
        (store_add, ":string", "str_name_presentation_text", "$g_presentation_state"),
        (str_store_string, s1, ":string"),
        (create_text_overlay, reg1, "str_name_presentation_text", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 500),
        (overlay_set_position, reg1, pos1),

        (create_simple_text_box_overlay, "$g_presentation_obj_name_kingdom_1"),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 400),
        (overlay_set_position, "$g_presentation_obj_name_kingdom_1", pos1),
        (assign, "$g_presentation_obj_banner_selection_1", -1),
        #SB : set up text box
        (try_begin),
          (eq, "$g_presentation_state", rename_kingdom),
          (try_begin),
            (store_and, ":name_set", "$players_kingdom_name_set", rename_kingdom),
            (eq, ":name_set", 1),
            (str_store_faction_name, s7, "fac_player_supporters_faction"),
          (else_try), #SB : kingdom naming based off first captured center, assigned to g_player_court
            (is_between, "$g_player_court", towns_begin, towns_end),
            (str_store_party_name, s7, "$g_player_court"),
            (str_store_string, s7, "@Kingdom of {s7}"), #castles can also be courts but we can't get the original name
          (else_try),
            (str_store_troop_name, s0, "trp_player"),
            (str_store_string, s7, "str_default_kingdom_name"),
          (try_end),
          #SB : add in the color option
          (eq, "$g_presentation_state", rename_kingdom),
          (create_button_overlay, "$g_presentation_obj_banner_selection_1", "str_color", tf_center_justify),
          (position_set_x, pos1, 500),
          (position_set_y, pos1, 300),
          (overlay_set_position, "$g_presentation_obj_banner_selection_1", pos1),
          (faction_get_color, ":color", "$players_kingdom"),
          (overlay_set_color, "$g_presentation_obj_banner_selection_1", ":color"),
        (else_try),
          (eq, "$g_presentation_state", rename_center),
          (str_store_party_name, s7, "$g_player_court"),
        (else_try),
          (eq, "$g_presentation_state", rename_party),
          (str_store_party_name, s7, "$g_encountered_party"),
        (else_try),
          (eq, "$g_presentation_state", rename_companion),
          (str_store_troop_name_plural, s7, "$g_player_troop"),
        (try_end),
        (overlay_set_text, "$g_presentation_obj_name_kingdom_1", s7),

        (create_button_overlay, "$g_presentation_obj_name_kingdom_2", "@Continue...", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 150),
        (overlay_set_position, "$g_presentation_obj_name_kingdom_2", pos1),
        # (create_button_overlay, "$g_presentation_obj_2", "str_continue", tf_center_justify),
        # (position_set_x, pos1, 500),
        # (position_set_y, pos1, 300),
        # (overlay_set_position, "$g_presentation_obj_2", pos1),

        (presentation_set_duration, 999999),
        ]),
      (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        (try_begin),
          (eq, ":object", "$g_presentation_obj_name_kingdom_1"),
          (str_store_string, s7, s0),
        (else_try),
          (eq, ":object", "$g_presentation_obj_name_kingdom_2"),
          (try_begin),
            (eq, "$g_presentation_state", rename_kingdom),
            (try_begin),
              (store_and, ":color_set", "$players_kingdom_name_set", rename_kingdom),
              (this_or_next|ge, "$cheat_mode", 1),
              (eq, ":color_set", 0),
              (troop_get_slot, ":banner", "$g_player_troop", slot_troop_banner_scene_prop),
              (gt, ":banner", 0),
              (val_sub, ":banner", banner_scene_props_begin),
              (troop_get_slot, ":color", "trp_banner_background_color_array", ":banner"),
              (gt, ":color", 0),
              (faction_set_color, "fac_player_supporters_faction", ":color"),
            (try_end),
            (faction_set_name, "fac_player_supporters_faction", s7),
            (val_or, "$players_kingdom_name_set", rename_kingdom),
          (else_try),
            (eq, "$g_presentation_state", rename_party),
            (party_set_name, "$g_encountered_party", s7),
          (else_try),
            (eq, "$g_presentation_state", rename_center),
            (try_begin), #probably add the feast requirement here
              (troop_is_hero, "$g_player_minister"),
              (store_skill_level, ":persuasion", "skl_persuasion", "$g_player_minister"),
              (store_sub, ":persuasion", 15, ":persuasion"),
              (call_script, "script_change_player_relation_with_center", "$g_player_court", ":persuasion"),
            (try_end),
            (party_set_name, "$g_player_court", s7),
            (val_or, "$players_kingdom_name_set", rename_center),
          (else_try),
            (eq, "$g_presentation_state", rename_companion),
            (troop_set_name, "$g_player_troop", s7),
            (troop_set_plural_name, "$g_player_troop", s7),
            (try_begin), #SB : set from title now that we've changed the base name
              (troop_slot_eq, "$g_player_troop", slot_troop_occupation, slto_kingdom_hero),
              (store_faction_of_troop, ":faction_no", "$g_player_troop"),
              (call_script, "script_troop_set_title_according_to_faction", "$g_player_troop", ":faction_no"),
            (try_end),
          (try_end),
          # (faction_set_name, "fac_player_supporters_faction", s7),
          # (faction_set_color, "fac_player_supporters_faction", 0xFF0000),
          # (assign, "$players_kingdom_name_set", 1),
          (presentation_set_duration, 0),
        (else_try), #SB : jump to recoloring kingdom(s)
          (eq, ":object", "$g_presentation_obj_banner_selection_1"),
          (eq, "$g_presentation_state", rename_kingdom), #carried over
          (assign, "$temp", 9), #player kingdom
          (assign, "$g_presentation_next_presentation", "prsnt_name_kingdom"),
          (assign, "$g_presentation_state", recolor_kingdom), #carried over
          (start_presentation, "prsnt_change_color"),
        (try_end),
        ]),
      ])
