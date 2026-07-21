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

battlegroup_place_around_leader_scripts = [
("battlegroup_place_around_leader", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),

      (try_begin),
        (le, ":fleader", 0),
        (display_message, "@{!}script_battlegroup_place_around_leader: invalid leader agent (bad call)"),

      (else_try),
        (agent_get_group, reg0, ":fleader"),
        (neq, reg0, ":fteam"),
        (display_message, "@{!}script_battlegroup_place_around_leader: leader team mismatch (bad call)"),

      (else_try),
        (agent_get_position, pos1, ":fleader"),
        (call_script, "script_battlegroup_place_around_pos1", ":fteam", ":fdivision", ":fleader"),
      (try_end),])
]
