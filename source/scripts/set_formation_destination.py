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

set_formation_destination_scripts = [
("set_formation_destination", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fposition", 3),

      (position_get_x, ":x", ":fposition"),
      (position_get_y, ":y", ":fposition"),
      (position_get_rotation_around_z, ":zrot", ":fposition"),

      (store_add, ":slot", slot_team_d0_destination_x, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":x"),
      (store_add, ":slot", slot_team_d0_destination_y, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":y"),
      (store_add, ":slot", slot_team_d0_destination_zrot, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":zrot"),

      (team_set_order_position, ":fteam", ":fdivision", ":fposition"),])
]
