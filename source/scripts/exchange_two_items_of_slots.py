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

exchange_two_items_of_slots_scripts = [
("exchange_two_items_of_slots",
    [
      (store_script_param, ":old_slot", 1),
      (store_script_param, ":new_slot", 2),
      (store_script_param, ":selected_troop", 3),

      (try_begin),
        (ge, ":old_slot", 10),
        (troop_get_inventory_slot, ":old_item", "trp_player", ":old_slot"),
        (troop_get_inventory_slot_modifier, ":old_imod", "trp_player", ":old_slot"),
        (troop_inventory_slot_get_item_amount, ":old_amount", "trp_player", ":old_slot"),
      (else_try),
        (troop_get_inventory_slot, ":old_item", ":selected_troop", ":old_slot"),
        (troop_get_inventory_slot_modifier, ":old_imod", ":selected_troop", ":old_slot"),
        (troop_inventory_slot_get_item_amount, ":old_amount", ":selected_troop", ":old_slot"),
      (try_end),
      (try_begin),
        (ge, ":new_slot", 10),
        (troop_get_inventory_slot, ":new_item", "trp_player", ":new_slot"),
        (troop_get_inventory_slot_modifier, ":new_imod", "trp_player", ":new_slot"),
        (troop_inventory_slot_get_item_amount, ":new_amount", "trp_player", ":new_slot"),
      (else_try),
        (troop_get_inventory_slot, ":new_item", ":selected_troop", ":new_slot"),
        (troop_get_inventory_slot_modifier, ":new_imod", ":selected_troop", ":new_slot"),
        (troop_inventory_slot_get_item_amount, ":new_amount", ":selected_troop", ":new_slot"),
      (try_end),

      (try_begin),
        (ge, ":old_slot", 10),
        (assign, ":old_troop", "trp_player"),
      (else_try),
        (assign, ":old_troop", ":selected_troop"),
      (try_end),
      (try_begin),
        (ge, ":new_slot", 10),
        (assign, ":new_troop", "trp_player"),
      (else_try),
        (assign, ":new_troop", ":selected_troop"),
      (try_end),

      (troop_set_inventory_slot, ":new_troop", ":new_slot", ":old_item"),
      (troop_set_inventory_slot_modifier, ":new_troop", ":new_slot", ":old_imod"),
      (try_begin),
        (gt, ":old_amount", 0),
        (troop_inventory_slot_set_item_amount, ":new_troop", ":new_slot", ":old_amount"),
      (try_end),
      (try_begin),
        (eq, ":new_item", -1),
        (troop_set_inventory_slot, ":old_troop", ":old_slot", -1),
      (else_try),
        (troop_set_inventory_slot, ":old_troop", ":old_slot", ":new_item"),
        (troop_set_inventory_slot_modifier, ":old_troop", ":old_slot", ":new_imod"),
        (try_begin),
          (gt, ":new_amount", 0),
          (troop_inventory_slot_set_item_amount, ":old_troop", ":old_slot", ":new_amount"),
        (try_end),
      (try_end),
    ])
]
