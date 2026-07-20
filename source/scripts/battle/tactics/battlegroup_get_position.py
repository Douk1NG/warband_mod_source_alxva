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

battlegroup_get_position_scripts = [
("battlegroup_get_position", [
      (store_script_param, ":bgposition", 1),
      (store_script_param, ":bgteam", 2),
      (store_script_param, ":bgdivision", 3),

      (assign, ":x", 0),
      (assign, ":y", 0),
      (init_position, ":bgposition"),
      (try_begin),
        (neg | is_between, ":bgdivision", 0, 9),
        (team_slot_ge, ":bgteam", slot_team_size, 1),
        (team_get_slot, ":x", ":bgteam", slot_team_avg_x),
        (team_get_slot, ":y", ":bgteam", slot_team_avg_y),
        (team_get_slot, ":zrot", ":bgteam", slot_team_avg_zrot),
      (else_try),
        (is_between, ":bgdivision", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":bgdivision"),
        (team_slot_ge, ":bgteam", ":slot", 1),

        (store_add, ":slot", slot_team_d0_avg_x, ":bgdivision"),
        (team_get_slot, ":x", ":bgteam", ":slot"),

        (store_add, ":slot", slot_team_d0_avg_y, ":bgdivision"),
        (team_get_slot, ":y", ":bgteam", ":slot"),

        (store_add, ":slot", slot_team_d0_avg_zrot, ":bgdivision"),
        (team_get_slot, ":zrot", ":bgteam", ":slot"),
      (try_end),
      (position_set_x, ":bgposition", ":x"),
      (position_set_y, ":bgposition", ":y"),
      (position_rotate_z, ":bgposition", ":zrot", 0),
      (position_set_z_to_ground_level, ":bgposition"),])
]
