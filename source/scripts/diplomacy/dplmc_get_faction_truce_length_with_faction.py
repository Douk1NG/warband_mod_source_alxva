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

dplmc_get_faction_truce_length_with_faction_scripts = [
#script_dplmc_lord_return_from_exile
# INPUT
#   arg1:  faction_1
#   arg2:  faction_2
# OUTPUT
#   reg0:  The length in days of faction_1's truce with faction_2, if any.
#          If no truce exists, the appropriate value to return is zero.
("dplmc_get_faction_truce_length_with_faction",
	   [
	    (store_script_param, ":faction_1", 1),
		(store_script_param, ":faction_2", 2),

		(assign, ":truce_length", 0),

		(try_begin),
			(is_between, ":faction_1", kingdoms_begin, kingdoms_end),
			(is_between, ":faction_2", kingdoms_begin, kingdoms_end),
			(neq, ":faction_1", ":faction_2"),
			(store_add, ":truce_slot", ":faction_2", slot_faction_truce_days_with_factions_begin),
			(val_sub, ":truce_slot", kingdoms_begin),
			(faction_get_slot, ":truce_length", ":faction_1", ":truce_slot"),
        (try_end),
	    (assign, reg0, ":truce_length"),
	   ])
]
