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

team_get_average_position_of_enemies_scripts = [
("team_get_average_position_of_enemies",
    [
      (store_script_param_1, ":team_no"),
      (init_position, pos0),
      (assign, ":num_enemies", 0),
      (assign, ":accum_x", 0),
      (assign, ":accum_y", 0),
      (assign, ":accum_z", 0),
      (try_for_agents,":enemy_agent"),
        (agent_is_alive, ":enemy_agent"),
        (agent_is_human, ":enemy_agent"),
        (agent_get_team, ":enemy_team", ":enemy_agent"),
        (teams_are_enemies, ":team_no", ":enemy_team"),

        (agent_get_position, pos62, ":enemy_agent"),

        (position_get_x, ":x", pos62),
        (position_get_y, ":y", pos62),
        (position_get_z, ":z", pos62),

        (val_add, ":accum_x", ":x"),
        (val_add, ":accum_y", ":y"),
        (val_add, ":accum_z", ":z"),
        (val_add, ":num_enemies", 1),
      (try_end),

      (try_begin), #to avoid division by zeros at below division part.
        (le, ":num_enemies", 0),
        (assign, ":num_enemies", 1),
      (try_end),

      (store_div, ":average_x", ":accum_x", ":num_enemies"),
      (store_div, ":average_y", ":accum_y", ":num_enemies"),
      (store_div, ":average_z", ":accum_z", ":num_enemies"),

      (position_set_x, pos0, ":average_x"),
      (position_set_y, pos0, ":average_y"),
      (position_set_z, pos0, ":average_z"),

      (assign, reg0, ":num_enemies"),
  ])
]
