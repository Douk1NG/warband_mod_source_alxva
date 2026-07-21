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

age_troop_one_year_scripts = [
("age_troop_one_year",
    [
	(store_script_param, ":troop_no", 1),
    ##diplomacy start+ use gender script
	#(troop_get_type, ":is_female", ":troop_no"),
	(assign, ":save_reg0", reg0),
	(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
	(assign, ":is_female", reg0),
	(assign, reg0, ":save_reg0"),
	##diplomacy end+

	(troop_get_slot, ":age", ":troop_no", slot_troop_age),
	(troop_get_slot, ":appearance", ":troop_no", slot_troop_age_appearance),

	(val_add, ":age", 1),
	(store_random_in_range, ":addition", 1, 5),

	(try_begin),
		(eq, ":is_female", 1),
#		(val_add, ":addition", 2), #the women's age slider seems to produce less change than the male one - commented out: makes women look too old.
	(try_end),

	(val_add, ":appearance", ":addition"),
	(try_begin),
		(gt, ":age", 45),
		(store_attribute_level, ":strength", ":troop_no", ca_strength),
		(store_attribute_level, ":agility", ":troop_no", ca_agility),
		(store_random_in_range, ":random", 0, 50), #2% loss brings it down to about 36% by age 90, but of course can be counteracted by new level gain
		(try_begin),
			(lt, ":random", ":strength"),
			(troop_raise_attribute, ":troop_no", ca_strength, -1),
		(try_end),
		(try_begin),
			(lt, ":random", ":agility"),
			(troop_raise_attribute, ":troop_no", ca_agility, -1),
		(try_end),
	(try_end),

	(val_clamp, ":appearance", 1, 100),

	(troop_set_slot, ":troop_no", slot_troop_age, ":age"),
	(troop_set_slot, ":troop_no", slot_troop_age_appearance, ":appearance"),
	(troop_set_age, ":troop_no", ":appearance"),
	])
]
