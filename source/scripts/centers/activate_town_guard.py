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

activate_town_guard_scripts = [
("activate_town_guard",
	[
	  (set_party_battle_mode),
	  #(get_player_agent_no, ":player_agent"),
	  #(agent_get_team, ":player_team", ":player_agent"),

	  (try_for_agents, ":cur_agent"),
	    (agent_get_troop_id, ":troop_type", ":cur_agent"),
	    (is_between, ":troop_type", soldiers_begin, soldiers_end), #dckplmc
        (agent_set_team, ":cur_agent", 1),
        #(team_give_order, 1, grc_everyone, mordr_charge), - for some reason, this freezes everyone if the player is not yet spawned
		#(try_begin),
		#	(eq, "$g_main_attacker_agent", 0),
		#	(assign, "$g_main_attacker_agent", ":cur_agent"),
		#(try_end),
	(else_try),
		(this_or_next|is_between, ":troop_type", walkers_begin, walkers_end),
		(is_between, ":troop_type", armor_merchants_begin, mayors_end),

		(agent_clear_scripted_mode, ":cur_agent"),
		#(agent_set_team, ":cur_agent", 2), #dckplmc don't want town guards to massacre townsfolk
	(try_end),
	])
]
