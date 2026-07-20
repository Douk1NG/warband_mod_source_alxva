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

simple_remove_disguise_scripts = [
("simple_remove_disguise",
 [
	(try_begin),
		(gt, "$sneaked_into_town", disguise_none),
		(display_message, "@You retrieve your hidden items.", message_alert),
		(try_begin),
			(eq, "$g_dplmc_player_disguise", 1),
			(set_show_messages, 0),
		(try_for_range, ":i_slot", ek_item_0, ek_food + 1),
			(troop_get_inventory_slot, ":item", "trp_player", ":i_slot"),
			(neq, ":item", -1),
			(troop_get_inventory_slot_modifier, ":imod", "trp_player", ":i_slot"),
			(troop_add_item, "trp_random_town_sequence", ":item", ":imod"),
		(try_end),
			(call_script, "script_move_inventory_and_gold", "trp_player", "trp_random_town_sequence", 0),
			(call_script, "script_dplmc_copy_inventory", "trp_random_town_sequence", "trp_player"),
			(call_script, "script_troop_transfer_gold", "trp_random_town_sequence", "trp_player", 0),
			(set_show_messages, 1),
		(try_end),
		(assign, "$sneaked_into_town", disguise_none),
	(try_end),
])
]
