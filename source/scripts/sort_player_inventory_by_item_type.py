# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

sort_player_inventory_by_item_type_scripts = [
("sort_player_inventory_by_item_type",
    [
      (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
      (troop_clear_inventory, "trp_temp_array_sort"),
      (try_for_range, ":slot_no", 10, ":inv_cap"),
        (troop_slot_eq, "trp_temp_array_lock", ":slot_no", 0),
        (troop_get_inventory_slot, ":item", "trp_player", ":slot_no"),
        (gt, ":item", -1),
        (troop_set_inventory_slot, "trp_temp_array_sort", ":slot_no", ":item"),
        (troop_get_inventory_slot_modifier, ":item_mod", "trp_player", ":slot_no"),
        (troop_set_inventory_slot_modifier, "trp_temp_array_sort", ":slot_no", ":item_mod"),
        (troop_inventory_slot_get_item_amount, ":item_amount", "trp_player", ":slot_no"),
        (try_begin),
          (gt, ":item_amount", 0),
          (troop_inventory_slot_set_item_amount, "trp_temp_array_sort", ":slot_no", ":item_amount"),
        (try_end),
        (troop_set_inventory_slot, "trp_player", ":slot_no", -1),
      (try_end),
      (call_script, "script_sort_food", "trp_temp_array_sort"),
      (assign, ":cur_item_slot", 10),
      (call_script, "script_new_order_of_item_types"),
      (try_for_range, ":slot_no", 0, 20),
        (troop_get_slot, ":item_type", "trp_temp_array_sort", ":slot_no"),
        (call_script, "script_get_num_of_item_by_type", "trp_temp_array_sort", ":item_type"),
        (assign, ":num_of_item", reg0),
        (gt, ":num_of_item", 0),
        (try_for_range, ":unused", 0, ":num_of_item"),
          (call_script, "script_find_best_item_slot_of_type", "trp_temp_array_sort", ":item_type"),
          (assign, ":best_item_slot", reg0),
          (gt, ":best_item_slot", -1),
          (troop_get_inventory_slot, ":item", "trp_temp_array_sort", ":best_item_slot"),
          (troop_get_inventory_slot_modifier, ":imod", "trp_temp_array_sort", ":best_item_slot"),
          (troop_inventory_slot_get_item_amount, ":amount", "trp_temp_array_sort", ":best_item_slot"),
          (troop_set_inventory_slot, "trp_temp_array_sort", ":best_item_slot", -1),
          (assign, ":upper_bound", ":inv_cap"),
          (assign, ":lower_bound", ":cur_item_slot"),
          (try_for_range, ":cur_slot_no", ":lower_bound", ":upper_bound"),
            (troop_slot_eq, "trp_temp_array_lock", ":cur_slot_no", 0),
            (troop_set_inventory_slot, "trp_player", ":cur_slot_no", ":item"),
            (troop_set_inventory_slot_modifier, "trp_player", ":cur_slot_no", ":imod"),
            (try_begin),
              (gt, ":amount", 0),
              (troop_inventory_slot_set_item_amount, "trp_player", ":cur_slot_no", ":amount"),
            (try_end),
            (assign, ":cur_item_slot", ":cur_slot_no"),
            (val_add, ":cur_item_slot", 1),
            (assign, ":upper_bound", 0),
          (try_end),
        (try_end),
      (try_end),
    ])
]
