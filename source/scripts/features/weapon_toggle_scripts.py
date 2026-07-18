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

def make_noswing_weapons(items):
    noswing_weapons = []
    for i_item in xrange(len(items)):
        noswing_name = 'noswing_' + items[i_item][0]
        i_noswing = find_object(items, noswing_name)
        if i_noswing > -1:
            noswing_weapons.append((item_set_slot, i_item, slot_item_alternate, i_noswing))
            noswing_weapons.append((item_set_slot, i_noswing, slot_item_alternate, i_item))
    return noswing_weapons[:]

weapon_toggle_scripts = [

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
    ]),
    
  ("all_toggle_weapons_set",
    [
      (store_script_param, ":strict_mode", 1),
    
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":cur_hero", "p_main_party", ":i_stack"),
        (troop_is_hero, ":cur_hero"),
        (troop_get_slot, ":troop_weapons_set_no", ":cur_hero", slot_troop_weapons_set_no),
        (call_script, "script_get_num_equiped_weapons_of_troop", ":cur_hero"),
        (assign, ":num_weapons", reg0),
        (call_script, "script_get_num_backup_weapons_of_troop", ":cur_hero"),
        (assign, ":num_backup_weapons", reg0),
        (try_begin),
          (neq, ":troop_weapons_set_no", "$g_weapons_set_no"),
          (try_begin),
            (this_or_next|gt, ":num_backup_weapons", 0),
            (this_or_next|eq, ":num_weapons", 0),
            (eq, ":strict_mode", 1),
            (call_script, "script_hero_toggle_weapons_set", ":cur_hero"),
          (try_end),
        (else_try),
            (gt, ":num_backup_weapons", 0),
            (eq, ":num_weapons", 0),
            (eq, ":strict_mode", 0),
            (call_script, "script_hero_toggle_weapons_set", ":cur_hero"),
        (try_end),
      (try_end),
    ]),
    
  ("get_num_equiped_weapons_of_troop", 
    [
      (store_script_param, ":troop_no", 1),
      
      (assign, ":num_weapons", 0),
      (try_for_range, ":cur_weapon_slot", ek_item_0, ek_head),
        (troop_get_inventory_slot, ":cur_weapon", ":troop_no", ":cur_weapon_slot"),
        (gt, ":cur_weapon", -1),
        (val_add, ":num_weapons", 1),
      (try_end),
      (assign, reg0, ":num_weapons"),
    ]),
    
  ("get_num_backup_weapons_of_troop", 
    [
      (store_script_param, ":troop_no", 1),
      
      (assign, ":num_backup_weapons", 0),
      (try_for_range, ":cur_2nd_weapon_slot", slot_2nd_weapons_1, slot_2nd_weapons_4+1),
        (troop_get_slot, ":cur_2nd_weapon_with_modifier", ":troop_no", ":cur_2nd_weapon_slot"),
        (gt, ":cur_2nd_weapon_with_modifier", 0),
        (val_add, ":num_backup_weapons", 1),
      (try_end),
      (assign, reg0, ":num_backup_weapons"),
    ]),

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
      (try_end),]),

("switch_from_noswing_weapons", [
      (store_script_param, ":agent", 1),
      (try_for_range, ":item_slot", ek_item_0, ek_head),
        (agent_get_item_slot, ":item", ":agent", ":item_slot"),
        (gt, ":item", "itm_items_end"),
        (item_get_slot, ":original_version", ":item", slot_item_alternate),
        (agent_unequip_item, ":agent", ":item", ":item_slot"),	#assumes first ek_* are the weapons
        (agent_equip_item, ":agent", ":original_version", ":item_slot"),	#assumes first ek_* are the weapons
      (try_end),]),

("init_noswing_weapons", make_noswing_weapons(items)),
]
