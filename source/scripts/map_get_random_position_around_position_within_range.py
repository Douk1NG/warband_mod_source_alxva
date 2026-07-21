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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

map_get_random_position_around_position_within_range_scripts = [
("map_get_random_position_around_position_within_range",
    [
      (store_script_param_1, ":min_distance"),
      (store_script_param_2, ":max_distance"),
      (val_mul, ":min_distance", 100),
      (assign, ":continue", 1),
      (try_for_range, ":unused", 0, 20),
        (eq, ":continue", 1),
        (map_get_random_position_around_position, pos2, pos1, ":max_distance"),
        (get_distance_between_positions, ":distance", pos2, pos1),
        (ge, ":distance", ":min_distance"),
        (assign, ":continue", 0),
      (try_end),
  ])
]
