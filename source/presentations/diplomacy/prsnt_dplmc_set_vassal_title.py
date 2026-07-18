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

dplmc_set_vassal_title = ("dplmc_set_vassal_title",0,mesh_load_window, [
      (ti_on_presentation_load,
       [(set_fixed_point_multiplier, 1000),
        (str_clear, s1),
        (str_clear, s2),

        (create_text_overlay, reg0, "@How will your male vassals be known?", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 600),
        (overlay_set_position, reg0, pos1),
        (create_text_overlay, reg0, "@How will your female vassals be known?", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 400),
        (overlay_set_position, reg0, pos1),

        (create_simple_text_box_overlay, "$g_presentation_obj_name_kingdom_1"),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 500),
        (overlay_set_position, "$g_presentation_obj_name_kingdom_1", pos1),
        (try_begin),
          (troop_slot_eq, "trp_heroes_end", 0, 1), #Pick a slot
          (str_store_troop_name, s0, "trp_heroes_end"),
        (else_try), #SB : str_clear, offset for npc kingdom titles
          (str_clear, s0),
          (store_sub, ":string", "$players_kingdom", kingdoms_begin),
          (val_add, ":string", "str_faction_title_male_player"),
          (str_store_string, s0, ":string"),
        (try_end),
        (overlay_set_text, "$g_presentation_obj_name_kingdom_1", s0),

        (create_simple_text_box_overlay, reg0),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 300),
        (overlay_set_position, reg0, pos1),
        (try_begin),
          (troop_slot_eq, "trp_heroes_end", 1, 1), #Pick a slot
          (str_store_troop_name_plural, s0, "trp_heroes_end"),
        (else_try),  #SB : str_clear
          (str_clear, s0),
          (store_sub, ":string", "$players_kingdom", kingdoms_begin),
          (val_add, ":string", "str_faction_title_female_player"),
          (str_store_string, s0, ":string"),
        (try_end),
        (overlay_set_text, reg0, s0),

        #SB : use actual buttons and center
        (create_game_button_overlay, reg0, "str_done", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 150),
        (overlay_set_position, reg0, pos1),

        (create_game_button_overlay, reg0, "str_reset_to_default", tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 100),
        (overlay_set_position, reg0, pos1),

        #SB : add tableau figures to the sides
        (assign, ":left_figure", "trp_quick_battle_6_player"),
        (assign, ":right_figure", "trp_knight_1_1_wife"),

        (assign, ":left_score", 0),
        (assign, ":right_score", 0),
        (assign, "$lord_selected", 0),
        #show spouses first
        (try_begin),
          (troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
          (is_between, ":spouse", heroes_begin, heroes_end),
          (try_begin),
            (call_script, "script_cf_dplmc_troop_is_female", ":spouse"),
            (assign, ":right_figure", ":spouse"),
            (assign, ":right_score", 9999),
          (else_try),
            (assign, ":left_figure", ":spouse"),
            (assign, ":left_score", 9999),
          (try_end),
        (try_end),
        #otherwise criteria is highest renown/age
        (try_for_range, ":troop_no", heroes_begin, heroes_end),
          (store_faction_of_troop, ":faction_no", ":troop_no"),
          (eq, ":faction_no", "$players_kingdom"),
          (troop_get_slot, ":occupation", ":troop_no", slot_troop_occupation),
          (try_begin),
            (eq, ":occupation", slto_kingdom_hero),
            (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
            (try_begin), #female lords
              (call_script, "script_cf_dplmc_troop_is_female", ":troop_no"),
              (lt, ":right_score", ":renown"),
              (assign, ":right_figure", ":troop_no"),
            (else_try),
              (lt, ":left_score", ":renown"),
              (assign, ":left_figure", ":troop_no"),
            (try_end),
          (else_try),
            (eq, ":occupation", slto_kingdom_lady),
            (troop_get_slot, ":renown", ":troop_no", slot_troop_age),
            (lt, ":right_score", ":renown"),
            (assign, ":right_figure", ":troop_no"),
          (try_end),
        (try_end),
        (init_position, pos1),
        #480x320 instead of 600x600 for retirement tableau
        (create_mesh_overlay_with_tableau_material, reg1, -1, "tableau_dplmc_lord_profile", ":left_figure"),
        (position_set_x, pos1, 10),
        (position_set_y, pos1, 100),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 750),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg1, pos1),

        (create_mesh_overlay_with_tableau_material, reg1, -1, "tableau_dplmc_lord_profile", ":right_figure"),
        (position_set_x, pos1, 750),
        (position_set_y, pos1, 100),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 750),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg1, pos1),
        (presentation_set_duration, 999999),
        ]),
      (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        (try_begin),
          (eq, ":object", "$g_presentation_obj_name_kingdom_1"),
          (str_store_string, s1, s0), #Male Title
        (else_try),
          (store_add, ":overlay", "$g_presentation_obj_name_kingdom_1", 1),
          (eq, ":object", ":overlay"),
          (str_store_string, s2, s0), ##Female Title
        (else_try),
          (val_add, ":overlay", 1),
          (eq, ":object", ":overlay"), #Custom
          (try_begin),
            (neg|str_is_empty, s1),
            (troop_set_name, "trp_heroes_end", s1),
            (troop_set_slot, "trp_heroes_end", 0, 1),
            (try_for_range, ":lord_lady", lords_begin, lords_end),
                (store_troop_faction, ":faction", ":lord_lady"),
                (eq, ":faction", "$players_kingdom"), #SB : change to players_kingdom, flip next script params
                (call_script, "script_troop_set_title_according_to_faction", ":lord_lady", "fac_player_supporters_faction"),
            (try_end),
          (try_end),
          (try_begin),
            (neg|str_is_empty, s2),
            (troop_set_plural_name, "trp_heroes_end", s2),
            (troop_set_slot, "trp_heroes_end", 1, 1),
            (try_for_range, ":lord_lady", kingdom_ladies_begin, kingdom_ladies_end),
                (store_troop_faction, ":faction", ":lord_lady"),
                (eq, ":faction", "$players_kingdom"), #SB : chance to players_kingdom
                (call_script, "script_troop_set_title_according_to_faction", ":lord_lady", "fac_player_supporters_faction"),
            (try_end),
          (try_end),
          (try_begin),
            (this_or_next|neg|str_is_empty, s1),
            (neg|str_is_empty, s2),
            (try_for_range, ":lord_lady", companions_begin, companions_end),
                (store_troop_faction, ":faction", ":lord_lady"),
                (eq, ":faction", "$players_kingdom"), #SB : chance to players_kingdom
                (troop_slot_eq, ":lord_lady", slot_troop_occupation, slto_kingdom_hero),
                (call_script, "script_troop_set_title_according_to_faction", ":lord_lady", "fac_player_supporters_faction"),
            (try_end),
          (try_end),
          (presentation_set_duration, 0),
        (else_try),
          (val_add, ":overlay", 1),
          (eq, ":object", ":overlay"), #Default
          (troop_set_slot, "trp_heroes_end", 0, 0),
          (troop_set_slot, "trp_heroes_end", 1, 0),
          (try_for_range, ":lord_lady", lords_begin, kingdom_ladies_end),
            (neg|is_between, ":lord_lady", pretenders_begin, pretenders_end),
            (store_troop_faction, ":faction", ":lord_lady"),
            (eq, ":faction", "$players_kingdom"),
            (call_script, "script_troop_set_title_according_to_faction", ":lord_lady", ":faction"),
          (try_end),
          (try_for_range, ":lord_lady", companions_begin, companions_end),
            (store_troop_faction, ":faction", ":lord_lady"),
            (eq, ":faction", "$players_kingdom"),
            (troop_slot_eq, ":lord_lady", slot_troop_occupation, slto_kingdom_hero),
            (call_script, "script_troop_set_title_according_to_faction", ":lord_lady", ":faction"),
          (try_end),
          (presentation_set_duration, 0),
        (try_end),
        ]),
      ])
