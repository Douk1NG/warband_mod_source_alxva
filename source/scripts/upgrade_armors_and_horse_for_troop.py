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

upgrade_armors_and_horse_for_troop_scripts = [
("upgrade_armors_and_horse_for_troop",
    [
      (store_script_param, ":troop", 1),
      (try_for_range, ":ek_slot", ek_head, ek_horse+1),
        (troop_slot_eq, "trp_temp_array_lock", ":ek_slot", 0),
        (try_begin),
          (is_between, ":ek_slot", ek_head, ek_horse),
          (store_sub, ":dest_type", ":ek_slot", ek_head),
          (val_add, ":dest_type", itp_type_head_armor),
        (else_try),
          (eq, ":ek_slot", ek_horse),
          (assign, ":dest_type", itp_type_horse),
        (try_end),
        (assign, ":best_slot", ":ek_slot"),
        (assign, ":best_val", 0),
        (troop_get_inventory_slot, ":troop_item", ":troop", ":ek_slot"),
        (try_begin),
          (gt, ":troop_item", -1),
          (troop_get_inventory_slot_modifier, ":troop_imod", ":troop", ":ek_slot"),
          (call_script, "script_get_item_capability_with_imod", ":troop_item", ":troop_imod"),
          (assign, ":best_val", reg0),
        (try_end),
        (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
        (try_for_range, ":i_slot", 10, ":inv_cap"),
          (troop_slot_eq, "trp_temp_array_lock", ":i_slot", 0),
          (troop_get_inventory_slot, ":item", "trp_player", ":i_slot"),
          (gt, ":item", -1),
          (item_get_type, ":i_type", ":item"),
          (eq, ":i_type", ":dest_type"),
          (troop_get_inventory_slot_modifier, ":imod", "trp_player", ":i_slot"),
          (call_script, "script_troop_can_use_item", ":troop", ":item", ":imod"),
          (eq, reg0, 1),
          (call_script, "script_get_item_capability_with_imod", ":item", ":imod"),
          (assign, ":item_capability", reg0),
          (gt, ":item_capability", ":best_val"),
          (assign, ":best_slot", ":i_slot"),
          (assign, ":best_val", ":item_capability"),
        (try_end),
        (ge, ":best_slot", 10),
        (troop_get_inventory_slot, ":best_item", "trp_player", ":best_slot"),
        (troop_get_inventory_slot_modifier, ":best_imod", "trp_player", ":best_slot"),
        (troop_set_inventory_slot, ":troop", ":ek_slot", ":best_item"),
        (troop_set_inventory_slot_modifier, ":troop", ":ek_slot", ":best_imod"),
        (try_begin),
          (gt, ":troop_item", -1),
          (troop_set_inventory_slot, "trp_player", ":best_slot", ":troop_item"),
          (troop_set_inventory_slot_modifier, "trp_player", ":best_slot", ":troop_imod"),
        (else_try),
          (troop_set_inventory_slot, "trp_player", ":best_slot", -1),
        (try_end),
      (try_end),
    ])
]
