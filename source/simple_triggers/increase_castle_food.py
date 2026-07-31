# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *



 #Increase castle food stores
  

increase_castle_food_simple_triggers = [
(2,
   [
   ##diplomacy start+ Change to vary with village prosperity
   (try_begin),
       (lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
       ##OLD:
       #unaltered block begin
       (try_for_range, ":center_no", castles_begin, castles_end),
         (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #castle is not under siege
         (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
         (val_add, ":center_food_store", 100),
         (call_script, "script_center_get_food_store_limit", ":center_no"),
         (assign, ":food_store_limit", reg0),
         (val_min, ":center_food_store", ":food_store_limit"),
         (party_set_slot, ":center_no", slot_party_food_store, ":center_food_store"),
       (try_end),
       #unaltered block end
   (else_try),
       ##NEW:
       (try_for_range, ":village_no", villages_begin, villages_end),
          (neg|party_slot_ge, ":village_no", slot_center_is_besieged_by, 0),
          (party_slot_eq, ":village_no", slot_village_state, svs_normal),
          (party_get_slot, ":center_no", ":village_no", slot_village_bound_center),
          (is_between, ":center_no", castles_begin, castles_end),
          (neg|party_slot_ge, ":center_no", slot_center_is_besieged_by, 0),
          (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
          (party_get_slot, reg0, ":village_no", slot_town_prosperity),
          (val_add, reg0, 75),
          (val_mul, reg0, 100),#base addition is 100
          (val_add, reg0, 62),
          (val_div, reg0, 125),#plus or minus 40%
          (val_add, ":center_food_store", reg0),
          (call_script, "script_center_get_food_store_limit", ":center_no"),
          (assign, ":food_store_limit", reg0),
          (val_min, ":center_food_store", ":food_store_limit"),
          (party_set_slot, ":center_no", slot_party_food_store, ":center_food_store"),
       (try_end),
   (try_end),
   ]),
]
