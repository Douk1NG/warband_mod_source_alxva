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

sort_food_scripts = [
("sort_food",
    [
      (store_script_param, ":troop_no", 1),
      (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
      (try_for_range_backwards, ":i_slot", 10, ":inv_cap"),
        (troop_get_inventory_slot, ":item", ":troop_no", ":i_slot"),
        (troop_get_inventory_slot_modifier, ":imod", ":troop_no", ":i_slot"),
        (gt, ":item", -1),
        (is_between, ":item", food_begin, food_end),
        (try_for_range_backwards, ":i_slot_2", 10, ":i_slot"),
          (troop_get_inventory_slot, ":item_2", ":troop_no", ":i_slot_2"),
          (troop_get_inventory_slot_modifier, ":imod_2", ":troop_no", ":i_slot_2"),
          (gt, ":item_2", -1),
          (eq, ":item_2", ":item"),
          (eq, ":imod_2", ":imod"),
          (troop_inventory_slot_get_item_max_amount, ":max_amount", ":troop_no", ":i_slot"),
          (troop_inventory_slot_get_item_amount, ":item_amount", ":troop_no", ":i_slot"),
          (troop_inventory_slot_get_item_amount, ":item_amount_2", ":troop_no", ":i_slot_2"),
          (store_add, ":total_amount", ":item_amount", ":item_amount_2"),
          (store_sub, ":dest_amount_i_slot_2", ":total_amount", ":max_amount"),
          (try_begin),
            (gt, ":dest_amount_i_slot_2", 0),
            (troop_inventory_slot_set_item_amount, ":troop_no", ":i_slot", ":max_amount"),
            (troop_inventory_slot_set_item_amount, ":troop_no", ":i_slot_2", ":dest_amount_i_slot_2"),
            (assign, ":i_slot_2", 0),
          (else_try),
            (troop_inventory_slot_set_item_amount, ":troop_no", ":i_slot", ":total_amount"),
            (troop_set_inventory_slot, ":troop_no", ":i_slot_2", -1),
          (try_end),
        (try_end),
      (try_end),
    ])
]
