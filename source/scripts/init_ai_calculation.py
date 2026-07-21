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

init_ai_calculation_scripts = [
# script_check_and_finish_active_army_quests_for_faction
# Input: none
# Output: none
("init_ai_calculation",
    [
      ##diplomacy start+
	  #(assign, ":real_party_strength"),
	  ##If terrain advantage is enabled, use it to calculate troop strengths.
      (try_begin),
         (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),

		 #First update all lords
		 (try_for_range, ":cur_troop", heroes_begin, heroes_end),
            (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
            (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
			(gt, ":cur_party", 0),
            (party_is_active, ":cur_party"),

		    (party_get_current_terrain, ":terrain_code", ":cur_party"),

			(party_get_attached_to, ":attachment", ":cur_party"),
			(try_begin),
				(ge, ":attachment", 0),
				(is_between, ":attachment", centers_begin, centers_end),
				(assign, ":terrain_code", dplmc_terrain_code_siege),#siege constant defined in header_terrain_types.py
			(try_end),

            (call_script, "script_dplmc_party_calculate_strength_in_terrain", ":cur_party", ":terrain_code", 0, 1), #will update slot_party_cached_strength
         (try_end),

		 #Then update player
		 (party_get_current_terrain, ":terrain_code", "p_main_party"),

		 (party_get_attached_to, ":attachment", "p_main_party"),
			(try_begin),
				(ge, ":attachment", 0),
				(is_between, ":attachment", centers_begin, centers_end),
				(assign, ":terrain_code", dplmc_terrain_code_siege),#siege constant defined in header_terrain_types.py
			(try_end),

		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_main_party", ":terrain_code", 0, 1), #will update slot_party_cached_strength

         (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
		    #Update with walled center alterations
            (call_script, "script_dplmc_party_calculate_strength_in_terrain", ":cur_center", -2, 0, 1),
         (try_end),
      (else_try),
	   #The old behavior, unchanged:
         (try_for_range, ":cur_troop", heroes_begin, heroes_end),
            (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
            (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
            (party_is_active, ":cur_party"),
            (call_script, "script_party_calculate_strength", ":cur_party", 0), #will update slot_party_cached_strength
         (try_end),
         (call_script, "script_party_calculate_strength", "p_main_party", 0), #will update slot_party_cached_strength
         (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
            (call_script, "script_party_calculate_strength", ":cur_center", 0), #will update slot_party_cached_strength
         (try_end),
      (try_end),
      ##diplomacy end+

      (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
        (call_script, "script_party_calculate_and_set_nearby_friend_enemy_follower_strengths", ":cur_center"),
      (try_end),

      (try_for_range, ":cur_troop", heroes_begin, heroes_end),
        (troop_get_slot, ":cur_troop_party", ":cur_troop", slot_troop_leaded_party),
        (gt, ":cur_troop_party", 0),
        (party_is_active, ":cur_troop_party"),
        (call_script, "script_party_calculate_and_set_nearby_friend_enemy_follower_strengths", ":cur_troop_party"),
      (try_end),
      (call_script, "script_party_calculate_and_set_nearby_friend_enemy_follower_strengths", "p_main_party"),
      ])
]
