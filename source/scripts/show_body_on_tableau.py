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

show_body_on_tableau_scripts = [
#DtheHun
#script_add_troop_to_custom_armor_tableau
# INPUT: troop_no, item (g_current_opened_item_details), side (g_custom_armor_angle)
# OUTPUT: reg0 (-1):do nothing, (0):equip body, (1):equip loincloth - for additional troop equip if must (character -> face morpf)
("show_body_on_tableau",
    [
		(store_script_param, ":troop_no", 1),
		(assign, reg0, -1),
		(try_begin),
			(troop_get_type, ":is_female", ":troop_no"),
			(ge, ":is_female", 1),
			(troop_get_inventory_slot, ":item_no", ":troop_no", ek_body),
			(eq, ":item_no", -1), #-1:none equipped
			(cur_tableau_clear_override_items),
			(cur_tableau_set_override_flags, af_override_everything), # makes it possible to set_override ek_body item without adding it to troop
			(try_begin),
				#(eq, "$g_cenzura", 1),
				(eq, 0, 1),
				(cur_tableau_add_override_item, "itm_loincloth"),
				(assign, reg0, 1),
			(else_try),
				(cur_tableau_add_override_item, "itm_body_fem"),
				(assign, reg0, 0),
			(try_end),
			(try_for_range, ":item_slot", ek_head, ek_horse), # do removed clothes back
				(troop_get_inventory_slot, ":item_no", ":troop_no", ":item_slot"),
				(ge, ":item_no", 0),
				(cur_tableau_add_override_item, ":item_no"),
			(try_end),
		(try_end),
     ])
]
