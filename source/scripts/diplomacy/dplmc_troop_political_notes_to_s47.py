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

dplmc_troop_political_notes_to_s47_scripts = [
("dplmc_troop_political_notes_to_s47",
      [
    (store_script_param, ":troop_no", 1),
    ##diplomacy start+
	(assign, ":save_reg1", reg1),#save to revert
    (assign, ":save_reg4", reg4),#save to revert

    (try_begin),
       (eq, 0, 1),#Always disable this right now
       (is_between, "$g_talk_troop", heroes_begin, heroes_end),#i.e. not your chancellor
       (assign, ":troop_speaker", "$g_talk_troop"),
	   (call_script, "script_troop_get_player_relation", ":troop_speaker"),
	   (assign, ":speaker_player_relation", reg0),
    (else_try),
       (assign, ":troop_speaker", -1),
	   (assign, ":speaker_player_relation", 100),
    (try_end),
    ##diplomacy end+

    (try_begin),
      (str_clear, s47),

      (store_faction_of_troop, ":troop_faction", ":troop_no"),

      (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),

      (str_clear, s40),
      (assign, ":logged_a_rivalry", 0),
      ##nested diplomacy start+
      (str_clear, s41),
      #lord can be married or related to player
      #(try_for_range, ":kingdom_hero", active_npcs_begin, active_npcs_end),
      (try_for_range, ":kingdom_hero", active_npcs_including_player_begin, active_npcs_end),
        #Also, don't include rivalries with retired (or dead) characters
        (neg|troop_slot_ge, ":troop_no", slot_troop_occupation, slto_retirement),
      ##nested diplomacy end+
        (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":kingdom_hero"),
        (lt, reg0, -10),

        (str_store_troop_name_link, s39, ":kingdom_hero"),
		  ##nested diplomacy start+ use second person
        (try_begin),
           (eq, ":kingdom_hero", "trp_player"),
           (str_store_string, s39, "str_you"),
        (try_end),
		  ##nested diplomacy end+
        (try_begin),
          (eq, ":logged_a_rivalry", 0),
          ##nested diplomacy start+
          (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),#use reg4 for gender-correct pronoun
          ##nested diplomacy end+
          (str_store_string, s40, "str_dplmc_s39_rival"),
          (assign, ":logged_a_rivalry", 1),
        (else_try),
          (str_store_string, s41, "str_s40"),
          (str_store_string, s40, "str_dplmc_s41_s39_rival"),
        (try_end),

      (try_end),

      (str_clear, s46),
      ##nested diplomacy start+
      #(troop_get_type, reg4, ":troop_no"),#use for gender-correct pronoun
		(call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),
      (str_store_troop_name, s46,":troop_no"),
	  (assign, ":details_available", 0),
	  (try_begin),
		#Enable details for lords you have met
		(neg|troop_slot_eq, ":troop_no", slot_troop_met, 0),
		(assign, ":details_available", 1),
          (else_try),
                #Enable details when using an "omniscient" or non-specific speaker
                (neg|is_between, ":troop_speaker", heroes_begin, heroes_end),
                (assign, ":details_available", 1),
          (else_try),
                #Enable details for NPCs that aren't standard heroes, because the following checks don't apply
                (neg|is_between, ":troop_no", heroes_begin, heroes_end),
                (assign, ":details_available", 1),
          (else_try),
                #Enable details for lords the speaker has met
                (is_between, ":troop_speaker", heroes_begin, heroes_end),
                (is_between, ":troop_no", heroes_begin, heroes_end),
                (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":troop_speaker"),
                (neq, reg0, 0),#between NPCs, relation 0 means "have not met"
                (assign, ":details_available", 1),
          (else_try),
                #Enable details for v. notable lords (based on renown)
                (troop_slot_ge, ":troop_no", slot_troop_renown, 500),
                (assign, ":details_available", 1),
          (else_try),
                #Enable details for v. notable lords (based on fiefs)
                (assign, reg0, 0),
                (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
                   (this_or_next|party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
                   (this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_no"),
                     (troop_slot_eq, ":troop_no", slot_troop_home, ":center_no"),
                   (val_add, reg0, 2),
                   (party_slot_eq, ":center_no", slot_party_type, spt_town),
                   (val_add, reg0, 2),
                (try_end),
                (ge, reg0, 4),#one town, or 2+ castles
                (assign, ":details_available", 1),
          (try_end),
      #xxx TODO: Make a full implementation of the above that takes into account the time of the last spy report.
      (try_begin),
		(eq, ":details_available", 0),
		(troop_get_slot, reg11, ":troop_no", slot_lord_reputation_type),
        (str_store_string, s46, "str_dplmc_reputation_unknown"),
	  (else_try),
	  ##nested diplomacy end+
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
        (str_store_string, s46, "str_dplmc_reputation_martial"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
        (str_store_string, s46, "str_dplmc_reputation_debauched"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
        (str_store_string, s46, "str_dplmc_reputation_pitiless"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
        (str_store_string, s46, "str_dplmc_reputation_calculating"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
        (str_store_string, s46, "str_dplmc_reputation_quarrelsome"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
        (str_store_string, s46, "str_dplmc_reputation_goodnatured"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
        (str_store_string, s46, "str_dplmc_reputation_upstanding"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_conventional),
        (str_store_string, s46, "str_dplmc_reputation_conventional"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_adventurous),
        (str_store_string, s46, "str_dplmc_reputation_adventurous"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_otherworldly),
        (str_store_string, s46, "str_dplmc_reputation_romantic"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
        (str_store_string, s46, "str_dplmc_reputation_moralist"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_ambitious),
        (str_store_string, s46, "str_dplmc_reputation_ambitious"),
      (else_try),
        (troop_get_slot, reg11, ":troop_no", slot_lord_reputation_type),
        (str_store_string, s46, "str_dplmc_reputation_unknown"),
      (try_end),

      ##diplomacy start+
      (str_clear, s39),#remove annoying bug
      (str_clear, s45),#remove annoying bug

      #Special-case spouse into showing up if it doesn't get added below
      (try_begin),
         (troop_get_slot, ":spouse", ":troop_no", slot_troop_spouse),
         (ge, ":spouse", 0),

         #Because blank memory is initially zero, enforce this
         (this_or_next|is_between, ":troop_no", heroes_begin, heroes_end),
            (neq, ":spouse", "trp_player"),
         #Initialize s45
         (str_store_troop_name, s39, ":spouse"),
         (try_begin),
           (eq, ":spouse", "trp_player"),
           (str_store_string, s39, "str_you"),##<-- dplmc+ note, this was s59 before, probably an accidental bug
         (else_try), #SB : speaker
           (eq, ":spouse", ":troop_speaker"),
           (str_store_string, s39, "str_me"),
         (try_end),
         (str_store_string, s45, "str_dplmc_s40_married_s39"),
      (try_end),
      ##diplomacy end+

      (try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
        (troop_get_slot, ":love_interest", ":troop_no", ":love_interest_slot"),
        ##nested diplomacy start+ ; some lords could romance opposite-gender lords
        #(is_between, ":love_interest", kingdom_ladies_begin, kingdom_ladies_end),
        (is_between, ":love_interest", active_npcs_begin, kingdom_ladies_end),
        #Also prevent a bug for companions / claimants who are lords
        (neq, ":love_interest", "trp_knight_1_1_wife"),#<- should not appear in the game
        #Also prevent bad messages for married/betrothed lords
        (this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, ":love_interest"),
           (troop_slot_eq, ":troop_no", slot_troop_spouse, -1),
        (this_or_next|troop_slot_eq, ":troop_no", slot_troop_betrothed, ":love_interest"),
           (troop_slot_eq, ":troop_no", slot_troop_betrothed, -1),
        ##nested diplomacy end+
        (str_store_troop_name, s39, ":love_interest"),
        ##nested diplomacy start+ Use second person properly
        (try_begin),
           (eq, ":love_interest", "trp_player"),
           (str_store_string, s39, "str_you"),
         (else_try), #SB : speaker
           (eq, ":love_interest", ":troop_speaker"),
           (str_store_string, s39, "str_me"),
        (try_end),
        ##nested diplomacy start+
        (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":love_interest"),
        ##nested diplomacy start+
        (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),#use reg4 for gender-correct pronoun
        ##nested diplomacy end+
        (str_store_string, s45, "str_dplmc_s40_love_interest_s39"),
        (try_begin),
        	(troop_slot_eq, ":troop_no", slot_troop_spouse, ":love_interest"),
        	(str_store_string, s45, "str_dplmc_s40_married_s39"),
        (else_try),
        	(troop_slot_eq, ":troop_no", slot_troop_betrothed, ":love_interest"),
        	(str_store_string, s45, "str_dplmc_s40_betrothed_s39"),
        (try_end),
      (try_end),

    (str_clear, s44),
    (try_begin),
      (neq, ":troop_no", ":faction_leader"),
      ##nested diplomacy start+
      (gt, ":details_available", 0),
	  #Ensure leader is valid
	  (assign, reg0, 0),#continue if 0
	  (try_begin),
	     (neq, ":troop_no", "trp_player"),
		 (neq, ":faction_leader", "trp_player"),
		 (this_or_next|neg|is_between, ":troop_no", heroes_begin, heroes_end),
			(neg|is_between, ":faction_leader", heroes_begin, heroes_end),
		 (assign, reg0, 1),
	  (try_end),
	  (eq, reg0, 0),

	  (try_begin),
	     (gt, ":troop_speaker", 0),
		 (call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_no", ":troop_speaker"),
		 #(val_min, reg0, 20),
		 #(neq, ":faction_leader", "trp_player"),
		 #(val_div, reg0, 2),
	  (try_end),
	  (this_or_next|lt, reg0, 1),
		(ge, ":speaker_player_relation", 1),
      ##nested diplomacy end+
      (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),

      (assign, ":relation", reg0),
	  ##diplomacy start+ Don't mention anything for kingdom ladies at the beginning; it doesn't add information.
	  (this_or_next|lt, reg0, 0),
	  (this_or_next|gt, reg0, 1),#Remember that relation 1 is neutral (it just means "met") between NPCs
	  (this_or_next|neg|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
	  (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	  (this_or_next|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
	     (troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
	  ##diplomacy end+
      (store_add, ":normalized_relation", ":relation", 100),
      (val_add, ":normalized_relation", 5),
      (store_div, ":str_offset", ":normalized_relation", 10),
      (val_clamp, ":str_offset", 0, 20),
      ##nested diplomacy start+
      #(troop_get_type, reg4, ":troop_no"),#use for gender-correct pronoun
      (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),
      #TODO: Come back and add this (take into account spying)
      #(neq, ":details_available", 0),#don't show unless more details are available
      ##nested diplomacy end+
      (store_add, ":str_id", "str_dplmc_relation_mnus_100_ns",  ":str_offset"),
      (try_begin),
        (eq, ":faction_leader", "trp_player"),
        ##nested diplomacy start+ "str_you" exists, so we might as well use it
        #(str_store_string, s59, "@you"),
        (str_store_string, s59, "str_you"),
        ##diplomacy end+
      (else_try),
        (str_store_troop_name, s59, ":faction_leader"),
      (try_end),
      (str_store_string, s59, ":str_id"),
      (str_store_string, s44, "@{!}^{s59}"),
    (try_end),

    (str_clear, s48),

    (try_begin),
      (eq, "$cheat_mode", 1),
      (store_current_hours, ":hours"),
      (gt, ":hours", 0),
      (call_script, "script_calculate_troop_political_factors_for_liege", ":troop_no", ":faction_leader"),
      (str_store_string, s48, "str_sense_of_security_military_reg1_court_position_reg3_"),
    (try_end),

    (str_store_string, s47, "str_s46s45s44s48"),

  (try_end),
     ##diplomacy start+
     (assign, reg1, ":save_reg1"),#revert register
     (assign, reg4, ":save_reg4"),#revert register to avoid clobbering
     ##diplomacy end+
    ])
]
