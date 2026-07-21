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

get_center_faction_relation_including_player_scripts = [
#DEPRECATED - Using new political issue system instead
# Input: arg1: center_no, arg2: target_faction_no
# Output: reg0: relation
#called from triggers
("get_center_faction_relation_including_player",
   [
     (store_script_param, ":center_no", 1),
     (store_script_param, ":target_faction_no", 2),
     (store_faction_of_party, ":center_faction", ":center_no"),
     (store_relation, ":relation", ":center_faction", ":target_faction_no"),
     (try_begin),
       (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
       (store_relation, ":relation", "fac_player_supporters_faction", ":target_faction_no"),
     (try_end),
     (assign, reg0, ":relation"),
     ])
]
