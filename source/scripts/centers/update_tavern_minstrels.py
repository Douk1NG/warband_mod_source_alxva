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

update_tavern_minstrels_scripts = [
#script_update_booksellers
# INPUT: none
# OUTPUT: none
("update_tavern_minstrels",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_minstrel, 0),
     (try_end),

     #SB : remove restriction on travel, add preference for feasts
     (try_for_range, ":troop_no", tavern_minstrels_begin, tavern_minstrels_end),
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (store_faction_of_party, ":faction_no", ":town_no"),
       #feasts can be in castles, we haven't added code to put minstrels in
       (try_begin),
         (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
         (faction_get_slot, ":center_no", ":faction_no", slot_faction_ai_object),
         (is_between, ":center_no", towns_begin, towns_end),
         (neg|party_slot_ge, ":center_no", slot_center_tavern_minstrel, tavern_minstrels_begin),
         (assign, ":town_no", ":center_no"),
       (try_end),
       (party_set_slot, ":town_no", slot_center_tavern_minstrel, ":troop_no"),
       (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"), #SB : set troop slot
       (try_begin),
        (eq, "$cheat_mode", 1),
        (str_store_troop_name, s4, ":troop_no"),
        (str_store_party_name, s5, ":town_no"),

        (display_message, "str_s4_is_at_s5"),
       (try_end),
     (try_end),


     ])
]
