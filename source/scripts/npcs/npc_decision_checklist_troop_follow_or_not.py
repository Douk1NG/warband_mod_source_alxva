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

npc_decision_checklist_troop_follow_or_not_scripts = [
# Jrider +
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
	])
]
