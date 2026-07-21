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

update_npc_volunteer_troops_in_village_scripts = [
#script_update_npc_volunteer_troops_in_village
# INPUT: arg1 = center_no
# OUTPUT: none
("update_npc_volunteer_troops_in_village",
    [
       (store_script_param, ":center_no", 1),
       (party_get_slot, ":center_culture", ":center_no", slot_center_culture),
       (faction_get_slot, ":volunteer_troop", ":center_culture", slot_faction_tier_1_troop),
       (assign, ":volunteer_troop_tier", 1),
       (try_for_range, ":unused", 0, 5),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 10),
         (store_random_in_range, ":random_no", 0, 2),
         (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", ":random_no"),
         (try_begin),
           (le, ":upgrade_troop_no", 0),
           (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", 0),
         (try_end),
         (gt, ":upgrade_troop_no", 0),
         (val_add, ":volunteer_troop_tier", 1),
         (assign, ":volunteer_troop", ":upgrade_troop_no"),
       (try_end),

       (assign, ":upper_limit", 12),

       (store_add, ":amount_random_divider", 2, ":volunteer_troop_tier"),
       (val_div, ":upper_limit", ":amount_random_divider"),

       (store_random_in_range, ":amount", 0, ":upper_limit"),
       (party_set_slot, ":center_no", slot_center_npc_volunteer_troop_type, ":volunteer_troop"),
       (party_set_slot, ":center_no", slot_center_npc_volunteer_troop_amount, ":amount"),
     ])
]
