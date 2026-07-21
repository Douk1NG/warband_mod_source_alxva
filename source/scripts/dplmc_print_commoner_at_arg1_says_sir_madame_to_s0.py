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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_print_commoner_at_arg1_says_sir_madame_to_s0_scripts = [
#"script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0"
#
#In a number of circumstances a commoner, who might or might not be a subject of
#the player, will refer to him as "sir" or "madame."  This script determines whether
#a different title would be warranted.
#
#input: party_no (usually a village or town)
#output: reg0 gets a number corresponding to the title used
("dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", [
		(store_script_param_1, ":party_no"),

		(assign, ":title_level", 1),
		(str_store_string, s0, "str_dplmc_sirmadam"),
		(store_faction_of_party, ":party_faction"),

		(try_begin),
			(eq, "$sneaked_into_town", disguise_none),#disable extra honors when the player is not recognized
			(ge, ":party_no", 0),

			#This is used in various conditions below, so I am calling it once
			#for simplicity.
			(assign, ":save_g_talk_troop", "$g_talk_troop"),
			(assign, ":save_g_encountered_party", "$g_encountered_party"),
            (try_begin),
              (neq, ":party_no", "$g_encountered_party"),
              (assign, "$g_encountered_party", -1),
              (assign, "$g_talk_troop", -1),
            (try_end),
			(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
			(assign, ":title_level", reg0),
			(assign, "$g_encountered_party", ":save_g_encountered_party"),
			(assign, "$g_talk_troop", ":save_g_talk_troop"),

			(try_begin),
				#The player is a full member of the faction: use full honors
				(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":party_faction"),
				(ge, reg0, DPLMC_FACTION_STANDING_DEPENDENT),
				#(nothing more needs to be done)
			(else_try),
				#the faction has recognized him formally: use full honors
				(this_or_next|eq, ":party_no", "p_main_party"),
				(this_or_next|eq, ":party_faction", "fac_player_supporters_faction"),
				   (faction_slot_ge, ":party_faction", slot_faction_recognized_player, 1),
				#(nothing more needs to be done)
			(else_try),
				#The player is the lord of the town: keep result from script_dplmc_print_subordinate_says_sir_madame_to_s0
				(is_between, ":party_no", centers_begin, centers_end),
				(party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
				#(nothing more needs to be done)
			(else_try),
				#Subjects of neutral kingdoms will use titles up to "my lord".
				(store_relation, ":relation", "fac_player_supporters_faction", ":party_faction"),
				(ge, ":relation", 0),
				(try_begin),
					(ge, ":title_level", 3),
					(assign, ":title_level", 2),
					(str_store_string, s0, "str_dplmc_my_lordlady"),
				(try_end),
			(else_try),
				#Subjects of kingdoms at war (that do not recognize the player) and all cases not
				#yet mentioned will reduce the "level" of the title awarded to the player by 1, to
				#a minimum of 1.
				(try_begin),
					(ge, ":title_level", 3),
					(assign, ":title_level", 2),
					(str_store_string, s0, "str_dplmc_my_lordlady"),
				(else_try),
					(eq, ":title_level", 2),
					(assign, ":title_level", 1),
				   (str_store_string, s0, "str_dplmc_sirmadam"),
				(try_end),
			(try_end),
		(try_end),

		##Special cases
		(try_begin),
			(neq, ":party_no", "$g_encountered_party"),
		(else_try),
			(eq, "$sneaked_into_town", disguise_none),
			(ge, ":title_level", 1),
			(is_between, "$g_talk_troop", companions_begin, companions_end),
			(neg|troop_slot_eq, "$g_talk_troop", slot_troop_met, 0),
			(this_or_next|neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_inactive),
				(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, 0),
			(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
			(troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
			(ge, ":honorific", "str_npc1_honorific"),
			(str_store_string, s0, ":honorific"),
		(else_try),
			(eq, ":title_level", 1),
			(is_between, "$g_talk_troop", heroes_begin, heroes_end),
			(assign, ":title_level", "str_dplmc_sirmadame"),
		(try_end),

		(assign, reg0, ":title_level"),

		##Switch to cultural equivalents
      #(try_begin),
		#   (eq, ":party_no", "$g_encountered_party"),
		#   (is_between, "$g_talk_troop", heroes_begin, heroes_end),
	   #   (troop_get_slot, ":culture_faction", "$g_talk_troop", slot_troop_original_faction),
		#   (is_between, ":culture_faction", npc_kingdoms_begin, npc_kingdoms_end),
		#(else_try),
		#   (eq, ":party_no", "$g_encountered_party"),
		#   (ge, "$g_talk_troop", soldiers_begin),
		#   (store_faction_of_troop, ":culture_faction", "$g_talk_troop"),
		#	(is_between, ":culture_faction", npc_kingdoms_begin, npc_kingdoms_end),
		#(else_try),
      #   (is_between, ":party_no", centers_begin, centers_end),
      #   (party_get_slot, ":culture_faction", ":party_no", slot_center_original_faction),
  		#	(is_between, ":culture_faction", npc_kingdoms_begin, npc_kingdoms_end),
		#(else_try),
		#   (assign, ":culture_faction", ":party_faction"),
		#(try_end),
		#(try_begin),
		#   (is_between, "$g_talk_troop", companions_begin, companions_end),#do not switch
		#(else_try),
		#  (eq, ":title_level", 1),
		#	(eq, ":culture_faction", "fac_kingdom_6"),
		#	(str_store_string, s0, "@{!}{sahib/sahiba}"),
		#(try_end),
	])
]
