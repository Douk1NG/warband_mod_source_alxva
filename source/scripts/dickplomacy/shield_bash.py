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

shield_bash_scripts = [
### Dice game ### Three Cards ### END ###
#COMBAT OSP BEGIN
#Shield Bash Script
("shield_bash",[
(this_or_next|multiplayer_is_server),
(neg|game_in_multiplayer_mode),
(get_player_agent_no,":player_agent"),
(store_skill_level,":shield_level", "skl_shield", "trp_player"),
(store_sub, ":player_shield_bash_time", 15, ":shield_level"),
(val_div,":player_shield_bash_time",3),
(store_mission_timer_a, ":current_time"),
(agent_get_slot, ":slot_last_shield_bash_time", ":player_agent", 27),
(store_add, ":time_to_shield_bash", ":player_shield_bash_time",":slot_last_shield_bash_time"),

(store_add, ":shieldstat", 1, ":shield_level"),
(store_mul, ":bash_radius", 13, ":shieldstat"),
(try_begin),
(ge, ":current_time", ":time_to_shield_bash"),
(try_begin),
(gt, ":player_agent", 0),
(agent_get_animation, ":anim", ":player_agent",0),
(agent_get_horse, ":my_horse", ":player_agent"),
(agent_get_wielded_item, ":shield_item", ":player_agent", 1),
(try_begin),
	(neq, ":anim", "anim_human_shield_bash"),
	(eq, ":my_horse", -1),
	(item_get_type, ":item_type", ":shield_item"),
	(eq, ":item_type", itp_type_shield),
	(agent_set_animation, ":player_agent","anim_human_shield_bash"),
	(agent_get_position, pos63,":player_agent"),
	(position_move_y,pos63,50),
	(agent_get_troop_id, ":id", ":player_agent"),
	(troop_get_type, ":type", ":id"),
	(try_begin),
		(eq, ":type", tf_male),
		(agent_play_sound, ":player_agent", "snd_man_grunt"), # Keep it down, this is a library.
		(agent_set_slot, ":player_agent", 27, ":current_time"),
	(else_try),
		(agent_play_sound, ":player_agent", "snd_woman_grunt"),	# Shhh...
        (agent_set_slot, ":player_agent", 27, ":current_time"),
	(try_end),
	(try_for_agents,":agent"),
		(gt, ":agent", 0),
		(neg|agent_is_ally,":agent"),#don't bash allies
		(agent_is_human, ":agent"),#stop if not human
		(agent_is_active,":agent"),
		(agent_is_alive,":agent"),
		(try_begin),
			(agent_get_position,pos62,":agent"),
			(get_distance_between_positions,":dist",pos63,pos62),
			(lt,":dist",":bash_radius"),# Now based on shield skill, not doing this for NPCs because that might get expensive.
			(agent_get_horse, ":horse", ":agent"),
			(eq, ":horse", -1),
			(neq,":agent",":player_agent"),
			(agent_play_sound, ":player_agent", "snd_wooden_hit_low_armor_high_damage"),
			(position_move_y,pos62,-25),
			(agent_set_position, ":agent", pos62),
			(try_begin),
				(store_random_in_range, ":rand", 3, 10), # No chance for critical strike unless shield skill +3
				(gt, ":shield_level", ":rand"),
				(agent_set_animation, ":agent","anim_shield_strike"),
			(else_try),
				(agent_set_animation, ":agent", "anim_shield_strike_small"),
			(try_end),
		(try_end),
	(try_end),
	(try_end),
(try_end),
(else_try),
#(display_message, "@You don't have enough shield skill to shield bash again this soon."),
# This message is super spammy and it's absolutely useless after the first time the palyer ever sees it.
(try_end),
])
]
