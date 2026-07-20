# ======================================================================
# SHARED DEPENDENCY
# Entity: change_troop_faction (script)
# Called by menus in 2 domains: kingdom_management, notifications
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

change_troop_faction_scripts = [
# script_cf_troop_get_random_enemy_troop_with_occupation
# Input: arg1 = troop_no, arg2 = faction
("change_troop_faction",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":faction_no"),
      (try_begin),
        #Reactivating inactive or defeated faction
        (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (neg|faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (faction_set_slot, ":faction_no", slot_faction_state, sfs_active),
        #(call_script, "script_store_average_center_value_per_faction"),
      (try_end),

	  #Political ramifications
	  (store_faction_of_troop, ":orig_faction", ":troop_no"),
	  ##diplomacy start+ save these for reference
	  #(faction_get_slot, ":orig_faction_leader", ":orig_faction", slot_faction_leader),
	  (faction_get_slot, ":new_faction_leader", ":faction_no", slot_faction_leader),
	  (try_begin),
		  #Avoid letting heroes get stuck as slto_inactive if petitioners switch away from the player's faction
		  (eq, ":orig_faction", "fac_player_supporters_faction"),
	     (gt, ":troop_no", 0),
	     (troop_is_hero, ":troop_no"),
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
		  (this_or_next|is_between, ":troop_no", lords_begin, lords_end),
		  (this_or_next|is_between, ":troop_no", kings_begin, kings_end),
		  (this_or_next|is_between, ":troop_no", pretenders_begin, pretenders_end),
		  (this_or_next|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
		     (troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
		  (troop_set_slot, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	  (try_end),
	  ##diplomacy end+

	  #remove if he is marshal
	  (try_begin),
		(faction_slot_eq, ":orig_faction", slot_faction_marshall, ":troop_no"),
        (call_script, "script_check_and_finish_active_army_quests_for_faction", ":orig_faction"),

		#No current issue on the agenda
		(try_begin),
			(faction_slot_eq, ":orig_faction", slot_faction_political_issue, 0),

			(faction_set_slot, ":orig_faction", slot_faction_political_issue, 1), #Appointment of marshal
			(store_current_hours, ":hours"),
			(val_max, ":hours", 0),
			(faction_set_slot, ":orig_faction", slot_faction_political_issue_time, ":hours"), #Appointment of marshal
			##diplomacy start+ Reset political stance for kingdom ladies as well
			#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),##OLD
			(try_for_range, ":active_npc", heroes_begin, heroes_end),##NEW
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":orig_faction"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			(try_begin),
				(eq, "$players_kingdom", ":orig_faction"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),
		(try_end),

        (try_begin),
		  (troop_get_slot, ":old_marshall_party", ":troop_no", slot_troop_leaded_party),
          (party_is_active, ":old_marshall_party"),
          (party_set_marshal, ":old_marshall_party", 0),
        (try_end),

		(faction_set_slot, ":orig_faction", slot_faction_marshall, -1),
	  (try_end),
	  #Removal as marshal ends

	  #Other political ramifications
	  (troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
	  ##diplomacy start+ Support promoted kingdom ladies
	  #(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
	  (try_for_range, ":active_npc", heroes_begin, heroes_end),
	  ##diplomacy end+
		(troop_slot_eq, ":active_npc", slot_troop_stance_on_faction_issue, ":troop_no"),
		(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
	  (try_end),
	  #Political ramifications end


		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":troop_no"),
			(display_message, "@{!}DEBUG - {s4} faction changed in normal faction change"),
		(try_end),

      (troop_set_faction, ":troop_no", ":faction_no"),
	  ##diplomacy start+
	  ##Don't give lords amnesia about what the player said to recruit them.
	  ##OLD:
      #(troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
      #(troop_set_slot, ":troop_no", slot_lord_recruitment_argument, 0),
      #(troop_set_slot, ":troop_no", slot_lord_recruitment_candidate, 0),
      #(troop_set_slot, ":troop_no", slot_troop_promised_fief, 0),
	  ##NEW
	  (try_begin),
		 (eq, ":troop_no", "trp_player"),
		 #Don't change of this for the player.
	  (else_try),
	    (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
		 (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
			(eq, ":faction_no", "$players_kingdom"),
		 (ge, ":new_faction_leader", 0),
		 (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
		 (this_or_next|eq, ":new_faction_leader", "trp_player"),
		 (this_or_next|troop_slot_eq, ":new_faction_leader", slot_troop_spouse, "trp_player"),
			(troop_slot_eq, "trp_player", slot_troop_spouse, ":new_faction_leader"),
		 #Joined faction that player is ruler or co-ruler of.  Don't forget
		 #any promises received.
		 (troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
	  (else_try),
	     #Joined a new faction.  Previous promises moot.
		 (troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
		 (troop_set_slot, ":troop_no", slot_lord_recruitment_argument, 0),
		 (troop_set_slot, ":troop_no", slot_lord_recruitment_candidate, 0),
		 (troop_set_slot, ":troop_no", slot_troop_promised_fief, 0),
	  (try_end),
	  ##diplomacy end+

      #Give new title
      # (call_script, "script_troop_set_title_according_to_faction", ":troop_no", ":faction_no"), moved down

      (try_begin),
        (this_or_next|eq, ":faction_no", "$players_kingdom"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (call_script, "script_check_concilio_calradi_achievement"),
      (try_end),

	  #Takes walled centers and dependent villages with him
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_set_faction, ":center_no", ":faction_no"),
        (try_for_range, ":village_no", villages_begin, villages_end),
          (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
          (party_set_faction, ":village_no", ":faction_no"),
          (party_get_slot, ":farmer_party_no", ":village_no", slot_village_farmer_party),
          (try_begin),
            (gt, ":farmer_party_no", 0),
            (party_is_active, ":farmer_party_no"),
            (party_set_faction, ":farmer_party_no", ":faction_no"),
          (try_end),
          (try_begin),
            (party_get_slot, ":old_town_lord", ":village_no", slot_town_lord),
            (neq, ":old_town_lord", ":troop_no"),
            (party_set_slot, ":village_no", slot_town_lord, stl_unassigned),
            ##diplomacy start+ Invalidate old lord's cached center points
            (gt, ":old_town_lord", -1),
            (troop_set_slot, ":old_town_lord", dplmc_slot_troop_center_points_plus_one, 0),
            ##diplomacy end+
          (try_end),
        (try_end),
      (try_end),

	  #Dependant kingdom ladies switch faction
	  (try_for_range, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
		##diplomacy start+ This is required if kingdom ladies can be promoted to other roles
        (this_or_next|troop_slot_eq, ":kingdom_lady", slot_troop_occupation, 0),#for prisoners
		   (troop_slot_eq, ":kingdom_lady", slot_troop_occupation, slto_kingdom_lady),
		(store_faction_of_troop, reg0, ":kingdom_lady"),
		(this_or_next|eq, reg0, ":orig_faction"),
		(neg|faction_slot_eq, reg0, slot_faction_state, sfs_active),
		##diplomacy end+
		(call_script, "script_get_kingdom_lady_social_determinants", ":kingdom_lady"),
		(assign, ":closest_male_relative", reg0),
		(assign, ":new_center", reg1),

		(eq, ":closest_male_relative", ":troop_no"),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":kingdom_lady"),
			(display_message, "@{!}DEBUG - {s4} faction changed by guardian moving"),
		(try_end),

		(troop_set_faction, ":kingdom_lady", ":faction_no"),
        (call_script, "script_troop_set_title_according_to_faction", ":kingdom_lady", ":faction_no"),
		(troop_slot_eq, ":kingdom_lady", slot_troop_prisoner_of_party, -1),
		(troop_set_slot, ":kingdom_lady", slot_troop_cur_center, ":new_center"),
	  (try_end),

      #Give new title
      (call_script, "script_troop_set_title_according_to_faction", ":troop_no", ":faction_no"), #moved from top

	  #Remove his control over villages under another fortress
      (try_for_range, ":village_no", villages_begin, villages_end),
        (party_slot_eq, ":village_no", slot_town_lord, ":troop_no"),
        (store_faction_of_party, ":village_faction", ":village_no"),
        (try_begin),
          (neq, ":village_faction", ":faction_no"),
          (party_set_slot, ":village_no", slot_town_lord, stl_unassigned),
          ##diplomacy start+ invalidate cached center points
          (gt, ":old_town_lord", -1),
          (troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, 0),
          ##diplomacy end+
        (try_end),
      (try_end),

	  #Free prisoners
      (try_begin),
        (troop_get_slot, ":leaded_party", ":troop_no", slot_troop_leaded_party),
        (gt, ":leaded_party", 0),
        (party_set_faction, ":leaded_party", ":faction_no"),
        (party_get_num_prisoner_stacks, ":num_stacks", ":leaded_party"),
        (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":leaded_party", ":troop_iterator"),
          (store_troop_faction, ":cur_faction", ":cur_troop_id"),
          (troop_is_hero, ":cur_troop_id"),
          (eq, ":cur_faction", ":faction_no"),
          (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
          (party_remove_prisoners, ":leaded_party", ":cur_troop_id", 1),
        (try_end),
      (try_end),

	  #Annull all quests of which the lord is giver
	  (try_for_range, ":quest", all_quests_begin, all_quests_end),
		(check_quest_active, ":quest"),
		(quest_slot_eq, ":quest", slot_quest_giver_troop, ":troop_no"),

		(str_store_troop_name, s4, ":troop_no"),
		(try_begin),
		  (eq, "$cheat_mode", 1),
  		  (display_message, "str_s4_changing_sides_aborts_quest"),
        (try_end),
		(call_script, "script_abort_quest", ":quest", 0),
	  (try_end),

	  #Boot all lords out of centers whose faction has changed
	  ##diplomacy start+ add check for promoted kingdom ladies
	  #(try_for_range, ":lord_to_move", active_npcs_begin, active_npcs_end),
	  (try_for_range, ":lord_to_move", heroes_begin, heroes_end),
		 (troop_slot_ge, ":lord_to_move", slot_troop_leaded_party, 1),
	  ##diplomacy end+
		(troop_get_slot, ":lord_led_party", ":lord_to_move", slot_troop_leaded_party),
	    (party_is_active, ":lord_led_party"),
		(party_get_attached_to, ":led_party_attached", ":lord_led_party"),
		(is_between, ":led_party_attached", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, ":led_party_faction", ":lord_led_party"),
		(store_faction_of_party, ":attached_party_faction", ":led_party_attached"),
		(neq, ":led_party_faction", ":attached_party_faction"),

		(party_detach, ":lord_led_party"),
	  (try_end),

	  #Increase relation with lord in new faction by 5
	  #Or, if player kingdom, make inactive pending confirmation
	  (faction_get_slot, ":faction_liege", ":faction_no", slot_faction_leader),
	  (try_begin),
		(eq, ":faction_liege", "trp_player"),
		(neq, ":troop_no", "$g_talk_troop"),
	    (troop_set_slot, ":troop_no", slot_troop_occupation, slto_inactive), #POSSIBLE REASON 1
	  (else_try),
	   ##diplomacy start+ Add support for promoted ladies
		##OLD:
		#(is_between, ":faction_liege", active_npcs_begin, active_npcs_end),
		#(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
		##NEW:
		(is_between, ":faction_liege", heroes_begin, heroes_end),
		(is_between, ":troop_no", heroes_begin, heroes_end),
		##diplomacy end+
		(call_script, "script_troop_change_relation_with_troop", ":faction_liege", ":troop_no", 5),
		(val_add, "$total_indictment_changes", 5),
	  (try_end),

	  #Break courtship relations
	  (try_begin),
	  	(troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
		#Already married, do nothing
	  (else_try),
		(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
		##diplomacy start+
		#Bug fix: don't do this for pretenders.
		(neg|is_between, ":troop_no", kings_begin, kings_end),
		(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
		##diplomacy end+
	    (try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_get_slot, ":courted_lady", ":troop_no", ":love_interest_slot"),
            ##diplomacy start+ don't call this for bad values
            (is_between, ":courted_lady", kingdom_ladies_begin, kingdom_ladies_end),
            ##diplomacy end+
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":courted_lady", ":troop_no"),
	    (try_end),
		##diplomacy start+
		# Don't call this script for married troops / rulers
		#(call_script, "script_assign_troop_love_interests", ":troop_no"),
		(try_begin),
			(neg|troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
			(neg|is_between, ":troop_no", kings_begin, kings_end),
			(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
			(call_script, "script_assign_troop_love_interests", ":troop_no"),
		(try_end),
		##diplomacy end+
	  (else_try),
		(is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
				(troop_slot_eq, ":active_npc", ":love_interest_slot", ":troop_no"),
				(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":troop_no", ":active_npc"),
			(try_end),
		(try_end),
	  (try_end),

	  #Stop raidings/sieges of new faction's fief if there is any
	  (troop_get_slot, ":troop_party", ":troop_no", slot_troop_leaded_party),
	  (try_for_range, ":center_no", centers_begin, centers_end),
	    (party_slot_eq, ":center_no", slot_party_type, spt_village),
	    (party_get_slot, ":raided_by", ":center_no", slot_village_raided_by),
	    (eq, ":raided_by", ":troop_party"),
	    (party_set_slot, ":center_no", slot_village_raided_by, -1),
	    (try_begin),
	      (party_slot_eq, ":center_no", slot_village_state, svs_being_raided),
	      (party_set_slot, ":center_no", slot_village_state, svs_normal),
	      (party_set_extra_text, ":center_no", "str_empty_string"),
	    (try_end),
	  (else_try),
	    (party_get_slot, ":besieged_by", ":center_no", slot_center_is_besieged_by),
	    (eq, ":besieged_by", ":troop_party"),
	    (party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
	    (try_begin),
	      (party_slot_eq, ":center_no", slot_village_state, svs_under_siege),
	      (party_set_slot, ":center_no", slot_village_state, svs_normal),
	      (party_set_extra_text, ":center_no", "str_empty_string"),
	    (try_end),
	  (try_end),

      (call_script, "script_update_all_notes"),

      (call_script, "script_update_village_market_towns"),
      (assign, "$g_recalculate_ais", 1),
      ])
]
