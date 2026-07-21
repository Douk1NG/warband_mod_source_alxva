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

set_attached_scene_prop_scripts = [
("set_attached_scene_prop",
   [
     (store_script_param, ":agent_id", 1),
     (store_script_param, ":flag_id", 2),

     (try_begin), #if current mod is capture the flag and attached scene prop is flag then change flag situation of flag owner team.
       (scene_prop_get_instance, ":red_flag_id", "spr_tutorial_flag_red", 0),
       (scene_prop_get_instance, ":blue_flag_id", "spr_tutorial_flag_blue", 0),
       (assign, ":flag_owner_team", -1),
       (try_begin),
         (ge, ":red_flag_id", 0),
         (eq, ":flag_id", ":red_flag_id"),
         (assign, ":flag_owner_team", 0),
       (else_try),
         (ge, ":blue_flag_id", 0),
         (eq, ":flag_id", ":blue_flag_id"),
         (assign, ":flag_owner_team", 1),
       (try_end),
       (ge, ":flag_owner_team", 0),
       (team_set_slot, ":flag_owner_team", slot_team_flag_situation, 1), #1-stolen flag
     (try_end),

     (agent_set_attached_scene_prop, ":agent_id", ":flag_id"),
     (agent_set_attached_scene_prop_x, ":agent_id", 20),
     (agent_set_attached_scene_prop_z, ":agent_id", 50),
   ])
]
