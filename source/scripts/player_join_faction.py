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

player_join_faction_scripts = [
# script_add_notification_menu
# INPUT: arg1 = faction_no
# OUTPUT: none
("player_join_faction",
    [
      (store_script_param, ":faction_no", 1),
      (assign,"$players_kingdom",":faction_no"),
      (faction_set_slot, "fac_player_supporters_faction", slot_faction_ai_state, sfai_default),
      (assign, "$players_oath_renounced_against_kingdom", 0),
      (assign, "$players_oath_renounced_given_center", 0),
      (assign, "$players_oath_renounced_begin_time", 0),

      (try_for_range,":other_kingdom",kingdoms_begin,kingdoms_end),
        (faction_slot_eq, ":other_kingdom", slot_faction_state, sfs_active),
        (neq, ":other_kingdom", "fac_player_supporters_faction"),
        (try_begin),
          (neq, ":other_kingdom", ":faction_no"),
          (store_relation, ":other_kingdom_reln", ":other_kingdom", ":faction_no"),
        (else_try),
          (store_relation, ":other_kingdom_reln", "fac_player_supporters_faction", ":other_kingdom"),
          (val_max, ":other_kingdom_reln", 12),
        (try_end),
        (call_script, "script_set_player_relation_with_faction", ":other_kingdom", ":other_kingdom_reln"),
      (try_end),

      (try_for_range, ":cur_center", centers_begin, centers_end),
        #Give center to kingdom if player is the owner
        (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
        (call_script, "script_give_center_to_faction_while_maintaining_lord", ":cur_center", ":faction_no"),
	  (else_try),
        #Give center to kingdom if part of player faction
     	(store_faction_of_party, ":cur_center_faction", ":cur_center"),
		(eq, ":cur_center_faction", "fac_player_supporters_faction"),
        (call_script, "script_give_center_to_faction_while_maintaining_lord", ":cur_center", ":faction_no"),
      (try_end),

      (try_for_range, ":quest_no", lord_quests_begin, lord_quests_end),
        (check_quest_active, ":quest_no"),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
        (store_relation, ":quest_giver_faction_relation", "fac_player_supporters_faction", ":quest_giver_faction"),
        (lt, ":quest_giver_faction_relation", 0),
        (call_script, "script_abort_quest", ":quest_no", 0),
      (try_end),
      (try_for_range, ":quest_no", lord_quests_begin_2, lord_quests_end_2),
        (check_quest_active, ":quest_no"),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
        (store_relation, ":quest_giver_faction_relation", "fac_player_supporters_faction", ":quest_giver_faction"),
        (lt, ":quest_giver_faction_relation", 0),
        (call_script, "script_abort_quest", ":quest_no", 0),
      (try_end),
      (try_begin),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
        (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
      (try_end),

	  (try_begin),
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
	    (is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":spouse"),
			(display_message, "@{!}DEBUG - {s4} faction changed by marriage, case 1"),
		(try_end),

	    (troop_set_faction, ":spouse", "$players_kingdom"),
        (call_script, "script_troop_set_title_according_to_faction", ":spouse", "$players_kingdom"),
	  (try_end),
	  ##diplomacy start+
	  #Make other vassals follow the player.
	  ##(There are other possibilities that we might want to explore, but
	  ##what happens now is that they remain members of the defunct faction.)
	  (try_begin),
		(neq, ":faction_no", "fac_player_supporters_faction"),
		  (try_for_range, ":troop_no", heroes_begin, heroes_end),
			 (store_troop_faction, ":other_troop_faction", ":troop_no"),
			 (eq, ":other_troop_faction", "fac_player_supporters_faction"),

			 (this_or_next|neg|is_between, ":troop_no", companions_begin, companions_end),
			 (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (this_or_next|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
				(troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
			 (this_or_next|neq, ":troop_no", ":spouse"),
				(neg|is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":troop_no"),
				(display_message, "@{!} DEBUG - {s4} changed by player's defection"),
			(try_end),
			(troop_set_faction, ":troop_no", "$players_kingdom"),
			#Clear troop slots
			(troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
			(troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
			(troop_set_slot, ":troop_no", slot_lord_recruitment_argument, 0),
			(troop_set_slot, ":troop_no", slot_lord_recruitment_candidate, 0),
			(troop_set_slot, ":troop_no", slot_troop_promised_fief, 0),
			#Give new title
			(try_begin),
				(this_or_next|neg|is_between,":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
					(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
				(call_script, "script_troop_set_title_according_to_faction", ":troop_no", ":faction_no"),
			(try_end),
			#Change led party
			(try_begin),
				(troop_get_slot, ":troop_leaded_party", ":troop_no", slot_troop_leaded_party),
				(gt, ":troop_leaded_party", 0),
				(party_is_active, ":troop_leaded_party"),
				(party_set_faction, ":troop_leaded_party", ":faction_no"),
			(try_end),
		  (try_end),
	  (try_end),
	  ##diplomacy end+

	  # (try_for_range, ":center", centers_begin, centers_end),
	    # (store_faction_of_party, ":center_faction", ":faction_no"),
		# (neq, ":center_faction", "$players_kingdom"),
		# (party_slot_eq, ":center", slot_town_lord, stl_reserved_for_player),
# #		(party_set_slot, ":center", slot_town_lord, stl_unassigned),
	  # (try_end),

	  (troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),

	  #remove prisoners of player's faction if he was member of his own faction. And free companions which is prisoned in that faction.
      (try_for_parties, ":party_no"),
        (store_faction_of_party, ":party_faction", ":party_no"),
        (eq, ":party_faction", ":faction_no"),

        (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
        (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":party_no", ":troop_iterator"),
          (store_troop_faction, ":cur_faction", ":cur_troop_id"),

          (this_or_next|eq, ":cur_faction", "fac_player_supporters_faction"),
          (this_or_next|eq, ":cur_faction", ":faction_no"),
          (is_between, ":cur_troop_id", companions_begin, companions_end),

          (try_begin),
            (troop_is_hero, ":cur_troop_id"),
            (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
          (try_end),

          (party_prisoner_stack_get_size, ":stack_size", ":party_no", ":troop_iterator"),
          (party_remove_prisoners, ":party_no", ":cur_troop_id", ":stack_size"),

          (try_begin),
            (is_between, ":cur_troop_id", companions_begin, companions_end),

            (try_begin),
              (is_between, ":party_no", towns_begin, towns_end),
              (troop_set_slot, ":cur_troop_id", slot_troop_cur_center, ":party_no"),
            (else_try),
              (store_random_in_range, ":random_town_no", towns_begin, towns_end),
              (troop_set_slot, ":cur_troop_id", slot_troop_cur_center, ":random_town_no"),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
      #remove prisoners end.

      #(call_script, "script_store_average_center_value_per_faction"),
      (call_script, "script_update_all_notes"),
      (assign, "$g_recalculate_ais", 1),
      ])
]
