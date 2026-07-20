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

randomly_start_war_peace_new_scripts = [
# script_make_kingdom_hostile_to_player
# Input: arg1 = initializing_war_peace_cond (1 = true, 0 = false)
# Output: none
#Aims to introduce a slightly simpler system in which the AI kings' reasoning could be made more  transparent to the player. At the start of the game, this may lead to less variation in outcomes, though
("randomly_start_war_peace_new",
    [
    (store_script_param_1, ":initializing_war_peace_cond"),

	(assign, ":players_kingdom_at_peace", 0), #if the player kingdom is at peace, then create an enmity
	(try_begin),
		(is_between, "$players_kingdom", "fac_kingdom_1", kingdoms_end),
		(assign, ":players_kingdom_at_peace", 1),
	(try_end),

	##diplomacy start+
	#Introduce some minor variation by changing the order in which factions consider things.
	##OLD:
    #(try_for_range, ":cur_kingdom", "fac_kingdom_1", kingdoms_end),
    #    (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
	#
	#	(try_for_range, ":cur_kingdom_2", kingdoms_begin, kingdoms_end),
	##NEW:
	(store_random_in_range, ":random_offset_1", "fac_kingdom_1", kingdoms_end),
	(val_sub, ":random_offset_1", "fac_kingdom_1"),
	(try_for_range, ":cur_kingdom", "fac_kingdom_1", kingdoms_end),
		(val_add, ":cur_kingdom", ":random_offset_1"),
		(try_begin),
			(ge, ":cur_kingdom", kingdoms_end),
			(val_sub, ":cur_kingdom", kingdoms_end),
			(val_add, ":cur_kingdom", "fac_kingdom_1"),
		(try_end),
		(faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
		(store_random_in_range, ":random_offset_2", kingdoms_begin, kingdoms_end),
		(val_sub, ":random_offset_2", kingdoms_begin),
		(try_for_range, ":cur_kingdom_2", kingdoms_begin, kingdoms_end),
			(val_add, ":cur_kingdom_2", ":random_offset_2"),
			(try_begin),
				(ge, ":cur_kingdom_2", kingdoms_end),
				(val_sub, ":cur_kingdom_2", kingdoms_end),
				(val_add, ":cur_kingdom_2", kingdoms_begin),
			(try_end),
	##diplomacy end+
			(neq, ":cur_kingdom", ":cur_kingdom_2"),
			(faction_slot_eq, ":cur_kingdom_2", slot_faction_state, sfs_active),

			(call_script, "script_npc_decision_checklist_peace_or_war", ":cur_kingdom", ":cur_kingdom_2", -1),
			(assign, ":kingdom_1_to_kingdom_2", reg0),

			(store_relation, ":cur_relation", ":cur_kingdom", ":cur_kingdom_2"),
			(try_begin),
				(lt, ":cur_relation", 0), #AT WAR

				(try_begin),
					(eq, ":cur_kingdom", "$players_kingdom"),
					(assign, ":players_kingdom_at_peace", 0),
				(try_end),

				(ge, ":kingdom_1_to_kingdom_2", 1),

        ##diplomacy begin
        (try_begin),
      	  (store_current_hours, ":cur_hours"),
          (faction_get_slot, ":faction_ai_last_decisive_event", ":cur_kingdom", slot_faction_ai_last_decisive_event),
          (store_sub, ":hours_since_last_decisive_event", ":cur_hours", ":faction_ai_last_decisive_event"),
          (ge, ":hours_since_last_decisive_event", 96), #wait 4 days until you conclude peace after war
        ##diplomacy end
          (try_begin),
            (eq, ":cur_kingdom_2", "fac_player_supporters_faction"),

            (store_mul, ":goodwill_level", ":kingdom_1_to_kingdom_2", 2),
            (store_random_in_range, ":random", 0, 20),
            (try_begin),
              (lt, ":random", ":goodwill_level"),
              (call_script, "script_add_notification_menu", "mnu_question_peace_offer", ":cur_kingdom", 0),
            (try_end),
          (else_try),
            (call_script, "script_npc_decision_checklist_peace_or_war", ":cur_kingdom_2", ":cur_kingdom", -1),
            (assign, ":kingdom_2_to_kingdom_1", reg0),
            (ge, ":kingdom_2_to_kingdom_1", 1),

            (store_mul, ":goodwill_level", ":kingdom_1_to_kingdom_2", ":kingdom_2_to_kingdom_1"),
            (store_random_in_range, ":random", 0, 20),
            (lt, ":random", ":goodwill_level"),

            (try_begin),
              (eq, "$g_include_diplo_explanation", 0),
              (assign, "$g_include_diplo_explanation", ":cur_kingdom"),
              (str_store_string, s57, "str_s14"),
            (try_end),

            (call_script, "script_diplomacy_start_peace_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
          (try_end),
        ##diplomacy begin
        (try_end),
        ##diplomacy end
			(else_try),
				(ge, ":cur_relation", 0), #AT PEACE

			    (call_script, "script_npc_decision_checklist_peace_or_war", ":cur_kingdom", ":cur_kingdom_2", -1),

				#negative, leans towards war/positive, leans towards peace
				(le, reg0, 0), #still no chance of war unless provocation, or at start of game

			    (assign, ":hostility", reg0),

			    (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":cur_kingdom", ":cur_kingdom_2"),
			    (le, reg0, 0), #no truce

				(val_add, ":hostility", reg0), #increase hostility if there is a provocation

				(val_sub, ":hostility", 1), #greater chance at start of game
				(val_add, ":hostility", ":initializing_war_peace_cond"), #this variable = 1 after the start

				(store_mul, ":hostility_squared", ":hostility", ":hostility"),
				(store_random_in_range, ":random", 0, 50),

        ##diplomacy begin
        #check for pact and lower probability if there is one
        (try_for_range, ":third_kingdom", kingdoms_begin, kingdoms_end),
          (neq, ":third_kingdom", ":cur_kingdom"),
          (neq, ":third_kingdom", ":cur_kingdom_2"),
		  ##nested diplomacy start+  Faction must be active
		  (faction_slot_eq, ":third_kingdom", slot_faction_state, sfs_active),
		  ##nested diplomacy end+

          (store_relation, ":cur_relation", ":cur_kingdom_2", ":third_kingdom"),
    			(ge, ":cur_relation", 0), #AT PEACE

          (store_add, ":truce_slot", ":third_kingdom", slot_faction_truce_days_with_factions_begin),
      		(val_sub, ":truce_slot", kingdoms_begin),
      		(faction_get_slot, ":truce_days", ":cur_kingdom_2", ":truce_slot"),
      		##nested diplomacy start+ replace "40" with a named constant
      		#(gt, ":truce_days", 40),
      		(gt, ":truce_days", dplmc_treaty_defense_days_expire),
      		##nested diplomacy end+
      		(store_div, ":hostility_change", ":truce_days", 20),
      		(val_sub, ":hostility_squared", ":hostility_change"),
        (try_end),
        ##diplomacy end

			    (lt, ":random", ":hostility_squared"),

				(try_begin),
					(eq, "$g_include_diplo_explanation", 0),
					(assign, "$g_include_diplo_explanation", ":cur_kingdom"),
					(str_store_string, s57, "str_s14"),
				(try_end),
                (call_script, "script_diplomacy_start_war_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),

				(try_begin), #do some war damage for
					(eq, ":initializing_war_peace_cond", 0),
					(store_random_in_range, ":war_damage_inflicted", 10, 120),
					(store_add, ":slot_war_damage_inflicted", ":cur_kingdom", slot_faction_war_damage_inflicted_on_factions_begin),
					(val_sub, ":slot_war_damage_inflicted", kingdoms_begin),
					(faction_set_slot, ":cur_kingdom_2",  ":slot_war_damage_inflicted", ":war_damage_inflicted"),

					(store_add, ":slot_war_damage_inflicted", ":cur_kingdom_2", slot_faction_war_damage_inflicted_on_factions_begin),
					(val_sub, ":slot_war_damage_inflicted", kingdoms_begin),
					(faction_set_slot, ":cur_kingdom", ":slot_war_damage_inflicted", ":war_damage_inflicted"),
				(try_end),
      ##diplomacy begin
      (else_try),
        (ge, ":cur_relation", 0), #AT PEACE
        (ge, ":kingdom_1_to_kingdom_2", 1),

        #(assign, ":barrier", 2),
        (store_add, ":faction1_to_faction2_slot", ":cur_kingdom_2", dplmc_slot_faction_attitude_begin),
        (party_get_slot, ":barrier",":cur_kingdom", ":faction1_to_faction2_slot"),

        (try_for_range, ":third_kingdom", kingdoms_begin, kingdoms_end),
          (neq, ":third_kingdom", ":cur_kingdom"),
          (neq, ":third_kingdom", ":cur_kingdom_2"),

          (store_add, ":slot_truce_days", ":cur_kingdom", slot_faction_truce_days_with_factions_begin),
          (val_sub, ":slot_truce_days", kingdoms_begin),
          (faction_get_slot, ":truce_days", ":third_kingdom", ":slot_truce_days"),
          ##nested diplomacy start+ change to use constants
          #(gt, ":truce_days", 10),
          (gt, ":truce_days", dplmc_treaty_truce_days_half_done),
          ##nested diplomacy end+
          (val_sub, ":barrier", 1),

          (try_begin), #debug
            (eq, "$cheat_mode", 1),
            (str_store_faction_name, s5, ":cur_kingdom"),
            (str_store_faction_name, s6, ":third_kingdom"),
            (str_store_faction_name, s7, ":cur_kingdom_2"),
            (display_message, "@{!}DEBUG: {s5} has truce with {s6}. Pact with {s7} is harder!"),
          (try_end),

        (try_end),

        (val_max, ":barrier", 0),
        (store_random_in_range, ":random", 0, 130),
        (le, ":random", ":barrier"),

        (store_add, ":slot_truce_days", ":cur_kingdom", slot_faction_truce_days_with_factions_begin),
        (val_sub, ":slot_truce_days", kingdoms_begin),
        (faction_get_slot, ":truce_days", ":cur_kingdom_2", ":slot_truce_days"),

        (store_random_in_range, ":random", 0, 3),
        (assign, ":continue", 0),
        (try_begin),
          ##nested diplomacy start+ change to use constants
          #(is_between, ":truce_days", 0, 50),
          (is_between, ":truce_days", 0, dplmc_treaty_defense_days_half_done),#50 = halfway from a defensive alliance to a trade treaty
          ##nested diplomacy end+
          (ge, ":cur_relation", 20),
          (try_begin),
            (le, ":random", 0), #1/3 for alliance, defensive
            (assign, ":continue", 1),
          (try_end),
        (else_try),
          ##nested diplomacy start+ change to use constants
          #(is_between, ":truce_days", 0, 10),
          (is_between, ":truce_days", 0, dplmc_treaty_truce_days_half_done),#10 = halfway done with a truce
          ##nested diplomacy end+
          (ge, ":cur_relation", 10),
          (try_begin),
            (le, ":random", 1), #2/3 # for trade
            (assign, ":continue", 1),
          (try_end),
        (else_try),
          (assign, ":continue", 1),  # for non-aggression
        (try_end),
        (eq, ":continue", 1),

        (try_begin),
		  ##nested diplomacy start+
		  (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":cur_kingdom_2"),
		  (this_or_next|ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		  ##nested diplomacy end+
          (eq, ":cur_kingdom_2", "fac_player_supporters_faction"),
          (ge, ":kingdom_1_to_kingdom_2", 1),

          (try_begin),
            ##nested diplomacy start+ change to use constants
            #(is_between, ":truce_days", 20, 50),
            (is_between, ":truce_days", dplmc_treaty_trade_days_expire, dplmc_treaty_defense_days_half_done),
            ##nested diplomacy end+
            (ge, ":cur_relation", 30),
            (faction_slot_eq, ":cur_kingdom", slot_faction_recognized_player, 1), #recognized us
            (call_script, "script_add_notification_menu", "mnu_dplmc_question_alliance_offer", ":cur_kingdom", 0),
          (else_try),
            ##nested diplomacy start+ change to use constants
            #(is_between, ":truce_days", 0, 30), #you need a non-aggression or trade aggreement for an defensive pact
            (is_between, ":truce_days", 0, dplmc_treaty_trade_days_half_done),
            ##nested diplomacy end+
            (ge, ":cur_relation", 20),
            (faction_slot_eq, ":cur_kingdom", slot_faction_recognized_player, 1), #recognized us
            (call_script, "script_add_notification_menu", "mnu_dplmc_question_defensive_offer", ":cur_kingdom", 0),
          (else_try),
            ##nested diplomacy start+ change to use constants
            #(is_between, ":truce_days", 0, 10),
            (is_between, ":truce_days", 0, dplmc_treaty_truce_days_half_done),
            ##diplomacy end+
            (ge, ":cur_relation", 10),
            (faction_slot_eq, ":cur_kingdom", slot_faction_recognized_player, 1), #recognized us
            (call_script, "script_add_notification_menu", "mnu_dplmc_question_trade_offer", ":cur_kingdom", 0),
          (else_try),
            (eq, ":truce_days", 0),
            (ge, ":cur_relation", 5),
            (call_script, "script_add_notification_menu", "mnu_dplmc_question_nonaggression_offer", ":cur_kingdom", 0),
          (try_end),
        (else_try),
          (ge, ":kingdom_1_to_kingdom_2", 1),

          (call_script, "script_npc_decision_checklist_peace_or_war", ":cur_kingdom_2", ":cur_kingdom", -1),
          (assign, ":kingdom_2_to_kingdom_1", reg0),
          (ge, ":kingdom_2_to_kingdom_1", 1),

          (try_begin),
            ##nested diplomacy start+ change to use constants
            #(is_between, ":truce_days", 20, 50),
            (is_between, ":truce_days", dplmc_treaty_trade_days_expire, dplmc_treaty_defense_days_half_done),
            ##nested diplomacy end+
            (ge, ":cur_relation", 30),
            (call_script, "script_dplmc_start_alliance_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
          (else_try),
            ##nested diplomacy start+ change to use constants
            #(is_between, ":truce_days", 0, 30), #you need a non-aggression or trade aggreement for an defensive pact
            (is_between, ":truce_days", 0, dplmc_treaty_trade_days_half_done),
            ##nested diplomacy end+
            (ge, ":cur_relation", 20),
            (call_script, "script_dplmc_start_defensive_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
          (else_try),
            ##nested diplomacy start+ change to use constants
            #(is_between, ":truce_days", 0, 10),
            (is_between, ":truce_days", 0, dplmc_treaty_truce_days_half_done),
            ##nested diplomacy end+
            (ge, ":cur_relation", 10),
            (call_script, "script_dplmc_start_trade_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
          (else_try),
            (eq, ":truce_days", 0),
            (call_script, "script_dplmc_start_nonaggression_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
          (try_end),
        (try_end),
      ##diplomacy end
      (try_end),
		(try_end),
	(try_end),

	(try_begin),
		(eq, ":players_kingdom_at_peace", 1),
		(val_add, "$players_kingdom_days_at_peace", 1),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(assign, reg3, "$players_kingdom_days_at_peace"),
			(display_message, "@{!}DEBUG -- Player's kingdom has had {reg3} days of peace"),
		(try_end),
	(else_try),
		(assign, "$players_kingdom_days_at_peace", 0),
	(try_end),

     ])
]
