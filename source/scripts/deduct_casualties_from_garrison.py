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

deduct_casualties_from_garrison_scripts = [
("deduct_casualties_from_garrison", #after a battle in a center, deducts any casualties from "$g_encountered_party"
	[
	##(display_message, "str_totalling_casualties_caused_during_mission"),

	(try_for_agents, ":agent"),
		(agent_get_troop_id, ":troop_type", ":agent"),
		(is_between, ":troop_type", regular_troops_begin, regular_troops_end),

		(neg|agent_is_alive, ":agent"),

		(try_begin), #if troop not present, search for another type which is
			(store_troop_count_companions, ":number", ":troop_type", "$g_encountered_party"),
			(eq, ":number", 0),
			(assign, ":troop_type", 0),
			(try_for_range, ":new_tier", slot_faction_tier_1_troop, slot_faction_tier_5_troop),
			(faction_get_slot, ":troop_type", "$g_encountered_party_faction", ":new_tier"),
				(faction_get_slot, ":new_troop_type", "$g_encountered_party_faction", ":new_tier"),
				(store_troop_count_companions, ":number", ":new_troop_type", "$g_encountered_party"),
				(gt, ":number", 0),
				(assign, ":troop_type", ":new_troop_type"),
			(try_end),
		(try_end),

		(gt, ":troop_type", 0),

		(party_remove_members, "$g_encountered_party", ":troop_type", 1),
		(str_store_troop_name, s4, ":troop_type"),
		(str_store_party_name, s5, "$g_encountered_party"),
	(try_end),
	])
]
