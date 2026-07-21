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

update_faction_traveler_notes_scripts = [
#script_update_faction_traveler_notes
# INPUT: faction_no
# OUTPUT: none
("update_faction_traveler_notes",
    [(store_script_param, ":faction_no", 1),
     (assign, ":total_men", 0),
     (try_for_parties, ":cur_party"),
       (store_faction_of_party, ":center_faction", ":cur_party"),
       (eq, ":center_faction", ":faction_no"),
       (party_get_num_companions, ":num_men", ":cur_party"),
       (val_add, ":total_men", ":num_men"),
     (try_end),
     (str_store_faction_name, s5, ":faction_no"),
     (assign, reg1, ":total_men"),
     (add_faction_note_from_sreg, ":faction_no", 1, "@{s5} has a strength of {reg1} men in total.", 1),
     ])
]
