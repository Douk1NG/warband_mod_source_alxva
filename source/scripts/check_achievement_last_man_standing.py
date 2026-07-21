# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

check_achievement_last_man_standing_scripts = [
("check_achievement_last_man_standing",
   [
   #LAST_MAN_STANDING achievement
	  (try_begin),
	    (store_script_param, ":value", 1),
		(is_between, ":value", 0, 2), #defender or attacker wins
	    (try_begin),
		  (eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
		  (multiplayer_get_my_player, ":my_player_no"),
		  (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
		  (player_get_agent_id, ":my_player_agent", ":my_player_no"),
		  (ge, ":my_player_agent", 0),
		  (agent_is_alive, ":my_player_agent"),
		  (agent_get_team, ":my_player_agent_team_no", ":my_player_agent"),
		  (eq, ":my_player_agent_team_no", ":value"), #winner team
		  (unlock_achievement, ACHIEVEMENT_LAST_MAN_STANDING),
		(try_end),
	  (try_end),
    #LAST_MAN_STANDING achievement end
    ])
]
