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

get_nearest_enemy_battlegroup_location_scripts = [
("get_nearest_enemy_battlegroup_location", [
      (store_script_param, ":bgposition", 1),
      (store_script_param, ":team_no", 2),
      (store_script_param, ":from_pos", 3),
      (assign, ":distance_to_nearest_enemy_battlegoup", Far_Away),
      (try_for_range, ":enemy_team_no", 0, 4),
        (team_slot_ge, ":enemy_team_no", slot_team_size, 1),
        (teams_are_enemies, ":enemy_team_no", ":team_no"),
        (try_for_range, ":enemy_division", 0, 9),
          (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
          (team_slot_ge, ":enemy_team_no", ":slot", 1),
          (call_script, "script_battlegroup_get_position", pos0, ":enemy_team_no", ":enemy_division"),
          (get_distance_between_positions, reg0, pos0, ":from_pos"),
          (try_begin),
            (gt, ":distance_to_nearest_enemy_battlegoup", reg0),
            (assign, ":distance_to_nearest_enemy_battlegoup", reg0),
            (copy_position, ":bgposition", pos0),
          (try_end),
        (try_end),
      (try_end),
      (assign, reg0, ":distance_to_nearest_enemy_battlegoup")])
]
