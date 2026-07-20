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

set_town_walker_destination_scripts = [
# script_set_town_walker_destination
# Input: arg1 = agent_no
# Output: none
("set_town_walker_destination",
    [(store_script_param_1, ":agent_no"),
     (assign, reg0, 9),
     (assign, reg1, 10),
     (assign, reg2, 12),
     (assign, reg3, 32),
     (assign, reg4, 33),
     (assign, reg5, 34),
     (assign, reg6, 35),
     (assign, reg7, 36),
     (assign, reg8, 37),
     (assign, reg9, 38),
     (assign, reg10, 39),
     (try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (agent_get_slot, ":target_entry_point", ":cur_agent", 0),
       (try_begin),
         (eq, ":target_entry_point", 9),
         (assign, reg0, 0),
       (else_try),
         (eq, ":target_entry_point", 10),
         (assign, reg1, 0),
       (else_try),
         (eq, ":target_entry_point", 12),
         (assign, reg2, 0),
       (else_try),
         (eq, ":target_entry_point", 32),
         (assign, reg3, 0),
       (else_try),
         (eq, ":target_entry_point", 33),
         (assign, reg4, 0),
       (else_try),
         (eq, ":target_entry_point", 34),
         (assign, reg5, 0),
       (else_try),
         (eq, ":target_entry_point", 35),
         (assign, reg6, 0),
       (else_try),
         (eq, ":target_entry_point", 36),
         (assign, reg7, 0),
       (else_try),
         (eq, ":target_entry_point", 37),
         (assign, reg8, 0),
       (else_try),
         (eq, ":target_entry_point", 38),
         (assign, reg9, 0),
       (else_try),
         (eq, ":target_entry_point", 39),
         (assign, reg10, 0),
       (try_end),
     (try_end),
     (assign, ":try_limit", 100),
     (assign, ":target_entry_point", 0),
     (try_for_range, ":unused", 0, ":try_limit"),
       (shuffle_range, 0, 11),
       (gt, reg0, 0),
       (assign, ":target_entry_point", reg0),
       (assign, ":try_limit", 0),
     (try_end),
     (try_begin),
       (gt, ":target_entry_point", 0),
       (agent_set_slot, ":agent_no", 0, ":target_entry_point"),
       (entry_point_get_position, pos1, ":target_entry_point"),
       (try_begin),
         (lt, ":target_entry_point", 32),
         (init_position, pos2),
         (position_set_y, pos2, 250),
         (position_transform_position_to_parent, pos1, pos1, pos2),
       (try_end),
       (agent_set_scripted_destination, ":agent_no", pos1, 0),
       (agent_set_speed_limit, ":agent_no", 5),
     (try_end),
  ])
]
