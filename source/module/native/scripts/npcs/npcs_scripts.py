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

####################################################################################################################
# NPC LOGIC & CONVERSATIONS
# 
# This file governs the behavior of Lords, Ladies, and Companions.
# It handles marriages, courtship, personality clashes, and family relationships.
####################################################################################################################

npcs_scripts = [
  # This script is called from the game engine when the companion limit is needed for a party.
  # INPUT: arg1 = none
  # OUTPUT: reg0 = companion_limit
  ("game_get_party_companion_limit",
    [
      (assign, ":troop_no", "trp_player"),

      (assign, ":limit", 30),
      (store_skill_level, ":skill", "skl_leadership", ":troop_no"),
      (store_attribute_level, ":charisma", ":troop_no", ca_charisma),
      (val_mul, ":skill", 5),
      (val_add, ":limit", ":skill"),
      (val_add, ":limit", ":charisma"),

      #SB : possibly inherit half of spouse's renown
      (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),
      (store_div, ":renown_bonus", ":troop_renown", 25),
      (val_add, ":limit", ":renown_bonus"),

      #SB : add non-standard size modifiers here
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
        (try_begin),
          (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
          (store_mul, ":king_bonus", "$player_right_to_rule", 5),
          (val_clamp, ":king_bonus", dplmc_marshal_party_bonus, dplmc_monarch_party_bonus + 1), #to match marshal amount
          (val_add, ":limit", ":king_bonus"),
        (try_end),
        (try_begin),
          (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
          (val_add, ":limit", dplmc_marshal_party_bonus),
        (try_end),
        #party takes additional 20 limit per each castle its party leader owns
        (try_for_range, ":cur_center", castles_begin, castles_end),
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          (val_add, ":limit", dplmc_castle_party_bonus),
        (try_end),

        ##diplomacy begin
        (assign, ":percent", 100),
        (assign, ":policy_min", -3),
        (assign, ":policy_max", 4),

        (try_begin),
            (this_or_next|eq, "$players_kingdom", "fac_player_supporters_faction"),
                (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
            (faction_get_slot, ":policy_max", "$players_kingdom", slot_faction_num_towns),
            (faction_get_slot, reg0, "$players_kingdom", slot_faction_num_castles),
            (val_add, ":policy_max", reg0),
            (val_clamp, ":policy_max", 0, 4),#0, 1, 2, 3
            (store_mul, ":policy_min", ":policy_max", -1),
            (val_add, ":policy_max", 1),#one greater than the maximum
        (try_end),
        ##diplomacy end+

        (try_begin),
          (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
          # (val_add, ":limit", "$player_right_to_rule"),
          (try_begin),
            (faction_get_slot, ":centralization", "$players_kingdom", dplmc_slot_faction_centralization),
            (neq, ":centralization", 0),
            (val_clamp, ":centralization", ":policy_min", ":policy_max"),
            (val_mul, ":centralization", 10),
            (val_add, ":percent", ":centralization"),
          (try_end),

        (else_try),
          (try_begin),
            (faction_get_slot, ":centralization", "$players_kingdom", dplmc_slot_faction_centralization),
            (neq, ":centralization", 0),
            (val_clamp, ":centralization", ":policy_min", ":policy_max"),
            (val_mul, ":centralization", -3),
            (val_add, ":percent", ":centralization"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":aristocracy", "$players_kingdom", dplmc_slot_faction_aristocracy),
            (neq, ":aristocracy", 0),
            (val_clamp, ":aristocracy", ":policy_min", ":policy_max"),
            (val_mul, ":aristocracy", 3),
            (val_add, ":percent", ":aristocracy"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":quality", "$players_kingdom", dplmc_slot_faction_quality),
            (neq, ":quality", 0),
            (val_clamp, ":quality", ":policy_min", ":policy_max"),
            (val_mul, ":quality", -4),
            (val_add, ":percent", ":quality"),
          (try_end),
        (try_end),

        (try_begin),
          (faction_get_slot, ":serfdom", "$players_kingdom", dplmc_slot_faction_serfdom),
          (neq, ":serfdom", 0),
          (val_clamp, ":serfdom", ":policy_min", ":policy_max"),
          (val_mul, ":serfdom", 2),
          (val_add, ":percent", ":serfdom"),
        (try_end),

        (val_mul, ":limit", ":percent"),
        ##nested diplomacy start+ Round correctly
        (val_add, ":limit", 50),
        ##nested diplomacy end+
        (val_div, ":limit", 100),
        ##diplomacy end
      (try_end),

      (assign, reg0, ":limit"),
      (set_trigger_result, reg0),
  ]),


  #script_game_reset_player_party_name:

  # script_npc_get_troop_wage
  # This script is called from module system to calculate troop wages for npc parties.
  # Input:
  # param1: troop_id
  # Output: reg0: weekly wage

  ("npc_get_troop_wage",
    [
      (store_script_param_1, ":troop_id"),
      (assign,":wage", 0),
      (try_begin),
        (troop_is_hero, ":troop_id"),
      (else_try),
        (store_character_level, ":wage", ":troop_id"),
        (val_mul, ":wage", ":wage"),
        (val_add, ":wage", 50),
        (val_div, ":wage", 30),
        (troop_is_mounted, ":troop_id"),
        (val_mul, ":wage", 5),
        (val_div, ":wage", 4),
      (try_end),
      (assign, reg0, ":wage"),
  ]),

  #script_setup_talk_info
  #script_setup_talk_info_companions
  ("setup_talk_info_companions",
    [
      ##diplomacy start+ Ensure $character_gender is set correctly (it should have been set during character creation)
      (try_begin),
         (call_script, "script_cf_dplmc_troop_is_female", "trp_player"),
	     (assign, "$character_gender", 1),
      (else_try),
	     (assign, "$character_gender", 0),
      (try_end),
	  ##diplomacy end+
      (call_script, "script_dplmc_npc_morale", "$g_talk_troop", 1), #SB : number + bar string in s63
      (assign, ":troop_morale", reg0),
      (talk_info_set_relation_bar, ":troop_morale"),
      (talk_info_set_line, 3, s63),

      (str_store_troop_name, s61, "$g_talk_troop"),
      (talk_info_set_line, 0, s61),
      # (str_store_string, s61, "@{!} {s61}"),
      (assign, reg1, ":troop_morale"),
      (str_store_string, s62, "str_morale_reg1"),
      (talk_info_set_line, 1, s62),
  ]),
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
  ]),

  #script_party_remove_all_prisoners:
  # INPUT:
  # param1: Party-id to add the second part
  # param2: Party-id which will be added to the first one.
  # "$g_move_heroes" : controls if heroes will also be added.

  ("party_add_party_companions",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_members, ":target_party", ":stack_troop", ":stack_size"),
        (party_stack_get_num_wounded, ":num_wounded", ":source_party", ":stack_no"),
        (party_wound_members, ":target_party", ":stack_troop", ":num_wounded"),
      (try_end),
  ]),

  #script_party_add_party_prisoners:
  # INPUT:
  # param1: Party-id to add the second part
  # param2: Party-id which will be added to the first one.
  # "$g_move_heroes" : controls if heroes will also be added.

  ("party_prisoners_add_party_companions",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_prisoners, ":target_party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),

  #script_party_prisoners_add_party_prisoners:
  # Input: arg1 = faction_no
  # Output: reg0 = troop_no, Can Fail!
  ("cf_get_random_lord_except_king_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),


  # script_cf_get_random_lord_from_another_faction_in_a_center
  # Input: arg1 = troop_no
  # Output: none
  ("calculate_hero_weekly_net_income_and_add_to_wealth",
    [
      (store_script_param_1, ":troop_no"),

      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),

      (assign, ":weekly_income", 750), #let every hero receive 750 denars by default

      (store_character_level, ":troop_level", ":troop_no"),
      (store_mul, ":level_income", ":troop_level", 10),
      (val_add, ":weekly_income", ":level_income"),

      (store_troop_faction,":faction_no", ":troop_no"),

	  ##diplomacy start+
	  #Bonus for marshall and/or faction leader (is 1000 in native)
	  (assign, ":leader_bonus_gold", 1000),
	  (assign, ":bonus_applied", 0),
	  (try_begin),
		   #OPTIONAL CHANGE (HIGH)
		   (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
 		   #Scale marshall and king bonus gold by number of remaining kingdoms,
           #so the total amount paid out remains the same even as kingdoms disappear.
           #This is only enabled if changes are on "HIGH".
           (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
           (store_sub, ":original_kingdoms", npc_kingdoms_end, npc_kingdoms_begin),#deliberately excludes player kingdom
           (ge, ":original_kingdoms", 2),
           (assign, ":current_kingdoms", 0),
           (try_for_range, ":other_fac", kingdoms_begin, kingdoms_end),#deliberately include player kingdom
             (faction_slot_eq, ":other_fac", slot_faction_state, sfs_active),
             (val_add, ":current_kingdoms", 1),
           (try_end),
           (ge, ":current_kingdoms", 1),
           (lt, ":current_kingdoms", ":original_kingdoms"),
           (val_mul, ":leader_bonus_gold", ":original_kingdoms"),
           (val_div, ":leader_bonus_gold", ":current_kingdoms"),
		   #Examples, assuming 6 starting kingdoms and no player kingdom:
		   #6 kingdoms: 1000 each, 1000 * 6 = 6000 total
		   #5 kingdoms: 1200 each, 1200 * 5 = 6000 total
		   #4 kingdoms: 1500 each, 1500 * 4 = 6000 total
		   #3 kingdoms: 2000 each, 2000 * 3 = 6000 total
		   #2 kingdoms: 3000 each, 3000 * 2 = 6000 total
		   #1 kingdom:  6000 each, 6000 * 1 = 6000 total
      (try_end),
	  ##diplomacy end+

      (try_begin), #check if troop is kingdom leader
        (faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
        ##diplomacy start+
		#OLD BEHAVIOR:
        #(val_add, ":weekly_income", 1000),
		#NEW BEHAVIOR:
		(val_add, ":weekly_income", ":leader_bonus_gold"),
		(val_add, ":bonus_applied", 1),
        ##diplomacy end+
      (try_end),

      (try_begin), #check if troop is marshall
        (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
        ##diplomacy start+
		#OLD BEHAVIOR:
        #(val_add, ":weekly_income", 1000),
		#NEW BEHAVIOR:
	    (val_add, ":weekly_income", ":leader_bonus_gold"),
		(val_add, ":bonus_applied", 1),
        ##diplomacy end+
      (try_end),

	  ##diplomacy start+
	  (try_begin),
	  	  #OPTIONAL CHANGE (MEDIUM)
		  (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		  #If the lord is the spouse of the faction leader and no better bonus
		  #applied, the lord gets half of the bonus if either (1) there is no
		  #marshall, or (2) the faction leader is the player.
		  (eq, ":bonus_applied", 0),
		  (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
  		  #Don't do the usual polygamy check: the bonus only applies to
		  #one of the spouses.
		  (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
		  (ge, ":faction_leader", 0),
		  (troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
		  #Don't apply the bonus unless the faction leader bonus is going
		  #all/partially uncollected, or the marshal bonus is going uncollected.
		  (this_or_next|neg|faction_slot_ge, ":faction_no", slot_faction_marshall, 0),
			(eq, ":faction_leader", "trp_player"),
		  #Apply bonus
		  (val_add, ":bonus_applied", 1),
		  (store_div, reg0, ":leader_bonus_gold", 2),
		  (val_add, ":weekly_income", reg0),
	  (try_end),
	  ##diplomacy end+

      (assign, ":cur_weekly_wage", 0),
      (try_begin),
        (gt, ":party_no",0),
        (call_script, "script_calculate_weekly_party_wage", ":party_no"),
        (assign, ":cur_weekly_wage", reg0),
      (try_end),
      ##diplomacy start+
      (try_begin),
	     #take into account leader's leadership skill, like in CC
	     #economics changes must be enabled
         (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
         (store_skill_level, ":leadership_level", "skl_leadership", ":troop_no"),
         (val_clamp, ":leadership_level", 0, 11),
         (store_mul, ":leadership_bonus", 5, ":leadership_level"),
         (store_sub, ":leadership_factor", 100, ":leadership_bonus"),
         (val_mul, ":cur_weekly_wage", ":leadership_factor"),  #wage = wage * (100 - 5*leadership)/100
         (val_div, ":cur_weekly_wage", 100),
      (try_end),

	  #Store the change in income for use below
	  (store_sub, ":net_income", ":weekly_income", ":cur_weekly_wage"),
      ##diplomacy end+
      (val_sub, ":weekly_income", ":cur_weekly_wage"),

      (val_add, ":cur_wealth", ":weekly_income"),

	  (try_begin),
		(lt, ":cur_wealth", 0),
		(store_sub, ":percent_under", 0, ":cur_wealth"),
		(val_mul, ":percent_under", 100),
		(val_div, ":percent_under", ":cur_weekly_wage"),
		(val_div, ":percent_under", 5), #Max 20 percent
		##diplomacy start+
		#The above assumption could be violated if the lord entered this
		#script with a negative wealth.  Add a failsafe.
		(val_clamp, ":percent_under", 0, 21),
		##diplomacy end+
		(call_script, "script_party_inflict_attrition", ":party_no", ":percent_under", 1),
	  (try_end),

	  ##diplomacy start+
	  #Apply gold change
	  (try_begin),
	     #If the wealth change was positive, some of it may go to the lord's holdings.
	     (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
	     (ge, ":net_income", 1),
		 (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":net_income", ":troop_no"),
	  (else_try),
	     #Fall through to old version:
		 #OLD VERSION:
         (val_max, ":cur_wealth", 0),
         (troop_set_slot, ":troop_no", slot_troop_wealth, ":cur_wealth"),
	  (try_end),
	  ##diplomacy end+
  ]),

  # script_cf_reinforce_party
  # Input: arg1 = troop_no (hero of the party)
  # Output: none
  ("hire_men_to_kingdom_hero_party",
    [
      (store_script_param_1, ":troop_no"),

      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),

      #while hiring reinforcements party leaders can only use 3/4 of their budget. This value is holding in ":hiring budget".
      (assign, ":hiring_budget", ":cur_wealth"),
      (val_mul, ":hiring_budget", 3),
      (val_div, ":hiring_budget", 4),

      (call_script, "script_party_get_ideal_size", ":party_no"),
      (assign, ":ideal_size", reg0),
      (store_mul, ":ideal_top_size", ":ideal_size", 3),
      (val_div, ":ideal_top_size", 2),

	  #(try_begin),
	  #	(ge, "$cheat_mode", 1),
      #  (str_store_troop_name, s7, ":troop_no"),
      #  (assign, reg9, ":cur_wealth"),
      #  (display_message, "@{!}DEBUGS : {s7} total budget is {reg9}"),
      #  (assign, reg6, ":ideal_size"),
      #  (assign, reg7, ":ideal_top_size"),
      #  (assign, reg8, ":hiring_budget"),
      #  (display_message, "str_debug__hiring_men_to_s7_ideal_size__reg6_ideal_top_size__reg7_hiring_budget__reg8"),
      #(try_end),

      (party_get_num_companions, ":party_size", ":party_no"),

      (store_faction_of_party, ":party_faction", ":party_no"),
      (try_begin),
        (this_or_next|eq, ":party_faction", "fac_player_supporters_faction"),
        (eq, ":party_faction", "$players_kingdom"),
        (assign, ":reinforcement_cost", reinforcement_cost_moderate),
      (else_try),
        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
        (assign, ":reinforcement_cost", reinforcement_cost_moderate),
        (try_begin),
          (eq, ":reduce_campaign_ai", 0), #hard
          (assign, ":reinforcement_cost", reinforcement_cost_hard),
        (else_try),
          (eq, ":reduce_campaign_ai", 1), #moderate
          (assign, ":reinforcement_cost", reinforcement_cost_moderate),
        (else_try),
          (eq, ":reduce_campaign_ai", 2), #easy
          (assign, ":reinforcement_cost", reinforcement_cost_easy),
        (try_end),
      (try_end),

      (assign, ":num_rounds", 1),
      (try_for_range, ":unused", 0 , ":num_rounds"),
        (try_begin),
          (lt, ":party_size", ":ideal_size"),
          (gt, ":hiring_budget", ":reinforcement_cost"),
          (gt, ":party_no", 0),
          (call_script, "script_cf_reinforce_party", ":party_no"),
          (val_sub, ":cur_wealth", ":reinforcement_cost"),
          (troop_set_slot, ":troop_no", slot_troop_wealth, ":cur_wealth"),
        (else_try),
          (gt, ":party_size", ":ideal_top_size"),
          (store_troop_faction, ":troop_faction", ":troop_no"),
          (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
          (assign, ":total_regulars", 0),
          (assign, ":total_regular_levels", 0),
          (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
            (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
            (store_character_level, ":stack_level", ":stack_troop"),
            (store_troop_faction, ":stack_faction", ":stack_troop"),
            (try_begin),
              (eq, ":troop_faction", ":stack_faction"),
              (val_mul, ":stack_level", 3), #reducing the chance of the faction troops' removal
            (try_end),
            (val_mul, ":stack_level", ":stack_size"),
            (val_add, ":total_regulars", ":stack_size"),
            (val_add, ":total_regular_levels", ":stack_level"),
          (try_end),
          (gt, ":total_regulars", 0),
          (store_div, ":average_level", ":total_regular_levels", ":total_regulars"),
          (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
            (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
            (store_character_level, ":stack_level", ":stack_troop"),
            (store_troop_faction, ":stack_faction", ":stack_troop"),
            (try_begin),
              (eq, ":troop_faction", ":stack_faction"),
              (val_mul, ":stack_level", 3),
            (try_end),
            (store_sub, ":level_dif", ":average_level", ":stack_level"),
            (val_div, ":level_dif", 3),
            (store_add, ":prune_chance", 10, ":level_dif"),
            (gt, ":prune_chance", 0),
            (call_script, "script_get_percentage_with_randomized_round", ":stack_size", ":prune_chance"),
            (gt, reg0, 0),
            (party_remove_members, ":party_no", ":stack_troop", reg0),
          (try_end),
        (try_end),
      (try_end),
  ]),

  # script_get_percentage_with_randomized_round
  # Input: arg1 = troop_no, arg2 = center_no
  # Output: $pout_party = party_no
  ("create_kingdom_hero_party",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":center_no", 2),

      (store_troop_faction, ":troop_faction_no", ":troop_no"),

      (assign, "$pout_party", -1),
      (try_begin),
        (eq, "$g_there_is_no_avaliable_centers", 0),
        (set_spawn_radius, 0),
      (else_try),
        (set_spawn_radius, 15),
      (try_end),
      (spawn_around_party, ":center_no", "pt_kingdom_hero_party"),

      (assign, "$pout_party", reg0),

      ###faction icons### dckplmc
      (try_begin),

        (assign, ":icon_faction", ":troop_faction_no"),

        (try_begin),
          (gt, ":troop_faction_no", "fac_commoners"),
          (this_or_next|eq, ":troop_faction_no", "fac_player_faction"),
          (this_or_next|eq, ":troop_faction_no", "fac_player_supporters_faction"),
          (eq, ":troop_faction_no", "$players_kingdom"),
          (neg|is_between, ":troop_faction_no", npc_kingdoms_begin, npc_kingdoms_end),
          (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
          (assign, ":icon_faction", "$g_player_culture"),
        (try_end),

          (is_between, ":icon_faction", npc_kingdoms_begin, kingdoms_end),
          (store_sub, ":fac_offset", ":icon_faction", npc_kingdoms_begin),
          (try_begin),
              (faction_slot_eq, ":icon_faction", slot_faction_leader, ":troop_no"),
              (store_add, ":icon", "icon_kingdom_1_king", ":fac_offset"),
              (party_set_icon, "$pout_party", ":icon"),
          (else_try),
              (store_add, ":icon", "icon_kingdom_1_lord", ":fac_offset"),
              (party_set_icon, "$pout_party", ":icon"),
          (try_end),
      (try_end),
      ###

      (party_set_faction, "$pout_party", ":troop_faction_no"),
      (party_set_slot, "$pout_party", slot_party_type, spt_kingdom_hero_party),
      (call_script, "script_party_set_ai_state", "$pout_party", spai_undefined, -1),
      (troop_set_slot, ":troop_no", slot_troop_leaded_party, "$pout_party"),
      (party_add_leader, "$pout_party", ":troop_no"),
      (str_store_troop_name, s5, ":troop_no"),
      (party_set_name, "$pout_party", "str_s5_s_party"),

      (party_set_slot, "$pout_party", slot_party_commander_party, -1), #we need this because 0 is player's party!

      #Setting the flag icon
      #normal_banner_begin
      (troop_get_slot, ":cur_banner", ":troop_no", slot_troop_banner_scene_prop),
      (try_begin),
        (gt, ":cur_banner", 0),
        (val_sub, ":cur_banner", banner_scene_props_begin),
        (val_add, ":cur_banner", banner_map_icons_begin),
        (party_set_banner_icon, "$pout_party", ":cur_banner"),
      (else_try),
      #custom_banner_begin
          (eq, ":cur_banner", -1),
          (troop_get_slot, ":flag_icon", ":troop_no", slot_troop_custom_banner_map_flag_type),
          (try_begin),
           (ge, ":flag_icon", 0),
           (val_add, ":flag_icon", custom_banner_map_icons_begin),
           (party_set_banner_icon, "$pout_party", ":flag_icon"),
          (try_end),
      (try_end),

      (try_begin),
        #because of below two lines, lords can only hire more than one party_template(stack) at game start once a time during all game.
        (troop_slot_eq, ":troop_no", slot_troop_spawned_before, 0),
        (troop_set_slot, ":troop_no", slot_troop_spawned_before, 1),
        (assign, ":num_tries", 20),
        (try_begin),
          (store_troop_faction, ":troop_kingdom", ":troop_no"),
          (faction_slot_eq, ":troop_kingdom", slot_faction_leader, ":troop_no"),
          (assign, ":num_tries", 50),
        (try_end),

        #(str_store_troop_name, s0, ":troop_no"),
        #(display_message, "{!}str_debug__hiring_men_to_party_for_s0"),

        (try_for_range, ":unused", 0, ":num_tries"),
          (call_script, "script_hire_men_to_kingdom_hero_party", ":troop_no"),
        (try_end),

        (assign, ":xp_rounds", 0),

        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
        (try_begin),
          (this_or_next|eq, ":troop_faction_no", "$players_kingdom"),
          (eq, ":troop_faction_no", "fac_player_supporters_faction"),
          (assign, ":xp_rounds", 0),
        (else_try),
          (eq, ":reduce_campaign_ai", 0), #hard
          (assign, ":xp_rounds", 2),
        (else_try),
          (eq, ":reduce_campaign_ai", 1), #moderate
          (assign, ":xp_rounds", 1),
        (else_try),
          (eq, ":reduce_campaign_ai", 2), #easy
          (assign, ":xp_rounds", 0),
        (try_end),

        (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
        (store_div, ":renown_xp_rounds", ":renown", 100),
        (val_add, ":xp_rounds", ":renown_xp_rounds"),
        (try_for_range, ":unused", 0, ":xp_rounds"),
          (call_script, "script_upgrade_hero_party", "$pout_party", 4000),
        (try_end),
      (try_end),
  ]),

  # script_create_kingdom_party_if_below_limit
  # Input: arg1 = troop_no,
  # Output: none
  ("recruit_troop_as_companion",
    [
      (store_script_param_1, ":troop_no"),
      ##diplomacy start+
      ##Save civilian clothing of companions (and ladies, etc.)
      (try_begin),
         (troop_is_hero, ":troop_no"),
         (neg|troop_slot_ge, ":troop_no", slot_troop_playerparty_history, 1),#only call this the first time they join
         (call_script, "script_dplmc_save_civilian_clothing", ":troop_no"),#although, redundant calls should be save
         (call_script, "script_change_troop_renown", ":troop_no", 1),#although, redundant calls should be save
      (try_end),
      ##Preserve former occupations enfeoffed companions
      (try_begin),
          (troop_is_hero, ":troop_no"),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (neg|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
          (troop_set_slot, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
      (try_end),
      ##diplomacy end+
      (try_begin), #SB :  spouse scripts
        (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
        (troop_set_slot, ":troop_no", slot_troop_occupation, slto_player_companion),
        (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
      (else_try), #SB : store that lady was recruited as companion
        (troop_set_slot, ":troop_no", slot_troop_first_encountered, "$current_town"),
        (troop_set_slot, ":troop_no", slot_troop_cur_center, -1), #dckplmc
      (try_end),
      (troop_set_auto_equip, ":troop_no", 0),
      (party_add_members, "p_main_party", ":troop_no", 1),
      (str_store_troop_name_link, s6, ":troop_no"),
      (display_log_message, "@{s6} has joined your party.", message_alert), #SB : colourize
      (play_sound, "snd_tutorial_2"), #SB : chime sound
      (troop_set_note_available, ":troop_no", 1),

      (try_begin),
        (is_between, ":troop_no", companions_begin, companions_end),
        (store_sub, ":companion_number", ":troop_no", companions_begin),

        (set_achievement_stat, ACHIEVEMENT_KNIGHTS_OF_THE_ROUND, ":companion_number", 1),

        (assign, ":number_of_companions_hired", 0),
        (try_for_range, ":cur_companion", 0, 16),
          (get_achievement_stat, ":is_hired", ACHIEVEMENT_KNIGHTS_OF_THE_ROUND, ":cur_companion"),
          (eq, ":is_hired", 1),
          (val_add, ":number_of_companions_hired", 1),
        (try_end),

        (try_begin),
          (ge, ":number_of_companions_hired", 6),
          (unlock_achievement, ACHIEVEMENT_KNIGHTS_OF_THE_ROUND),
        (try_end),
      (try_end),
  ]),


  # script_setup_random_scene
("setup_meet_lady",
    [
      (store_script_param_1, ":lady_no"),
      (store_script_param_2, ":center_no"),

      #(mission_tpl_entry_set_override_flags, "mt_visit_town_castle", 0, af_override_horse),
      (troop_set_slot, ":lady_no", slot_lady_last_suitor, "trp_player"),

      (set_jump_mission,"mt_visit_town_castle"),
      (party_get_slot, ":castle_scene", ":center_no", slot_town_castle),
      (modify_visitors_at_site,":castle_scene"),
      (reset_visitors),

	  (troop_set_age, "trp_nurse_for_lady", 100),
      (set_visitor, 7, "trp_nurse_for_lady"),

      (assign, ":cur_pos", 16),
	  (set_visitor, ":cur_pos", ":lady_no"),

      (assign, "$talk_context", tc_garden),

      (jump_to_scene,":castle_scene"),
      (scene_set_slot, ":castle_scene", slot_scene_visited, 1),
      (change_screen_mission),
	]),

  # script_find_high_ground_around_pos1
("troop_write_family_relations_to_s1",
    [
    (str_clear, s1),
    #redo, possibly using base from update_troop_notes
    ]),

   # script_write_family_relation_as_s3s_s2_to_s4

  # Inputs: arg1 = troop_no, arg2 = family_no (valid slot no after slot_troop_family_begin)
  # Outputs: s11 = what troop_1 is to troop_2, reg0 = strength of relationship. Normally, "$g_talk_troop" should be troop_2

  ("troop_get_family_relation_to_troop",
    [
    (store_script_param_1, ":troop_1"),
    (store_script_param_2, ":troop_2"),

    ##diplomacy start+ use gender script
    #(troop_get_type, ":gender_1", ":troop_1"),
	(call_script, "script_dplmc_store_troop_is_female", ":troop_1"),
	(assign, ":gender_1", reg0),
	##diplomacy end+
	(assign, ":relation_strength", 0),

    (troop_get_slot, ":spouse_of_1", ":troop_1", slot_troop_spouse),
    (troop_get_slot, ":spouse_of_2", ":troop_2", slot_troop_spouse),

	(try_begin),
		(gt, ":spouse_of_1", -1),
		(troop_get_slot, ":father_of_spouse_of_1", ":spouse_of_1", slot_troop_father),
	(else_try),
		(assign, ":father_of_spouse_of_1", -1),
	(try_end),

	(try_begin),
		(gt, ":spouse_of_2", -1),
		(troop_get_slot, ":father_of_spouse_of_2", ":spouse_of_2", slot_troop_father),
	(else_try),
		(assign, ":father_of_spouse_of_2", -1),
	(try_end),

	(try_begin),
		(gt, ":spouse_of_2", -1),
		(troop_get_slot, ":mother_of_spouse_of_2", ":spouse_of_2", slot_troop_mother),
	(else_try),
		(assign, ":mother_of_spouse_of_2", -1),
	(try_end),

    (troop_get_slot, ":father_of_1", ":troop_1", slot_troop_father),
    (troop_get_slot, ":father_of_2", ":troop_2", slot_troop_father),

	#For the sake of simplicity, we can assume that all male aristocrats in prior generations either married commoners or procured their brides from the Old Country, thus discounting intermarriage
    (troop_get_slot, ":mother_of_1", ":troop_1", slot_troop_mother),
    (troop_get_slot, ":mother_of_2", ":troop_2", slot_troop_mother),

    ##diplomacy start+
	#Fix a native bug where daughters are their own mothers
        #(fixed in this mod, but still affects old saved games)
        #REMOVED - Instead this occurs once in simple triggers

	##Adding paternal grandmother (begin mostly-unaltered section)
	(try_begin),
		(this_or_next|eq, ":father_of_1", "trp_player"),#dplmc+ added
		(is_between, ":father_of_1", companions_begin, kingdom_ladies_end),
		(troop_get_slot, ":paternal_grandfather_of_1", ":father_of_1", slot_troop_father),
		(troop_get_slot, ":paternal_grandmother_of_1", ":father_of_1", slot_troop_mother),#added
	(else_try),
		(assign, ":paternal_grandfather_of_1", -1),
		(assign, ":paternal_grandmother_of_1", -1),#added
	(try_end),

	(try_begin),
		(this_or_next|eq, ":father_of_2", "trp_player"),#dplmc+ added
		(is_between, ":father_of_2", companions_begin, kingdom_ladies_end),
		(troop_get_slot, ":paternal_grandfather_of_2", ":father_of_2", slot_troop_father),
		(troop_get_slot, ":paternal_grandmother_of_2", ":father_of_2", slot_troop_mother),#added
	(else_try),
		(assign, ":paternal_grandfather_of_2", -1),
		(assign, ":paternal_grandmother_of_2", -1),#added
	(try_end),
	#(end mostly-unaltered section)

	##Adding maternal grandfather and maternal grandmother
	(try_begin),
		(this_or_next|eq, ":mother_of_1", "trp_player"),#dplmc+ added
		(is_between, ":mother_of_1", companions_begin, kingdom_ladies_end),
		(troop_get_slot, ":maternal_grandfather_of_1", ":mother_of_1", slot_troop_father),
		(troop_get_slot, ":maternal_grandmother_of_1", ":mother_of_1", slot_troop_mother),
	(else_try),
		(assign, ":maternal_grandfather_of_1", -1),
		(assign, ":maternal_grandmother_of_1", -1),
	(try_end),

	(try_begin),
		(this_or_next|eq, ":mother_of_2", "trp_player"),#dplmc+ added
		(is_between, ":mother_of_2", companions_begin, kingdom_ladies_end),
		(troop_get_slot, ":maternal_grandfather_of_2", ":mother_of_2", slot_troop_father),
		(troop_get_slot, ":maternal_grandmother_of_2", ":mother_of_2", slot_troop_mother),
	(else_try),
		(assign, ":maternal_grandfather_of_2", -1),
		(assign, ":maternal_grandmother_of_2", -1),
	(try_end),
	##diplomacy end+

    (troop_get_slot, ":guardian_of_1", ":troop_1", slot_troop_guardian),
    (troop_get_slot, ":guardian_of_2", ":troop_2", slot_troop_guardian),

	(str_store_string, s11, "str_no_relation"),

	(try_begin),
	  (eq, ":troop_1", ":troop_2"),
	  #self
	(else_try),
	  ##diplomacy start+
      (this_or_next|eq, ":spouse_of_2", ":troop_1"),#polygamy helper
	  ##diplomacy end+
	  (eq, ":spouse_of_1", ":troop_2"),
	  (assign, ":relation_strength", 20),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_wife"),
	  (else_try),
	    (str_store_string, s11, "str_husband"),
	  (try_end),
	(else_try),
	  (eq, ":father_of_2", ":troop_1"),
	  (assign, ":relation_strength", 15),
	  (str_store_string, s11, "str_father"),
	(else_try),
	  (eq, ":mother_of_2", ":troop_1"),
	  (assign, ":relation_strength", 15),
	  (str_store_string, s11, "str_mother"),
	(else_try),
	  (this_or_next|eq, ":father_of_1", ":troop_2"),
	  (eq, ":mother_of_1", ":troop_2"),
	  (assign, ":relation_strength", 15),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_daughter"),
	  (else_try),
	    (str_store_string, s11, "str_son"),
	  (try_end),
	##diplomacy start+
	(else_try),
	   #Check for half-siblings: sharing a father
	   (neq, ":father_of_1", -1),
	   (eq, ":father_of_1", ":father_of_2"),
	   (neq, ":mother_of_1", ":mother_of_2"),
	   (assign, ":relation_strength", 10),
	   (try_begin),
	     (eq, ":gender_1", tf_female),
	     (str_store_string, s11, "str_dplmc_half_sister"),
	   (else_try),
	     (str_store_string, s11, "str_dplmc_half_brother"),
	   (try_end),
   (else_try),
	   #Check for half-siblings: sharing a mother
	   (neq, ":mother_of_1", -1),
	   (eq, ":mother_of_1", ":mother_of_2"),
	   (neq, ":father_of_1", ":father_of_2"),
	   (assign, ":relation_strength", 10),
	   (try_begin),
	     (eq, ":gender_1", tf_female),
	     (str_store_string, s11, "str_dplmc_half_sister"),
	   (else_try),
	     (str_store_string, s11, "str_dplmc_half_brother"),
	   (try_end),
	##diplomacy end+
	(else_try),
	  #(gt, ":father_of_1", -1), #necessary, as some lords do not have the father registered #dplmc+ replaced
	  (neq, ":father_of_1", -1), #dplmc+ added
	  (eq, ":father_of_1", ":father_of_2"),
	  (assign, ":relation_strength", 10),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_sister"),
	  (else_try),
	    (str_store_string, s11, "str_brother"),
	  (try_end),
	(else_try),
	  (eq, ":guardian_of_2", ":troop_1"),
	  (assign, ":relation_strength", 10),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_sister"),
	  (else_try),
	    (str_store_string, s11, "str_brother"),
	  (try_end),
	(else_try),
	  (eq, ":guardian_of_1", ":troop_2"),
	  (assign, ":relation_strength", 10),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_sister"),
	  (else_try),
	    (str_store_string, s11, "str_brother"),
	  (try_end),
	##diplomacy start+
    (else_try),#polygamy, between two people married to the same person
	   (neq, ":spouse_of_1", -1),
	   (eq, ":spouse_of_2", ":spouse_of_1"),
	   (assign, ":relation_strength", 10),
	   (try_begin),
	      (eq, ":gender_1", tf_female),
	      (str_store_string, s11, "str_dplmc_sister_wife"),
	   (else_try),
	      (str_store_string, s11, "str_dplmc_co_husband"),
	   (try_end),
	##diplomacy end+
	(else_try),
	  #(gt, ":paternal_grandfather_of_1", -1),#dplmc+ replaced
	  (neq, ":father_of_2", -1),#dplmc+ added
	  (this_or_next|eq, ":maternal_grandfather_of_1", ":father_of_2"),#dplmc+ added
	  (eq, ":paternal_grandfather_of_1", ":father_of_2"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_niece"),
	  (else_try),
	    (str_store_string, s11, "str_nephew"),
	  (try_end),
	##diplomacy start+: add niece/nephew through mother
	(else_try),
	  (neq, ":mother_of_2", -1),
  	  (this_or_next|eq, ":maternal_grandmother_of_1", ":mother_of_2"),
	  (eq, ":paternal_grandmother_of_1", ":mother_of_2"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_niece"),
	  (else_try),
	    (str_store_string, s11, "str_nephew"),
	  (try_end),
	##diplomacy end+
	(else_try), #specifically aunt and uncle by blood -- i assume that in a medieval society with lots of internal family conflicts, they would not include aunts and uncles by marriage
	  #(gt, ":paternal_grandfather_of_2", -1),#dplmc+ replaced
	  (neq, ":father_of_1", -1),#dplmc+ added
	  (this_or_next|eq, ":maternal_grandfather_of_2", ":father_of_1"),#dplmc+ added
	  (eq, ":paternal_grandfather_of_2", ":father_of_1"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_aunt"),
	  (else_try),
	    (str_store_string, s11, "str_uncle"),
	  (try_end),
	##diplomacy start+
	#blood uncles & blood aunts, continued (via mother)
	(else_try),
	  (neq, ":mother_of_1", -1),
	  (this_or_next|eq, ":maternal_grandmother_of_2", ":mother_of_1"),
	  (eq, ":paternal_grandmother_of_2", ":mother_of_1"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_aunt"),
	  (else_try),
	    (str_store_string, s11, "str_uncle"),
	  (try_end),
	##diplomacy end+
	(else_try),
	  #(gt, ":paternal_grandfather_of_1", 0),#dplmc+ replaced (why was this one "gt 0" but the previous "gt -1"?)
	  (neq, ":paternal_grandfather_of_1", -1),#dplmc+ added
	  (this_or_next|eq, ":maternal_grandfather_of_2", ":paternal_grandfather_of_1"),#dplmc+ added
	  (eq, ":paternal_grandfather_of_2", ":paternal_grandfather_of_1"),
	  (assign, ":relation_strength", 2),
	  (str_store_string, s11, "str_cousin"),
	##diplomacy start+
	#Add cousin via paternal grandmother or maternal grandparents
	(else_try),
	  (neq, ":maternal_grandfather_of_1", -1),
	  (this_or_next|eq, ":maternal_grandfather_of_2", ":maternal_grandfather_of_1"),
	  (eq, ":paternal_grandfather_of_2", ":maternal_grandfather_of_1"),
	  (assign, ":relation_strength", 2),
	  (str_store_string, s11, "str_cousin"),
	(else_try),
	  (neq, ":paternal_grandmother_of_1", -1),
	  (this_or_next|eq, ":maternal_grandmother_of_2", ":paternal_grandmother_of_1"),
	  (eq, ":paternal_grandmother_of_2", ":paternal_grandmother_of_1"),
	  (assign, ":relation_strength", 2),
	  (str_store_string, s11, "str_cousin"),
	(else_try),
	  (neq, ":maternal_grandmother_of_1", -1),
	  (this_or_next|eq, ":maternal_grandmother_of_2", ":maternal_grandmother_of_1"),
	  (eq, ":paternal_grandmother_of_2", ":maternal_grandmother_of_1"),
	  (assign, ":relation_strength", 2),
	  (str_store_string, s11, "str_cousin"),
	##diplomacy end+
   	(else_try),
   	  (eq, ":father_of_spouse_of_1", ":troop_2"),
   	  (assign, ":relation_strength", 5),
   	  (try_begin),
   	    (eq, ":gender_1", tf_female),
   	    (str_store_string, s11, "str_daughterinlaw"),
   	  (else_try),
   	    (str_store_string, s11, "str_soninlaw"),
   	  (try_end),
	(else_try),
	  (eq, ":father_of_spouse_of_2", ":troop_1"),
	  (assign, ":relation_strength", 5),
	  (str_store_string, s11, "str_fatherinlaw"),
	(else_try),
	  (eq, ":mother_of_spouse_of_2", ":troop_1"),
	  (neq, ":mother_of_spouse_of_2", "trp_player"), #May be necessary if mother for troops not set to -1
	  (assign, ":relation_strength", 5),
	  (str_store_string, s11, "str_motherinlaw"),

	(else_try),
	  #(gt, ":father_of_spouse_of_1", -1), #necessary #dplmc+ replaced
	  (neq, ":father_of_spouse_of_1", -1), #dplmc+ added
	  (eq, ":father_of_spouse_of_1", ":father_of_2"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_sisterinlaw"),
	  (else_try),
	    (str_store_string, s11, "str_brotherinlaw"),
	  (try_end),
	(else_try),
	  #(gt, ":father_of_spouse_of_2", -1), #necessary #dplmc+ replaced
	  (neq, ":father_of_spouse_of_2", -1), #dplmc+ added
	  (eq, ":father_of_spouse_of_2", ":father_of_1"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_sisterinlaw"),
	  (else_try),
	    (str_store_string, s11, "str_brotherinlaw"),
	  (try_end),
	(else_try),
#	  (gt, ":spouse_of_2", -1), #necessary to avoid bug #dplmc+ replaced
	  (neq, ":spouse_of_2", -1), #dplmc+ added
	  (troop_slot_eq, ":spouse_of_2", slot_troop_guardian, ":troop_1"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    #(eq, ":gender_1", tf_female),#dplmc+ replaced
	    (eq, ":gender_1", tf_female),#dplmc+ added
	    (str_store_string, s11, "str_sisterinlaw"),
	  (else_try),
	    (str_store_string, s11, "str_brotherinlaw"),
	  (try_end),
	(else_try),
	  #(gt, ":spouse_of_1", -1), #necessary to avoid bug #dplmc+ replaced
	  (neq, ":spouse_of_1", -1), #dplmc+ added
	  (troop_slot_eq, ":spouse_of_1", slot_troop_guardian, ":troop_2"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_sisterinlaw"),
	  (else_try),
	    (str_store_string, s11, "str_brotherinlaw"),
	  (try_end),
	(else_try),
	  #grandchild
	  (neq, ":troop_2", -1),
	   (this_or_next|eq, ":paternal_grandfather_of_1", ":troop_2"),
	   (this_or_next|eq, ":maternal_grandfather_of_1", ":troop_2"),
	   (this_or_next|eq, ":paternal_grandmother_of_1", ":troop_2"),
		   (eq, ":maternal_grandmother_of_1", ":troop_2"),
	   (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_dplmc_granddaughter"),
	  (else_try),
	    (str_store_string, s11, "str_dplmc_grandson"),
	  (try_end),
	(else_try),
	   #grandparent
	   (neq, ":troop_1", -1),
	   (this_or_next|eq, ":paternal_grandfather_of_2", ":troop_1"),
	   (this_or_next|eq, ":maternal_grandfather_of_2", ":troop_1"),
	   (this_or_next|eq, ":paternal_grandmother_of_2", ":troop_1"),
		   (eq, ":maternal_grandmother_of_2", ":troop_1"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_dplmc_grandmother"),
	  (else_try),
	    (str_store_string, s11, "str_dplmc_grandfather"),
	  (try_end),
	(try_end),

	##diplomacy start+
	##Add relations for rulers not already encoded
	(try_begin),
		(eq, ":relation_strength", 0),
		(neq, ":troop_1", ":troop_2"),
		(try_begin),
			#Lady Isolla of Suno's father King Esterich was King Harlaus's cousin,
			#making them first cousins once removed.  Assign a weight of "1"
			#to this (for reference, the lowest value normally given in Native is 2).
			(this_or_next|eq, ":troop_1", "trp_kingdom_1_lord"),
			    (eq, ":troop_1", "trp_kingdom_1_pretender"),
			(this_or_next|eq, ":troop_2", "trp_kingdom_1_lord"),
			    (eq, ":troop_2", "trp_kingdom_1_pretender"),
			(assign, ":relation_strength", 1),
			(str_store_string, s11, "str_cousin"),
		(else_try),
			#Prince Valdym's uncle was Regent Burelek, father of King Yaroglek,
			#making the two of them first cousins.
			(this_or_next|eq, ":troop_1", "trp_kingdom_2_lord"),
			    (eq, ":troop_1", "trp_kingdom_2_pretender"),
			(this_or_next|eq, ":troop_2", "trp_kingdom_2_lord"),
				(eq, ":troop_2", "trp_kingdom_2_pretender"),
			(assign, ":relation_strength", 2),
			(str_store_string, s11, "str_cousin"),
		(else_try),
			#Sanjar Khan and Dustum Khan were both sons of Janakir Khan
			#(although by different mothers) making them half-brothers.
			(this_or_next|eq, ":troop_1", "trp_kingdom_3_lord"),
			    (eq, ":troop_1", "trp_kingdom_3_pretender"),
			(this_or_next|eq, ":troop_2", "trp_kingdom_3_lord"),
				(eq, ":troop_2", "trp_kingdom_3_pretender"),
			(assign, ":relation_strength", 10),
			(str_store_string, s11, "str_dplmc_half_brother"),
			#Adjust their parentage to make this work automatically
			(try_begin),
		      	(troop_slot_eq, ":troop_1", slot_troop_father, -1),
				(troop_slot_eq, ":troop_2", slot_troop_father, -1),
				#Set their "father" slot to a number guaranteed not to have spurious collisions
				(store_mul, ":janakir_khan", "trp_kingdom_3_lord", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),#defined in module_constants.py
				(val_add, ":janakir_khan", DPLMC_VIRTUAL_RELATIVE_FATHER_OFFSET),#defined in module_constants.py
				(troop_set_slot, ":troop_1", slot_troop_father, ":janakir_khan"),
				(troop_set_slot, ":troop_2", slot_troop_father, ":janakir_khan"),
				#Differentiate their mothers, so they are half-brothers instead of full-brothers
				(try_begin),
					(troop_slot_eq, ":troop_1", slot_troop_mother, -1),
					(store_mul, reg0, ":troop_1", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),
					(val_add, reg0, DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),
					(troop_set_slot, ":troop_1", slot_troop_mother, reg0),
				(try_end),
				(try_begin),
					(troop_slot_eq, ":troop_2", slot_troop_mother, -1),
					(store_mul, reg0, ":troop_2", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),
					(val_add, reg0, DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),
					(troop_set_slot, ":troop_2", slot_troop_mother, reg0),
				(try_end),
			(try_end),
		(try_end),
	(try_end),
	##Add uncles and aunts by marriage.
	##In Native, the relation strength for blood uncles/aunts is 4, and for cousins is 2.
	##In light of this I've decided to set the relation strength for aunts/uncles by marriage to 2.
	(try_begin),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_1 is married to a sibling of one of troop_2's parents, pt. 1
		(ge, ":spouse_of_1", 0),
		(neg|troop_slot_eq, ":spouse_of_1", slot_troop_father, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_1", slot_troop_father, ":paternal_grandfather_of_2"),
			(troop_slot_eq, ":spouse_of_1", slot_troop_father, ":maternal_grandfather_of_2"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(str_store_string, s11, "str_aunt"),
		(else_try),
			(str_store_string, s11, "str_uncle"),
		(try_end),
	(else_try),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_1 is married to a sibling of one of troop_2's parents, pt. 2
		(ge, ":spouse_of_1", 0),
		(neg|troop_slot_eq, ":spouse_of_1", slot_troop_mother, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_1", slot_troop_mother, ":paternal_grandmother_of_2"),
			(troop_slot_eq, ":spouse_of_1", slot_troop_mother, ":maternal_grandmother_of_2"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(str_store_string, s11, "str_aunt"),
		(else_try),
			(str_store_string, s11, "str_uncle"),
		(try_end),
	(else_try),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_2 is married to a sibling of one of troop_1's parents, pt. 1
		(ge, ":spouse_of_2", 0),
		(neg|troop_slot_eq, ":spouse_of_2", slot_troop_father, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_2", slot_troop_father, ":paternal_grandfather_of_1"),
			(troop_slot_eq, ":spouse_of_2", slot_troop_father, ":maternal_grandfather_of_1"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(str_store_string, s11, "str_niece"),
		(else_try),
			(str_store_string, s11, "str_nephew"),
		(try_end),
	(else_try),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_2 is married to a sibling of one of troop_1's parents, pt. 2
		(ge, ":spouse_of_2", 0),
		(neg|troop_slot_eq, ":spouse_of_2", slot_troop_mother, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_2", slot_troop_mother, ":paternal_grandmother_of_1"),
			(troop_slot_eq, ":spouse_of_2", slot_troop_mother, ":maternal_grandmother_of_1"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(str_store_string, s11, "str_niece"),
		(else_try),
			(str_store_string, s11, "str_nephew"),
		(try_end),
	(try_end),
	##diplomacy end+
    (assign, reg4, ":gender_1"),
	(assign, reg0, ":relation_strength"),
	]),


  # script_complete_family_relations
  # INPUT: arg1 = party_id, arg2 = xp_amount
  ("upgrade_hero_party",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":xp_amount", 2),
      ##diplomacy start+
      #Take into account faction quality/quantity settings.  Do not apply this
      #to the player party or to special parties.
      (try_begin),
        (ge, ":party_no", spawn_points_begin),
        (store_faction_of_party, ":var1", ":party_no"),
        (faction_get_slot, ":var1", ":var1", dplmc_slot_faction_quality),
        (val_add, ":var1", 100),
        (val_clamp, ":var1", 97, 104),#100 plus or minus three percent
        (val_mul, ":xp_amount", ":var1"),
        (val_div, ":xp_amount", 100),
      (try_end),
       ##diplomacy end+
      (party_upgrade_with_xp, ":party_no", ":xp_amount", 0),
    ]),

  #script_get_improvement_details
  ("initialize_npcs",
    [

# set strings

        (troop_set_slot, "trp_npc1", slot_troop_morality_type, tmt_egalitarian),  #borcha
        (troop_set_slot, "trp_npc1", slot_troop_morality_value, 4),  #borcha
        (troop_set_slot, "trp_npc1", slot_troop_2ary_morality_type, tmt_aristocratic),  #borcha
        (troop_set_slot, "trp_npc1", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc1", slot_troop_personalityclash_object, "trp_npc7"),  #borcha - deshavi
        (troop_set_slot, "trp_npc1", slot_troop_personalityclash2_object, "trp_npc16"),  #borcha - klethi
        (troop_set_slot, "trp_npc1", slot_troop_personalitymatch_object, "trp_npc2"),  #borcha - marnid
        (troop_set_slot, "trp_npc1", slot_troop_home, "p_village_25"), #Dashbiga
        (troop_set_slot, "trp_npc1", slot_troop_payment_request, 300),
		(troop_set_slot, "trp_npc1", slot_troop_kingsupport_argument, argument_ruler),
		(troop_set_slot, "trp_npc1", slot_troop_kingsupport_opponent, "trp_npc14"), #lezalit
		(troop_set_slot, "trp_npc1", slot_troop_town_with_contacts, "p_town_17"),
		(troop_set_slot, "trp_npc1", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc1", slot_lord_reputation_type, lrep_roguish), #



        (troop_set_slot, "trp_npc2", slot_troop_morality_type, tmt_humanitarian), #marnid
        (troop_set_slot, "trp_npc2", slot_troop_morality_value, 2),
        (troop_set_slot, "trp_npc2", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc2", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc2", slot_troop_personalityclash_object, "trp_npc5"), #marnid - beheshtur
        (troop_set_slot, "trp_npc2", slot_troop_personalityclash2_object, "trp_npc9"), #marnid - alayen
        (troop_set_slot, "trp_npc2", slot_troop_personalitymatch_object, "trp_npc1"),  #marnid - borcha
        (troop_set_slot, "trp_npc2", slot_troop_home, "p_town_1"), #Sargoth
        (troop_set_slot, "trp_npc2", slot_troop_payment_request, 0),
		(troop_set_slot, "trp_npc2", slot_troop_kingsupport_argument, argument_victory),
		(troop_set_slot, "trp_npc2", slot_troop_kingsupport_opponent, "trp_npc16"), #klethi
		(troop_set_slot, "trp_npc2", slot_troop_town_with_contacts, "p_town_1"), #Sargoth
		(troop_set_slot, "trp_npc2", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc2", slot_lord_reputation_type, lrep_custodian), #

#
        (troop_set_slot, "trp_npc3", slot_troop_morality_type, tmt_humanitarian), #Ymira
        (troop_set_slot, "trp_npc3", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc3", slot_troop_2ary_morality_type, tmt_aristocratic),
        (troop_set_slot, "trp_npc3", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc3", slot_troop_personalityclash_object, "trp_npc14"), #Ymira - artimenner
        (troop_set_slot, "trp_npc3", slot_troop_personalityclash2_object, "trp_npc8"), #Ymira - matheld
        (troop_set_slot, "trp_npc3", slot_troop_personalitymatch_object, "trp_npc9"), #Ymira - alayen
        (troop_set_slot, "trp_npc3", slot_troop_home, "p_town_3"), #Veluca
        (troop_set_slot, "trp_npc3", slot_troop_payment_request, 0),
		(troop_set_slot, "trp_npc3", slot_troop_kingsupport_argument, argument_lords),
		(troop_set_slot, "trp_npc3", slot_troop_kingsupport_opponent, "trp_npc5"), #klethi
		(troop_set_slot, "trp_npc3", slot_troop_town_with_contacts, "p_town_15"), #yalen
		(troop_set_slot, "trp_npc3", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc3", slot_lord_reputation_type, lrep_benefactor), #



        (troop_set_slot, "trp_npc4", slot_troop_morality_type, tmt_aristocratic), #Rolf
        (troop_set_slot, "trp_npc4", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc4", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc4", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc4", slot_troop_personalityclash_object, "trp_npc10"), #Rolf - bunduk
        (troop_set_slot, "trp_npc4", slot_troop_personalityclash2_object, "trp_npc7"), #Rolf - deshavi
        (troop_set_slot, "trp_npc4", slot_troop_personalitymatch_object, "trp_npc5"), #Rolf - beheshtur
        (troop_set_slot, "trp_npc4", slot_troop_home, "p_village_34"), #Ehlerdah
        (troop_set_slot, "trp_npc4", slot_troop_payment_request, 300),
        (troop_set_slot, "trp_npc4", slot_troop_renown, 100), #SB : renown
		(troop_set_slot, "trp_npc4", slot_troop_kingsupport_argument, argument_claim),
		(troop_set_slot, "trp_npc4", slot_troop_kingsupport_opponent, "trp_npc6"), #firentis
		(troop_set_slot, "trp_npc4", slot_troop_town_with_contacts, "p_town_3"), #veluca
		(troop_set_slot, "trp_npc4", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc4", slot_lord_reputation_type, lrep_cunning), #


        (troop_set_slot, "trp_npc5", slot_troop_morality_type, tmt_egalitarian),  #beheshtur
        (troop_set_slot, "trp_npc5", slot_troop_morality_value, 3),  #beheshtur
        (troop_set_slot, "trp_npc5", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc5", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc5", slot_troop_personalityclash_object, "trp_npc2"),  #beheshtur - marnid
        (troop_set_slot, "trp_npc5", slot_troop_personalityclash2_object, "trp_npc11"),  #beheshtur- katrin
        (troop_set_slot, "trp_npc5", slot_troop_personalitymatch_object, "trp_npc4"),  #beheshtur - rolf
        (troop_set_slot, "trp_npc5", slot_troop_home, "p_town_14"), #Halmar
        (troop_set_slot, "trp_npc5", slot_troop_payment_request, 400),
        (troop_set_slot, "trp_npc5", slot_troop_renown, 100), #SB : renown
		(troop_set_slot, "trp_npc5", slot_troop_kingsupport_argument, argument_ruler),
		(troop_set_slot, "trp_npc5", slot_troop_kingsupport_opponent, "trp_npc9"), #firentis
		(troop_set_slot, "trp_npc5", slot_troop_town_with_contacts, "p_town_10"), #tulga
		(troop_set_slot, "trp_npc5", slot_troop_original_faction, "fac_kingdom_3"), #khergit
		(troop_set_slot, "trp_npc5", slot_lord_reputation_type, lrep_cunning), #



        (troop_set_slot, "trp_npc6", slot_troop_morality_type, tmt_humanitarian), #firenz
        (troop_set_slot, "trp_npc6", slot_troop_morality_value, 2),  #beheshtur
        (troop_set_slot, "trp_npc6", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc6", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc6", slot_troop_personalityclash_object, "trp_npc11"), #firenz
        (troop_set_slot, "trp_npc6", slot_troop_personalityclash2_object, "trp_npc13"), #firenz - nizar
        (troop_set_slot, "trp_npc6", slot_troop_personalitymatch_object, "trp_npc12"),  #firenz - jeremus
        (troop_set_slot, "trp_npc6", slot_troop_home, "p_town_4"), #Suno
        (troop_set_slot, "trp_npc6", slot_troop_payment_request, 0),
        (troop_set_slot, "trp_npc6", slot_troop_renown, 50), #SB : renown
		(troop_set_slot, "trp_npc6", slot_troop_kingsupport_argument, argument_victory),
		(troop_set_slot, "trp_npc6", slot_troop_kingsupport_opponent, "trp_npc8"), #firentis
		(troop_set_slot, "trp_npc6", slot_troop_town_with_contacts, "p_town_7"), #uxkhal
		(troop_set_slot, "trp_npc6", slot_troop_original_faction, "fac_kingdom_1"), #swadia
		(troop_set_slot, "trp_npc6", slot_lord_reputation_type, lrep_upstanding), #



        (troop_set_slot, "trp_npc7", slot_troop_morality_type, tmt_egalitarian),  #deshavi
        (troop_set_slot, "trp_npc7", slot_troop_morality_value, 3),  #beheshtur
        (troop_set_slot, "trp_npc7", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc7", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc7", slot_troop_personalityclash_object, "trp_npc1"),  #deshavi
        (troop_set_slot, "trp_npc7", slot_troop_personalityclash2_object, "trp_npc4"),  #deshavi - rolf
        (troop_set_slot, "trp_npc7", slot_troop_personalitymatch_object, "trp_npc16"),  #deshavi - klethi
        (troop_set_slot, "trp_npc7", slot_troop_home, "p_village_5"), #Kulum
#        (troop_set_slot, "trp_npc7", slot_troop_payment_request, 300),
		(troop_set_slot, "trp_npc7", slot_troop_kingsupport_argument, argument_victory),
		(troop_set_slot, "trp_npc7", slot_troop_kingsupport_opponent, "trp_npc3"), #ymira
		(troop_set_slot, "trp_npc7", slot_troop_town_with_contacts, "p_town_2"), #tihr
		(troop_set_slot, "trp_npc7", slot_troop_original_faction, 0), #swadia
		(troop_set_slot, "trp_npc7", slot_lord_reputation_type, lrep_custodian), #



        (troop_set_slot, "trp_npc8", slot_troop_morality_type, tmt_aristocratic), #matheld
        (troop_set_slot, "trp_npc8", slot_troop_morality_value, 3),  #beheshtur
        (troop_set_slot, "trp_npc8", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc8", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc8", slot_troop_personalityclash_object, "trp_npc12"), #matheld
        (troop_set_slot, "trp_npc8", slot_troop_personalityclash2_object, "trp_npc3"), #matheld - ymira
        (troop_set_slot, "trp_npc8", slot_troop_personalitymatch_object, "trp_npc13"),  #matheld - nizar
        (troop_set_slot, "trp_npc8", slot_troop_home, "p_village_35"), #Fearichen
        (troop_set_slot, "trp_npc8", slot_troop_payment_request, 500),
        (troop_set_slot, "trp_npc8", slot_troop_renown, 75), #SB : renown
		(troop_set_slot, "trp_npc8", slot_troop_kingsupport_argument, argument_lords),
		(troop_set_slot, "trp_npc8", slot_troop_kingsupport_opponent, "trp_npc2"), #marnid
		(troop_set_slot, "trp_npc8", slot_troop_town_with_contacts, "p_town_12"), #wercheg
		(troop_set_slot, "trp_npc8", slot_troop_original_faction, "fac_kingdom_4"), #nords
		(troop_set_slot, "trp_npc8", slot_lord_reputation_type, lrep_martial), #


        (troop_set_slot, "trp_npc9", slot_troop_morality_type, tmt_aristocratic), #alayen
        (troop_set_slot, "trp_npc9", slot_troop_morality_value, 2),  #beheshtur
        (troop_set_slot, "trp_npc9", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc9", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc9", slot_troop_personalityclash_object, "trp_npc13"), #alayen vs nizar
        (troop_set_slot, "trp_npc9", slot_troop_personalityclash2_object, "trp_npc2"), #alayen vs marnid
        (troop_set_slot, "trp_npc9", slot_troop_personalitymatch_object, "trp_npc3"),  #alayen - ymira
        (troop_set_slot, "trp_npc9", slot_troop_home, "p_town_13"), #Rivacheg
        (troop_set_slot, "trp_npc9", slot_troop_payment_request, 300),
        (troop_set_slot, "trp_npc9", slot_troop_renown, 100), #SB : renown
		(troop_set_slot, "trp_npc9", slot_troop_kingsupport_argument, argument_lords),
		(troop_set_slot, "trp_npc9", slot_troop_kingsupport_opponent, "trp_npc1"), #borcha
		(troop_set_slot, "trp_npc9", slot_troop_town_with_contacts, "p_town_8"), #reyvadin
		(troop_set_slot, "trp_npc9", slot_troop_original_faction, "fac_kingdom_2"), #vaegirs
		(troop_set_slot, "trp_npc9", slot_lord_reputation_type, lrep_martial), #


        (troop_set_slot, "trp_npc10", slot_troop_morality_type, tmt_humanitarian), #bunduk
        (troop_set_slot, "trp_npc10", slot_troop_morality_value, 2),
        (troop_set_slot, "trp_npc10", slot_troop_2ary_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc10", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc10", slot_troop_personalityclash_object, "trp_npc4"), #bunduk vs rolf
        (troop_set_slot, "trp_npc10", slot_troop_personalityclash2_object, "trp_npc14"), #bunduk vs lazalet
        (troop_set_slot, "trp_npc10", slot_troop_personalitymatch_object, "trp_npc11"),  #bunduk likes katrin
        (troop_set_slot, "trp_npc10", slot_troop_home, "p_castle_28"), #Grunwalder Castle
        (troop_set_slot, "trp_npc10", slot_troop_payment_request, 200),
        (troop_set_slot, "trp_npc10", slot_troop_renown, 75), #SB : renown
		(troop_set_slot, "trp_npc10", slot_troop_kingsupport_argument, argument_ruler),
		(troop_set_slot, "trp_npc10", slot_troop_kingsupport_opponent, "trp_npc7"), #nizar
		(troop_set_slot, "trp_npc10", slot_troop_town_with_contacts, "p_town_5"), #jelkala
		(troop_set_slot, "trp_npc10", slot_troop_original_faction, "fac_kingdom_5"), #rhodoks
		(troop_set_slot, "trp_npc10", slot_lord_reputation_type, lrep_benefactor), #



        (troop_set_slot, "trp_npc11", slot_troop_morality_type, tmt_egalitarian),  #katrin
        (troop_set_slot, "trp_npc11", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc11", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc11", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc11", slot_troop_personalityclash_object, "trp_npc6"),  #katrin vs firenz
        (troop_set_slot, "trp_npc11", slot_troop_personalityclash2_object, "trp_npc5"),  #katrin - beheshtur
        (troop_set_slot, "trp_npc11", slot_troop_personalitymatch_object, "trp_npc10"),  #katrin likes bunduk
        (troop_set_slot, "trp_npc11", slot_troop_home, "p_town_6"), #Praven
        (troop_set_slot, "trp_npc11", slot_troop_payment_request, 100),
		(troop_set_slot, "trp_npc11", slot_troop_kingsupport_argument, argument_claim),
		(troop_set_slot, "trp_npc11", slot_troop_kingsupport_opponent, "trp_npc15"), #borcha
		(troop_set_slot, "trp_npc11", slot_troop_town_with_contacts, "p_town_6"), #praven
		(troop_set_slot, "trp_npc11", slot_troop_original_faction, 0), #
		(troop_set_slot, "trp_npc11", slot_lord_reputation_type, lrep_custodian), #


        (troop_set_slot, "trp_npc12", slot_troop_morality_type, tmt_humanitarian), #jeremus
        (troop_set_slot, "trp_npc12", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc12", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc12", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc12", slot_troop_personalityclash_object, "trp_npc8"), #jerem
        (troop_set_slot, "trp_npc12", slot_troop_personalityclash2_object, "trp_npc15"), #jeremus - artimenner
        (troop_set_slot, "trp_npc12", slot_troop_personalitymatch_object, "trp_npc6"),  #jeremus - firenz
        (troop_set_slot, "trp_npc12", slot_troop_home, "p_castle_16"), #undetermined #University
        (troop_set_slot, "trp_npc12", slot_troop_payment_request, 0),
        (troop_set_slot, "trp_npc12", slot_troop_renown, 100), #SB : renown
		(troop_set_slot, "trp_npc12", slot_troop_kingsupport_argument, argument_claim),
		(troop_set_slot, "trp_npc12", slot_troop_kingsupport_opponent, "trp_npc13"), #nizar
		(troop_set_slot, "trp_npc12", slot_troop_town_with_contacts, "p_town_14"), #halmar
		(troop_set_slot, "trp_npc12", slot_troop_original_faction, 0), #
		(troop_set_slot, "trp_npc12", slot_lord_reputation_type, lrep_benefactor), #



        (troop_set_slot, "trp_npc13", slot_troop_morality_type, tmt_aristocratic), #nizar
        (troop_set_slot, "trp_npc13", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc13", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc13", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc13", slot_troop_personalityclash_object, "trp_npc9"), #nizar
        (troop_set_slot, "trp_npc13", slot_troop_personalityclash2_object, "trp_npc6"), #nizar - firenz
        (troop_set_slot, "trp_npc13", slot_troop_personalitymatch_object, "trp_npc8"), #nizar - matheld
        (troop_set_slot, "trp_npc13", slot_troop_home, "p_castle_15"), #Ergellon Castle
        (troop_set_slot, "trp_npc13", slot_troop_payment_request, 300),
        (troop_set_slot, "trp_npc13", slot_troop_renown, 75), #SB : renown
		(troop_set_slot, "trp_npc13", slot_troop_kingsupport_argument, argument_claim),
		(troop_set_slot, "trp_npc13", slot_troop_kingsupport_opponent, "trp_npc10"), #nizar
		(troop_set_slot, "trp_npc13", slot_troop_town_with_contacts, "p_town_4"), #suno
		(troop_set_slot, "trp_npc13", slot_troop_original_faction, 0), #
		(troop_set_slot, "trp_npc13", slot_lord_reputation_type, lrep_roguish), #



        (troop_set_slot, "trp_npc14", slot_troop_morality_type, tmt_aristocratic), #lezalit
        (troop_set_slot, "trp_npc14", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc14", slot_troop_2ary_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc14", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc14", slot_troop_personalityclash_object, "trp_npc3"), #lezalit
        (troop_set_slot, "trp_npc14", slot_troop_personalityclash2_object, "trp_npc10"), #lezalit - bunduk
        (troop_set_slot, "trp_npc14", slot_troop_personalitymatch_object, "trp_npc15"), #lezalit - artimenner
        (troop_set_slot, "trp_npc14", slot_troop_home, "p_castle_18"), #Ismirala Castle
        (troop_set_slot, "trp_npc14", slot_troop_payment_request, 400),
        (troop_set_slot, "trp_npc14", slot_troop_renown, 100), #SB : renown
		(troop_set_slot, "trp_npc14", slot_troop_kingsupport_argument, argument_victory),
		(troop_set_slot, "trp_npc14", slot_troop_kingsupport_opponent, "trp_npc11"), #nizar
		(troop_set_slot, "trp_npc14", slot_troop_town_with_contacts, "p_town_16"), #dhirim
		(troop_set_slot, "trp_npc14", slot_troop_original_faction, 0), #
		(troop_set_slot, "trp_npc14", slot_lord_reputation_type, lrep_selfrighteous), #


        (troop_set_slot, "trp_npc15", slot_troop_morality_type, tmt_egalitarian),  #artimenner
        (troop_set_slot, "trp_npc15", slot_troop_morality_value, 2),
        (troop_set_slot, "trp_npc15", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc15", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc15", slot_troop_personalityclash_object, "trp_npc16"), #artimenner - klethi
        (troop_set_slot, "trp_npc15", slot_troop_personalityclash2_object, "trp_npc12"), #artimenner - jeremus
        (troop_set_slot, "trp_npc15", slot_troop_personalitymatch_object, "trp_npc14"), #lazalit - artimenner
        (troop_set_slot, "trp_npc15", slot_troop_home, "p_castle_1"), #Culmarr Castle
        (troop_set_slot, "trp_npc15", slot_troop_payment_request, 300),
        (troop_set_slot, "trp_npc15", slot_troop_renown, 100), #SB : renown
		(troop_set_slot, "trp_npc15", slot_troop_kingsupport_argument, argument_ruler),
		(troop_set_slot, "trp_npc15", slot_troop_kingsupport_opponent, "trp_npc4"), #nizar
 		(troop_set_slot, "trp_npc15", slot_troop_town_with_contacts, "p_town_20"), #durquba
		(troop_set_slot, "trp_npc15", slot_lord_reputation_type, lrep_custodian), #


        (troop_set_slot, "trp_npc16", slot_troop_morality_type, tmt_aristocratic), #klethi
        (troop_set_slot, "trp_npc16", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc16", slot_troop_2ary_morality_type, tmt_humanitarian),
        (troop_set_slot, "trp_npc16", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc16", slot_troop_personalityclash_object, "trp_npc15"), #klethi
        (troop_set_slot, "trp_npc16", slot_troop_personalityclash2_object, "trp_npc1"), #klethi - borcha
        (troop_set_slot, "trp_npc16", slot_troop_personalitymatch_object, "trp_npc7"),  #deshavi - klethi
        (troop_set_slot, "trp_npc16", slot_troop_home, "p_village_20"), #Uslum
        (troop_set_slot, "trp_npc16", slot_troop_payment_request, 200),
        (troop_set_slot, "trp_npc16", slot_troop_kingsupport_argument, argument_lords),
        (troop_set_slot, "trp_npc16", slot_troop_kingsupport_opponent, "trp_npc12"), #nizar
        (troop_set_slot, "trp_npc16", slot_troop_town_with_contacts, "p_town_9"), #khudan
        (troop_set_slot, "trp_npc16", slot_lord_reputation_type, lrep_roguish), #



        (store_sub, "$number_of_npc_slots", slot_troop_strings_end, slot_troop_intro),

        (try_for_range, ":npc", companions_begin, companions_end),


            (try_for_range, ":slot_addition", 0, "$number_of_npc_slots"),
                (store_add, ":slot", ":slot_addition", slot_troop_intro),

                (store_mul, ":string_addition", ":slot_addition", 16),
                (store_add, ":string", "str_npc1_intro", ":string_addition"),
                (val_add, ":string", ":npc"),
                (val_sub, ":string", companions_begin),

                (troop_set_slot, ":npc", ":slot", ":string"),
            (try_end),
        (try_end),


#Post 0907 changes begin
        (call_script, "script_add_log_entry", logent_game_start, "trp_player", -1, -1, -1),
#Post 0907 changes end

    #Rebellion changes begin
        (troop_set_slot, "trp_kingdom_1_pretender",  slot_troop_original_faction, "fac_kingdom_1"),
        (troop_set_slot, "trp_kingdom_2_pretender",  slot_troop_original_faction, "fac_kingdom_2"),
        (troop_set_slot, "trp_kingdom_3_pretender",  slot_troop_original_faction, "fac_kingdom_3"),
        (troop_set_slot, "trp_kingdom_4_pretender",  slot_troop_original_faction, "fac_kingdom_4"),
        (troop_set_slot, "trp_kingdom_5_pretender",  slot_troop_original_faction, "fac_kingdom_5"),
        (troop_set_slot, "trp_kingdom_6_pretender",  slot_troop_original_faction, "fac_kingdom_6"),

    #        (troop_set_slot, "trp_kingdom_1_pretender", slot_troop_support_base,     "p_town_4"), #suno
    #        (troop_set_slot, "trp_kingdom_2_pretender", slot_troop_support_base,     "p_town_11"), #curaw
    #        (troop_set_slot, "trp_kingdom_3_pretender", slot_troop_support_base,     "p_town_18"), #town_18
    #        (troop_set_slot, "trp_kingdom_4_pretender", slot_troop_support_base,     "p_town_12"), #wercheg
    #        (troop_set_slot, "trp_kingdom_5_pretender", slot_troop_support_base,     "p_town_3"), #veluca
        ##diplomacy start+
        (troop_set_slot, "trp_kingdom_1_pretender", slot_troop_home, "p_town_4"),#Lady Isolle - Suno
        (troop_set_slot, "trp_kingdom_2_pretender", slot_troop_home, "p_town_11"),#Prince Valdym - Curaw
        (troop_set_slot, "trp_kingdom_3_pretender", slot_troop_home, "p_town_18"),#Dustum Khan - Narra
        (troop_set_slot, "trp_kingdom_4_pretender", slot_troop_home, "p_town_12"),#Lethwin Far-Seeker - Wercheg
        (troop_set_slot, "trp_kingdom_5_pretender", slot_troop_home, "p_town_3"),#Lord Kastor - Veluca
        (troop_set_slot, "trp_kingdom_6_pretender", slot_troop_home, "p_town_20"),#Arwa the Pearled One - Durquba
        ##diplomacy end+
        (try_for_range, ":pretender", pretenders_begin, pretenders_end),
            (troop_set_slot, ":pretender", slot_lord_reputation_type, lrep_none),
            ##diplomacy start+
            (troop_get_slot, ":home", ":pretender", slot_troop_home),
            (ge, ":home", 1),
            (neg|party_slot_ge, ":home", dplmc_slot_center_original_lord, 1),
            (party_set_slot, ":home", dplmc_slot_center_original_lord, ":pretender"),
            ##diplomacy end+
        (try_end),
#Rebellion changes end
     ]),



    ("npc_morale",
[
        (store_script_param_1, ":npc"),

        (troop_get_slot, ":morality_grievances", ":npc", slot_troop_morality_penalties),
        (troop_get_slot, ":personality_grievances", ":npc", slot_troop_personalityclash_penalties),
        (party_get_morale, ":party_morale", "p_main_party"),

        (store_sub, ":troop_morale", ":party_morale", ":morality_grievances"),
        (val_sub, ":troop_morale", ":personality_grievances"),
        (val_add, ":troop_morale", 50), #SB : this should scale from actual relation

        (assign, reg8, ":troop_morale"),

        (val_mul, ":troop_morale", 3),
        (val_div, ":troop_morale", 4),
        (val_clamp, ":troop_morale", 0, 100),

        (assign, reg5, ":party_morale"),
        (assign, reg6, ":morality_grievances"),
        (assign, reg7, ":personality_grievances"),
        (assign, reg9, ":troop_morale"),

#        (str_store_troop_name, s11, ":npc"),
#        (display_message, "@{!}{s11}'s morale = PM{reg5} + 50 - MG{reg6} - PG{reg7} = {reg8} x 0.75 = {reg9}"),

        (try_begin),
            (lt, ":morality_grievances", 3),
            (str_store_string, 7, "str_happy"),
        (else_try),
            (lt, ":morality_grievances", 15),
            (str_store_string, 7, "str_content"),
        (else_try),
            (lt, ":morality_grievances", 30),
            (str_store_string, 7, "str_concerned"),
        (else_try),
            (lt, ":morality_grievances", 45),
            (str_store_string, 7, "str_not_happy"),
        (else_try),
            (str_store_string, 7, "str_miserable"),
        (try_end),


        (try_begin),
            (lt, ":personality_grievances", 3),
            (str_store_string, 6, "str_happy"),
        (else_try),
            (lt, ":personality_grievances", 15),
            (str_store_string, 6, "str_content"),
        (else_try),
            (lt, ":personality_grievances", 30),
            (str_store_string, 6, "str_concerned"),
        (else_try),
            (lt, ":personality_grievances", 45),
            (str_store_string, 6, "str_not_happy"),
        (else_try),
            (str_store_string, 6, "str_miserable"),
        (try_end),


        (try_begin),
            (gt, ":troop_morale", 80),
            (str_store_string, 8, "str_happy"),
            (str_store_string, 63, "str_bar_enthusiastic"),
        (else_try),
            (gt, ":troop_morale", 60),
            (str_store_string, 8, "str_content"),
            (str_store_string, 63, "str_bar_content"),
        (else_try),
            (gt, ":troop_morale", 40),
            (str_store_string, 8, "str_concerned"),
            (str_store_string, 63, "str_bar_weary"),
        (else_try),
            (gt, ":troop_morale", 20),
            (str_store_string, 8, "str_not_happy"),
            (str_store_string, 63, "str_bar_disgruntled"),
        (else_try),
            (str_store_string, 8, "str_miserable"),
            (str_store_string, 63, "str_bar_miserable"),
        (try_end),


        (str_store_string, 21, "str_npc_morale_report"),
        (assign, reg0, ":troop_morale"),

     ]),
#NPC morale both returns a string and reg0 as the morale value


#
  ("retire_companion",
[
    (store_script_param_1, ":npc"),
    (store_script_param_2, ":length"),

    (remove_member_from_party, ":npc", "p_main_party"),
    (troop_set_slot, ":npc", slot_troop_personalityclash_penalties, 0),
    (troop_set_slot, ":npc", slot_troop_morality_penalties, 0),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (store_add, ":return_renown", ":renown", ":length"),
    (troop_set_slot, ":npc", slot_troop_occupation, slto_retirement),
    (troop_set_slot, ":npc", slot_troop_return_renown, ":return_renown"),
    ]),

#NPC companion changes end

  #script_reduce_companion_morale_for_clash
  # INPUT: arg1 = troop_no for companion1 arg2 = troop_no for companion2 arg3 = slot_for_clash_state
  # slot_for_clash_state means: 1=give full penalty to companion1; 2=give full penalty to companion2; 3=give penalty equally
  ("reduce_companion_morale_for_clash",
   [
    (store_script_param, ":companion_1", 1),
    (store_script_param, ":companion_2", 2),
    (store_script_param, ":slot_for_clash_state", 3),

    (troop_get_slot, ":clash_state", ":companion_1", ":slot_for_clash_state"),
    (troop_get_slot, ":grievance_1", ":companion_1", slot_troop_personalityclash_penalties),
    (troop_get_slot, ":grievance_2", ":companion_2", slot_troop_personalityclash_penalties),
    (try_begin),
      (eq, ":clash_state", pclash_penalty_to_self),
      (val_add, ":grievance_1", 5),
    (else_try),
      (eq, ":clash_state", pclash_penalty_to_other),
      (val_add, ":grievance_2", 5),
    (else_try),
      (eq, ":clash_state", pclash_penalty_to_both),
      (val_add, ":grievance_1", 3),
      (val_add, ":grievance_2", 3),
    (try_end),
    (troop_set_slot, ":companion_1", slot_troop_personalityclash_penalties, ":grievance_1"),
    (troop_set_slot, ":companion_2", slot_troop_personalityclash_penalties, ":grievance_2"),
    ]),

#Hunting scripts end
  # Input: arg1 = troop_no
  # Output: none
  ("event_hero_taken_prisoner_by_player",
    [
      (store_script_param_1, ":troop_no"),
      (try_begin),
        (check_quest_active, "qst_persuade_lords_to_make_peace"),
        (try_begin),
          (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":troop_no"),
          (val_mul, ":troop_no", -1),
          (quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":troop_no"),
          (val_mul, ":troop_no", -1),
        (else_try),
          (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":troop_no"),
          (val_mul, ":troop_no", -1),
          (quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":troop_no"),
          (val_mul, ":troop_no", -1),
        (try_end),
        (neg|check_quest_concluded, "qst_persuade_lords_to_make_peace"),
        (neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, 0),
        (neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, 0),
        (call_script, "script_succeed_quest", "qst_persuade_lords_to_make_peace"),
      (try_end),
      (call_script, "script_update_troop_location_notes", ":troop_no", 0),
  ]),

  # script_cf_check_hero_can_escape_from_player
  # Input: arg1 = troop_no
  # Output: none (can fail)
  ("cf_check_hero_can_escape_from_player",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":quest_target", 0),
      (try_begin),
        (check_quest_active, "qst_persuade_lords_to_make_peace"),
        (this_or_next|quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":troop_no"),
        (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":troop_no"),
        (assign, ":quest_target", 1),
      (else_try),
        (ge, ":troop_no", "trp_sea_raider_leader"),
        (lt, ":troop_no", "trp_bandit_leaders_end"),
        (try_begin),
          (check_quest_active, "qst_learn_where_merchant_brother_is"),
          (assign, ":quest_target", 1), #always catched
        (else_try),
          (assign, ":quest_target", -1), #always run.
        (try_end),
      (try_end),

      (assign, ":continue", 0),
      (try_begin),
        (eq, ":quest_target", 0), #if not quest target
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", hero_escape_after_defeat_chance),
        (assign, ":continue", 1),
      (else_try),
        (eq, ":quest_target", -1), #if (always run) quest target
        (assign, ":continue", 1),
      (try_end),

      (eq, ":continue", 1),
  ]),

  # script_cf_party_remove_random_regular_troop
  # Input: arg1 = party_no, arg2 = escape_chance_mul_1000
  # Output: none
  ("randomly_make_prisoner_heroes_escape_from_party",
    [(store_script_param, ":party_no", 1),
     (store_script_param, ":escape_chance", 2),
     (assign, ":quest_troop_1", -1),
     (assign, ":quest_troop_2", -1),
     (try_begin),
       (check_quest_active, "qst_rescue_lord_by_replace"),
       (quest_get_slot, ":quest_troop_1", "qst_rescue_lord_by_replace", slot_quest_target_troop),
     (try_end),
     (try_begin),
       (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
       (quest_get_slot, ":quest_troop_2", "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop),
     (try_end),
     (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
     (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
       (party_prisoner_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (neq, ":stack_troop", ":quest_troop_1"),
       (neq, ":stack_troop", ":quest_troop_2"),
       (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
       (store_random_in_range, ":random_no", 0, 1000),
       (lt, ":random_no", ":escape_chance"),
       (party_remove_prisoners, ":party_no", ":stack_troop", 1),
       (call_script, "script_remove_troop_from_prison", ":stack_troop"),
       (str_store_troop_name_link, s1, ":stack_troop"),
       (try_begin),
         (eq, ":party_no", "p_main_party"),
         (str_store_string, s2, "@your party"),
       (else_try),
         (str_store_party_name, s2, ":party_no"),
       (try_end),
       (assign, reg0, 0),
       (try_begin),
         (this_or_next|eq, ":party_no", "p_main_party"),
         (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
         (assign, reg0, 1),
       (try_end),
       (store_troop_faction, ":troop_faction", ":stack_troop"),
       (str_store_faction_name_link, s3, ":troop_faction"),
       (faction_get_color, ":color", ":troop_faction"),
       #SB : factionalize color, set to log
       (display_log_message, "@{reg0?One of your prisoners, :}{s1} of {s3} has escaped from captivity!", ":color"),
     (try_end),
     ]),


  # script_fill_tournament_participants_troop
("lord_comment_to_s43",
    [(store_script_param, ":lord", 1),
     (store_script_param, ":default_string", 2),

    (troop_get_slot,":reputation", ":lord", slot_lord_reputation_type),

		#some default strings will have added comments for the added commons reputation types
		##diplomacy start+
		(try_begin),
		#Don't reassign personalities of lords
			(is_between, ":reputation", lrep_none, lrep_upstanding + 1),
       		(else_try),
		#Special case for anti-humanitarians (Klethi in Native)
		    (neg|is_between, ":reputation", lrep_none, lrep_upstanding + 1),
	            (neq, ":reputation", lrep_benefactor),
	            (neq, ":reputation", lrep_moralist),
	            (neq, ":reputation", lrep_conventional),
		    (call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
	      	    (lt, reg0, 0),#<- In Native, this only applies to Klethi
		    #Use lrep_debauched by default, and refine further below.
		    (assign, ":reputation", lrep_debauched),
		    (try_begin),
			#If pious, anti-humanitarians use lrep_selfrighteous
		    	(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_pious),
			(ge, reg0, 1),#<- Describes no one in Native
			(assign, ":reputation", lrep_selfrighteous),
		    (else_try),
			#If aggressive, anti-humanitarians use lrep_quarrelsome
		    	(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_aristocratic),
			(this_or_next|eq, ":reputation", lrep_adventurous),
				(ge, reg0, 1),#<- In Native describes Alayen, Matheld, Rolf, Nizar, Lezalit, Klethi (but only Klethi can even reach here)
			(assign, ":reputation", lrep_quarrelsome),
		    (try_end),
		(else_try),
		#Special case for "pious" characters (no one in Native)
			(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_pious),
			(ge, reg0, 1),
			(try_begin),
				#Handle these separately to prevent inappropriate reassignment
				(this_or_next|eq, ":reputation", lrep_benefactor),
					(eq, ":reputation", lrep_moralist),
				(assign, ":reputation", lrep_upstanding),
			(else_try),
				#Ordinarily upstanding
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
				(ge, reg0, 0),#<- In Native describes all but Klethi
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
				(ge, reg0, 0),#<- In Native describes all but Lezalit
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
				(ge, reg0, 0),#<- In Native describes all but Rolf
				(assign, ":reputation", lrep_upstanding),
		    	(else_try),
				#If vicious, self-righteous is also a possibility
			        (assign, ":reputation", lrep_selfrighteous),
		     	(try_end),
		(else_try),
		#Special case for dishonest commoners.
		#Pragmatic-style amoral: lrep_cunning
		#Jerk-style amoral: lrep_debauched
	 	 	(neg|is_between, ":reputation", lrep_none, lrep_upstanding + 1),
	            	(neq, ":reputation", lrep_moralist),
	            	(neq, ":reputation", lrep_benefactor),
			(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
			(lt, reg0, 0),#<- In Native only describes Rolf (who wouldn't reach here, since he is lrep_cunning)
			(try_begin),
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
				(lt, reg0, 1),
				(assign, ":egalitarian", reg0),
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
				(lt, reg0, 1),
				(this_or_next|lt, reg0, 0),
					(lt, ":egalitarian", 0),
				(assign, ":reputation", lrep_debauched),
			(else_try),
				(assign, ":reputation", lrep_cunning),
			(try_end),
		(else_try),
			(eq, ":reputation", lrep_roguish),
			(assign, ":reputation", lrep_goodnatured),
		(else_try),
			(eq, ":reputation", lrep_custodian),
			(assign, ":reputation", lrep_cunning),
		(else_try),
			(eq, ":reputation", lrep_benefactor),
			(assign, ":reputation", lrep_goodnatured),
        #add support for lady personalities
        (else_try),
            (eq, ":reputation", lrep_ambitious),
            (assign, ":reputation", lrep_cunning),
	(else_try),
	    (this_or_next|eq, ":reputation", lrep_conventional),
	    	(eq, ":reputation", lrep_otherworldly),
	    (assign, ":reputation", lrep_goodnatured),
	(else_try),
	    (eq, ":reputation", lrep_adventurous),
   	    (assign, ":reputation", lrep_martial),
  	    (call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
	    (try_begin),
		    (lt, reg0, 0),#<- In Native describes no one
		    (assign, ":reputation", lrep_quarrelsome),
	    (try_end),
	(else_try),
	    (eq, ":reputation", lrep_moralist),
	    (assign, ":reputation", lrep_upstanding),
	(try_end),
	##diplomacy end+

	##diplomacy start+ Add some variability
	#For non-companion, non-monarchs who don't have any tmt_* morality values, this
	# just amounts to a 5% chance to use lrep_none instead of their real reputation
	# (except where that would cause problems).
	#Otherwise,
	# 16,17:
	#   tmt_pious > 0, with lrep_debauched or lrep_quarrelsome or lrep_selfrighteous: lrep_selfrighteous
	#   tmt_pious > 0, with one of (tmt_egalitarian, tmt_honest, tmt_humanitarian) < 0 and none > 0: lrep_selfrighteous
	#   (tmt_pious >= 0 and tmt_honest >= 0) and (tmt_pious > 0 or tmt_honest > 0): lrep_upstanding
	#   tmt_honest < 0: lrep_cunning
	#   lrep_none and is a king or pretender: lrep_cunning
	#
	# 18,19:
	#   tmt_aristocratic > 0, with lrep_debauched or lrep_quarrelsome: lrep_quarrelsome
	#   lrep_martial, with (tmt_honest, tmt_egalitarian, tmt_humanitarian) all non-positive and
	#      at least one negative, and tmt_pious < 1 (so not to overlap with 16,17): lrep_quarrelsome
	#   tmt_aristocratic > 0: lrep_martial
	#   lrep_none and is a king or pretender: lrep_martial
	(store_random_in_range, ":random_chance", 0, 20),
	(assign, ":new_reputation", ":reputation"),
	(try_begin),
		(eq, 1, 1),#Disable this feature for now.
	(else_try),
		#Disable the first time you're talking to someone, or if you haven't
		#spoken to this NPC recently.
		(store_current_hours, ":recently"),
		(val_sub, ":recently", 24),
		(this_or_next|neq, "$g_talk_troop_met", 1),
		(this_or_next|neg|troop_slot_ge, ":lord", slot_troop_met, 1),
		(this_or_next|neg|troop_slot_ge, ":lord", slot_troop_last_talk_time, ":recently"),
		#Disable for things that come in sequences
		(this_or_next|eq, ":default_string", "str_rebellion_dilemma_default"),
			(eq, ":default_string", "str_rebellion_dilemma_2_default"),
		#Set this value to signal to the debug message at the end
		(assign, ":random_chance", -1),
	(else_try),
		#10% chance of lrep_martial or lrep_quarrelsome if appropriate...
		#if already lrep_martial, check separately here for possible conversion
		#to lrep_quarrelsome
		(is_between, ":random_chance", 18, 20),
		(eq, ":reputation", lrep_martial),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
		(lt, reg0, 1),
		(assign, ":bad_sum", reg0),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
		(lt, reg0, 1),
		(val_add, ":bad_sum", reg0),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
		(lt, reg0, 1),
		(val_add, ":bad_sum", reg0),
		#at least one of tmt_egalitarian, tmt_humanitarian, and tmt_honest were negative (and none were positive)
		(lt, ":bad_sum", 0),
		#disable for positive tmt_pious, since that's handled separately as an alternative to lrep_upstanding for [16,17]
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
		(lt, reg0, 1),
		(assign, ":new_reputation", lrep_quarrelsome),
     	(else_try),
		#10% chance of lrep_martial or lrep_quarrelsome if appropriate
		#Applies to: Rolf, Nizar, Lezalit, Klethi
		#(Also Alayen and Matheld, but they are already lrep_martial)
		(is_between, ":random_chance", 18, 20),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_aristocratic),
		(ge, reg0, 1),
		(try_begin),
			#some personalities use lrep_quarrelsome (only Klethi in Native)
			(this_or_next|eq, ":reputation", lrep_debauched),
				(eq, ":reputation", lrep_quarrelsome),#<-- i.e. no change
			(assign, ":new_reputation", lrep_quarrelsome),
		(else_try),
			#other personalities use lrep_martial
	      		(assign, ":new_reputation", lrep_martial),
		(try_end),
	(else_try),
		#10% chance of lrep_upstanding or lrep_selfrighteous if appropriate
		#Applies to: Marnid, Alayen, Artimenner
		#(Also Firentis, but he is already lrep_upstanding)
		(is_between, ":random_chance", 16, 18),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
		(assign, ":honest", reg0),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_pious),
		(assign, ":pious", reg0),
		(this_or_next|ge, ":honest", 1),#one or the other must be greater than zero
			(ge, ":pious", 1),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
		(assign, ":egalitarian", reg0),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
		(assign, ":humanitarian", reg0),
		(try_begin),
			#Unpleasant personalities use "selfrighteous" instead
			#(Applies to no one in Native)
			(this_or_next|eq, ":reputation", lrep_debauched),
			(this_or_next|eq, ":reputation", lrep_quarrelsome),
			(this_or_next|eq, ":reputation", lrep_selfrighteous),#<- i.e. no change
			(this_or_next|lt, ":honest", 0),
			(this_or_next|lt, ":egalitarian", 0),
				(lt, ":humanitarian", 0),
			(assign, ":new_reputation", lrep_selfrighteous),
		(else_try),
		   	#Other personalities use upstanding
			(assign, ":new_reputation", lrep_upstanding),
		(try_end),
	(else_try),
		#10% chance of lrep_cunning if appropriate
		(is_between, ":random_chance", 16, 18),
		(lt, ":honest", 0),#<- In Native only Rolf satisfies this, but he is already lrep_cunning
		(assign, ":reputation", lrep_cunning),
	(else_try),
		#Ruler, if personality triggers not met: 10% cunning, 10% martial
		(is_between, ":random_chance", 16, 20),
		(eq, ":reputation", lrep_none),
		(this_or_next|is_between, ":lord", kings_begin, kings_end),
			(is_between, ":lord", pretenders_begin, pretenders_end),
		(try_begin),
			(is_between, ":random_chance", 16, 18),
			(assign, ":new_reputation", lrep_cunning),
		(else_try),
			(is_between, ":random_chance", 18, 20),
			(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_aristocratic),
			(ge, reg0, 0),#Won't reach here if positive, so you could just check if it equals zero
			(assign, ":new_reputation", lrep_martial),
		(try_end),
	(else_try),
		#Others, if personality triggers not met: 5% chance of null
		(is_between, ":random_chance", 16, 20),#base 20%
		(store_mod, ":rand_mod", ":random_chance",4),
		(troop_get_slot, reg0, ":lord", slot_troop_temp_decision_seed),
		(val_mod, reg0, 4),
		(eq, ":rand_mod", reg0),#1/4 of the time, 5%
		#disable for things that don't have a "lrep_none" version defined
		(neq, ":default_string", "str_rebellion_dilemma_default"),
		(neq, ":default_string", "str_rebellion_dilemma_2_default"),
		(neq, ":default_string", "str_changed_my_mind_default"),
		(neq, ":default_string", "str_political_philosophy_default"),
		(neq, ":default_string", "str_rebellion_rival_default"),
		(neq, ":default_string", "str_rebellion_agree_default"),
		(neq, ":default_string", "str_rebellion_refuse_default"),
		(neq, ":default_string", "str_talk_later_default"),
		(neq, ":default_string", "str_npc_claim_throne_liege"),
		#use lrep_none
		(assign, ":new_reputation", lrep_none),
	(try_end),
	(try_begin),
		(eq, 1, 0),#Disable this feature for now.
		(ge, "$cheat_mode", 1),
		(assign, ":save_reg1", reg1),
		(assign, ":save_reg2", reg2),
		(assign, reg0, ":random_chance"),
		(assign, reg1, ":reputation"),
		(assign, reg2, ":new_reputation"),
		(try_begin),
			(neq, ":reputation", ":new_reputation"),
			(display_message, "@{!} DEBUG - random {reg0} (0 to 20), used reputation {reg2} instead of {reg1}"),
		(else_try),
			(lt, ":random_chance", 0),
			(display_message, "@{!} DEBUG - variable responses disabled, kept reputation {reg2}"),
		(else_try),
			(display_message, "@{!} DEBUG - random {reg0} (0 to 20), kept reputation {reg2}"),
		(try_end),
		(assign, reg1, ":save_reg1"),
		(assign, reg2, ":save_reg2"),
	(try_end),
	(assign, ":reputation", ":new_reputation"),
	##diplomacy end+

    (store_add, ":result", ":reputation", ":default_string"),

    (str_store_string, 43, ":result"),
	(assign, reg0, ":result"),


	]),

#Troop Commentaries begin
("add_lady_items",
	[
	(store_script_param, ":lady_no", 1),
	(troop_equip_items, ":lady_no"),

	(store_faction_of_troop, ":faction_no", ":lady_no"),

	(store_random_in_range, ":random", 0, 6),

	(try_begin), #assign clothes
		(this_or_next|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_adventurous),
			(troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_ambitious),

		(this_or_next|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_adventurous),
			(lt, ":random", 2),

		(neg|troop_slot_ge, ":lady_no", slot_troop_age, 40),
		(try_begin),
			(eq, ":faction_no", "fac_kingdom_2"),
			(lt, ":random", 4),
			(troop_add_item, ":lady_no", "itm_fur_coat", 0),
		(else_try),
			(eq, ":faction_no", "fac_kingdom_3"),
			(lt, ":random", 3),
			(troop_add_item, ":lady_no", "itm_nomad_robe", 0),
		(else_try),
			(troop_add_item, ":lady_no", "itm_nomad_vest", 0),
		(try_end),
	(else_try),
		(eq, ":faction_no", "fac_kingdom_1"),
		(try_begin),
			(lt, ":random", 2),
			(troop_add_item, ":lady_no", "itm_lady_dress_ruby", 0),
		(else_try),
			(lt, ":random", 4),
			(troop_add_item, ":lady_no", "itm_lady_dress_green", 0),
		(else_try),
			(troop_add_item, ":lady_no", "itm_lady_dress_blue", 0),
		(try_end),
	(else_try),
		(eq, ":faction_no", "fac_kingdom_2"),
		(try_begin),
			(eq, ":random", 0),
			(troop_add_item, ":lady_no", "itm_blue_dress", 0),
		(else_try),
			(eq, ":random", 1),
			(troop_add_item, ":lady_no", "itm_lady_dress_green", 0),
		(else_try),
			(eq, ":random", 2),
			(troop_add_item, ":lady_no", "itm_lady_dress_blue", 0),
		(else_try),
			(lt, ":random", 5),
			(neg|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_conventional),
			(neg|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_ambitious),
			(troop_add_item, ":lady_no", "itm_peasant_dress", 0),
		(else_try),
			(lt, ":random", 5),
			(troop_add_item, ":lady_no", "itm_lady_dress_ruby", 0),
		(else_try),
			(troop_add_item, ":lady_no", "itm_court_dress", 0),
		(try_end),

	(else_try),
		(eq, ":faction_no", "fac_kingdom_3"),
		(troop_add_item, ":lady_no", "itm_khergit_lady_dress", 0),

	(else_try),
		(eq, ":faction_no", "fac_kingdom_4"),

	(else_try),
		(eq, ":faction_no", "fac_kingdom_5"),


	(try_end),
	(troop_equip_items, ":lady_no"),

	#also available:
	#itm_blue_dress
	#itm_court_dress

	#to add for khergits -- salwar/shalvar?
	#western tang costume (p105, china's golden age)
	#kipchak woman from russia book

	(try_begin), #assign headguear matched to item
		(this_or_next|troop_has_item_equipped, ":lady_no", "itm_nomad_vest"),
		(this_or_next|troop_has_item_equipped, ":lady_no", "itm_fur_coat"),
			(troop_has_item_equipped, ":lady_no", "itm_nomad_robe"),

		#assign no headgear
	(else_try),
		(this_or_next|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_moralist),
		(this_or_next|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_conventional),
			(lt, ":random", 2),


		(try_begin),
			(troop_has_item_equipped, ":lady_no", "itm_khergit_lady_dress"),
			(troop_add_item, ":lady_no", "itm_khergit_lady_hat", 0),

		(else_try),
			(troop_has_item_equipped, ":lady_no", "itm_lady_dress_ruby"),
			(troop_add_item, ":lady_no", "itm_turret_hat_ruby", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving ruby turret hat to {s4}"),
		(else_try),
			(troop_has_item_equipped, ":lady_no", "itm_lady_dress_blue"),
			(troop_add_item, ":lady_no", "itm_turret_hat_blue", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving blue turret hat to {s4}"),
		(else_try),
			(troop_has_item_equipped, ":lady_no", "itm_lady_dress_green"),
			(troop_add_item, ":lady_no", "itm_turret_hat_green", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving green turret hat to {s4}"),
		(else_try),
			(troop_has_item_equipped, ":lady_no", "itm_green_dress"),
			(troop_add_item, ":lady_no", "itm_wimple_with_veil", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving green-lined wimple to {s4}"),
		(else_try),
			(neq, ":faction_no", "fac_kingdom_3"),
			(neq, ":faction_no", "fac_kingdom_6"),
			(troop_add_item, ":lady_no", "itm_wimple_a", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving red-lined wimple to {s4}"),
		(else_try),
			(eq, ":faction_no", "fac_kingdom_6"),
			(try_begin),
				(troop_has_item_equipped, ":lady_no", "itm_sarranid_lady_dress"),
				(troop_add_item, ":lady_no", "itm_sarranid_head_cloth", 0),
			(else_try),
				(troop_add_item, ":lady_no", "itm_sarranid_head_cloth_b", 0),
			(try_end),
		(try_end),
	(try_end),
	(troop_equip_items, ":lady_no"),
	##diplomacy start+
	##Save personal items of kingdom ladies
	(call_script, "script_dplmc_save_civilian_clothing", ":lady_no"),
	##diplomacy end+
	]
	),

	("lady_evaluate_troop_as_suitor",
	[
	(store_script_param, ":lady", 1),
	(store_script_param, ":suitor", 2),

	(call_script, "script_troop_get_romantic_chemistry_with_troop", ":lady", ":suitor"),
	(assign, ":romantic_chemistry", reg0),

	(try_begin),
      (call_script, "script_cf_test_lord_incompatibility_to_s17", ":lady", ":suitor"),
    (try_end),

	(store_sub, ":personality_modifier", 0, reg0),
	(assign, reg2, ":personality_modifier"),

	(try_begin),
		(troop_get_slot, ":renown_modifier", ":suitor", slot_troop_renown),
		(val_div, ":renown_modifier", 20),
		(try_begin),
			(this_or_next|troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_conventional),
				(troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_ambitious),
			(val_mul, ":renown_modifier", 2),
			(val_sub, ":renown_modifier", 15),
		(try_end),
	(try_end),

	(store_add, ":final_score", ":renown_modifier", ":personality_modifier"),
	(val_add, ":final_score", ":romantic_chemistry"),
	(assign, reg0, ":final_score"),
	]),

	("courtship_event_troop_court_lady",
	[
	(store_script_param, ":suitor", 1),
	(store_script_param, ":lady", 2),


	#(try_begin),
	  #(eq, "$cheat_mode", 1),
	  #(str_store_troop_name, s4, ":suitor"),
	  #(str_store_troop_name, s5, ":lady"),
	  #(troop_get_slot, ":lady_location", ":lady", slot_troop_cur_center),
	  #(str_store_party_name, s7, ":lady_location"),
	  #(display_message, "str_s4_pursues_suit_with_s5_in_s7"),
	#(try_end),

	(troop_get_slot, ":previous_suitor", ":lady", slot_lady_last_suitor),
	(troop_set_slot, ":lady", slot_lady_last_suitor, ":suitor"), #can determine quarrels

	(try_begin),
		(eq, ":previous_suitor", "trp_player"),

		(troop_slot_ge, ":lady", slot_troop_met, 2),
		(call_script, "script_troop_get_relation_with_troop", ":suitor", "trp_player"), #add this to list of quarrels
		(assign, ":suitor_relation_w_player", reg0),

		(try_begin),
			(this_or_next|troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_quarrelsome),
				(troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_debauched),
			(gt, ":suitor_relation_w_player", -20),
			(call_script, "script_add_log_entry", logent_lords_quarrel_over_woman, ":suitor", "trp_player", ":lady", 0),
		(else_try),
			(is_between, ":suitor_relation_w_player", -5, -25),
			(call_script, "script_add_log_entry", logent_lords_quarrel_over_woman, ":suitor", "trp_player", ":lady", 0),
		(try_end),
	(else_try),
		(neq, ":previous_suitor", "trp_player"), #not the player

		(neq, ":suitor", ":previous_suitor"),
		(ge, ":previous_suitor", active_npcs_begin),

		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":suitor", ":previous_suitor"),
		(call_script, "script_add_log_entry", logent_lords_quarrel_over_woman, ":suitor", ":previous_suitor", ":lady", 0),

		(call_script, "script_troop_get_relation_with_troop", ":suitor", ":previous_suitor"), #add this to list of quarrels
		(ge, reg0, 0),
		(call_script, "script_troop_change_relation_with_troop", ":suitor", ":previous_suitor", -20),
		(val_add, "$total_courtship_quarrel_changes", -20),
	(else_try),	 #quarrelsome lords quarrel anyway
		(troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_quarrelsome),
		(neq, ":suitor", ":previous_suitor"),
		(ge, ":previous_suitor", active_npcs_begin),

#		(neq, ":previous_suitor", "trp_player"),

		(call_script, "script_troop_get_relation_with_troop", ":suitor", ":previous_suitor"), #add this to list of quarrels
		(lt, reg0, 10),
		(call_script, "script_add_log_entry", logent_lords_quarrel_over_woman, ":suitor", ":previous_suitor", ":lady", 0),
		(ge, reg0, 0),
		(call_script, "script_troop_change_relation_with_troop", ":suitor", ":previous_suitor", -20),
		(val_add, "$total_courtship_quarrel_changes", -20),

	(try_end),


#	(call_script, "script_troop_get_relation_with_troop", ":lady", ":suitor"),
#	(assign, ":orig_relation", reg0),

    (call_script, "script_lady_evaluate_troop_as_suitor", ":lady", ":suitor"),

	(store_random_in_range, ":random", 5, 16),
	(store_div, ":relationship_change", reg0, ":random"),

	(call_script, "script_troop_get_relation_with_troop", ":lady", ":suitor"),
	(assign, ":orig_relation", reg0),

	(call_script, "script_troop_change_relation_with_troop", ":lady", ":suitor", ":relationship_change"),

	(call_script, "script_troop_get_relation_with_troop", ":lady", ":suitor"),
	(assign, ":lady_suitor_relation", reg0),

	(try_begin),
		(ge, ":lady_suitor_relation", 10),
		(lt, ":orig_relation", 10),
		(call_script, "script_add_log_entry", logent_lady_favors_suitor, ":lady", 0, ":suitor", 0),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(display_message, "str_note__favor_event_logged"),
		(try_end),

	(else_try),
		(this_or_next|lt, ":lady_suitor_relation", -20),
			(ge, ":lady_suitor_relation", 20),

		(call_script, "script_get_kingdom_lady_social_determinants", ":lady"),
		(assign, ":guardian", reg0),
		(call_script, "script_troop_get_relation_with_troop", ":suitor", ":guardian"),
		(assign, ":suitor_guardian_relation", reg0),
		#things come to a head, one way or another

		(assign, ":highest_competitor_lady_score", -1),
		(assign, ":competitor_preferred_by_lady", -1),

		(assign, ":highest_competitor_guardian_score", ":suitor_guardian_relation"),
		(assign, ":competitor_preferred_by_guardian", -1),

		#log potential competitors
		(try_for_range, ":possible_competitor", lords_begin, lords_end),
			(neq, ":possible_competitor", ":suitor"),

			(this_or_next|troop_slot_eq, ":possible_competitor", slot_troop_love_interest_1, ":lady"),
			(this_or_next|troop_slot_eq, ":possible_competitor", slot_troop_love_interest_2, ":lady"),
				(troop_slot_eq, ":possible_competitor", slot_troop_love_interest_3, ":lady"),

			(try_begin),
				(call_script, "script_troop_get_relation_with_troop", ":possible_competitor", ":lady"),
				(gt, reg0, ":highest_competitor_lady_score"),
				(assign, ":competitor_preferred_by_lady", ":possible_competitor"),
				(assign, ":highest_competitor_lady_score", reg0),
			(try_end),

			(try_begin),
				(call_script, "script_troop_get_relation_with_troop", ":possible_competitor", ":guardian"),
				(gt, reg0, ":highest_competitor_guardian_score"),
				(assign, ":competitor_preferred_by_guardian", ":possible_competitor"),
				(assign, ":highest_competitor_guardian_score", reg0),
			(try_end),
		(try_end),

		#RESULTS
		#Guardian forces lady to be betrothed to suitor now
		(try_begin),
			(lt, ":lady_suitor_relation", -20),
			(this_or_next|troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_debauched),
				(troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_quarrelsome),
			(eq, ":competitor_preferred_by_guardian", -1),

			(this_or_next|troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_debauched),
				(troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_quarrelsome),

			(troop_slot_eq, ":suitor", slot_troop_betrothed, -1),
			(troop_slot_eq, ":lady", slot_troop_betrothed, -1),

			(call_script, "script_add_log_entry", logent_lady_betrothed_to_suitor_by_family, ":lady", 0, ":suitor", 0),
			(troop_set_slot, ":suitor", slot_troop_betrothed, ":lady"),
			(troop_set_slot, ":lady", slot_troop_betrothed, ":suitor"),
			(store_current_hours, ":hours"),
			(troop_set_slot, ":lady", slot_troop_betrothal_time, ":hours"),
			(troop_set_slot, ":suitor", slot_troop_betrothal_time, ":hours"),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_result_lady_forced_to_agree_to_engagement"),
			(try_end),

		#Lady rejects the suitor
		(else_try),
			(lt, ":lady_suitor_relation", -20),

			(call_script, "script_add_log_entry", logent_lady_rejects_suitor, ":lady", 0, ":suitor", 0),
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":lady", ":suitor"),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_result_lady_rejects_suitor"),
			(try_end),

		#A happy engagement, with parental blessing
		(else_try),
			(gt, ":lady_suitor_relation", 20),
			(gt, ":suitor_guardian_relation", 0),
			(eq, ":competitor_preferred_by_lady", -1),

			(troop_slot_eq, ":suitor", slot_troop_betrothed, -1),
			(troop_slot_eq, ":lady", slot_troop_betrothed, -1),

			(call_script, "script_add_log_entry", logent_lady_betrothed_to_suitor_by_choice, ":lady", 0, ":suitor", 0),
			(troop_set_slot, ":suitor", slot_troop_betrothed, ":lady"),
			(troop_set_slot, ":lady", slot_troop_betrothed, ":suitor"),
			(store_current_hours, ":hours"),
			(troop_set_slot, ":lady", slot_troop_betrothal_time, ":hours"),
			(troop_set_slot, ":suitor", slot_troop_betrothal_time, ":hours"),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":lady"),
				(str_store_troop_name, s5, ":suitor"),
				(display_message, "str_result_happy_engagement_between_s4_and_s5"),
			(try_end),

		#Lady elopes
		(else_try),
			(gt, ":lady_suitor_relation", 20),

			(eq, ":competitor_preferred_by_lady", -1),
			##diplomacy start+
			##Fix Native bug, the following line should be checking ":lady", not ":guardian"
			##OLD:
			#(this_or_next|troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_adventurous),
			#	(troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_ambitious),
			##NEW:
			(this_or_next|troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_adventurous),
				(troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_ambitious),
			##diplomacy end+

			(troop_slot_eq, ":suitor", slot_troop_betrothed, -1),
			(troop_slot_eq, ":lady", slot_troop_betrothed, -1),

			#lady elopes
			(call_script, "script_courtship_event_bride_marry_groom", ":lady", ":suitor", 1),
			#add elopements to quarrel descriptions

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":lady"),
				(str_store_troop_name, s5, ":suitor"),
				(display_message, "str_result_s4_elopes_with_s5"),
			(try_end),

		#Lady reluctantly agrees to marry under pressure from family
		(else_try),
			(troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_conventional),
			(eq, ":competitor_preferred_by_guardian", -1),
			(gt, ":suitor_guardian_relation", 4),

			(store_random_in_range, ":random", 0, 5),
			(eq, ":random", 0),

			(troop_slot_eq, ":suitor", slot_troop_betrothed, -1),
			(troop_slot_eq, ":lady", slot_troop_betrothed, -1),

			(call_script, "script_add_log_entry", logent_lady_betrothed_to_suitor_by_pressure, ":lady", 0, ":suitor", 0),
			(troop_set_slot, ":suitor", slot_troop_betrothed, ":lady"),
			(troop_set_slot, ":lady", slot_troop_betrothed, ":suitor"),
			(store_current_hours, ":hours"),
			(troop_set_slot, ":lady", slot_troop_betrothal_time, ":hours"),
			(troop_set_slot, ":suitor", slot_troop_betrothal_time, ":hours"),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":lady"),
				(str_store_troop_name, s5, ":suitor"),
				(display_message, "str_result_s4_reluctantly_agrees_to_engagement_with_s5"),
			(try_end),

		#Stalemate -- make patience roll
		(else_try),
			(gt, ":lady_suitor_relation", 20),

			(store_random_in_range, reg3, 0, 3),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_result_stalemate_patience_roll_=_reg3"),
			(try_end),

			(eq, reg3, 0),
			(call_script, "script_add_log_entry", logent_lady_rejected_by_suitor, ":lady", 0, ":suitor", 0),
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":lady", ":suitor"),
		(try_end),

	(try_end),

	]),



	("npc_decision_checklist_take_stand_on_issue",
	#Called from dialogs, and from simple_triggers

	#This a very inefficient checklist, and if I did it again, I would score for each troop. That way the troop could answer "why not" to an individual lord
	[
	(store_script_param, ":troop_no", 1),
	(store_faction_of_troop, ":troop_faction", ":troop_no"),

	(assign, ":result", -1),
	(faction_get_slot, ":faction_issue", ":troop_faction", slot_faction_political_issue),

	(assign, ":player_declines_honor", 0),
	(try_begin),
		(is_between, ":faction_issue", centers_begin, centers_end),
	    (gt, "$g_dont_give_fief_to_player_days", 1),
		(assign, ":player_declines_honor", 1),
	(else_try),
	    (gt, "$g_dont_give_marshalship_to_player_days", 1),
		(assign, ":player_declines_honor", 1),
	(try_end),

	##diplomacy start+
	(faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
	(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
	(assign, ":affiliated_with_player", reg0),

	(assign, ":subaltern_gender", -1),#The gender subject to sexism (as far as leadership is concerned).
	(try_begin),
		(lt, "$g_disable_condescending_comments", 2),#Prejudice not disabled
		(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),#Don't bother with the rest of the check
		(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),#if the lord has an unbiased outlook.
		(neg|troop_slot_ge, ":troop_no", slot_lord_reputation_type, lrep_roguish),
		(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
		(store_sub, ":subaltern_gender", 1, reg0),
		(try_begin),
			(call_script, "script_cf_dplmc_faction_has_bias_against_gender", ":troop_faction", ":subaltern_gender"),
		(else_try),
			(assign, ":subaltern_gender", -1),
		(try_end),
	(try_end),

	(assign, ":faction_lord_count", 0),#Keep track of the number of lords in the faction
	##diplomacy end+

	(assign, ":total_faction_renown", 0),
	(troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
	(try_begin),
		(eq, "$players_kingdom", ":troop_faction"),
		(eq, "$player_has_homage", 1),
		(troop_get_slot, ":total_faction_renown", "trp_player", slot_troop_renown),
		##diplomacy start+
		#Increment the faction lord count
		(val_add, ":faction_lord_count", 1),

		(try_begin),
			(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
			(eq, ":subaltern_gender", "$character_gender"),
			(val_mul, ":total_faction_renown", 4),
			(val_add, ":total_faction_renown", 3),
			(val_div, ":total_faction_renown", 5),
		(try_end),
		##diplomacy end+
	(try_end),

##diplomacy start+
	(try_for_range, ":active_npc", heroes_begin, heroes_end),#Changed range to include kingdom ladies
	    (troop_set_slot, ":active_npc", dplmc_slot_troop_temp_slot, 0), #this will hold distance to closest owned fief
##diplomacy end+
		(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0), #reset to zero

		(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
		(eq, ":active_npc_faction", ":troop_faction"),
		(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

		(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
		##diplomacy start+
		#Increment the faction lord count
		(val_add, ":faction_lord_count", 1),

		(try_begin),#If the player has set the prejudice mode to "high".
			(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
			(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
			(eq, reg0, ":subaltern_gender"),
			(val_mul, ":renown", 4),
			(val_add, ":renown", 3),
			(val_div, ":renown", 5),
		(try_end),
		##diplomacy end+
		(val_add, ":total_faction_renown", ":renown"),
	(try_end),


	(assign, ":total_faction_center_value", 0),
	(try_for_range, ":center", centers_begin, centers_end),
		(store_faction_of_party, ":center_faction", ":center"),
		(eq, ":center_faction", ":troop_faction"),

		(assign, ":center_value", 1),
		(try_begin),
		##diplomacy start+
		#Use different scoring scheme
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
			(try_begin),
			   (party_slot_eq, ":center", slot_party_type, spt_town),
  			   (assign, ":center_value", 3),
			(else_try),
			   (neg|party_slot_eq, ":center", slot_party_type, spt_village),
			   (this_or_next|party_slot_eq, ":center", slot_party_type, spt_castle),
				(is_between, ":center", walled_centers_begin, walled_centers_end),
			   (assign, ":center_value", 2),
			(try_end),
		#Otherwise fall through to old behavior
		(else_try),
		##diplomacy end+
			(is_between, ":center", towns_begin, towns_end),
			(assign, ":center_value", 2),
		(try_end),

		(val_add, ":total_faction_center_value", ":center_value"),

		(party_get_slot, ":town_lord", ":center", slot_town_lord),
		##diplomacy start+
		#The rest of the script assumes that non-player lords are heroes,
		#so add that condition here to get the count right.
		#(gt, ":town_lord", -1),
		(this_or_next|eq, ":town_lord", "trp_player"),
			(is_between, ":town_lord", heroes_begin, heroes_end),

		#Calculate distance for alternate scoring if the issue is a center
		(try_begin),
			(is_between, ":faction_issue", centers_begin, centers_end),
			(neq, ":center", ":faction_issue"),
			(troop_get_slot, ":dplmc_temp_slot", ":town_lord", dplmc_slot_troop_temp_slot),
			(store_distance_to_party_from_party, reg0, ":center", ":faction_issue"),
			(gt, reg0, 0),
			(try_begin),
				(eq, ":dplmc_temp_slot", 0),
				(assign, ":dplmc_temp_slot", reg0),
			(else_try),
				(val_min, ":dplmc_temp_slot", reg0),
			(try_end),
			(troop_set_slot, ":town_lord", dplmc_slot_troop_temp_slot, ":dplmc_temp_slot"),
		(try_end),
		##diplomacy end+

		(troop_get_slot, ":temp_slot", ":town_lord", slot_troop_temp_slot),
		(val_add, ":temp_slot", ":center_value"),
		(troop_set_slot, ":town_lord", slot_troop_temp_slot, ":temp_slot"),
	(try_end),
	(val_max, ":total_faction_center_value", 1),

	(store_div, ":average_renown_per_center_point", ":total_faction_renown", ":total_faction_center_value"),
	##diplomacy start+
	(val_max, ":faction_lord_count", 1),

#	(store_mul, ":avg_renown_plus_500_per_cp", ":faction_lord_count", 500),
#	(val_add, ":avg_renown_plus_500_per_cp", ":total_faction_renown"),
#	(store_add, reg0, ":total_faction_center_value", ":faction_lord_count"),
#	(val_div, ":avg_renown_plus_500_per_cp", reg0),

	#Get the standard deviation of renown per center point
	(assign, ":renown_per_center_point_variance", 0),
#	(assign, ":renown_plus_500_per_center_point_variance", 0),

	(try_for_range, ":active_npc", active_npcs_including_player_begin, heroes_end),
		(store_sub, ":active_npc_faction", ":troop_faction", 1),#guaranteed not to equal
		(try_begin),
			#handle player
			(eq, ":active_npc", active_npcs_including_player_begin),
			(assign, ":active_npc", "trp_player"),
			(eq, "$players_kingdom", ":troop_faction"),
			(eq, "$player_has_homage", 1),
			(assign, ":active_npc_faction", ":troop_faction"),
		(else_try),
			#handle kingdom heroes
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
		(try_end),

		(eq, ":active_npc_faction", ":troop_faction"),

		(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
		(try_begin),
			(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
			(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
			(eq, reg0, ":subaltern_gender"),
			(val_mul, ":renown", 4),
			(val_add, ":renown", 3),
			(val_div, ":renown", 5),
		(try_end),
		(troop_get_slot, ":center_points", ":active_npc", slot_troop_temp_slot),
		#Variance for renown / center points
		(val_max, ":center_points", 1),
		(store_div, reg0, ":renown", ":center_points"),
		(val_sub, reg0, ":average_renown_per_center_point"),
		(val_mul, reg0, reg0),
		(val_add, ":renown_per_center_point_variance", reg0),

#		#Variance for renown + 500 / center points + 1
#		(troop_get_slot, ":center_points", ":active_npc", slot_troop_temp_slot),
#		(val_add, ":center_points", 1),
#		(store_add, reg0, ":renown", 500),
#		(val_div, reg0, ":center_points"),
#		(val_sub, reg0, ":avg_renown_plus_500_per_cp"),
#		(val_mul, reg0, reg0),
#		(val_add, ":renown_plus_500_per_center_point_variance", reg0),
	(try_end),

	#Get renown per center point standard deviation, or 10%, whichever is greater
	(store_div, reg0, ":faction_lord_count", 2),#for rounding
	(val_add, ":renown_per_center_point_variance", reg0),
	(val_div, ":renown_per_center_point_variance", 	":faction_lord_count"),

	(assign, reg0, ":renown_per_center_point_variance"),
	(convert_to_fixed_point, reg0),
	(store_sqrt, reg0, reg0),
	(convert_from_fixed_point, reg0),
	(assign, ":renown_per_center_point_standard_deviation", reg0),
	(val_add, reg0, 5),
	(val_div, reg0, 10),
	(val_max, ":renown_per_center_point_standard_deviation", reg0),
	(store_sub, ":renown_low_target", ":average_renown_per_center_point", ":renown_per_center_point_standard_deviation"),
	(val_max, ":renown_low_target", 0),

#	#Get (renown + 500) per (center point plus one) standard deviation, or 10%, whichever is greater
#	(store_div, reg0, ":faction_lord_count", 2),#for rounding
#	(val_add, ":renown_plus_500_per_center_point_variance", reg0),
#	(val_div, ":renown_plus_500_per_center_point_variance", ":faction_lord_count"),
#
#	(assign, reg0, ":renown_plus_500_per_center_point_variance"),
#	(convert_to_fixed_point, reg0),
#	(store_sqrt, reg0, reg0),
#	(convert_from_fixed_point, reg0),
#	(assign, ":renown_plus_500_per_center_point_standard_deviation", reg0),
#	(val_add, reg0, 5),
#	(val_div, reg0, 10),
#	(val_max, ":renown_plus_500_per_center_point_standard_deviation", reg0),
#	(store_sub, ":renown_500_low_target", ":avg_renown_plus_500_per_cp", ":renown_plus_500_per_center_point_standard_deviation"),
#	(val_max, ":renown_500_low_target", 0),
	##diplomacy end+

	(try_begin),
		(is_between, ":faction_issue", centers_begin, centers_end),
		#NOTE -- The algorithms here might seem a bit repetitive, but are designed that way to create internal cliques among the lords in a faction.



		(try_begin),#If the center is a village, and a lord has no fief, choose him
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),

			(is_between, ":faction_issue", villages_begin, villages_end),
			(assign, ":favorite_lord_without_center", -1),
			(assign, ":score_to_beat", -1),
			##diplomacy start+
			(try_begin),
				#With changes enabled, widen the range of scores to check for certain personality types
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				(try_begin),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_conventional),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
					(this_or_next|is_between, ":troop_no", kings_begin, kings_end),
						(is_between, ":troop_no", pretenders_begin, pretenders_end),
					(assign, ":score_to_beat", -6),#-5 or better is indifferent
				(else_try),
					(ge, ":faction_leader", 0),
					(this_or_next|eq, ":faction_leader", ":troop_no"),
					(this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
						(troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"),
					(assign, ":score_to_beat", -6),#-5 or better is indifferent
				(try_end),
			(try_end),
			##diplomacy end+

			(try_begin),
				(eq, "$players_kingdom", ":troop_faction"),
				(eq, "$player_has_homage", 1),
				(eq, ":player_declines_honor", 0),

				(troop_slot_eq, "trp_player", slot_troop_temp_slot, 0),
				(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
				(assign, ":relation", reg0),
				##diplomacy start+
				#If the player doesn't have prejudice disabled, don't automatically support for a first fief
				(try_begin),
					(this_or_next|neq, ":subaltern_gender", "$character_gender"),
					(this_or_next|is_between, ":troop_no", companions_begin, companions_end),#Former companions will support the player
					(this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),#Spouses will support the player
						(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),
				(else_try),
					(val_sub, ":relation", 20),
				(try_end),
				##diplomacy end+

				(gt, ":relation", ":score_to_beat"),
				(neg|troop_slot_ge, "trp_player", slot_troop_controversy, 75),
				(assign, ":favorite_lord_without_center", "trp_player"),
				(assign, ":score_to_beat", ":relation"),
			(try_end),
			##diplomacy start+  Support promoted kingdom ladise
			#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),  #<-- replace this
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":troop_faction"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

				(troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
				(try_begin),
					(eq, ":active_npc", ":troop_no"),
					(assign, ":relation", 50),
				(else_try),
					(call_script, "script_troop_get_relation_with_troop", ":active_npc", ":troop_no"),
					(assign, ":relation", reg0),
				(try_end),
				##diplomacy start+ Disadvantage the subaltern gender
				(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
				(try_begin),
					(eq, reg0, ":subaltern_gender"),
					(val_sub, ":relation", 20),
				(try_end),
				##diplomacy end+
				(neg|troop_slot_ge, ":active_npc", slot_troop_controversy, 75),

				(gt, ":relation", ":score_to_beat"),
				(assign, ":favorite_lord_without_center", ":active_npc"),
				(assign, ":score_to_beat", ":relation"),
			(try_end),

			(gt, ":favorite_lord_without_center", -1),
			(assign, ":result", ":favorite_lord_without_center"),
			(assign, ":result_explainer", "str_political_explanation_lord_lacks_center"),
		##diplomacy start+
		##Faction leaders are more rational about whom they support.
	   (else_try),
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
			(call_script, "script_dplmc_get_troop_standing_in_faction", ":troop_no", ":troop_faction"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":best_candidate", -1),
			(assign, ":best_score", -1),
			(assign, ":explanation", 0),
			(try_begin),
			   (eq,"$players_kingdom", ":troop_faction"),
				(eq, "$player_has_homage", 1),
				(eq, ":player_declines_honor", 0),
				(call_script, "script_dplmc_calculate_troop_score_for_center_aux", ":troop_no", "trp_player", ":faction_issue"),#reg0 = score, reg1 = explanation
				(assign, ":best_candidate", "trp_player"),
				(assign, ":best_score", reg0),
				(assign, ":explanation", reg1),
			(try_end),
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
			   (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":troop_faction"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
				(call_script, "script_dplmc_calculate_troop_score_for_center_aux", ":troop_no", ":active_npc", ":faction_issue"),#reg0 = score, reg1 = explanation
				(this_or_next|eq, ":best_candidate", -1),
				   (gt, reg0, ":best_score"),
				(assign, ":best_candidate", ":active_npc"),
				(assign, ":best_score", reg0),
				(assign, ":explanation", reg1),
			(try_end),
			(gt, ":best_candidate", -1),
			(assign, ":result", ":best_candidate"),
			(assign, ":result_explainer", ":explanation"),
		##diplomacy end+
		(else_try),	#taken by troop
			(is_between, ":faction_issue", walled_centers_begin, walled_centers_end),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),

			(party_get_slot, ":last_taken_by_troop", ":faction_issue", slot_center_last_taken_by_troop),
			(try_begin),
				(try_begin),
					(neq, ":troop_faction", "$players_kingdom"),
					(assign, ":last_taken_by_troop", -1),
				(else_try),
					(eq, "$player_has_homage", 0),
					(assign, ":last_taken_by_troop", -1),
				(else_try),
					(eq, ":faction_issue", "$g_castle_requested_by_player"),
					(assign, ":last_taken_by_troop", "trp_player"),
				(else_try),
					(eq, ":faction_issue", "$g_castle_requested_for_troop"),
					(assign, ":last_taken_by_troop", "trp_player"),
				(else_try), #ie, the fellow who took it is no longer in the faction
					(gt, ":last_taken_by_troop", -1),
					(store_faction_of_troop, ":last_take_by_troop_faction", ":last_taken_by_troop"),
					(neq, ":last_take_by_troop_faction", ":troop_faction"),
					(assign, ":last_taken_by_troop", -1),
				(try_end),
			(try_end),
			(gt, ":last_taken_by_troop", -1),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(gt, ":last_taken_by_troop", -1),
				(str_store_troop_name, s3, ":last_taken_by_troop"),
				(display_message, "@{!}Castle taken by {s3}"),
			(try_end),


			(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":last_taken_by_troop"),
			##diplomacy start+
			#If behavior changes are enabled, increase the accepted range for certain personality types.
			(assign, ":relation", reg0),
			(try_begin),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				(try_begin),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
					(val_add, reg0, 5),#i.e. accept at -5 (indifferent) or higher
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
					(val_add, reg0, 5),#i.e. accept at -5 (indifferent) or higher
				(try_end),
			(try_end),
			##diplomacy end+
			(ge, reg0, 0),

			(neg|troop_slot_ge, ":last_taken_by_troop", slot_troop_controversy, 25),

			(troop_get_slot, ":renown", ":last_taken_by_troop", slot_troop_renown),
			##diplomacy start+
			(try_begin),
				(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
				(call_script, "script_dplmc_store_troop_is_female", ":last_taken_by_troop"),
				(eq, reg0, ":subaltern_gender"),
				(val_mul, ":renown", 4),
				(val_add, ":renown", 3),
				(val_div, ":renown", 5),
			(try_end),
			##diplomacy end+
			(troop_get_slot, ":center_points", ":last_taken_by_troop", slot_troop_temp_slot),
			(val_max, ":center_points", 1),
			(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),
			(val_mul, ":renown_divided_by_center_points", 6), #was five
			(val_div, ":renown_divided_by_center_points", 4),

			##diplomacy start+
			(try_begin),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				#Possibly raise renown_divided_by_center_points
				(store_div, reg0, ":renown", ":center_points"),
				(val_add, reg0, ":renown_per_center_point_standard_deviation"),
				(val_max, ":renown_divided_by_center_points", reg0),
			(try_end),
			##diplomacy end+
			(ge, ":renown_divided_by_center_points", ":average_renown_per_center_point"),


			(assign, ":result", ":last_taken_by_troop"),
			(assign, ":result_explainer", "str_political_explanation_lord_took_center"),


		#Check self, immediate family
		#This is done instead of a single weighted score to create cliques -- groups of NPCs who support one another
		(else_try),
			(assign, ":most_deserving_close_friend", -1),
			(assign, ":score_to_beat", ":average_renown_per_center_point"),
			(val_div, ":score_to_beat", 3),
			(val_mul, ":score_to_beat", 2),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(assign, reg3, ":score_to_beat"),
				(display_message, "@{!}Two-thirds average_renown = {reg3}"),
			(try_end),

			###diplomacy start+
			#(try_begin),
			#	(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
			#	(try_begin),
			#		(eq, "$cheat_mode", 1),
			#		(assign, reg3, ":renown_low_target"),
			#		(display_message, "@{!}Average renown per center minus one standard deviation = {reg3}"),
			#	(try_end),
			#(try_end),
			###diplomacy end+

			(try_begin),
				(eq, "$players_kingdom", ":troop_faction"),
				(eq, "$player_has_homage", 1),
				(eq, ":player_declines_honor", 0),

				(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
				(assign, ":relation", reg0),
				##diplomacy start+
				#If affiliated with player
				(this_or_next|gt, ":affiliated_with_player", 0),
				##diplomacy end+
				(ge, ":relation", 20),
				(neg|troop_slot_ge, "trp_player", slot_troop_controversy, 50),

				(troop_get_slot, ":renown", "trp_player", slot_troop_renown),
				##diplomacy start+
				(try_begin),
					(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
					(eq, ":subaltern_gender", "$character_gender"),
					(val_mul, ":renown", 4),
					(val_add, ":renown", 3),
					(val_div, ":renown", 5),
				(try_end),
				(troop_get_slot, ":center_points", "trp_player", slot_troop_temp_slot),
				(val_max, ":center_points", 1),
				(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),


				(assign, ":most_deserving_close_friend", "trp_player"),
				(assign, ":score_to_beat", ":renown_divided_by_center_points"),
			(try_end),
			##diplomacy start+  Support promoted kingdom ladies
			#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end), #<- replace
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":troop_faction"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

				(call_script, "script_troop_get_relation_with_troop", ":active_npc", ":troop_no"),
				(assign, ":relation", reg0),
				##diplomacy start+
				(assign, reg0, 0),
				#If affiliated with player
				(try_begin),
					(lt, ":relation", 20),
					(gt, ":affiliated_with_player", 0),
					(neq, ":active_npc", ":troop_no"),
					(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
				(try_end),
				(this_or_next|gt, reg0, 0),#<-- both affiliated
				##diplomacy end+
				(this_or_next|eq, ":active_npc", ":troop_no"),
					(ge, ":relation", 20),
				(neg|troop_slot_ge, ":active_npc", slot_troop_controversy, 50),

				(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
				##diplomacy start+
				(try_begin),
					(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
					(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
					(eq, reg0, ":subaltern_gender"),
					(val_mul, ":renown", 4),
					(val_add, ":renown", 3),
					(val_div, ":renown", 5),
				(try_end),
				##diplomacy end+
				(troop_get_slot, ":center_points", ":active_npc", slot_troop_temp_slot),
				(val_max, ":center_points", 1),
				(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),


				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s10, ":active_npc"),
					(assign, reg3, ":renown_divided_by_center_points"),
					(display_message, "@{!}DEBUG -- Colleague test: score for {s10} = {reg3}"),
				(try_end),


				(gt, ":renown_divided_by_center_points", ":score_to_beat"),

				(assign, ":most_deserving_close_friend", ":active_npc"),
				(assign, ":score_to_beat", ":renown_divided_by_center_points"),
			(try_end),

			(gt, ":most_deserving_close_friend", -1),


			(assign, ":result", ":most_deserving_close_friend"),
			(assign, ":result_explainer", "str_political_explanation_most_deserving_friend"),



		(else_try),
		#Most deserving in entire faction, minus those with no relation
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),

			(assign, ":most_deserving_in_faction", -1),
			(assign, ":score_to_beat", 0),

			(try_begin),
				(eq, "$players_kingdom", ":troop_faction"),
				(eq, "$player_has_homage", 1),
				(eq, ":player_declines_honor", 0),

				(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
				(assign, ":relation", reg0),
				(ge, ":relation", 0),
				(troop_get_slot, ":renown", "trp_player", slot_troop_renown),
				##diplomacy start+
				(try_begin),
					(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
					(eq, ":subaltern_gender", "$character_gender"),
					(val_mul, ":renown", 4),
					(val_add, ":renown", 3),
					(val_div, ":renown", 5),
				(try_end),
				##diplomacy end+
				(troop_get_slot, ":center_points", "trp_player", slot_troop_temp_slot),
				(neg|troop_slot_ge, "trp_player", slot_troop_controversy, 25),

				(val_max, ":center_points", 1),
				(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),

				(assign, ":most_deserving_in_faction", "trp_player"),
				(assign, ":score_to_beat", ":renown_divided_by_center_points"),
			(try_end),
			##diplomacy start+ add support for promoted kingdom ladies
			#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
			   (this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
			      (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":troop_faction"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

				(call_script, "script_troop_get_relation_with_troop", ":active_npc", ":troop_no"),
				(assign, ":relation", reg0),
				(this_or_next|eq, ":active_npc", ":troop_no"),
					(ge, ":relation", 0),
				(neg|troop_slot_ge, ":active_npc", slot_troop_controversy, 25),

				(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
				##diplomacy start+
				(try_begin),
					(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
					(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
					(eq, reg0, ":subaltern_gender"),
					(val_mul, ":renown", 4),
					(val_add, ":renown", 3),
					(val_div, ":renown", 5),
				(try_end),
				##diplomacy end+
				(troop_get_slot, ":center_points", ":active_npc", slot_troop_temp_slot),
				(val_max, ":center_points", 1),

				(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),
				(gt, ":renown_divided_by_center_points", ":score_to_beat"),

				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_string, s10, ":active_npc"),
					(assign, reg3, ":renown_divided_by_center_points"),
					(display_message, "@{!}DEBUG -- Open test: score for {s10} = {reg3}"),
				(try_end),


				(assign, ":most_deserving_in_faction", ":active_npc"),
				(assign, ":score_to_beat", ":renown_divided_by_center_points"),
			(try_end),


			(gt, ":most_deserving_in_faction", -1),
			(assign, ":result", ":most_deserving_in_faction"),
			(assign, ":result_explainer", "str_political_explanation_most_deserving_in_faction"),
		##diplomacy start+
		(else_try),
			#The lord wasn't able to find any suitable candidates,
			#so now we perform the evaluation from another perspective.
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
			#DPLMC_AI_CHANGES >= LOW
			#DPLMC_AI_CHANGES >= MEDIUM   XOR   status >= DPLMC_FACTION_STANDING_LEADER_SPOUSE
			(call_script, "script_dplmc_get_troop_standing_in_faction", ":troop_no", ":troop_faction"),
			(this_or_next|ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
			(this_or_next|lt, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				(lt, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
			(assign, ":save_reg1", reg1),

			(assign, ":score_to_beat", 0),
			(assign, ":most_deserving_in_faction", -1),
			#(assign, ":tmp_explanation", 0),

			(try_for_range, ":active_npc", active_npcs_including_player_begin, heroes_end),
				(store_sub, ":active_npc_faction", ":troop_faction", 1),
				(try_begin),
					(eq, ":active_npc", active_npcs_including_player_begin),
					(assign, ":active_npc", "trp_player"),
					(eq, "$players_kingdom", ":troop_faction"),
					(eq, "$player_has_homage", 1),
					(assign, ":active_npc_faction", ":troop_faction"),
				(else_try),
					(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
					(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(try_end),
				(eq, ":active_npc_faction", ":troop_faction"),

				#(call_script, "script_dplmc_aux_troop_evaluate_troop_for_center", ":troop_no", ":active_npc", ":faction_issue"),#reg0 = score, reg1 = explanation
				(call_script, "script_dplmc_calculate_troop_score_for_center_aux", ":troop_no", ":active_npc", ":faction_issue"),#reg0 = score, reg1 = explanation

				(this_or_next|eq, ":most_deserving_in_faction", -1),
					(ge, reg0, ":score_to_beat"),
				(assign, ":score_to_beat", reg0),
            (assign, ":result_explainer", reg1),
				(assign, ":most_deserving_in_faction", ":active_npc"),
			(try_end),

			(gt, ":most_deserving_in_faction", -1),
			(assign, ":result", ":most_deserving_in_faction"),
			#(assign, ":result_explainer", ":result_explainer"),#unneeded
         (assign, reg1, ":save_reg1"),
		##diplomacy end+
		(else_try),
			(assign, ":result", ":troop_no"),
			(assign, ":result_explainer", "str_political_explanation_self"),
		(try_end),


	(else_try),
		(eq, ":faction_issue", 1),

		(assign, ":relationship_threshhold", 15),
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
			(assign, ":relationship_threshhold", 5),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(assign, ":relationship_threshhold", 25),
		(try_end),

		#For marshals, score marshals according to renown divided by controversy - first for friends and family, then for everyone
		(assign, ":marshal_candidate", -1),
		(assign, ":score_to_beat", 0),
		(try_begin),
			(eq, "$players_kingdom", ":troop_faction"),
			(eq, "$player_has_homage", 1),
			(eq, "$g_player_is_captive", 0),
			(eq, ":player_declines_honor", 0),


			(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
			(ge, reg0, ":relationship_threshhold"),
			(assign, ":marshal_candidate", "trp_player"),
			(troop_get_slot, ":renown", "trp_player", slot_troop_renown),
			##diplomacy start+
			(try_begin),
				(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
				(eq, ":subaltern_gender", "$character_gender"),
				(val_mul, ":renown", 4),
				(val_add, ":renown", 3),
				(val_div, ":renown", 5),
			(try_end),
			##diplomacy end+
			(troop_get_slot, ":controversy_divisor", "trp_player", slot_troop_controversy),
			(val_add, ":controversy_divisor", 50),
			(store_div, ":score_to_beat", ":renown", ":controversy_divisor"),
		(try_end),

      ##diplomacy start+ Support promoted ladies
		#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
		(try_for_range, ":active_npc", heroes_begin, heroes_end),
      ##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":troop_faction"),
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			(troop_slot_eq, ":active_npc", slot_troop_prisoner_of_party, -1),

			(neg|faction_slot_eq, ":troop_faction", slot_faction_leader, ":active_npc"),

			(call_script, "script_troop_get_relation_with_troop", ":active_npc", ":troop_no"),
			(assign, ":relation", reg0),
			(this_or_next|eq, ":active_npc", ":troop_no"),
				(ge, ":relation", ":relationship_threshhold"),

			(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
			##diplomacy start+
			(try_begin),
				(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
				(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
				(eq, reg0, ":subaltern_gender"),
				(val_mul, ":renown", 4),
				(val_add, ":renown", 3),
				(val_div, ":renown", 5),
			(try_end),
			##diplomacy end+
			(troop_get_slot, ":controversy_divisor", ":active_npc", slot_troop_controversy),
			(val_add, ":controversy_divisor", 50),
			(store_div, ":score", ":renown", ":controversy_divisor"),

			(gt, ":score", ":score_to_beat"),

			(assign, ":marshal_candidate", ":active_npc"),
			(assign, ":score_to_beat", ":score"),

		(try_end),

		(assign, ":result", ":marshal_candidate"),
		(assign, ":result_explainer", "str_political_explanation_marshal"),
	(try_end),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(gt, ":result", -1),
		(str_store_troop_name, s8, ":troop_no"),
		(str_store_troop_name, s9, ":result"),
		(str_store_string, s10, ":result_explainer"),
		(display_message, "@{!}DEBUG -- {s8} backs {s9}:{s10}"),
	(try_end),

	(assign, reg0, ":result"),
	(assign, reg1, ":result_explainer"),

	]),


	("npc_decision_checklist_evaluate_faction_strategy",
	[
	#Decides whether the strategy is good or bad -- to be added
	]),


	
("dplmc_copy_upgrade_to_all_heroes",
  [
    (store_script_param_1, ":troop"),
    (store_script_param_2, ":type"),

    (try_begin),
      (eq, ":type", dplmc_wpn_setting_1),
      (troop_get_slot,":upg_wpn0", ":troop",dplmc_slot_upgrade_wpn_0),
      (troop_get_slot,":upg_wpn1", ":troop",dplmc_slot_upgrade_wpn_1),
      (troop_get_slot,":upg_wpn2", ":troop",dplmc_slot_upgrade_wpn_2),
      (troop_get_slot,":upg_wpn3", ":troop",dplmc_slot_upgrade_wpn_3),
      (try_for_range, ":hero", heroes_begin, heroes_end),
        (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_0,":upg_wpn0"),
        (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_1,":upg_wpn1"),
        (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_2,":upg_wpn2"),
        (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_3,":upg_wpn3"),
      (try_end),
    (else_try),
      (eq, ":type", dplmc_armor_setting),
      (troop_get_slot,":upg_armor", ":troop",dplmc_slot_upgrade_armor),
      (try_for_range, ":hero", heroes_begin, heroes_end),
        (troop_set_slot,":hero",dplmc_slot_upgrade_armor,":upg_armor"),
      (try_end),
    (else_try),
      (eq, ":type", dplmc_horse_setting),
      (troop_get_slot,":upg_horse", ":troop",dplmc_slot_upgrade_horse),
      (try_for_range, ":hero", heroes_begin, heroes_end),
        (troop_set_slot,":hero",dplmc_slot_upgrade_horse,":upg_horse"),
      (try_end),
    (try_end),
  ]),

  ("dplmc_is_affiliated_family_member",
  [
      (store_script_param, ":troop_id", 1),

      (assign, ":is_affiliated_family_member", 0),
	  ##nested diplomacy start+
	  (assign, ":save_reg1", reg1),#<- Save reg1 which gets overwritten by script_dplmc_troop_get_family_relation_to_troop
	  ##nested diplomacy end+
      (try_begin),
        (is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
        (try_begin),
		  ##nested diplomacy start+ add use of dplmc_slot_troop_affiliated
		  (this_or_next|troop_slot_eq, ":troop_id", dplmc_slot_troop_affiliated, 3),
		  ##diplomacy end+
          (eq, "$g_player_affiliated_troop", ":troop_id"),
          (assign, ":is_affiliated_family_member", 1),
        (else_try),
          (is_between, ":troop_id", lords_begin, kingdom_ladies_end),
		  ##nested diplomacy start+
          #(call_script, "script_troop_get_family_relation_to_troop", ":troop_id", "$g_player_affiliated_troop"),
		  (call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_id", "$g_player_affiliated_troop"),
		  ##nested diplomacy end+
          (gt, reg0, 0),
          (call_script, "script_troop_get_relation_with_troop", "$g_player_affiliated_troop", ":troop_id"),
          (ge, reg0, -10),
		  (assign, ":is_affiliated_family_member", 1),
        (try_end),
      (try_end),
	  ##nested diplomacy start+
	  (assign, reg1, ":save_reg1"),#revert register
	  ##nested diplomacy end+
      (assign, reg0, ":is_affiliated_family_member"),
  ]),

    # INPUT: arg1 = troop_id, arg2 = new faction_no
  # OUTPUT: none
  ("dplmc_lord_return_from_exile",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":faction_no"),
      #Check validity
	  (try_begin),
		  (is_between, ":troop_no", heroes_begin, heroes_end),
		  (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
		  (neq, ":troop_no", "trp_player"),
		  (faction_get_slot, ":faction_liege", ":faction_no", slot_faction_leader),
		  #The lord definitely should not already belong to a kingdom
		  (store_troop_faction, ":old_faction", ":troop_no"),
		  (neg|is_between, ":old_faction", kingdoms_begin, kingdoms_end),
		  (try_begin),
			#Handle separately for adding to the player's faction
			#The player may decide to accept or reject the return
			(this_or_next|eq, ":faction_liege", "trp_player"),
			(eq, ":faction_no", "fac_player_supporters_faction"),
			#(eq, 1, 0),#<-- temporarily disable
			#Lord comes to petition the player instead of automatically returning
			(call_script, "script_change_troop_faction", ":troop_no", ":faction_no"),
			(troop_set_slot, ":troop_no", slot_troop_occupation, slto_inactive),
			#Show event (no log without actual faction change)
			(str_store_troop_name_link, s4, ":troop_no"),
			(str_store_faction_name_link, s5, ":faction_no"),
			(faction_get_color, ":color", ":faction_no"), #SB : store colour for logs
			(str_store_troop_name_link, s6, ":faction_liege"),
			(display_message, "@{s4} has returned from exile, seeking refuge with {s6} of {s5}.", ":color"),
		    #Remove party
			(troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
			(try_begin),
				(party_is_active, ":led_party"),
				(neq, ":led_party", "p_main_party"),
				(remove_party, ":led_party"),
				(troop_set_slot, ":troop_no", slot_troop_leaded_party, -1),
			(try_end),
			#
		  (else_try),
			 #NPC king auto-accepts
			 #Normalize relation between NPC and king
			 (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_liege"),
			 (store_sub, ":relation_change", 0, reg0),#enough to increase to 0 if negative
			 (val_max, ":relation_change", 5),
			 (call_script, "script_troop_change_relation_with_troop", ":troop_no", ":faction_liege", ":relation_change"),
			 #Perform reverse of relation change for exile
			 (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end), #all lords in own faction, and relatives regardless of faction
				(assign, ":relation_change", 0),#no change for non-relatives in other factions
				(try_begin),
					(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
					(eq, ":faction_no", ":active_npc_faction"),
					#Auto-exiling someone at -75 relation to his liege gives a -1 base
					#relation penalty from other lords, so the gain is 1 by default.
					(assign, ":relation_change", 1),
				(try_end),
				##(call_script, "script_troop_get_family_relation_to_troop", ":troop_no", ":active_npc"),
				(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_no", ":active_npc"),
				(assign, ":family_relation", reg0),
				(try_begin),
					(gt, ":family_relation", 1),
					(store_div, ":family_modifier", reg0, 3),
					(val_add, ":relation_change", ":family_modifier"),
				(try_end),

				(neq, ":relation_change", 0),

				(call_script, "script_troop_change_relation_with_troop", ":faction_liege", ":active_npc", ":relation_change"),
				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s17, ":active_npc"),
					(str_store_troop_name, s18, ":faction_liege"),
					(assign, reg3, ":relation_change"),
					(display_message, "str_trial_influences_s17s_relation_with_s18_by_reg3"),
				(try_end),
			 (try_end),#end try for range :active_npc

			#Now actually change the faction
			(call_script, "script_change_troop_faction", ":troop_no", ":faction_no"),
			(try_begin), #new-begin
				(neq, ":faction_no", "fac_player_supporters_faction"),
				(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
					(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_retirement),
					(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_exile), #SB : revoke exile
				(troop_set_slot, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		    (try_end), #new-end

			#Log event
			(str_store_troop_name_link, s4, ":troop_no"),
			(str_store_faction_name_link, s5, ":faction_no"),
			(str_store_troop_name_link, s6, ":faction_liege"),
			(faction_get_color, ":color", ":faction_no"), #SB : store colour for logs
			(display_log_message, "@{s4} has been granted a pardon by {s6} of {s5} and has returned from exile.", ":color"),

            #SB : spawn full army
            (troop_set_slot, ":troop_no", slot_troop_spawned_before, 0),
			(troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
			(try_begin),
				(party_is_active, ":led_party"),
				(neq, ":led_party", "p_main_party"),
				(remove_party, ":led_party"),
				(troop_set_slot, ":troop_no", slot_troop_leaded_party, -1),
			(try_end),
		  (try_end),#end NPC king auto-accepts
      (else_try),
	    #Failure.  Perform string register assignment first to avoid differences
		#between debug and non-debug behavior.
		(str_store_troop_name, s5, ":troop_no"),
		(str_store_faction_name, s7, ":faction_no"),
		#(ge, "$cheat_mode", 1),#<-- always show this
		(display_message, "@{!}DEBUG : failure in dplmc_lord_return_from_exile((s5}, {s7})"),
	  (try_end),
    ]),

    #script_dplmc_get_troop_morality_value
  #
  #Related to script_dplmc_remove_gold_from_lord_and_holdings, divides the gold
  #between the lord and his fortresses in a semi-intelligent way.
  #
  #INPUT:
  #   arg1: the amount of gold
  #   arg2: the lord's ID
  ("dplmc_distribute_gold_to_lord_and_holdings",
   [
	(store_script_param_1, ":gold_left"),
	(store_script_param_2, ":lord_no"),

	(try_begin),
		(lt, ":lord_no", 0),#Invalid ID
	(else_try),
		#If the number is negative, handle this using script_dplmc_remove_gold_from_lord_and_holdings
		(lt, ":gold_left", 0),
		(val_mul, ":gold_left", -1),
		(call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":gold_left", ":lord_no"),
		(assign, ":gold_left", 0),
	(else_try),
		(neq, ":lord_no", "trp_player"),
		(neg|troop_is_hero, ":lord_no"),#Not hero or player
        (troop_add_gold, ":lord_no", ":gold_left"),
        (assign, ":gold_left", 0),
	(else_try),
		#The player doesn't use center wealth to pay garrison wages, so just
		#give it directly.
		(eq, ":lord_no", "trp_player"),
		(troop_add_gold, "trp_player", ":gold_left"),
		(assign, ":gold_left", 0),
	(else_try),
		(neg|troop_is_hero, ":lord_no"),#If the lord isn't the player, and isn't a hero, do nothing
	(else_try),
		(troop_get_slot, ":target_gold", ":lord_no", slot_troop_wealth),
		(val_max, ":target_gold", 0),
		#If the lord is low on gold, first he takes enough gold so he isn't low on funds,
		#or all of the gold, whichever is less.
		(store_sub, ":gold_to_give", 6000, ":target_gold"),#6000 is the standard starting gold for lords (kings start with more, but don't increase this for them, since I'm using this number as a "low on gold" threshold)
		(val_max, ":gold_to_give", 0),
		(val_min, ":gold_to_give", ":gold_left"),

		(val_add, ":target_gold", ":gold_to_give"),
		(troop_set_slot, ":lord_no", slot_troop_wealth, ":target_gold"),
		(val_sub, ":gold_left", ":gold_to_give"),
		#If gold remains, the lord gives some to any castles or towns he owns that have
		#low wealth.  Note that iterating in this order means that towns get checked
		#before castles do.
		(gt, ":gold_left", 0),
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, ":lord_no"),
			(party_get_slot, ":target_gold", ":center_no", slot_town_wealth),
			#Don't give gold to centers with garrisons more than 50% above the ideal size
			(store_party_size_wo_prisoners, ":garrison_size", ":center_no"),
			(call_script, "script_party_get_ideal_size", ":center_no"),#This script has been modified to support this use
			(val_mul, reg0, 3),
			(val_div, reg0, 2),
			(ge, reg0, ":garrison_size"),

			(try_begin),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(store_sub, ":gold_to_give", 4000, ":target_gold"),#4000 is the standard starting gold for towns
			(else_try),
				(store_sub, ":gold_to_give", 2000, ":target_gold"),#2000 is the standard starting gold for castles
			(try_end),

			(val_max, ":gold_to_give", 0),
			(val_min, ":gold_to_give", ":gold_left"),
			(gt, ":gold_to_give", 0),
			(val_add, ":target_gold", ":gold_to_give"),
			(party_set_slot, ":center_no", slot_town_wealth, ":target_gold"),
			(val_sub, ":gold_left", ":gold_to_give"),
		(try_end),
		#If gold is left -- the lord isn't low on gold, and none of his walled centers are --
		#he pockets the remainder.
		(gt, ":gold_left", 0),
		(troop_get_slot, ":target_gold", ":lord_no", slot_troop_wealth),
		(val_add, ":target_gold", ":gold_left"),
		(val_max, ":target_gold", 0),
		(troop_set_slot, ":lord_no", slot_troop_wealth, ":target_gold"),
		(assign, ":gold_left", 0),
	(try_end),
	]),


  #"script_dplmc_remove_gold_from_lord_and_holdings"
  #
  #
  #INPUT:
  #   arg1: the amount of money to remove (greater than zero)
  #   arg2: the ID of the lord spending the money
  #
  #OUTPUT:
  #   None
    ("dplmc_remove_gold_from_lord_and_holdings",
   [
    (store_script_param_1, ":gold_cost"),
	(store_script_param_2, ":lord_no"),

	(try_begin),
		(lt, ":lord_no", 0),#Invalid ID
	(else_try),
		(neq, ":lord_no", "trp_player"),
		(neg|troop_is_hero, ":lord_no"),#Not player or hero
	(else_try),
		#If the number is negative, give gold instead of taking it.
		#Handle this using script_dplmc_distribute_gold_to_lord_and_holdings
		(lt, ":gold_cost", 0),
		(val_mul, ":gold_cost", -1),
		(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":gold_cost", ":lord_no"),
		(assign, ":gold_cost", 0),
	(else_try),
		#For the player, first subtract the gold from his treasury (if any).
		(eq, ":lord_no", "trp_player"),
	    (store_troop_gold, ":treasury", "trp_household_possessions"),
		(try_begin),
		(ge, ":treasury", 1),
		(val_min, ":treasury", ":gold_cost"),
		(call_script, "script_dplmc_withdraw_from_treasury", ":treasury"),
		(val_sub, ":gold_cost", ":treasury"),
		(try_end),
		(store_troop_gold, ":treasury", "trp_player"),
		(try_begin),
			(ge, ":treasury", 1),
			(val_min, ":treasury", ":gold_cost"),
			(troop_remove_gold, "trp_player", ":treasury"),
			(val_sub, ":gold_cost", ":treasury"),
		(try_end),
		#Fall through to the next section if the treasury didn't cover it.
		(lt, ":gold_cost", 1),
	(else_try),
		#Remove the gold directly from the lord's wealth slot
		(ge, ":gold_cost", 1),
		(ge, ":lord_no", 1),#not the player
		(troop_get_slot, ":treasure", ":lord_no", slot_troop_wealth),
		(ge, ":treasure", 1),
		(try_begin),
			(ge, ":treasure", ":gold_cost"),
			(val_sub, ":treasure", ":gold_cost"),
			(assign, ":gold_cost", 0),
		(else_try),
			(val_sub, ":gold_cost", ":treasure"),
			(assign, ":treasure", 0),
		(try_end),
		(troop_set_slot, ":lord_no", slot_troop_wealth, ":treasure"),
		#Fall through to the next section if his personal wealth didn't cover it.
		(lt, ":gold_cost", 1),
	(else_try),
		#Remove remaining gold from uncollected taxes.
		#We iterate backwards in order to remove from villages before castles and towns.
		(ge, ":gold_cost", 1),
		(try_for_range_backwards, ":center_no", centers_begin, centers_end),
			(ge, ":gold_cost", 1),
			(party_slot_eq, ":center_no", slot_town_lord, ":lord_no"),
			(party_get_slot, ":treasure", ":center_no", slot_center_accumulated_rents),
			(try_begin),
               	(gt, ":treasure", 0),
				(ge, ":treasure", ":gold_cost"),
				(val_sub, ":treasure", ":gold_cost"),
				(assign, ":gold_cost", 0),
			(else_try),
               	(gt, ":treasure", 0),
				(val_sub, ":gold_cost", ":treasure"),
				(assign, ":treasure", 0),
			(try_end),
				(party_set_slot, ":center_no", slot_center_accumulated_rents, ":treasure"),

			(ge, ":gold_cost", 1),
			(party_get_slot, ":treasure", ":center_no", slot_center_accumulated_tariffs),
			(try_begin),
               	(gt, ":treasure", 0),
				(ge, ":treasure", ":gold_cost"),
				(val_sub, ":treasure", ":gold_cost"),
				(assign, ":gold_cost", 0),
			(else_try),
               	(gt, ":treasure", 0),
				(val_sub, ":gold_cost", ":treasure"),
				(assign, ":treasure", 0),
			(try_end),
			(party_set_slot, ":center_no", slot_center_accumulated_tariffs, ":treasure"),
		(try_end),
		#Fall through to the next section if the uncollected taxes didn't cover it.
		(lt, ":gold_cost", 1),
	(else_try),
		#Remove remaining gold from center wealth.  We iterate backwards to remove from
		#castles before towns.
		(ge, ":gold_cost", 1),
		(try_for_range_backwards, ":center_no", centers_begin, centers_end),
			(ge, ":gold_cost", 1),
			(party_slot_eq, ":center_no", slot_town_lord, ":lord_no"),
			(party_get_slot, ":treasure", ":center_no", slot_town_wealth),
		(ge, ":treasure", 1),
		(try_begin),
			(ge, ":treasure", ":gold_cost"),
			(val_sub, ":treasure", ":gold_cost"),
			(assign, ":gold_cost", 0),
		(else_try),
			(val_sub, ":gold_cost", ":treasure"),
			(assign, ":treasure", 0),
		(try_end),
			(party_set_slot, ":center_no", slot_town_wealth, ":treasure"),
		(try_end),
		(lt, ":gold_cost", 1),
	(else_try),
	    #Try to remove the gold from the hero himself
		(store_troop_gold, ":treasure", ":lord_no"),
		(gt, ":treasure", 0),
		(try_begin),
			(ge, ":treasure", ":gold_cost"),
			(troop_remove_gold, ":lord_no", ":gold_cost"),
			(assign, ":gold_cost", 0),
		(else_try),
			(troop_remove_gold, ":treasure"),
			(val_sub, ":gold_cost", ":treasure"),
		(try_end),
	(try_end),

   ]),

  # "script_dplmc_prepare_hero_center_points_ignoring_center"
  #
  #INPUT:
  #  arg1: troop_no
  #  arg2: whether the first letter must be capitalized
  #
  #OUTPUT:
  #    s0: a string that can be substituted for "my {husband/wife}" or "my love"
  ("dplmc_print_player_spouse_says_my_husband_wife_to_s0",
   [
     (store_script_param_1, ":troop_no"),
     (store_script_param_2, ":capitalized"),

 	 (assign, ":save_reg0", reg0),
	 (assign, ":save_reg6", reg6),
	 (assign, ":save_reg7", reg7),
	 #(assign, reg6, ":capitalized"),
	 (assign, reg7, 0),

    #Base switch is 50 (i.e. where the "brave champion" greeting starts)
    (try_begin),
      (lt, ":troop_no", 1),#bad value
      (assign, reg0, 0),
      (assign, reg6, lrep_none),
    (else_try),
	   (call_script, "script_troop_get_player_relation", ":troop_no"),#write relation to reg0
      (troop_get_slot, reg6, ":troop_no", slot_lord_reputation_type),#write relation to reg6
      (eq, reg6, lrep_conventional),#...jumps to next branch (keeping reg0 and reg6) if this isn't true
		(val_add, reg0, 25),#from 25+
	 (else_try),
      (eq, reg6, lrep_otherworldly),
		(val_add, reg0, 30),#from 20+
	 (else_try),
      (eq, reg6, lrep_moralist),
      (store_sub, reg7, "$player_honor", 10),
      (val_clamp, reg7, -40, 31),
      (val_add, reg0, reg7),
      (assign, reg7, 0),
    (else_try),
      (eq, reg6, lrep_ambitious),
      (assign, reg7, -10),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
            (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
         (val_add, reg7, 10),
         (party_slot_eq, ":center_no", slot_party_type, spt_town),
         (val_add, reg7,  10),
      (try_end),
      (val_clamp, reg7, -10, 30),
      (val_add, reg0, reg7),
      (assign, reg7, 0),
    (else_try),
      (eq, reg6, lrep_adventurous),
      (val_add, reg7, 20),#from 30+
    (else_try),
      (eq, reg6, lrep_none),
      (is_between, reg6, heroes_begin, heroes_end),
      (val_sub, reg0, 20),#from 70+
    (else_try),
      (eq, reg6, lrep_cunning),
      (val_sub, reg0, 20),#from 70+
    (else_try),
      (this_or_next|eq, reg6, lrep_debauched),
      (this_or_next|eq, reg6, lrep_quarrelsome),
      (this_or_next|eq, reg6, lrep_selfrighteous),
      (val_sub, reg0, 30),#from 80+
	 (try_end),

    (try_begin),
       (ge, reg0, 50),
       (assign, reg7, 1),
    (try_end),

    (try_begin),
       #Embellishment: diminuitive pet-names
       (eq, reg6, lrep_debauched),
       (gt, ":troop_no", 0),
       (store_character_level, ":player_level", "trp_player"),
       (store_character_level, ":troop_level", ":troop_no"),
       (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
       (this_or_next|ge, ":troop_level", ":player_level"),
       (this_or_next|troop_slot_ge, ":troop_no", slot_troop_renown, ":player_renown"),
          (lt, reg0, 50),
       (assign, reg6, ":capitalized"),#Whether the first letter needs to be upper case
       (str_store_string, s0, "@{reg6?M:m}y poppet"),
    (else_try),
       #The basic idea.  Further embellishments may come.
       (assign, reg6, ":capitalized"),#Whether the first letter needs to be upper case
       (str_store_string, s0, "str_dplmc_reg6my_reg7spouse"),
    (try_end),

	 #Revert registers
	 (assign, reg0, ":save_reg0"),
	 (assign, reg6, ":save_reg6"),
	 (assign, reg7, ":save_reg7"),
   ]),

  ##"script_dplmc_initialize_autoloot"
##
##Like troop_get_family_relation_to_troop, except instead of writing to s11,
##it writes the index of the relation string to reg1, and writes nothing at
##all to reg4.
  ("dplmc_troop_get_family_relation_to_troop",
    [
    (store_script_param_1, ":troop_1"),
    (store_script_param_2, ":troop_2"),

    ##dplmc start+

	(try_begin),
		(eq, ":troop_1", active_npcs_including_player_begin),
		(assign, ":troop_1", "trp_player"),
	(try_end),
	(try_begin),
		(eq, ":troop_2", active_npcs_including_player_begin),
		(assign, ":troop_2", "trp_player"),
	(try_end),

	#use gender script
    #(troop_get_type, ":gender_1", ":troop_1"),
	(call_script, "script_dplmc_store_troop_is_female", ":troop_1"),
	(assign, ":gender_1", reg0),
	(assign, ":relation_string", "str_no_relation"),
	##dplmc end+
	(assign, ":relation_strength", 0),

	##dplmc start+
	#Uninitialized memory is 0, which equals "trp_player", which is the cause
	#of some annoying bugs.  In Native the game doesn't set the various family
	#slots to -1 except for the player and in the heroes_begin to heroes_end
	#range.

	(troop_get_slot, ":spouse_of_1", ":troop_1", slot_troop_spouse),#just do this to get an error if the troop ID is bad
	(troop_get_slot, ":spouse_of_2", ":troop_2", slot_troop_spouse),#just do this to get an error if the troop ID is bad

	(call_script, "script_dplmc_helper_get_troop1_troop2_family_slot_aux", ":troop_1", ":troop_2", slot_troop_spouse),
	(assign, ":spouse_of_1", reg0),
	(assign, ":spouse_of_2", reg1),

	(call_script, "script_dplmc_helper_get_troop1_troop2_family_slot_aux", ":spouse_of_1", ":spouse_of_2", slot_troop_father),
	(assign, ":father_of_spouse_of_1", reg0),
	(assign, ":father_of_spouse_of_2", reg1),

	(call_script, "script_dplmc_helper_get_troop1_troop2_family_slot_aux", ":spouse_of_1", ":spouse_of_2", slot_troop_mother),
	#(assign, ":mother_of_spouse_of_1", reg0),
	(assign, ":mother_of_spouse_of_2", reg1),

	(call_script, "script_dplmc_helper_get_troop1_troop2_family_slot_aux", ":troop_1", ":troop_2", slot_troop_father),
	(assign, ":father_of_1", reg0),
	(assign, ":father_of_2", reg1),

	(call_script, "script_dplmc_helper_get_troop1_troop2_family_slot_aux", ":troop_1", ":troop_2", slot_troop_mother),
	(assign, ":mother_of_1", reg0),
	(assign, ":mother_of_2", reg1),

	(call_script, "script_dplmc_helper_get_troop1_troop2_family_slot_aux", ":father_of_1", ":father_of_2", slot_troop_father),
	(assign, ":paternal_grandfather_of_1", reg0),
	(assign, ":paternal_grandfather_of_2", reg1),

	(call_script, "script_dplmc_helper_get_troop1_troop2_family_slot_aux", ":father_of_1", ":father_of_2", slot_troop_mother),
	(assign, ":paternal_grandmother_of_1", reg0),
	(assign, ":paternal_grandmother_of_2", reg1),

	(call_script, "script_dplmc_helper_get_troop1_troop2_family_slot_aux", ":mother_of_1", ":mother_of_2", slot_troop_father),
	(assign, ":maternal_grandfather_of_1", reg0),
	(assign, ":maternal_grandfather_of_2", reg1),

	(call_script, "script_dplmc_helper_get_troop1_troop2_family_slot_aux", ":mother_of_1", ":mother_of_2", slot_troop_mother),
	(assign, ":maternal_grandmother_of_1", reg0),
	(assign, ":maternal_grandmother_of_2", reg1),

	(call_script, "script_dplmc_helper_get_troop1_troop2_family_slot_aux", ":troop_1", ":troop_2", slot_troop_guardian),
	(assign, ":guardian_of_1", reg0),
	(assign, ":guardian_of_2", reg1),
	##diplomacy end+

	#(str_store_string, s11, "str_no_relation"),

	(try_begin),
	  (eq, ":troop_1", ":troop_2"),
	  #self
	(else_try),
	  ##diplomacy start+
      (this_or_next|eq, ":spouse_of_2", ":troop_1"),#polygamy helper
	  ##diplomacy end+
	  (eq, ":spouse_of_1", ":troop_2"),
	  (assign, ":relation_strength", 20),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_wife"),
	  (else_try),
	    (assign, ":relation_string", "str_husband"),
	  (try_end),
	(else_try),
	  (eq, ":father_of_2", ":troop_1"),
	  (assign, ":relation_strength", 15),
	  (assign, ":relation_string", "str_father"),
	(else_try),
	  (eq, ":mother_of_2", ":troop_1"),
	  (assign, ":relation_strength", 15),
	  (assign, ":relation_string", "str_mother"),
	(else_try),
	  (this_or_next|eq, ":father_of_1", ":troop_2"),
	  (eq, ":mother_of_1", ":troop_2"),
	  (assign, ":relation_strength", 15),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_daughter"),
	  (else_try),
	    (assign, ":relation_string", "str_son"),
	  (try_end),
	##diplomacy start+
	(else_try),
	   #Check for half-siblings: sharing a father
	   (neq, ":father_of_1", -1),
	   (eq, ":father_of_1", ":father_of_2"),
	   (neq, ":mother_of_1", ":mother_of_2"),
	   (assign, ":relation_strength", 10),
	   (try_begin),
	     (eq, ":gender_1", tf_female),
	     (assign, ":relation_string", "str_dplmc_half_sister"),
	   (else_try),
	     (assign, ":relation_string", "str_dplmc_half_brother"),
	   (try_end),
   (else_try),
	   #Check for half-siblings: sharing a mother
	   (neq, ":mother_of_1", -1),
	   (eq, ":mother_of_1", ":mother_of_2"),
	   (neq, ":father_of_1", ":father_of_2"),
	   (assign, ":relation_strength", 10),
	   (try_begin),
	     (eq, ":gender_1", tf_female),
	     (assign, ":relation_string", "str_dplmc_half_sister"),
	   (else_try),
	     (assign, ":relation_string", "str_dplmc_half_brother"),
	   (try_end),
	##diplomacy end+
	(else_try),
	  #(gt, ":father_of_1", -1), #necessary, as some lords do not have the father registered #dplmc+ replaced
	  (neq, ":father_of_1", -1), #dplmc+ added
	  (eq, ":father_of_1", ":father_of_2"),
	  (assign, ":relation_strength", 10),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_sister"),
	  (else_try),
	    (assign, ":relation_string", "str_brother"),
	  (try_end),
	(else_try),
	  (eq, ":guardian_of_2", ":troop_1"),
	  (assign, ":relation_strength", 10),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_sister"),
	  (else_try),
	    (assign, ":relation_string", "str_brother"),
	  (try_end),
	(else_try),
	  (eq, ":guardian_of_1", ":troop_2"),
	  (assign, ":relation_strength", 10),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_sister"),
	  (else_try),
	    (assign, ":relation_string", "str_brother"),
	  (try_end),
	##diplomacy start+
    (else_try),#polygamy, between two people married to the same person
	   (neq, ":spouse_of_1", -1),
	   (eq, ":spouse_of_2", ":spouse_of_1"),
	   (assign, ":relation_strength", 10),
	   (try_begin),
	      (call_script, "script_dplmc_store_troop_is_female", ":troop_2"),
		  (neq, ":gender_1", reg0),
		  (assign, ":relation_string", "str_dplmc_co_spouse"),
	   (else_try),
	      (eq, ":gender_1", tf_female),
	     (assign, ":relation_string", "str_dplmc_sister_wife"),
	   (else_try),
	      (assign, ":relation_string", "str_dplmc_co_husband"),
	   (try_end),
	##diplomacy end+
	(else_try),
	  #(gt, ":paternal_grandfather_of_1", -1),#dplmc+ replaced
	  (neq, ":father_of_2", -1),#dplmc+ added
	  (this_or_next|eq, ":maternal_grandfather_of_1", ":father_of_2"),#dplmc+ added
	  (eq, ":paternal_grandfather_of_1", ":father_of_2"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_niece"),
	  (else_try),
	    (assign, ":relation_string", "str_nephew"),
	  (try_end),
	##diplomacy start+: add niece/nephew through mother
	(else_try),
	  (neq, ":mother_of_2", -1),
  	  (this_or_next|eq, ":maternal_grandmother_of_1", ":mother_of_2"),
	  (eq, ":paternal_grandmother_of_1", ":mother_of_2"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_niece"),
	  (else_try),
	    (assign, ":relation_string", "str_nephew"),
	  (try_end),
	##diplomacy end+
	(else_try), #specifically aunt and uncle by blood -- i assume that in a medieval society with lots of internal family conflicts, they would not include aunts and uncles by marriage
	  #(gt, ":paternal_grandfather_of_2", -1),#dplmc+ replaced
	  (neq, ":father_of_1", -1),#dplmc+ added
	  (this_or_next|eq, ":maternal_grandfather_of_2", ":father_of_1"),#dplmc+ added
	  (eq, ":paternal_grandfather_of_2", ":father_of_1"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_aunt"),
	  (else_try),
	    (assign, ":relation_string", "str_uncle"),
	  (try_end),
	##diplomacy start+
	#blood uncles & blood aunts, continued (via mother)
	(else_try),
	  (neq, ":mother_of_1", -1),
	  (this_or_next|eq, ":maternal_grandmother_of_2", ":mother_of_1"),
	  (eq, ":paternal_grandmother_of_2", ":mother_of_1"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_aunt"),
	  (else_try),
	    (assign, ":relation_string", "str_uncle"),
	  (try_end),
	##diplomacy end+
	(else_try),
	  #(gt, ":paternal_grandfather_of_1", 0),#dplmc+ replaced (why was this one "gt 0" but the previous "gt -1"?)
	  (neq, ":paternal_grandfather_of_1", -1),#dplmc+ added
	  (this_or_next|eq, ":maternal_grandfather_of_2", ":paternal_grandfather_of_1"),#dplmc+ added
	  (eq, ":paternal_grandfather_of_2", ":paternal_grandfather_of_1"),
	  (assign, ":relation_strength", 2),
	  (assign, ":relation_string", "str_cousin"),
	##diplomacy start+
	#Add cousin via paternal grandmother or maternal grandparents
	(else_try),
	  (neq, ":maternal_grandfather_of_1", -1),
	  (this_or_next|eq, ":maternal_grandfather_of_2", ":maternal_grandfather_of_1"),
	  (eq, ":paternal_grandfather_of_2", ":maternal_grandfather_of_1"),
	  (assign, ":relation_strength", 2),
	  (assign, ":relation_string", "str_cousin"),
	(else_try),
	  (neq, ":paternal_grandmother_of_1", -1),
	  (this_or_next|eq, ":maternal_grandmother_of_2", ":paternal_grandmother_of_1"),
	  (eq, ":paternal_grandmother_of_2", ":paternal_grandmother_of_1"),
	  (assign, ":relation_strength", 2),
	  (assign, ":relation_string", "str_cousin"),
	(else_try),
	  (neq, ":maternal_grandmother_of_1", -1),
	  (this_or_next|eq, ":maternal_grandmother_of_2", ":maternal_grandmother_of_1"),
	  (eq, ":paternal_grandmother_of_2", ":maternal_grandmother_of_1"),
	  (assign, ":relation_strength", 2),
	  (assign, ":relation_string", "str_cousin"),
	##diplomacy end+
   	(else_try),
   	  (eq, ":father_of_spouse_of_1", ":troop_2"),
   	  (assign, ":relation_strength", 5),
   	  (try_begin),
   	    (eq, ":gender_1", tf_female),
   	    (assign, ":relation_string", "str_daughterinlaw"),
   	  (else_try),
   	    (assign, ":relation_string", "str_soninlaw"),
   	  (try_end),
	(else_try),
	  (eq, ":father_of_spouse_of_2", ":troop_1"),
	  (assign, ":relation_strength", 5),
	  (assign, ":relation_string", "str_fatherinlaw"),
	(else_try),
	  (eq, ":mother_of_spouse_of_2", ":troop_1"),
	  (neq, ":mother_of_spouse_of_2", "trp_player"), #May be necessary if mother for troops not set to -1
	  (assign, ":relation_strength", 5),
	  (assign, ":relation_string", "str_motherinlaw"),

	(else_try),
	  #(gt, ":father_of_spouse_of_1", -1), #necessary #dplmc+ replaced
	  (neq, ":father_of_spouse_of_1", -1), #dplmc+ added
	  (eq, ":father_of_spouse_of_1", ":father_of_2"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_sisterinlaw"),
	  (else_try),
	    (assign, ":relation_string", "str_brotherinlaw"),
	  (try_end),
	(else_try),
	  #(gt, ":father_of_spouse_of_2", -1), #necessary #dplmc+ replaced
	  (neq, ":father_of_spouse_of_2", -1), #dplmc+ added
	  (eq, ":father_of_spouse_of_2", ":father_of_1"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_sisterinlaw"),
	  (else_try),
	    (assign, ":relation_string", "str_brotherinlaw"),
	  (try_end),
	(else_try),
#	  (gt, ":spouse_of_2", -1), #necessary to avoid bug #dplmc+ replaced
	  (neq, ":spouse_of_2", -1), #dplmc+ added
	  (troop_slot_eq, ":spouse_of_2", slot_troop_guardian, ":troop_1"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    #(eq, ":gender_1", tf_female),#dplmc+ replaced
	    (eq, ":gender_1", tf_female),#dplmc+ added
	    (assign, ":relation_string", "str_sisterinlaw"),
	  (else_try),
	    (assign, ":relation_string", "str_brotherinlaw"),
	  (try_end),
	(else_try),
	  #(gt, ":spouse_of_1", -1), #necessary to avoid bug #dplmc+ replaced
	  (neq, ":spouse_of_1", -1), #dplmc+ added
	  (troop_slot_eq, ":spouse_of_1", slot_troop_guardian, ":troop_2"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_sisterinlaw"),
	  (else_try),
	    (assign, ":relation_string", "str_brotherinlaw"),
	  (try_end),
	(else_try),
	  #grandchild
	  (neq, ":troop_2", -1),
	   (this_or_next|eq, ":paternal_grandfather_of_1", ":troop_2"),
	   (this_or_next|eq, ":maternal_grandfather_of_1", ":troop_2"),
	   (this_or_next|eq, ":paternal_grandmother_of_1", ":troop_2"),
		   (eq, ":maternal_grandmother_of_1", ":troop_2"),
	   (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_dplmc_granddaughter"),
	  (else_try),
	    (assign, ":relation_string", "str_dplmc_grandson"),
	  (try_end),
	(else_try),
	   #grandparent
	   (neq, ":troop_1", -1),
	   (this_or_next|eq, ":paternal_grandfather_of_2", ":troop_1"),
	   (this_or_next|eq, ":maternal_grandfather_of_2", ":troop_1"),
	   (this_or_next|eq, ":paternal_grandmother_of_2", ":troop_1"),
		   (eq, ":maternal_grandmother_of_2", ":troop_1"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (assign, ":relation_string", "str_dplmc_grandmother"),
	  (else_try),
	    (assign, ":relation_string", "str_dplmc_grandfather"),
	  (try_end),
	(try_end),
	##diplomacy start+
	##Add relations for rulers not already encoded
	(try_begin),
		(eq, ":relation_strength", 0),
		(neq, ":troop_1", ":troop_2"),
		(try_begin),
			#Lady Isolla of Suno's father King Esterich was King Harlaus's cousin,
			#making them first cousins once removed.  Assign a weight of "1"
			#to this (for reference, the lowest value normally given in Native is 2).
			(this_or_next|eq, ":troop_1", "trp_kingdom_1_lord"),
			    (eq, ":troop_1", "trp_kingdom_1_pretender"),
			(this_or_next|eq, ":troop_2", "trp_kingdom_1_lord"),
			    (eq, ":troop_2", "trp_kingdom_1_pretender"),
			(assign, ":relation_strength", 1),
			(assign, ":relation_string", "str_cousin"),
		(else_try),
			#Prince Valdym's uncle was Regent Burelek, father of King Yaroglek,
			#making the two of them first cousins.
			(this_or_next|eq, ":troop_1", "trp_kingdom_2_lord"),
			    (eq, ":troop_1", "trp_kingdom_2_pretender"),
			(this_or_next|eq, ":troop_2", "trp_kingdom_2_lord"),
				(eq, ":troop_2", "trp_kingdom_2_pretender"),
			(assign, ":relation_strength", 2),
			(assign, ":relation_string", "str_cousin"),
		(else_try),
			#Sanjar Khan and Dustum Khan were both sons of Janakir Khan
			#(although by different mothers) making them half-brothers.
			(this_or_next|eq, ":troop_1", "trp_kingdom_3_lord"),
			    (eq, ":troop_1", "trp_kingdom_3_pretender"),
			(this_or_next|eq, ":troop_2", "trp_kingdom_3_lord"),
				(eq, ":troop_2", "trp_kingdom_3_pretender"),
			(assign, ":relation_strength", 10),
			(assign, ":relation_string", "str_dplmc_half_brother"),
			#Adjust their parentage to make this work automatically
			(try_begin),
		      	(troop_slot_eq, ":troop_1", slot_troop_father, -1),
				(troop_slot_eq, ":troop_2", slot_troop_father, -1),
				#Set their "father" slot to a number guaranteed not to have spurious collisions
				(store_mul, ":janakir_khan", "trp_kingdom_3_lord", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),#defined in module_constants.py
				(val_add, ":janakir_khan", DPLMC_VIRTUAL_RELATIVE_FATHER_OFFSET),#defined in module_constants.py
				(troop_set_slot, ":troop_1", slot_troop_father, ":janakir_khan"),
				(troop_set_slot, ":troop_2", slot_troop_father, ":janakir_khan"),
				#Differentiate their mothers, so they are half-brothers instead of full-brothers
				(try_begin),
					(troop_slot_eq, ":troop_1", slot_troop_mother, -1),
					(store_mul, reg0, ":troop_1", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),
					(val_add, reg0, DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),
					(troop_set_slot, ":troop_1", slot_troop_mother, reg0),
				(try_end),
				(try_begin),
					(troop_slot_eq, ":troop_2", slot_troop_mother, -1),
					(store_mul, reg0, ":troop_2", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),
					(val_add, reg0, DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),
					(troop_set_slot, ":troop_2", slot_troop_mother, reg0),
				(try_end),
			(try_end),
		(try_end),
	(try_end),
	##Add uncles and aunts by marriage.
	##In Native, the relation strength for blood uncles/aunts is 4, and for cousins is 2.
	##In light of this I've decided to set the relation strength for aunts/uncles by marriage to 2.
	(try_begin),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_1 is married to a sibling of one of troop_2's parents, pt. 1
		(ge, ":spouse_of_1", 0),
		(neg|troop_slot_eq, ":spouse_of_1", slot_troop_father, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_1", slot_troop_father, ":paternal_grandfather_of_2"),
			(troop_slot_eq, ":spouse_of_1", slot_troop_father, ":maternal_grandfather_of_2"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(assign, ":relation_string", "str_aunt"),
		(else_try),
			(assign, ":relation_string", "str_uncle"),
		(try_end),
	(else_try),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_1 is married to a sibling of one of troop_2's parents, pt. 2
		(ge, ":spouse_of_1", 0),
		(neg|troop_slot_eq, ":spouse_of_1", slot_troop_mother, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_1", slot_troop_mother, ":paternal_grandmother_of_2"),
			(troop_slot_eq, ":spouse_of_1", slot_troop_mother, ":maternal_grandmother_of_2"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(assign, ":relation_string", "str_aunt"),
		(else_try),
			(assign, ":relation_string", "str_uncle"),
		(try_end),
	(else_try),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_2 is married to a sibling of one of troop_1's parents, pt. 1
		(ge, ":spouse_of_2", 0),
		(neg|troop_slot_eq, ":spouse_of_2", slot_troop_father, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_2", slot_troop_father, ":paternal_grandfather_of_1"),
			(troop_slot_eq, ":spouse_of_2", slot_troop_father, ":maternal_grandfather_of_1"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(assign, ":relation_string", "str_niece"),
		(else_try),
			(assign, ":relation_string", "str_nephew"),
		(try_end),
	(else_try),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_2 is married to a sibling of one of troop_1's parents, pt. 2
		(ge, ":spouse_of_2", 0),
		(neg|troop_slot_eq, ":spouse_of_2", slot_troop_mother, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_2", slot_troop_mother, ":paternal_grandmother_of_1"),
			(troop_slot_eq, ":spouse_of_2", slot_troop_mother, ":maternal_grandmother_of_1"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(assign, ":relation_string", "str_niece"),
		(else_try),
			(assign, ":relation_string", "str_nephew"),
		(try_end),
	(try_end),

	(try_begin),
		(this_or_next|neg|troop_is_hero, ":troop_1"),
		(neg|troop_is_hero, ":troop_2"),
		(assign, ":relation_string", "str_no_relation"),
		(assign, ":relation_strength", 0),
	(try_end),

	(assign, reg0, ":relation_strength"),
	(assign, reg1, ":relation_string"),
	]),

##"script_cf_dplmc_faction_has_bias_against_gender"
##
## Helper function that does something specific that I want in
## script_dplmc_troop_get_family_relation_to_troop.
##
## Gets the slot value, but for troops that aren't trp_player
## and are not within (heroes_begin, heroes_end), values of "0"
## are transformed to -1.  Also gives a result of -1 (instead of
## an error) for negative troop IDs, which is what I want in
## this situation (otherwise I'd be explicitly checking this and
## setting the result to -1 if it was bad).
##
## Also, values equal to "active_npcs_including_player_begin" are
## transformed to "trp_player" (i.e. 0), to allow storing that
## value.
##
##INPUT:  arg1   :troop_1
##        arg2   :troop_2
##        arg3   :slot_no
##
##OUTPUT: reg0   value of slot for troop_1, or -1
##        reg1   value of slot for troop_2, or -1
("dplmc_helper_get_troop1_troop2_family_slot_aux",
	[
		(store_script_param, ":troop_1", 1),
		(store_script_param, ":troop_2", 2),
		(store_script_param, ":slot_no", 3),

		#(1) Get the value for the first troop into reg0
		(try_begin),
			#Negative numbers are placeholders for invalid family members
			(lt, ":troop_1", 0),
			(assign, reg0, -1),
		(else_try),
			#For active_npcs_including_player_begin, use the family slot from trp_player
			(eq, ":troop_1", active_npcs_including_player_begin),
			(troop_get_slot, reg0, "trp_player", ":slot_no"),
		(else_try),
			#Otherwise get the family member slot
			(troop_get_slot, reg0, ":troop_1", ":slot_no"),
			#However, for non-heroes, the memory might not be initialized,
			#so don't take a value of 0 at face-value.
			(eq, reg0, 0),
			(neg|is_between, ":troop_1", heroes_begin, heroes_end),
			(neq, ":troop_1", "trp_player"),
			(assign, reg0, -1),
		(try_end),

		#Translate from active_npcs_including_player_begin to trp_player
		(try_begin),
			(eq, reg0, active_npcs_including_player_begin),
			(assign, reg0, "trp_player"),
		(try_end),

		#(2) Get the value for the second troop into reg1
		(try_begin),
			#Negative numbers are placeholders for invalid family members
			(lt, ":troop_2", 0),
			(assign, reg1, -1),
		(else_try),
			#For active_npcs_including_player_begin, use the family slot from trp_player
			(eq, ":troop_2", active_npcs_including_player_begin),
			(troop_get_slot, reg1, "trp_player", ":slot_no"),
		(else_try),
			#Otherwise get the family member slot
			(troop_get_slot, reg1, ":troop_2", ":slot_no"),
			#However, for non-heroes, the memory might not be initialized,
			#so don't take a value of 0 at face-value.
			(eq, reg1, 0),
			(neg|is_between, ":troop_2", heroes_begin, heroes_end),
			(neq, ":troop_2", "trp_player"),
			(assign, reg1, -1),
		(try_end),

		#Translate from active_npcs_including_player_begin to trp_player
		(try_begin),
			(eq, reg1, active_npcs_including_player_begin),
			(assign, reg1, "trp_player"),
		(try_end),
	]),

	##"script_dplmc_estimate_center_weekly_income"
    ("dplmc_npc_morale",
      [
        (store_script_param_1, ":npc"),
        (store_script_param_2, ":mode"),
        (try_begin), #if we actually care
          (eq, ":mode", 1),
          (call_script, "script_npc_morale", ":npc"),
        (else_try), #we just want the numbers
          (troop_get_slot, ":morality_grievances", ":npc", slot_troop_morality_penalties),
          (troop_get_slot, ":personality_grievances", ":npc", slot_troop_personalityclash_penalties),
          (party_get_morale, ":party_morale", "p_main_party"),

          (store_sub, ":troop_morale", ":party_morale", ":morality_grievances"),
          (val_sub, ":troop_morale", ":personality_grievances"),
          (val_add, ":troop_morale", 50),

          # (assign, reg8, ":troop_morale"),

          (val_mul, ":troop_morale", 3),
          (val_div, ":troop_morale", 4),
          (val_clamp, ":troop_morale", 0, 100),
          (assign, reg0, ":troop_morale"),
        (try_end),
    ]),

    #script_build_background_answer_story
  ("cf_has_companion_emissary",
    [
    (assign, ":companion_found", companions_end),
    (try_for_range, ":emissary", companions_begin, companions_end),
      (main_party_has_troop, ":emissary"),
      (assign, ":companion_found", companions_begin),
    (try_end),
    (neq, ":companion_found", companions_end),
    ]),

  #script_get_chest_troop fetches the appropriate placeholder for player storage
]
