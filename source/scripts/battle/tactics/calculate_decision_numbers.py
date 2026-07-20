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

calculate_decision_numbers_scripts = [
("calculate_decision_numbers", [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_presence", 2),
      (try_begin),
        (team_get_slot, reg0, ":team_no", slot_team_level),
        (store_div, reg1, reg0, 3),
        (store_add, reg0, ":battle_presence", reg1),	#decision w.r.t.  all enemy teams
      (try_end)])
]
