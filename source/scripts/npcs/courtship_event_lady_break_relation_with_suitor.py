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

courtship_event_lady_break_relation_with_suitor_scripts = [
("courtship_event_lady_break_relation_with_suitor", #parameters from dialog
	[
	(store_script_param, ":lady", 1),
	(store_script_param, ":suitor", 2),

	(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
		(troop_slot_eq, ":suitor", ":love_interest_slot", ":lady"),
		##diplomacy start+ set to -1 instead, since 0 is the player (how annoying)
		#(troop_set_slot, ":suitor", ":love_interest_slot", 0),
		(troop_set_slot, ":suitor", ":love_interest_slot", -1),
		##diplomacy end+
	(try_end),
	(call_script, "script_assign_troop_love_interests", ":suitor"),

	(try_begin),
		(troop_slot_eq, ":lady", slot_troop_betrothed, ":suitor"),


		(troop_set_slot, ":lady", slot_troop_betrothed, -1),
	##diplomacy start+ perform the same check for the suitor that was done,
	#for the lady, so this script has no unfortunate consequences even if
	#called inappropriately.
	(try_end),
	(try_begin),
		(troop_slot_eq, ":suitor", slot_troop_betrothed, ":lady"),
		(troop_set_slot, ":suitor", slot_troop_betrothed, -1),
	##diplomacy end+
	(try_end),


	])
]
