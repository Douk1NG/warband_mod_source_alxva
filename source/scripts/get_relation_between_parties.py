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

get_relation_between_parties_scripts = [
#script_get_chest_troop fetches the appropriate placeholder for player storage
("get_relation_between_parties",
    [
      (store_script_param_1, ":party_no_1"),
      (store_script_param_2, ":party_no_2"),

      (store_faction_of_party, ":party_no_1_faction", ":party_no_1"),
      (store_faction_of_party, ":party_no_2_faction", ":party_no_2"),
      (try_begin),
        (eq, ":party_no_1_faction", ":party_no_2_faction"),
        (assign, reg0, 100),
      (else_try),
        (store_relation, ":relation", ":party_no_1_faction", ":party_no_2_faction"),
        (assign, reg0, ":relation"),
      (try_end),
  ])
]
