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

multiplayer_display_available_items_for_troop_and_item_classes_scripts = [
#script_multiplayer_display_available_items_for_troop_and_item_classes
# Input: arg1 = troop_no, arg2 = item_classes_begin, arg3 = item_classes_end, arg4 = pos_x_begin, arg5 = pos_y_begin
# Output: none
("multiplayer_display_available_items_for_troop_and_item_classes",
   [
     (store_script_param, ":troop_no", 1),
     (store_script_param, ":item_classes_begin", 2),
     (store_script_param, ":item_classes_end", 3),
     (store_script_param, ":pos_x_begin", 4),
     (store_script_param, ":pos_y_begin", 5),

     (assign, ":x_adder", 100),
     (try_begin),
       (gt, ":pos_x_begin", 500),
       (assign, ":x_adder", -100),
     (try_end),

     (store_sub, ":item_troop_slot", ":troop_no", multiplayer_troops_begin),
     (val_add, ":item_troop_slot", slot_item_multiplayer_availability_linked_list_begin),

     (try_for_range, ":cur_slot", multi_data_item_button_indices_begin, multi_data_item_button_indices_end),
       (troop_set_slot, "trp_multiplayer_data", ":cur_slot", -1),
     (try_end),

     (assign, ":num_available_items", 0),

     (try_for_range, ":item_no", all_items_begin, all_items_end),
       (item_get_slot, ":item_class", ":item_no", slot_item_multiplayer_item_class),
       (is_between, ":item_class", ":item_classes_begin", ":item_classes_end"),
       (this_or_next|eq, "$g_multiplayer_disallow_ranged_weapons", 0),
       (neg|is_between, ":item_class", multi_item_class_type_ranged_weapons_begin, multi_item_class_type_ranged_weapons_end),
       (item_slot_ge, ":item_no", ":item_troop_slot", 1),
       (store_add, ":cur_slot_index", ":num_available_items", multi_data_item_button_indices_begin),
       #using the result array for item_ids
       (troop_set_slot, "trp_multiplayer_data", ":cur_slot_index", ":item_no"),
       (val_add, ":num_available_items", 1),
     (try_end),

     #sorting
     (store_add, ":item_slots_end", ":num_available_items", multi_data_item_button_indices_begin),
     (store_sub, ":item_slots_end_minus_one", ":item_slots_end", 1),
     (try_for_range, ":cur_slot", multi_data_item_button_indices_begin, ":item_slots_end_minus_one"),
       (store_add, ":cur_slot_2_begin", ":cur_slot", 1),
       (try_for_range, ":cur_slot_2", ":cur_slot_2_begin", ":item_slots_end"),
         (troop_get_slot, ":item_1", "trp_multiplayer_data", ":cur_slot"),
         (troop_get_slot, ":item_2", "trp_multiplayer_data", ":cur_slot_2"),
         (call_script, "script_multiplayer_get_item_value_for_troop", ":item_1", ":troop_no"),
         (assign, ":item_1_point", reg0),
         (call_script, "script_multiplayer_get_item_value_for_troop", ":item_2", ":troop_no"),
         (assign, ":item_2_point", reg0),
         (item_get_slot, ":item_1_class", ":item_1", slot_item_multiplayer_item_class),
         (item_get_slot, ":item_2_class", ":item_2", slot_item_multiplayer_item_class),
         (val_mul, ":item_1_class", 1000000), #assuming maximum item price is 1000000
         (val_mul, ":item_2_class", 1000000), #assuming maximum item price is 1000000
         (val_add, ":item_1_point", ":item_1_class"),
         (val_add, ":item_2_point", ":item_2_class"),
         (lt, ":item_2_point", ":item_1_point"),
         (troop_set_slot, "trp_multiplayer_data", ":cur_slot", ":item_2"),
         (troop_set_slot, "trp_multiplayer_data", ":cur_slot_2", ":item_1"),
       (try_end),
     (try_end),

     (troop_get_slot, ":last_item_no", "trp_multiplayer_data", multi_data_item_button_indices_begin),
     (assign, ":num_item_classes", 0),
     (try_begin),
       (ge, ":last_item_no", 0),
       (item_get_slot, ":last_item_class", ":last_item_no", slot_item_multiplayer_item_class),

       (try_for_range, ":cur_slot", multi_data_item_button_indices_begin, ":item_slots_end"),
         (troop_get_slot, ":item_no", "trp_multiplayer_data", ":cur_slot"),
         (item_get_slot, ":item_class", ":item_no", slot_item_multiplayer_item_class),
         (neq, ":item_class", ":last_item_class"),
         (val_add, ":num_item_classes", 1),
         (assign, ":last_item_class", ":item_class"),
       (try_end),

       (try_begin),
         (store_mul, ":required_y", ":num_item_classes", 100),
         (gt, ":required_y", ":pos_y_begin"),
         (store_sub, ":dif", ":required_y", ":pos_y_begin"),
         (val_div, ":dif", 100),
         (val_add, ":dif", 1),
         (val_mul, ":dif", 100),
         (val_add, ":pos_y_begin", ":dif"),
       (try_end),

       (item_get_slot, ":last_item_class", ":last_item_no", slot_item_multiplayer_item_class),
     (try_end),
     (assign, ":cur_x", ":pos_x_begin"),
     (assign, ":cur_y", ":pos_y_begin"),
     (try_for_range, ":cur_slot", multi_data_item_button_indices_begin, ":item_slots_end"),
       (troop_get_slot, ":item_no", "trp_multiplayer_data", ":cur_slot"),
       (item_get_slot, ":item_class", ":item_no", slot_item_multiplayer_item_class),
       (try_begin),
         (neq, ":item_class", ":last_item_class"),
         (val_sub, ":cur_y", 100),
         (assign, ":cur_x", ":pos_x_begin"),
         (assign, ":last_item_class", ":item_class"),
       (try_end),
       (create_image_button_overlay, ":cur_obj", "mesh_mp_inventory_choose", "mesh_mp_inventory_choose"),
       (position_set_x, pos1, 800),
       (position_set_y, pos1, 800),
       (overlay_set_size, ":cur_obj", pos1),
       (position_set_x, pos1, ":cur_x"),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, ":cur_obj", pos1),
       (create_mesh_overlay_with_item_id, reg0, ":item_no"),
       (store_add, ":item_x", ":cur_x", 50),
       (store_add, ":item_y", ":cur_y", 50),
       (position_set_x, pos1, ":item_x"),
       (position_set_y, pos1, ":item_y"),
       (overlay_set_position, reg0, pos1),
       (val_add, ":cur_x", ":x_adder"),
     (try_end),
     ])
]
