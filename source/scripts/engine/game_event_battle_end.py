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

game_event_battle_end_scripts = [
# script_game_event_party_encounter:
# This script is called whenever the game ends the battle between two parties on the map.
# INPUT:
# param1: Defender Party
# param2: Attacker Party
("game_event_battle_end",
    [
##       (store_script_param_1, ":root_defender_party"),
##       (store_script_param_2, ":root_attacker_party"),

      #Fixing deleted heroes
      ##diplomacy start+ kingdom ladies may also potentially lead parties
      (try_for_range, ":cur_troop", heroes_begin, heroes_end),#<- changed active_npcs to heroes
      #diplomacy end+
		(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
        (is_between, ":cur_troop", companions_begin, companions_end),
        (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
        (troop_get_slot, ":cur_prisoner_of_party", ":cur_troop", slot_troop_prisoner_of_party),
        (try_begin),
          (ge, ":cur_party", 0),
          (assign, ":continue", 0),
          (try_begin),
            (neg|party_is_active, ":cur_party"),
            (assign, ":continue", 1),
          (else_try),
            (party_count_companions_of_type, ":amount", ":cur_party", ":cur_troop"),
            (le, ":amount", 0),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_troop_name, s1, ":cur_troop"),
            (display_message, "@{!}DEBUG: {s1} no longer leads a party."),
          (try_end),

          (troop_set_slot, ":cur_troop", slot_troop_leaded_party, -1),
          #(str_store_troop_name, s5, ":cur_troop"),
          #(display_message, "@{!}DEBUG : {s5}'s troop_leaded_party set to -1"),
        (try_end),
        (try_begin),
          (ge, ":cur_prisoner_of_party", 0),
          (assign, ":continue", 0),
          (try_begin),
            (neg|party_is_active, ":cur_prisoner_of_party"),
            (assign, ":continue", 1),
          (else_try),
            (party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party", ":cur_troop"),
            (le, ":amount", 0),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_troop_name, s1, ":cur_troop"),
            (display_message, "@{!}DEBUG: {s1} is no longer a prisoner."),
          (try_end),
          (call_script, "script_remove_troop_from_prison", ":cur_troop"),
          #searching player
          (try_begin),
            (party_count_prisoners_of_type, ":amount", "p_main_party", ":cur_troop"),
            (gt, ":amount", 0),
            (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, "p_main_party"),
            (troop_set_slot, ":cur_troop", slot_troop_courtesan, -1),
            (assign, ":continue", 0),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, s1, ":cur_troop"),
              (display_message, "@{!}DEBUG: {s1} is now a prisoner of player."),
            (try_end),
          (try_end),
          (eq, ":continue", 1),
		  ##diplomacy start+
		  #Add increased information for affiliates.
		  (call_script, "script_dplmc_store_troop_is_eligible_for_affiliate_messages", ":cur_troop"),
		  (assign, ":is_affiliated", reg0),
		  ##diplomacy end+
          #searching kingdom heroes
	  ##diplomacy start+ support for promoted kingdom ladies
          (try_for_range, ":cur_troop_2", heroes_begin, heroes_end),#<-- changed active_npcs to heroes
          ##diplomacy end+
			(this_or_next|troop_slot_eq, ":cur_troop_2", slot_troop_occupation, slto_kingdom_hero),
            (is_between, ":cur_troop_2", companions_begin, companions_end),
			(eq, ":continue", 1),
            (troop_get_slot, ":cur_prisoner_of_party_2", ":cur_troop_2", slot_troop_leaded_party),
            (party_is_active, ":cur_prisoner_of_party_2"),
            (party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party_2", ":cur_troop"),
            (gt, ":amount", 0),
            (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, ":cur_prisoner_of_party_2"),
            (assign, ":continue", 0),
            (try_begin),
			##diplomacy start+ Show for affiliates
			  (ge, ":is_affiliated", 1),
			  (str_store_troop_name, s1, ":cur_troop"),
			  (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
			  (display_message, "@{s1} is now a prisoner of {s2}."),
			(else_try),
			##diplomacy end+
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, s1, ":cur_troop"),
              (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
              (display_message, "@{!}DEBUG: {s1} is now a prisoner of {s2}."),
            (try_end),
          (try_end),
          #searching walled centers
          (try_for_range, ":cur_prisoner_of_party_2", walled_centers_begin, walled_centers_end),
            (eq, ":continue", 1),
            (party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party_2", ":cur_troop"),
            (gt, ":amount", 0),
            (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, ":cur_prisoner_of_party_2"),
            (assign, ":continue", 0),
            (try_begin),
			##diplomacy start+ Show for affiliates
			  (ge, ":is_affiliated", 1),
			  (str_store_troop_name, s1, ":cur_troop"),
			  (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
			  (display_message, "@{s1} is now a prisoner of {s2}."),
			(else_try),
			##diplomacy end+
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, s1, ":cur_troop"),
              (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
              (display_message, "@{!}DEBUG: {s1} is now a prisoner of {s2}."),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
  ])
]
