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

get_heroes_attached_to_center_as_prisoner_scripts = [
# script_get_heroes_attached_to_center_as_prisoner
# Input: arg1 = center_no, arg2 = party_no_to_collect_heroes
# Output: none, adds heroes to the party_no_to_collect_heroes party
("get_heroes_attached_to_center_as_prisoner",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_clear, ":party_no_to_collect_heroes"),
      (call_script, "script_get_heroes_attached_to_center_as_prisoner_aux", ":center_no", ":party_no_to_collect_heroes"),
  ])
]
