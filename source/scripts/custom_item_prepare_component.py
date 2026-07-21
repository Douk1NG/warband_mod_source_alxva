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

custom_item_prepare_component_scripts = [
#script_item_add_component
# INPUT: 	1:agent_no, 2:troop_no, 3:use_agent_slots, 4:item_script_no, 5:mesh_num, 6:random_begin, 7:random_end, 8:special_part
# 	$g_presentation_obj_item_select_2, reg1(:troop_item_slots_begin), reg2(:agent_item_slots_begin)
# OUTPUT: ":special_part" (reg3)
# SETS: 	item (g_current_opened_item_details)
("custom_item_prepare_component",
	[
	  (store_script_param, ":agent_no", 1),
	  (store_script_param, ":troop_no", 2),
      (store_script_param, ":use_agent_slots", 3),
	  (store_script_param, ":item_script_no", 4),
      (store_script_param, ":mesh_num", 5),
	  (store_script_param, ":random_begin", 6),
	  (store_script_param, ":random_end", 7),
	  (store_script_param, ":special_part", 8),	#(has requirements) 0: nothing, 1: assa. cover, 2:symm. with prev, 3: angela cover
	#GET
	  (store_add, ":troop_item_slot_no", reg1 , ":mesh_num"),
	  (store_add, ":agent_item_slot_no", reg2 , ":mesh_num"),	#<- only body

	  (try_begin),
		(try_begin),
			(eq, ":use_agent_slots", 0),
			(troop_get_slot, ":value", ":troop_no", ":troop_item_slot_no"), # slot_troop_armor_slots_begin + :mesh_num (0-13)
		(else_try),
			(agent_get_slot, ":value", ":agent_no", ":agent_item_slot_no"), #
		(try_end),
      #RANDOMIZE
		(eq, ":value", -1),
		(try_begin),
			(eq, "$g_dthehun_sync_random", 1),
			(troop_get_slot, ":value", "trp_temp_array_a", ":troop_item_slot_no"), # get prev random for tableau mask be sync.
		(else_try),
			(store_random_in_range, ":value", ":random_begin", ":random_end"),
			(try_begin), #special_part
			  #ass cover
				(eq, ":special_part", 1),
				(try_begin),
					(this_or_next|eq, ":value", 1),	# assassin
								 (eq, ":value", 2),	# Angela
					(try_begin),
						(this_or_next|troop_slot_eq, "trp_temp_array_a", slot_troop_armor_slots_begin + 0, 1), 	#has assa skin
						(this_or_next|troop_slot_eq, "trp_temp_array_a", slot_troop_armor_slots_begin + 2, 1), 	#has assa panty
						(this_or_next|troop_slot_eq, "trp_temp_array_a", slot_troop_armor_slots_begin + 2, 2), 	#has Angela panty
						(troop_slot_eq, "trp_temp_array_a", slot_troop_armor_slots_begin + 3, 1), 				#has assa belt
					(else_try),	#<- there is nothing to hanging on it
						(store_random_in_range, ":value", 1, ":random_end"), #<- new shuffle
						(eq, ":value", 1),
						(assign, ":value", 0),
					(try_end),
				(try_end),
			(else_try),
			  # symm. with previous component
				(eq, ":special_part", 2),
				(store_random_in_range, ":rand", 0, 6),	#(less than 16.66% could be asymmetric)
				(ge, ":rand", 1),
				(store_sub, ":prev_troop_item_slot_no", ":troop_item_slot_no", 1),
				(troop_get_slot, ":prev_value", "trp_temp_array_a", ":prev_troop_item_slot_no"),
				(assign, ":value", ":prev_value"),
			(try_end),
		(try_end),
	  (try_end),
	  (troop_set_slot, "trp_temp_array_a", ":troop_item_slot_no", ":value"), # remember randomization for tableau alpha
	  (try_begin),
		(neq, ":value", 0),
		(call_script, ":item_script_no", ":agent_no", ":troop_no", ":mesh_num", ":value"),#
		(neg|str_is_empty, s1),
		(cur_item_add_mesh, s1),
	  (try_end),
	]
  )
]
