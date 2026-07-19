# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

kingdom_management_menus = [
  ("faction_orders",0,
   "{!}{s9}",
   "none",
   [
    (str_clear, s9),
    (store_current_hours, ":cur_hours"),
    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),

        (faction_get_slot, ":old_faction_ai_state", ":faction_no", slot_faction_ai_state),

	    (try_begin),
			(faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
			(gt, ":faction_marshal", -1),
			(assign, ":faction_ai_decider", ":faction_marshal"),
	    (else_try),
			(faction_get_slot, ":faction_ai_decider", ":faction_no", slot_faction_leader),
	    (try_end),


        #(*1) these two lines moved to here from (*2)
        (call_script, "script_npc_decision_checklist_faction_ai_alt", ":faction_ai_decider"),
	    (assign, ":new_strategy", reg0),
	    (str_store_string, s26, s14),

        #(3*) these three lines moved to here from (*4)
        (faction_get_slot, ":faction_ai_state", ":faction_no", slot_faction_ai_state),
        (faction_get_slot, ":faction_ai_object", ":faction_no", slot_faction_ai_object),
        (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),

        (faction_get_slot, ":faction_ai_offensive_max_followers", ":faction_no", slot_faction_ai_offensive_max_followers),
        (str_store_faction_name, s10, ":faction_no"),

	   (try_begin),
			(faction_get_slot, ":faction_issue", ":faction_no", slot_faction_political_issue),

			(try_begin),
				(eq, ":faction_issue", 1),
				(str_store_string, s11, "@Appoint next marshal"),
			(else_try),
				(is_between, ":faction_issue", centers_begin, centers_end),
				(str_store_party_name, s12, ":faction_issue"),
				(str_store_string, s11, "@Award {s12} as fief"),
			(else_try),
				(eq, ":faction_issue", 0),
				(str_store_string, s11, "str_dplmc_none"),
			(else_try),
				(assign, reg3, ":faction_issue"),
				(str_store_string, s11, "@{!}Error ({reg3})"),
			(try_end),

			(store_current_hours, reg4),
			(faction_get_slot, ":faction_issue_put_on_agenda", ":faction_no", slot_faction_political_issue_time),
			(val_sub, reg4, ":faction_issue_put_on_agenda"),

	        (str_store_string, s10, "@{!}{s10}^Faction political issue: {s11}"),
			(try_begin),
				(faction_slot_ge, ":faction_no", slot_faction_political_issue, 1),
				(str_store_string, s10, "@{!}{s10} (on agenda {reg4} hours)"),
			(try_end),
	   (try_end),


       (assign, reg2, ":faction_ai_offensive_max_followers"),
       (try_begin),
         (eq, ":faction_ai_state", sfai_default),
         (str_store_string, s11, "@{!}Defending"),
       (else_try),
         (eq, ":faction_ai_state", sfai_gathering_army),
         (str_store_string, s11, "@{!}Gathering army"),
       (else_try),
         (eq, ":faction_ai_state", sfai_attacking_center),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "@{!}Besieging {s11}"),
       (else_try),
         (eq, ":faction_ai_state", sfai_raiding_village),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "@{!}Raiding {s11}"),
       (else_try),
         (eq, ":faction_ai_state", sfai_attacking_enemy_army),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "str_attacking_enemy_army_near_s11"),
       (else_try),
         (eq, ":faction_ai_state", sfai_feast),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "str_holding_feast_at_s11"),
	   (else_try),
         (eq, ":faction_ai_state", sfai_attacking_enemies_around_center),
         (str_store_party_name, s11, ":faction_ai_object"),
         (str_store_string, s11, "@{!}Attacking enemies around {s11}"),
       (else_try),
	     (assign, reg4, ":faction_ai_state"),
		 (str_store_string, s11, "str_sfai_reg4"),
	   (try_end),

       (try_begin),
         (lt, ":faction_marshall", 0),
         (str_store_string, s12, "@No one"),
       (else_try),
         (str_store_troop_name, s12, ":faction_marshall"),
		 (troop_get_slot, reg21, ":faction_marshall", slot_troop_controversy),
		 (str_store_string, s12, "@{!}{s12} (controversy: {reg21})"),
       (try_end),

	   (try_for_parties, ":screen_party"),
			(party_slot_eq, ":screen_party", slot_party_ai_state, spai_screening_army),
			(store_faction_of_party, ":screen_party_faction", ":screen_party"),
			(eq, ":screen_party_faction", ":faction_no"),

			(str_store_party_name, s38, ":screen_party"),
			(str_store_string, s12, "@{!}{s12}^Screening party: {s38}"),
	   (try_end),

       #(*2) these two lines moved to up (look *1)
	   #(call_script, "script_npc_decision_checklist_faction_ai", ":faction_no"),
	   #(assign, ":new_strategy", reg0),

       #(try_begin),
       #  (this_or_next|eq, ":new_strategy", sfai_default),
       #  (eq, ":new_strategy", sfai_feast),
	   #
	   #  (store_current_hours, ":hours"),
	   #  (faction_set_slot, ":faction_no", slot_faction_ai_last_rest_time, ":hours"),
	   #(try_end),
      (try_begin),
         #new condition to rest, (a faction's new strategy should be feast or default) and (":hours_at_current_state" > 20)
         (this_or_next|eq, ":new_strategy", sfai_default),
         (eq, ":new_strategy", sfai_feast),

         (store_current_hours, ":hours_at_current_state"),
         (faction_get_slot, ":current_state_started", ":faction_no", slot_faction_ai_current_state_started),
         (val_sub, ":hours_at_current_state", ":current_state_started"),
         (ge, ":hours_at_current_state", 18),

         (store_current_hours, ":hours"),
         (faction_set_slot, ":faction_no", slot_faction_ai_last_rest_time, ":hours"),
       (try_end),

        #Change of strategy
        (try_begin),
          (neq, ":new_strategy", ":old_faction_ai_state"),

          (store_current_hours, ":hours"),
          (faction_set_slot, ":faction_no", slot_faction_ai_current_state_started, ":hours"),
        (try_end),

	   (call_script, "script_evaluate_realm_stability", ":faction_no"),
	   (assign, ":disgruntled_lords", reg0),
	   (assign, ":restless_lords", reg1),

	   (faction_get_slot, ":last_feast_ended", ":faction_no", slot_faction_last_feast_start_time),
	   (store_sub, ":hours_since_last_feast", ":cur_hours", ":last_feast_ended"),
	   (val_sub, ":hours_since_last_feast", 72),

	   (faction_get_slot, ":current_state_started", ":faction_no", slot_faction_ai_current_state_started),
	   (store_sub, ":hours_at_current_state", ":cur_hours", ":current_state_started"),

       (faction_get_slot, ":faction_ai_last_offensive_time", ":faction_no", slot_faction_last_offensive_concluded),
       (store_sub, ":hours_since_last_offensive", ":cur_hours", ":faction_ai_last_offensive_time"),

       (faction_get_slot, ":faction_ai_last_rest", ":faction_no", slot_faction_ai_last_rest_time),
       (store_sub, ":hours_since_last_rest", ":cur_hours", ":faction_ai_last_rest"),

       (faction_get_slot, ":faction_ai_last_decisive_event", ":faction_no", slot_faction_ai_last_decisive_event),
       (store_sub, ":hours_since_last_decisive_event", ":cur_hours", ":faction_ai_last_decisive_event"),

	   (assign, reg3, ":hours_at_current_state"),
	   (assign, reg4, ":hours_since_last_offensive"),
	   (assign, reg5, ":hours_since_last_feast"),

	   (assign, reg7, ":disgruntled_lords"),
	   (assign, reg8, ":restless_lords"),
	   (assign, reg9, ":hours_since_last_rest"),
	   (assign, reg10, ":hours_since_last_decisive_event"),
	   (str_store_string, s14, s26),

       (str_store_string, s9, "str_s9s10_current_state_s11_hours_at_current_state_reg3_current_strategic_thinking_s14_marshall_s12_since_the_last_offensive_ended_reg4_hours_since_the_decisive_event_reg10_hours_since_the_last_rest_reg9_hours_since_the_last_feast_ended_reg5_hours_percent_disgruntled_lords_reg7_percent_restless_lords_reg8__"),
     (try_end),

     (try_begin),
       (neg|is_between, "$g_cheat_selected_faction", kingdoms_begin, kingdoms_end),
       (call_script, "script_get_next_active_kingdom", kingdoms_end),
       (assign, "$g_cheat_selected_faction", reg0),
     (try_end),
     (str_store_faction_name, s10, "$g_cheat_selected_faction"),
     (str_store_string, s9, "@Selected faction is: {s10}^^{s9}"),
    ],
    [
      ("faction_orders_next_faction", [],"{!}Select next faction.",
       [
         (call_script, "script_get_next_active_kingdom", "$g_cheat_selected_faction"),
         (assign, "$g_cheat_selected_faction", reg0),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),

       #SB : debug slots
      ("faction_orders_slots", [],"{!}Debug slots.",
       [
         (assign, "$g_presentation_input", rename_kingdom),
         (assign, "$g_presentation_state", 0),
         (start_presentation, "prsnt_modify_slots"),
        ]
       ),

      ("faction_orders_political_collapse", [],"{!}CHEAT - Cause all lords in faction to fall out with their liege.",
       [
	   (try_for_range, ":lord", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
			(store_faction_of_troop, ":troop_faction", ":lord"),
			(eq, ":troop_faction", "$g_cheat_selected_faction"),
			(faction_get_slot, ":faction_liege", ":troop_faction", slot_faction_leader),
			(call_script, "script_troop_change_relation_with_troop", ":lord", ":faction_liege", -200),
	   (try_end),

	   ]
       ),

      ("faction_orders_defend", [],"{!}Force defend.",
       [
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_state, sfai_default),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_object, -1),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),
      ("faction_orders_feast", [],"{!}Force feast.",
       [

		 (assign, ":location_high_score", 0),
		 (try_for_range, ":location", walled_centers_begin, walled_centers_end),
			(neg|party_slot_ge, ":location", slot_center_is_besieged_by, 1),
			(store_faction_of_party, ":location_faction", ":location"),
			(eq, ":location_faction", "$g_cheat_selected_faction"),
			(party_get_slot, ":location_lord", ":location", slot_town_lord),
			(troop_get_slot, ":location_score", ":location_lord", slot_troop_renown),
			(store_random_in_range, ":random", 0, 1000), #will probably be king or senior lord
			(val_add, ":location_score", ":random"),
			(gt, ":location_score", ":location_high_score"),
			(assign, ":location_high_score", ":location_score"),
			(assign, ":location_feast", ":location"),
		 (try_end),

		 (try_begin),
			(gt, ":location_feast", centers_begin),
			(faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_state, sfai_feast),
			(faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_object, ":location_feast"),
			(try_begin),
			  (eq, "$g_player_eligible_feast_center_no", ":location_feast"),
			  (assign, "$g_player_eligible_feast_center_no", -1),
			(try_end),

			(store_current_hours, ":hours"),
			(faction_set_slot, "$g_cheat_selected_faction", slot_faction_last_feast_start_time, ":hours"),
		 (try_end),

	     (jump_to_menu, "mnu_faction_orders"),
        ]
       ),


      ("faction_orders_gather", [],"{!}Force gather army.",
       [
         (store_current_hours, ":cur_hours"),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_state, sfai_gathering_army),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_last_offensive_concluded, ":cur_hours"),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_offensive_max_followers, 1),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_ai_object, -1),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),
      ("faction_orders_increase_time", [],"{!}Increase last offensive time by 24 hours.",
       [
         (faction_get_slot, ":faction_ai_last_offensive_time", "$g_cheat_selected_faction", slot_faction_last_offensive_concluded),
         (val_sub, ":faction_ai_last_offensive_time", 24),
         (faction_set_slot, "$g_cheat_selected_faction", slot_faction_last_offensive_concluded, ":faction_ai_last_offensive_time"),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),
      ("faction_orders_rethink", [],"{!}Force rethink.",
       [
         (call_script, "script_init_ai_calculation"),
         (call_script, "script_decide_faction_ai", "$g_cheat_selected_faction"),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),
      ("faction_orders_rethink_all", [],"{!}Force rethink for all factions.",
       [
         (call_script, "script_recalculate_ais"),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),

	   # ("enable_alt_ai",[(eq, "$g_use_alternative_ai", 2),],"{!}CHEAT! - enable alternative ai",
       # [
	   # (assign, "$g_use_alternative_ai", 1),
	   # (jump_to_menu, "mnu_faction_orders"),
       # ]
       # ),

	   # ("disable_alt_ai",[(eq, "$g_use_alternative_ai", 2)],"{!}CHEAT! - disable alternative ai",
       # [
	   # (assign, "$g_use_alternative_ai", 0),
	   # (jump_to_menu, "mnu_faction_orders"),
       # ]
       # ),

       #SB : see if this works
     ("faction_orders_pretend", [],"{!}Restore pretender.",
       [
         # (call_script, "script_recalculate_ais"),
         (store_sub, "$supported_pretender", "$g_cheat_selected_faction", npc_kingdoms_begin),
         (val_add, "$supported_pretender", pretenders_begin),
         (assign, "$g_talk_troop", "$supported_pretender"),
         (party_add_members, "p_main_party", "$supported_pretender", 1),
         # (troop_get_slot, "$supported_pretender_old_faction", "$supported_pretender", slot_troop_original_faction),
         (assign, "$supported_pretender_old_faction", "$g_cheat_selected_faction"),
         (troop_set_faction, "$g_talk_troop", "fac_player_supporters_faction"),
         (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "$supported_pretender"),
         (assign, "$g_talk_troop_faction", "fac_player_supporters_faction"),

         (quest_set_slot, "qst_rebel_against_kingdom", slot_quest_giver_troop, "$supported_pretender"),
         (quest_set_slot, "qst_rebel_against_kingdom", slot_quest_target_faction, "$supported_pretender_old_faction"),

         (str_store_faction_name_link, s14, "$supported_pretender_old_faction"),
         (str_store_troop_name_link, s13, "$supported_pretender"),
         (setup_quest_text,"qst_rebel_against_kingdom"),
         (str_store_string, s2, "@You promised to help {s13} claim the throne of {s14}."),
         (call_script, "script_start_quest", "qst_rebel_against_kingdom", "$supported_pretender"),

         #merge lords
         (try_begin),
           (eq, "$players_kingdom", "fac_player_supporters_faction"),
           (call_script, "script_deactivate_player_faction"),
           (try_for_range, ":npc", active_npcs_begin, active_npcs_end),
              (store_faction_of_troop, ":npc_faction", ":npc"),
              (eq, ":npc_faction", "fac_player_supporters_faction"),
              (troop_slot_eq, ":npc", slot_troop_occupation, slto_kingdom_hero),
              (call_script, "script_change_troop_faction", ":npc", "$g_talk_troop_faction"),
           (try_end),
         (try_end),

         (try_begin),
           (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
           (neq, "$players_kingdom", "fac_player_supporters_faction"),
           (neq, "$players_kingdom", "$g_talk_troop_faction"), #ie, don't leave faction if the player is already part of the same kingdom

           (faction_get_slot, ":old_leader", "$players_kingdom", slot_faction_leader),
           (call_script, "script_add_log_entry", logent_renounced_allegiance,   "trp_player",  -1, ":old_leader", "$players_kingdom"),
           (call_script, "script_activate_player_faction", "$g_talk_troop"),
         (try_end),

         (call_script, "script_player_join_faction", "$g_talk_troop_faction"),

         (call_script, "script_add_notification_menu", "mnu_notification_faction_defeated", "$g_cheat_selected_faction", 0),
         (change_screen_return),
        ]
       ),
      ("faction_orders_init_econ", [],"{!}Initialize economic stats.",
       [
         (call_script, "script_initialize_economic_information"),
         (jump_to_menu, "mnu_faction_orders"),
        ]
       ),



      ("go_back_dot",[],"{!}Go back.",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  ("marshall_selection_candidate_ask",0,
   "{s15} will soon select a new marshall for {s23}. Some of the lords have suggested your name as a likely candidate.",
   "none",
   [
     (try_begin),
       (eq, "$g_presentation_marshall_selection_ended", 1),
       (change_screen_return),
     (try_end),
     (faction_get_slot, ":king", "$players_kingdom", slot_faction_leader),
     (str_store_troop_name, s15, ":king"),
     (str_store_faction_name, s23, "$players_kingdom"),
     ],
    [
      ("marshall_candidate_accept", [], "Let {s15} learn that you are willing to serve as marshall.",
       [
         (start_presentation, "prsnt_marshall_selection"),
        ]
       ),
      ("marshall_candidate_reject", [], "Tell everyone that you are too busy these days.",
       [
         (try_begin),
           (eq, "$g_presentation_marshall_selection_max_renown_2_troop", "trp_player"),
           (assign, "$g_presentation_marshall_selection_max_renown_2", "$g_presentation_marshall_selection_max_renown_3"),
           (assign, "$g_presentation_marshall_selection_max_renown_2_troop", "$g_presentation_marshall_selection_max_renown_3_troop"),
         (else_try),
           (assign, "$g_presentation_marshall_selection_max_renown_1", "$g_presentation_marshall_selection_max_renown_2"),
           (assign, "$g_presentation_marshall_selection_max_renown_1_troop", "$g_presentation_marshall_selection_max_renown_2_troop"),
           (assign, "$g_presentation_marshall_selection_max_renown_2", "$g_presentation_marshall_selection_max_renown_3"),
           (assign, "$g_presentation_marshall_selection_max_renown_2_troop", "$g_presentation_marshall_selection_max_renown_3_troop"),
         (try_end),
         (start_presentation, "prsnt_marshall_selection"),
        ]
       ),
      ]
  ),




##    [
##      ("renew_oath",[],"Renew your oath to {s1} for another month.",[
##          (store_current_day, ":cur_day"),
##          (store_add, "$g_oath_end_day", ":cur_day", 30),
##          (change_screen_return)]),
##      ("dont_renew_oath",[],"Become free of your bond.",[
##          (assign, "$players_kingdom",0),
##          (assign, "$g_player_permitted_castles", 0),
##          (change_screen_return)]),
##    ]
##  ),


#####################################################################
## Captivity....
#####################################################################
#####################################################################
#####################################################################
#####################################################################,
  (
    "kingdom_army_quest_join_siege_order",mnf_scale_picture,
    "{s8} sends word that you are to join the siege of {s9} in preparation for a full assault.\
 Your troops are to take {s9} at all costs.",
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (quest_get_slot, ":quest_target_center", "qst_join_siege_with_army", slot_quest_target_center),
        (str_store_troop_name, s8, ":faction_marshall"),
        (str_store_party_name, s9, ":quest_target_center"),
      ],
    [
      ("continue",[],"Continue...",
       [
           (call_script, "script_end_quest", "qst_follow_army"),
           (quest_get_slot, ":quest_target_center", "qst_join_siege_with_army", slot_quest_target_center),
           (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
           (str_store_troop_name_link, s13, ":faction_marshall"),
           (str_store_party_name_link, s14, ":quest_target_center"),
           (setup_quest_text, "qst_join_siege_with_army"),
           (str_store_string, s2, "@{s13} ordered you to join the assault against {s14}."),
           (call_script, "script_start_quest", "qst_join_siege_with_army", ":faction_marshall"),
           (change_screen_return),
        ]),
     ]
  ),
  (
    "kingdom_army_follow_failed",mnf_scale_picture,
    "You have failed to follow {s8}. The marshal assumes that you were otherwise engaged, but would have appreciated your support.",
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (str_store_troop_name, s8, ":faction_marshall"),
        (call_script, "script_abort_quest", "qst_follow_army", 1),
#        (call_script, "script_change_player_relation_with_troop", ":faction_marshall", -3),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "invite_player_to_faction_without_center",mnf_scale_picture,
##diplomacy start+ fix gender of pronouns
    "You receive an offer of vassalage!^^\
 {s8} of {s9} has sent a royal herald to bring you an invititation in {reg4?her:his} own hand.\
 You would be granted the honour of becoming a vassal {lord/lady} of {s9},\
 and in return {s8} asks you to swear an oath of homage to {reg4?her:him} and fight in {reg4?her:his} military campaigns,\
 although {reg4?she:he} offers you no lands or titles.\
 {reg4?She:He} will surely be offended if you do not take the offer...",
##diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, "$g_invite_faction_lord", "$g_invite_faction", slot_faction_leader),
        ##diplomacy start+ store gender in reg4
        (call_script, "script_dplmc_store_troop_is_female", "$g_invite_faction_lord"),
        (assign, reg4, reg0),
        ##diplomacy start+
        (str_store_troop_name, s8, "$g_invite_faction_lord"),
        (str_store_faction_name, s9, "$g_invite_faction"),
      ],
    [
      ("faction_accept",[],"Accept!",
       [(str_store_troop_name,s1,"$g_invite_faction_lord"),
        (setup_quest_text,"qst_join_faction"),

        (str_store_troop_name_link, s3, "$g_invite_faction_lord"),
        (str_store_faction_name_link, s4, "$g_invite_faction"),
        (quest_set_slot, "qst_join_faction", slot_quest_giver_troop, "$g_invite_faction_lord"),
        (quest_set_slot, "qst_join_faction", slot_quest_expiration_days, 30),
		(quest_set_slot, "qst_join_faction", slot_quest_failure_consequence, 0),
	##diplomacy start+ fix gender of pronoun
        (str_store_string, s2, "@Find and speak with {s3} of {s4} to give {reg4?her:him} your oath of homage."),
        ##diplomacy end+
        (call_script, "script_start_quest", "qst_join_faction", "$g_invite_faction_lord"),
        (call_script, "script_report_quest_troop_positions", "qst_join_faction", "$g_invite_faction_lord", 3),
        (jump_to_menu, "mnu_invite_player_to_faction_accepted"),
        ]),
      ("faction_reject",[],"Decline the invitation.",
       [(call_script, "script_change_player_relation_with_troop", "$g_invite_faction_lord", -3),
        (call_script, "script_change_player_relation_with_faction", "$g_invite_faction", -10),
        (assign, "$g_invite_faction", 0),
        (assign, "$g_invite_faction_lord", 0),
        (assign, "$g_invite_offered_center", 0),
        (change_screen_return),
        ]),
     ]
  ),
  (
    "invite_player_to_faction",mnf_scale_picture,
##diplomacy start+ fix gender of pronouns
    "You receive an offer of vassalage!^^\
 {s8} of {s9} has sent a royal herald to bring you an invititation in {reg4?her:his} own hand.\
 You would be granted the honour of becoming a vassal {lord/lady} of {s9},\
 and in return {s8} asks you to swear an oath of homage to {reg4?her:him} and fight in {reg4?her:his} military campaigns,\
 offering you the fief of {s2} for your loyal service.\
 {reg4?She:He} will surely be offended if you do not take the offer...",
##diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, "$g_invite_faction_lord", "$g_invite_faction", slot_faction_leader),
        ##diplomacy start+ store gender in reg4
        (call_script, "script_dplmc_store_troop_is_female", "$g_invite_faction_lord"),
        (assign, reg4, reg0),
        ##diplomacy start+
        (str_store_troop_name, s8, "$g_invite_faction_lord"),
        (str_store_faction_name, s9, "$g_invite_faction"),
        (str_store_party_name, s2, "$g_invite_offered_center"),
      ],
    [
      ("faction_accept",[],"Accept!",
       [(str_store_troop_name,s1,"$g_invite_faction_lord"),
        (setup_quest_text,"qst_join_faction"),

        (str_store_troop_name_link, s3, "$g_invite_faction_lord"),
        (str_store_faction_name_link, s4, "$g_invite_faction"),
        (quest_set_slot, "qst_join_faction", slot_quest_giver_troop, "$g_invite_faction_lord"),
        (quest_set_slot, "qst_join_faction", slot_quest_expiration_days, 30),
        ##diplomacy start+ fix gender of pronoun
        (str_store_string, s2, "@Find and speak with {s3} of {s4} to give {reg4?her:him} your oath of homage."),
        ##diplomacy end+
        (call_script, "script_start_quest", "qst_join_faction", "$g_invite_faction_lord"),
        (call_script, "script_report_quest_troop_positions", "qst_join_faction", "$g_invite_faction_lord", 3),
        (jump_to_menu, "mnu_invite_player_to_faction_accepted"),
        ]),
      ("faction_reject",[],"Decline the invitation.",
       [(call_script, "script_change_player_relation_with_troop", "$g_invite_faction_lord", -3),
        (assign, "$g_invite_faction", 0),
        (assign, "$g_invite_faction_lord", 0),
        (assign, "$g_invite_offered_center", 0),
        (change_screen_return),
        ]),
     ]
  ),
  (
    "invite_player_to_faction_accepted",0,
##diplomacy start+ fix gender of pronouns (king's gender should already be in reg4)
    "In order to become a vassal, you must swear an oath of homage to {s3}.\
 You shall have to find {reg4?her:him} and give {reg4?her:him} your oath in person. {s5}",
##diplomacy end+
    "none",
    [
        (call_script, "script_get_information_about_troops_position", "$g_invite_faction_lord", 0),
        (str_store_troop_name, s3, "$g_invite_faction_lord"),
        (str_store_string, s5, "@{!}{s1}"),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "question_peace_offer",0,
    "You Receive a Peace Offer^^The {s1} offers you a peace agreement. What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),

      ##diplomacy begin
      (store_relation,  ":relation", "fac_player_supporters_faction", "$g_notification_menu_var1"),
      (try_begin),
        (ge, ":relation", 0),
        (change_screen_return),
      (try_end),
      ##diplomacy end
      ],
    [
      ("peace_offer_accept",[],"Accept",
       [
         (call_script, "script_diplomacy_start_peace_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (change_screen_return),
        ]),
        ##diplomacy begin
      ("dplmc_peace_offer_terms",[],"Dictate the peace terms",
       [
        (start_presentation, "prsnt_dplmc_peace_terms"),
        ]),
        ##diplomacy end
      ("peace_offer_reject",[],"Reject",
       [
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -5),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "minister_confirm",0,
    "{s9}can be found at your court in {s12}. You should consult {reg4?her:him} periodically, to avoid the accumulation of unresolved issues that may sap your authority...",
    "none",
    [
    (try_begin),
        (store_and, ":name_set", "$players_kingdom_name_set", rename_kingdom),
        (eq, ":name_set", rename_kingdom),
        (change_screen_return),
    (try_end),

	(try_begin),
		(eq, "$g_player_minister", "trp_temporary_minister"),
		(str_store_string, s9, "str_your_new_minister_"),
	(else_try),
		(str_store_troop_name, s10, "$g_player_minister"),
		(str_store_string, s9, "str_s10_is_your_new_minister_and_"),
	(try_end),

	(try_begin),
		(main_party_has_troop, "$g_player_minister"),
		(remove_member_from_party, "$g_player_minister", "p_main_party"),
	(try_end),

    #SB : tableau notes
    (set_fixed_point_multiplier, 100),
    (position_set_x, pos0, 70),
    (position_set_y, pos0, 5),
    (position_set_z, pos0, 75),
    (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", "$g_player_minister", pos0),
    #also gender string
    (call_script, "script_dplmc_store_troop_is_female_reg", "$g_player_minister", 4),
	],
    [
      ("continue",[],"Continue...",
       [
         #SB : explicitly state kingdom
         (assign, "$g_presentation_state", rename_kingdom),
         (start_presentation, "prsnt_name_kingdom"),
        ]),
     ]
  ),
  (
    "auto_return_to_map",0,
    "stub",
    "none",
    [(change_screen_map)],
    []
  ),

    (
    "bandit_lair",0,
    "{s3}",
    "none",
    [
      (try_begin),
        (eq, "$loot_screen_shown", 1),

        (try_for_range, ":bandit_template", bandit_party_templates_begin, bandit_party_templates_end), #SB : template range
          (party_template_slot_eq, ":bandit_template", slot_party_template_lair_party, "$g_encountered_party"),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),

           #dckplmc
           (store_current_hours, ":cur_hours"),
           (val_add, ":cur_hours", bandit_lair_respawn_hours), #spawn again after configured delay
           (party_template_set_slot, ":bandit_template", slot_party_template_lair_next_spawn, ":cur_hours"),

        (try_end),

        (try_begin),
          (ge, "$g_encountered_party", 0),
          (party_is_active, "$g_encountered_party"),
          (party_get_template_id, ":template", "$g_encountered_party"),
          (neq, ":template", "pt_looter_lair"),
          (remove_party, "$g_encountered_party"),
        (try_end),

        (assign, "$g_leave_encounter", 0),
        (change_screen_return),

      (else_try),
        (party_stack_get_troop_id, ":bandit_type", "$g_encountered_party", 0),
        (str_store_troop_name_plural, s4, ":bandit_type"),
        (str_store_string, s5, "str_bandit_approach_defile"),

        #SB : set pictures
        (try_begin),
          (eq, ":bandit_type", "trp_desert_bandit"),
          (str_store_string, s5, "str_bandit_approach_defile"),
        (else_try),
          (eq, ":bandit_type", "trp_mountain_bandit"),
          (str_store_string, s5, "str_bandit_approach_cliffs"),
          (set_background_mesh, "mesh_pic_mountain_bandits"),
        (else_try),
          (eq, ":bandit_type", "trp_forest_bandit"),
          (str_store_string, s5, "str_bandit_approach_swamp"),
          (set_background_mesh, "mesh_pic_forest_bandits"),
        (else_try),
          (eq, ":bandit_type", "trp_taiga_bandit"),
          (str_store_string, s5, "str_bandit_approach_swamp"),
          (set_background_mesh, "mesh_pic_steppe_bandits"),
        (else_try),
          (eq, ":bandit_type", "trp_steppe_bandit"),
          (str_store_string, s5, "str_bandit_approach_thickets"),
          (set_background_mesh, "mesh_pic_steppe_bandits"),
        (else_try),
          (eq, ":bandit_type", "trp_sea_raider"),
          (str_store_string, s5, "str_bandit_approach_cove"),
          (set_background_mesh, "mesh_pic_sea_raiders"),
        (try_end),


        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 0), #used in place of global variable
          (str_store_string, s3, "str_bandit_hideout_preattack"),
        (else_try),
          (party_get_template_id, ":template", "$g_encountered_party"),
          (eq, ":template", "pt_looter_lair"),
          (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 1), #used in place of global variable
          (str_store_string, s3, "str_lost_startup_hideout_attack"),
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 1), #used in place of global variable
          (str_store_string, s3, "str_bandit_hideout_failure"),
          (set_background_mesh, "mesh_pic_wounded"),
          (try_begin),
            (eq, "$character_gender", tf_female),
            (set_background_mesh, "mesh_pic_wounded_fem"),
          (try_end),
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 2), #used in place of global variable
          (str_store_string, s3, "str_bandit_hideout_success"),
          (set_background_mesh, "mesh_pic_victory"),
        (try_end),
      (try_end),
    ],
    [
      ("continue_1",
      [
        (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 0), #used in place of global variable
      ],
      "Attack the hideout...",

      [
        (party_set_slot, "$g_encountered_party", slot_party_ai_substate, 1),
        (party_get_template_id, ":template", "$g_encountered_party"),
        (assign, "$g_enemy_party", "$g_encountered_party"),

        (try_begin),
          (eq, ":template", "pt_sea_raider_lair"),
          (assign, ":bandit_troop", "trp_sea_raider"),
          (assign, ":scene_to_use", "scn_lair_sea_raiders"),
        (else_try),
          (eq, ":template", "pt_forest_bandit_lair"),
          (assign, ":bandit_troop", "trp_forest_bandit"),
          (assign, ":scene_to_use", "scn_lair_forest_bandits"),
        (else_try),
          (eq, ":template", "pt_desert_bandit_lair"),
          (assign, ":bandit_troop", "trp_desert_bandit"),
          (assign, ":scene_to_use", "scn_lair_desert_bandits"),
        (else_try),
          (eq, ":template", "pt_mountain_bandit_lair"),
          (assign, ":bandit_troop", "trp_mountain_bandit"),
          (assign, ":scene_to_use", "scn_lair_mountain_bandits"),
        (else_try),
          (eq, ":template", "pt_taiga_bandit_lair"),
          (assign, ":bandit_troop", "trp_taiga_bandit"),
          (assign, ":scene_to_use", "scn_lair_taiga_bandits"),
        (else_try),
          (eq, ":template", "pt_steppe_bandit_lair"),
          (assign, ":bandit_troop", "trp_steppe_bandit"),
          (assign, ":scene_to_use", "scn_lair_steppe_bandits"),
        (else_try),
          (eq, ":template", "pt_looter_lair"),
          (assign, ":bandit_troop", "trp_looter"),

          (store_faction_of_party, ":starting_town_faction", "$g_starting_town"),

          (try_begin),
            (eq, ":starting_town_faction", "fac_kingdom_1"), #player selected swadian city as starting town.
            (assign, ":scene_to_use", "scn_lair_forest_bandits"),
          (else_try),
            (eq, ":starting_town_faction", "fac_kingdom_2"), #player selected Vaegir city as starting town.
            (assign, ":scene_to_use", "scn_lair_taiga_bandits"),
          (else_try),
            (eq, ":starting_town_faction", "fac_kingdom_3"), #player selected Khergit city as starting town.
            (assign, ":scene_to_use", "scn_lair_steppe_bandits"),
          (else_try),
            (eq, ":starting_town_faction", "fac_kingdom_4"), #player selected Nord city as starting town.
            (assign, ":scene_to_use", "scn_lair_sea_raiders"),
          (else_try),
            (eq, ":starting_town_faction", "fac_kingdom_5"), #player selected Rhodok city as starting town.
            (assign, ":scene_to_use", "scn_lair_mountain_bandits"),
          (else_try),
            (eq, ":starting_town_faction", "fac_kingdom_6"), #player selected Sarranid city as starting town.
            (assign, ":scene_to_use", "scn_lair_desert_bandits"),
          (try_end),
        (try_end),

        (modify_visitors_at_site,":scene_to_use"),
        (reset_visitors),

        (store_character_level, ":player_level", "trp_player"),
        (store_add, ":number_of_bandits_will_be_spawned_at_each_period", 5, ":player_level"),
        (val_div, ":number_of_bandits_will_be_spawned_at_each_period", 3),

        (try_for_range, ":unused", 0, ":number_of_bandits_will_be_spawned_at_each_period"),
          (store_random_in_range, ":random_entry_point", 2, 11),
          (set_visitor, ":random_entry_point", ":bandit_troop", 1),
        (try_end),

        (party_clear, "p_temp_casualties"),

        (set_party_battle_mode),
        (set_battle_advantage, 0),
        (assign, "$g_battle_result", 0),
        (set_jump_mission,"mt_bandit_lair"),

        (jump_to_scene, ":scene_to_use"),
        (change_screen_mission),
      ]),

      ("leave_no_attack",
      [
        (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 0),
      ],
      "Leave...",
      [
        (change_screen_return),
      ]),

      ("leave_victory",
      [
        (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 2),
      ],
      "Continue...",
      [
        (try_for_range, ":bandit_template", bandit_party_templates_begin, bandit_party_templates_end), #SB : template range
          (party_template_slot_eq, ":bandit_template", slot_party_template_lair_party, "$g_encountered_party"),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
          #dckplmc : keep this bandit type suppressed for the configured delay
          (store_current_hours, ":cur_hours"),
          (val_add, ":cur_hours", bandit_lair_respawn_hours),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_next_spawn, ":cur_hours"),
        (try_end),

        (party_get_template_id, ":template", "$g_encountered_party"),
        (try_begin),
          (neq, ":template", "pt_looter_lair"),
          (check_quest_active, "qst_destroy_bandit_lair"),
          (quest_slot_eq, "qst_destroy_bandit_lair", slot_quest_target_party, "$g_encountered_party"),
          (call_script, "script_succeed_quest", "qst_destroy_bandit_lair"),
        (try_end),

        (assign, "$g_leave_encounter", 0),
        (change_screen_return),

        (try_begin),
          (eq, "$loot_screen_shown", 0),
          (assign, "$loot_screen_shown", 1),
#          (try_begin),
#            (gt, "$g_ally_party", 0),
#            (call_script, "script_party_add_party", "$g_ally_party", "p_temp_party"), #Add remaining prisoners to ally TODO: FIX it.
#          (else_try),
#            (party_get_num_attached_parties, ":num_quick_attachments", "p_main_party"),
#            (gt, ":num_quick_attachments", 0),
#            (party_get_attached_party_with_rank, ":helper_party", "p_main_party", 0),
#            (call_script, "script_party_add_party", ":helper_party", "p_temp_party"), #Add remaining prisoners to our reinforcements
#          (try_end),
          (troop_clear_inventory, "trp_temp_troop"),

          (party_get_num_companion_stacks, ":num_stacks", "p_temp_casualties"),
          (try_for_range, ":stack_no", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", "p_temp_casualties", ":stack_no"),
            (try_begin),
              (party_stack_get_size, ":stack_size", "p_temp_casualties", ":stack_no"),
              (party_stack_get_troop_id, ":stack_troop", "p_temp_casualties", ":stack_no"),
              (gt, ":stack_size", 0),
              (party_add_members, "p_total_enemy_casualties", ":stack_troop", ":stack_size"), #addition_to_p_total_enemy_casualties
              (party_stack_get_num_wounded, ":stack_wounded_size", "p_temp_casualties", ":stack_no"),
              (gt, ":stack_wounded_size", 0),
              (party_wound_members, "p_total_enemy_casualties", ":stack_troop", ":stack_wounded_size"),
            (try_end),
          (try_end),

          (call_script, "script_party_calculate_loot", "p_total_enemy_casualties"), #p_encountered_party_backup changed to total_enemy_casualties
          (gt, reg0, 0),
          (troop_sort_inventory, "trp_temp_troop"),
          ##diplomacy start+
          ##OLD:
          #(change_screen_loot, "trp_temp_troop"),
          ##NEW:
          ##jump to rubik's CC autoloot
          (try_begin),
            (call_script, "script_party_calculate_loot", "p_total_enemy_casualties"),
            (assign, "$dplmc_return_menu", "mnu_bandit_lair"),
            #SB : variable resets
            (assign, "$lord_selected", "trp_player"),
            (str_clear, dplmc_loot_string),
            (jump_to_menu, "mnu_dplmc_manage_loot_pool"),
          (else_try),
             #Fall back to old behavior
            (change_screen_loot, "trp_temp_troop"),
          (try_end),
          ##diplomacy end+
        (try_end),

        (try_begin),
          (ge, "$g_encountered_party", 0),
          (party_is_active, "$g_encountered_party"),
          (party_get_template_id, ":template", "$g_encountered_party"),
          (eq, ":template", "pt_looter_lair"),
          (remove_party, "$g_encountered_party"),
        (try_end),
      ]),

      ("leave_defeat",
      [
        (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 1),
      ],
      "Continue...",
      [
        (try_for_range, ":bandit_template", bandit_party_templates_begin, bandit_party_templates_end), #SB : template range
          (party_template_slot_eq, ":bandit_template", slot_party_template_lair_party, "$g_encountered_party"),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
          #dckplmc : keep this bandit type suppressed for the configured delay
          (store_current_hours, ":cur_hours"),
          (val_add, ":cur_hours", bandit_lair_respawn_hours),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_next_spawn, ":cur_hours"),
        (try_end),

        (try_begin),
          (party_get_template_id, ":template", "$g_encountered_party"),
          (neq, ":template", "pt_looter_lair"),
          (check_quest_active, "qst_destroy_bandit_lair"),
          (quest_slot_eq, "qst_destroy_bandit_lair", slot_quest_target_party, "$g_encountered_party"),
          (call_script, "script_fail_quest", "qst_destroy_bandit_lair"),
        (try_end),

        (try_begin),
          (ge, "$g_encountered_party", 0),
          (party_is_active, "$g_encountered_party"),
          (party_get_template_id, ":template", "$g_encountered_party"),
          (neq, ":template", "pt_looter_lair"),
          (remove_party, "$g_encountered_party"),
        (try_end),

        (assign, "$g_leave_encounter", 0),

        (try_begin),
            (party_is_active, "$g_encountered_party"),
            (party_set_slot, "$g_encountered_party", slot_party_ai_substate, 0),
        (try_end),

        (change_screen_return),
        ]),

     ]
  ),
]
