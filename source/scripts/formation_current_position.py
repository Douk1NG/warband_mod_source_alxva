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

formation_current_position_scripts = [
("formation_current_position", [
      (store_script_param, ":fposition", 1),
      (store_script_param, ":fteam", 2),
      (store_script_param, ":fdivision", 3),
      (call_script, "script_battlegroup_get_position", ":fposition", ":fteam", ":fdivision"),
      (call_script, "script_get_formation_destination", pos0, ":fteam", ":fdivision"),
      (position_copy_rotation, ":fposition", pos0),
      (call_script, "script_battlegroup_dist_center_to_front", ":fteam", ":fdivision"),
      (position_move_y, ":fposition", reg0, 0),])
]
