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

cf_battlegroup_valid_formation_scripts = [
("cf_battlegroup_valid_formation", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fformation", 3),

      (assign, ":valid_type", 0),
      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (team_get_slot, ":sd_type", ":fteam", ":slot"),
      (try_begin), #Eventually make this more complex with the sub-divisions
        (this_or_next | eq, ":sd_type", sdt_cavalry),
        (eq, ":sd_type", sdt_harcher),
        (assign, ":size_minimum", formation_min_cavalry_troops),
        (try_begin),
          (eq, ":fformation", formation_wedge),
          (assign, ":valid_type", 1),
        (try_end),
      (else_try),
        (eq, ":sd_type", sdt_archer),
        (assign, ":size_minimum", formation_min_foot_troops),
        (try_begin),
          # (this_or_next|eq, ":fformation", formation_ranks), uncheck for proper
          # ranks
          (eq, ":fformation", formation_default),
          (assign, ":valid_type", 1),
        (try_end),
      (else_try),
        (assign, ":size_minimum", formation_min_foot_troops),
        (gt, ":fformation", formation_none),
        (assign, ":valid_type", 1), #all types valid
      (try_end),

      (try_begin),
        (eq, ":valid_type", 0),
        (assign, ":num_troops", 0),
      (else_try),
        (store_add, ":slot", slot_team_d0_size, ":fdivision"),
        (team_get_slot, ":num_troops", ":fteam", ":slot"),
        (lt, ":num_troops", ":size_minimum"),
        (assign, ":num_troops", 1),
      (try_end),

      (assign, reg0, ":num_troops"),
      (gt, ":num_troops", 1)])
]
