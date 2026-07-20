# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_auto_loot_menu = [
("dplmc_auto_loot",
		0,
##diplomacy start+
		"Your heroes will automatically grab items from the loot pool based on their pre-selected upgrade options. Heroes listed first in the party order will have first pick. Any equipment no longer needed will be dropped back into the loot pool. Any items in the loot pool will be lost when you leave.^ Are you sure you wish to do this?",
##diplomacy end+
		"none",
		[],
		[
			("dplmc_autoloot_no",
				[],
				"No, I've changed my mind.",
				[
					(jump_to_menu, "mnu_dplmc_manage_loot_pool"),
				]
			),
			("dplmc_autoloot_yes",
				[],
				"Yes, perform the upgrading.",
				[
					##diplomacy start+
					(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
					(assign, "$pool_troop", "trp_temp_troop"),
					#SB : reset variables
					(set_player_troop, "trp_player"),
					(assign, "$lord_selected", "trp_player"),
					##diplomacy end+
					(call_script, "script_dplmc_auto_loot_all", "trp_temp_troop", dplmc_loot_string),
					(jump_to_menu, "mnu_dplmc_manage_loot_pool"),
				]
			),

            #SB : individual looting
			("dplmc_autoloot_personal",
				[(is_between, "$lord_selected", companions_begin, companions_end),(str_store_troop_name, s1, "$lord_selected")],
				"Yes, only upgrade {s1}.",
				[
					##diplomacy start+
					(assign, "$pool_troop", "trp_temp_troop"),
					(call_script, "script_dplmc_auto_loot_troop", "$lord_selected", "$pool_troop", dplmc_loot_string),
					##diplomacy end+
					(jump_to_menu, "mnu_dplmc_manage_loot_pool"),
				]
			),
		]
	)
]
