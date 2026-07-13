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

misc_scripts_extra2 = [
    # INPUT: troop_no
    # OUTPUT: reg0
	(
	"npc_decision_checklist_troop_follow_or_not", [

	(store_script_param, ":troop_no", 1),
	(store_faction_of_troop, ":faction_no", ":troop_no"),
	(faction_get_slot, ":faction_ai_state", ":faction_no", slot_faction_ai_state),

	(troop_get_slot, ":troop_reputation", ":troop_no", slot_lord_reputation_type),
	(faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
    ##diplomacy start+
    #Get the centralization value for use below.  It should be a value in [-3,3].
    #A centralization value of 0 should not result in any behavior change.
    (try_begin),
       #If the player altered the kingdom policy, always apply its effects to
       #the AI of his kingdom's lords.
       (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
       (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
       (faction_get_slot, ":centralization", ":faction_no", dplmc_slot_faction_centralization),
       (val_clamp, ":centralization", -3, 4),
    (else_try),
       #Currently, do not apply centralization to the AI for NPC kingdoms, since
       #NPC rulers set their policies randomly and do not gain the same monthly
       #relation bonuses/penalties from centralization that the player does.
       (assign, ":centralization", 0),
    (try_end),
    ##diplomacy end+

	(assign, ":result", 0),
	(try_begin),
		##diplomacy start+ add another check
		(this_or_next|lt, ":faction_marshall", 0),
		##diplomacy end+
		(eq, ":faction_marshall", -1),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__i_am_acting_independently_because_no_marshal_is_appointed"),
		(try_end),
	(else_try),
		(troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
		(neg|party_is_active, ":faction_marshall_party"),

		#Not doing an offensive
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__i_am_acting_independently_because_our_marshal_is_currently_indisposed"),
		(try_end),
	(else_try),
		(neq, ":faction_ai_state", sfai_attacking_center),
        (neq, ":faction_ai_state", sfai_raiding_village),
        (neq, ":faction_ai_state", sfai_attacking_enemies_around_center),
        (neq, ":faction_ai_state", sfai_attacking_enemy_army),
        (neq, ":faction_ai_state", sfai_gathering_army),

		#Not doing an offensive
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__i_am_acting_independently_because_our_realm_is_currently_not_on_campaign"),
		(try_end),
	(else_try),
		(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_marshall"),
		(assign, ":relation_with_marshall", reg0),

		(try_begin),
		  (le, ":relation_with_marshall", -10),
		  (assign, ":acceptance_level", 10000),
		(else_try),
		  (store_mul, ":acceptance_level", ":relation_with_marshall", -1000),
		(try_end),

		(val_add, ":acceptance_level", 1500),

        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		(try_begin),
		  (neq, ":faction_no", "$players_kingdom"),
          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard
            (val_add, ":acceptance_level", -1250),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate
          (else_try),
            (eq, ":reduce_campaign_ai", 2), #easy
            (val_add, ":acceptance_level", 1250),
          (try_end),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_marshall, "trp_player"),
          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard/player's faction
            (val_add, ":acceptance_level", -1000),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate/player's faction
            (val_add, ":acceptance_level", -1500),
          (else_try),
            (eq, ":reduce_campaign_ai", 2), #easy/player's faction
            (val_add, ":acceptance_level", -2000),
          (try_end),
		(try_end),

		(troop_get_slot, ":temp_ai_seed", ":troop_no", slot_troop_temp_decision_seed),

		(le, ":temp_ai_seed", ":acceptance_level"),

		#Very low opinion of marshall
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__i_am_not_accompanying_the_marshal_because_i_fear_that_he_may_lead_us_into_disaster"),
		(try_end),
		#Make nuanced, depending on personality type
	(else_try),
		(troop_get_slot, ":marshal_controversy", ":faction_marshall", slot_faction_marshall),

		(lt, ":relation_with_marshall", 0),
		(ge, ":marshal_controversy", 50),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str_i_am_not_accompanying_the_marshal_because_i_question_his_judgment"),
		(try_end),
	(else_try),
		(troop_get_slot, ":marshal_controversy", ":faction_marshall", slot_faction_marshall),
		(neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":faction_marshall"),

		(lt, ":relation_with_marshall", 5),
		(ge, ":marshal_controversy", 80),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str_i_am_not_accompanying_the_marshal_because_will_be_reappointment"),
		(try_end),
	(else_try),
		#(lt, ":relation_with_marshall", 45),
		#(eq, ":faction_marshall", "trp_player"), #moved below as only effector. Search "think about this".

		(store_sub, ":relation_with_marshal_difference", 50, ":relation_with_marshall"),

		#for 50 relation with marshal ":acceptance_level" will be 0
		#for 20 relation with marshal ":acceptance_level" will be 2100
		#for 10 relation with marshal ":acceptance_level" will be 2800
		#for 0 relation with marshal ":acceptance_level" will be 3500
		#for -10 relation with marshal ":acceptance_level" will be 4200
		#average is about 2500
		(store_mul, ":acceptance_level", ":relation_with_marshal_difference", 70),

        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		(try_begin),
		  (neq, ":faction_no", "$players_kingdom"),

          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard
            (val_add, ":acceptance_level", -1200),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate
          (else_try),
            (eq, ":reduce_campaign_ai", 2), #easy
            (val_add, ":acceptance_level", 1200),
          (try_end),
		(else_try),
          (eq, ":faction_marshall", "trp_player"),

          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard
            (val_add, ":acceptance_level", -1000),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate
            (val_add, ":acceptance_level", -1500),
          (else_try),
            (eq, ":reduce_campaign_ai", 2), #easy
            (val_add, ":acceptance_level", -2000),
          (try_end),
		(try_end),

		(try_begin),
		  (eq, ":troop_reputation", lrep_selfrighteous),
		  (val_add, ":acceptance_level", 1500),
		(else_try),
		  (this_or_next|eq, ":troop_reputation", lrep_martial),
		  (this_or_next|eq, ":troop_reputation", lrep_roguish),
		  (eq, ":troop_reputation", lrep_quarrelsome),
		  (val_add, ":acceptance_level", 1000),
		(else_try),
		  (eq, ":troop_reputation", lrep_cunning),
		  (val_add, ":acceptance_level", 500),
		(else_try),
		  (eq, ":troop_reputation", lrep_upstanding), #neutral
		(else_try),
		  (this_or_next|eq, ":troop_reputation", lrep_benefactor), #helper
		  (eq, ":troop_reputation", lrep_goodnatured),
		  (val_add, ":acceptance_level", -500),
		(else_try),
		  (eq, ":troop_reputation", lrep_custodian), #very helper
		  (val_add, ":acceptance_level", -1000),
		(try_end),

		(try_begin),
		  (troop_slot_eq, ":faction_marshall", slot_lord_reputation_type, lrep_quarrelsome),
		  (val_add, ":acceptance_level", -750),
		(else_try),
		  (this_or_next|troop_slot_eq, ":faction_marshall", slot_lord_reputation_type, lrep_martial),
		  (troop_slot_eq, ":faction_marshall", slot_lord_reputation_type, lrep_upstanding),
		  (val_add, ":acceptance_level", -250),
		(try_end),

		(val_add, ":acceptance_level", 2000),
		#average become 2500 + 2000 = 4500, (45% of lords will not join campaign because of this reason. (33% for hard, 57% for easy, 30% for marshal player))

      ##diplomacy start+ Apply centralization.
      #Adjusting acceptance level seems a natural place to represent this.
      (store_mul, reg0, ":centralization", 100),
      (val_clamp, reg0, -300, 301),#should be unnecessary
      (val_sub, ":acceptance_level", reg0),#adjust the chance of following the marshall by +/- 1% for every step of centralization
      ##diplomacy end+
		(troop_get_slot, ":temp_ai_seed", ":troop_no", slot_troop_temp_decision_seed),

		(le, ":temp_ai_seed", ":acceptance_level"),

		(try_begin),
		  (eq, ":troop_no", "$g_talk_troop"),
		  (str_store_string, s15, "str_i_am_not_accompanying_the_marshal_because_i_can_do_greater_deeds"),
		(try_end),

		#(try_begin),
		#  (ge, "$cheat_mode", 1),
		#  (assign, reg7, ":acceptance_level"),
		#  (assign, reg8, ":relation_with_marshall"),
		#  (display_message, "@{!}DEBUGS : acceptance level : {reg7}, relation with marshal : {reg8}"),
		#(try_end),
	(else_try),
		(store_current_hours, ":hours_since_last_faction_rest"),
		(faction_get_slot, ":last_rest_time", ":faction_no", slot_faction_ai_last_rest_time),
		(val_sub, ":hours_since_last_faction_rest", ":last_rest_time"),

		#nine days on average, marshal will usually end after 10 days
		#ozan changed, 360 hours (15 days) in average, marshal cannot end it during a siege attack/defence anymore.
		(assign, ":troop_campaign_limit", 360),
		(store_mul, ":marshal_relation_modifier", ":relation_with_marshall", 6), #ozan changed 4 to 6.
		(val_add, ":troop_campaign_limit", ":marshal_relation_modifier"),

		(try_begin),
			(eq, ":troop_reputation", lrep_upstanding),
			(val_mul, ":troop_campaign_limit", 4),
			(val_div, ":troop_campaign_limit", 3),
		(try_end),

		(str_store_troop_name, s16, ":faction_marshall"),

		(gt, ":hours_since_last_faction_rest", ":troop_campaign_limit"),

		#Too long a campaign
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__s16_has_kept_us_on_campaign_on_far_too_long_and_there_are_other_pressing_matters_to_which_i_must_attend"),
		(try_end),
		#Also make nuanced, depending on personality type
	(else_try),
		(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
		(neg|party_is_active, ":party_no"),
		#This string should not occur, as it will only happen if a lord is contemplating following the player
	(else_try),
		(troop_get_slot, ":marshal_party", ":faction_marshall", slot_troop_leaded_party),

		(assign, ":information_radius", 40),
		(try_begin),
		  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		  (assign, ":information_radius", 50),
		(try_end),

        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		(try_begin),
		  (neq, ":faction_no", "fac_player_supporters_faction"),
		  (neq, ":faction_no", "$players_kingdom"),
		  ##diplomacy start+ the player may be able to become leader in other situations
		  (neg|faction_slot_eq, ":faction_no", slot_faction_leader, "trp_player"),
		  ##diplomacy end+
		  (try_begin),
		    (eq, ":reduce_campaign_ai", 2), #easy
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", -10),
		    (else_try),
		      (val_add, ":information_radius", -8),
		    (try_end),
		  (else_try),
		    (eq, ":reduce_campaign_ai", 1), #moderate
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", -5),
		    (else_try),
		      (val_add, ":information_radius", -4),
		    (try_end),
		  (try_end),
		(else_try),
		  (try_begin),
		    (eq, ":reduce_campaign_ai", 2), #easy
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", 25),
		    (else_try),
		      (val_add, ":information_radius", 20),
		    (try_end),
		  (else_try),
		    (eq, ":reduce_campaign_ai", 1), #moderate
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", 15),
		    (else_try),
		      (val_add, ":information_radius", 12),
		    (try_end),
		  (else_try),
		    (eq, ":reduce_campaign_ai", 0), #hard
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", 5),
		    (else_try),
		      (val_add, ":information_radius", 4),
		    (try_end),
		  (try_end),
		(try_end),
      ##diplomacy start+ Apply centralization to the AI here.
      (store_add, reg0, 10, ":centralization"),
      (val_clamp, reg0, 7, 14),#should be unnecessary
      (val_mul, ":information_radius", reg0),
      (val_add, ":information_radius", 5),
      (val_div, ":information_radius", 10),#Adjust +/- 10% for every level of centralization
      ##diplomacy end+

		(faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
		(assign, reg17, 0),
		(try_begin),
		  (try_begin),
		    (neg|is_between, ":faction_object", villages_begin, villages_end),
		    (assign, reg17, 1),
		  (try_end),
		  (try_begin),
		    (neg|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
		    (assign, reg17, 1),
		  (try_end),
		  (eq, reg17, 1),

		  (store_distance_to_party_from_party, ":distance", ":marshal_party", ":party_no"),

		  (gt, ":distance", ":information_radius"),

          (try_begin),
            (eq, ":troop_no", "$g_talk_troop"),
            (str_store_string, s15, "str__i_am_not_participating_in_the_marshals_campaign_because_i_do_not_know_where_to_find_our_main_army"),
  		  (try_end),
		(else_try),
		  (eq, reg17, 0),

          (assign, reg17, 1),
          (try_begin),
            #if we are already accompanying marshal forget below.
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
            (party_slot_eq, ":party_no", slot_party_ai_object, ":marshal_party"),
            (assign, reg17, 0),
          (try_end),
          (eq, reg17, 1),

		  #if faction ai is "attacking enemies around a center" is then do not find and compare distance to marshal, find and compare distance to "attacked village"
		  (party_get_slot, ":enemy_strength_nearby", ":faction_object", slot_center_sortie_enemy_strength),

		  (try_begin), #changes between 70..x (as ":enemy_strength_nearby" increases, ":information_radius" increases too.),
		    (ge, ":enemy_strength_nearby", 4000),
		    (val_sub, ":enemy_strength_nearby", 4000),
		    (store_div, ":information_radius", ":enemy_strength_nearby", 200),
		    (val_add, ":information_radius", 70),
		  (else_try), #changes between 30..70
		    (store_div, ":information_radius", ":enemy_strength_nearby", 100),
		    (val_add, ":information_radius", 30),
		  (try_end),

		  (store_distance_to_party_from_party, ":distance", ":faction_object", ":party_no"),

		  (gt, ":distance", ":information_radius"),

          (try_begin),
            (eq, ":troop_no", "$g_talk_troop"),
            (str_store_string, s15, "str__i_am_acting_independently_although_some_enemies_have_been_spotted_within_our_borders_they_havent_come_in_force_and_the_local_troops_should_be_able_to_dispatch_them"),
  		  (try_end),
		(try_end),

		(gt, ":distance", ":information_radius"),
	(else_try),
		(try_begin),
		  (eq, ":troop_no", "$g_talk_troop"),
		  (str_store_string, s15, "str__the_needs_of_the_realm_must_come_first"),
		(try_end),
		(assign, ":result", 1),
	(try_end),

	(assign, reg0, ":result"),
	]),

	#script_find_total_prosperity_score
    # INPUT: center_no
    # OUTPUT: reg0 = total_prosperity_score
	(
	"find_total_prosperity_score",
	[
	  (store_script_param, ":center_no", 1),

      (try_begin), #":total_prosperity_score" changes between 10..100
        (is_between, ":center_no", walled_centers_begin, walled_centers_end),

        (party_get_slot, ":center_prosperity", ":center_no", slot_town_prosperity),
        (store_add, ":center_prosperity_add_200_div_10", ":center_prosperity", 200),
        (val_div, ":center_prosperity_add_200_div_10", 10),
        (try_begin),
          (is_between, ":center_no", towns_begin, towns_end),
          (store_mul, ":this_center_score", ":center_prosperity_add_200_div_10", 15),
        (else_try),
          (store_mul, ":this_center_score", ":center_prosperity_add_200_div_10", 5),
        (try_end),
        (assign, ":total_prosperity_score", ":this_center_score"),

        (try_for_range_backwards, ":village_no", villages_begin, villages_end),
          (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),

          (party_get_slot, ":village_prosperity", ":village_no", slot_town_prosperity),
          (store_add, ":village_prosperity_add_200_div_10", ":village_prosperity", 200),
          (val_div, ":village_prosperity_add_200_div_10", 10),
          (store_mul, ":this_village_score", ":village_prosperity_add_200_div_10", 5),

          (val_add, ":total_prosperity_score", ":this_village_score"),
        (try_end),
      (else_try),
        (party_get_slot, ":center_prosperity", ":center_no", slot_town_prosperity),
        (store_add, ":center_prosperity_add_200_div_10", ":center_prosperity", 200),
        (val_div, ":center_prosperity_add_200_div_10", 10),
        (store_mul, ":this_center_score", ":center_prosperity_add_200_div_10", 5),
        (assign, ":total_prosperity_score", ":this_center_score"),
      (try_end),
      (val_div, ":total_prosperity_score", 10),

      (assign, reg0, ":total_prosperity_score"),
	]),

    #script_calculate_center_assailability_score
    # INPUT: faction_no
    # param1: faction_no
    # param2: all_vassals_included, (becomes 1 if we want to find attackable center if we collected 20% of vassals during gathering army phase)
    # OUTPUT:
    # reg0 = center_to_attack (-1 if none is logical)
    # reg1 = maximum_attack_score
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
    ]),

    #script_find_center_to_defend
    # INPUT:
    # param1: faction_no
    # OUTPUT:
    # reg0 = center_to_defend (-1 if none is logical)
    # reg1 = maximum_defend_score
    # reg3 = enemy_strength_near_most_threatened_center
    (
    "find_center_to_defend",
    [
      (store_script_param, ":troop_no", 1),

	  (store_faction_of_troop, ":faction_no", ":troop_no"),

      (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
      (faction_get_slot, ":current_ai_state", ":faction_no", slot_faction_ai_state),
      (assign, ":marshal_party", -1),
      (try_begin),
        (gt, ":faction_marshal", 0),
        (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
      (try_end),

      (assign, ":most_threatened_center", -1),
      (assign, ":maximum_threat_score", 0),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (store_faction_of_party, ":center_faction", ":cur_center"),
        (eq, ":center_faction", ":faction_no"),

        (party_get_slot, ":exact_enemy_strength", ":cur_center", slot_center_sortie_enemy_strength),
		#Distort this to account for questionable intelligence
		#(call_script, "script_reduce_exact_number_to_estimate", ":exact_enemy_strength"),
		#(assign, ":enemy_strength_nearby", reg0),
		(assign, ":enemy_strength_nearby", ":exact_enemy_strength"),

        (assign, ":threat_importance", 0),
        (try_begin),
          (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
          (party_slot_ge, ":cur_center", slot_center_is_besieged_by, 0),

          (call_script, "script_find_total_prosperity_score", ":cur_center"),
          (assign, ":total_prosperity_score", reg0),

          (party_get_slot, ":cur_center_strength", ":cur_center", slot_party_cached_strength),
          (val_mul, ":cur_center_strength", 4),
          (val_div, ":cur_center_strength", 3), #give 33% bonus to insiders because they are inside a castle

          #I removed below line and assigned ":cur_center_nearby_strength" to 0, because if not when defender army comes to help
          #threat become less because of high defence power but not yet enemy cleared.
          #(party_get_slot, ":cur_center_nearby_strength", ":cur_center", slot_party_nearby_friend_strength),
          (assign, ":cur_center_nearby_strength", 0),

          (val_add, ":cur_center_strength", ":cur_center_nearby_strength"), #add nearby friends and find ":cur_center_strength"

          (store_mul, ":power_ratio", ":enemy_strength_nearby", 100),
          (val_add, ":cur_center_strength", 1),
		  (val_max, ":cur_center_strength", 1),
          (val_div, ":power_ratio", ":cur_center_strength"),

          (assign, ":player_is_attacking", 0),
          (party_get_slot, ":besieger_party", ":cur_center", slot_center_is_besieged_by),
          (try_begin),
            (party_is_active, ":besieger_party"),
            (try_begin),
              (eq, ":besieger_party", "p_main_party"),
              (assign, ":player_is_attacking", 1),
              #(display_message, "@{!}DEBUG : player is attacking a center (1)"),
            (else_try),
              (store_faction_of_party, ":besieger_faction", ":besieger_party"),
              (eq, ":besieger_faction", "fac_player_faction"),
              (assign, ":player_is_attacking", 1),
              #(display_message, "@{!}DEBUG : player is attacking a center (2)"),
            (else_try),
              (party_get_attached_to, ":player_is_attached_to", "p_main_party"),
              (ge, ":player_is_attached_to", 0),
              (eq, ":player_is_attached_to", ":besieger_party"),
              (assign, ":player_is_attacking", 1),
              #(display_message, "@{!}DEBUG : player is attacking a center (3)"),
            (try_end),
          (try_end),

          (try_begin),
            (eq, ":player_is_attacking", 0),

            (try_begin),
              (lt, ":power_ratio", 40), #changes between 1..1
              (assign, ":threat_importance", 1),
            (else_try),
              (lt, ":power_ratio", 80), #changes between 1..7
              (store_sub, ":threat_importance", ":power_ratio", 40),
              (val_div, ":threat_importance", 5),
              (val_add, ":threat_importance", 1), #1
            (else_try),
              (lt, ":power_ratio", 120), #changes between 7..17
              (store_sub, ":threat_importance", ":power_ratio", 80),
              (val_div, ":threat_importance", 4),
              (val_add, ":threat_importance", 7), #1 + 6
            (else_try),
              (lt, ":power_ratio", 200),
              (store_sub, ":threat_importance", ":power_ratio", 120),
              (val_div, ":threat_importance", 10),
              (val_add, ":threat_importance", 17), #1 + 6 + 10
            (else_try),
              (assign, ":threat_importance", 25),
            (try_end),
          (else_try),
            (try_begin),
              (lt, ":power_ratio", 200), #changes between 5..25
              (store_div, ":threat_importance", ":power_ratio", 10),    #MOTO correction (thanks MOTO:) (mexxico))
              (val_add, ":threat_importance", 6 ),
            (else_try),
              (assign, ":threat_importance", 26),
            (try_end),
          (try_end),
        (else_try),
          (is_between, ":cur_center", villages_begin, villages_end),
          (party_slot_eq, ":cur_center", slot_village_state, svs_being_raided),

          (gt, ":enemy_strength_nearby", 0),

          (call_script, "script_find_total_prosperity_score", ":cur_center"),
          (assign, ":power_ratio", 100), #useless
          (assign, ":total_prosperity_score", reg0),
          (assign, ":threat_importance", 10), #if faction village is looted they lose money for shorter time period. So importance is something low (6-8).
        (try_end),

        (gt, ":threat_importance", 0),

        (try_begin),
          (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
          (assign, ":enemy_strength_nearby_score", 120),

          (try_begin),
            (ge, ":marshal_party", 0),
            (party_is_active, ":marshal_party"),
            (store_distance_to_party_from_party, ":marshal_dist_to_cur_center", ":marshal_party", ":cur_center"),
          (else_try),
            (assign, ":marshal_dist_to_cur_center", 100),
          (try_end),

          (try_begin),
            #if currently our target is ride to break a siege then
            #divide marshal_distance for other center's to "2" instead of "4" and add some small more distance to avoid easily
            #changing mind during siege because of small score differences.

	        #(faction_get_slot, ":current_ai_state", ":faction_no", slot_faction_ai_state),
            (eq, ":current_ai_state", sfai_attacking_enemies_around_center),
            (faction_get_slot, ":current_ai_object", ":faction_no", slot_faction_ai_object),
            (is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
            (neq, ":current_ai_object", ":cur_center"),
            (val_mul, ":marshal_dist_to_cur_center", 2),
            (val_add, ":marshal_dist_to_cur_center", 20),
          (try_end),

          (val_mul, ":marshal_dist_to_cur_center", 2), #standard multipication (1.5x) to adjust distance scoring same with formula at find_center_to_attack
          #(val_div, ":marshal_dist_to_cur_center", 2),

          (try_begin),
            (lt, ":marshal_dist_to_cur_center", 10), #very close (100p)
            (assign, ":distance_score", 100),
          (else_try),
            (lt, ":marshal_dist_to_cur_center", 160), #close (50p-100p)
            (store_sub, ":distance_score", ":marshal_dist_to_cur_center", 10),
            (val_div, ":distance_score", 3),
            (store_sub, ":distance_score", 100, ":distance_score"),
          (else_try),
            (lt, ":marshal_dist_to_cur_center", 360), #far (10p-50p)
            (store_sub, ":distance_score", ":marshal_dist_to_cur_center", 250),
            (val_div, ":distance_score", 5),
            (store_sub, ":distance_score", 50, ":distance_score"),
          (else_try),
            (assign, ":distance_score", 10), #very far
          (try_end),
        (else_try),
          (store_add, ":enemy_strength_nearby_score", ":enemy_strength_nearby", 20000),
          (val_div, ":enemy_strength_nearby_score", 200),
          (assign, ":distance_score", 70), #not related to marshal's position, because everybody is going same place (no gathering in most village raids)
        (try_end),

		##diplomacy start+
		(try_begin),
			#AI changes LOW: Give priority to defending centers with lords
			(le, DPLMC_AI_CHANGES_LOW, "$g_dplmc_ai_changes"),
			(party_slot_ge, ":cur_center", slot_town_lord, 0),
			(val_mul, ":threat_importance", 120),
			(val_div, ":threat_importance", 100),
		(try_end),
		##diplomacy end+
        (store_mul, ":threat_score", ":enemy_strength_nearby_score", ":total_prosperity_score"),
        (val_mul, ":threat_score", ":threat_importance"),
        (val_mul, ":threat_score", ":distance_score"),
        (val_div, ":threat_score", 10000),

        (try_begin),
		  (ge, "$cheat_mode", 1),
          (gt, ":threat_score", 0),
          (eq, ":faction_no", "fac_kingdom_6"),
          (assign, reg0, ":threat_score"),
          (str_store_party_name, s32, ":cur_center"),
          (assign, reg1,  ":total_prosperity_score"),
          (assign, reg2, ":enemy_strength_nearby_score"),
          (assign, reg3, ":threat_importance"),
          (assign, reg4, ":distance_score"),
          #(display_message, "@{!}DEBUG : defend of {s32} is {reg0}, prosperity:{reg1}, enemy nearby:{reg2}, threat importance:{reg3}, distance: {reg4}"),
        (try_end),

        (gt, ":threat_score", ":maximum_threat_score"),

        (assign, ":most_threatened_center", ":cur_center"),
        (assign, ":maximum_threat_score", ":threat_score"),
        (assign, ":enemy_strength_near_most_threatened_center", ":enemy_strength_nearby"),
      (try_end),

      (val_mul, ":maximum_threat_score", 3),
      (val_div, ":maximum_threat_score", 2),

      (assign, reg0, ":most_threatened_center"),
      (assign, reg1, ":maximum_threat_score"),
      (assign, reg2, ":enemy_strength_near_most_threatened_center"),
    ]),


	#script_npc_decision_checklist_peace_or_war
   (
   "initialize_tavern_variables",
   [
     (assign, "$g_main_attacker_agent", 0),
     (assign, "$g_attacker_drawn_weapon", 0),
     (assign, "$g_start_belligerent_drunk_fight", 0),
     (assign, "$g_start_hired_assassin_fight", 0),
     (assign, "$g_belligerent_drunk_leaving", 0),
   ]),

   #script_prepare_alley_to_fight
   (
   "prepare_alley_to_fight",
   [
     (party_get_slot, ":scene_no", "$current_town", slot_town_alley),

     #(store_faction_of_party, ":faction_no", "$current_town"),

     (modify_visitors_at_site, ":scene_no"),

     (reset_visitors),
     (set_visitor, 0, "trp_player"),

     #(set_visitor, 3, ":bandit_troop"),
     (set_visitor, 3, "trp_bandit"),

     (assign, "$talked_with_merchant", 0),
     (set_jump_mission, "mt_alley_fight"),
     (jump_to_scene, ":scene_no"),
     (change_screen_mission),
   ]),

   #script_prepare_town_to_fight
   (
   "prepare_town_to_fight",
   [
     (str_store_party_name_link, s9, "$g_starting_town"),
     (str_store_string, s2, "str_save_town_from_bandits"),
     (call_script, "script_start_quest", "qst_save_town_from_bandits", "$g_talk_troop"),

     (assign, "$g_mt_mode", tcm_default),
     (store_faction_of_party, ":town_faction", "$current_town"),
     (faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_3_troop),
     (faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),
     (faction_get_slot, ":tier_4_troop", ":town_faction", slot_faction_tier_4_troop),

     (party_get_slot, ":town_scene", "$current_town", slot_town_center),

     (set_jump_mission,"mt_town_fight"), #dckplmc

     (modify_visitors_at_site, ":town_scene"),
     (reset_visitors),

     #people spawned at #32, #33, #34, #35, #36, #37, #38 and #39 are town walkers.
     (try_begin),
       #(eq, "$town_nighttime", 0),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
         (party_get_slot, ":walker_troop_id", "$current_town", ":troop_slot"),
         (gt, ":walker_troop_id", 0),
         (store_add, ":entry_no", town_walker_entries_start, ":walker_no"),

		 #dckplmc - add daggers and clubs
		 (mission_tpl_entry_set_override_flags, "mt_town_fight", ":entry_no", af_override_weapons),
		 (store_random_in_range, ":r", 0,2),
		 (try_begin),
			(eq, ":r", 0),
			(mission_tpl_entry_add_override_item, "mt_town_fight", ":entry_no", "itm_dagger"),
		 (else_try),
			(mission_tpl_entry_add_override_item, "mt_town_fight", ":entry_no", "itm_club"),
		 (try_end),

         (set_visitor, ":entry_no", ":walker_troop_id"),
       (try_end),
     (try_end),

     #guards will be spawned at #25, #26 and #27
     (set_visitors, 25, ":tier_2_troop", 1),
     (set_visitors, 26, ":tier_3_troop", 1),
     (set_visitors, 27, ":tier_4_troop", 1),

     (set_visitors, 10, "trp_looter", 1),
     (set_visitors, 11, "trp_bandit", 1),
     (set_visitors, 12, "trp_looter", 1),

     # (store_faction_of_party, ":starting_town_faction", "$g_starting_town"),
     #SB : add a few bandits alongside the looters
     (call_script, "script_center_get_bandits", "$g_starting_town", 0),
     (assign, ":bandit_troop", reg0),
     (call_script, "script_get_troop_of_merchant"),
     (assign, ":troop_of_merchant", reg0),
     (str_store_troop_name, s10, ":troop_of_merchant"),

     (set_visitors, 24, "trp_looter", 1),
     (set_visitors, 2, ":bandit_troop", 2),
     (set_visitors, 4, "trp_looter", 1),
     (set_visitors, 5, "trp_looter", 2),
     (set_visitors, 6, "trp_looter", 1),
     (set_visitors, 7, ":bandit_troop", 1),

	 #dckplmc
	 (mission_tpl_entry_set_override_flags, "mt_town_fight", 3, af_override_weapons),
	 (mission_tpl_entry_add_override_item, "mt_town_fight", 3, "itm_dagger"),
     (set_visitors, 3, ":troop_of_merchant", 1),


     #(set_jump_mission,"mt_town_fight"),
     (jump_to_scene, ":town_scene"),
     (change_screen_mission),
   ]),

   (
   "change_player_right_to_rule",
   [
     (store_script_param_1, ":right_to_rule_dif"),
     (val_add, "$player_right_to_rule", ":right_to_rule_dif"),
     (val_clamp, "$player_right_to_rule", 0, 100),
     (try_begin),
       (gt, ":right_to_rule_dif", 0),
       (display_message, "@You gain right to rule.", message_positive),
     (else_try),
       (lt, ":right_to_rule_dif", 0),
       (display_message, "@You lose right to rule.", message_negative),
     (try_end),
   ]),

     #recruiter kit begin
]
