# ======================================================================
# SHARED DEPENDENCY
# Entity: party_remove_all_companions (script)
# Called by menus in 2 domains: battle, siege
# ======================================================================

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

party_remove_all_companions_scripts = [
#NPC companion changes end
# INPUT:
# param1: Party-id from which  companions will be removed.
# "$g_move_heroes" : controls if heroes will also be removed.
("party_remove_all_companions",
    [
      (store_script_param_1, ":party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_companion_stacks",":party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_companion_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party",":stack_no"),

        (party_stack_get_size, ":stack_size", ":party", ":stack_no"),

        (try_begin),
		##diplomacy start+
		  #To avoid problems with temporarily-rejoined promoted companions and ladies
		  #suddenly forgetting that they're lords, check this.
			#If the troop is a companion or a kingdom lady...
			(this_or_next|is_between, ":stack_troop", companions_begin, companions_end),
				(is_between, ":stack_troop", kingdom_ladies_begin, kingdom_ladies_end),
			#...but has since become a lord
			(this_or_next|troop_slot_eq, ":stack_troop", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
			(this_or_next|troop_slot_eq, ":stack_troop", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
				(troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
			#...and the troop would be removed
			(this_or_next|eq, "$g_move_heroes", 1),
				(eq, ":party", "p_main_party"),
			#Then set up the troop as if it was a lord that was just defeated but escaped
			(troop_set_slot, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
			(troop_set_slot, ":stack_troop", slot_troop_leaded_party, -1),
			(troop_set_slot, ":stack_troop", slot_troop_prisoner_of_party, -1),
			(troop_set_slot, ":stack_troop", slot_troop_cur_center, -1),
			(party_remove_members, ":party", ":stack_troop", ":stack_size"),
		#Fall through to standard behavior:
		(else_try),
	    ##diplomacy end+
          (troop_is_hero, ":stack_troop"),
          (neg|is_between, ":stack_troop", pretenders_begin, pretenders_end),
          #SB : insert fix for wife as companion, do not let her get imprisoned because dialogues aren't fun to debug
          (neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":stack_troop"),
          (neq, ":stack_troop", "trp_player"),
          (eq, "$g_prison_heroes", 1),
          (eq, ":party", "p_main_party"),
          (store_random_in_range, ":succeed_escaping", 0, 2),
          (neq, ":succeed_escaping", 0), #50% chance companion stays with us.
          (troop_set_health, ":stack_troop", 100), #heal before leaving
          (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
          (assign, ":minimum_distance", 99999),
          (assign, ":prison_center", -1),
          (try_for_range, ":center", walled_centers_begin, walled_centers_end),
            (store_faction_of_party, ":center_faction", ":center"),
            (eq, ":center_faction", ":enemy_faction"),
            (store_distance_to_party_from_party, ":dist", ":center", "p_main_party"),
            (lt, ":dist", ":minimum_distance"),
            (assign, ":minimum_distance", ":dist"),
            (assign, ":prison_center", ":center"),
          (try_end),
          (assign, reg1, ":prison_center"),
          #(display_message, "@{!}DEBUG : prison center is {reg1}"),
          (try_begin),
            (ge, ":prison_center", 0),
            (store_random_in_range, ":succeed_escaping", 0, 4),
            (neq, ":succeed_escaping", 0), #25% chance companion escapes to a tavern.
            (party_add_prisoners, ":prison_center", ":stack_troop", ":stack_size"),
            (troop_set_slot, ":stack_troop", slot_troop_prisoner_of_party, ":prison_center"),
            (troop_set_slot, ":stack_troop", slot_troop_playerparty_history, pp_history_scattered),
            (troop_set_slot, ":stack_troop", slot_troop_turned_down_twice, 0),
            (troop_set_slot, ":stack_troop", slot_troop_occupation, 0),
            (party_remove_members, ":party", ":stack_troop", ":stack_size"),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (str_store_party_name, s1, ":prison_center"),
              (display_message, "str_your_hero_prisoned_at_s1"),
            (try_end),
          (else_try),
            #bandits or deserters won and captured companion. So place it randomly in a town's tavern.
            (assign, ":end_condition", 1000),
            (try_for_range, ":unused", 0, ":end_condition"),
              (store_random_in_range, ":town_no", towns_begin, towns_end),
			  ##diplomacy start+
			  #OLD (NATIVE) VERSION:
			  #(neg|troop_slot_eq, ":stack_troop", slot_troop_home, ":town_no"),
              #(neg|troop_slot_eq, ":stack_troop", slot_troop_first_encountered, ":town_no"),
			  #
			  #NEW (DIPLOMACY+) VERSION:
			  #If the player owns the town, the companion is no longer in "never return" mode.
			  (party_get_slot, ":town_lord", ":town_no", slot_town_lord),
			  (this_or_next|eq, ":town_lord", "trp_player"),
			  (this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
				(neg|troop_slot_eq, ":stack_troop", slot_troop_home, ":town_no"),
              (this_or_next|eq, ":town_lord", "trp_player"),
			  (this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
			     (neg|troop_slot_eq, ":stack_troop", slot_troop_first_encountered, ":town_no"),
			  ##diplomacy end+
              (assign, ":end_condition", -1),
            (try_end),
            (troop_set_slot, ":stack_troop", slot_troop_cur_center, ":town_no"),
            (troop_set_slot, ":stack_troop", slot_troop_playerparty_history, pp_history_scattered),
            (troop_set_slot, ":stack_troop", slot_troop_turned_down_twice, 0),
            (troop_set_slot, ":stack_troop", slot_troop_occupation, 0),
            (party_remove_members, ":party", ":stack_troop", ":stack_size"),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, 4, ":stack_troop"),
              (str_store_party_name, 5, ":town_no"),
              (display_message, "@{!}{s4} is sent to {s5} after defeat"),
            (try_end),
          (try_end),
        (else_try),
          (this_or_next|neg|troop_is_hero, ":stack_troop"),
          (eq, "$g_move_heroes", 1),
          (party_remove_members, ":party", ":stack_troop", ":stack_size"),
        (try_end),
      (try_end),
  ])
]
