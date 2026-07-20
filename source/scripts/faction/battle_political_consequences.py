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

battle_political_consequences_scripts = [
#lord recruitment scripts end
#called from game_event_simulate_battle
#Includes a number of consequences that follow on battles, mostly affecting relations between different NPCs
#This only fires from complete victories
("battle_political_consequences",
    [
	(store_script_param, ":defeated_party", 1),
	(store_script_param, ":winner_party", 2),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(str_store_party_name, s4, ":winner_party"),
		(str_store_party_name, s5, ":defeated_party"),
		(display_message, "str_do_political_consequences_for_s4_victory_over_s5"),
	(try_end),

	(store_faction_of_party, ":winner_faction", ":winner_party"),
	(try_begin),
		(eq, ":winner_party", "p_main_party"),
		(assign, ":winner_faction", "$players_kingdom"),
	(try_end),

	(party_get_template_id, ":defeated_party_template", ":defeated_party"),

	#did the battle involve travellers?
	(try_begin),
		(this_or_next|eq, ":defeated_party_template", "pt_village_farmers"),
			(eq, ":defeated_party_template", "pt_kingdom_caravan_party"),


		(party_get_slot, ":destination", ":defeated_party", slot_party_ai_object),
		(party_get_slot, ":origin", ":defeated_party", slot_party_last_traded_center),

        (call_script, "script_add_log_entry", logent_traveller_attacked, ":winner_party",  ":origin", ":destination", ":winner_faction"),

		(try_begin),
			(eq, "$cheat_mode", 2),
			(neg|is_between, ":winner_faction", kingdoms_begin, kingdoms_end),
			(str_store_string, s65, "str_bandits_attacked_a_party_on_the_roads_so_a_bounty_is_probably_available"),
			(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),

			(str_store_party_name, s15, ":origin"),
			(str_store_party_name, s16, ":destination"),
			(display_message, "str_travellers_attacked_on_road_from_s15_to_s16"),
		(try_end),


		#by logging the faction and the party, we can verify that the party number is unlikely to have been reassigned - or at any rate, that the factions have not changed
	(try_end),

	#winner consequences:
	#1)   leader improves relations with other leaders
	#2)  Player given credit for victory if the victorious party is following the player's advice
	(try_begin),
		(party_get_template_id, ":winner_party_template", ":winner_party"),
		(eq, ":winner_party_template", "pt_kingdom_hero_party"),
		(neq, ":winner_party", "p_main_party"),
		#Do not do for player party, as is included in post-battle dialogs

		(party_stack_get_troop_id, ":winner_leader", ":winner_party", 0),
		##diplomacy start+ Support additional types
		(troop_is_hero, ":winner_leader"),
		(this_or_next|troop_slot_eq, ":winner_leader", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
		(is_between, ":winner_leader", active_npcs_begin, active_npcs_end),

		(store_faction_of_party, ":winner_faction", ":winner_party"),

		(party_collect_attachments_to_party, ":winner_party", "p_temp_party_2"),
        (party_get_num_companion_stacks, ":num_stacks", "p_temp_party_2"),
		(try_for_range, ":troop_iterator", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":cur_troop_id", "p_temp_party_2", ":troop_iterator"),
	    ##diplomacy start+ support promoted kingdom ladies
	    (is_between, ":cur_troop_id", heroes_begin, heroes_end),
	    (this_or_next|troop_slot_eq, ":cur_troop_id", slot_troop_occupation, slto_kingdom_hero),
	    ##diplomacy end+
            (is_between, ":cur_troop_id", active_npcs_begin, active_npcs_end),

			(try_begin),
				(troop_get_slot, ":winner_lord_party", ":cur_troop_id", slot_troop_leaded_party),
				(party_is_active, ":winner_lord_party"),
				(call_script, "script_cf_party_under_player_suggestion", ":winner_lord_party"),
				(call_script, "script_add_log_entry", logent_player_suggestion_succeeded, "trp_player", -1, ":cur_troop_id", -1),
			(try_end),


			(store_faction_of_troop, ":troop_faction", ":cur_troop_id"),
			(eq, ":troop_faction", ":winner_faction"),
			(neq, ":cur_troop_id", ":winner_leader"),

			(try_begin),
				(eq, "$cheat_mode", 4),
				(str_store_troop_name, s15, ":cur_troop_id"),
				(str_store_troop_name, s16, ":winner_leader"),
				(display_message, "str_s15_shares_joy_of_victory_with_s16"),
			(try_end),

			(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", ":winner_leader", 3),
			(val_add, "$total_battle_ally_changes", 3),

		(try_end),
		(party_clear, "p_temp_party_2"),
	(try_end),

	#consequences of defeat,
	#1) -1 relation with lord per lord, plus -15 if there is an incompatible marshal
	#2)  losers under player suggestion blame the player
	#3) Some losers resent the victor lord
	#4) Possible quarrels over defeat
	(try_begin),
		(party_collect_attachments_to_party, ":defeated_party", "p_temp_party_2"),
        (party_get_num_companion_stacks, ":num_stacks", "p_temp_party_2"),

		(try_begin),
			(gt, "$marshall_defeated_in_battle", 0),
			(str_store_troop_name, s15, "$marshall_defeated_in_battle"),
			(store_faction_of_troop, ":defeated_marshall_faction", "$marshall_defeated_in_battle"),
            (try_begin),
                (eq, "$cheat_mode", 1),
			    (display_message, "str_faction_marshall_s15_involved_in_defeat"),
            (try_end),
		(else_try),
			(eq, "$marshall_defeated_in_battle", "trp_player"),
			(eq, ":defeated_party", "p_main_party"),
			(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
            (try_begin),
                (eq, "$cheat_mode", 1),
			    (display_message, "str_player_faction_marshall_involved_in_defeat"),
            (try_end),
		(else_try),
			(assign, "$marshall_defeated_in_battle", -1),
		(try_end),

		(try_for_range, ":troop_iterator", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":cur_troop_id", "p_temp_party_2", ":troop_iterator"),
            (troop_slot_eq, ":cur_troop_id", slot_troop_occupation, slto_kingdom_hero),

			(try_begin), #is party under suggestion?
				(troop_get_slot, ":defeated_lord_party", ":cur_troop_id", slot_troop_leaded_party),
				(party_is_active, ":defeated_lord_party"),

				#is party under suggestion?
				(call_script, "script_cf_party_under_player_suggestion", ":defeated_lord_party"),
				(call_script, "script_add_log_entry", logent_player_suggestion_failed, "trp_player", -1, ":cur_troop_id", -1),
			(try_end),


			(store_faction_of_troop, ":troop_faction", ":cur_troop_id"),

			(faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
			(neq, ":cur_troop_id", ":faction_leader"),

			#Lose one point relation with liege
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s14, ":cur_troop_id"),
				(str_store_faction_name, s15, ":troop_faction"),

				(display_message, "str_s14_of_s15_defeated_in_battle_loses_one_point_relation_with_liege"),
			(try_end),

			(try_begin),
				(this_or_next|neq, ":faction_leader", "trp_player"), #if leader is zero at beginning of game. I'm not entirely sure how this could happen...
					(eq, "$players_kingdom", ":troop_faction"),

				(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", ":faction_leader", -1),
				(val_add, "$total_battle_ally_changes", -1),
			(try_end),


			(call_script, "script_faction_inflict_war_damage_on_faction", ":winner_faction", ":troop_faction", 10),


			(try_begin),
				(this_or_next|is_between, ":winner_leader", active_npcs_begin, active_npcs_end),
					(eq, ":winner_leader", "trp_player"),

				(this_or_next|neq, ":winner_leader", "trp_player"), #prevents winner leader being zero, for whatever reason
					(eq, ":winner_party", "p_main_party"),

				(this_or_next|troop_slot_eq, ":cur_troop_id", slot_lord_reputation_type, lrep_quarrelsome),
				(this_or_next|troop_slot_eq, ":cur_troop_id", slot_lord_reputation_type, lrep_selfrighteous),
					(troop_slot_eq, ":cur_troop_id", slot_lord_reputation_type, lrep_debauched),

				(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", ":winner_leader", -1),
				(val_add, "$total_battle_enemy_changes", -1),

				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s14, ":cur_troop_id"),
					(str_store_troop_name, s15, ":winner_leader"),

					(display_message, "str_s14_defeated_in_battle_by_s15_loses_one_point_relation"),
				(try_end),


			(try_end),

			(gt, "$marshall_defeated_in_battle", -1),
			(eq, ":troop_faction", ":defeated_marshall_faction"),
			(str_store_troop_name, s14, ":cur_troop_id"),

			(call_script, "script_cf_test_lord_incompatibility_to_s17", ":cur_troop_id", "$marshall_defeated_in_battle"),
            (try_begin),
                (eq, "$cheat_mode", 1),
			    (display_message, "str_s14_blames_s15_for_defeat"),
            (try_end),

			(call_script, "script_add_log_entry", logent_lord_blames_defeat, ":cur_troop_id", "$marshall_defeated_in_battle", ":faction_leader", ":winner_faction"),

			(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", ":faction_leader", -15),
			(val_add, "$total_battle_ally_changes", -15),

			(neq, "$marshall_defeated_in_battle", ":faction_leader"),
			(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", "$marshall_defeated_in_battle", -15),
			(val_add, "$total_battle_ally_changes", -15),

		(try_end),

		(party_clear, "p_temp_party_2"),
	(try_end),
	])
]
