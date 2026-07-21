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

get_random_tournament_prize_scripts = [
# script_custom_battle_end
# Input: none
# Output: reg0 = troop_no
("get_random_tournament_prize",
    [(store_script_param, ":party_no", 1),
     (party_get_slot, ":cur_faction", ":party_no", slot_center_original_faction),
     (assign, ":cur_merchant", "trp_salt_mine_merchant"),

     (troop_clear_inventory, ":cur_merchant"),
     (store_random_in_range, ":r", 0, 4),

     (try_begin),
         (eq, ":r", 0),
         (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_body_armor, 8),
     (else_try),
         (eq, ":r", 1),
         (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_head_armor, 12),
     (else_try),
         (eq, ":r", 2),
          (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_one_handed_wpn, 5),
          (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_two_handed_wpn, 5),
          (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_polearm, 5),
          (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_shield, 6),
          (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_bow, 4),
          (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_crossbow, 3),
     (else_try),
         (eq, ":r", 3),
         (troop_add_merchandise_with_faction,":cur_merchant", ":cur_faction",itp_type_horse,5),
     (try_end),
     (troop_sort_inventory, ":cur_merchant"),
     (troop_get_inventory_capacity, ":inv_cap", ":cur_merchant"),
     (try_for_range, ":i_slot", ek_food + 2, ":inv_cap"),
        (troop_set_inventory_slot,":cur_merchant",":i_slot",-1),
     (try_end),

     ])
]
