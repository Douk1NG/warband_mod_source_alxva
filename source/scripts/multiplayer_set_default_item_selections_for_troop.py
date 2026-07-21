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

multiplayer_set_default_item_selections_for_troop_scripts = [
#script_multiplayer_set_default_item_selections_for_troop
# Input: arg1 = troop_no
# Output: none
("multiplayer_set_default_item_selections_for_troop",
   [
     (store_script_param, ":troop_no", 1),
     (multiplayer_get_my_player, ":my_player_no"),
     (call_script, "script_multiplayer_clear_player_selected_items", ":my_player_no"),
     (assign, ":cur_weapon_slot", 0),
     (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
     (try_for_range, ":i_slot", 0, ":inv_cap"),
       (troop_get_inventory_slot, ":item_id", ":troop_no", ":i_slot"),
       (ge, ":item_id", 0),
       (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
       (try_begin),
         (is_between, ":item_class", multi_item_class_type_weapons_begin, multi_item_class_type_weapons_end),
         (this_or_next|eq, "$g_multiplayer_disallow_ranged_weapons", 0),
         (neg|is_between, ":item_class", multi_item_class_type_ranged_weapons_begin, multi_item_class_type_ranged_weapons_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, ":cur_weapon_slot"),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
         (val_add, ":cur_weapon_slot", 1),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_heads_begin, multi_item_class_type_heads_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 4),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_bodies_begin, multi_item_class_type_bodies_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 5),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_feet_begin, multi_item_class_type_feet_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 6),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_gloves_begin, multi_item_class_type_gloves_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 7),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_horses_begin, multi_item_class_type_horses_end),
         (eq, "$g_horses_are_avaliable", 1),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 8),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (try_end),
     (try_end),
     ])
]
