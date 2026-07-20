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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

diplomacy_faction_get_diplomatic_status_with_faction_scripts = [
# INPUT:
(
	"diplomacy_faction_get_diplomatic_status_with_faction",
	#result: -1 faction_1 has a casus belli against faction_2. 1, faction_1 has a truce with faction_2, -2, the two factions are at war
	[
	(store_script_param, ":actor_faction", 1),
	(store_script_param, ":target_faction", 2),
	##diplomacy start+
	#Since "fac_player_supporters_faction" is used as a shorthand for the faction
	#run by the player, intercept that here instead of the various places this is
	#called from.
	(call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":actor_faction", ":target_faction"),
	(assign, ":actor_faction", reg0),
	(assign, ":target_faction", reg1),
	##diplomacy end+

	(store_add, ":truce_slot", ":target_faction", slot_faction_truce_days_with_factions_begin),
	(store_add, ":provocation_slot", ":target_faction", slot_faction_provocation_days_with_factions_begin),
	(val_sub, ":truce_slot", kingdoms_begin),
	(val_sub, ":provocation_slot", kingdoms_begin),

	(assign, ":result", 0),
	(assign, ":duration", 0),

	(try_begin),
		(store_relation, ":relation", ":actor_faction", ":target_faction"),
		(lt, ":relation", 0),
		(assign, ":result", -2),
	(else_try),
		(faction_slot_ge, ":actor_faction", ":truce_slot", 1),
		(assign, ":result", 1),

		(faction_get_slot, ":duration", ":actor_faction", ":truce_slot"),
	(else_try),
		(faction_slot_ge, ":actor_faction", ":provocation_slot", 1),
		(assign, ":result", -1),

		(faction_get_slot, ":duration", ":actor_faction", ":provocation_slot"),
	(try_end),

	(assign, reg0, ":result"),
	(assign, reg1, ":duration"),
	])
]
