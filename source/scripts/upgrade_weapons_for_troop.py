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

upgrade_weapons_for_troop_scripts = [
("upgrade_weapons_for_troop",
    [
      (store_script_param, ":troop", 1),
      (try_for_range, ":ek_slot", ek_item_0, ek_item_3+1),
        (troop_slot_eq, "trp_temp_array_lock", ":ek_slot", 0),
        (troop_get_inventory_slot, ":troop_item", ":troop", ":ek_slot"),
        (gt, ":troop_item", -1),
        (item_get_type, ":dest_type", ":troop_item"),
        (assign, ":best_slot", ":ek_slot"),
        (assign, ":best_val", 0),
        (troop_get_inventory_slot_modifier, ":troop_imod", ":troop", ":ek_slot"),
        (call_script, "script_get_item_capability_with_imod", ":troop_item", ":troop_imod"),
        (assign, ":best_val", reg0),
        (call_script, "script_item_is_blunt_weapon", ":troop_item"),
        (assign, ":troop_item_is_blunt_weapon", reg0),
        (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
        (try_for_range, ":i_slot", 10, ":inv_cap"),
          (troop_slot_eq, "trp_temp_array_lock", ":i_slot", 0),
          (troop_get_inventory_slot, ":item", "trp_player", ":i_slot"),
          (gt, ":item", -1),
          (item_get_type, ":i_type", ":item"),
          (eq, ":i_type", ":dest_type"),
          (call_script, "script_cf_weapons_have_the_same_important_properties", ":troop_item", ":item"),
          (call_script, "script_item_is_blunt_weapon", ":item"),
          (assign, ":item_is_blunt_weapon", reg0),
          (eq, ":item_is_blunt_weapon", ":troop_item_is_blunt_weapon"),
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
        (troop_set_inventory_slot, "trp_player", ":best_slot", ":troop_item"),
        (troop_set_inventory_slot_modifier, "trp_player", ":best_slot", ":troop_imod"),
      (try_end),
    ])
]
