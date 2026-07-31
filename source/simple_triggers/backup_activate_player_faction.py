# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *




	#This is a backup script to activate the player faction if it doesn't happen automatically, for whatever reason
  

backup_activate_player_faction_simple_triggers = [
(3,
	[
	(try_for_range, ":center", walled_centers_begin, walled_centers_end),
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(store_faction_of_party, ":center_faction", ":center"),
		(eq, ":center_faction", "fac_player_supporters_faction"),
		(call_script, "script_activate_player_faction", "trp_player"),
	(try_end),
	##diplomacy start+
	#Piggyback on this: if the minister somehow gets cleared, or wasn't set
	#automatically, reappoint one.
	(try_begin),
		(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		(le, "$g_player_minister", 0),
		(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		(ge, ":faction_leader", 0),
		(try_begin),
			(this_or_next|eq, ":faction_leader", "trp_player"),
				(troop_slot_eq, "trp_player", slot_troop_spouse, ":faction_leader"),
			(assign, "$g_player_minister", "trp_temporary_minister"),
			(troop_set_faction, "trp_temporary_minister", "fac_player_supporters_faction"),
		(else_try),
			(is_between, ":faction_leader", heroes_begin, heroes_end),
			(troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
			(assign, "$g_player_minister", "trp_temporary_minister"),
			(troop_set_faction, "trp_temporary_minister", "fac_player_supporters_faction"),
		(try_end),
	(try_end),
	##diplomacy end+
	]),
]
