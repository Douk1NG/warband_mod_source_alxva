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

calculate_center_assailability_score_scripts = [
(
    "calculate_center_assailability_score",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":potential_target", 2),
      (store_script_param, ":all_vassals_included", 3),

      (assign, ":target_score", -1),

      (store_faction_of_troop, ":faction_no", ":troop_no"),

      (store_current_hours, ":hours_since_last_offensive"),
      (faction_get_slot, ":last_offensive_time", ":faction_no", slot_faction_last_offensive_concluded),
      (val_sub, ":hours_since_last_offensive", ":last_offensive_time"),

      (store_div, ":last_offensive_time_score", ":hours_since_last_offensive", 12), #30..50
      (val_add, ":last_offensive_time_score", 30),
      (val_min, ":last_offensive_time_score", 100),

      (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),

      (assign, ":marshal_party", -1),
      (assign, ":marshal_strength", 0),
      #(assign, ":strength_of_nearby_friend", 0),

      (try_begin),
        (gt, ":faction_marshal", 0),
        (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
        (party_is_active, ":marshal_party"),
        (party_get_slot, ":marshal_strength", ":marshal_party", slot_party_cached_strength),
        #(eq, ":all_vassals_included", 0),
        (party_get_slot, ":strength_of_current_followers", ":marshal_party", slot_party_follower_strength),
        #(party_get_slot, ":strength_of_nearby_friend", ":marshal_party", slot_party_nearby_friend_strength),
      (try_end),

      #(try_begin),
      #  (eq, ":all_vassals_included", 0),
      #
      #  (try_begin),
      #    (gt, ":faction_marshal", 0),
      #    (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
      #    (party_is_active, ":marshal_party"),
      #    (party_get_slot, ":strength_of_potential_followers", ":marshal_party", slot_party_follower_strength),
      #  (try_end),
      #(else_try),
      #  (eq, ":all_vassals_included", 1),
      #
      #  (assign, ":strength_of_potential_followers", 0),
      #
      #  (try_for_parties, ":party_no"),
      #    (store_faction_of_party, ":party_faction", ":party_no"),
      #    (eq, ":party_faction", ":faction_no"),
      #    (neq, ":party_no", ":marshal_party"),
      #    (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
      #    (call_script, "script_party_calculate_strength", ":party_no", 0),
      #    (val_add, ":strength_of_potential_followers", reg0),
      #  (try_end),
      #
      #  (val_div, ":strength_of_potential_followers", 2), #Ozan - Think about this, will you divide strength_of_potential_followers to 3 or 2.5 or 2
      #(else_try),
      #  (assign, ":strength_of_potential_followers", 0),
      #(try_end),

      (faction_get_slot, ":last_attacked_center", ":faction_no", slot_faction_last_attacked_center),
      (faction_get_slot, ":last_attacked_hours", ":faction_no", slot_faction_last_attacked_hours),

      (try_begin),
        (store_current_hours, ":hours"),
        (store_add, ":last_attacked_hours_plus_24", ":last_attacked_hours", 24),
        (gt, ":hours", ":last_attacked_hours_plus_24"),
        (faction_set_slot, ":faction_no", slot_faction_last_attacked_center, 0),
        (assign, ":last_attacked_center", 0),
      (try_end),

      (try_begin),
        (this_or_next|eq, ":last_attacked_center", 0),
        (this_or_next|eq, ":last_attacked_center", ":potential_target"),
        (this_or_next|eq, "$g_do_not_skip_other_than_current_ai_object", 1),
        (neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),

        (party_is_active, ":potential_target"),
        (store_faction_of_party, ":potential_target_faction", ":potential_target"),

        (store_relation, ":relation", ":potential_target_faction", ":faction_no"),
        (lt, ":relation", 0),

        #attack if and only if we are already besieging that center or anybody do not making besiege.
        (assign, ":faction_of_besieger_party", -1),
        (try_begin),
          (is_between, ":potential_target", walled_centers_begin, walled_centers_end),
          (neg|party_slot_eq, ":potential_target", slot_center_is_besieged_by, -1),
          (party_get_slot, ":besieger_party", ":potential_target", slot_center_is_besieged_by),
          (party_is_active, ":besieger_party"),
          (store_faction_of_party, ":faction_of_besieger_party", ":besieger_party"),
        (try_end),

        (this_or_next|eq, ":faction_of_besieger_party", -1),
        (eq, ":faction_of_besieger_party", ":faction_no"),

        #attack if and only if this center is not a village or if it is village it should not be raided or looted
        (assign, ":village_is_looted_or_raided_already", 0),
        (try_begin),
          (is_between, ":potential_target", villages_begin, villages_end),
          (try_begin),
            (party_slot_eq, ":potential_target", slot_village_state, svs_being_raided),
            (party_get_slot, ":raider_party", ":potential_target", slot_village_raided_by),
			(party_is_active, ":raider_party"),

            (store_faction_of_party, ":raider_faction", ":raider_party"),
            (neq, ":raider_faction", ":faction_no"),
            (assign, ":raiding_by_one_other_faction", 1),
          (else_try),
            (assign, ":raiding_by_one_other_faction", 0),
          (try_end),
          (this_or_next|party_slot_eq, ":potential_target", slot_village_state, svs_looted),
          (eq, ":raiding_by_one_other_faction", 1),
          (assign, ":village_is_looted_or_raided_already", 1),
        (try_end),
        (eq, ":village_is_looted_or_raided_already", 0),

        #if ":potential_target" is faction object of some other faction which is enemy to owner of
        #":potential_target" then this target cannot be new target we are looking for.
        (assign, ":this_potantial_target_is_target_of_some_other_faction", 0),
        (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
          (is_between, ":cur_faction", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
          (neq, ":cur_faction", ":faction_no"),
          (faction_get_slot, ":faction_object", ":cur_faction", slot_faction_ai_object),
          (eq, ":faction_object", ":potential_target"),
          (store_relation, ":rel", ":potential_target_faction", ":cur_faction"),
          (lt, ":rel", 0),
          (assign, ":this_potantial_target_is_target_of_some_other_faction", 1),
        (try_end),
        (eq, ":this_potantial_target_is_target_of_some_other_faction", 0),

        (try_begin),
          (is_between, ":potential_target", walled_centers_begin, walled_centers_end),
          (party_get_slot, ":potential_target_inside_strength", ":potential_target", slot_party_cached_strength),
          (party_get_slot, ":potential_target_nearby_enemy_strength", ":potential_target", slot_party_nearby_friend_strength),
          (val_div, ":potential_target_nearby_enemy_strength", 2),
          (store_add, ":potential_target_strength", ":potential_target_inside_strength", ":potential_target_nearby_enemy_strength"),

          #(try_begin),
            #(eq, ":faction_no", "fac_kingdom_4"),
            #(assign, reg0, ":potential_target_inside_strength"),
            #(assign, reg1, ":potential_target_nearby_enemy_strength"),
            #(assign, reg2, ":marshal_strength"),
            #(assign, reg3, ":strength_of_potential_followers"),
            #(assign, reg4, ":strength_of_nearby_friend"),
            #(assign, reg6, ":marshal_party"),
            #(str_store_party_name, s8, ":potential_target"),
            #(eq, ":all_vassals_included", 0),
            #(display_message, "@DEBUG : {s8}:{reg0}, neare {reg1}, our {reg2}, follow {reg3}, nearf {reg4}"),
          #(try_end),

          (val_mul, ":potential_target_strength", 4), #in walled centers defenders have advantage.
          (val_div, ":potential_target_strength", 3),

          #(store_add, ":army_strength", ":marshal_strength", ":strength_of_potential_followers"),
          (assign, ":army_strength", ":marshal_strength"),
          (val_add, ":army_strength", ":strength_of_current_followers"),
          (store_mul, ":power_ratio", ":army_strength", 100),

          #this ratio ":power_ratio" shows (our total army power) / (their total army power)
          (try_begin),
            (gt, ":potential_target_strength", 0),
            (val_div, ":power_ratio", ":potential_target_strength"),
          (else_try),
            (assign, ":power_ratio", 1000),
          (try_end),
        (else_try),
          (party_get_slot, ":potential_target_nearby_enemy_strength", ":potential_target", slot_party_nearby_friend_strength),
          (assign, ":potential_target_strength", 1000),

          #(store_add, ":army_strength", ":marshal_strength", ":strength_of_potential_followers"),
          (assign, ":army_strength", ":marshal_strength"),
          (val_add, ":army_strength", ":strength_of_current_followers"),
          (store_mul, ":power_ratio", ":army_strength", 100),

          (try_begin),
            (gt, ":potential_target_strength", 0),
            (val_div, ":power_ratio", ":potential_target_strength"),
          (else_try),
            (assign, ":power_ratio", 1000),
          (try_end),
        (try_end),

        (ge, ":power_ratio", 120), #attack if and only if our army is at least 1.2 times powerfull
        (store_sub, ":power_ratio_sub_120", ":power_ratio", 120),

        (try_begin),
          (lt, ":power_ratio_sub_120", 100), #changes between 20..120
          (store_add, ":power_ratio_score", ":power_ratio_sub_120", 20),
        (else_try),
          (lt, ":power_ratio_sub_120", 200), #changes between 120..170
          (store_sub, ":power_ratio_score", ":power_ratio_sub_120", 100),
          (val_div, ":power_ratio_score", 2),
          (val_add, ":power_ratio_score", 120),
        (else_try),
          (lt, ":power_ratio_sub_120", 400), #changes between 170..210
          (store_sub, ":power_ratio_score", ":power_ratio_sub_120", 200),
          (val_div, ":power_ratio_score", 5),
          (val_add, ":power_ratio_score", 170),
        (else_try),
          (lt, ":power_ratio_sub_120", 800), #changes between 210..250
          (store_sub, ":power_ratio_score", ":power_ratio_sub_120", 400),
          (val_div, ":power_ratio_score", 10),
          (val_add, ":power_ratio_score", 210),
        (else_try),
          (assign, ":power_ratio_score", 250),
        (try_end),

        (assign, ":number_of_walled_centers", 0),
        (assign, ":total_distance", 0),
        (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
          (store_faction_of_party, ":walled_center_faction", ":walled_center"),
          (eq, ":walled_center_faction", ":faction_no"),

          (store_distance_to_party_from_party, ":dist", ":walled_center", ":potential_target"),
          (val_add, ":total_distance", ":dist"),

          (val_add, ":number_of_walled_centers", 1),
        (try_end),

        (try_begin),
          (gt, ":number_of_walled_centers", 0),
          (store_div, ":average_distance", ":total_distance", ":number_of_walled_centers"),
          #(assign, reg0, ":average_distance"),
          #(str_store_faction_name, s7, ":faction_no"),
          #(str_store_party_name, s8, ":potential_target"),
          #(display_message, "@average distance for {s7} for {s8} is {reg0}"),

          (try_begin),
            (ge, ":marshal_party", 0),
            (party_is_active, ":marshal_party"),
            (store_distance_to_party_from_party, ":marshal_dist_to_potential_target", ":marshal_party", ":potential_target"),
          (else_try),
            (assign, ":marshal_dist_to_potential_target", 100),
          (try_end),

          (try_begin),
            #if currently main aim of our faction is attacking to an enemy center and that center is already besieged/raided by one of
            #our parties then divide marshal_dist_to_potential_target_div_x score for current center to "3/2" instead of "3" and this
            #result in decrease at distance_score, and also decrease some scores from power_ratio_score in order to avoid frequently
            #changes at main aimed target city of our faction during sieges.

            (faction_get_slot, ":current_ai_state", ":faction_no", slot_faction_ai_state),
            (eq, ":current_ai_state", sfai_attacking_center),
            (faction_get_slot, ":current_ai_object", ":faction_no", slot_faction_ai_object),

            (ge, ":current_ai_object", 0),
            (neq, ":current_ai_object", ":potential_target"),

            (try_begin),
              (ge, ":power_ratio_score", 300), #200 max
              (assign, ":power_ratio_score", 200),
            (else_try),
              (ge, ":power_ratio_score", 100), #100..200
              (val_sub, ":power_ratio_score", 100),
              (val_div, ":power_ratio_score", 2),
              (val_add, ":power_ratio_score", 100),
            (try_end),

            (try_begin),
              (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
              (eq, "$g_do_not_skip_other_than_current_ai_object", 0),
              (assign, ":power_ratio_score", 0), #lets completely forget all other choices if we are already besieging one center.
            (try_end),

            (faction_set_slot, ":faction_no", slot_faction_last_attacked_center, ":current_ai_object"),
            (store_current_hours, ":hours"),
            (faction_set_slot, ":faction_no", slot_faction_last_attacked_hours, ":hours"),

            (eq, ":all_vassals_included", 0),

            (store_mul, ":marshal_dist_to_potential_target_div_x", ":marshal_dist_to_potential_target", 2),
            (val_div, ":marshal_dist_to_potential_target_div_x", 3),
          (else_try),
            (store_div, ":marshal_dist_to_potential_target_div_x", ":marshal_dist_to_potential_target", 3),
          (try_end),

          (store_add, ":total_distance", ":average_distance", ":marshal_dist_to_potential_target_div_x"), #in average ":total_distance" is about 150, min : 0, max : 1000
        (else_try),
          (assign, ":total_distance", 100),
        (try_end),

        (try_begin),
          #according to cautious troop distance is more important
          ##diplomacy start+ Take into account lady & companion personality types
		  ##OLD:
	      #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
	      #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
	      #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
	      #(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
		  #
		  ##NEW:
		  (call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
		  (assign, ":troop_caution", reg0),
		  (gt, ":troop_caution", 0),
		  ##diplomacy end+

          (try_begin),
            (lt, ":total_distance", 30), #very close (100p)
            (assign, ":distance_score", 100),
          (else_try),
            (lt, ":total_distance", 80), #close (50p-100p)
            (store_sub, ":distance_score", ":total_distance", 30),
            (val_div, ":distance_score", 1),
            (store_sub, ":distance_score", 100, ":distance_score"),
          (else_try),
            (lt, ":total_distance", 160), #far (10p-50p)
            (store_sub, ":distance_score", ":total_distance", 80),
            (val_div, ":distance_score", 2),
            (store_sub, ":distance_score", 50, ":distance_score"),
          (else_try),
            (assign, ":distance_score", 10), #very far
          (try_end),
        (else_try),
          #according to agressive troop distance is less important

          (try_begin),
            (lt, ":total_distance", 40), #very close (100p)
            (assign, ":distance_score", 100),
          (else_try),
            (lt, ":total_distance", 140), #close (50p-100p)
            (store_sub, ":distance_score", ":total_distance", 40),
            (val_div, ":distance_score", 2),
            (store_sub, ":distance_score", 100, ":distance_score"),
          (else_try),
            (lt, ":total_distance", 300), #far (10p-50p)
            (store_sub, ":distance_score", ":total_distance", 140),
            (val_div, ":distance_score", 4),
            (store_sub, ":distance_score", 50, ":distance_score"),
          (else_try),
            (assign, ":distance_score", 10), #very far
          (try_end),
        (try_end),
		##diplomacy start+ If AI changes are enabled, reduce distance penalty (increase score)
		##for recently-lost fiefs.
		(try_begin),
			(lt, ":distance_score", 100),
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
			(party_slot_eq, ":potential_target", slot_center_ex_faction, ":faction_no"),
			(party_get_slot, reg0, ":potential_target", dplmc_slot_center_last_transfer_time),
			(gt, reg0, 0),#0 means the slot was uninitialized.  A negative number would be before the start of the game.
			(store_current_hours, ":hours_since_transfer"),
			(val_sub, ":hours_since_transfer", reg0),
			(try_begin),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
				(assign, reg0, 24 * 21),#within last three weeks
			(else_try),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				(assign, reg0, 24 * 14),#within last two weeks
			(else_try),
				(assign, reg0, 24 * 7),#within last week
			(try_end),
			(lt, ":hours_since_transfer", reg0),
			(val_add, ":distance_score", 100),
			(val_div, ":distance_score", 2),
		(try_end),
		##diplomacy end+

        (store_mul, ":target_score", ":distance_score", ":power_ratio_score"),
        (val_mul, ":target_score", ":last_offensive_time_score"),
        (val_div, ":target_score", 100), #target score is between 0..10000 generally here

        (call_script, "script_find_total_prosperity_score", ":potential_target"),
        (assign, ":total_prosperity_score", reg0),

        #(try_begin), #new for increase attackability of villages by ai
          #(is_between, ":potential_target", villages_begin, villages_end),
          (val_mul, ":total_prosperity_score", 3),
          (val_div, ":total_prosperity_score", 2),
        #(try_end),

        (val_mul, ":target_score", ":total_prosperity_score"),

        (try_begin), #if both that center was our (original center) and (ex center) than bonus is 1.2x
          (party_slot_eq, ":potential_target", slot_center_ex_faction, ":faction_no"),
          (party_slot_eq, ":potential_target", slot_center_original_faction, ":faction_no"),
          (val_mul, ":target_score", 12),
          (val_div, ":target_score", 10),
        (else_try), #if either that center was our (original center) or (ex center) than bonus is 1.1x
          (this_or_next|party_slot_eq, ":potential_target", slot_center_ex_faction, ":faction_no"),
          (party_slot_eq, ":potential_target", slot_center_original_faction, ":faction_no"),
          (val_mul, ":target_score", 11),
          (val_div, ":target_score", 10),
        (try_end),

        (val_div, ":target_score", 1000), #target score is between 0..1000 generally here

        (try_begin),
          (eq, ":potential_target_faction", "fac_player_supporters_faction"),
          (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),

          (assign, ":number_of_walled_centers_player_have", 0),
          (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
            (store_faction_of_party, ":center_faction", ":center_no"),
            (eq, ":center_faction", "fac_player_supporters_faction"),
            (val_add, ":number_of_walled_centers_player_have", 1),
          (try_end),

          (try_begin),
            (eq, ":reduce_campaign_ai", 2), #easy

            (try_begin),
              (le, ":number_of_walled_centers_player_have", 2),
              (assign, ":hardness_score", 0),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 3),
              (assign, ":hardness_score", 20),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 4),
              (assign, ":hardness_score", 40),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 5),
              (eq, ":number_of_walled_centers_player_have", 6),
              (assign, ":hardness_score", 55),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 7),
              (eq, ":number_of_walled_centers_player_have", 8),
              (eq, ":number_of_walled_centers_player_have", 9),
              (assign, ":hardness_score", 70),
            (else_try),
              (assign, ":hardness_score", 85),
            (try_end),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #medium

            (try_begin),
              (le, ":number_of_walled_centers_player_have", 1),
              (assign, ":hardness_score", 25),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 2),
              (assign, ":hardness_score", 45),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 3),
              (assign, ":hardness_score", 60),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 4),
              (eq, ":number_of_walled_centers_player_have", 5),
              (assign, ":hardness_score", 75),
            (else_try),
              (eq, ":number_of_walled_centers_player_have", 6),
              (eq, ":number_of_walled_centers_player_have", 7),
              (eq, ":number_of_walled_centers_player_have", 8),
              (assign, ":hardness_score", 85),
            (else_try),
              (assign, ":hardness_score", 92),
            (try_end),
          (else_try), #hard
            (assign, ":hardness_score", 100),
          (try_end),

          (val_mul, ":target_score", ":hardness_score"),
          (val_div, ":target_score", 100),
        (try_end),

        (try_begin),
          (ge, "$cheat_mode", 1),
          (eq, ":faction_no", "fac_kingdom_4"),
          (ge, ":target_score", -1),
          (assign, reg0, ":target_score"),
          (assign, reg7, ":total_prosperity_score"),
          (assign, reg8, ":power_ratio_score"),
          (assign, reg9, ":distance_score"),
          (assign, reg10, ":last_offensive_time_score"),
          (str_store_party_name, s8, ":potential_target"),
          #(eq, ":all_vassals_included", 0),
          (assign, reg11, ":all_vassals_included"),
          #(display_message, "@DEBUG : attack of {s8} is {reg0}({reg11}), prs:{reg7}, pow:{reg8}, dis:{reg9}, lst:{reg10}"),
        (try_end),
      (try_end),

      (assign, reg0, ":target_score"),
      (assign, reg1, ":power_ratio"),
      (assign, reg2, ":distance_score"),
      (assign, reg3, ":total_prosperity_score"),
    ])
]
