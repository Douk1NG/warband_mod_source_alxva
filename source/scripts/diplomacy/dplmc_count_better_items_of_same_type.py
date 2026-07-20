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

dplmc_count_better_items_of_same_type_scripts = [
##diplomacy start+
#"script_dplmc_count_better_items_of_same_type"
#
#INPUT:
#   arg1 :inventory_troop
#   arg2 :item
#   arg2 :item_imod
#   arg3 :troop_using
#
#OUTPUT:
#   reg0 number of items of same type
("dplmc_count_better_items_of_same_type", [
	(store_script_param, ":inventory_troop",1),
	(store_script_param, ":base_item",2),
	(store_script_param, ":base_imod",3),
	(store_script_param, ":troop_using", 4),

	(assign, ":number_better_of_type", 0),
	#(assign, ":total_items_of_type", 0),

	# (item_get_type, ":main_item_type", ":base_item"),
	# (try_begin),
		# (item_has_property, ":item", itp_type_two_handed_wpn),
		# (neg|item_has_property, ":item", itp_two_handed),
		# (assign, ":main_item_type", 11), # type 11 = two-handed/one-handed
	# (try_end),
    #SB : metatype
    (call_script, "script_item_get_type_aux", ":base_item"),
    (assign, ":main_item_type", reg0),

	(call_script, "script_dplmc_get_item_score_with_imod", ":base_item", ":base_imod"),
	(assign, ":primary_score", reg0),

	(call_script, "script_dplmc_troop_can_use_item", ":troop_using", ":base_item", ":base_imod"),
	(assign, ":can_use", 1),
	(try_begin),
		(neq, reg0, 1),
		(assign, ":primary_score", -1000),
		(assign, ":can_use", 0),
	(try_end),
	(assign, ":exact_matches_found", 0),

	(troop_get_inventory_capacity, ":inv_cap", ":inventory_troop"),
	(try_for_range, ":i_slot", 0, ":inv_cap"),
		(troop_get_inventory_slot, ":item", ":inventory_troop", ":i_slot"),
		(ge, ":item", 0),
        # SB : metatype
        (call_script, "script_item_get_type_aux", ":item"),
		(eq, ":main_item_type", reg0),
		#(val_add, ":total_items_of_type", 1),
		(troop_get_inventory_slot_modifier, ":imod", ":inventory_troop", ":i_slot"),
		(call_script, "script_dplmc_troop_can_use_item", ":troop_using", ":item", ":imod"),
		(this_or_next|eq, ":can_use", 0),
			(ge, reg0, 1),
		(try_begin),
			(eq, ":item", ":base_item"),
			(eq, ":imod", ":base_imod"),
			(val_add, ":exact_matches_found", 1),
		(try_end),
		(this_or_next|neq, ":item", ":base_item"),
		(this_or_next|neq, ":imod", ":base_imod"),
			(ge, ":exact_matches_found", 2),
		(call_script, "script_dplmc_get_item_score_with_imod", ":item", ":imod"),
		(ge, reg0, ":primary_score"),#deliberately ge instead of gt because of what I want this for
		(val_add, ":number_better_of_type", 1),
	(try_end),

	(assign, reg0, ":number_better_of_type"),
	#(assign, reg1, ":total_items_of_type"),
])
]
