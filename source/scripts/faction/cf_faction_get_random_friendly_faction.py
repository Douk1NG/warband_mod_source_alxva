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

cf_faction_get_random_friendly_faction_scripts = [
# script_cf_faction_get_random_friendly_faction
# Input: arg1 = faction_no
# Output: reg0 = faction_no (Can fail)
("cf_faction_get_random_friendly_faction",
    [
      (store_script_param_1, ":faction_no"),

      (assign, ":result", -1),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (neq, ":cur_faction", ":faction_no"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (ge, ":cur_relation", 0),
        (val_add, ":count_factions", 1),
      (try_end),
      (store_random_in_range,":random_faction",0,":count_factions"),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (eq, ":result", -1),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (neq, ":cur_faction", ":faction_no"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (ge, ":cur_relation", 0),
        (val_add, ":count_factions", 1),
        (gt, ":count_factions", ":random_faction"),
        (assign, ":result", ":cur_faction"),
      (try_end),

      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ])
]
