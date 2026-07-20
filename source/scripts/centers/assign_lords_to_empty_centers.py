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

assign_lords_to_empty_centers_scripts = [
# script_assign_lords_to_empty_centers
# Input: none
# Output: none
#Now ONLY called from the start
("assign_lords_to_empty_centers",
   [

    (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_assigning_lords_to_empty_centers"),
		(str_store_string, s65, "str_assign_lords_to_empty_centers_just_happened"),
		(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),
    (try_end),

	(try_for_range, ":faction", kingdoms_begin, kingdoms_end),
		(faction_set_slot, ":faction", slot_faction_temp_slot, 0),
    (try_end),

	(try_for_range, ":active_npc", 0, active_npcs_end),
		(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
    (try_end),

    #Factions will keep one unassigned center in reserve, unless they have landless lords
    (try_for_range, ":cur_center", centers_begin, centers_end),
	    (party_get_slot, ":center_lord", ":cur_center", slot_town_lord),
		(try_begin),
			(this_or_next|eq, ":center_lord", stl_unassigned),
				(eq, ":center_lord", stl_rejected_by_player),
			(store_faction_of_party, ":center_faction", ":cur_center"),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_party_name, s4, ":cur_center"),
				(str_store_faction_name, s5, ":center_faction"),
				(display_message, "str_s4_of_the_s5_is_unassigned"),
			(try_end),

			(faction_get_slot, ":number_of_unassigned_centers_plus_landless_lords", ":center_faction", slot_faction_temp_slot),
			(val_add, ":number_of_unassigned_centers_plus_landless_lords", 1),
			(faction_set_slot,  ":center_faction", slot_faction_temp_slot, ":number_of_unassigned_centers_plus_landless_lords"),
		(else_try),
			(eq, ":center_lord", stl_reserved_for_player),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_party_name, s4, ":cur_center"),
				(str_store_faction_name, s5, ":center_faction"),
				(display_message, "str_s4_of_the_s5_is_reserved_for_player"),
			(try_end),

		(else_try),
			(ge, ":center_lord", 0),
			(troop_set_slot, ":center_lord", slot_troop_temp_slot, 1),
		(try_end),
	(try_end),

	(try_for_range, ":active_npc", 0, active_npcs_end),
		(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
		(this_or_next|gt, ":active_npc", "trp_player"),
			(eq, "$player_has_homage", 1),

		(troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
		(store_faction_of_troop, ":npc_faction", ":active_npc"),

		(is_between, ":npc_faction", npc_kingdoms_begin, npc_kingdoms_end),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":active_npc"),
			(str_store_faction_name, s5, ":npc_faction"),
			(display_message, "str_s4_of_the_s5_has_no_fiefs"),
		(try_end),

		(faction_get_slot, ":number_of_unassigned_centers_plus_landless_lords", ":npc_faction", slot_faction_temp_slot),
		(val_add, ":number_of_unassigned_centers_plus_landless_lords", 1),
		(faction_set_slot,  ":npc_faction", slot_faction_temp_slot, ":number_of_unassigned_centers_plus_landless_lords"),
	(try_end),

   	(try_begin),
	  (eq, "$cheat_mode", 1),
 	  (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
		(faction_get_slot, reg4, ":faction", slot_faction_temp_slot),
		(str_store_faction_name, s4, ":faction"),
		(display_message, "str_s4_unassigned_centers_plus_landless_lords_=_reg4"),
	  (try_end),
    (try_end),

	(try_for_range, ":cur_center", centers_begin, centers_end),
		(party_get_slot, ":center_lord", ":cur_center", slot_town_lord),
        (this_or_next|eq, ":center_lord", stl_unassigned),
			(eq, ":center_lord", stl_rejected_by_player),

        (store_faction_of_party, ":center_faction", ":cur_center"),
        (is_between, ":center_faction", kingdoms_begin, kingdoms_end),
        (neg|faction_slot_eq, ":center_faction", slot_faction_leader, "trp_player"),

        (try_begin),
	      (eq, "$cheat_mode", 1),
		  (str_store_party_name, s5, ":cur_center"),
	      (try_begin),
			(neg|faction_slot_ge, ":center_faction", slot_faction_temp_slot, 2),
			(str_store_faction_name, s4, ":center_faction"),
			(display_message, "str_s4_holds_s5_in_reserve"),
		  (try_end),
        (try_end),

		(faction_slot_ge, ":center_faction", slot_faction_temp_slot, 2),

		#(display_message, "@Considering grant of {s5}"),

		(assign, ":best_lord", -1),
		(assign, ":best_lord_score", -1),
		(try_begin),
			(eq, ":center_lord", stl_unassigned),
			(try_begin),
				(eq, "$players_kingdom", ":center_faction"),
				(eq, "$player_has_homage", 1),
				(assign, ":best_lord", stl_reserved_for_player),
				(call_script, "script_calculate_troop_score_for_center", "trp_player", ":cur_center"),
				(assign, ":best_lord_score", reg0),
			(try_end),
		(try_end),

		(try_for_range, ":cur_troop", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":troop_faction", ":cur_troop"),
			(eq, ":troop_faction", ":center_faction"),

			(call_script, "script_calculate_troop_score_for_center", ":cur_troop", ":cur_center"),
			(assign, ":score", reg0),

			#This prioritizes granting of centers for troops which do not already have one
			(try_begin),
				(troop_slot_eq, ":cur_troop", slot_troop_temp_slot, 0),
				(is_between, ":cur_center", villages_begin, villages_end),
				(val_mul, ":score", 10),
			(try_end),

			(gt, ":score", ":best_lord_score"),
			(assign, ":best_lord_score", ":score"),
			(assign, ":best_lord", ":cur_troop"),
		(try_end),

	    #Adjust count of centers and lords
 		(try_begin),
			(this_or_next|ge, ":best_lord", 0),
				(eq, ":best_lord", stl_reserved_for_player),

			(faction_get_slot, ":landless_lords_plus_unassigned_centers", ":center_faction", slot_faction_temp_slot),
			(val_sub, ":landless_lords_plus_unassigned_centers", 1),

			(try_begin),
				(eq, ":best_lord", stl_reserved_for_player),
				(troop_slot_eq, "trp_player", slot_troop_temp_slot, 0),
				(troop_set_slot, "trp_player", slot_troop_temp_slot, 1),
				(val_sub, ":landless_lords_plus_unassigned_centers", 1),
			(else_try),
				(troop_slot_eq, ":best_lord", slot_troop_temp_slot, 0),
				(troop_set_slot, ":best_lord", slot_troop_temp_slot, 1),
				(val_sub, ":landless_lords_plus_unassigned_centers", 1),
			(try_end),

			(faction_set_slot, ":center_faction", slot_faction_temp_slot, ":landless_lords_plus_unassigned_centers"),
		(try_end),

	    #Give the center to the lord
		(try_begin),
			(ge, ":best_lord", 0),
			(call_script, "script_give_center_to_lord", ":cur_center", ":best_lord", 1),
		(else_try),
			(eq, ":best_lord", stl_reserved_for_player),
			(party_set_slot, ":cur_center", slot_town_lord, stl_reserved_for_player),
			(try_begin), #grant bound villages to player, if granting a castle
				(party_slot_eq, ":cur_center", slot_party_type, spt_castle),
#				(assign, ":give_at_least_one_village", 0),
				(try_for_range, ":cur_village", villages_begin, villages_end),
#					(eq, ":give_at_least_one_village", 0),
					(party_slot_eq, ":cur_village", slot_village_bound_center, ":cur_center"),
					(party_slot_eq, ":cur_village", slot_town_lord, stl_unassigned),
					(party_set_slot, ":cur_village", slot_town_lord, stl_reserved_for_player),
#					(assign, ":give_at_least_one_village", 1),
				(try_end),
			(try_end),
		(try_end),
    (try_end),
    ])
]
