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

party_inflict_attrition_scripts = [
("party_inflict_attrition", #parameters from dialog
	[
	(store_script_param, ":party", 1),
	(store_script_param, ":attrition_rate", 2),
#	(store_script_param, ":attrition_type", 3), #1 = desertion, 2 = sickness

    (party_clear, "p_temp_casualties"),

	(party_get_num_companion_stacks, ":num_stacks", ":party"),

	#add to temp casualties
	(try_for_range, ":stack", 0, ":num_stacks"),
		(party_stack_get_troop_id, ":troop_type", ":party", ":stack"),
		(neg|troop_is_hero, ":troop_type"),
		(party_stack_get_size, ":size", ":party", ":stack"),
		(store_mul, ":casualties_x_100", ":attrition_rate", ":size"),
		(store_div, ":casualties", ":casualties_x_100", 100),
		(party_add_members, "p_temp_casualties", ":troop_type", ":casualties"),

		(store_mul, ":subtractor", ":casualties", 100),
		(store_sub, ":chance_of_additional_casualty", ":casualties_x_100", ":subtractor"),

		(try_begin),
			(gt, ":chance_of_additional_casualty", 0),
			(store_random_in_range, ":random", 0, 100),
			(lt, ":random", ":chance_of_additional_casualty"),
			(party_add_members, "p_temp_casualties", ":troop_type", ":casualties"),
		(try_end),

#		(try_begin),
#			(eq, "$cheat_mode", 1),
#			(str_store_party_name, s7, ":party"),
#           		...
#		(try_end),
	(try_end),

	#take temp casualties from main party
	(party_get_num_companion_stacks, ":num_stacks", "p_temp_casualties"),

	#add to temp casualties
	(try_for_range, ":stack", 0, ":num_stacks"),
		(party_stack_get_troop_id, ":troop_type", "p_temp_casualties", ":stack"),
		(party_stack_get_size, ":size", "p_temp_casualties", ":stack"),
		(party_remove_members, ":party", ":troop_type", ":size"),

		(eq, "$cheat_mode", 1),
		(assign, reg3, ":size"),
		(str_store_troop_name, s4, ":troop_type"),
		(str_store_party_name, s5, ":party"),
#		(display_message, "str_s5_suffers_attrition_reg3_x_s4"),
		(str_store_string, s65, "str_s5_suffers_attrition_reg3_x_s4"),
		(display_message, "str_s65"),
		(try_begin),
			(eq, "$debug_message_in_queue", 0),
			(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),
			(assign, "$debug_message_in_queue", 1),
		(try_end),
	(try_end),

	])
]
