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



  # Setting item modifiers for food
  

item_modifiers_for_food_simple_triggers = [
(24,
   [
     (troop_get_inventory_capacity, ":inv_size", "trp_player"),
     #SB : add chance to prevent spoilage
     (store_skill_level, ":management", "skl_inventory_management", "trp_player"),
     (val_mul, ":management", 4),
     (val_div, ":management", 5),
     (try_for_range, ":i_slot", 10, ":inv_size"),
       (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
       (this_or_next|eq, ":item_id", "itm_cattle_meat"),
       (this_or_next|eq, ":item_id", "itm_chicken"),
       (eq, ":item_id", "itm_pork"),

       (troop_get_inventory_slot_modifier, ":modifier", "trp_player", ":i_slot"),
       (try_begin),
         (is_between, ":modifier", imod_fresh, imod_rotten),
         (val_add, ":modifier", 1),
         (try_begin), # SB : spoilage, objection
           (eq, ":modifier", imod_rotten),
           (troop_inventory_slot_get_item_amount, ":amount", "trp_player", ":i_slot"),
           (troop_inventory_slot_get_item_max_amount, ":max", "trp_player", ":i_slot"),
           (store_sub, ":amount", ":max", ":amount"), #get amount consumed already
           (val_mul, ":amount", 100),
           (val_div, ":amount", ":max"),
           (store_random_in_range, ":max", 0, ":amount"),
           (try_begin),
             (lt, ":max", ":management"), # saving throw
             (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
             (assign, ":modifier", imod_smelling),
           #(else_try), # spoiled critic
             #(call_script, "script_objectionable_action", tmt_aristocratic, "str_rotten_food"), dckplmc: this doesn't make any sense
           (try_end),
         (try_end),
         (troop_set_inventory_slot_modifier, "trp_player", ":i_slot", ":modifier"),
       (else_try),
         (lt, ":modifier", imod_fresh),
         (troop_set_inventory_slot_modifier, "trp_player", ":i_slot", imod_fresh),
       (try_end),
     (try_end),
    ]),
]
