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

multiplayer_buy_agent_equipment_scripts = [
#script_multiplayer_buy_agent_equipment
# Input: arg1 = player_no
# Output: none
("multiplayer_buy_agent_equipment",
   [
     (store_script_param, ":player_no", 1),
     (player_get_troop_id, ":player_troop", ":player_no"),
     (player_get_gold, ":player_gold", ":player_no"),
     (player_get_slot, ":added_gold", ":player_no", slot_player_last_rounds_used_item_earnings),
     (player_set_slot, ":player_no", slot_player_last_rounds_used_item_earnings, 0),
     (val_add, ":player_gold", ":added_gold"),
     (assign, ":armor_bought", 0),

     #moving original values to temp slots
     (try_for_range, ":i_item", slot_player_selected_item_indices_begin, slot_player_selected_item_indices_end),
       (player_get_slot, ":selected_item_index", ":player_no", ":i_item"),
       (store_sub, ":i_cur_selected_item", ":i_item", slot_player_selected_item_indices_begin),
       (try_begin),
         (player_item_slot_is_picked_up, ":player_no", ":i_cur_selected_item"),
         (assign, ":selected_item_index", -1),
       (try_end),
       (val_add, ":i_cur_selected_item", slot_player_cur_selected_item_indices_begin),
       (player_set_slot, ":player_no", ":i_cur_selected_item", ":selected_item_index"),
     (try_end),
     (assign, ":end_cond", 1000),
     (try_for_range, ":unused", 0, ":end_cond"),
       (call_script, "script_multiplayer_calculate_cur_selected_items_cost", ":player_no", 0),
       (assign, ":total_cost", reg0),
       (try_begin),
         (gt, ":total_cost", ":player_gold"),
         #downgrade one of the selected items
         #first normalize the prices
         #then prioritize some of the weapon classes for specific troop classes
         (call_script, "script_multiplayer_get_troop_class", ":player_troop"),
         (assign, ":player_troop_class", reg0),

         (assign, ":max_cost_value", 0),
         (assign, ":max_cost_value_index", -1),
         (try_for_range, ":i_item", slot_player_cur_selected_item_indices_begin, slot_player_cur_selected_item_indices_end),
           (player_get_slot, ":item_id", ":player_no", ":i_item"),
           (ge, ":item_id", 0), #might be -1 for horses etc.
           (call_script, "script_multiplayer_get_item_value_for_troop", ":item_id", ":player_troop"),
           (assign, ":item_value", reg0),
           (store_sub, ":item_type", ":i_item", slot_player_cur_selected_item_indices_begin),
           (try_begin), #items
             (this_or_next|eq, ":item_type", 0),
             (this_or_next|eq, ":item_type", 1),
             (this_or_next|eq, ":item_type", 2),
             (eq, ":item_type", 3),
             (val_mul, ":item_value", 5),
           (else_try), #head
             (eq, ":item_type", 4),
             (val_mul, ":item_value", 4),
           (else_try), #body
             (eq, ":item_type", 5),
             (val_mul, ":item_value", 2),
           (else_try), #foot
             (eq, ":item_type", 6),
             (val_mul, ":item_value", 8),
           (else_try), #gloves
             (eq, ":item_type", 7),
             (val_mul, ":item_value", 8),
           (else_try), #horse
             #base value (most expensive)
           (try_end),
           (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
           (try_begin),
             (eq, ":player_troop_class", multi_troop_class_infantry),
             (this_or_next|eq, ":item_class", multi_item_class_type_sword),
             (this_or_next|eq, ":item_class", multi_item_class_type_axe),
             (this_or_next|eq, ":item_class", multi_item_class_type_blunt),
             (this_or_next|eq, ":item_class", multi_item_class_type_war_picks),
             (this_or_next|eq, ":item_class", multi_item_class_type_two_handed_sword),
             (this_or_next|eq, ":item_class", multi_item_class_type_small_shield),
             (eq, ":item_class", multi_item_class_type_two_handed_axe),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_spearman),
             (this_or_next|eq, ":item_class", multi_item_class_type_spear),
             (eq, ":item_class", multi_item_class_type_large_shield),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_cavalry),
             (this_or_next|eq, ":item_class", multi_item_class_type_lance),
             (this_or_next|eq, ":item_class", multi_item_class_type_sword),
             (eq, ":item_class", multi_item_class_type_horse),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_archer),
             (this_or_next|eq, ":item_class", multi_item_class_type_bow),
             (eq, ":item_class", multi_item_class_type_arrow),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_crossbowman),
             (this_or_next|eq, ":item_class", multi_item_class_type_crossbow),
             (eq, ":item_class", multi_item_class_type_bolt),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_mounted_archer),
             (this_or_next|eq, ":item_class", multi_item_class_type_bow),
             (this_or_next|eq, ":item_class", multi_item_class_type_arrow),
             (eq, ":item_class", multi_item_class_type_horse),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_mounted_crossbowman),
             (this_or_next|eq, ":item_class", multi_item_class_type_crossbow),
             (this_or_next|eq, ":item_class", multi_item_class_type_bolt),
             (eq, ":item_class", multi_item_class_type_horse),
             (val_div, ":item_value", 2),
           (try_end),

           (try_begin),
             (gt, ":item_value", ":max_cost_value"),
             (assign, ":max_cost_value", ":item_value"),
             (assign, ":max_cost_value_index", ":i_item"),
           (try_end),
         (try_end),

         #max_cost_value and max_cost_value_index will definitely be valid
         #unless no items are left (therefore some items must cost 0 gold)
         (player_get_slot, ":item_id", ":player_no", ":max_cost_value_index"),
         (call_script, "script_multiplayer_get_previous_item_for_item_and_troop", ":item_id", ":player_troop"),
         (assign, ":item_id", reg0),
         (player_set_slot, ":player_no", ":max_cost_value_index", ":item_id"),
       (else_try),
         (assign, ":end_cond", 0),
         (val_sub, ":player_gold", ":total_cost"),
         (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
         (try_for_range, ":i_item", slot_player_cur_selected_item_indices_begin, slot_player_cur_selected_item_indices_end),
           (player_get_slot, ":item_id", ":player_no", ":i_item"),
           #checking if different class default item replace is needed for weapons
           (try_begin),
             (ge, ":item_id", 0),
             #then do nothing
           (else_try),
             (store_sub, ":base_index_slot", ":i_item", slot_player_cur_selected_item_indices_begin),
             (store_add, ":selected_item_index_slot", ":base_index_slot", slot_player_selected_item_indices_begin),
             (player_get_slot, ":selected_item_index", ":player_no", ":selected_item_index_slot"),
             (this_or_next|eq, ":selected_item_index", -1),
             (player_item_slot_is_picked_up, ":player_no", ":base_index_slot"),
             #then do nothing
           (else_try),
             #an item class without a default value is -1, then find a default weapon
             (item_get_slot, ":item_class", ":selected_item_index", slot_item_multiplayer_item_class),
             (is_between, ":item_class", multi_item_class_type_weapons_begin, multi_item_class_type_weapons_end),
             (assign, ":dc_replaced_item", -1),
             (try_for_range, ":i_dc_item_class", multi_item_class_type_melee_weapons_begin, multi_item_class_type_melee_weapons_end),
               (lt, ":dc_replaced_item", 0),
               (assign, ":dc_item_class_used", 0),
               (try_for_range, ":i_dc_item", slot_player_cur_selected_item_indices_begin, slot_player_cur_selected_item_indices_end),
                 (player_get_slot, ":dc_cur_item", ":player_no", ":i_dc_item"),
                 (ge, ":dc_cur_item", 0),
                 (item_get_slot, ":dc_item_class", ":dc_cur_item", slot_item_multiplayer_item_class),
                 (eq, ":dc_item_class", ":i_dc_item_class"),
                 (assign, ":dc_item_class_used", 1),
               (try_end),
               (eq, ":dc_item_class_used", 0),
               (assign, ":dc_end_cond", all_items_end),
               (try_for_range, ":i_dc_new_item", all_items_begin, ":dc_end_cond"),
                 (item_slot_eq, ":i_dc_new_item", slot_item_multiplayer_item_class, ":i_dc_item_class"),
                 (call_script, "script_cf_multiplayer_is_item_default_for_troop", ":i_dc_new_item", ":player_troop"),
                 (assign, ":dc_end_cond", 0), #break
                 (assign, ":dc_replaced_item", ":i_dc_new_item"),
               (try_end),
             (try_end),
             (ge, ":dc_replaced_item", 0),
             (player_set_slot, ":player_no", ":i_item", ":dc_replaced_item"),
             (assign, ":item_id", ":dc_replaced_item"),
           (try_end),

           #finally, add the item to agent
           (try_begin),
             (ge, ":item_id", 0), #might be -1 for horses etc.
             (store_sub, ":item_slot", ":i_item", slot_player_cur_selected_item_indices_begin),
             (player_add_spawn_item, ":player_no", ":item_slot", ":item_id"),
             (try_begin),
               (eq, ":item_slot", ek_body), #ek_body is the slot for armor
               (assign, ":armor_bought", 1),
             (try_end),
           (try_end),
         (try_end),

         (player_set_slot, ":player_no", slot_player_total_equipment_value, ":total_cost"),
       (try_end),
     (try_end),
     (try_begin),
       (eq, ":armor_bought", 0),
       (eq, "$g_multiplayer_force_default_armor", 1),
       (assign, ":end_cond", all_items_end),
       (try_for_range, ":i_new_item", all_items_begin, ":end_cond"),
         (this_or_next|item_slot_eq, ":i_new_item", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
         (this_or_next|item_slot_eq, ":i_new_item", slot_item_multiplayer_item_class, multi_item_class_type_medium_armor),
         (item_slot_eq, ":i_new_item", slot_item_multiplayer_item_class, multi_item_class_type_heavy_armor),
         (call_script, "script_cf_multiplayer_is_item_default_for_troop", ":i_new_item", ":player_troop"),
         (assign, ":end_cond", 0), #break
         (player_add_spawn_item, ":player_no", ek_body, ":i_new_item"), #ek_body is the slot for armor
       (try_end),
     (try_end),
     ])
]
