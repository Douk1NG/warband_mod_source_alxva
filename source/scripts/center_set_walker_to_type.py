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

center_set_walker_to_type_scripts = [
# script_center_set_walker_to_type
# Input: arg1 = center_no, arg2 = walker_no, arg3 = walker_type,
# Output: none
("center_set_walker_to_type",
   [
       (store_script_param, ":center_no", 1),
       (store_script_param, ":walker_no", 2),
       (store_script_param, ":walker_type", 3),
       (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
       (party_set_slot, ":center_no", ":type_slot", ":walker_type"),
       (party_get_slot, ":center_faction", ":center_no", slot_center_original_faction),
       (faction_get_slot, ":center_culture", ":center_faction", slot_faction_culture),
       (store_random_in_range, ":walker_troop_slot", 0, 2),
       (try_begin),
         (party_slot_eq, ":center_no", slot_party_type, spt_village),
         (val_add, ":walker_troop_slot", slot_faction_village_walker_male_troop),
       (else_try),
         (val_add, ":walker_troop_slot", slot_faction_town_walker_male_troop),
       (try_end),
       (try_begin),
         (eq,":walker_type", walkert_spy),
         (assign,":original_walker_slot",":walker_troop_slot"),
         (val_add,":walker_troop_slot",4), # select spy troop id slot
       (try_end),
       (faction_get_slot, ":walker_troop_id", ":center_culture", ":walker_troop_slot"),
       (try_begin),
         (eq,":walker_type", walkert_spy),
         (faction_get_slot, ":original_walker", ":center_culture", ":original_walker_slot"),
         # restore spy inventory
         (try_for_range,":item_no","itm_horse_meat","itm_wooden_stick"),
            (store_item_kind_count,":num_items",":item_no",":original_walker"),
            (ge,":num_items",1),
            (store_item_kind_count,":num_items",":item_no",":walker_troop_id"),
            (lt,":num_items",1),
            (troop_add_items,":walker_troop_id",":item_no",1),
         (try_end),
         # determine spy recognition item
         (store_random_in_range,":spy_item_type",itp_type_head_armor,itp_type_hand_armor),
         (assign,":num",0),
         (try_for_range,":item_no","itm_horse_meat","itm_wooden_stick"),
            (store_item_kind_count,":num_items",":item_no",":walker_troop_id"),
            (ge,":num_items",1),
            (item_get_type, ":itp", ":item_no"),
            (eq,":itp",":spy_item_type"),
            (val_add,":num",1),
            (troop_remove_items,":walker_troop_id",":item_no",":num_items"),
         (try_end),
         (store_random_in_range,":random_item",0,":num"),
         (assign,":num",-1),
         (try_for_range,":item_no","itm_horse_meat","itm_wooden_stick"),
            (store_item_kind_count,":num_items",":item_no",":original_walker"),
            (ge,":num_items",1),
            (item_get_type, ":itp", ":item_no"),
            (eq,":itp",":spy_item_type"),
            (val_add,":num",1),
            (eq,":num",":random_item"),
            (troop_add_items,":walker_troop_id",":item_no",1),
            (assign,":spy_item",":item_no"),
         (try_end),
         (assign,"$spy_item_worn",":spy_item"),
         (assign,"$spy_quest_troop",":walker_troop_id"),
         (troop_equip_items,":walker_troop_id"),
       (try_end),
       (store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
       (party_set_slot, ":center_no", ":troop_slot", ":walker_troop_id"),
       (store_random_in_range, ":walker_dna", 0, 1000000),
       (store_add, ":dna_slot", slot_center_walker_0_dna, ":walker_no"),
       (party_set_slot, ":center_no", ":dna_slot", ":walker_dna"),
     ])
]
