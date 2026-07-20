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

vc_decap_special_effects_scripts = [
# Description: for decapitation -> blood, helmet, spawn head
# Input: inflicted_agent_id, head_position
# Output: none
("vc_decap_special_effects",
    [
    #Check if the player has decapitation enabled first
    (try_begin),
    (ge, "$g_decapitation_enabled", 1),
    (store_script_param_1, ":inflicted_agent_id"),

      # Checks if agent was using a helmet
      (try_begin),
        (agent_get_item_slot, ":head_gear", ":inflicted_agent_id", ek_head),
        (ge, ":head_gear", 1),
        (assign, ":spawn_for_timer", 60),

        # helmet on the ground
        (copy_position, pos2, pos1),
        (position_move_x, pos2, 20, 0),
        (position_move_z, pos2, -30, 0),
        (store_random_in_range, ":rot_x", 10, 40),
        (store_random_in_range, ":rot_z", 15, 75),
        (position_rotate_x, pos2, ":rot_x", 1),
        (position_rotate_z, pos2, ":rot_z", 1),
        (position_set_z_to_ground_level, pos2),
        (position_move_y, pos2, -5, 1),
        (set_spawn_position, pos2),
        (spawn_item, ":head_gear", 0, ":spawn_for_timer"),

        (agent_unequip_item, ":inflicted_agent_id", ":head_gear"),
      (try_end),

      # equip invisible head on agent
      (agent_equip_item, ":inflicted_agent_id", "itm_untitled"),

      # blood
      (copy_position, pos2, pos0),
      (set_spawn_position, pos2),
      (particle_system_burst, "psys_game_blood", pos2, 5),

      # fake head
      (spawn_scene_prop, "spr_physics_head"),
      (assign, ":head_id", reg0),

      (prop_instance_enable_physics, ":head_id", 1),

      # makes sure the agent dies
      (agent_set_hit_points,":inflicted_agent_id", 0, 1),
      (try_end),
      ])
]
