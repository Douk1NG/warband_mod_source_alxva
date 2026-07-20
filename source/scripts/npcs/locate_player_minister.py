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

locate_player_minister_scripts = [
("locate_player_minister", #maybe deprecate this
    [
	##diplomacy start+ Handle player is co-ruler of NPC faction
	(assign, ":alt_faction", "fac_player_supporters_faction"),
	(try_begin),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(assign, ":alt_faction", "$players_kingdom"),
	(try_end),
	##diplomacy end+
	(assign, ":walled_center_found", 0),
	(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
		(lt, ":walled_center_found", centers_begin),
		(store_faction_of_party, ":walled_center_faction", ":walled_center"),
		##diplomacy start+
		(this_or_next|eq, ":walled_center_faction", ":alt_faction"),
		##diplomacy end+
		(eq, ":walled_center_faction", "fac_player_supporters_faction"),
		(neg|party_slot_ge, ":walled_center", slot_town_lord, active_npcs_begin), #ie, player or a reserved slot
		(assign, ":walled_center_found", ":walled_center"),
	(try_end),

	(troop_get_slot, ":old_location", "$g_player_minister", slot_troop_cur_center),
	(troop_set_slot, "$g_player_minister", slot_troop_cur_center, ":walled_center_found"),

	(try_begin),
		(neq, ":old_location", ":walled_center"),
		(str_store_party_name, s10, ":walled_center"),
		(str_store_troop_name, s11, "$g_player_minister"),
		(display_message, "str_s11_relocates_to_s10"),
	(try_end),

	])
]
