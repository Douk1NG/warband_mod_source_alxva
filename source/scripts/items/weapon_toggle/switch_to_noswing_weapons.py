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

switch_to_noswing_weapons_scripts = [
("switch_to_noswing_weapons", [
      (store_script_param, ":agent", 1),
      (store_script_param, ":formation_spacing", 2),
      (try_for_range, ":item_slot", ek_item_0, ek_head),
        (agent_get_item_slot, ":item", ":agent", ":item_slot"),
        (call_script, "script_cf_is_thrusting_weapon", ":item"),
        (item_get_weapon_length, ":weap_len",":item"),

        (try_begin),
          (ge, ":weap_len", ":formation_spacing"),	#avoid switching when weapon still has room to be swung
          (item_get_slot, ":noswing_version", ":item", slot_item_alternate),
          (gt, ":noswing_version", "itm_items_end"),
          (agent_unequip_item, ":agent", ":item", ":item_slot"),	#assumes first ek_* are the weapons
          (agent_equip_item, ":agent", ":noswing_version", ":item_slot"),	#assumes first ek_* are the weapons

        #undo legacy switches
        (else_try),
          (gt, ":item", "itm_items_end"),
          (item_get_slot, ":original_version", ":item", slot_item_alternate),
          (agent_unequip_item, ":agent", ":item", ":item_slot"),	#assumes first ek_* are the weapons
          (agent_equip_item, ":agent", ":original_version", ":item_slot"),	#assumes first ek_* are the weapons
        (try_end),
      (try_end),])
]
