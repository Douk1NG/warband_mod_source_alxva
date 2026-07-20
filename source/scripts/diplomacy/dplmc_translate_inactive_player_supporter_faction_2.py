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

dplmc_translate_inactive_player_supporter_faction_2_scripts = [
## "script_dplmc_store_troop_is_eligible_for_affiliate_messages"
#
#Since "fac_player_supporters_faction" is often used as a parameter when what
#is really meant is "the faction led by the player" (which is never a different
#faction in Native), there are many calls we want to change.  Another solution
#is to approach the problem from the other side, and "correct" the arguments.
#
#If exactly one argument is equal to fac_player_supporters_faction, and fac_player_supporters_faction
#is not sfs_active, and $players_kingdom is an NPC kingdom of which the player is ruler or co-ruler,
#and the other argument is not equal to $players_kingdom, then the argument equal to fac_player_supporters_faction
#will be replaced with $players_kingdom.
#
#INPUT:
# arg1 - faction_1
# arg2 - faction_2
#OUTPUT:
# reg0 - faction_1, possibly replacing fac_player_supporters_faction with $players_kingdom (see above)
# reg1 - faction_2, possibly replacing fac_player_supporters_faction with $players_kingdom (see above)
("dplmc_translate_inactive_player_supporter_faction_2",
[
    (store_script_param_1, ":faction_1"),
    (store_script_param_2, ":faction_2"),

	(try_begin),
		(this_or_next|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
		(this_or_next|neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(this_or_next|eq, ":faction_1", "$players_kingdom"),
		(this_or_next|eq, ":faction_2", "$players_kingdom"),
			(eq, ":faction_1", ":faction_2"),
      #Do nothing
	(else_try),
		(eq, ":faction_1", "fac_player_supporters_faction"),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(assign, ":faction_1", "$players_kingdom"),
	(else_try),
		(eq, ":faction_2", "fac_player_supporters_faction"),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(assign, ":faction_2", "$players_kingdom"),
	(try_end),

	(assign, reg0, ":faction_1"),
	(assign, reg1, ":faction_2"),
])
]
