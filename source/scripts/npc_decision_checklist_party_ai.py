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

npc_decision_checklist_party_ai_scripts = [
# script_diplomacy_start_peace_between_kingdoms
# DECISION CHECKLISTS (OCT 14)
# I was thinking of trying to convert as much AI decision-making as possible to the checklist format
# While outcomes are not as nuanced and varied as a random decision using weighted chances for each outcoms,
# the checklist has the advantage of being much more transparent, both to developers and to players
# The checklist can yield a string (standardized to s14) which explains the rationale for the decision
# When the script yields a yes/no/maybe result, than that is standardized from -3 to +3
# INPUT: troop_no
# OUTPUT: none
("npc_decision_checklist_party_ai",
	[
	#this script can replace decide_kingdom_hero_ai and decide_kingdom_hero_ai_follow_or_not
	#However, it does not contain script_party_set_ai_state

	(store_script_param, ":troop_no", 1),

	(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
    #(party_get_slot, ":our_strength", ":party_no", slot_party_cached_strength),
    #(store_div, ":min_strength_behind", ":our_strength", 2),
    #(party_get_slot, ":our_follower_strength", ":party_no", slot_party_follower_strength),

    (try_begin),
      (eq, "$cheat_mode", 1),
      (assign, "$g_talk_troop", ":troop_no"),
    (try_end),

    (store_troop_faction, ":faction_no", ":troop_no"),
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

    (try_begin),
      (eq, ":troop_no", "$g_talk_troop"),
      (str_store_string, s15, "str__i_must_attend_to_this_matter_before_i_worry_about_the_affairs_of_the_realm"),
    (try_end),

    #find current center
    (party_get_attached_to, ":cur_center_no", ":party_no"),
    (try_begin),
      (lt, ":cur_center_no", 0),
      (party_get_cur_town, ":cur_center_no", ":party_no"),
    (try_end),
    (assign, ":besieger_party", -1),
    (try_begin),
      (neg|is_between, ":cur_center_no", centers_begin, centers_end),
      (assign, ":cur_center_no", -1),
    (else_try),
      (party_get_slot, ":besieger_party", ":cur_center_no", slot_center_is_besieged_by),
      (try_begin),
        (neg|party_is_active, ":besieger_party"),
        (assign, ":besieger_party", -1),
      (try_end),
    (try_end),

    #party_count
    (call_script, "script_party_count_fit_for_battle", ":party_no"),
    (assign, ":party_fit_for_battle", reg0),
    (call_script, "script_party_get_ideal_size", ":party_no"),
    (assign, ":ideal_size", reg0),
    (store_mul, ":party_strength_as_percentage_of_ideal", ":party_fit_for_battle", 100),
    (val_div, ":party_strength_as_percentage_of_ideal", ":ideal_size"),
    (try_begin),
      (faction_slot_eq, ":faction_no", slot_faction_num_towns, 0),
      (faction_slot_eq, ":faction_no", slot_faction_num_castles, 0),
      (assign, ":party_ratio_of_prisoners", 0), #do not let prisoners have an effect on ai calculation
    (else_try),
      (party_get_num_prisoners, ":num_prisoners", ":party_no"),
      (val_max, ":party_fit_for_battle", 1), #avoid division by zero error
      (store_div, ":party_ratio_of_prisoners", ":num_prisoners", ":party_fit_for_battle"),
    (try_end),

	(assign, ":faction_is_at_war", 0),
	(try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
	  (faction_slot_eq, ":kingdom", slot_faction_state, sfs_active),
	  (store_relation, ":relation", ":faction_no", ":kingdom"),
	  (lt, ":relation", 0),
	  (assign, ":faction_is_at_war", 1),
	(try_end),

	(assign, ":operation_in_progress", 0),
	(try_begin),
	  (this_or_next|party_slot_eq, ":party_no", slot_party_ai_state, spai_raiding_around_center),
	  (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),

	  (party_get_slot, ":target_center", ":party_no", slot_party_ai_object),
	  (is_between, ":target_center", centers_begin, centers_end),

	  (store_faction_of_party, ":target_center_faction", ":target_center"),
	  (store_relation, ":relation", ":faction_no", ":target_center_faction"),
	  (lt, ":relation", 0),

	  (store_distance_to_party_from_party, ":distance", ":party_no", ":target_center"),
	  (lt, ":distance", 10),
	  (this_or_next|party_slot_eq, ":target_center", slot_village_state, svs_under_siege),
	  (this_or_next|party_slot_eq, ":target_center", slot_village_state, svs_normal),
	  (party_slot_eq, ":target_center", slot_village_state, svs_being_raided),

	  (assign, ":operation_in_progress", 1),
	(try_end),

	(troop_get_slot, ":troop_reputation", ":troop_no", slot_lord_reputation_type),

    (party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),
    (party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),

	(party_get_slot, ":party_cached_strength", ":party_no", slot_party_cached_strength),

	(store_current_hours, ":hours_since_last_rest"),
	(party_get_slot, ":last_rest_time", ":party_no", slot_party_last_in_any_center),
	(val_sub, ":hours_since_last_rest", ":last_rest_time"),

	(store_current_hours, ":hours_since_last_home"),
	(party_get_slot, ":last_home_time", ":party_no", slot_party_last_in_home_center),
	(val_sub, ":hours_since_last_home", ":last_home_time"),

	(store_current_hours, ":hours_since_last_combat"),
	(party_get_slot, ":last_combat_time", ":party_no", slot_party_last_in_combat),
	(val_sub, ":hours_since_last_combat", ":last_combat_time"),

	(store_current_hours, ":hours_since_last_courtship"),
	(party_get_slot, ":last_courtship_time", ":party_no", slot_party_leader_last_courted),
	(val_sub, ":hours_since_last_courtship", ":last_courtship_time"),

    (troop_get_slot, ":temp_ai_seed", ":troop_no", slot_troop_temp_decision_seed),
    (store_mod, ":aggressiveness", ":temp_ai_seed", 73), #To derive the
    (try_begin),
      (eq, ":troop_reputation", lrep_martial),
      (val_add, ":aggressiveness", 27),
    (else_try),
      (neq, ":troop_reputation", lrep_debauched),
      (neq, ":troop_reputation", lrep_quarrelsome),
      (val_add, ":aggressiveness", 14),
    (try_end),

    (try_begin),
      (gt, ":aggressiveness", ":hours_since_last_combat"),
      (val_add, ":aggressiveness", ":hours_since_last_combat"),
      (val_div, ":aggressiveness", 2),
    (try_end),

    (try_begin),
      (eq, "$cheat_mode", 1), #100
      (eq, ":troop_no", "$g_talk_troop"),
      (str_store_troop_name, s4, ":troop_no"),
      (assign, reg3, ":hours_since_last_rest"),
      (assign, reg4, ":hours_since_last_courtship"),
      (assign, reg5, ":hours_since_last_combat"),
      (assign, reg6, ":hours_since_last_home"),
      (assign, reg7, ":aggressiveness"),
      #(display_message, "@{!}{s4}: hours since rest {reg3}, courtship {reg4}, combat {reg5}, home {reg6}, aggressiveness {reg7}"),
    (try_end),

	##I am inspecting an estate (use slot_center_npc_volunteer_troop_amount)

	(str_store_string, s17, "str_the_other_matter_took_precedence"),

	(assign, ":do_only_collecting_rents", 0),

	#Wait in current city (dangerous to travel with less (<=10) men)
	(try_begin),
      #NOTE : I added also this condition to very top of list. Because if this condition does not exists in top then a bug happens.
      #Bug is about alone wounded lords without any troop near him travels between cities, sometimes it want to return his home city
      #to collect reinforcements, sometimes it want to patrol ext, but his party is so weak even without anyone. So we sometimes see
      #(0/1) parties in map with only one wounded lord inside. Because after wars completely defeated lords spawn again in a walled center
      #in 48 hours periods (by codes in module_simple_trigers). He spawns with only wounded himself. Then he should wait in there for
      #a time to collect new men to his (0/1) party. If a lord is the only one in his party and if he is at any walled center already then he
      #should stay where he is. He should not travel to anywhere because of any reason. If he is the only one and he is wounded and
      #he is not in any walled center this means this situation happens because of one another bug, because any lord cannot be out of
      #walled centers with wounded himself only. So I am adding this condition below.

      #SUMMARY : If lord has not got enought troops (<10 || <10%) with himself and he is currently at a walled center he should not leave
      #his current center because of any reason.

      (ge, ":cur_center_no", 0),

      (this_or_next|le, ":party_fit_for_battle", 10),
      (le, ":party_strength_as_percentage_of_ideal", 30),

      (assign, ":action", spai_holding_center),
      (assign, ":object", ":cur_center_no"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_need_to_raise_some_men_before_attempting_anything_else"),
	    (str_store_string, s16, "str_i_need_to_raise_some_men_before_attempting_anything_else"),
	  (try_end),

	#Stand in a siege
	(else_try),
	  (gt, ":besieger_party", -1),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":cur_center_no"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_cannot_leave_this_fortress_now_as_it_is_under_siege"),
	    (str_store_string, s16, "str_after_all_we_are_under_siege"),
	  (try_end),

	#Continue retreat to walled center
	(else_try),
	  (eq, ":old_ai_state", spai_retreating_to_center),
	  (neg|party_is_in_any_town, ":party_no"),

	  (ge, ":old_ai_object", 0),
	  (party_is_active, ":old_ai_object"),

	  (store_faction_of_party, ":retreat_center_faction", ":old_ai_object"),
	  (eq, ":faction_no", ":retreat_center_faction"),

	  (assign, ":action", spai_retreating_to_center),
	  (assign, ":object", ":old_ai_object"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_we_are_not_strong_enough_to_face_the_enemy_out_in_the_open"),
	    (str_store_string, s16, "str_i_should_probably_seek_shelter_behind_some_stout_walls"),
	  (try_end),

	#Stand by in current center against enemies
	(else_try),
	  (is_between, ":cur_center_no", walled_centers_begin, walled_centers_end),

	  (party_get_slot, ":enemy_strength_in_area", ":cur_center_no", slot_center_sortie_enemy_strength),
	  (party_get_slot, ":enemy_strength_in_area", ":cur_center_no", slot_center_sortie_enemy_strength),
	  (ge, ":enemy_strength_in_area", 50),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":cur_center_no"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_enemies_are_reported_to_be_nearby_and_we_should_stand_ready_to_either_man_the_walls_or_sortie_out_to_do_battle"),
	    (str_store_string, s16, "str_the_enemy_is_nearby"),
	  (try_end),

	#As the marshall, lead faction campaign
	(else_try),
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  (str_clear, s15), #Does not say that overrides faction orders
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),

	  (party_set_ai_initiative, ":party_no", 10),

	  #new ozan added - active gathering
	  #this code will allow marshal to travel around cities while gathering army if currently collected are less than 60%.
	  #By ratio increases travel distances become less. Travels will be only points around walled centers.
	  (party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),
	  (assign, ":travel_target", ":old_ai_object"),

      (call_script, "script_find_center_to_defend", ":troop_no"),
	  (assign, ":most_threatened_center", reg0),
	  (assign, ":travel_target_new_assigned", 0),

      (try_begin),
        (lt, ":old_ai_object", 0),

        (store_random_in_range, ":random_value", 0, 8), #to eanble marshal to wait sometime during active gathering
        (this_or_next|eq, "$g_gathering_new_started", 1),
        (eq, ":random_value", 0),

        (assign, ":vassals_already_assembled", 0),
        (assign, ":total_vassals", 0),
        (try_for_range, ":lord", active_npcs_begin, active_npcs_end),
          (store_faction_of_troop, ":lord_faction", ":lord"),
          (eq, ":lord_faction", ":faction_no"),
          (troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
          (party_is_active, ":led_party"),
          (val_add, ":total_vassals", 1),

          (party_slot_eq, ":led_party", slot_party_ai_state, spai_accompanying_army),
          (party_slot_eq, ":led_party", slot_party_ai_object, ":party_no"),

          (party_is_active, ":party_no"),
          (store_distance_to_party_from_party, ":distance_to_marshal", ":led_party", ":party_no"),
          (lt, ":distance_to_marshal", 15),
          (val_add, ":vassals_already_assembled", 1),
        (try_end),

        (assign, ":ratio_of_vassals_assembled", -1),
        (try_begin),
          (gt, ":total_vassals", 0),
          (store_mul, ":ratio_of_vassals_assembled", ":vassals_already_assembled", 100),
          (val_div, ":ratio_of_vassals_assembled", ":total_vassals"),
        (try_end),

        (try_begin),
          #if more than 35% of vassals already collected do not make any more active gathering, just hold and wait last vassals to participate.
          (le, ":ratio_of_vassals_assembled", 35),

          (assign, ":best_center_to_travel", ":most_threatened_center"),

          (try_begin),
            (eq, "$g_gathering_new_started", 1),

            (assign, ":minimum_distance", 100000),
            (try_for_range, ":center_no", centers_begin, centers_end),
              (store_faction_of_party, ":center_faction", ":center_no"),
              (eq, ":center_faction", ":faction_no"), #200
              (try_begin),
                (neq, ":center_no", ":most_threatened_center"),
                (store_distance_to_party_from_party, ":dist", ":party_no", ":center_no"),
                (lt, ":dist", ":minimum_distance"),
                (assign, ":minimum_distance", ":dist"),
                (assign, ":best_center_to_travel", ":center_no"),
              (try_end),
            (try_end),
          (else_try),
            #active gathering
            (assign, ":max_travel_distance", 150),
            (try_begin),
              (ge, ":ratio_of_vassals_assembled",15),
              (store_sub, ":max_travel_distance", 35, ":ratio_of_vassals_assembled"),
              (val_add, ":max_travel_distance", 5), #5..25
              (val_mul, ":max_travel_distance", 6), #30..150
            (try_end),

            (try_begin),
              (ge, ":most_threatened_center", 0),
              (store_distance_to_party_from_party, reg12, ":party_no", ":most_threatened_center"),
            (else_try),
              (assign, reg12, 0),
            (try_end),

            (assign, ":num_centers", 0),
            (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
              (store_faction_of_party, ":center_faction", ":center_no"),
              (eq, ":center_faction", ":faction_no"),
              (try_begin),
                #(ge, ":max_travel_distance", 0),
                (store_distance_to_party_from_party, ":dist", ":party_no", ":center_no"),

                (try_begin),
                  (ge, ":most_threatened_center", 0),
                  (store_distance_to_party_from_party, reg13, ":center_no", ":most_threatened_center"),
                (else_try),
                  (assign, reg13, 0),
                (try_end),

                (store_sub, reg11, reg13, reg12),

                (this_or_next|ge, reg11, 40),
                (this_or_next|ge, ":dist", ":max_travel_distance"),
                (eq, ":center_no", ":most_threatened_center"),
              (else_try),
                #this center is a candidate so increase num_centers by one.
                (val_add, ":num_centers", 1),
              (try_end),
            (try_end),

            (try_begin),
              (ge, ":num_centers", 0),
              (store_random_in_range, ":random_center_no", 0, ":num_centers"),
              (val_add, ":random_center_no", 1),
              (assign, ":num_centers", 0),
              (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
                (store_faction_of_party, ":center_faction", ":center_no"),
                (eq, ":center_faction", ":faction_no"),
                (try_begin),
                  (neq, ":center_no", ":most_threatened_center"),
                  (store_distance_to_party_from_party, ":dist", ":party_no", ":center_no"),
                  (lt, ":dist", ":max_travel_distance"),

                  (try_begin),
                    (ge, ":most_threatened_center", 0),
                    (store_distance_to_party_from_party, reg13, ":center_no", ":most_threatened_center"),
                  (else_try),
                    (assign, reg13, 0),
                  (try_end),

                  (store_sub, reg11, reg13, reg12),
                  (lt, reg11, 40),

                  (val_sub, ":random_center_no", 1),
                  (eq, ":random_center_no", 0),
                  (assign, ":best_center_to_travel", ":center_no"),
                (try_end),
              (try_end),
            (try_end),
          (try_end),

          (assign, ":travel_target", ":best_center_to_travel"),
          (assign, ":travel_target_new_assigned", 1),
        (try_end),
      (else_try),
        #if party has an ai object and they are close to that object while gathering army,
        #forget that ai object so they will select a new ai object next.
        (is_between, ":old_ai_object", centers_begin, centers_end),
        (party_get_position, pos1, ":party_no"),
        (party_get_position, pos2, ":old_ai_object"),
        (get_distance_between_positions, ":dist", pos1, pos2),
        (le, ":dist", 3),
        (assign, ":travel_target", -1),
      (try_end),
      #end ozan

      (try_begin),
        (eq, ":travel_target", -1),
        (assign, ":action", spai_undefined),
      (else_try),
        (assign, ":action", spai_visiting_village),
      (try_end),

      (assign, ":object", ":travel_target"),

      (try_begin),
        (eq, ":troop_no", "$g_talk_troop"),
        (try_begin),
          (eq, ":travel_target", -1),
          (str_store_string, s14, "str_as_the_marshall_i_am_assembling_the_army_of_the_realm"),
        (else_try),
          (try_begin),
            (eq, ":faction_no", "$players_kingdom"),
            (eq, ":travel_target_new_assigned", 1),
            (le, "$number_of_report_to_army_quest_notes", 13),
            (check_quest_active, "qst_report_to_army"),
            (str_store_party_name_link, s10, ":travel_target"),

            (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall), #300

            (str_store_troop_name_link, s11, ":faction_marshal"),
            (store_current_hours, ":hours"),
            (call_script, "script_game_get_date_text", 0, ":hours"),

            (str_store_string, s14, "str_as_the_marshall_i_am_assembling_the_army_of_the_realm_and_travel_to_lands_near_s10_to_inform_more_vassals"),
            (str_store_string, s14, "@({s1}) {s11}: {s14}"),
            (add_quest_note_from_sreg, "qst_report_to_army", "$number_of_report_to_army_quest_notes", s14, 0),
            (val_add, "$number_of_report_to_army_quest_notes", 1),
          (try_end),

          (assign, reg0, ":travel_target"),
          (str_store_party_name, s10, ":travel_target"),
          (str_store_string, s14, "str_as_the_marshall_i_am_assembling_the_army_of_the_realm_and_travel_to_lands_near_s10_to_inform_more_vassals"),
        (try_end),
        (str_store_string, s16, "str_i_intend_to_assemble_the_army_of_the_realm"),
      (try_end),
	(else_try),
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
	  (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),

	  (assign, ":action", spai_besieging_center),
	  (assign, ":object", ":faction_object"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_as_the_marshall_i_am_leading_the_siege"),
	    (str_store_string, s16, "str_i_intend_to_begin_the_siege"),
	  (try_end),

	(else_try),
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
	  (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),

	  (assign, ":action", spai_raiding_around_center),
	  (assign, ":object", ":faction_object"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_as_the_marshall_i_am_leading_our_raid"),
	    (str_store_string, s16, "str_i_intend_to_start_our_raid"),
	  (try_end),

	(else_try),
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
	  (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
	  (party_is_active, ":faction_object"),

	  #moved (party_set_ai_initiative, ":party_no", 10), #new to avoid losing time of marshal with attacking unimportant targets while there is a threat in our centers.

	  (party_get_battle_opponent, ":besieger_party", ":faction_object"),

	  (try_begin),
	    (gt, ":besieger_party", 0),
        (party_is_active, ":besieger_party"),

	    (assign, ":action", spai_engaging_army),
	    (assign, ":object", ":besieger_party"),
	    (try_begin),
          (eq, ":troop_no", "$g_talk_troop"),
          (str_store_string, s14, "str_as_the_marshall_i_am_leading_our_forces_to_engage_the_enemy_in_battle"),
          (str_store_string, s16, "str_i_intend_to_lead_our_forces_out_to_engage_the_enemy"),
        (try_end),
      (else_try),
        (assign, ":action", spai_patrolling_around_center),
        (assign, ":object", ":faction_object"),
        (try_begin),
          (eq, ":troop_no", "$g_talk_troop"),
          (str_store_string, s14, "str_as_the_marshall_i_am_leading_our_forces_in_search_of_the_enemy"),
          (str_store_string, s16, "str_i_intend_to_lead_our_forces_out_to_find_the_enemy"),
        (try_end),
      (try_end),

    (else_try),
      (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemy_army),
      (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
      (party_is_active, ":faction_object"),

      (assign, ":action", spai_engaging_army),
      (assign, ":object", ":faction_object"),
      (try_begin),
        (eq, ":troop_no", "$g_talk_troop"),
        (str_store_string, s14, "str_as_the_marshall_i_am_leading_our_forces_to_engage_the_enemy_in_battle"),
        (str_store_string, s16, "str_i_intend_to_lead_our_forces_out_to_engage_the_enemy"),
      (try_end),

	#Get reinforcements
	(else_try),
	  (assign, ":lowest_acceptable_strength_percentage", 30),

	  #if troop has enought gold then increase by 10%
	  #(troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
	  #(try_begin),
	  #  (ge, ":cur_wealth", 2000),
	  #  (assign, ":wealth_addition", 10),
	  #(else_try),
	  #  (store_div, ":wealth_addition", ":cur_wealth", 200),
	  #(try_end),
	  #(val_add, ":lowest_acceptable_strength_percentage", ":wealth_addition"),

	  (call_script, "script_lord_get_home_center", ":troop_no"),
	  (assign, ":home_center", reg0),
	  (gt, ":home_center", -1),
	  (party_slot_eq, ":home_center", slot_town_lord, ":troop_no"), #newly added

	  #if troop is very close to its home center increase by 20%
	  (assign, ":distance_addition", 0),
	  (party_get_position, pos0, ":home_center"),
	  (party_get_position, pos1, ":party_no"),
	  (get_distance_between_positions, ":dist", pos0, pos1),

	  (try_begin),
	    (le, ":dist", 9000),
	    (store_div, ":distance_addition", ":dist", 600),
	    (store_sub, ":distance_addition", 15, ":distance_addition"),
	  (else_try),
	    (assign, ":distance_addition", 0),
	  (try_end),
	  (val_add, ":lowest_acceptable_strength_percentage", ":distance_addition"),

	  #if there is no campaign for faction increase by 35%
	  (assign, ":no_campaign_addition", 35),
	  (try_begin),
	    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemy_army),
	    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
	    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
	    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
	    (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
	    (assign, ":no_campaign_addition", 0),

	    #If marshal is player itself and if there is a campaign then lower lowest_acceptable_strength_percentage by 10 instead of not changing it.
	    #Because players become confused when they see very less participation from AI lords to their campaigns.
	    (try_begin), #400
	      (faction_slot_eq, ":faction_no", slot_faction_marshall, "trp_player"),
	      (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
	      (try_begin),
	        (eq, ":reduce_campaign_ai", 0), #hard
	        (assign, ":no_campaign_addition", 0),
	      (else_try),
	        (eq, ":reduce_campaign_ai", 1), #medium
	        (assign, ":no_campaign_addition", -10),
	      (else_try),
	        (eq, ":reduce_campaign_ai", 2), #easy
	        (assign, ":no_campaign_addition", -15),
	      (try_end),
	    (try_end),
	  (try_end),
	  (val_add, ":lowest_acceptable_strength_percentage", ":no_campaign_addition"),
  	  (val_max, ":lowest_acceptable_strength_percentage", 25),

	  #max : 30%+15%+35% = 80% (happens when there is no campaign and player is near to its home center.)
	  (lt, ":party_strength_as_percentage_of_ideal", ":lowest_acceptable_strength_percentage"),

	  (try_begin),
	    (store_div, ":lowest_acceptable_strength_percentage_div_3", ":lowest_acceptable_strength_percentage", 3),
	    (ge, ":party_strength_as_percentage_of_ideal", ":lowest_acceptable_strength_percentage_div_3"),
	    (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth),
	    (le, ":troop_wealth", 1800),
	    (assign, ":do_only_collecting_rents", 1),
	  (try_end),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":home_center"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_dont_have_enough_troops_and_i_need_to_get_some_more"),

	    (str_store_string, s16, "str_i_am_running_low_on_troops"),
	  (try_end),

	  (eq, ":do_only_collecting_rents", 0),

	#follow player orders
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (party_slot_ge, ":party_no", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),

	  (party_get_slot, ":orders_type", ":party_no", slot_party_orders_type),
	  (party_get_slot, ":orders_object", ":party_no", slot_party_orders_object),
	  (party_get_slot, ":orders_time", ":party_no", slot_party_orders_time),

	  (ge, ":orders_object", 0),

	  (store_current_hours, ":hours_since_orders_given"),
	  (val_sub, ":hours_since_orders_given", ":orders_time"),
     ##diplomacy start+ If the player set the Centralization value, modify the
     #maximum time vassals will follow commands by a maximum of +/- 25%
     #(normally the maximum is 48 hours, so that would be +/- 12 hours).
     (store_mul, reg0, ":centralization", 4),
     (val_clamp, reg0, -12, 12),#<-- This should be unnecessary
     (val_sub, ":hours_since_orders_given", reg0),
     ##diplomacy end+

	  (party_is_active, ":orders_object"),
	  (party_get_slot, ":object_state", ":orders_object", slot_village_state),
	  (store_faction_of_party, ":object_faction", ":orders_object"),
	  (store_relation, ":relation_with_object", ":faction_no", ":object_faction"),

	  (assign, ":orders_are_appropriate", 1),
	  (try_begin),
	    (gt, ":hours_since_orders_given", 48),
	    (assign, ":orders_are_appropriate", 0),
	  (else_try),
	    (eq, ":orders_type", spai_raiding_around_center),
	    (this_or_next|ge, ":relation_with_object", 0),
	    (ge, ":object_state", 2),
	    (assign, ":orders_are_appropriate", 0),
	  (else_try),
	    (eq, ":orders_type", spai_besieging_center),
	    (ge, ":relation_with_object", 0),
	    (assign, ":orders_are_appropriate", 0),
	  (else_try),
	    (this_or_next|eq, ":orders_type", spai_holding_center),
	    (this_or_next|eq, ":orders_type", spai_retreating_to_center),
	    (this_or_next|eq, ":orders_type", spai_accompanying_army),
	    (eq, ":orders_type", spai_visiting_village),
	    (le, ":relation_with_object", 0),
	    (assign, ":orders_are_appropriate", 0),
	  (try_end),

	  (eq, ":orders_are_appropriate", 1),

	  (assign, ":action", ":orders_type"),
	  (assign, ":object", ":orders_object"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_we_are_following_your_direction"),
	  (try_end),

	#Host of player wedding
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":operation_in_progress", 0),
	  (check_quest_active, "qst_wed_betrothed"),
	  (quest_slot_eq, "qst_wed_betrothed", slot_quest_giver_troop, ":troop_no"),
	  (quest_get_slot, ":bride", "qst_wed_betrothed", slot_quest_target_troop),
	  (call_script, "script_get_kingdom_lady_social_determinants", ":bride"),
	  (assign, ":wedding_venue", reg1),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":wedding_venue"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_need_to_make_preparations_for_your_wedding"),
	    (str_store_string, s16, "str_after_all_i_need_to_make_preparations_for_your_wedding"),
	  (try_end),

	#Bridegroom at player wedding
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":operation_in_progress", 0),
	  (check_quest_active, "qst_wed_betrothed_female"),
	  (quest_slot_eq, "qst_wed_betrothed_female", slot_quest_giver_troop, ":troop_no"),

	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
	  (faction_get_slot, ":feast_venue", ":faction_no", slot_faction_ai_object),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":feast_venue"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_am_heading_to_the_site_of_our_wedding"), #500
	    (str_store_string, s16, "str_after_all_we_are_soon_to_be_wed"),
	  (try_end),

	#Host of other feast
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":operation_in_progress", 0),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
	  (faction_get_slot, ":feast_venue", ":faction_no", slot_faction_ai_object),
	  (party_slot_eq, ":feast_venue", slot_town_lord, ":troop_no"),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":feast_venue"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_am_hosting_a_feast_there"),
	    (str_store_string, s16, "str_i_have_a_feast_to_host"),
	  (try_end),

	#I am the bridegroom at a feast
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":operation_in_progress", 0),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
	  (troop_get_slot, ":troop_betrothed", ":troop_no", slot_troop_betrothed),
	  (is_between, ":troop_betrothed", kingdom_ladies_begin, kingdom_ladies_end),

	  (faction_get_slot, ":feast_venue", ":faction_no", slot_faction_ai_object),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":feast_venue"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_am_to_be_the_bridegroom_there"),
	    (str_store_string, s16, "str_my_wedding_day_draws_near"),
	  (try_end),

	#Drop off prisoners
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (gt,  ":party_ratio_of_prisoners", 35),
	  (eq, ":operation_in_progress", 0),

	  (call_script, "script_lord_get_home_center", ":troop_no"),
	  (assign, ":home_center", reg0),

	  (gt, ":home_center", -1),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":home_center"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_have_too_much_loot_and_too_many_prisoners_and_need_to_secure_them"),
	    (str_store_string, s16, "str_i_should_think_of_dropping_off_some_of_my_prisoners"),
	  (try_end),

	#Reinforce a weak center
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (assign, ":center_to_reinforce", -1),
	  (assign, ":center_reinforce_score", 100),
	  (eq, ":operation_in_progress", 0),

	  (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
	    (party_slot_eq, ":walled_center", slot_town_lord, ":troop_no"),
	    (party_get_slot, ":center_strength", ":walled_center", slot_party_cached_strength),
	    (lt, ":center_strength", ":center_reinforce_score"),
	    (assign, ":center_to_reinforce", ":walled_center"),
	    (assign, ":center_reinforce_score", ":center_strength"),
	  (try_end),

	  (gt, ":center_to_reinforce", -1),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":center_to_reinforce"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_need_to_reinforce_it_as_it_is_poorly_garrisoned"),
	    (str_store_string, s16, "str_there_is_a_hole_in_our_defenses"),
	  (try_end),

	#Continue screening, if already doing so
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":old_ai_state", spai_screening_army), #566

	  (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
          (ge, ":faction_marshal", 0),
	  (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
	  (party_is_active, ":marshal_party"),

	  (call_script, "script_npc_decision_checklist_troop_follow_or_not", ":troop_no"),
	  (eq, reg0, 1),

	  (assign, ":action", spai_screening_army),
	  (assign, ":object", ":marshal_party"),
	  (try_begin),
	    (eq, "$g_talk_troop", ":troop_no"),
	    (str_store_string, s14, "str_i_am_following_the_marshals_orders"),
	    (str_store_string, s16, "str_the_marshal_has_given_me_this_command"),
	  (try_end),

    (else_try), #special case for sfai_attacking_enemies_around_center for village raids
      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
      (is_between, ":faction_object", villages_begin, villages_end),

      (call_script, "script_npc_decision_checklist_troop_follow_or_not", ":troop_no"),
      (eq, reg0, 1),

      (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
      (party_get_slot, ":raider_party", ":faction_object", slot_village_raided_by),
      (party_is_active, ":raider_party"),

      #think about adding one more condition here, what if raider army is so powerfull, again lords will go and engage enemy one by one?
      (party_get_slot, ":enemy_strength_nearby", ":faction_object", slot_center_sortie_enemy_strength),
      (lt, ":enemy_strength_nearby", 4000),
      #end think

      (assign, ":action", spai_engaging_army),
      (assign, ":object", ":raider_party"),
      (try_begin),
        (eq, ":troop_no", "$g_talk_troop"),
        (str_store_string, s14, "str_our_realm_needs_my_support_there_is_enemy_raiding_one_of_our_villages_which_is_not_to_far_from_here_i_am_going_there"),
        (str_store_string, s16, "str_the_marshal_has_issued_a_summons"),
      (try_end),

	#Follow the marshall's orders - if on the offensive, and the campaign has not lasted too long. Readiness is currently randomly set
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (call_script, "script_npc_decision_checklist_troop_follow_or_not", ":troop_no"),
	  (eq, reg0, 1),

	  (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
          (ge, ":faction_marshal", 0),
	  (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),

	  (assign, ":action", spai_accompanying_army),
	  (assign, ":object", ":marshal_party"),

	  (try_begin),
	    (eq, "$g_talk_troop", ":troop_no"),
	    (str_store_string, s14, "str_i_am_answering_the_marshals_summons"),
	    (str_store_string, s16, "str_the_marshal_has_issued_a_summons"),
	  (try_end),

	#Support a nearby ally who is on the offensive
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":faction_is_at_war", 1),

	  (assign, ":party_to_support", -1),
	  (try_for_range, ":allied_hero", active_npcs_begin, active_npcs_end),
	    (troop_slot_eq, ":allied_hero", slot_troop_occupation, slto_kingdom_hero),
	    (store_faction_of_troop, ":allied_hero_faction", ":allied_hero"),
	    (eq, ":allied_hero_faction", ":faction_no"),

	    (neq, ":allied_hero", ":troop_no"),

	    (troop_get_slot, ":allied_hero_party", ":allied_hero", slot_troop_leaded_party),
	    (gt, ":allied_hero_party", 1),
	    (party_is_active, ":allied_hero_party"),


	    (this_or_next|party_slot_eq, ":allied_hero_party", slot_party_ai_state, spai_raiding_around_center),
			(party_slot_eq, ":allied_hero_party", slot_party_ai_state, spai_besieging_center),

	    (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":allied_hero"),
	    (gt, reg0, 4),

	    (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),
	    (troop_get_slot, ":ally_renown", ":allied_hero", slot_troop_renown),
	    (le, ":troop_renown", ":ally_renown"), #Ally to support must have higher renown

	    (store_distance_to_party_from_party, ":distance", ":party_no", ":allied_hero_party"),

	    (lt, ":distance", 5),

 	    (assign, ":party_to_support", ":allied_hero_party"),
	  (try_end),
	  (gt, ":party_to_support", 0),

	  (assign, ":action", spai_accompanying_army),
	  (assign, ":object", ":party_to_support"),
	  (try_begin),
		  (eq, ":troop_no", "$g_talk_troop"),
		  (party_stack_get_troop_id, ":leader", ":object", 0),
		  (str_store_troop_name, s10, ":leader"),

		  (call_script, "script_troop_get_family_relation_to_troop", ":leader", "$g_talk_troop"),
		  (try_begin),
		    (eq, reg0, 0),
		    (str_store_string, s11, "str_comradeinarms"),
		  (try_end),
		  (str_store_string, s14, "str_i_am_supporting_my_s11_s10"),
		  (str_store_string, s16, "str_i_believe_that_one_of_my_comrades_is_in_need"),
	  (try_end),
    #I have decided to attack a vulnerable fortress
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":faction_is_at_war", 1),
	  (eq, ":operation_in_progress", 0),

	  (assign, ":walled_center_to_attack", -1),
	  (assign, ":walled_center_score", 50),

	  (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
	    (store_faction_of_party, ":walled_center_faction", ":walled_center"),
	    (store_relation, ":relation", ":faction_no", ":walled_center_faction"),
	    (lt, ":relation", 0),

	    (party_get_slot, ":center_cached_strength", ":walled_center", slot_party_cached_strength),
	    (val_mul, ":center_cached_strength", 3),
	    (val_mul, ":center_cached_strength", 2),

	    (lt, ":center_cached_strength", ":party_cached_strength"),
	    (lt, ":center_cached_strength", 750),

	    (party_slot_eq, ":walled_center", slot_village_state, svs_normal),
	    (store_distance_to_party_from_party, ":distance", ":walled_center", ":party_no"),
	    (lt, ":distance", ":walled_center_score"),

	    (assign, ":walled_center_to_attack", ":walled_center"),
	    (assign, ":walled_center_score", ":distance"),
	  (try_end),

	  (is_between, ":walled_center_to_attack", centers_begin, centers_end),

	  (assign, ":action", spai_besieging_center),
	  (assign, ":object", ":walled_center_to_attack"),
	  (try_begin),
	    (eq, "$cheat_mode", 1),
	    (str_store_faction_name, s20, ":faction_no"),
	    (str_store_party_name, s21, ":object"),
	    (display_message, "str_s20_decided_to_attack_s21"),
	  (try_end),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_a_fortress_is_vulnerable"),
	    (str_store_string, s16, "str_i_believe_that_the_enemy_may_be_vulnerable"),
	  (try_end),

	#I am visiting an estate
	(else_try),
	  (assign, ":center_to_visit", -1),
	  (assign, ":score_to_beat", 300), #at least 300 gold to pick up
	  (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth), #average troop wealth is 2000
	  (val_div, ":troop_wealth", 10), #average troop wealth 10% is is 200
	  (val_add, ":score_to_beat", ":troop_wealth"), #average score to beat is 500
	  (eq, ":operation_in_progress", 0),

	  (try_begin),
	    (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),

	    (assign, reg17, 0),
	    (try_begin),
	      (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
	      (party_slot_eq, ":party_no", slot_party_ai_object, ":faction_marshal"),
	      (assign, reg17, 1),
	    (else_try),
	      (party_slot_eq, ":party_no", slot_party_following_player, 1),
	      (assign, reg17, 1),
	    (try_end),
	    (eq, reg17, 1),

	    (try_begin),
	      (neq, ":faction_marshal", "trp_player"),
	      (neg|party_slot_eq, ":party_no", slot_party_following_player, 1),
	      (val_add, ":score_to_beat", 125),
	    (else_try),
	      (val_add, ":score_to_beat", 250),
	    (try_end),
	  (try_end),

	  (try_for_range, ":center_no", centers_begin, centers_end),
	    (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),

	    (assign, reg17, 0),
	    (try_begin),
	      (is_between, ":center_no", villages_begin, villages_end),
	      (party_slot_eq, ":center_no", slot_village_state, svs_normal),
	      (assign, reg17, 1),
	    (else_try),
	      (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
	      (assign, reg17, 1),
	    (try_end),
	    (eq, reg17, 1),

	    (party_get_slot, ":tariffs_available", ":center_no", slot_center_accumulated_tariffs),
	    (party_get_slot, ":rents_available", ":center_no", slot_center_accumulated_rents),
	    (store_add, ":money_available", ":rents_available", ":tariffs_available"),

	    (gt, ":money_available", ":score_to_beat"),
	    (assign, ":center_to_visit", ":center_no"),
	    (assign, ":score_to_beat", ":money_available"),
	  (try_end),

	  (is_between, ":center_to_visit", centers_begin, centers_end),

	  (try_begin),
	    (is_between, ":center_to_visit", walled_centers_begin, walled_centers_end),
	    (assign, ":action", spai_holding_center),
	    (assign, ":object", ":center_to_visit"),
	  (else_try),
        (assign, ":action", spai_visiting_village),
  	    (assign, ":object", ":center_to_visit"),
	  (try_end),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_need_to_inspect_my_properties_and_collect_my_dues"),
	    (str_store_string, s16, "str_it_has_been_too_long_since_i_have_inspected_my_estates"),
	  (try_end),

	#My men are weary, and I wish to return home
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (this_or_next|gt, ":hours_since_last_rest", 504), #Three weeks
	  (lt, ":aggressiveness", 25),
	  (gt, ":hours_since_last_rest", 168), #one week if aggressiveness < 25
	  (eq, ":operation_in_progress", 0),

	  (call_script, "script_lord_get_home_center", ":troop_no"),
	  (assign, ":home_center", reg0),

	  (gt, ":home_center", -1),
	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":home_center"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_my_men_are_weary_so_we_are_returning_home"),
	    (str_store_string, s16, "str_my_men_are_becoming_weary"),
	  (try_end),

	#I have a score to settle with the enemy
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (this_or_next|gt, ":hours_since_last_combat", 12),
	  (lt, ":hours_since_last_rest", 96),
	  (eq, ":operation_in_progress", 0),

	  (eq, ":faction_is_at_war", 1),
	  ##diplomacy start+ roguish lords can also do this, but humanitarian lords of any kind won't
	  (call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
	  (lt, reg0, 1),
	  (this_or_next|eq, ":troop_reputation", lrep_roguish),
	  ##diplomacy end+
	  (this_or_next|eq, ":troop_reputation", lrep_debauched),
	  (eq, ":troop_reputation", lrep_quarrelsome),

	  (assign, ":target_village", -1),
	  (assign, ":score_to_beat", 0), #based on relation

	  (try_for_range, ":possible_target", villages_begin, villages_end),
	    (store_faction_of_party, ":village_faction", ":possible_target"),
	    (store_relation, ":relation", ":village_faction", ":faction_no"),
	    (lt, ":relation", 0),

	    (neg|party_slot_ge, ":possible_target", slot_village_state, svs_looted),
	    (party_get_slot, ":town_lord", ":possible_target", slot_town_lord),
	    (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":town_lord"),
	    (assign, ":village_score", reg0),

	    (lt, ":village_score", ":score_to_beat"),
	    (assign, ":score_to_beat", ":village_score"),
	    (assign, ":target_village", ":possible_target"),
	  (try_end),

	  (is_between, ":target_village", centers_begin, centers_end),
	  (assign, ":action", spai_raiding_around_center),
	  (assign, ":object", ":target_village"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_have_a_score_to_settle_with_the_lord_there"),
	    (str_store_string, s16, "str_i_am_thinking_of_settling_an_old_score"),
	  (try_end),

	#I need money, so I am raiding where the money is
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":faction_is_at_war", 1),
	  (eq, ":operation_in_progress", 0),

	  (this_or_next|gt, ":hours_since_last_combat", 12),
	  (lt, ":hours_since_last_rest", 96),
	  (gt, ":aggressiveness", 40),

	  ##diplomacy start+
	  #Roguish lords can also do this.  Humanitarian companions will never
	  #do this, even if they otherwise have an eligible reputation.  Companions
	  #who actively enjoy raiding can also do this, regardless of whether they
	  #have an eligible reputation.
	  (call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
	  (lt, reg0, 1),
	  (this_or_next|lt, reg0, 0),
	  (this_or_next|eq, ":troop_reputation", lrep_roguish),
	  ##diplomacy end+
	  (this_or_next|eq, ":troop_reputation", lrep_debauched),
	  (this_or_next|eq, ":troop_reputation", lrep_selfrighteous),
	  (this_or_next|eq, ":troop_reputation", lrep_cunning),
	  (eq, ":troop_reputation", lrep_quarrelsome),

	  (troop_get_slot, ":wealth", ":troop_no", slot_troop_wealth),
	  (lt, ":wealth", 500),

	  (assign, ":score_to_beat", 0),
	  (assign, ":target_village", -1),

	  (try_for_range, ":possible_target", villages_begin, villages_end),
	    (store_faction_of_party, ":village_faction", ":possible_target"),
	    (store_relation, ":relation", ":village_faction", ":faction_no"),
	    (lt, ":relation", 0),

	    (this_or_next|party_slot_eq, ":possible_target", slot_village_state, svs_normal),
	    (party_slot_eq, ":possible_target", slot_village_state, svs_being_raided),

	    (party_get_slot, reg17, ":possible_target", slot_town_prosperity),
	    (store_distance_to_party_from_party, ":distance", ":party_no", ":possible_target"),
	    (val_sub, reg17, ":distance"),

	    (gt, reg17, ":score_to_beat"),
	    (assign, ":score_to_beat", reg17),
	    (assign, ":target_village", ":possible_target"),
	  (try_end),

	  (gt, ":target_village", -1),

	  (assign, ":action", spai_raiding_around_center),
	  (assign, ":object", ":target_village"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_am_short_of_money_and_i_hear_that_there_is_much_wealth_there"),
	    (str_store_string, s16, "str_i_need_to_refill_my_purse_preferably_with_the_enemys_money"),
	  (try_end),

	#Attacking wealthiest lands
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(eq, ":faction_is_at_war", 1),
		(eq, ":operation_in_progress", 0),
		(gt, ":aggressiveness", 65),

		(assign, ":score_to_beat", 0),
		(assign, ":target_village", -1),

		(try_for_range, ":possible_target", villages_begin, villages_end),
			(store_faction_of_party, ":village_faction", ":possible_target"),
			(store_relation, ":relation", ":village_faction", ":faction_no"),
			(lt, ":relation", 0),
			(neg|party_slot_eq, ":possible_target", slot_village_state, svs_looted),
			(party_get_slot, ":village_prosperity", ":possible_target", slot_town_prosperity),
			(val_mul, ":village_prosperity", 2),

			(store_distance_to_party_from_party, ":distance", ":party_no", ":possible_target"),
			(val_sub, ":village_prosperity", ":distance"),
			(gt, ":village_prosperity", ":score_to_beat"),

			(assign, ":score_to_beat", ":village_prosperity"),
			(assign, ":target_village", ":possible_target"),
		(try_end),

		##diplomacy start+ companions who hate raiding will not raid
		(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
		(lt, reg0, 1),
		##diplomacy end+
		(gt, ":target_village", -1),

		(assign, ":action", spai_raiding_around_center),
		(assign, ":object", ":target_village"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_by_striking_at_the_enemys_richest_lands_perhaps_i_can_draw_them_out_to_battle"),
			(str_store_string, s16, "str_i_am_thinking_of_going_on_the_attack"),
		(try_end),

	#End the war
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	    ##diplomacy start+
		(assign, reg0, 0),
		(try_begin),
			#A liege in service to another lord or allied with the player can do this.
			(this_or_next|eq, ":troop_reputation", lrep_none),
			(this_or_next|is_between, ":troop_no", kings_begin, kings_end),
			(is_between, ":troop_no", pretenders_begin, pretenders_end),
			(this_or_next|neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),
				(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),
			(assign, reg0, 0),
		(else_try),
			#Lords who are simulatenously Martial and tmt_honest (such as Alayen),
			#or Custodian and tmt_honest (such as Artimenner) can also do this.
			(this_or_next|eq, ":troop_reputation", lrep_martial),
			(eq, ":troop_reputation", lrep_custodian),
			(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
		(try_end),
		(this_or_next|ge, reg0, 1),
		##diplomacy end+
		(eq, ":troop_reputation", lrep_upstanding),
		(eq, ":faction_is_at_war", 1),
		(eq, ":operation_in_progress", 0),

		(assign, ":faction_to_attack", -1),
		(try_for_range, ":possible_faction_to_attack", kingdoms_begin, kingdoms_end),
			(store_relation, ":relation", ":faction_no", ":possible_faction_to_attack"),
			(lt, ":relation", 0),
			(faction_slot_eq, ":possible_faction_to_attack", slot_faction_state, sfs_active),

			(store_add, ":war_damage_inflicted_slot", ":possible_faction_to_attack", slot_faction_war_damage_inflicted_on_factions_begin),
			(val_sub, ":war_damage_inflicted_slot", kingdoms_begin),
			(faction_get_slot, ":war_damage_inflicted", ":faction_no", ":war_damage_inflicted_slot"),

			(store_add, ":war_damage_suffered_slot", ":faction_no", slot_faction_war_damage_inflicted_on_factions_begin),
			(val_sub, ":war_damage_suffered_slot", kingdoms_begin),
			(faction_get_slot, ":war_damage_suffered", ":possible_faction_to_attack", ":war_damage_suffered_slot"),

			(gt, ":war_damage_inflicted", 80),
			(lt, ":war_damage_inflicted", ":war_damage_suffered"),
			(assign, ":faction_to_attack", ":possible_faction_to_attack"),
		(try_end),

		(gt, ":faction_to_attack", -1),

		(assign, ":target_village", -1),
		(assign, ":score_to_beat", 50),

		(try_for_range, ":possible_target_village", villages_begin, villages_end),
			(store_faction_of_party, ":village_faction", ":possible_target_village"),
			(eq, ":village_faction", ":faction_to_attack"),
			(neg|party_slot_eq, ":possible_target_village", slot_village_state, svs_looted),
			(store_distance_to_party_from_party, ":distance", ":party_no", ":possible_target_village"),
			(lt, ":distance", ":score_to_beat"),

			(assign, ":score_to_beat", ":distance"),
			(assign, ":target_village", ":possible_target_village"),
		(try_end),

		(gt, ":target_village", -1),

		(assign, ":action", spai_raiding_around_center),
		(assign, ":object", ":target_village"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_perhaps_if_i_strike_one_more_blow_we_may_end_this_war_on_our_terms_"),
			(str_store_string, s16, "str_we_may_be_able_to_bring_this_war_to_a_close_with_a_few_more_blows"),
		(try_end),

	#I have a feast to attend
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
		(faction_get_slot, ":feast_venue", ":faction_no", slot_faction_ai_object),
		(party_get_slot, ":feast_host", ":feast_venue", slot_town_lord),
		(eq, ":operation_in_progress", 0),

		(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":feast_host"),
		(assign, ":relation_with_host", reg0),

        (ge, ":relation_with_host", 0),

		(assign, ":action", spai_holding_center),
		(assign, ":object", ":feast_venue"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_wish_to_attend_the_feast_there"),
			(str_store_string, s16, "str_there_is_a_feast_which_i_wish_to_attend"),
		(try_end),
	#A lady to court
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(neg|troop_slot_eq, "trp_player", slot_troop_betrothed, ":troop_no"),
		(troop_slot_eq, ":troop_no", slot_troop_spouse, -1),
		(neg|is_between, ":troop_no", kings_begin, kings_end),
		(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),


		(gt, ":hours_since_last_courtship", 72),
		(eq, ":operation_in_progress", 0),

		(assign, ":center_to_visit", -1),
		(assign, ":score_to_beat", 150),

		(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_get_slot, ":love_interest", ":troop_no", ":love_interest_slot"),
			(is_between, ":love_interest", kingdom_ladies_begin, kingdom_ladies_end),
			(troop_get_slot, ":love_interest_center", ":love_interest", slot_troop_cur_center),
			(is_between, ":love_interest_center", centers_begin, centers_end),
			(store_faction_of_party, ":love_interest_faction_no", ":love_interest_center"),
			(eq, ":faction_no", ":love_interest_faction_no"),
            #(store_relation, ":relation", ":faction_no", ":love_interest_faction_no"),
            #(ge, ":relation", 0),

			(store_distance_to_party_from_party, ":distance", ":party_no", ":love_interest_center"),

			(lt, ":distance", ":score_to_beat"),
			(assign, ":center_to_visit", ":love_interest_center"),
			(assign, ":score_to_beat", ":distance"),
        (try_end),

		(gt, ":center_to_visit", -1),

		(assign, ":action", spai_holding_center),
		(assign, ":object", ":center_to_visit"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_there_is_a_fair_lady_there_whom_i_wish_to_court"),
			(str_store_string, s16, "str_i_have_the_inclination_to_pay_court_to_a_fair_lady"),
		(try_end),

	#Patrolling an alarmed center
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(assign, ":target_center", -1),
		(assign, ":score_to_beat", 60),
		(eq, ":operation_in_progress", 0),
		(gt, ":aggressiveness", 40),

		(try_for_range, ":center_to_patrol", centers_begin, centers_end), #find closest center that has spotted enemies.
            (store_faction_of_party, ":center_faction", ":center_to_patrol"),
            (eq, ":center_faction", ":faction_no"),
			(party_slot_ge, ":center_to_patrol", slot_center_last_spotted_enemy, 0),

			#new - begin
			(party_get_slot, ":sortie_strength", ":center_to_patrol", slot_center_sortie_strength),
			(party_get_slot, ":enemy_strength", ":center_to_patrol", slot_center_sortie_enemy_strength),
			(store_mul, ":enemy_strength_mul_14_div_10", ":enemy_strength", 14),
			(val_div, ":enemy_strength_mul_14_div_10", 10),
			(party_get_slot, ":party_strength", ":party_no", slot_party_cached_strength),

			(this_or_next|neg|party_is_in_town, ":party_no", ":center_to_patrol"),
			(gt, ":sortie_strength", ":enemy_strength_mul_14_div_10"),

			(ge, ":party_strength", 100),
			#new - end

			(party_get_slot, reg17, ":center_to_patrol", slot_town_lord),
			(call_script, "script_troop_get_relation_with_troop", reg17, ":troop_no"),

			(this_or_next|eq, ":troop_reputation", lrep_upstanding),
				(gt, reg0, -5),

            (store_distance_to_party_from_party, ":distance", ":party_no", ":center_to_patrol"),
			(lt, ":distance", ":score_to_beat"),

			(assign, ":target_center", ":center_to_patrol"),
			(assign, ":score_to_beat", ":distance"),
		(try_end),

		(is_between, ":target_center", centers_begin, centers_end),

		(assign, ":action", spai_patrolling_around_center),
		(assign, ":object", ":target_center"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_we_have_heard_reports_that_the_enemy_is_in_the_area"),
			(str_store_string, s16, "str_i_have_heard_reports_of_enemy_incursions_into_our_territory"),
		(try_end),

	#Time in household
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(gt, ":hours_since_last_home", 168),
		(eq, ":operation_in_progress", 0),

		(call_script, "script_lord_get_home_center", ":troop_no"),
		(assign, ":home_center", reg0),
		(gt, ":home_center", -1),

		(assign, ":action", spai_holding_center),
		(assign, ":object", ":home_center"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_need_to_spend_some_time_with_my_household"),
			(str_store_string, s16, "str_it_has_been_a_long_time_since_i_have_been_able_to_spend_time_with_my_household"),
		(try_end),

	#Patrolling the borders
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(eq, ":faction_is_at_war", 1),
		(gt, ":aggressiveness", 65),
		(eq, ":operation_in_progress", 0),

		(assign, ":center_to_patrol", -1),
		(assign, ":score_to_beat", 75),

		(try_for_range, ":village", villages_begin, villages_end),
			(store_faction_of_party, ":village_faction", ":village"),
			(store_relation, ":relation", ":village_faction", ":faction_no"),
			(lt, ":relation", 0),

			(store_distance_to_party_from_party, ":distance", ":village", ":party_no"),
			(lt, ":distance", ":score_to_beat"),

			(assign, ":score_to_beat", ":distance"),
			(assign, ":center_to_patrol", ":village"),
		(try_end),

		(is_between, ":center_to_patrol", villages_begin, villages_end),

		(assign, ":action", spai_patrolling_around_center),
		(assign, ":object", ":center_to_patrol"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_am_watching_the_borders"),
			(str_store_string, s16, "str_i_may_be_needed_to_watch_the_borders"),
		(try_end),

	#Visiting a friend - temporarily disabled
	(else_try),
		(eq, 1, 0),

	#Patrolling home
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(call_script, "script_lord_get_home_center", ":troop_no"),
		(assign, ":home_center", reg0),

		(is_between, ":home_center", centers_begin, centers_end),
		(eq, ":operation_in_progress", 0),

		(assign, ":action", spai_patrolling_around_center),
		(assign, ":object", ":home_center"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_will_guard_the_areas_near_my_home"),
			(str_store_string, s16, "str_i_am_perhaps_needed_most_at_home"),
		(try_end),

	#Default end
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(eq, ":operation_in_progress", 0),

		(call_script, "script_lord_get_home_center", ":troop_no"),
		(assign, ":home_center", reg0),
		(is_between, ":home_center", walled_centers_begin, walled_centers_end),

		(assign, ":action", spai_holding_center),
		(assign, ":object", ":home_center"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_cant_think_of_anything_better_to_do"),
		(try_end),
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(eq, ":operation_in_progress", 1),

		(party_get_slot, ":action", ":party_no", slot_party_ai_state),
		(party_get_slot, ":object", ":party_no", slot_party_ai_object),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_am_completing_what_i_have_already_begun"),
		(try_end),
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(assign, ":action", spai_undefined),
		(assign, ":object", -1),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_dont_even_have_a_home_to_which_to_return"),
		(try_end),
	(try_end),

	(try_begin),
		(eq, "$cheat_mode", 2),
		(str_store_troop_name, s10, ":troop_no"),
		(display_message, "str_debug__s10_decides_s14_faction_ai_s15"),
	(try_end),

    (assign, reg0, ":action"),
	(assign, reg1, ":object"),
	])
]
