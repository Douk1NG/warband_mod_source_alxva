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

game_get_troop_note_scripts = [
#script_game_get_troop_note
# This script is called from the game engine when the notes of a troop is needed.
# INPUT: arg1 = troop_no, arg2 = note_index
# OUTPUT: s0 = note
("game_get_troop_note",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":note_index"),
      (set_trigger_result, 0),

      (str_store_troop_name, s54, ":troop_no"),
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (this_or_next|eq, "$player_has_homage", 1),
        (eq, "$players_kingdom", "fac_player_supporters_faction"),
        (assign, ":troop_faction", "$players_kingdom"),
      (else_try),
        (store_troop_faction, ":troop_faction", ":troop_no"),
      (try_end),
      (str_clear, s49),

	  #Family notes
      (try_begin),
	    ##diplomacy start+ add support for displaying relations with kings and claimants
		#(this_or_next|is_between, ":troop_no", lords_begin, kingdom_ladies_end),
        #(eq, ":troop_no", "trp_player"),
        #(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),

		(this_or_next|eq, ":troop_no", "trp_player"),
		(this_or_next|is_between, ":troop_no", lords_begin, kingdom_ladies_end),#includes pretenders
			(is_between, ":troop_no", kings_begin, kings_end),

		##The following would only show relations for kings and claimants if they are married.
        #(this_or_next|troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
		#	(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
		#(this_or_next|troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
		#	(neg|is_between, ":troop_no", kings_begin, kings_end),

		##diplomacy end+
        (assign, ":num_relations", 0),

        (try_begin),
          (call_script, "script_troop_get_family_relation_to_troop", "trp_player", ":troop_no"),
          (gt, reg0, 0),
          (val_add, ":num_relations", 1),
        (try_end),
		##diplomacy start+
        #(try_for_range, ":aristocrat", lords_begin, kingdom_ladies_end),
		#Display relations with kings and claimants
		(try_for_range, ":aristocrat", heroes_begin, heroes_end),
		  (this_or_next|is_between, ":aristocrat", lords_begin, kingdom_ladies_end),#includes pretenders
			  (is_between, ":aristocrat", kings_begin, kings_end),
		##diplomacy end+
          (call_script, "script_troop_get_family_relation_to_troop", ":aristocrat", ":troop_no"),
          (gt, reg0, 0),
          (val_add, ":num_relations", 1),
        (try_end),
        (try_begin),
          (gt, ":num_relations", 0),
          (try_begin),
            (eq, ":troop_no", "trp_player"),
            (str_store_string, s49, "str__family_"),
          (else_try),
            (troop_get_slot, reg1, ":troop_no", slot_troop_age),
            (str_store_string, s49, "str__age_reg1_family_"),
          (try_end),
          (try_begin),
            (call_script, "script_troop_get_family_relation_to_troop", "trp_player", ":troop_no"),
            (gt, reg0, 0),
            (str_store_troop_name_link, s12, "trp_player"),
            (val_sub, ":num_relations", 1),
            (try_begin),
              (eq, ":num_relations", 0),
              (str_store_string, s49, "str_s49_s12_s11_end"),
            (else_try),
              (str_store_string, s49, "str_s49_s12_s11"),
            (try_end),
          (try_end),
		  ##diplomacy start+
          #(try_for_range, ":aristocrat", lords_begin, kingdom_ladies_end),
		  #Display relations with kings and claimants
		  (try_for_range, ":aristocrat", heroes_begin, heroes_end),
		    (this_or_next|is_between, ":aristocrat", lords_begin, kingdom_ladies_end),#includes pretenders
			   (is_between, ":aristocrat", kings_begin, kings_end),
		  ##diplomacy end+
            (call_script, "script_troop_get_family_relation_to_troop", ":aristocrat", ":troop_no"),
            (gt, reg0, 0),
            (try_begin),
              (neg|is_between, ":aristocrat", kingdom_ladies_begin, kingdom_ladies_end),
              (eq, "$cheat_mode", 1),
              (str_store_troop_name_link, s12, ":aristocrat"),
              (call_script, "script_troop_get_relation_with_troop", ":aristocrat", ":troop_no"),
              (str_store_string, s49, "str_s49_s12_s11_rel_reg0"),
            (else_try),
              (str_store_troop_name_link, s12, ":aristocrat"),
              (val_sub, ":num_relations", 1),
              (try_begin),
                (eq, ":num_relations", 0),
                (str_store_string, s49, "str_s49_s12_s11_end"),
              (else_try),
                (str_store_string, s49, "str_s49_s12_s11"),
              (try_end),
            (try_end),
          (try_end),
        (try_end),
      (try_end),

      (try_begin),
        (neq, ":troop_no", "trp_player"),
        (neg|is_between, ":troop_faction", kingdoms_begin, kingdoms_end),
        (neg|is_between, ":troop_no", companions_begin, companions_end),
        (neg|is_between, ":troop_no", pretenders_begin, pretenders_end),

        (try_begin),
          (eq, ":note_index", 0),
          (str_store_string, s0, "str_s54_has_left_the_realm"),
          ##diplomacy start+
          #Check for "deceased" instead
          (try_begin),
             (troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
             (str_store_string, s0, "str_s54_is_deceased"),
          (try_end),
          ##diplomacy end+
          (set_trigger_result, 1),
        (else_try),
          (str_clear, s0),
          (this_or_next|eq, ":note_index", 1),
          (eq, ":note_index", 2),
          (set_trigger_result, 1),
        (try_end),

      (else_try),
        (is_between, ":troop_no", companions_begin, companions_end),
        (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (eq, ":note_index", 0),
        (set_trigger_result, 1),
        (str_clear, s0),
        (assign, ":companion", ":troop_no"),
        (str_store_troop_name, s4, ":companion"),
        (try_begin),
			# (troop_get_slot, ":days_left", ":companion", slot_troop_days_on_mission),

			(this_or_next|main_party_has_troop, ":companion"),
			(this_or_next|troop_slot_ge, ":companion", slot_troop_current_mission, 1),
				(eq, "$g_player_minister", ":companion"),
            #SB : replace the call
            (call_script, "script_companion_get_mission_string", ":companion"),

			# (try_begin),
				# (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_kingsupport),
				# (str_store_string, s8, "str_gathering_support"),
				# (try_begin),
					# (eq, ":days_left", 1),
					# (str_store_string, s5, "str_expected_back_imminently"),
				# (else_try),
					# (assign, reg3, ":days_left"),
					# (str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				# (try_end),
			# (else_try),
				# (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_gather_intel),
				# (troop_get_slot, ":town_with_contacts", ":companion", slot_troop_town_with_contacts),
				# (str_store_party_name, s11, ":town_with_contacts"),

				# (str_store_string, s8, "str_gathering_intelligence"),
				# (try_begin),
					# (eq, ":days_left", 1),
					# (str_store_string, s5, "str_expected_back_imminently"),
				# (else_try),
					# (assign, reg3, ":days_left"),
					# (str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				# (try_end),
			# (else_try),

				# (troop_slot_ge, ":companion", slot_troop_current_mission, npc_mission_peace_request),
				# (neg|troop_slot_ge, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible), #SB : replace hard constant 8

				# (troop_get_slot, ":faction", ":companion", slot_troop_mission_object),
				# (str_store_faction_name, s9, ":faction"),
				# (str_store_string, s8, "str_diplomatic_embassy_to_s9"),
				# (try_begin),
					# (eq, ":days_left", 1),
					# (str_store_string, s5, "str_expected_back_imminently"),
				# (else_try),
					# (assign, reg3, ":days_left"),
					# (str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				# (try_end),
			# (else_try),
				# (eq, ":companion", "$g_player_minister"),
				# (str_store_string, s8, "str_serving_as_minister"),
				# (str_store_party_name, s9, "$g_player_court"),
				# (is_between, "$g_player_court", centers_begin, centers_end),
				# (str_store_string, s5, "str_in_your_court_at_s9"),
			# (else_try),
				# (eq, ":companion", "$g_player_minister"),
				# (str_store_string, s8, "str_serving_as_minister"),
				# (str_store_string, s5, "str_awaiting_the_capture_of_a_fortress_which_can_serve_as_your_court"),
			# (else_try),
				# (main_party_has_troop, ":companion"),
				# (str_store_string, s8, "str_under_arms"),
				# (str_store_string, s5, "str_in_your_party"),
			# (try_end),

			# (str_store_string, s0, "str_s4_s8_s5"),
		##diplomacy start+
		#Check for explicit "exiled" and "dead" settings
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
			(str_store_string, s0, "str_s54_is_deceased"),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
			(str_store_string, s0, "str_s54_has_left_the_realm"),
		##diplomacy end+
		(else_try),
			(str_store_string, s0, "str_whereabouts_unknown"),
		(try_end),


      (else_try),
        (is_between, ":troop_no", pretenders_begin, pretenders_end),
        (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (neq, ":troop_no", "$supported_pretender"),


        (troop_get_slot, ":orig_faction", ":troop_no", slot_troop_original_faction),
        (try_begin),
          (faction_slot_eq, ":orig_faction", slot_faction_state, sfs_active),
          (faction_slot_eq, ":orig_faction", slot_faction_has_rebellion_chance, 1),
          (try_begin),
            (eq, ":note_index", 0),
            (str_store_faction_name_link, s56, ":orig_faction"),
            ##diplomacy start+ xxx Removed third argument (was it doing anything?)
            #(str_store_string, s0, "@{s54} is a claimant to the throne of {s56}.", 0),
            (str_store_string, s0, "@{s54} is a claimant to the throne of {s56}."),
            ##diplomacy end+
            (set_trigger_result, 1),
          (try_end),
        (else_try),
          (try_begin),
            (str_clear, s0),
            (this_or_next|eq, ":note_index", 0),
            (this_or_next|eq, ":note_index", 1),
            (eq, ":note_index", 2),
            (set_trigger_result, 1),
          (try_end),
        (try_end),

      (else_try),
        (try_begin),
          (eq, ":note_index", 0),
          (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
          (str_store_troop_name_link, s55, ":faction_leader"),
          (str_store_faction_name_link, s56, ":troop_faction"),
          (assign, ":troop_is_player_faction", 0),
          (assign, ":troop_is_faction_leader", 0),
          (try_begin),
            (eq, ":troop_faction", "fac_player_faction"),
            (assign, ":troop_is_player_faction", 1),
          (else_try),
            (eq, ":faction_leader", ":troop_no"),
            (assign, ":troop_is_faction_leader", 1),
          (try_end),
          #SB: add marshal check
          (try_begin),
            (faction_slot_eq, ":troop_faction", slot_faction_marshall, ":troop_no"),
            (assign, ":troop_is_marshal", 1),
          (else_try),
            (assign, ":troop_is_marshal", 0),
          (try_end),
          (assign, ":num_centers", 0),
          (str_store_string, s58, "@nowhere"),
          (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
            (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
            (try_begin),
              (eq, ":num_centers", 0),
              (str_store_party_name_link, s58, ":cur_center"),
            (else_try),
              (eq, ":num_centers", 1),
              (str_store_party_name_link, s57, ":cur_center"),
              (str_store_string, s58, "@{s57} and {s58}"),
            (else_try),
              (str_store_party_name_link, s57, ":cur_center"),
              (str_store_string, s58, "@{!}{s57}, {s58}"),
            (try_end),
            (val_add, ":num_centers", 1),
          (try_end),
          ##diplomacy start+ use script for gender
          #(troop_get_type, reg3, ":troop_no"),
          (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 3),
          #(assign, reg3, reg0),
          ##diplomacy end+


          (str_clear, s59),
          (try_begin),
            (call_script, "script_troop_get_player_relation", ":troop_no"),
            (assign, ":relation", reg0),
            (store_add, ":normalized_relation", ":relation", 100),
            (val_add, ":normalized_relation", 5),
            (store_div, ":str_offset", ":normalized_relation", 10),
            (val_clamp, ":str_offset", 0, 20),
            (store_add, ":str_id", "str_relation_mnus_100_ns",  ":str_offset"),
            (neq, ":str_id", "str_relation_plus_0_ns"),
            (str_store_string, s60, "@{reg3?She:He}"),
            (str_store_string, s59, ":str_id"),
            (str_store_string, s59, "@{!}^{s59}"),
          (try_end),
          #lord recruitment changes begin
          #This sends a bunch of political information to s47.

          #refresh registers
          (assign, reg9, ":num_centers"),
          ##diplomacy start+ use script for gender
          #(troop_get_type, reg3, ":troop_no"),
          (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 3),
          ##diplomacy end+

          #SB : rearrange registers a bit
          (assign, reg4, ":troop_is_faction_leader"),
          (assign, reg5, ":troop_is_marshal"),
          (assign, reg6, ":troop_is_player_faction"),

          #SB : TODO, add rounding based on personal relation/time last met?
          (troop_get_slot, reg15, ":troop_no", slot_troop_renown),
          (troop_get_slot, reg16, ":troop_no", slot_troop_controversy),
          #SB : actually use this wealth in string
          (troop_get_slot, reg17, ":troop_no", slot_troop_wealth), #DEBUGS
          (str_store_string, s61, "@unknown"),
          (try_begin),
            (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
            (this_or_next|neq, "$cheat_mode", 0),
            (troop_slot_eq, ":troop_no", slot_troop_met, 1),
            (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
            (store_add, ":rep_string", ":reputation", "str_personality_archetypes"),
            (str_store_string, s61, ":rep_string"),
          (try_end),
          ##diplomacy start+ xxx remove third argument (was it doing anything?)
          #(str_store_string, s0, "str_lord_info_string", 0),
          (str_store_string, s0, "str_lord_info_string"),
          ##diplomacy end+
          #lord recruitment changes end
          (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
          (set_trigger_result, 1),
        (try_end),
      (try_end),
     ])
]
