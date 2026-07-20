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

set_custom_armor_slots_scripts = [
("set_custom_armor_slots",
	[
	   #set slots random for everyone
		(try_for_range, ":npc", 0, "trp_coop_companion_equipment_ui_0"),
			(try_for_range, ":slot_no", slot_troop_armor_slots_begin, slot_troop_helm_slots_end),
				(troop_set_slot, ":npc", ":slot_no", -1), # random = -1
			(try_end),
		(try_end),

	    #(display_message, "@Initializing troop slots DONE"),

	   #Light
		(item_set_slot, "itm_custom_armor1", slot_item_num_components, 14), #14 customizable
		(item_set_slot, "itm_custom_armor1", slot_item_init_script, "script_init_custom_armor1"),
	   #Medium
		(item_set_slot, "itm_custom_armor2", slot_item_num_components, 14), #14 customizable
		(item_set_slot, "itm_custom_armor2", slot_item_init_script, "script_init_custom_armor2"),
	   #Heavy
		(item_set_slot, "itm_custom_armor3", slot_item_num_components, 14), #14 customizable
		(item_set_slot, "itm_custom_armor3", slot_item_init_script, "script_init_custom_armor3"),
	   #Plate Helm
		(item_set_slot, "itm_plate_helm_dthun", slot_item_num_components, 1), #1 customizable
		(item_set_slot, "itm_plate_helm_dthun", slot_item_init_script, "script_init_plate_helm_dthun"),
	   #Angela Helm
		(item_set_slot, "itm_angela_helm", slot_item_num_components, 3), #3 customizable
		(item_set_slot, "itm_angela_helm", slot_item_init_script, "script_init_angela_helm"),
		#(try_for_range, ":slot_no", slot_item_player_slots_begin, slot_item_player_slots_end + 1), # troop slots added insted item slots
		#  (item_set_slot, "itm_plate_helm_dthun", ":slot_no", -1), # random = -1
		#(try_end),

		#(display_message, "@Initializing armor slots DONE"),

		#(troop_set_slot, "trp_player", slot_troop_tattoo, 0),
	]
  )
]
