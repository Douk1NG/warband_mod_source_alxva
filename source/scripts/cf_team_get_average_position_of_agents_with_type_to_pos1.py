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

cf_team_get_average_position_of_agents_with_type_to_pos1_scripts = [
("cf_team_get_average_position_of_agents_with_type_to_pos1",
    [
      (store_script_param_1, ":team_no"),
      (store_script_param_2, ":division_no"),
      (assign, ":total_pos_x", 0),
      (assign, ":total_pos_y", 0),
      (assign, ":total_pos_z", 0),
      (assign, ":num_agents", 0),
      (set_fixed_point_multiplier, 100),
      (try_for_agents, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":cur_team_no", ":cur_agent"),
        (eq, ":cur_team_no", ":team_no"),
        (agent_get_division, ":cur_agent_division", ":cur_agent"),
        (this_or_next|eq, ":division_no", grc_everyone),
        (eq, ":division_no", ":cur_agent_division"),
        (agent_get_position, pos1, ":cur_agent"),
        (position_get_x, ":cur_pos_x", pos1),
        (val_add, ":total_pos_x", ":cur_pos_x"),
        (position_get_y, ":cur_pos_y", pos1),
        (val_add, ":total_pos_y", ":cur_pos_y"),
        (position_get_z, ":cur_pos_z", pos1),
        (val_add, ":total_pos_z", ":cur_pos_z"),
        (val_add, ":num_agents", 1),
      (try_end),
      (gt, ":num_agents", 1),
      (val_div, ":total_pos_x", ":num_agents"),
      (val_div, ":total_pos_y", ":num_agents"),
      (val_div, ":total_pos_z", ":num_agents"),
      (init_position, pos1),
      (position_move_x, pos1, ":total_pos_x"),
      (position_move_y, pos1, ":total_pos_y"),
      (position_move_z, pos1, ":total_pos_z"),
  ])
]
