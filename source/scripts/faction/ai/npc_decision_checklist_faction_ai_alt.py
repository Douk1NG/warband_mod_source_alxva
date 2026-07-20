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

npc_decision_checklist_faction_ai_alt_scripts = [
(
	"npc_decision_checklist_faction_ai_alt", #This is called from within decide_faction_ai, or from
	[
		(store_script_param, ":troop_no", 1),

		(store_faction_of_troop, ":faction_no", ":troop_no"),

		(str_store_troop_name, s4, ":troop_no"),
		(str_store_faction_name, s33, ":faction_no"),
		(try_begin),
			(eq, "$cheat_mode", 1),
		    (display_message, "@{!}DEBUG -- {s4} produces a faction strategy for {s33}"),
		(try_end),

		#INFORMATIONS COLLECTING STEP 0: Here we obtain general information about current faction like how much parties that faction has, which lord is the marshall, current ai state and current ai target object
		#(faction_get_slot, ":faction_strength", ":faction_no", slot_faction_number_of_parties),
		(faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
		(faction_get_slot, ":current_ai_state", ":faction_no", slot_faction_ai_state),
		(faction_get_slot, ":current_ai_object", ":faction_no", slot_faction_ai_object),

		(assign, ":marshal_party", -1),
		(assign, ":marshal_party_strength", 0),

		(try_begin),
		  (gt, ":faction_marshal", 0),
		  (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
		  (party_is_active, ":marshal_party"),
		  (party_get_slot, ":marshal_party_itself_strength", ":marshal_party", slot_party_cached_strength),
		  (party_get_slot, ":marshal_party_follower_strength", ":marshal_party", slot_party_follower_strength),
		  (store_add, ":marshal_party_strength", ":marshal_party_itself_strength", ":marshal_party_follower_strength"),
	    (try_end),

	    #INFORMATIONS COLLECTING STEP 1: Here we are learning how much hours past from last offensive situation/feast concluded/current state started
	    (store_current_hours, ":hours_since_last_offensive"),
	    (faction_get_slot, ":last_offensive_time", ":faction_no", slot_faction_last_offensive_concluded),
	    (val_sub, ":hours_since_last_offensive", ":last_offensive_time"),

	    (store_current_hours, ":hours_since_last_feast_start"),
	    (faction_get_slot, ":last_feast_time", ":faction_no", slot_faction_last_feast_start_time),
	    (val_sub, ":hours_since_last_feast_start", ":last_feast_time"),

	    (store_current_hours, ":hours_at_current_state"),
	    (faction_get_slot, ":current_state_started", ":faction_no", slot_faction_ai_current_state_started),
	    (val_sub, ":hours_at_current_state", ":current_state_started"),

	    (store_current_hours, ":hours_since_last_faction_rest"),
	    (faction_get_slot, ":last_rest_time", ":faction_no", slot_faction_ai_last_rest_time),
	    (val_sub, ":hours_since_last_faction_rest", ":last_rest_time"),

	    (try_begin), #calculating ":last_offensive_time_score", this will be used in #11 and #12
	        (ge, ":hours_since_last_offensive", 1080), #more than 45 days (100p)
	        (assign, ":last_offensive_time_score", 100),
	    (else_try),
	        (ge, ":hours_since_last_offensive", 480), #more than 20 days (65p..99p)
	        (store_sub, ":last_offensive_time_score", ":hours_since_last_offensive", 480),
	        (val_div, ":last_offensive_time_score", 20),
	        (val_add, ":last_offensive_time_score", 64),
	    (else_try),
	        (ge, ":hours_since_last_offensive", 240), #more than 10 days (41p..64p)
	        (store_sub, ":last_offensive_time_score", ":hours_since_last_offensive", 240),
	        (val_div, ":last_offensive_time_score", 10),
	        (val_add, ":last_offensive_time_score", 40),
	    (else_try), #less than 10 days (0p..40p)
	        (store_div, ":last_offensive_time_score", ":hours_since_last_offensive", 6), #0..40
	    (try_end),

	    #INFORMATION COLLECTING STEP 3: Here we are finding the most threatened center
	    (call_script, "script_find_center_to_defend", ":troop_no"),
	    (assign, ":most_threatened_center", reg0),
	    (assign, ":threat_danger_level", reg1),
	    (assign, ":enemy_strength_near_most_threatened_center", reg2), #NOTE! This will be off by as much as 50%

	    #INFORMATION COLLECTING STEP 4: Here we are finding number of vassals who are already following the marshal, and the assigned vassal ratio of current faction.
	    (assign, ":vassals_already_assembled", 0),
	    (assign, ":total_vassals", 0),
		##diplomacy start+ add support for promoted kingdom ladies
	    #(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
		(try_for_range, ":lord", heroes_begin, heroes_end),
			(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
				(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
	        (store_faction_of_troop, ":lord_faction", ":lord"),
	        (eq, ":lord_faction", ":faction_no"),
	        (troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
	        (party_is_active, ":led_party"),
	        (val_add, ":total_vassals", 1),

	        (party_slot_eq, ":led_party", slot_party_ai_state, spai_accompanying_army),
	        (party_slot_eq, ":led_party", slot_party_ai_object, ":marshal_party"),

	        (party_is_active, ":marshal_party"),
	        (store_distance_to_party_from_party, ":distance_to_marshal", ":led_party", ":marshal_party"),
	        (lt, ":distance_to_marshal", 15),
	        (val_add, ":vassals_already_assembled", 1),
	    (try_end),
	    (assign, ":ratio_of_vassals_assembled", -1),
	    (try_begin),
	        (gt, ":total_vassals", 0),
	        (store_mul, ":ratio_of_vassals_assembled", ":vassals_already_assembled", 100),
	        (val_div, ":ratio_of_vassals_assembled", ":total_vassals"),
	    (try_end),

	    #50% of vassals means that the campaign hour limit is ten days
	    (store_mul, ":campaign_hour_limit", ":ratio_of_vassals_assembled", 3),
	    (val_add, ":campaign_hour_limit", 90),

	    #To Steve - I understand your concern about some marshals will gather army and some will not be able to find any valueable center to attack after gathering,
	    #and these marshals will be questioned by other marshals ext. This is ok but if we search for a target without adding all other vassals what if
	    #AI cannot find any target for long time because of its low power ratio if enemy cities are equal defended? Do not forget if we do not count other vassals in
	    #faction while making target search we can only add marshal army's power and vassals around him. And if there is any threat in our centers even it is smaller,
	    #its threat_danger_level will be more than target_value_level if marshal new started gathering for ofensive. Because we only assume marshal and around vassals
	    #will join attack. And in our scenarios currently there are less vassals are around him. So power ratio will be low and any small threat will be enought to stop
	    #an offensive. Then when players finds out this they periodically will take under siege to enemy's any center and they will be saved from any kind of newly started
	    #offensive they will be faced. So we have to calculate both attack levels and select highest one to compare with threat level. Please do not change this part.

		(try_begin),
		  (ge, ":faction_marshal", 0),
		  (ge, ":marshal_party", 0),
		  (party_is_active, ":marshal_party"),

		  (call_script, "script_party_count_fit_for_battle", ":marshal_party"),
		  (assign, ":number_of_fit_soldiers_in_marshal_party", reg0),
		  (ge, ":number_of_fit_soldiers_in_marshal_party", 40),

		  (call_script, "script_find_center_to_attack_alt", ":troop_no", 1, 0),
		  (assign, ":center_to_attack_all_vassals_included", reg0),
		  (assign, ":target_value_level_all_vassals_included", reg1),

		  (call_script, "script_find_center_to_attack_alt", ":troop_no", 1, 1),
		  (assign, ":center_to_attack_only_marshal_and_followers", reg0),
		  (assign, ":target_value_level_only_marshal_and_followers", reg1),
		(else_try),
		  (assign, ":target_value_level_all_vassals_included", 0),
		  (assign, ":target_value_level_only_marshal_and_followers", 0),
		  (assign, ":center_to_attack_all_vassals_included", -1),
		  (assign, ":center_to_attack_only_marshal_and_followers", -1),
		(try_end),

		(try_begin),
		  (ge, ":target_value_level_all_vassals_included", ":center_to_attack_only_marshal_and_followers"),
		  (assign, ":center_to_attack", ":center_to_attack_all_vassals_included"),
		  (assign, ":target_value_level", ":target_value_level_all_vassals_included"),
		(else_try),
		  (assign, ":center_to_attack", ":center_to_attack_only_marshal_and_followers"),
		  (assign, ":target_value_level", ":target_value_level_only_marshal_and_followers"),
		(try_end),

		(try_begin),
		  (eq, ":current_ai_state", sfai_attacking_center),
		  (val_mul, ":target_value_level", 3),
		  (val_div, ":target_value_level", 2),
		(try_end),

		(try_begin),
		  (eq, "$cheat_mode", 1),
		  (try_begin),
		    (is_between, ":center_to_attack", centers_begin, centers_end),
		    (str_store_party_name, s4, ":center_to_attack"),
		    (display_message, "@{!}Best offensive target {s4} has value level of {reg1}"),
		  (else_try),
		    (display_message, "@{!}No center found to attack"),
		  (try_end),

		  (try_begin),
		    (is_between, ":most_threatened_center", centers_begin, centers_end),
		    (str_store_party_name, s4, ":most_threatened_center"),
		    (assign, reg1, ":threat_danger_level"),
		    (display_message, "@{!}Best threat of {s4} has value level of {reg1}"),
		  (else_try),
		    (display_message, "@{!}No center found to defend"),
		  (try_end),
		(try_end),

		(try_begin),
		  (eq, "$cheat_mode", 1),

		  (try_begin),
  		    (is_between, ":most_threatened_center", centers_begin, centers_end),
 		    (str_store_party_name, s4, ":most_threatened_center"),
		    (assign, reg1, ":threat_danger_level"),
		    (display_message, "@Best threat of {s4} has value level of {reg1}"),
		  (else_try),
		    (display_message, "@No center found to defend"),
		  (try_end),
		(try_end),

	    (assign, "$g_target_after_gathering", -1),

	    (store_current_hours, ":hours"),
	    (try_begin),
	      (ge, ":target_value_level", ":threat_danger_level"),
	      (faction_set_slot, ":faction_no", slot_faction_last_safe_hours, ":hours"),
	    (try_end),
	    (faction_get_slot, ":last_safe_hours", ":faction_no", slot_faction_last_safe_hours),
	    (try_begin),
	      (eq, ":last_safe_hours", 0),
	      (faction_set_slot, ":faction_no", slot_faction_last_safe_hours, ":hours"),
	    (try_end),
	    (faction_get_slot, ":last_safe_hours", ":faction_no", slot_faction_last_safe_hours),
	    (store_sub, ":hours_since_days_defensive_started", ":hours", ":last_safe_hours"),
	    (str_store_faction_name, s7, ":faction_no"),

		(assign, ":at_peace_with_everyone", 1),
		(try_for_range, ":faction_at_war", kingdoms_begin, kingdoms_end),
			(store_relation, ":relation", ":faction_no", ":faction_at_war"),
			(lt, ":relation", 0),
			(assign, ":at_peace_with_everyone", 0),
		(try_end),


	    #INFORMATIONS ARE COLLECTED, NOW CHECK ALL POSSIBLE ACTIONS AND DECIDE WHAT TO DO	NEXT
		#Player marshal
		(try_begin), # a special case to end long-running feasts
			(eq, ":troop_no", "trp_player"),

			(eq, ":current_ai_state", sfai_feast),
			(ge, ":hours_at_current_state", 72),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),

			#Normally you are not supposed to set permanent values in this state, but this is a special case to end player-called feasts
			(assign, "$player_marshal_ai_state", sfai_default),
			(assign, "$player_marshal_ai_object", -1),
		(else_try), #another special state, to make player-called feasts last for a while when the player is the leader of the faction, but not the marshal
			(eq, "$players_kingdom", "fac_player_supporters_faction"),
			(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
			(neq, ":troop_no", "trp_player"),

			(eq, ":current_ai_state", sfai_feast),
			(le, ":hours_at_current_state", 48),

			(party_slot_eq, ":current_ai_object", slot_town_lord, "trp_player"),
			(store_faction_of_party, ":current_ai_object_faction", ":current_ai_object"),
			(eq, ":current_ai_object_faction", "$players_kingdom"),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":current_ai_object"),


		(else_try), #this is the main player marshal state
			(eq, ":troop_no", "trp_player"),

			(str_clear, s14),
			(assign, ":action", "$player_marshal_ai_state"),
			(assign, ":object", "$player_marshal_ai_object"),

	    #1-RESTING IF NEEDED
	    #If not currently attacking a besieging a center and vassals did not rest for long time, let them rest.
	    #If we do not take this part to toppest level, tired vassals already did not accept any order, so that
	    #faction cannot do anything already. So first let vassals rest if they need. Thats why it should be toppest.
		(else_try),
			(neq, ":current_ai_state", sfai_default),
			(neq, ":current_ai_state", sfai_feast),
			(party_is_active, ":marshal_party"),

			(party_slot_eq, ":marshal_party", slot_party_ai_state, spai_retreating_to_center),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),
			(str_store_string, s14, "str_the_enemy_temporarily_has_the_field"),

		(else_try),
		    (neq, ":current_ai_state", sfai_feast),

		    (assign, ":currently_besieging", 0),
		    (try_begin),
			    (eq, ":current_ai_state", sfai_attacking_center),
			    (is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
			    (party_get_slot, ":besieger_party", ":current_ai_object", slot_center_is_besieged_by),
			    (party_is_active, ":besieger_party"),
			    (store_faction_of_party, ":besieger_faction", ":besieger_party"),
			    (eq, ":besieger_faction", ":faction_no"),
			    (assign, ":currently_besieging", 1),
		    (try_end),

		    (assign, ":currently_defending_center", 0),
	        (try_begin),
		        (eq, ":current_ai_state", sfai_attacking_enemies_around_center),
		        (gt, ":marshal_party", 0),
		        (party_is_active, ":marshal_party"),

				(assign, ":besieged_center", -1),
				(try_begin),
					(party_slot_eq, ":marshal_party", slot_party_ai_state, spai_holding_center), #if commander is holding a center
					(party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object), #get commander's ai object (center they are holding)
					(party_get_battle_opponent, ":besieger_enemy", ":marshal_object"), #get this object's battle opponent
					(ge, ":besieger_enemy", 0),
					(assign, ":besieged_center", ":marshal_object"),
				(else_try),
					(party_slot_eq, ":marshal_party", slot_party_ai_state, spai_engaging_army), #if commander is engaging an army
					(party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object), #get commander's ai object (army which they engaded)
					(ge, ":marshal_object", 0), #if commander has an object
					(neg|is_between, ":marshal_object", centers_begin, centers_end), #if this object is not a center, so it is a party
					(party_is_active, ":marshal_object"),
					(party_get_battle_opponent, ":besieged_center", ":marshal_object"), #get this object's battle opponent
				(try_end),

				(eq, ":besieged_center", ":current_ai_object"),
				(assign, ":currently_defending_center", 1),
	        (try_end),

		    (eq, ":currently_besieging", 0),
		    (eq, ":currently_defending_center", 0),
		    (ge, ":hours_since_last_faction_rest", 1240),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),
			(str_store_string, s14, "str_the_vassals_are_tired_we_let_them_rest_for_some_time"),

	  #2-DEFENSIVE ACTIONS : GATHERING ARMY FOR DEFENDING
          (else_try),
            (party_is_active, ":marshal_party"),
			(eq, ":at_peace_with_everyone", 0),

            (is_between, ":most_threatened_center", centers_begin, centers_end),
            (this_or_next|eq, ":current_ai_state", sfai_default),    #MOTO not going to attack anyway
            (this_or_next|eq, ":current_ai_state", sfai_feast),    #MOTO not going to attack anyway (THIS is the emergency to stop feast)
            (gt, ":threat_danger_level", ":target_value_level"),

            (assign, ":continue_gathering", 0),
            (assign, ":start_gathering", 0),

            (try_begin),
              (is_between, ":most_threatened_center", villages_begin, villages_end),

              (assign, ":continue_gathering", 0),
            (else_try),
              (try_begin),
                (lt, ":hours_since_days_defensive_started", 3),
                (assign, ":multiplier", 150),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 6),
                (assign, ":multiplier", 140),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 9),
                (assign, ":multiplier", 132),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 12),
                (assign, ":multiplier", 124),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 15),
                (assign, ":multiplier", 118),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 18),
                (assign, ":multiplier", 114),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 21),
                (assign, ":multiplier", 110),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 24),
                (assign, ":multiplier", 106),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 27),
                (assign, ":multiplier", 102),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 31),
                (assign, ":multiplier", 98),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 34),
                (assign, ":multiplier", 94),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 37),
                (assign, ":multiplier", 90),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 40),
                (assign, ":multiplier", 86),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 43),
                (assign, ":multiplier", 82),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 46),
                (assign, ":multiplier", 79),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 49),
                (assign, ":multiplier", 76),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 52),
                (assign, ":multiplier", 73),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 56),
                (assign, ":multiplier", 70),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 60),
                (assign, ":multiplier", 68),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 66),
                (assign, ":multiplier", 66),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 72),
                (assign, ":multiplier", 64),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 80),
                (assign, ":multiplier", 62),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 90),
                (assign, ":multiplier", 60),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 100),
                (assign, ":multiplier", 58),
              (else_try),
                (assign, ":multiplier", 56),
              (try_end),

              (store_mul, ":enemy_strength_multiplied", ":enemy_strength_near_most_threatened_center", ":multiplier"),
              (val_div, ":enemy_strength_multiplied", 100),

              (try_begin),
                (lt, ":marshal_party_strength", ":enemy_strength_multiplied"),
                (assign, ":continue_gathering", 1),
              (try_end),
            (else_try),
              (eq, ":current_ai_state", sfai_attacking_enemies_around_center),
              (neq, ":most_threatened_center", ":current_ai_object"),

              (assign, ":marshal_is_already_defending_a_center", 0),
              (try_begin),
                (gt, ":marshal_party", 0),
                (party_is_active, ":marshal_party"),

                (assign, ":besieged_center", -1),
                (try_begin),
                  (party_slot_eq, ":marshal_party", slot_party_ai_state, spai_holding_center), #if commander is holding a center
                  (party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object), #get commander's ai object (center they are holding)
                  (party_get_battle_opponent, ":besieger_enemy", ":marshal_object"), #get this object's battle opponent
                  (ge, ":besieger_enemy", 0),
                  (assign, ":besieged_center", ":marshal_object"),
                (else_try),
                  (party_slot_eq, ":marshal_party", slot_party_ai_state, spai_engaging_army), #if commander is engaging an army
                  (party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object), #get commander's ai object (army which they engaded)
                  (ge, ":marshal_object", 0), #if commander has an object
                  (neg|is_between, ":marshal_object", centers_begin, centers_end), #if this object is not a center, so it is a party
				  (party_is_active, ":marshal_object"),
                  (party_get_battle_opponent, ":besieged_center", ":marshal_object"), #get this object's battle opponent
                (try_end),

                (eq, ":besieged_center", ":current_ai_object"),

                (assign, ":marshal_is_already_defending_a_center", 1),
              (try_end),

              (eq, ":marshal_is_already_defending_a_center", 0),

              (store_mul, ":enemy_strength_multiplied", ":enemy_strength_near_most_threatened_center", 80),
              (val_div, ":enemy_strength_multiplied", 100),
              (lt, ":marshal_party_strength", ":enemy_strength_multiplied"),

              (this_or_next|is_between, ":most_threatened_center", walled_centers_begin, walled_centers_end),
              (neq, ":faction_no", "$players_kingdom"),

              (assign, ":start_gathering", 1),
            (try_end),

            (this_or_next|eq, ":continue_gathering", 1),
            (eq, ":start_gathering", 1),

            (assign, ":action", sfai_gathering_army),
            (assign, ":object", -1),
            (str_store_party_name, s21, ":most_threatened_center"),
            (str_store_string, s14, "str_we_should_prepare_to_defend_s21_but_we_should_gather_our_forces_until_we_are_strong_enough_to_engage_them"),

            (try_begin),
              (eq, ":faction_no", "$players_kingdom"),
              (assign, "$g_gathering_reason", ":most_threatened_center"),
            (try_end),

	    #3-DEFENSIVE ACTIONS : RIDE TO BREAK ENEMY SIEGE / DEFEAT ENEMIES NEAR OUR CENTER
		(else_try),
			(party_is_active, ":marshal_party"),
			(is_between, ":most_threatened_center", walled_centers_begin, walled_centers_end),
                        (this_or_next|eq, ":current_ai_state", sfai_default),    #MOTO not going to attack anyway
                        (this_or_next|eq, ":current_ai_state", sfai_feast),    #MOTO not going to attack anyway (THIS is the emergency to stop feast)
			(ge, ":threat_danger_level", ":target_value_level"),
			(party_slot_ge, ":most_threatened_center", slot_center_is_besieged_by, 0),

			(assign, ":action", sfai_attacking_enemies_around_center),
			(assign, ":object", ":most_threatened_center"),

			(str_store_party_name, s21, ":most_threatened_center"),
			(str_store_string, s14, "str_we_should_ride_to_break_the_siege_of_s21"),

		#3b - DEFEAT ENEMIES NEAR CENTER - similar to above, but a different string
		(else_try),
			(party_is_active, ":marshal_party"),
                        (this_or_next|eq, ":current_ai_state", sfai_default),    #MOTO not going to attack anyway
                        (this_or_next|eq, ":current_ai_state", sfai_feast),    #MOTO not going to attack anyway (THIS is the emergency to stop feast)
			(ge, ":threat_danger_level", ":target_value_level"),
			(is_between, ":most_threatened_center", villages_begin, villages_end),

			(assign, ":action", sfai_attacking_enemies_around_center),
			(assign, ":object", ":most_threatened_center"),
			(str_store_party_name, s21, ":most_threatened_center"),
			(str_store_string, s14, "str_we_should_ride_to_defeat_the_enemy_gathered_near_s21"),

		#4-DEMOBILIZATION
		#Let vassals attend their own business
		(else_try),
			(this_or_next|eq, ":current_ai_state", sfai_gathering_army),
			(this_or_next|eq, ":current_ai_state", sfai_attacking_center),
			(eq, ":current_ai_state", sfai_raiding_village),

			(ge, ":hours_since_last_faction_rest", ":campaign_hour_limit"), #Effected by ratio of vassals
			(ge, ":hours_at_current_state", 24),

			#Ozan : I am adding some codes here because sometimes armies demobilize during last seconds of an important event like taking a castle, ext.
			(assign, ":there_is_an_important_situation", 0),
			(try_begin), #do not demobilize during taking a castle/town (fighting in the castle)
				(is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
				(party_get_battle_opponent, ":besieger_party", ":current_ai_object"),
				(party_is_active, ":besieger_party"),
				(store_faction_of_party, ":besieger_faction", ":besieger_party"),
				(this_or_next|eq, ":besieger_faction", ":faction_no"),
				(eq, ":besieger_faction", "fac_player_faction"),
				(assign, ":there_is_an_important_situation", 1),
			(else_try), #do not demobilize during besieging a siege (holding around castle)
				(is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
				(party_get_slot, ":besieger_party", ":current_ai_object", slot_center_is_besieged_by),
				(party_is_active, ":besieger_party"),
				(store_faction_of_party, ":besieger_faction", ":besieger_party"),
				(this_or_next|eq, ":besieger_faction", ":faction_no"),
				(eq, ":besieger_faction", "fac_player_faction"),
				(assign, ":there_is_an_important_situation", 1),
			(else_try), #do not demobilize during raiding a village (holding around village)
				(is_between, ":current_ai_object", centers_begin, centers_end),
				(neg|is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
				(party_slot_eq, ":current_ai_object", slot_village_state, svs_being_raided),
				(assign, ":there_is_an_important_situation", 1),
			(try_end),

			(eq, ":there_is_an_important_situation", 0),
			#end addition ozan

			(assign, reg7, ":hours_since_last_faction_rest"),
			(assign, reg8, ":campaign_hour_limit"),

			(str_store_string, s14, "str_this_offensive_needs_to_wind_down_soon_so_the_vassals_can_attend_to_their_own_business"),
			(assign, ":action", sfai_default),
			(assign, ":object", -1),

		#6-GATHERING BECAUSE OF NO REASON
		#Start to gather the army
		(else_try),
			(party_is_active, ":marshal_party"),
			(eq, ":at_peace_with_everyone", 0),


			(eq, ":current_ai_state", sfai_default),
			(ge, ":hours_since_last_offensive", 60),
			(lt, ":hours_since_last_faction_rest", 120),

			#There should not be a center as a precondition for attack
			#Otherwise, we are unlikely to have a situation in which the army gathers, but does nothing -- which is important to have for role-playing purposes

			(assign, ":action", sfai_gathering_army),
			(assign, ":object", -1),
			(str_store_string, s14, "str_it_is_time_to_go_on_the_offensive_and_we_must_first_assemble_the_army"),

            (try_begin),
              (eq, ":faction_no", "$players_kingdom"),
              (assign, "$g_gathering_reason", -1),
            (try_end),

		#7-OFFENSIVE ACTIONS : CONTINUE GATHERING
		(else_try),
			(party_is_active, ":marshal_party"),
			(eq, ":current_ai_state", sfai_gathering_army),
			(eq, ":at_peace_with_everyone", 0),

			(lt, ":hours_at_current_state", 54), #gather army for 54 hours

			(lt, ":ratio_of_vassals_assembled", 12),

			(str_store_string, s14, "str_we_must_continue_to_gather_the_army_before_we_ride_forth_on_an_offensive_operation"),
			(assign, ":action", sfai_gathering_army),
			(assign, ":object", -1),

		#7-OFFENSIVE ACTIONS PART 2 : CONTINUE GATHERING
		(else_try),
		    (assign, ":minimum_possible_attackable_target_value_level", 50),
			(eq, ":at_peace_with_everyone", 0),

            (try_begin), #agressive marshal
			  ##diplomacy start+
			  ##OLD:
			  #(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
			  #(this_or_next|eq, ":reputation", lrep_martial),
			  #(this_or_next|eq, ":reputation", lrep_quarrelsome),
			  #(eq, ":reputation", lrep_selfrighteous),
			  ##NEW:
			  (call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
			  (lt, reg0, 0),
			  ##diplomacy end+
			  (val_mul, ":minimum_possible_attackable_target_value_level", 9),
			  (val_div, ":minimum_possible_attackable_target_value_level", 10),
            (try_end),

			(party_is_active, ":marshal_party"),
			(eq, ":current_ai_state", sfai_gathering_army),

			(try_begin),
				(lt, ":hours_at_current_state", 6),
				(assign, ":minimum_needed_target_value_level", 1500),
			(else_try),
				(lt, ":hours_at_current_state", 10),
				(assign, ":minimum_needed_target_value_level", 1000),
			(else_try),
		        (lt, ":hours_at_current_state", 14),
		        (assign, ":minimum_needed_target_value_level", 720),
			(else_try),
				(lt, ":hours_at_current_state", 18),
				(assign, ":minimum_needed_target_value_level", 480),
			(else_try),
				(lt, ":hours_at_current_state", 22),
				(assign, ":minimum_needed_target_value_level", 360),
			(else_try),
				(lt, ":hours_at_current_state", 26),
				(assign, ":minimum_needed_target_value_level", 240),
			(else_try),
				(lt, ":hours_at_current_state", 30),
				(assign, ":minimum_needed_target_value_level", 180),
			(else_try),
				(lt, ":hours_at_current_state", 34),
				(assign, ":minimum_needed_target_value_level", 120),
			(else_try),
				(lt, ":hours_at_current_state", 38),
				(assign, ":minimum_needed_target_value_level", 100),
			(else_try),
				(lt, ":hours_at_current_state", 42),
				(assign, ":minimum_needed_target_value_level", 80),
			(else_try),
				(lt, ":hours_at_current_state", 46),
				(assign, ":minimum_needed_target_value_level", 65),
			(else_try),
				(lt, ":hours_at_current_state", 50),
				(assign, ":minimum_needed_target_value_level", 55),
			(else_try),
				(assign, ":minimum_needed_target_value_level", ":minimum_possible_attackable_target_value_level"),
			(try_end),

            (try_begin), #agressive marshal
			  ##diplomacy start+
			  ##OLD:
			  #(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
			  #(this_or_next|eq, ":reputation", lrep_martial),
			  #(this_or_next|eq, ":reputation", lrep_quarrelsome),
			  #(eq, ":reputation", lrep_selfrighteous),
			  ##NEW:
			  (call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
			  (lt, reg0, 0),
			  ##diplomacy end+
			  (val_mul, ":minimum_needed_target_value_level", 9),
			  (val_div, ":minimum_needed_target_value_level", 10),
            (try_end),

			(le, ":target_value_level", ":minimum_needed_target_value_level"),
			(le, ":hours_at_current_state", 54),

			(str_store_string, s14, "str_we_have_assembled_some_vassals"),
			(assign, ":action", sfai_gathering_army),
			(assign, ":object", -1),

		#8-ATTACK AN ENEMY CENTER case 1, reconnaissance against walled center
		#(else_try),
			#(party_is_active, ":marshal_party"),
			#(neq, ":current_ai_state", sfai_default),
			#(neq, ":current_ai_state", sfai_feast),
			#(is_between, ":center_to_attack", walled_centers_begin, walled_centers_end),

			#(store_sub, ":faction_recce_slot", ":faction_no", kingdoms_begin),
			#(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
			#(store_current_hours, ":hours_since_last_recon"),
			#(party_get_slot, ":last_recon_time", ":center_to_attack", ":faction_recce_slot"),
			#(val_sub, ":hours_since_last_recon", ":last_recon_time"),
			#(this_or_next|eq, ":last_recon_time", 0),
			#(gt, ":hours_since_last_recon", 96),

		    #(assign, ":action", sfai_attacking_center),
			#(assign, ":object", ":center_to_attack"),
			#(str_store_string, s14, "str_we_are_conducting_recce"),

		#8-ATTACK AN ENEMY CENTER case 2, reconnaissance against village
		#(else_try),
			#(party_is_active, ":marshal_party"),
			#(neq, ":current_ai_state", sfai_default),
			#(neq, ":current_ai_state", sfai_feast),
			#(is_between, ":center_to_attack", villages_begin, villages_end),

			#(store_sub, ":faction_recce_slot", ":faction_no", kingdoms_begin),
			#(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
			#(store_current_hours, ":hours_since_last_recon"),
			#(party_get_slot, ":last_recon_time", ":center_to_attack", ":faction_recce_slot"),
			#(val_sub, ":hours_since_last_recon", ":last_recon_time"),
			#(this_or_next|eq, ":last_recon_time", 0),
			#(gt, ":hours_since_last_recon", 96),


			#(assign, ":action", sfai_raiding_village),
			#(assign, ":object", ":center_to_attack"),
			#(str_store_string, s14, "str_we_are_conducting_recce"),
		(else_try),
			(party_is_active, ":marshal_party"),
			(neq, ":current_ai_state", sfai_default),
			(neq, ":current_ai_state", sfai_feast),

			(assign, ":center_to_attack", ":center_to_attack_only_marshal_and_followers"),

			(is_between, ":center_to_attack", walled_centers_begin, walled_centers_end),

			(ge, ":target_value_level", ":minimum_possible_attackable_target_value_level"),

		    (assign, ":action", sfai_attacking_center),
			(assign, ":object", ":center_to_attack"),
			(str_store_string, s14, "str_we_believe_the_fortress_will_be_worth_the_effort_to_take_it"),
		(else_try),
			(party_is_active, ":marshal_party"),
			(neq, ":current_ai_state", sfai_default),
			(neq, ":current_ai_state", sfai_feast),

			(assign, ":center_to_attack", ":center_to_attack_only_marshal_and_followers"),

			(is_between, ":center_to_attack", villages_begin, villages_end),

			(ge, ":target_value_level", ":minimum_possible_attackable_target_value_level"),

			(assign, ":action", sfai_raiding_village),
			(assign, ":object", ":center_to_attack"),
			(str_store_string, s14, "str_we_shall_leave_a_fiery_trail_through_the_heart_of_the_enemys_lands_targeting_the_wealthy_settlements_if_we_can"),

		#9 -- DISBAND THE ARMY
		(else_try),
			(eq, ":current_ai_state", sfai_gathering_army),

			(str_store_string, s14, "str_the_army_will_be_disbanded_because_we_have_been_waiting_too_long_without_a_target"),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),
		#OFFENSIVE OPERATIONS END

		#FEAST-RELATED OPERATIONS BEGIN
		#10-CONCLUDE CURRENT FEAST
		(else_try),
			(eq, ":current_ai_state", sfai_feast),
			(gt, ":hours_at_current_state", 72),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),
			(str_store_string, s14, "str_it_is_time_for_the_feast_to_conclude"),

		#11-CONTINE FEAST UNLESS THERE IS AN EMERGENCY
		(else_try),
			(eq, ":current_ai_state", sfai_feast),
			(le, ":hours_at_current_state", 72),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":current_ai_object"),
			(str_store_string, s14, "str_we_should_continue_the_feast_unless_there_is_an_emergency"),

		#12-HOLD A FEAST BECAUSE THE PLAYER WANTS TO ORGANIZE ONE
		(else_try),
			(check_quest_active, "qst_organize_feast"),
			(eq, "$players_kingdom", ":faction_no"),

			(quest_get_slot, ":target_center", "qst_organize_feast", slot_quest_target_center),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":target_center"),
			(str_store_string, s14, "str_you_had_wished_to_hold_a_feast"),

		#13-HOLD A FEAST BECAUSE FEMALE PLAYER SCHEDULED TO GET MARRIED
		(else_try),
			(check_quest_active, "qst_wed_betrothed_female"),

			(quest_get_slot, ":groom", "qst_wed_betrothed_female", slot_quest_giver_troop),
			(troop_slot_eq, ":groom", slot_troop_prisoner_of_party, -1),

			(store_faction_of_troop, ":groom_faction", ":groom"),
			(eq, ":groom_faction", ":faction_no"),

			(faction_get_slot, ":faction_leader", ":groom_faction", slot_faction_leader),

			(assign, ":location_feast", -1),
			(try_for_range, ":possible_location", walled_centers_begin, walled_centers_end),
			   (eq, ":location_feast", -1),
			    (party_slot_eq, ":possible_location", slot_town_lord, ":groom"),
			    (party_slot_ge, ":possible_location", slot_center_is_besieged_by, 0),
			    (assign, ":location_feast", ":possible_location"),
			(try_end),

			(try_for_range, ":possible_location", walled_centers_begin, walled_centers_end),
				(eq, ":location_feast", -1),
				(party_slot_eq, ":possible_location", slot_town_lord, ":faction_leader"),
				(party_slot_ge, ":possible_location", slot_center_is_besieged_by, 0),
				(assign, ":location_feast", ":possible_location"),
			(try_end),

			(is_between, ":location_feast", walled_centers_begin, walled_centers_end),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":location_feast"),
			(str_store_string, s14, "str_your_wedding_day_approaches_my_lady"),

		#14-HOLD A FEAST BECAUSE A MALE CHARACTER WANTS TO GET MARRIED
		(else_try),
			(check_quest_active, "qst_wed_betrothed"),
			(neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 362),

			(quest_get_slot, ":bride", "qst_wed_betrothed", slot_quest_target_troop),
			(call_script, "script_get_kingdom_lady_social_determinants", ":bride"),
			(assign, ":feast_host", reg0),
			(store_faction_of_troop, ":feast_host_faction", ":feast_host"),
			(eq, ":feast_host_faction", ":faction_no"),

			(troop_slot_eq, ":feast_host", slot_troop_prisoner_of_party, -1),
			(assign, ":wedding_venue", reg1),

			(is_between, ":wedding_venue", centers_begin, centers_end),
			(party_slot_eq, ":wedding_venue", slot_center_is_besieged_by, -1),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":wedding_venue"),
			(str_store_string, s14, "str_your_wedding_day_approaches"),

		#15-HOLD A FEAST BECAUSE AN NPC WANTS TO GET MARRIED
		(else_try),
            (ge, ":hours_since_last_feast_start", 192), #If at least eight days past last feast start time

			(assign, ":location_feast", -1),

			(try_for_range, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
				(troop_get_slot, ":groom", ":kingdom_lady", slot_troop_betrothed),
				(gt, ":groom", 0), #not the player

				(store_faction_of_troop, ":lady_faction", ":kingdom_lady"),
				(store_faction_of_troop, ":groom_faction", ":groom"),

				(try_begin), #The groom checks if he wants to continue or break off relations. This causes actions, rather than just returns a value, so it probably should be moved elsewhere
					(troop_slot_ge, ":groom", slot_troop_prisoner_of_party, 0),
				(else_try),
					(neq, ":groom_faction", ":lady_faction"),
					(neq, ":groom_faction", "fac_player_faction"),
					(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":kingdom_lady", ":groom"),
				(else_try),
					(eq, ":lady_faction", ":faction_no"),
			        ##diplomacy start+
					#neither the bride nor the groom is in retirement, dead, etc.
					(neg|troop_slot_ge, ":groom", slot_troop_occupation, slto_retirement),
					(neg|troop_slot_ge, ":kingdom_lady", slot_troop_occupation, slto_retirement),
					##diplomacy end+
		            (store_current_hours, ":hours_since_betrothal"),
		            (troop_get_slot, ":betrothal_time", ":kingdom_lady", slot_troop_betrothal_time),
		            (val_sub, ":hours_since_betrothal", ":betrothal_time"),
		            (ge, ":hours_since_betrothal", 719), #30 days

					(call_script, "script_get_kingdom_lady_social_determinants", ":kingdom_lady"),
					(assign, ":wedding_venue", reg1),

		            (assign, ":location_feast", ":wedding_venue"),
		            (assign, ":final_bride", ":kingdom_lady"),
		            (assign, ":final_groom", ":groom"),
				(try_end),
			(try_end),

			(ge, ":location_feast", centers_begin),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":location_feast"),

			(str_store_troop_name, s22, ":final_bride"),
			(str_store_troop_name, s23, ":final_groom"),
			(str_store_string, s14, "str_s22_and_s23_wish_to_marry"),

		#16-HOLD A FEAST ANYWAY
		(else_try),
			(eq, ":current_ai_state", sfai_default),
            (gt, ":hours_since_last_feast_start", 240), #If at least 10 days past after last feast. (added by ozan)

			(assign, ":location_high_score", 0),
			(assign, ":location_feast", -1),

			(try_for_range, ":location", walled_centers_begin, walled_centers_end),
				(store_faction_of_party, ":location_faction", ":location"),
				(eq, ":location_faction", ":faction_no"),

				(try_begin),
			        (neg|party_slot_eq, ":location", slot_village_state, svs_under_siege),
		            (party_get_slot, ":location_lord", ":location", slot_town_lord),
		            (is_between, ":location_lord", active_npcs_begin, active_npcs_end),
		            (troop_get_slot, ":location_score", ":location_lord", slot_troop_renown),
		            (store_random_in_range, ":random", 0, 1000), #will probably be king or senior lord
		            (val_add, ":location_score", ":random"),
		            (gt, ":location_score", ":location_high_score"),
		            (assign, ":location_high_score", ":location_score"),
		            (assign, ":location_feast", ":location"),
				(else_try), #do not start new feasts if any place is under siege or being raided
		            (this_or_next|party_slot_eq, ":location", slot_village_state, svs_under_siege),
						(party_slot_eq, ":location", slot_village_state, svs_being_raided),
		            (assign, ":location_high_score", 9999),
		            (assign, ":location_feast", -1),
				(try_end),
			(try_end),

			(is_between, ":location_feast", walled_centers_begin, walled_centers_end),
			(party_get_slot, ":feast_host", ":location_feast", slot_town_lord),
			(troop_slot_eq, ":feast_host", slot_troop_prisoner_of_party, -1),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":location_feast"),
			(str_store_string, s14, "str_it_has_been_a_long_time_since_the_lords_of_the_realm_gathered_for_a_feast"),

		#17-DO NOTHING
		(else_try),
			(neq, ":current_ai_state", sfai_default),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),
			(str_store_string, s14, "str_the_circumstances_which_led_to_this_decision_no_longer_apply_so_we_should_stop_and_reconsider_shortly"),

		#18-DO NOTHING
		(else_try),
			(eq, ":current_ai_state", sfai_default),

			(eq, ":at_peace_with_everyone", 1),

		    (assign, ":action", sfai_default),
		    (assign, ":object", -1),
			(str_store_string, s14, "str_we_are_currently_at_peace"),
		(else_try),
			(eq, ":current_ai_state", sfai_default),
			(faction_slot_eq, ":faction_no", slot_faction_marshall, -1),
		    (assign, ":action", sfai_default),
		    (assign, ":object", -1),
			(str_store_string, s14, "str_we_are_waiting_for_selection_of_marshal"),

		(else_try),
			(eq, ":current_ai_state", sfai_default),

		    (assign, ":action", sfai_default),
		    (assign, ":object", -1),
			(str_store_string, s14, "str_the_vassals_still_need_time_to_attend_to_their_own_business"),
		(try_end),

		(assign, reg0, ":action"),
		(assign, reg1, ":object"),
	])
]
