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

remove_body_from_inventory_scripts = [
#script_add_troop_to_custom_armor_tableau
# INPUT: troop_no, item (g_current_opened_item_details), side (g_custom_armor_angle)
# OUTPUT: none
("remove_body_from_inventory",
    [
		(store_script_param, ":troop_no", 1),
		(troop_get_type, ":is_female", ":troop_no"),
		(try_begin),
			(ge, ":is_female", 1),	#check: body/loincloth equipped ->remove it from inventory (equipped in character window for face morph scene)
			(try_begin),	# troop has it from opening character tab till next inventory opening -> can lose it in battle, has unique flag -> won't see back (hopefully noone equips it)
				(troop_has_item_equipped, ":troop_no", "itm_body_fem"),
				(troop_remove_item, ":troop_no", "itm_body_fem"),
			(else_try),
				(troop_has_item_equipped, ":troop_no", "itm_loincloth"),
				(troop_remove_item, ":troop_no", "itm_loincloth"),
			(else_try),
				#(eq, "$g_cenzura", 1),
				(eq, 0, 1),
				(try_begin),
					(troop_has_item_equipped, ":troop_no", "itm_loin_top"),
					(troop_remove_item, ":troop_no", "itm_loin_top"),
				(else_try),
					(troop_has_item_equipped, ":troop_no", "itm_loin_skirt"),
					(troop_remove_item, ":troop_no", "itm_loin_skirt"),
				(try_end),
			(try_end),
		(try_end),
     ])
]
