# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

game_get_troop_wage_scripts = [
#script_start_wedding_cutscene
# This script is called from the game engine for calculating troop wages.
# Input:
# param1: troop_id, param2: party-id
# Output: reg0: weekly wage
("game_get_troop_wage",
    [
      (store_script_param_1, ":troop_id"),
      (call_script, "script_initialize_exchange_screen_extensions", ":troop_id"), 
	  (troop_set_slot, "trp_temp_array_d", slot_last_requested_troop, ":troop_id"),

      (assign,":wage", 0),
      (try_begin),
        (this_or_next|eq, ":troop_id", "trp_player"),
        (eq, ":troop_id", "trp_kidnapped_girl"),
      (else_try),
        (is_between, ":troop_id", pretenders_begin, pretenders_end),
      ##diplomacy start+
      (else_try),
      #Temporarily joined lords and ladies don't require wages.
        (is_between, ":troop_id", heroes_begin, heroes_end),
        (this_or_next|troop_slot_eq, ":troop_id", slot_troop_playerparty_history,dplmc_pp_history_lord_rejoined),
        (this_or_next|troop_slot_eq, ":troop_id", slot_troop_occupation, slto_kingdom_hero),
           (troop_slot_eq, ":troop_id",slot_troop_occupation, slto_kingdom_lady),
      ##diplomacy end+
      (else_try),
        (store_character_level, ":troop_level", ":troop_id"),
        (assign, ":wage", ":troop_level"),
        (val_add, ":wage", 3),
        (val_mul, ":wage", ":wage"),
        (val_div, ":wage", 25),
      (try_end),

      (try_begin), #mounted troops cost 65% more than the normal cost
        (neg|is_between, ":troop_id", companions_begin, companions_end),
        (troop_is_mounted, ":troop_id"),
        (val_mul, ":wage", 5),
        (val_div, ":wage", 3),
      (try_end),

      (try_begin), #mercenaries cost %50 more than the normal cost
        (is_between, ":troop_id", mercenary_troops_begin, mercenary_troops_end),
        (val_mul, ":wage", 3),
        (val_div, ":wage", 2),
      (try_end),

      (try_begin),
        (is_between, ":troop_id", companions_begin, companions_end),
        (val_mul, ":wage", 2),
      (try_end),

      (store_skill_level, ":leadership_level", "skl_leadership", "trp_player"),
      (store_mul, ":leadership_bonus", 5, ":leadership_level"),
      (store_sub, ":leadership_factor", 100, ":leadership_bonus"),
      (val_mul, ":wage", ":leadership_factor"),  #wage = wage * (100 - 5*leadership)/100
	  (val_div, ":wage", 100),

      (try_begin),
        (neq, ":troop_id", "trp_player"),
        (neq, ":troop_id", "trp_kidnapped_girl"),
        (neg|is_between, ":troop_id", pretenders_begin, pretenders_end),
          ##diplomacy start+ For temporarily rejoined lords, and temporarily joined ladies
        (neg|troop_slot_eq, ":troop_id", slot_troop_playerparty_history,dplmc_pp_history_lord_rejoined),
        (neg|troop_slot_eq, ":troop_id", slot_troop_occupation, slto_kingdom_hero),
        (neg|is_between, ":troop_id", kingdom_ladies_begin, kingdom_ladies_end),
          ##diplomacy end+
        (val_max, ":wage", 1),
      (try_end),

      (assign, reg0, ":wage"),
      (set_trigger_result, reg0),
  ])
]
