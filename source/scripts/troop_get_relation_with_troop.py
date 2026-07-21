# ======================================================================
# SHARED DEPENDENCY
# Entity: troop_get_relation_with_troop (script)
# Called by menus in 4 domains: cheats, court, reports, town
# ======================================================================

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

troop_get_relation_with_troop_scripts = [
("troop_get_relation_with_troop",
    [
	(store_script_param, ":troop1", 1),
	(store_script_param, ":troop2", 2),

	(assign, ":relation", 0),
	(try_begin),
		##diplomacy start+
		#Change "eq -1", to "lt 0"
		(this_or_next|lt, ":troop1", 0),
			(lt, ":troop2", 0),
		##diplomacy end+

		#Possibly switch to relation with liege
		(assign, ":relation", 0),
	(else_try),
		(eq, ":troop1", "trp_player"),
		(call_script, "script_troop_get_player_relation", ":troop2"),
		(assign, ":relation", reg0),
	(else_try),
		(eq, ":troop2", "trp_player"),
		(call_script, "script_troop_get_player_relation", ":troop1"),
		(assign, ":relation", reg0),
	(else_try),
		(store_add, ":troop1_slot_for_troop2", ":troop2", slot_troop_relations_begin),
		(troop_get_slot, ":relation", ":troop1", ":troop1_slot_for_troop2"),
	(try_end),


	(val_clamp, ":relation", -100, 101),
	(assign, reg0, ":relation"),

	])
]
