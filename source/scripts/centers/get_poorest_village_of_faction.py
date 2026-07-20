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

get_poorest_village_of_faction_scripts = [
# INPUT: arg1 = center_no
# OUTPUT: reg0 = ideal_prosperity
("get_poorest_village_of_faction",
    [(store_script_param, ":faction_no", 1),
     (assign, ":min_prosperity_village", -1),
     (assign, ":min_prosperity", 101),
     (try_for_range, ":village_no", villages_begin, villages_end),
       (store_faction_of_party, ":village_faction", ":village_no"),
       (eq, ":village_faction", ":faction_no"),
       (party_get_slot, ":prosperity", ":village_no", slot_town_prosperity),
       (lt, ":prosperity", ":min_prosperity"),
       (assign, ":min_prosperity", ":prosperity"),
       (assign, ":min_prosperity_village", ":village_no"),
     (try_end),
     (assign, reg0, ":min_prosperity_village"),
     ])
]
