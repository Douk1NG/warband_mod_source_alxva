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

agent_shield_bash_scripts = [
#RAMARAUNT SCRIPT - with code from Xenoargh's shield bashing OSP.
#AI shield bashing script
("agent_shield_bash",[
(this_or_next|multiplayer_is_server),
(neg|game_in_multiplayer_mode),
(store_script_param, ":agent", 1),
(agent_get_troop_id, ":troop_id", ":agent"),
(store_skill_level,":shield_level", "skl_shield", ":troop_id"),
(gt, ":shield_level", 5),
(store_sub, ":agent_shield_bash_time", 13, ":shield_level"),
(store_mission_timer_a, ":current_time"),
#Ren - I don't think we need all these nested trys but I'm not familiar enough with this script to mess with it.
(try_begin),
(agent_get_wielded_item, ":shield_item", ":agent", 1),
(neq, ":shield_item", -1),
(neq, ":shield_item", 0),
(item_get_type, ":item_type", ":shield_item"),
(eq, ":item_type", itp_type_shield),
(agent_get_slot, ":slot_last_shield_bash_time", ":agent", 27),
(store_add, ":time_to_shield_bash", ":agent_shield_bash_time",":slot_last_shield_bash_time"),
(try_begin),
(ge, ":current_time", ":time_to_shield_bash"),
(try_begin),
(gt, ":agent", 0),
(agent_get_animation, ":anim", ":agent",0),
(agent_get_horse, ":my_horse", ":agent"),
(try_begin),
	(neq, ":anim", "anim_human_shield_bash"),
	(eq, ":my_horse", -1),
	(agent_set_animation, ":agent","anim_human_shield_bash"),
	(agent_get_position, pos63,":agent"),
	(position_move_y,pos63,75),#75 cm directly ahead, so it's not a cuboid space around player center
	(agent_get_troop_id, ":id", ":agent"),
	(troop_get_type, ":type", ":id"),
	(try_begin),
		(eq, ":type", tf_male),
		(agent_play_sound, ":agent", "snd_man_grunt"),
		(agent_set_slot, ":agent", 27, ":current_time"),
	    #(display_message, "@{s2} has shield bashed!"),
	(else_try),
		(agent_play_sound, ":agent", "snd_woman_grunt"),
        (agent_set_slot, ":agent", 27, ":current_time"),
		#(display_message, "@{s2} has shield bashed!"),
	(try_end),
	(try_for_agents,":victims"),
		(gt, ":victims", 0),
		(agent_get_team, ":victim_team", ":victims"),
		(agent_get_team, ":agent_team", ":agent"),
		(teams_are_enemies, ":victim_team", ":agent_team"), #don't bash allies
		(agent_is_human, ":victims"),#stop if not human
		(agent_is_active,":victims"),
		(agent_is_alive,":victims"),
		(try_begin),
			(agent_get_position,pos62,":victims"),
			(get_distance_between_positions,":dist",pos63,pos62),
			(lt,":dist",100),#Set this to whatever you like- 1 meter radius clears a big section of crowd
			(agent_get_horse, ":horse", ":victims"),
			(eq, ":horse", -1),
			(neq,":agent",":victims"),
			(agent_play_sound, ":victims", "snd_wooden_hit_low_armor_high_damage"),
			(position_move_y,pos62,-25),
			(agent_set_position, ":victims", pos62),
			(try_begin),
				(store_random_in_range, ":rand", 6, 10), # No chance for critical strike unless shield skill +3
				(gt, ":shield_level", ":rand"),
				(agent_set_animation, ":agent","anim_shield_strike"),
			(else_try),
				(agent_set_animation, ":agent", "anim_shield_strike_small"),
			(try_end),
            (try_begin),
                (get_player_agent_no,":player"),
                (eq,":victims",":player"),
                (display_message, "@You have been shield bashed!"),
            (try_end),
		(try_end),
	(try_end),
	(try_end),
(try_end),
(try_end),
(try_end),
])
]
