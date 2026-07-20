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

dplmc_print_wpn_upgrades_to_s0_scripts = [
#### Autoloot improved by rubik end
###################
# Used in conversations
("dplmc_print_wpn_upgrades_to_s0", [
	(store_script_param_1, ":troop"),

	(str_store_string, s0, "str_empty_string"),
	(troop_get_slot, ":upg", ":troop", dplmc_slot_upgrade_wpn_0),
	(troop_get_inventory_slot, ":item", ":troop", 0),
	(try_begin),
		(ge, ":item", 0),
		(str_store_item_name, s10, ":item"),
	(else_try),
		(str_store_string, s10, "str_dplmc_none"),
	(try_end),
	(val_add, ":upg", "str_dplmc_hero_wpn_slot_none"),
	(str_store_string, s1, ":upg"),
	(str_store_string, s0, "@{s0}^{s1}"),
	(troop_get_slot, ":upg", ":troop", dplmc_slot_upgrade_wpn_1),
	(troop_get_inventory_slot, ":item", ":troop", 1),
	(try_begin),
		(ge, ":item", 0),
		(str_store_item_name, s10, ":item"),
	(else_try),
		(str_store_string, s10, "str_dplmc_none"),
	(try_end),
	(val_add, ":upg", "str_dplmc_hero_wpn_slot_none"),
	(str_store_string, s1, ":upg"),
	(str_store_string, s0, "@{s0}^{s1}"),
	(troop_get_slot, ":upg", ":troop", dplmc_slot_upgrade_wpn_2),
	(troop_get_inventory_slot, ":item", ":troop", 2),
	(try_begin),
		(ge, ":item", 0),
		(str_store_item_name, s10, ":item"),
	(else_try),
		(str_store_string, s10, "str_dplmc_none"),
	(try_end),
	(val_add, ":upg", "str_dplmc_hero_wpn_slot_none"),
	(str_store_string, s1, ":upg"),
	(str_store_string, s0, "@{s0}^{s1}"),
	(troop_get_slot, ":upg", ":troop", dplmc_slot_upgrade_wpn_3),
	(troop_get_inventory_slot, ":item", ":troop", 3),
	(try_begin),
		(ge, ":item", 0),
		(str_store_item_name, s10, ":item"),
	(else_try),
		(str_store_string, s10, "str_dplmc_none"),
	(try_end),
	(val_add, ":upg", "str_dplmc_hero_wpn_slot_none"),
	(str_store_string, s1, ":upg"),
	(str_store_string, s0, "@{s0}^{s1}"),
])
]
