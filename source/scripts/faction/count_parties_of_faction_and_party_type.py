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

count_parties_of_faction_and_party_type_scripts = [
# counts number of active parties with a template and faction.
# Input: arg1 = faction_no, arg2 = party_type
# Output: reg0 = count
("count_parties_of_faction_and_party_type",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":party_type"),
      (assign, reg0, 0),
      (try_for_parties, ":party_no"),
        (party_is_active, ":party_no"),
        (party_get_slot, ":cur_party_type", ":party_no", slot_party_type),
        (store_faction_of_party, ":cur_faction", ":party_no"),
        (eq, ":cur_party_type", ":party_type"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, reg0, 1),
      (try_end),
  ])
]
