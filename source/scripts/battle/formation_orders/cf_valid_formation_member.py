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

cf_valid_formation_member_scripts = [
("cf_valid_formation_member", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      (store_script_param, ":agent", 4),
      (neq, ":fleader", ":agent"),
      (agent_get_division, ":bgdivision", ":agent"),
      (eq, ":bgdivision", ":fdivision"),
      (agent_get_group, ":team", ":agent"),
      (eq, ":team", ":fteam"),
      (agent_is_alive, ":agent"),
      (agent_is_human, ":agent"),
      (agent_slot_eq, ":agent", slot_agent_is_running_away, 0),])
]
