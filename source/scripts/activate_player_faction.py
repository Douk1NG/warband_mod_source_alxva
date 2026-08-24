# ======================================================================
# SHARED DEPENDENCY
# Entity: activate_player_faction (script)
# Called by menus in 2 domains: diplomacy, kingdom_management
# ======================================================================

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

activate_player_faction_scripts = [
#script_activate_player_faction
# INPUT: arg1 = last_interaction_with_faction
# OUTPUT: none
#When a player convinces her husband to rebel
#When a player proclaims herself queen
#When a player seizes control of a center
#When a player recruits a lord through intrigue
#When a player
("activate_player_faction",
    [
    (store_script_param, ":liege", 1),

	#This moved to top, so that mnu_notification does not occur twice
	(try_begin),
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(neg|is_between, ":liege", pretenders_begin, pretenders_end),
		(try_begin),
			(eq, ":liege", "trp_player"),
			(assign, "$cstm_open_troop_tree_view", 1),
		(try_end),
		(call_script, "script_add_notification_menu", "mnu_notification_player_faction_active", 0, 0),
		##diplomacy begin
		(call_script, "script_add_notification_menu", "mnu_dplmc_domestic_policy", 0, 0),
		##diplomacy end
	(try_end),


    (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_active),
    (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, ":liege"),

	(assign, ":original_kingdom", "$players_kingdom"),

	(try_begin),
		(is_between, ":original_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_player_leave_faction", 0), #Ends quests, transfers control of centers
	(try_end),

	#Name faction
	(try_begin),
		(is_between, ":liege", active_npcs_begin, active_npcs_end),
		(store_faction_of_troop, ":liege_faction"),
		(is_between, ":liege_faction", npc_kingdoms_begin, npc_kingdoms_end),
		(faction_get_slot, ":adjective_string", ":liege_faction", slot_faction_adjective),
		(str_store_string, s1, ":adjective_string"),
		(faction_set_name, "fac_player_supporters_faction", "@{s1} Rebels"),
        #SB : opposite faction color
        (faction_get_color, ":color", ":liege_faction"),
        (store_sub, ":color", 0xFFFFFF, ":color"),#we get the opposite color
        (faction_set_color, "fac_player_supporters_faction", ":color"),
	(else_try),
		(str_store_troop_name, s2, ":liege"),
        (str_store_string, s1, "str_s2s_rebellion"),
	(try_end),


    (assign, "$players_kingdom", "fac_player_supporters_faction"),
    (assign, "$g_player_banner_granted", 1),



	#Any oaths renounced?
	(try_begin),
		(is_between, ":original_kingdom", npc_kingdoms_begin, npc_kingdoms_end),

        (faction_get_slot, ":old_leader", ":original_kingdom", slot_faction_leader),
        (call_script, "script_add_log_entry", logent_renounced_allegiance,   "trp_player",  -1, ":old_leader", "$players_kingdom"),

        #Initializing renounce war variables
        (assign, "$players_oath_renounced_against_kingdom", ":original_kingdom"),
        (assign, "$players_oath_renounced_given_center", 0),
        (store_current_hours, "$players_oath_renounced_begin_time"),

        (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
          (store_faction_of_party, ":cur_center_faction", ":cur_center"),
          (party_set_slot, ":cur_center", slot_center_faction_when_oath_renounced, ":cur_center_faction"),
        (try_end),
        (party_set_slot, "$g_center_to_give_to_player", slot_center_faction_when_oath_renounced, "$players_oath_renounced_against_kingdom"),

		(store_relation, ":relation", ":original_kingdom", "fac_player_supporters_faction"),
		(ge, ":relation", 0),
		(call_script, "script_diplomacy_start_war_between_kingdoms", ":original_kingdom", "fac_player_supporters_faction", 1),
	(try_end),


	(try_begin),
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
	    (is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),


		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":spouse"),
			(display_message, "@{!}DEBUG - {s4} faction changed by marriage, case 2"),
		(try_end),

	    (troop_set_faction, ":spouse", "fac_player_supporters_faction"),
        (call_script, "script_troop_set_title_according_to_faction", ":spouse", "fac_player_supporters_faction"),
	(try_end),


    #(call_script, "script_store_average_center_value_per_faction"),
    (call_script, "script_update_all_notes"),
	(assign, "$g_recalculate_ais", 1),

    ])
]
