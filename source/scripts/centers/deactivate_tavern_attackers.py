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

deactivate_tavern_attackers_scripts = [
("deactivate_tavern_attackers",
	[
	  (finish_party_battle_mode),
	  (try_for_agents, ":cur_agent"),
	    (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
	    (this_or_next|eq, ":cur_agent_troop", "trp_fugitive"),
	    (this_or_next|eq, ":cur_agent_troop", "trp_belligerent_drunk"),
	    (eq, ":cur_agent_troop", "trp_hired_assassin"),
	    (agent_set_team, ":cur_agent", 0),
	    (agent_ai_set_aggressiveness, ":cur_agent", 0),
	  (try_end),
	])
]
