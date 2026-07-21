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

find_customizable_item_equipped_on_troop_scripts = [
#script_find_customizable_item_equipped_on_troop
# INPUT: 	troop_no
# OUTPUT: none
# SETS: 	item (g_current_opened_item_details)
("find_customizable_item_equipped_on_troop",
	[

	#Here's my lazy way.
	 (store_script_param, ":troop_no", 1),
	 (assign, "$g_current_opened_item_details", -1),
	 (assign, ":begin", ek_item_0), #should add a global as iterator
     (try_for_range, ":item_slot", ":begin", ek_foot),
		(troop_get_inventory_slot, ":item_no", ":troop_no", ":item_slot"),
		(gt, ":item_no", -1),
		(this_or_next|eq, ":item_no", itm_custom_armor1),
		(this_or_next|eq, ":item_no", itm_custom_armor2),
		(this_or_next|eq, ":item_no", itm_custom_armor3),
		(this_or_next|eq, ":item_no", itm_plate_helm_dthun),
		(eq, ":item_no", itm_angela_helm),
		(assign, "$g_current_opened_item_details", ":item_no"),
	 (else_try),
		(troop_get_type, ":is_female", ":troop_no"),
		(eq, ":is_female", 5),
		(assign, "$g_current_opened_item_details", "itm_body_fem"),
     (try_end),
	 (gt, "$g_current_opened_item_details", -1),
	# (store_script_param, ":troop_no", 1),
	# (assign, "$g_current_opened_item_details", -1),
	# (assign, ":begin", ek_item_0), #should add a global as iterator
    # (try_for_range_backwards, ":item_slot", ":begin", ek_foot),	#backwards: body armor first
	#	(troop_get_inventory_slot, ":item_no", ":troop_no", ":item_slot"),
	#	(gt, ":item_no", -1),
	#	(item_slot_ge, ":item_no", slot_item_num_components, 1),
	#	(assign, "$g_current_opened_item_details", ":item_no"),
	#	(assign, ":begin", ek_foot),
    # (else_try),	#to be able to change tattoo without custom item # Good idea but leads to unexpected results with the other body, best to just disable it.
	#	(troop_get_type, ":is_female", ":troop_no"),
	#	(ge, ":is_female", 1),
	#	(troop_get_inventory_slot, ":item_no", ":troop_no", ek_body),
	#	(try_begin),
	#		(gt, ":item_no", -1),
	#		(assign, "$g_current_opened_item_details", ":item_no"),
	#	(else_try),
	#		(assign, "$g_current_opened_item_details", "itm_body_fem"),
	#	(try_end),
    # (try_end),
	]
  )
]
