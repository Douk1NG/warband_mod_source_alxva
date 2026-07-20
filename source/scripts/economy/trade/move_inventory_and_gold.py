# ======================================================================
# SHARED DEPENDENCY
# Entity: move_inventory_and_gold (script)
# Called by menus in 2 domains: castle, diplomacy
# ======================================================================

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

move_inventory_and_gold_scripts = [
##"script_dplmc_print_cultural_word_to_sreg"
# generally this is used to move the backup to the player
# Input: arg1 = source, arg2 = destnation
# Output: none
("move_inventory_and_gold",
    [
      (store_script_param, ":source", 1),
      (store_script_param, ":destination", 2),
      (store_script_param, ":move_gold", 3),
      #assume trp_temp_troop is an available placeholder

      (troop_sort_inventory, ":source"), #order them, too lazy to maintain 2 loops
      (troop_get_inventory_capacity, ":inv_cap", ":source"),
      (troop_get_inventory_capacity, ":player_cap", ":destination"),
      (assign, ":inv_slot", ek_food + 1), #start from the bottom, skip source's equipment
      (try_for_range, ":i_slot", ek_food + 1, ":player_cap"),
        (troop_get_inventory_slot, ":cur_item", ":destination", ":i_slot"),
        (eq, ":cur_item", -1), #empty slot
        (troop_get_inventory_slot, ":item", ":source", ":inv_slot"),
        (troop_set_inventory_slot, ":destination", ":i_slot", ":item"),
        #(try_begin),
          #(neq, ":cur_item", -1), #?????
          (troop_get_inventory_slot_modifier, ":imod", ":source", ":inv_slot"),
          (troop_set_inventory_slot_modifier, ":destination", ":i_slot", ":imod"),
          (try_begin),
            (troop_inventory_slot_get_item_amount, ":amount", ":source", ":inv_slot"),
            (gt, ":amount", 0),
            (troop_inventory_slot_set_item_amount, ":destination", ":i_slot", ":amount"),
          (try_end),
        #(try_end),
        (troop_set_inventory_slot, ":source", ":inv_slot", -1),
        (val_add, ":inv_slot", 1),

        (try_begin), #loop break
          (ge, ":inv_slot", ":inv_cap"),
          (assign, ":player_cap", -1),
        (try_end),
      (try_end),
      (troop_clear_inventory, ":source"), #clear off the rest if no capacity in destination
      #do gold addition
      (try_begin),
        (eq, ":move_gold", -1), #move all
        (store_troop_gold, ":cur_amount", ":source"),
        (troop_remove_gold, ":source", ":cur_amount"),
        (troop_add_gold, ":destination", ":cur_amount"),
      (else_try),
        (gt, ":move_gold", 0),  #specific amount
        (call_script, "script_troop_transfer_gold", ":source", ":destination", ":move_gold"),
      (try_end),
    ])
]
