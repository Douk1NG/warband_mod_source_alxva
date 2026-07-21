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

update_ransom_brokers_scripts = [
("update_ransom_brokers",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_ransom_broker, 0),
     (try_end),

     (try_for_range, ":troop_no", ransom_brokers_begin, ransom_brokers_end),
       #SB : random-brokers prefer towns with actual prisoners
       (assign, ":limit", 20),
       (try_for_range, ":unused", 0, ":limit"), #also exclude Tihr since it has Ramun
          (store_random_in_range, ":town_no", towns_begin, towns_end),
          (neq, ":town_no", "p_town_2"),
          (neq, ":town_no", "p_town_19"),
          #also exclude centers under siege
          (neg|party_slot_ge, ":town_no", slot_center_is_besieged_by, 1),
          (party_get_num_prisoners, ":prisoner_count", ":town_no"),
          (gt, ":prisoner_count", 0),
          (party_set_slot, ":town_no", slot_center_ransom_broker, ":troop_no"),
          (assign, ":limit", 0), #loop breaker
       (try_end),
       (eq, ":limit", 20), #none found
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_ransom_broker, ":troop_no"),
     (try_end),

     (party_set_slot,"p_town_2",slot_center_ransom_broker,"trp_ramun_the_slave_trader"),
     (party_set_slot,"p_town_19",slot_center_ransom_broker,"trp_galeas"),
     ])
]
