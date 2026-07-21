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

update_booksellers_scripts = [
("update_booksellers",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (neg|party_slot_ge, ":town_no", slot_center_is_besieged_by, 1), #keep them there
       (party_set_slot, ":town_no", slot_center_tavern_bookseller, 0),
     (try_end),

     (try_for_range, ":troop_no", tavern_booksellers_begin, tavern_booksellers_end),
       (troop_get_slot, ":cur_center", ":troop_no", slot_troop_cur_center),
       (neg|party_slot_ge, ":cur_center", slot_center_is_besieged_by, 1), #can't travel
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_bookseller, ":troop_no"),
       (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"), #SB : set troop slot
     (try_end),



     ])
]
