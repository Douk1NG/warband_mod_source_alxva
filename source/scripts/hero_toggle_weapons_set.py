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
from module_items import items

hero_toggle_weapons_set_scripts = [
("hero_toggle_weapons_set",
    [
      (store_script_param, ":cur_hero", 1),
      
      (try_for_range, ":cur_2nd_weapon_slot", slot_2nd_weapons_1, slot_2nd_weapons_4+1),
        (troop_get_slot, ":cur_2nd_slot_value", ":cur_hero", ":cur_2nd_weapon_slot"),
        (try_begin),
          (le, ":cur_2nd_slot_value", 0),
          (assign, ":cur_weapon_modifier_2", 0),
          (assign, ":cur_weapon_2", -1),
        (else_try),
          (store_mod, ":cur_weapon_modifier_2", ":cur_2nd_slot_value", 100),
          (store_div, ":cur_weapon_2", ":cur_2nd_slot_value", 100),
        (try_end),
        (store_sub, ":cur_weapon_slot", ":cur_2nd_weapon_slot", slot_2nd_weapons_1),
        (val_add, ":cur_weapon_slot", ek_item_0),
        (troop_get_inventory_slot, ":cur_weapon", ":cur_hero", ":cur_weapon_slot"),
        (troop_get_inventory_slot_modifier, ":cur_weapon_modifier", ":cur_hero", ":cur_weapon_slot"),
        (troop_set_inventory_slot, ":cur_hero", ":cur_weapon_slot", ":cur_weapon_2"),
        (troop_set_inventory_slot_modifier, ":cur_hero", ":cur_weapon_slot", ":cur_weapon_modifier_2"),
        (store_mul, ":new_2nd_slot_value", ":cur_weapon", 100),
        (val_add, ":new_2nd_slot_value", ":cur_weapon_modifier"),
        (troop_set_slot, ":cur_hero", ":cur_2nd_weapon_slot", ":new_2nd_slot_value"),
      (try_end),

      (troop_get_slot, ":troop_weapons_set_no", ":cur_hero", slot_troop_weapons_set_no),
      (val_add, ":troop_weapons_set_no", 1),
      (val_mod, ":troop_weapons_set_no", 2),
      (troop_set_slot, ":cur_hero", slot_troop_weapons_set_no, ":troop_weapons_set_no"),
    ])
]
