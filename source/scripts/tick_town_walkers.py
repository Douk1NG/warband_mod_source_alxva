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

tick_town_walkers_scripts = [
# script_tick_town_walkers
# Input: none
# Output: none
("tick_town_walkers",
    [(try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (agent_get_slot, ":target_entry_point", ":cur_agent", 0),
       (entry_point_get_position, pos1, ":target_entry_point"),
       (try_begin),
         (lt, ":target_entry_point", 32),
         (init_position, pos2),
         (position_set_y, pos2, 250),
         (position_transform_position_to_parent, pos1, pos1, pos2),
       (try_end),
       (agent_get_position, pos2, ":cur_agent"),
       (get_distance_between_positions, ":distance", pos1, pos2),
       (lt, ":distance", 400),
       (assign, ":random_no", 0),
       (try_begin),
         (lt, ":target_entry_point", 32),
         (store_random_in_range, ":random_no", 0, 100),
       (try_end),
       (lt, ":random_no", 20),
       (call_script, "script_set_town_walker_destination", ":cur_agent"),
     (try_end),
  ])
]
