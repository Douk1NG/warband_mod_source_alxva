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

npc_decision_checklist_evaluate_enemy_center_for_attack_scripts = [
("npc_decision_checklist_evaluate_enemy_center_for_attack",
    [
      #NOTES -- LAST OFFENSIVE TIME SCORE IS NOT USED

      (store_script_param, ":troop_no", 1),
      (store_script_param, ":potential_target", 2),
      (store_script_param, ":attack_by_faction", 3),
      (store_script_param, ":all_vassals_included", 4),

      (assign, ":result", -1),
      (assign, ":explainer_string", -1),
      #(assign, ":reason_is_obvious", 0),
      (assign, ":power_ratio", 0),
      #(assign, ":hours_since_last_recce", -1),

      #(assign, ":value_of_target", 0),
      #(assign, ":difficulty_of_capture", 0),
      (store_faction_of_troop, ":faction_no", ":troop_no"),

      (try_begin),
        (eq, ":attack_by_faction", 1),
        (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
        (ge, ":faction_marshal", 0), #STEVE ADDITION TO AVOID MESSAGE SPAM
        (troop_get_slot, ":party_no", ":faction_marshal", slot_troop_leaded_party),
      (else_try),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (try_end),

      (assign, "$g_use_current_ai_object_as_s8", 0),
	  ##diplomacy start+ Use this if AI changes are enabled.
	  (party_get_slot, ":hours_since_capture", ":potential_target", dplmc_slot_center_last_transfer_time),
	  (try_begin),
	     #If the slot was uninitialized, set it to negative to indicate invalid.
	     (eq, ":hours_since_capture", 0),
		 (assign, ":hours_since_capture", -1),
	  (else_try),
	     (store_current_hours, reg0),
	     (val_sub, ":hours_since_capture", reg0),
	  (try_end),
	  #How recent counts as "recent" depends on the AI settings.
	  (try_begin),
	     (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
		 (assign, ":recency_maximum", 24 * 21),#The last three weeks
	  (else_try),
		 (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
		 (assign, ":recency_maximum", 24 * 14),#The last two weeks
	  (else_try),
	     (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		 (assign, ":recency_maximum", 24 * 7),#The last week
	  (else_try),
	     (assign, ":recency_maximum", 0),
	  (try_end),
	  ##diplomacy end+

      #THE FIRST BATCH OF DISQUALIFYING CONDITIONS DO NOT REQUIRE THE ATTACKING PARTY TO HAVE CURRENT INTELLIGENCE ON THE TARGET
      (try_begin),
        (neg|party_is_active, ":party_no"),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_party_not_active"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
        (store_faction_of_party, ":potential_target_faction", ":potential_target"),
        (store_relation, ":relation", ":potential_target_faction", ":faction_no"),
        (ge, ":relation", 0),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_is_friendly"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
        (is_between, ":potential_target", walled_centers_begin, walled_centers_end),
        (assign, ":faction_of_besieger_party", -1),
        (try_begin),
          (neg|party_slot_eq, ":potential_target", slot_center_is_besieged_by, -1),
          (party_get_slot, ":besieger_party", ":potential_target", slot_center_is_besieged_by),
          (party_is_active, ":besieger_party"),
          (store_faction_of_party, ":faction_of_besieger_party", ":besieger_party"),
        (try_end),

        (neq, ":faction_of_besieger_party", -1),
        (neq, ":faction_of_besieger_party", ":faction_no"),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_is_already_besieged"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
        (is_between, ":potential_target", villages_begin, villages_end),
        (assign, ":village_is_looted_or_raided_already", 0),
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

        (try_begin),
          (this_or_next|party_slot_eq, ":potential_target", slot_village_state, svs_looted),
          (eq, ":raiding_by_one_other_faction", 1),
          (assign, ":village_is_looted_or_raided_already", 1),
        (try_end),

        (eq, ":village_is_looted_or_raided_already", 1),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_is_looted_or_raided_already"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
	    ##diplomacy start+ Add support for companion / lady personality types: does not want to attack innocents
		(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
		(this_or_next|gt, reg0, 0),
		(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
		(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
		#diplomacy end+
        (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),

        (is_between, ":potential_target", villages_begin, villages_end),
        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_marshal_does_not_want_to_attack_innocents"),
      (else_try),
        (assign, ":distance_from_our_closest_walled_center", 1000),
        (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
           (store_faction_of_party, ":cur_center_faction", ":cur_center"),
           (eq, ":cur_center_faction", ":faction_no"),
           (store_distance_to_party_from_party, ":distance_from_cur_center", ":cur_center", ":potential_target"),
           (lt, ":distance_from_cur_center", ":distance_from_our_closest_walled_center"),
           (assign, ":distance_from_our_closest_walled_center", ":distance_from_cur_center"),
        (try_end),

        (gt, ":distance_from_our_closest_walled_center", 75),
		##diplomacy start+ Add support for companion / lady personality types: cautious
		##OLD:
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
        #(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
		##NEW:
		(call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
		(gt, reg0, 0),
		##Do not apply the check to recently-lost centers if AI changes are on.
		(this_or_next|lt, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(this_or_next|neg|party_slot_eq,":potential_target", slot_center_ex_faction, ":faction_no"),
		(this_or_next|lt, ":hours_since_capture", 0), #i.e. invalid
		(ge, ":hours_since_capture", ":recency_maximum"),#hasn't been taken recently
		##diplomacy end+

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_far_away_our_cautious_marshal_does_not_wish_to_reconnoiter"),
      #RECONNOITERING BEGINS HERE - VALUE WILL BE TEN OR LESS
      (else_try),
        (gt, ":distance_from_our_closest_walled_center", 90),
		##diplomacy start+ Do not apply the check to recently-lost centers if AI changes are on.
		(this_or_next|lt, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(this_or_next|neg|party_slot_eq,":potential_target", slot_center_ex_faction, ":faction_no"),
		(this_or_next|lt, ":hours_since_capture", 0), #i.e. invalid
		(ge, ":hours_since_capture", ":recency_maximum"),#hasn't been taken recently
		##diplomacy end+

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_far_away_even_for_our_aggressive_marshal_to_reconnoiter"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
        (is_between, ":potential_target", walled_centers_begin, walled_centers_end),
		##diplomacy start+ Add support for companion / lady personality types: aggessive
		##OLD:
        #(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
        #(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
        #(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
		##NEW:
		(call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
		(lt, reg0, 0),
		##Do not apply the check to recently-lost centers if AI changes are on.
		(this_or_next|lt, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(this_or_next|neg|party_slot_eq,":potential_target", slot_center_ex_faction, ":faction_no"),
		(this_or_next|lt, ":hours_since_capture", 0), #i.e. invalid
		(ge, ":hours_since_capture", ":recency_maximum"),#hasn't been taken recently
		##diplomacy end+

        (assign, ":close_center_found", 0),
        (try_for_range, ":friendly_walled_center", walled_centers_begin, walled_centers_end),
          (eq, ":close_center_found", 0),
          (store_faction_of_party, ":friendly_walled_center_faction", ":friendly_walled_center"),
          (eq, ":friendly_walled_center_faction", ":faction_no"),
          (store_distance_to_party_from_party, ":distance_from_walled_center", ":potential_target", ":friendly_walled_center"),
          (lt, ":distance_from_walled_center", 60),
          (assign, ":close_center_found", 1),
        (try_end),
        (eq, ":close_center_found", 0),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_is_indefensible"),
      #(else_try),
        #For now it is removed as Armagan's decision, we can add this option in later patchs. I and Armagan accept it has good potential. But this system needs also
        #scouting quests and scouting AI added together. If we only add this then we limit AI very much, it can attack only very few of centers, this damages
        #variability of game and surprise attacks of AI. Player can predict where AI will attack and he can full garnisons of only this center.
        #We can add asking travellers about how good defended center X by paying 100 denars for example to equalize situations of AI and human player.
        #But these needs much work and detailed AI tests so Armagan decided to skip this for now.

        #(store_sub, ":faction_recce_slot", ":faction_no", kingdoms_begin),
        #(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
        #(party_get_slot, ":last_recce_time", ":potential_target", ":faction_recce_slot"),
        #(store_current_hours, ":hours_since_last_recce"),
        #(val_sub, ":hours_since_last_recce", ":last_recce_time"),

        #(this_or_next|eq, ":last_recce_time", 0),
        #(gt, ":hours_since_last_recce", 96), #Information is presumed to be accurate for four days

        #(store_sub, ":150_minus_distance_div_by_10", 150, ":distance_from_party"),
        #(val_div, ":150_minus_distance_div_by_10", 10),

        #(assign, ":result", ":150_minus_distance_div_by_10"),
        #(assign, ":explainer_string", "str_center_has_not_been_scouted"),
      #DECISIONS BASED ON ENEMY STRENGTH BEGIN HERE
      (else_try),
        (party_get_slot, ":party_strength", ":party_no", slot_party_cached_strength),
        (party_get_slot, ":follower_strength", ":party_no", slot_party_follower_strength),
        (party_get_slot, ":strength_of_nearby_friend", ":party_no", slot_party_nearby_friend_strength),

        (store_add, ":total_strength", ":party_strength", ":follower_strength"),
        (val_add, ":total_strength", ":strength_of_nearby_friend"),

        #(party_get_slot, ":potential_target_nearby_enemy_exact_strength", ":potential_target", slot_party_nearby_friend_strength),
        #(assign, ":potential_target_nearby_enemy_strength", ":potential_target_nearby_enemy_exact_strength"),
        (try_begin),
          (is_between, ":potential_target", villages_begin, villages_end),
          (assign, ":enemy_strength", 10),
        (else_try),
          (party_get_slot, ":enemy_strength", ":potential_target", slot_party_cached_strength),
          (party_get_slot, ":enemy_strength_nearby", ":potential_target", slot_party_nearby_friend_strength),
          (val_add, ":enemy_strength", ":enemy_strength_nearby"),
        (try_end),
        (val_max, ":enemy_strength", 1),
		##diplomacy start+  Add support for lady/companion personalities: aggressive
		##OLD:
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
        #(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
		##NEW:
		(call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
		(lt, reg0, 0),
		###xxx yyy zzz TODO: The logic here seems backwards!
		###Later look at this and verify that it's what we want.
		##diplomacy end+

        (store_mul, ":power_ratio", ":total_strength", 100),
        (val_div, ":power_ratio", ":enemy_strength"),
        (lt, ":power_ratio", 150),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_protected_by_enemy_army_aggressive"),
      (else_try),
        (ge, ":enemy_strength", ":total_strength"), #if enemy is powerful

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_protected_by_enemy_army_cautious"),
      (else_try),
        (store_mul, ":power_ratio", ":total_strength", 100),
        (val_div, ":power_ratio", ":enemy_strength"),
        (lt, ":power_ratio", 185),
		##diplomacy start+ Add support for companion/lady personalities: cautious
		##OLD:
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
        #(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
		##NEW:
		(call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
		(gt, reg0, 0),
		##diplomacy end+

        #equations here
        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_cautious_marshal_believes_center_too_difficult_to_capture"),
      (else_try),
        (lt, ":power_ratio", 140), #it was 140

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_even_aggressive_marshal_believes_center_too_difficult_to_capture"),
      #To Steve - I moved below two if statement here from upper places, to enable in answering different different answers even
      #if we are close to an unlooted enemy village. For example now it can say "center X" is too far too while our army is
      #looting a village because of its closeness.
      (else_try),
        #if the party has already started the siege
        (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
        (faction_get_slot, ":current_object", ":faction_no", slot_faction_ai_object),
        (is_between, ":current_object", villages_begin, villages_end),
        (neq, ":potential_target", ":current_object"),
        (party_slot_eq, ":current_object", slot_village_state, svs_under_siege),

        (store_current_hours, ":hours_since_siege_began"),
        (party_get_slot, ":hour_that_siege_began", ":current_object", slot_center_siege_begin_hours),
        (val_sub, ":hours_since_siege_began", ":hour_that_siege_began"),
        (gt, ":hours_since_siege_began", 4),

        (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack", ":troop_no", ":current_object", ":attack_by_faction", 0),
        (gt, reg0, -1),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_we_have_already_committed_too_much_time_to_our_present_siege_to_move_elsewhere"),
      (else_try),
        #If the party is close to an unlooted village
        (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
        (faction_get_slot, ":current_object", ":faction_no", slot_faction_ai_object),
        (neq, ":potential_target", ":current_object"),
        (is_between, ":current_object", villages_begin, villages_end),
        (store_distance_to_party_from_party, ":distance_to_cur_object", ":party_no", ":current_object"),
        (lt, ":distance_to_cur_object", 10),

        (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack", ":troop_no", ":current_object", ":attack_by_faction", 0),
        (gt, reg0, -1),

        (assign, "$g_use_current_ai_object_as_s8", 1),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_we_are_already_here_we_should_at_least_loot_the_village"),
      #DECISION TO ATTACK IS HERE
      #(else_try),
        #To Steve - I removed below lines, as here decided. We will use pre-function to evaluate assailability scores for centers rather than below lines to make AI
        #selecting better targets. If you want to make some marshals to select not-best options I can add that option into script_calculate_center_assailability_score,
        #for that we can need seed values for each center and for each lord, so we can add these seed values to create variability, clever marshals have seeds with less
        #standard deviation and less values and less-clever marshals have bigger seeds. Then probability of some lords to disagree marshal increases because their seed
        #values will be different from marshal's. If Steve wants it from me to implement I can add this.

        #(try_begin),
        #  (is_between, ":potential_target", villages_begin, villages_end),
        #  (party_get_slot, ":score", ":potential_target", slot_town_prosperity),
        #  (val_add, ":score", 50), #average 100
        #(else_try),
        #  (is_between, ":potential_target", castles_begin, castles_end),
        #  (assign, ":score", ":power_ratio"), #ie, at least 140
        #(else_try),
        #  (party_get_slot, ":score", ":potential_target", slot_town_prosperity),
        #  (val_add, ":score", 75),
        #  (val_mul, ":score", ":power_ratio"),
        #  (val_div, ":score", 100), #ie, at least about 200
        #(try_end),
        #
        #(val_sub, ":score", ":distance_from_party"),
        #(lt, ":score", -1),

        #(assign, ":result", -1),
        #(assign, ":explainer_string", "str_center_value_outweighed_by_difficulty_of_capture"),
      (else_try),
        (try_begin),
          (eq, "$cheat_mode", 1),
          (eq, ":faction_no", "fac_kingdom_3"),
          (store_faction_of_party, ":potential_target_faction", ":potential_target"),
          (store_relation, ":relation", ":potential_target_faction", ":faction_no"),
          (lt, ":relation", 0),
        (try_end),

        (call_script, "script_calculate_center_assailability_score", ":troop_no", ":potential_target", ":all_vassals_included"),
        (assign, ":score", reg0),
        (assign, ":power_ratio", reg1),
        #(assign, ":distance_score", reg2),

        (assign, ":result", ":score"),

        (try_begin),
          (le, ":power_ratio", 100),
          (try_begin),
			##diplomacy start+ Add support for companion / lady personalities: cautious
			##OLD:
            #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
            #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
            #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
            #(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
			##NEW:
			(call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
			(gt, reg0, 0),
			##diplomacy end+
            (assign, ":explainer_string", "str_center_cautious_marshal_believes_center_too_difficult_to_capture"),
          (else_try),
            (assign, ":explainer_string", "str_center_even_aggressive_marshal_believes_center_too_difficult_to_capture"),
          (try_end),
        (else_try),
          (le, ":power_ratio", 150),

          (try_begin),
			##diplomacy start+ Add support for companion / lady personalities: cautious
			##OLD
	        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
	        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
	        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
	        #(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
			##NEW:
			(call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
			(lt, reg0, 0),
			##diplomacy end+
	        (assign, ":explainer_string", "str_center_protected_by_enemy_army_cautious"),
	      (else_try),
	        (assign, ":explainer_string", "str_center_protected_by_enemy_army_aggressive"),
	      (try_end),
	    (else_try),
	      (try_begin),
	        (le, ":score", "$g_faction_object_score"),
	        (assign, ":explainer_string", "str_center_value_outweighed_by_difficulty_of_capture"),
	      (else_try),
	        #To Steve, does not this sentence needs to explain why we are not attacking that city?
	        #This sentence says it justifies, so why we are not attacking?
	        (assign, ":explainer_string", "str_center_value_justifies_the_difficulty_of_capture"),
	      (try_end),
	    (try_end),
	  (try_end),

	  (assign, reg0, ":result"),
	  (assign, reg1, ":explainer_string"),
	  (assign, reg2, ":power_ratio"),
     ])
]
