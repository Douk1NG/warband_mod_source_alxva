# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

requested_castle_granted_to_player_husband_menu = [
(
    "requested_castle_granted_to_player_husband", mnf_scale_picture,
    "You receive a message from your liege, {s3}.^^\
 {reg4?She:He} has decided to grant {s2}{reg3? and the nearby village of {s4}:} to your husband, {s7}.",
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),
		(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		(str_store_troop_name, s3, ":faction_leader"),
		(str_store_party_name, s2, "$g_center_to_give_to_player"),
		(try_begin),
			(party_slot_eq, "$g_center_to_give_to_player", slot_party_type, spt_castle),
			(assign, reg3, 1),
			(try_for_range, ":cur_village", villages_begin, villages_end),
				(party_slot_eq, ":cur_village", slot_village_bound_center, "$g_center_to_give_to_player"),
				(str_store_party_name, s4, ":cur_village"),
			(try_end),
		(else_try),
			(assign, reg3, 0),
		(try_end),
		##diplomacy start+ use script for gender
		#(troop_get_type, reg4, ":faction_leader"),#<- OLD
		(call_script, "script_dplmc_store_troop_is_female_reg", ":faction_leader", 4),
		##diplomacy end+

		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
		(str_store_troop_name, s11, ":spouse"),
		(str_store_string, s7, "str_to_your_husband_s11"),
    ],
    [
		("continue",[],"Continue.",
			[
			(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
			(call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", ":spouse", 0),
			],
		),
	]
)
]
