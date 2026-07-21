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

village_recruit_volunteers_recruit_scripts = [
#script_village_recruit_volunteers_recruit
# INPUT: none
# OUTPUT: none
("village_recruit_volunteers_recruit",
    [(party_get_slot, ":volunteer_troop", "$current_town", slot_center_volunteer_troop_type),
     (party_get_slot, ":volunteer_amount", "$current_town", slot_center_volunteer_troop_amount),
     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
     (val_min, ":volunteer_amount", ":free_capacity"),
     (store_troop_gold, ":gold", "trp_player"),
     (store_div, ":gold_capacity", ":gold", 10),#10 denars per man
     (val_min, ":volunteer_amount", ":gold_capacity"),
     (party_add_members, "p_main_party", ":volunteer_troop", ":volunteer_amount"),
     (party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1),
     (store_mul, ":cost", ":volunteer_amount", 10),#10 denars per man
     (troop_remove_gold, "trp_player", ":cost"),
     ])
]
