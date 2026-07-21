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

find_best_item_slot_of_type_scripts = [
("find_best_item_slot_of_type",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":item_type"),
      (assign, ":best_item_slot", -1),
      (assign, ":best_item_id", -1),
      (assign, ":max_value", -1),
      (assign, ":max_value_with_imod", -1),
      (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
      (try_for_range, ":i_slot", 10, ":inv_cap"),
        (troop_get_inventory_slot, ":item", ":troop_no", ":i_slot"),
        (gt, ":item", -1),
        (item_get_type, ":type", ":item"),
        (eq, ":type", ":item_type"),
        (store_item_value, ":item_value", ":item"),
        (troop_get_inventory_slot_modifier, ":imod", ":troop_no", ":i_slot"),
        (call_script, "script_get_item_value_with_imod", ":item", ":imod"),
        (assign, ":item_value_with_imod", reg0),
        (try_begin),
          (gt, ":item_value", ":max_value"),
          (assign, ":best_item_slot", ":i_slot"),
          (assign, ":best_item_id", ":item"),
          (assign, ":max_value", ":item_value"),
          (assign, ":max_value_with_imod", ":item_value_with_imod"),
        (else_try),
          (eq, ":item_value", ":max_value"),
          (lt, ":item", ":best_item_id"),
          (assign, ":best_item_slot", ":i_slot"),
          (assign, ":best_item_id", ":item"),
          (assign, ":max_value", ":item_value"),
          (assign, ":max_value_with_imod", ":item_value_with_imod"),
        (else_try),
          (eq, ":item", ":best_item_id"),
          (gt, ":item_value_with_imod", ":max_value_with_imod"),
          (assign, ":best_item_slot", ":i_slot"),
          (assign, ":max_value_with_imod", ":item_value_with_imod"),
        (try_end),
      (try_end),
      (assign, reg0, ":best_item_slot"),
    ])
]
