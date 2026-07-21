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

cf_vc_decap_check_if_possible_scripts = [
#End Shield Bash Script
#VIKING CONQUEST DECAP STUFF - NOTE THIS CODE IS SLIGHTLY ALTERED CODE FROM VC, WHICH IS LEGAL AS LONG AS YOU GIVE CREDIT - Ramaraunt
("cf_vc_decap_check_if_possible",
	[
    #Check if the player has decapitation enabled first
    (try_begin),
    (ge, "$g_decapitation_enabled", 1),
    (store_script_param_1, ":inflicted_agent_id"),
	(store_script_param_2, ":damage"),
	(store_script_param, ":weapon_id",3),
	(store_script_param, ":attacker_id", 4),

	# Can't be: player, hero or horse nor female
	(agent_is_non_player, ":inflicted_agent_id"),
	(agent_get_troop_id, ":troop_inflicted", ":inflicted_agent_id"),
	(neg | troop_is_hero,":troop_inflicted"),
	(agent_is_human, ":inflicted_agent_id"),
	(troop_get_type, ":is_female", ":troop_inflicted"),
	(val_mod, ":is_female", 2),
	(neq, ":is_female", 1),

	#test if head hit
	(agent_get_position, pos1, ":inflicted_agent_id"),
	(get_distance_between_positions, ":distance", pos1, pos0),
	(is_between, ":distance", 90, 185), # *zing*

	#test if within melee range (this stops most ranged decaps unless they are SUPER close, which doesnt happen often so its ok)
	(agent_get_position, pos2, ":attacker_id"),
	(get_distance_between_positions, ":distance", pos2, pos1),
	(is_between, ":distance", 0, 200),


	# test weapon: cutting damage from a weapon (no missiles)
	(gt, ":weapon_id", 0),
	(item_get_swing_damage_type, ":damage_type", ":weapon_id"),
	(eq, ":damage_type", cut),

	# test to make sure it's a huge hit
	(ge, ":damage", 40),

	# test if agent is dying from the hit
	(store_agent_hit_points, ":inflicted_hp", ":inflicted_agent_id", 1),
	(store_sub, ":inflicted_new_hp", ":inflicted_hp", ":damage"),
	(le, ":inflicted_new_hp", 0),
    (try_end),
      ])
]
