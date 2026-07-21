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

cf_village_normal_cond_scripts = [
#talking to people outside the court (neutral, tc_castle_gate)
# INPUT: none
# OUTPUT: none
("cf_village_normal_cond",
    [
    (store_script_param, ":party_no", 1),
    (neg|party_slot_eq, ":party_no", slot_village_state, svs_looted),
    (neg|party_slot_eq, ":party_no", slot_village_state, svs_deserted), #SB : addition here
    (neg|party_slot_eq, ":party_no", slot_village_state, svs_being_raided),
    (neg|party_slot_ge, ":party_no", slot_village_infested_by_bandits, 1),
    ]
  )
]
