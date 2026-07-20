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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

diplomacy_start_war_between_kingdoms_scripts = [
("diplomacy_start_war_between_kingdoms", #sets relations between two kingdoms and their vassals.
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3), #1 = after start of game

	  (call_script, "script_npc_decision_checklist_peace_or_war", ":kingdom_a", ":kingdom_b", -1),
	  (assign, ":explainer_string", reg1),

	  #
    ##diplomacy begin
    (try_begin),
      (lt, ":initializing_war_peace_cond", 2),
    ##diplomacy end
	  (try_begin),
	    (eq, ":kingdom_a", "fac_player_supporters_faction"),
		(assign, ":war_event", logent_player_faction_declares_war),
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_declared_war_to_control_calradia"),
		(assign, ":war_event", logent_player_faction_declares_war), #for savegame compatibility, this event stands in for the attempt to declare war on all of calradia
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_considers_s16_to_be_dangerous_and_untrustworthy_and_shehe_wants_to_bring_s16_down"),
		(assign, ":war_event", logent_faction_declares_war_out_of_personal_enmity),
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_is_anxious_to_reclaim_old_lands_such_as_s18_now_held_by_s16"),
		(assign, ":war_event", logent_faction_declares_war_to_regain_territory),
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_faces_too_much_internal_discontent_to_feel_comfortable_ignoring_recent_provocations_by_s16s_subjects"),
		(assign, ":war_event", logent_faction_declares_war_to_respond_to_provocation),
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_is_alarmed_by_the_growing_power_of_s16"),
		(assign, ":war_event", logent_faction_declares_war_to_curb_power),
	  (try_end),
	  (call_script, "script_add_log_entry", ":war_event", ":kingdom_a", 0, 0, ":kingdom_b"),



	  (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":kingdom_a", ":kingdom_b"),
	  (assign, ":current_diplomatic_status", reg0),
	  (try_begin), #effects of policy only after the start of the game
	    (eq, ":initializing_war_peace_cond", 1),
		(eq, ":current_diplomatic_status", -1),
		(call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_declares_war_with_justification),
	  (else_try),
	    (eq, ":initializing_war_peace_cond", 1),
		(eq, ":current_diplomatic_status", 0),
		(call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_attacks_without_provocation),
	  (else_try),
		(eq, ":current_diplomatic_status", 1),
		(call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_breaks_truce),
	  (try_end),
	  ##diplomacy begin
    (else_try),
      (assign, ":war_event", logent_faction_declares_war_to_fulfil_pact),
      (call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_declares_war_with_justification),
      (assign, ":initializing_war_peace_cond", 1),
	  (try_end),
	  ##diplomacy end

      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_min, ":relation", -10),
      (val_add, ":relation", -30),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_min, ":relation", -30),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_min, ":relation", -30),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),

		#Remove this -- this scrambles who declares war on whom
#        (try_begin),
 #         (store_random_in_range, ":random_no", 0, 2),
  #        (this_or_next|eq, ":kingdom_a", "fac_player_supporters_faction"),
	#		(eq, ":random_no", 0),
     #     (assign, ":local_temp", ":kingdom_a"),
      #    (assign, ":kingdom_a", ":kingdom_b"),
       #   (assign, ":kingdom_b", ":local_temp"),
        #(try_end),

        (str_store_faction_name_link, s1, ":kingdom_a"),
        #SB : don't colorize message, if it's relevant script_set_player_relation_with_faction calls will show it
        # (faction_get_color, ":color", ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
        (display_log_message, "@{s1} has declared war against {s2}.", message_alert),

		(store_current_hours, ":hours"),
		(faction_set_slot, ":kingdom_a", slot_faction_ai_last_decisive_event, ":hours"),
		(faction_set_slot, ":kingdom_b", slot_faction_ai_last_decisive_event, ":hours"),

		#set provocation and truce days
		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(store_add, ":provocation_slot", ":kingdom_b", slot_faction_provocation_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
		(val_sub, ":provocation_slot", kingdoms_begin),
		(faction_set_slot, ":kingdom_a", ":truce_slot", 0),
		(faction_set_slot, ":kingdom_a", ":provocation_slot", 0),

		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(store_add, ":provocation_slot", ":kingdom_a", slot_faction_provocation_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
		(val_sub, ":provocation_slot", kingdoms_begin),
		(faction_set_slot, ":kingdom_b", ":truce_slot", 0),
		(faction_set_slot, ":kingdom_b", ":provocation_slot", 0),

        (call_script, "script_add_notification_menu", "mnu_notification_war_declared", ":kingdom_a", ":kingdom_b"),

        (call_script, "script_update_faction_notes", ":kingdom_a"),
        (call_script, "script_update_faction_notes", ":kingdom_b"),
        (assign, "$g_recalculate_ais", 1),
      (try_end),

	  (try_begin),
		(check_quest_active, "qst_cause_provocation"),
	    (neg|check_quest_succeeded, "qst_cause_provocation"),
		(this_or_next|eq, "$players_kingdom", ":kingdom_a"),
			(eq, "$players_kingdom", ":kingdom_b"),
		(call_script, "script_abort_quest", "qst_cause_provocation", 0),
	  (try_end),
    ##diplomacy begin
    #check for defensive
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (neq, ":cur_kingdom", ":kingdom_a"),
      (neq, ":cur_kingdom", ":kingdom_b"),

      (store_relation, ":cur_relation", ":cur_kingdom", ":kingdom_a"),
			(ge, ":cur_relation", 0), #AT PEACE

      (store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
  		(val_sub, ":truce_slot", kingdoms_begin),
  		(faction_get_slot, ":truce_days", ":cur_kingdom", ":truce_slot"),
  		##nested diplomacy start+ replace "40" with a named constant
  		#(gt, ":truce_days", 40),
  		(gt, ":truce_days", dplmc_treaty_defense_days_expire),
  		##nested diplomacy end+
  		(try_begin),
  		  (lt, ":initializing_war_peace_cond", 2), #only if war was not caused by defensive or alliance pact
  		  (call_script, "script_diplomacy_start_war_between_kingdoms", ":cur_kingdom", ":kingdom_a", 2),
  		(try_end),
    (try_end),

    #check for alliance
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (neq, ":cur_kingdom", ":kingdom_a"),
      (neq, ":cur_kingdom", ":kingdom_b"),

      (store_relation, ":cur_relation", ":cur_kingdom", ":kingdom_b"),
			(ge, ":cur_relation", 0), #AT PEACE

  		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
  		(val_sub, ":truce_slot", kingdoms_begin),
  		(faction_get_slot, ":truce_days", ":cur_kingdom", ":truce_slot"),
  		##nested diplomacy start+ replace "60" with a named constant
  		#(gt, ":truce_days", 60),
  		(gt, ":truce_days", dplmc_treaty_alliance_days_expire),
  		##nested diplomacy end+
  		(call_script, "script_diplomacy_start_war_between_kingdoms", ":cur_kingdom", ":kingdom_b", 3),
    (try_end),
    ##diplomacy end
  ])
]
